"""Pre-publish safety scan (2026-10-24, after the trailer v1 leak).
Reads every on-screen word of a video (OCR on a frame every 0.25 s, contrast-stretched so faint
background text is caught too) plus any caption/spec text files, and FAILS on:
  - banned words from the private list (owner identity, employer, account details, size claims)
  - any $ figure or % not listed with --allow (allowed = the numbers on the Theo fact sheet)
Usage: safety_scan.py video.mp4 --banned-file <private list.json> [--text file ...] [--allow '$100' '$99' ...]
(or set RE_BANNED_FILE). The list lives ONLY in Database · Posts settings/privacy; fetch it to a temp file outside the repo.
Exit 0 = clean, 1 = blocked (prints each hit with its time).
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
def check(chunks, allow):
    hits = []
    norm_allow = {a.replace(" ", "").lower() for a in allow}
    for where, txt in chunks:
        low = txt.lower()
        for b in BANNED:
            for m in re.finditer(b, low): hits.append((where, "BANNED", m.group(0)))
        for m in MONEY.finditer(txt):
            v = m.group(0).replace(" ", "").lower().rstrip(",")
            if v not in norm_allow: hits.append((where, "NUMBER not on --allow", m.group(0)))
    return hits
if __name__ == "__main__":
    a = sys.argv[1:]; video = a[0]; texts, allow, mode, banned_file, hits_dir = [], [], None, os.environ.get("RE_BANNED_FILE"), None
    for x in a[1:]:
        if x in ("--text", "--allow", "--banned-file", "--hits-dir"): mode = x; continue
        if mode == "--banned-file": banned_file = x; mode = None; continue
        if mode == "--hits-dir": hits_dir = x; mode = None; continue
        (texts if mode == "--text" else allow).append(x)
    load_banned(banned_file)
    chunks = [(f"{t:5.2f}s", s) for t, s in ocr_frames(video)] if video != "-" else []
    chunks += [(os.path.basename(f), open(f).read()) for f in texts]
    hits = check(chunks, allow)
    for h in hits: print("BLOCK", *h)
    if hits_dir: write_hits(hits, hits_dir)
    print("CLEAN" if not hits else f"BLOCKED: {len(hits)} hit(s)"); sys.exit(1 if hits else 0)
