"""Kit's outfit layer for the V2.03 rigs (2026-11-23, board 20261123-092000-penny-lj01, Penny's 6 PM video).

An outfit is drawn ON each frame of a rig, so it moves with every animation (idle, walk, talk, nod, point, celebrate,
facepalm, shrug, holdsign, shakehead, standing). It never scales or rotates a sprite: it repaints that frame's torso and
arm pixels into the outfit's own 6-tone ramp, keeping the frame's original shading (light from the top-left), and leaves
the belly showing as the shirt under an open jacket.

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
#   xmax: last column that belongs to the body (tails start right of it).  belly: the shirt colours left showing.
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
    """Outfit on one NATIVE padded frame (k=1, not flipped), as rigs.load gives it. Returns a new RGBA image."""
    if ch not in CAST or name not in OUTFITS: return im
    O = OUTFITS[name]; c = CAST[ch]; rank = _ramp_map(ch)
    out = im.copy(); src = im.load(); dst = out.load(); W, H = im.size
    dy = _feet(im) - _idle_feet(ch); y0, y1 = c["band"][0] + dy, c["band"][1] + dy
    belly = c["belly"]
    solid = lambda x, y: 0 <= x < W and 0 <= y < H and src[x, y][3] > 0
    def is_belly(x, y): return solid(x, y) and hexof(src[x, y]) in belly
    for y in range(max(0, y0), min(H, y1 + 1)):
        row = [x for x in range(min(W, c["xmax"] + 1)) if solid(x, y)]
        if not row: continue
        bx = [x for x in row if is_belly(x, y)]
        for x in row:
            if x in bx: continue
            p = src[x, y]; l = lum(p)
            edge = not (solid(x - 1, y) and solid(x + 1, y) and solid(x, y - 1) and solid(x, y + 1))
            if edge or l < 60: col = O["out"]
            else: col = O["ramp"][rank.get(hexof(p), 2 if l > 128 else 1)]
            dst[x, y] = rgb(col)
        body = [x for x in row if not (x in bx)]
        if bx:      # open jacket: zipper teeth on the left front edge, a lit lapel on the right one
            l_edge, r_edge = min(bx) - 1, max(bx) + 1
            if solid(l_edge, y) and l_edge not in bx: dst[l_edge, y] = rgb(O["zip"][(y - y0) % 2])
            if solid(r_edge, y) and r_edge not in bx: dst[r_edge, y] = rgb(O["lapel"])
        elif len(body) > 6:   # closed below the belly: one zipper line down the middle
            mid = (min(body) + max(body)) // 2
            if solid(mid, y) and solid(mid - 1, y) and solid(mid + 1, y): dst[mid, y] = rgb(O["zip"][(y - y0) % 2])
    # gloss: a 1-2 px shine on the lit (top-left) shoulder of each sleeve/side panel, never on the right half
    jacket = lambda x, y: 0 <= x < W and 0 <= y < H and hexof(dst[x, y]) in O["ramp"]
    xs = [x for y in range(max(0, y0), min(H, y1 + 1)) for x in range(min(W, c["xmax"] + 1)) if jacket(x, y)]
    if xs:
        cx = (min(xs) + max(xs)) / 2; shine = []
        for y in range(max(0, y0), min(H, y0 + (y1 - y0) // 2)):
            for x in range(min(W, c["xmax"] + 1)):
                if x < cx and jacket(x, y) and not jacket(x - 1, y) and not jacket(x, y - 1) and jacket(x + 1, y + 1):
                    shine.append((x, y))
        for x, y in shine[:3]:
            dst[x, y] = rgb(O["gloss"])
            if jacket(x + 1, y + 1): dst[x + 1, y + 1] = rgb(O["ramp"][3])
    # collar: the top two band rows get a lit fold at the outer edge of each lapel, and the collar points one row up
    for yy in (y0, y0 + 1):
        if not (0 <= yy < H): continue
        bx = [x for x in range(min(W, c["xmax"] + 1)) if is_belly(x, yy)]
        if not bx: continue
        for x in (min(bx) - 2, max(bx) + 2):
            if solid(x, yy) and hexof(dst[x, yy]) != O["out"]: dst[x, yy] = rgb(O["lapel"])
    if 0 < y0 < H:
        bx = [x for x in range(min(W, c["xmax"] + 1)) if is_belly(x, y0)]
        if bx:
            for x in (min(bx) - 1, max(bx) + 1):
                if solid(x, y0 - 1): dst[x, y0 - 1] = rgb(O["ramp"][2])
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
