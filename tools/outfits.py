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
#   neck: (shoulder row, neckline bottom row, neckline half-width) - the jacket's top edge sits at the shoulder row at
#   the sides and scoops down to a round neckline under the chin; cx: body centre column.
CAST = {
    "theo":  {"band": (53, 68), "xmax": 99, "belly": {"fff5e3", "f2ecd5", "ead1b0"}, "neck": (51, 56, 10), "cx": 47},
    "penny": {"band": (54, 68), "xmax": 99, "belly": {"f0f2f5", "d8cfbc"}, "neck": (53, 57, 9), "cx": 47},
    "ada":   {"band": (53, 67), "xmax": 61, "belly": {"9dd8cf", "8cc0ba"}, "neck": (51, 56, 8), "cx": 46},
    "kit":   {"band": (52, 67), "xmax": 63, "belly": {"fde6eb"}, "neck": (50, 55, 8), "cx": 51},
    "roz":   {"band": (66, 88), "xmax": 99, "belly": {"ebe1ae", "c9b77c"}, "neck": (62, 67, 10), "cx": 61},
}
FOOT = {c: None for c in CAST}      # idle frame 0 feet row, filled on first use

OUTFITS = {
    # deep outline -> gloss. Cool near-blacks (never pure black), warm-grey zipper metal.
    "leather_jacket": {"out": "0c0c12", "ramp": ["15161d", "1f2029", "2b2d38", "3d4150"], "gloss": "8a90a3",
                       "zip": ("b8bcc6", "6e7280"), "lapel": "5a6075", "rib": "474c5c"},
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
    A CLOSED jacket: covers the shoulders, torso, belly and the arms below the shoulder line. Its top edge is a
    round scoop neckline under the chin with a ribbed collar band, the shoulders round off at the corners, it sits
    1 px proud of the body at the sides, centre zipper with a pull tab, waistband hem, gloss on the lit shoulder."""
    if ch not in CAST or name not in OUTFITS: return im
    O = OUTFITS[name]; c = CAST[ch]; rank = _ramp_map(ch); R = O["ramp"]
    out = im.copy(); src = im.load(); dst = out.load(); W, H = im.size
    dy = _feet(im) - _idle_feet(ch); y1 = c["band"][1] + dy
    sh, nk, hw = c["neck"]; sh += dy; nk += dy; cx = c["cx"]
    belly = c["belly"]; X = min(W, c["xmax"] + 1)
    solid = lambda x, y: 0 <= x < X and 0 <= y < H and src[x, y][3] > 0
    def top(x):   # scoop neckline: nk at the centre, rising on a round curve to the shoulder row at +-hw
        d = abs(x - cx)
        if d >= hw: return sh
        return sh + int(round((nk - sh) * (1 - (d / hw) ** 2) ** 0.5))
    mask = {(x, y) for x in range(X) for y in range(max(0, top(x)), min(H, y1 + 1)) if solid(x, y)}
    if not mask: return out
    # round the shoulder corners: drop the top edge by 2 px on the outermost column and 1 px on the next
    for y in range(sh, sh + 3):
        xs = sorted(x for (x, yy) in mask if yy == y)
        if not xs: continue
        for x, drop in ((xs[0], 2), (xs[-1], 2), (xs[0] + 1, 1), (xs[-1] - 1, 1)):
            if y < top(x) + drop: mask.discard((x, y))
    # 1 px of bulk at the sides, below the shoulder curve
    bulk = set()
    for y in range(sh + 3, min(H, y1 + 1)):
        xs = [x for (x, yy) in mask if yy == y]
        if len(xs) > 4:
            for x in (min(xs) - 1, max(xs) + 1):
                if 0 <= x < X and not solid(x, y): bulk.add((x, y))
    full = mask | bulk
    inside = lambda x, y: (x, y) in full
    bel = sorted({hexof(src[x, y]) for (x, y) in mask if hexof(src[x, y]) in belly}, key=lambda h: lum(rgb(h)))
    for (x, y) in full:
        edge = not (inside(x - 1, y) and inside(x + 1, y) and inside(x, y - 1) and (inside(x, y + 1) or y == y1))
        if (x, y) in bulk or edge: col = O["out"]
        else:
            p = src[x, y]; h = hexof(p); l = lum(p)
            if h in belly: col = R[1 + min(1, bel.index(h) * 2 // max(1, len(bel)))]
            elif l < 60: col = O["out"]
            else: col = R[rank.get(h, 2 if l > 128 else 1)]
        dst[x, y] = rgb(col)
    for (x, y) in mask:   # right front panel a step darker (light from the top-left)
        if x > cx + 1 and hexof(dst[x, y]) in (R[2], R[3]) and hexof(src[x, y]) in belly: dst[x, y] = rgb(R[1])
    # ribbed collar band: the row just inside the top edge, all along the neckline and over the shoulders
    for (x, y) in full:
        if hexof(dst[x, y]) != O["out"] and not inside(x, y - 2) and inside(x, y - 1) and hexof(dst[x, y - 1]) == O["out"]:
            dst[x, y] = rgb(O["lapel"] if x <= cx else O["rib"])
    # waistband hem
    for (x, y) in full:
        if y == y1 and hexof(dst[x, y]) != O["out"]: dst[x, y] = rgb(R[0])
        if y == y1 - 1 and hexof(dst[x, y]) != O["out"]: dst[x, y] = rgb(R[2])
    # zipper from the bottom of the collar down, pull tab under the collar
    zt = nk + 2
    for y in range(zt, min(H, y1 + 1)):
        if inside(cx, y) and hexof(dst[cx, y]) != O["out"]: dst[cx, y] = rgb(O["zip"][(y - zt) % 2])
    for y, z in ((zt, 0), (zt + 1, 1)):
        if inside(cx + 1, y): dst[cx + 1, y] = rgb(O["zip"][z])
    # gloss: a 1-2 px shine on the lit (top-left) shoulder, never right of the neckline
    shine = [(x, y) for y in range(sh, min(H, sh + 6)) for x in range(X)
             if x < cx - hw and inside(x, y) and hexof(dst[x, y]) in R and inside(x + 1, y + 1)
             and hexof(dst[x, y - 1]) in (O["out"], O["lapel"]) and hexof(dst[x - 1, y]) == O["out"]]
    for x, y in shine[:2]:
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
