"""Pre-publish safety scan (2026-10-24, after the trailer v1 leak).
Reads every on-screen word of a video (OCR on a frame every 0.25 s, contrast-stretched so faint
background text is caught too) plus any caption/spec text files, and FAILS on:
  - banned words from the private list (owner identity, employer, account details, size claims)
  - any $ figure or % not listed with --allow (allowed = the numbers on the Theo fact sheet)
Usage: safety_scan.py video.mp4 --banned-file <private list.json> [--text file ...] [--allow '$100' '$99' ...]
(or set RE_BANNED_FILE). The list lives ONLY in Database · Posts settings/privacy; fetch it to a temp file outside the repo.
Exit 0 = clean, 1 = blocked (prints each hit with its time).
T-111 (2026-11-13): a NUMBER read in a VIDEO frame blocks only when the same token is read in 3 frames in a row (0.75 s)
  and it is not a near-match of an allowed figure (near_allowed) or a garbled echo of one read correctly in the same frame (echo_of). Fading, shaking or sliding text reads differently every
  frame and drops out. Unchanged: private-list hits on every frame and text, and exact matching for caption/title/description
  text. --strict = the old rule (every frame, exact match), for comparing.
--hits-dir DIR (T-103, the boss 2026-11-05: "put the frame with the issue ... a red box ... so I can click ignore"):
  also writes DIR/hits.json and, for each NUMBER hit in the video, DIR/<id>.jpg = that frame (360 px wide) with a red box
  around what was read. Hits of the same figure less than 0.6 s apart are grouped into one. Private-list (BANNED) hits get
  NO frame and NO text in hits.json (kind "private", time or file only): those are never shown, only fixed."""
import sys, os, re, subprocess, tempfile, glob
from PIL import Image, ImageOps
BANNED = []  # loaded at run time from a PRIVATE list (Database · Posts settings/privacy), never stored in this public repo
def load_banned(path):
    import json
    if not path or not os.path.exists(path):
        print("BLOCKED: no private banned list given (--banned-file); refusing to scan without it"); sys.exit(2)
    d = json.load(open(path)); pats = d.get("banned_patterns", d) if isinstance(d, dict) else d
    BANNED[:] = list(pats)
MONEY = re.compile(r"[$]\s?\d[\d,]*(\.\d+)?|\b\d+(\.\d+)?\s?%")
def _mask_sprites(im):
    """High-contrast pass only: blank the character band (y 1230-1730 at 1080x1920), where tools/daily.py draws the
    pixel-art mascots. Their glasses and eyes read as '6%' (2026-10-26 false positives that held the HOOD preview).
    The normal-contrast pass still reads that band, so real text there (bubbles, the end card) is still scanned."""
    from PIL import ImageDraw
    im = im.copy(); h = im.height; ImageDraw.Draw(im).rectangle([0, int(h * 1230 / 1920), im.width, int(h * 1730 / 1920)], fill=255); return im
def ocr_frames(video, step=0.25):
    d = tempfile.mkdtemp()
    subprocess.run(["ffmpeg", "-v", "error", "-i", video, "-vf", f"fps={1/step},scale=1080:-1", os.path.join(d, "f%05d.png")], check=True)
    out = []
    FRAMES.clear()
    for p in sorted(glob.glob(os.path.join(d, "f*.png"))):
        t = (int(os.path.basename(p)[1:6]) - 1) * step
        g = Image.open(p).convert("L"); txt = ""
        # pass 1: normal contrast; pass 2: anything not near-black becomes ink, so faint background text is read too
        for k, im in enumerate((ImageOps.invert(ImageOps.autocontrast(g, cutoff=1)), _mask_sprites(g.point(lambda v: 0 if v > 34 else 255)))):
            q = p[:-4] + f"_{k}.png"; im.save(q)
            txt += subprocess.run(["tesseract", q, "-", "--psm", "11"], capture_output=True, text=True).stdout + "\n"
        out.append((t, txt)); FRAMES[f"{t:5.2f}s"] = p
    return out
