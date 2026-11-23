"""Kit's outfit layer for the V2.03 rigs (2026-11-23, board 20261123-092000-penny-lj01, Penny's 6 PM video).

An outfit is drawn ON each frame of a rig, so it moves with every animation (idle, walk, talk, nod, point, celebrate,
facepalm, shrug, holdsign, shakehead, standing). It never scales or rotates a sprite: it repaints that frame's torso and
arm pixels into the outfit's own 6-tone ramp, keeping the frame's original shading (light from the top-left), and closes
it over the belly with a centre zipper.

    import outfits
    outfits.names()                                   -> ["leather_jacket"]
    outfits.outfit(sprite, "theo", "leather_jacket")  -> RGBA, works on any rigs.frame() output (any k, flipped or not)
    rigs.frame("penny", "walk", t, k=7, outfit="leather_jacket")   # same thing, cached per frame
    rigs.OUTFIT = "leather_jacket"                    # every rigs.frame() call wears it (what spec["outfit"] sets)
    rigs.OUTFIT = {"theo": "leather_jacket"}          # or only some of the cast

Spec switch (tools/newwave.py and tools/daily.py): spec["outfit"] = "leather_jacket" (whole cast) or
{"theo": "leather_jacket", "roz": "leather_jacket"}. Leave it out for no outfit.

Characters: theo, penny, ada, kit, roz. The boss characters are never dressed (they are not in the video cast).
Desk animations (desk*, desk34*) are skipped: the desk sits inside the torso band.
Art rules (rec-marketing-pixel-art): generic biker jacket, no logos, no words, no digits; outline in the material's own
darkest tone; a gloss highlight only where the frame was already lit; a zipper line and lapels. Check sheet:
python3 tools/outfits.py sheet <out.png>"""
import os, sys
from PIL import Image

PAD = 24
# Per character, on the padded native frame of rigs.load(ch, "idle")[0][0] (feet at the bottom row):
#   band: torso rows (top, bottom) measured on idle frame 0; every other frame is shifted by its own feet line.
#   xmax: last column that belongs to the body (tails start right of it).  belly: the belly colours (covered by the jacket's front panels).
CAST = {
    "theo":  {"band": (53, 68), "xmax": 99, "belly": {"fff5e3", "f2ecd5", "ead1b0"}},
    "penny": {"band": (54, 68), "xmax": 99, "belly": {"f0f2f5", "d8cfbc"}},
    "ada":   {"band": (53, 67), "xmax": 61, "belly": {"9dd8cf", "8cc0ba"}},
    "kit":   {"band": (52, 67), "xmax": 63, "belly": {"fde6eb"}},
    "roz":   {"band": (66, 88), "xmax": 99, "belly": {"ebe1ae", "c9b77c"}},
}
FOOT = {c: None for c in CAST}      # idle frame 0 feet row, filled on first use

OUTFITS = {
    # deep outline -> gloss. Cool near-blacks (never pure black), warm-grey zipper metal.
    "leather_jacket": {"out": "0c0c12", "ramp": ["15161d", "1f2029", "2b2d38", "3d4150"], "gloss": "8a90a3",
                       "zip": ("b8bcc6", "6e7280"), "lapel": "4a4f60"},
}
_CACHE = {}


def names(): return list(OUTFITS)
def rgb(h): return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)
def hexof(p): return "%02x%02x%02x" % p[:3]
def lum(p): return 0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]


def _feet(im):
    bb = im.getbbox(); return bb[3] - 1 if bb else im.height - 1


def _idle_feet(ch):
    if FOOT[ch] is None:
        import rigs
        FOOT[ch] = _feet(rigs.load(ch, "idle")[0][0])
    return FOOT[ch]


def _ramp_map(ch):
    """The character's distinct non-belly body colours in the torso band (all idle frames), darkest to lightest,
    mapped by rank onto the 4-step ramp: {hex: ramp index}. Ranking colours, not pixels, keeps a big flat fur area
    from all landing on one tone."""
    k = ("ramp", ch)
    if k in _CACHE: return _CACHE[k]
    import rigs
    c = CAST[ch]; y0, y1 = c["band"]; cols = set()
    for an in rigs.anims(ch):
        for im in rigs.load(ch, an)[0]:
            px = im.load(); dy = _feet(im) - _idle_feet(ch)
            for y in range(max(0, y0 + dy), min(im.height, y1 + dy + 1)):
                for x in range(min(im.width, c["xmax"] + 1)):
                    p = px[x, y]
                    if p[3] and hexof(p) not in c["belly"] and lum(p) >= 60: cols.add(hexof(p))
    srt = sorted(cols, key=lambda h: lum(rgb(h))); n = len(srt)
    _CACHE[k] = {h: min(3, int(4 * i / max(1, n))) for i, h in enumerate(srt)}
    return _CACHE[k]


