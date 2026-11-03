"""Kit's palette swaps (Mascot Designs, 'V2.04 <Name> · palette swaps · 4 ramps (skill 11)') applied to any rig frame.

Each swap board draws the same character five times (current + 4 ramps) with identical rects in identical order, so pairing
rect fills gives an exact colour map current -> swap. Any rig animation runs on any swap (Kit's note on the board).

    import swaps
    swaps.names("kit")                    -> ["Leucistic", "Gold", "Lavender", "Wild"]
    swaps.recolor(img, "kit", "Gold")     -> RGBA with Kit's main material on the Gold ramp
Boards are read from RE_MASCOT_DIR (a local copy of the Mascot Designs project files)."""
import os, re
from PIL import Image
DIR = os.environ.get("RE_MASCOT_DIR", "/tmp/claude-0/-home-claude/97ad6b31-1277-5795-987d-0d7c1b8393c4/scratchpad/mascotcanvas/project")
_MAPS = {}

def _fills(svg):
    return [m.lower() for m in re.findall(r'<rect[^>]*?fill="(#[0-9A-Fa-f]{6})"', svg)]

def maps(ch):
    if ch in _MAPS: return _MAPS[ch]
    s = open(os.path.join(DIR, f"V2_04{ch.capitalize()}Swaps.dc.html"), encoding="utf-8").read()
    body = re.sub(r"<style.*?</style>", "", s, flags=re.S)
    parts = re.split(r"(<svg[^>]*width=\"248\".*?</svg>)", body, flags=re.S)
    svgs, labels = [], []
    for i, p in enumerate(parts):
        if p.startswith("<svg"):
            svgs.append(p)
            after = re.sub(r"<[^>]+>", " ", parts[i + 1] if i + 1 < len(parts) else "")
            after = re.sub(r"<svg.*", "", after); labels.append(re.sub(r"\s+", " ", after).strip().split("  ")[0])
    base = _fills(svgs[0]); out = {}
    for svg, lab in zip(svgs[1:], labels[1:]):
        f = _fills(svg); m = {}
        for a, b in zip(base, f): m.setdefault(a, b)
        name = re.sub(r"[^A-Za-z ].*", "", lab).replace(" Skill", "").strip() or f"swap{len(out) + 1}"
        out[name] = {tuple(int(a[i:i + 2], 16) for i in (1, 3, 5)): tuple(int(b[i:i + 2], 16) for i in (1, 3, 5)) for a, b in m.items() if a != b}
    _MAPS[ch] = out; return out

def names(ch): return list(maps(ch))

def recolor(img, ch, swap):
    m = maps(ch)[swap]; im = img.copy(); px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a and (r, g, b) in m: px[x, y] = m[(r, g, b)] + (a,)
    return im

def coverage(img, ch):
    """share of opaque pixels whose colour the swap maps know (a check that the rig and the swap board share Kit's palette)."""
    keys = set().union(*[set(v) for v in maps(ch).values()]); n = k = 0
    for r, g, b, a in img.getdata():
        if a: n += 1; k += (r, g, b) in keys
    return k / max(1, n)
