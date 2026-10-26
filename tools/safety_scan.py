"""Pre-publish safety scan (2026-10-24, after the trailer v1 leak).
Reads every on-screen word of a video (OCR on a frame every 0.25 s, contrast-stretched so faint
background text is caught too) plus any caption/spec text files, and FAILS on:
  - banned words: the owner's name, employer, the boss, 'unsupervised', account numbers, size claims
  - any $ figure or % not listed with --allow (allowed = the numbers on the Theo fact sheet)
Usage: safety_scan.py video.mp4 [--text file ...] [--allow '$100' '$99' ...]
Exit 0 = clean, 1 = blocked (prints each hit with its time)."""
import sys, os, re, subprocess, tempfile, glob
from PIL import Image, ImageOps
BANNED = [r"migu[e3]l", r"the boss", r"the boss", r"max\s*chub", r"unsupervised", r"the boss", r"\bagentic\b",
          r"account\s+value", r"contributed", r"fund\s+size", r"\b\d{2,3}\s*k\b", r"\$\s*\d{2,3}\s*k\b", r"\$\s*\d{2,3},\d{3}"]
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
    for p in sorted(glob.glob(os.path.join(d, "f*.png"))):
        t = (int(os.path.basename(p)[1:6]) - 1) * step
        g = Image.open(p).convert("L"); txt = ""
        # pass 1: normal contrast; pass 2: anything not near-black becomes ink, so faint background text is read too
        for k, im in enumerate((ImageOps.invert(ImageOps.autocontrast(g, cutoff=1)), _mask_sprites(g.point(lambda v: 0 if v > 34 else 255)))):
            q = p[:-4] + f"_{k}.png"; im.save(q)
            txt += subprocess.run(["tesseract", q, "-", "--psm", "11"], capture_output=True, text=True).stdout + "\n"
        out.append((t, txt))
    return out
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
    a = sys.argv[1:]; video = a[0]; texts, allow, mode = [], [], None
    for x in a[1:]:
        if x in ("--text", "--allow"): mode = x; continue
        (texts if mode == "--text" else allow).append(x)
    chunks = [(f"{t:5.2f}s", s) for t, s in ocr_frames(video)] if video != "-" else []
    chunks += [(os.path.basename(f), open(f).read()) for f in texts]
    hits = check(chunks, allow)
    for h in hits: print("BLOCK", *h)
    print("CLEAN" if not hits else f"BLOCKED: {len(hits)} hit(s)"); sys.exit(1 if hits else 0)