def dress(im, ch, name="leather_jacket"):
    """Outfit on one NATIVE padded frame (k=1, not flipped), as rigs.load gives it. Returns a new RGBA image.
    A CLOSED jacket: covers the whole torso and the arms in the band (belly included), sits 1 px proud of the body
    at the sides, centre zipper with a pull tab, V-neck collar with a shirt notch and lapels, a waistband hem."""
    if ch not in CAST or name not in OUTFITS: return im
    O = OUTFITS[name]; c = CAST[ch]; rank = _ramp_map(ch); R = O["ramp"]
    out = im.copy(); src = im.load(); dst = out.load(); W, H = im.size
    dy = _feet(im) - _idle_feet(ch); y0, y1 = c["band"][0] + dy, c["band"][1] + dy
    belly = c["belly"]; X = min(W, c["xmax"] + 1)
    solid = lambda x, y: 0 <= x < X and 0 <= y < H and src[x, y][3] > 0
    rows = range(max(0, y0), min(H, y1 + 1))
    mask = {(x, y) for y in rows for x in range(X) if solid(x, y)}
    if not mask: return out
    # centre line: middle of the belly on the band's rows (falls back to the middle of the torso)
    bx = [x for (x, y) in mask if hexof(src[x, y]) in belly]
    cx = round(sum(bx) / len(bx)) if bx else round(sum(x for x, _ in mask) / len(mask))
    # 1 px of bulk at the sides: an outline pixel just outside the body on each torso row
    bulk = set()
    for y in rows:
        xs = [x for x in range(X) if (x, y) in mask]
        if len(xs) > 4:
            for x in (min(xs) - 1, max(xs) + 1):
                if 0 <= x < X and not solid(x, y): bulk.add((x, y))
    full = mask | bulk
    inside = lambda x, y: (x, y) in full
    bel = sorted({hexof(src[x, y]) for (x, y) in mask if hexof(src[x, y]) in belly}, key=lambda h: lum(rgb(h)))
    for (x, y) in full:
        edge = not (inside(x - 1, y) and inside(x + 1, y) and (inside(x, y - 1) or y == y0) and (inside(x, y + 1) or y == y1))
        if (x, y) in bulk or edge: col = O["out"]
        else:
            p = src[x, y]; h = hexof(p); l = lum(p)
            if h in belly: col = R[1 + min(1, bel.index(h) * 2 // max(1, len(bel)))]   # front panels: flat, mid tones
            elif l < 60: col = O["out"]
            else: col = R[rank.get(h, 2 if l > 128 else 1)]
        dst[x, y] = rgb(col)
    # front panels: right panel a step darker than the left (light from the top-left)
    for (x, y) in mask:
        if x > cx + 1 and hexof(dst[x, y]) in (R[2], R[3]) and hexof(src[x, y]) in belly: dst[x, y] = rgb(R[1])
    # waistband hem: the bottom two rows of the jacket
    for (x, y) in full:
        if y == y1 and hexof(dst[x, y]) != O["out"]: dst[x, y] = rgb(R[0])
        if y == y1 - 1 and hexof(dst[x, y]) not in (O["out"],): dst[x, y] = rgb(R[2])
    # zipper down the centre, pull tab near the top
    for y in rows:
        if inside(cx, y) and hexof(dst[cx, y]) != O["out"]: dst[cx, y] = rgb(O["zip"][(y - y0) % 2])
    if inside(cx + 1, y0 + 4): dst[cx + 1, y0 + 4] = rgb(O["zip"][0]); 
    if inside(cx + 1, y0 + 5): dst[cx + 1, y0 + 5] = rgb(O["zip"][1])
    # V-neck: a small shirt notch at the throat, lapels running down and out from it, collar points above the band
    shirt = (232, 232, 238, 255)
    for i, half in enumerate((2, 1, 0)):
        y = y0 + i
        for x in range(cx - half, cx + half + 1):
            if inside(x, y): dst[x, y] = shirt
    for i in range(5):
        y = y0 + i
        for x in (cx - 3 - i // 2 - (1 if i == 0 else 0), cx + 3 + i // 2 + (1 if i == 0 else 0)):
            if inside(x, y) and hexof(dst[x, y]) != O["out"]: dst[x, y] = rgb(O["lapel"] if x < cx else R[3])
        for x in (cx - 2 - i // 2, cx + 2 + i // 2):
            if inside(x, y) and i > 0 and hexof(dst[x, y]) != O["out"]: dst[x, y] = rgb(R[0])
    for x, col in ((cx - 4, O["lapel"]), (cx - 3, O["lapel"]), (cx + 3, R[3]), (cx + 4, R[3])):
        if 0 <= y0 - 1 < H and 0 <= x < W and src[x, y0 - 1][3]: dst[x, y0 - 1] = rgb(col)
    for x in (cx - 5, cx + 5):
        if 0 <= y0 - 1 < H and 0 <= x < W and src[x, y0 - 1][3]: dst[x, y0 - 1] = rgb(O["out"])
    # gloss: a 1-2 px shine on the lit (top-left) shoulder, never on the right half
    shine = [(x, y) for y in range(max(0, y0), min(H, y0 + (y1 - y0) // 2)) for x in range(X)
             if x < cx - 5 and inside(x, y) and hexof(dst[x, y]) in R and not inside(x - 1, y - 1) and inside(x + 1, y + 1)
             and hexof(dst[x - 1, y]) == O["out"]]
    for x, y in shine[:3]:
        dst[x, y] = rgb(O["gloss"])
        if inside(x + 1, y + 1) and hexof(dst[x + 1, y + 1]) in R: dst[x + 1, y + 1] = rgb(R[3])
    return out


def outfit(sprite, ch, name="leather_jacket", k=None, flip=None):
    """Outfit on any rigs.frame() output. k and flip are worked out from the size if not given; prefer
    rigs.frame(..., outfit=name), which dresses the native frame before scaling and caches it."""
    import rigs
    nat = rigs.load(ch, "idle")[0][0]
    if k is None: k = max(1, round(sprite.height / nat.height))
    im = sprite if k == 1 else sprite.resize((sprite.width // k, sprite.height // k), Image.NEAREST)
    if flip is None:   # a flipped frame has its tail on the left: compare mass either side of centre
        bb = im.getbbox(); a = im.crop((0, 0, im.width // 2, im.height)).getbbox(); flip = False
        if CAST.get(ch, {}).get("xmax", 99) < 99 and bb:
            L = sum(1 for p in im.crop((0, 0, im.width // 2, im.height)).getdata() if p[3])
            R = sum(1 for p in im.crop((im.width // 2, 0, im.width, im.height)).getdata() if p[3])
            flip = L > R
    if flip: im = im.transpose(Image.FLIP_LEFT_RIGHT)
    im = dress(im, ch, name)
    if flip: im = im.transpose(Image.FLIP_LEFT_RIGHT)
    return im if k == 1 else im.resize((im.width * k, im.height * k), Image.NEAREST)


def sheet(path, chars=("theo", "penny", "ada", "kit", "roz"), name="leather_jacket", k=4):
    """Check sheet: every frame of every core animation, before (top) and after (bottom) per character."""
    import rigs
    rows = []
    for ch in chars:
        for an in rigs.anims(ch):
            ims = rigs.load(ch, an)[0]
            rows.append((ims, [dress(i, ch, name) for i in ims]))
    cw = max(i.width for r in rows for i in r[0]) * k; chh = max(i.height for r in rows for i in r[0]) * k
    n = max(len(r[0]) for r in rows)
    out = Image.new("RGBA", (cw * n, chh * 2 * len(rows)), (196, 198, 208, 255))
    for j, (a, b) in enumerate(rows):
        for i, (x, y) in enumerate(zip(a, b)):
            out.alpha_composite(x.resize((x.width * k, x.height * k), Image.NEAREST), (i * cw, 2 * j * chh))
            out.alpha_composite(y.resize((y.width * k, y.height * k), Image.NEAREST), (i * cw, (2 * j + 1) * chh))
    out.save(path); return path


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "sheet": print(sheet(sys.argv[2], *(sys.argv[3:] and [tuple(sys.argv[3:])])))
    else: print(__doc__)