FRAMES = {}  # "  0.75s" -> the 1080-wide frame png (for --hits-dir)
def _boxes(png, token):
    """Where tesseract read `token` on this frame (both passes, word boxes from TSV). Returns [(x0,y0,x1,y1)]."""
    want = re.sub(r"[^0-9]", "", token); found = []
    for q in (png[:-4] + "_0.png", png[:-4] + "_1.png"):
        if not os.path.exists(q): continue
        tsv = subprocess.run(["tesseract", q, "-", "--psm", "11", "tsv"], capture_output=True, text=True).stdout.splitlines()[1:]
        for row in tsv:
            c = row.split("\t")
            if len(c) < 12 or not c[11].strip(): continue
            d = re.sub(r"[^0-9]", "", c[11])
            if want and d and (want in d or (len(d) >= 2 and d in want)):
                x, y, w, h = map(int, c[6:10]); found.append((x, y, x + w, y + h))
    return found
def write_hits(hits, out_dir):
    import json
    from PIL import ImageDraw
    os.makedirs(out_dir, exist_ok=True)
    groups = []
    for where, kind, tok in hits:
        is_t = where.endswith("s") and where.strip()[:-1].replace(".", "").isdigit()
        if kind == "BANNED":
            groups.append({"kind": "private", ("t" if is_t else "field"): (float(where.strip()[:-1]) if is_t else where)}); continue
        if not is_t:
            groups.append({"kind": "text_number", "field": where, "token": tok.strip()}); continue
        t = float(where.strip()[:-1]); key = re.sub(r"\s", "", tok)
        g = next((g for g in groups if g.get("kind") == "number" and g["key"] == key and t - g["t_end"] <= 0.6), None)
        if g: g["t_end"] = t; continue
        groups.append({"kind": "number", "t": t, "t_end": t, "token": tok.strip(), "key": key, "where": where})
    for i, g in enumerate(groups, 1):
        g["id"] = f"h{i}"
        if g["kind"] != "number": continue
        png = FRAMES.get(g.pop("where")); g.pop("key")
        if not png: continue
        im = Image.open(png).convert("RGB"); bx = _boxes(png, g["token"]); dr = ImageDraw.Draw(im)
        for (x0, y0, x1, y1) in bx:
            for k in range(10): dr.rectangle([x0 - 14 - k, y0 - 14 - k, x1 + 14 + k, y1 + 14 + k], outline=(255, 40, 40) if k > 2 else (255, 255, 255))
        g["boxed"] = bool(bx)
        im.thumbnail((360, 640)); g["frame"] = f"{g['id']}.jpg"; im.save(os.path.join(out_dir, g["frame"]), quality=62)
    for g in groups: g.pop("key", None); g.pop("where", None)
    json.dump(groups, open(os.path.join(out_dir, "hits.json"), "w"), indent=1)
STABLE_FRAMES = 3  # T-111 (a): a video number counts only when the same token is read in 3 frames in a row (0.75 s at 4 fps)
def _norm(tok): return tok.replace(" ", "").lower().rstrip(",")
def _digits(v): return re.sub(r"[^0-9]", "", v)
def _lev(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1): cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]
def near_allowed(v, norm_allow):
    """T-111 (b): an OCR misread of a figure that IS on the allow list. Same kind ($ or %), and one of:
    the same digits ('$1,00' ~ '$1.00', '072%' ~ '0.72%'); one digit string inside the other, at least 2 digits,
    at most 2 extra ('$4115' ~ '$115', '$67' ~ '$67.50'); or, for figures of 3+ digits, 1 character changed
    (2 for 5+ digits: '$90.24' ~ '$90.21'). One- and two-digit figures never match by edit: '12%' is not '13%'."""
    kind = "$" if v.startswith("$") else "%"; dv = _digits(v)
    if not dv: return False
    for a in norm_allow:
        if ("$" if a.startswith("$") else "%") != kind: continue
        da = _digits(a)
        if not da: continue
        if dv == da: return True
        sh, lg = (dv, da) if len(dv) <= len(da) else (da, dv)
        if len(sh) >= 2 and sh in lg and len(lg) - len(sh) <= 2: return True
        if min(len(dv), len(da)) >= 3 and _lev(v, a) <= (2 if min(len(dv), len(da)) >= 5 else 1): return True
    return False
