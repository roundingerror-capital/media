"""Kit's library pieces as they play on the canvas (V3.01: most pieces are animated: plants sway, screens flicker, neon buzzes).
Each board (e.g. MON-01.dc.html, PLT-03.dc.html, LIBOFFICE.dc.html) has an '<Name> at actual size' svg; we capture it in Chromium
at 10 fps over one loop and cache the frames as PNGs, then serve the frame for any time t.

    import kitpieces as K
    im = K.piece("MON-01", t)                         # first '... at actual size' svg on the board, trimmed to its drawing
    im = K.piece("LIBOFFICE", t, "Desk phone, coiled cord")
Assets: RE_ASSETS_DIR (local copy of Assets Designs project files). Cache: RE_PIECE_CACHE."""
import os, re, glob
from PIL import Image
from board_capture import capture
ASSETS = os.environ.get("RE_ASSETS_DIR", "/tmp/claude-0/-home-claude/97ad6b31-1277-5795-987d-0d7c1b8393c4/scratchpad/assets3/project")
CACHE = os.environ.get("RE_PIECE_CACHE", "/home/claude/out/piececache")
_MEM = {}

def frames(board, name=None, dur=None, fps=10):
    key = (board, name)
    if key in _MEM: return _MEM[key]
    path = board if board.endswith(".dc.html") else os.path.join(ASSETS, board + ".dc.html"); html = open(path, encoding="utf-8").read()
    import html as _h
    labels = [_h.unescape(l) for l in re.findall(r'aria-label="([^"]+)"', html) if l.endswith("actual size")]
    nth = ""
    if name and "#" in name: name, nth = name.rsplit("#", 1); nth = "#" + nth          # "Label#2": the 2nd board with that label
    label = next((l for l in labels if name is None or l.startswith(name)), None)
    if label is None: raise KeyError(f"{board}: no '{name} at actual size'")
    label = label + nth
    if dur is None:
        ds = [float(x) for x in re.findall(r'animation:[^;"]*?([\d.]+)s', html)]; dur = min(4.0, max(ds)) if ds else 0.1
    d = os.path.join(CACHE, re.sub(r"[^A-Za-z0-9]+", "_", f"{os.path.basename(board)}_{label}")); os.makedirs(d, exist_ok=True)
    n = max(1, int(round(dur * fps)))
    have = sorted(glob.glob(os.path.join(d, "f*.png")))
    if len(have) != n:
        ims = capture(path, label.split(" at actual size")[0], [i / fps + 0.02 for i in range(n)], scale=1) if False else \
              capture(path, label.replace(" at actual size", "") if nth else label, [i / fps + 0.02 for i in range(n)], scale=1)
        for i, im in enumerate(ims): im.save(os.path.join(d, f"f{i:03d}.png"))
        have = sorted(glob.glob(os.path.join(d, "f*.png")))
    ims = [Image.open(f).convert("RGBA") for f in have]
    bbs = [i.getbbox() for i in ims if i.getbbox()]
    if bbs:
        bb = (min(b[0] for b in bbs), min(b[1] for b in bbs), max(b[2] for b in bbs), max(b[3] for b in bbs)); ims = [i.crop(bb) for i in ims]
    _MEM[key] = ims; return ims

def piece(board, t, name=None, fps=10):
    fr = frames(board, name); return fr[int(t * fps) % len(fr)]