_CONF = {frozenset("68"), frozenset("38"), frozenset("08"), frozenset("17"), frozenset("56")}  # digit pairs OCR swaps
def echo_of(v, present):
    """T-111 (b2): the scan reads every frame twice (normal and high contrast). When one pass reads an allowed figure
    correctly, the other pass often garbles the SAME text. v is an echo when an allowed figure that IS read exactly in this
    frame (present) starts with v's digits ('$6' or '$6,' beside '$6,750'; '$67' beside '$67.50'), or when v equals that
    figure's leading group (the digits before its first , or .) with one look-alike digit swapped ('$87' beside '$67.50')."""
    kind = "$" if v.startswith("$") else "%"; dv = _digits(v)
    if not dv: return False
    for a in present:
        if ("$" if a.startswith("$") else "%") != kind: continue
        da = _digits(a)
        if len(dv) < len(da) and da.startswith(dv): return True
        lead = _digits(re.split(r"[.,]", a.lstrip("$"))[0])
        if len(lead) >= 2 and len(dv) == len(lead) and len(da) > len(lead):
            diff = [(x, y) for x, y in zip(dv, lead) if x != y]
            if len(diff) == 1 and frozenset(diff[0]) in _CONF: return True
    return False
STATS = {"unstable": 0, "near": 0, "echo": 0}
def check(chunks, allow, strict=False):
    """chunks = [(where, text)], video frames first in time order (where like ' 0.75s'), then text files.
    Private-list (BANNED) hits: every frame and every text, always. Number hits in text files: exact allow list, always.
    Number hits in video frames (T-111, the boss 2026-11-13 "I don't want to keep having to review these false positives"):
    only a token that is STABLE (same token in STABLE_FRAMES consecutive frames) and not a near-match of an allowed figure.
    strict=True is the old behaviour (every frame, exact match)."""
    hits = []
    norm_allow = {_norm(a) for a in allow}
    STATS["unstable"] = STATS["near"] = STATS["echo"] = 0
    is_frame = lambda w: w.endswith("s") and w.strip()[:-1].replace(".", "").isdigit()
    frames = [i for i, (w, _) in enumerate(chunks) if is_frame(w)]
    toks = {i: [(m.group(0), _norm(m.group(0))) for m in MONEY.finditer(chunks[i][1])] for i in frames}
    sets = [set(v for _, v in toks[i]) for i in frames]
    def stable(k, v):  # frame number k (position in `frames`): is v part of a run of STABLE_FRAMES frames?
        lo = k
        while lo > 0 and v in sets[lo - 1]: lo -= 1
        hi = k
        while hi + 1 < len(sets) and v in sets[hi + 1]: hi += 1
        return hi - lo + 1 >= STABLE_FRAMES
    pos = {i: k for k, i in enumerate(frames)}
    for i, (where, txt) in enumerate(chunks):
        low = txt.lower()
        for b in BANNED:
            for m in re.finditer(b, low): hits.append((where, "BANNED", m.group(0)))
        if i in pos:
            for raw, v in toks[i]:
                if v in norm_allow: continue
                if not strict:
                    if not stable(pos[i], v): STATS["unstable"] += 1; continue
                    if near_allowed(v, norm_allow): STATS["near"] += 1; continue
                    if echo_of(v, sets[pos[i]] & norm_allow): STATS["echo"] += 1; continue
                hits.append((where, "NUMBER not on --allow", raw))
        else:
            for m in MONEY.finditer(txt):
                if _norm(m.group(0)) not in norm_allow: hits.append((where, "NUMBER not on --allow", m.group(0)))
    return hits
if __name__ == "__main__":
    a = sys.argv[1:]; video = a[0]; texts, allow, mode, banned_file, hits_dir = [], [], None, os.environ.get("RE_BANNED_FILE"), None
    strict = "--strict" in a; a = [x for x in a if x != "--strict"]
    for x in a[1:]:
        if x in ("--text", "--allow", "--banned-file", "--hits-dir"): mode = x; continue
        if mode == "--banned-file": banned_file = x; mode = None; continue
        if mode == "--hits-dir": hits_dir = x; mode = None; continue
        (texts if mode == "--text" else allow).append(x)
    load_banned(banned_file)
    chunks = [(f"{t:5.2f}s", s) for t, s in ocr_frames(video)] if video != "-" else []
    chunks += [(os.path.basename(f), open(f).read()) for f in texts]
    hits = check(chunks, allow, strict)
    if not strict and (STATS["unstable"] or STATS["near"] or STATS["echo"]): print(f"skipped as OCR noise: {STATS['unstable']} unstable (under {STABLE_FRAMES} frames in a row), {STATS['near']} near-match of an allowed figure, {STATS['echo']} echo of an allowed figure read in the same frame")
    for h in hits: print("BLOCK", *h)
    if hits_dir: write_hits(hits, hits_dir)
    print("CLEAN" if not hits else f"BLOCKED: {len(hits)} hit(s)"); sys.exit(1 if hits else 0)
