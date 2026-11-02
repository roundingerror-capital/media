"""PIXKIT: the small pixel-art toolkit every generated asset uses (rec-marketing-pixel-art).
Draw at the final size, one light source (top-left), 3-5 tone hue-shifted ramps per material, shade by form (normals, never
rectangles), selective outline (darkest tone on the shadow side, one step darker on the lit side), whole-number NEAREST scaling,
and a readability check (1x, 4x, silhouette, grayscale) before anything ships. Animation = separate drawings per frame, never a
transform of one image (holiday_assets.py, props.py and scenes.py redraw every frame from scratch).

    P = Px(24, 24)                       # transparent canvas
    R = ramp((200, 60, 60))               # 5 tones: deep shadow, shadow, base, light, highlight
    P.sphere((4, 4, 19, 19), R)           # a shaded ball
    P.selout()                            # selective outline from the canvas's own ramps
    P.im  (PIL RGBA)   scaled(P.im, 4)    strip(frames, 4)   gif(frames, ticks, path)   data_uri(im, 4)
"""
import colorsys, math, io, base64, random
from PIL import Image, ImageDraw

LIGHT = (-.55, -.7, .5)   # top-left, slightly in front
TICK_MS = 100              # 1 tick = 100 ms (Kit's V2.03 idle test)

# ---------------------------------------------------------------- colour
def _hsv(c): return colorsys.rgb_to_hsv(c[0] / 255, c[1] / 255, c[2] / 255)
def _rgb(h, s, v): return tuple(int(round(x * 255)) for x in colorsys.hsv_to_rgb(h % 1, max(0, min(1, s)), max(0, min(1, v))))
def _toward(h, target, k):
    d = ((target - h + .5) % 1) - .5
    return h + d * k
def hexc(s):
    s = s.lstrip("#"); return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16))

def ramp(base, dark=0.66, light=0.5, shift=0.035):
    """5 hue-shifted tones from one base colour: [deep shadow, shadow, base, light, highlight].
    Darker steps turn cool (toward blue-purple, 260 deg) and a little more saturated; lighter steps turn warm (toward 50 deg)
    and less saturated; the ends never hit full saturation or pure white/black."""
    if isinstance(base, str): base = hexc(base)
    h, s, v = _hsv(base); out = []
    for k in (-2, -1):
        n = -k; out.append(_rgb(_toward(h, 0.72, shift * n * 2.2), min(.92, s * (1.12 ** n) + .04 * n), v * (dark ** n)))
    out.append(tuple(base[:3]))
    for k in (1, 2):
        out.append(_rgb(_toward(h, 0.14, shift * k * 2.2), s * (0.72 ** k), v + (1 - v) * (light * k * .85)))
    return out

def mixc(a, b, t): return tuple(int(x + (y - x) * t) for x, y in zip(a[:3], b[:3]))
def darker(c, k=0.7): h, s, v = _hsv(c); return _rgb(_toward(h, .72, .03), min(.95, s * 1.08), v * k)

GREY = ramp((150, 150, 158)); WHITE = ramp((228, 228, 224), dark=.72); BLACK = ramp((54, 52, 60), dark=.6, light=.35)
WOOD = ramp((160, 108, 62)); GOLD = ramp((232, 184, 64)); SILVER = ramp((190, 196, 206), dark=.7)
RED = ramp((206, 48, 52)); GREEN = ramp((60, 150, 76)); BLUE = ramp((58, 96, 200)); LIME = ramp((200, 240, 60), light=.3)
SKIN = ramp((236, 190, 150)); PINK = ramp((238, 120, 160)); ORANGE = ramp((236, 130, 44)); YELLOW = ramp((240, 206, 70))
PURPLE = ramp((132, 80, 190)); TEAL = ramp((60, 170, 170)); BROWN = ramp((120, 76, 44)); CREAM = ramp((238, 224, 190), dark=.7)
INK = (22, 18, 26)

# ---------------------------------------------------------------- canvas
class Px:
    def __init__(self, w, h):
        self.w, self.h = w, h; self.im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); self.px = self.im.load(); self.ramps = []
    def _reg(self, R):
        if R not in self.ramps: self.ramps.append(R)
    def put(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h and c is not None: self.px[int(x), int(y)] = tuple(c[:3]) + (255,)
    def get(self, x, y):
        if 0 <= x < self.w and 0 <= y < self.h: return self.px[int(x), int(y)]
        return (0, 0, 0, 0)
    def rect(self, x0, y0, x1, y1, c):
        for y in range(int(min(y0, y1)), int(max(y0, y1)) + 1):
            for x in range(int(min(x0, x1)), int(max(x0, x1)) + 1): self.put(x, y, c)
    def hline(self, x0, x1, y, c): self.rect(x0, y, x1, y, c)
    def vline(self, x, y0, y1, c): self.rect(x, y0, x, y1, c)
    def line(self, x0, y0, x1, y1, c):
        n = max(abs(x1 - x0), abs(y1 - y0), 1)
        for i in range(n + 1): self.put(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n), c)
    def mask(self, fn):
        """mask image from a draw callback fn(ImageDraw) -> set of (x, y)."""
        m = Image.new("L", (self.w, self.h), 0); fn(ImageDraw.Draw(m)); mp = m.load()
        return {(x, y) for y in range(self.h) for x in range(self.w) if mp[x, y]}
    def ell_mask(self, box): return self.mask(lambda d: d.ellipse([box[0], box[1], box[2], box[3]], fill=255))
    def poly_mask(self, pts): return self.mask(lambda d: d.polygon(pts, fill=255))
    def fill(self, cells, c):
        for x, y in cells: self.put(x, y, c)
    # ---- form shading
    def shade(self, cells, box, R, light=LIGHT, bands=(.14, .36, .66, .9), rim=False, flat=False, shape="sphere"):
        """Shade a set of cells by a pseudo-normal from `box` (sphere: ellipsoid; vcyl: vertical cylinder, tone varies with x;
        hcyl: horizontal cylinder; flat: all base) into the 5 tones of ramp R. Bands = lambert thresholds (flat clusters, no gradients)."""
        self._reg(R); x0, y0, x1, y1 = box; cx, cy = (x0 + x1 + 1) / 2, (y0 + y1 + 1) / 2; rx, ry = max(.5, (x1 - x0 + 1) / 2), max(.5, (y1 - y0 + 1) / 2)
        lx, ly, lz = light; ln = (lx * lx + ly * ly + lz * lz) ** .5; lx, ly, lz = lx / ln, ly / ln, lz / ln
        for x, y in cells:
            if flat: self.put(x, y, R[2]); continue
            nx, ny = (x + .5 - cx) / rx, (y + .5 - cy) / ry
            if shape == "vcyl": ny = 0
            if shape == "hcyl": nx = 0
            r2 = min(1.0, nx * nx + ny * ny); nz = (1 - r2) ** .5
            lam = max(0.0, nx * lx + ny * ly + nz * lz) ** 1.25
            k = 0 if lam < bands[0] else 1 if lam < bands[1] else 2 if lam < bands[2] else 3 if lam < bands[3] else 4
            if rim and r2 > .78 and nx > .25 and ny > -.1 and k < 2: k = 2
            self.put(x, y, R[k])
    def sphere(self, box, R, **kw): self.shade(self.ell_mask(box), box, R, **kw)
    def vcyl(self, box, R, **kw):
        cells = {(x, y) for y in range(box[1], box[3] + 1) for x in range(box[0], box[2] + 1)}; self.shade(cells, box, R, shape="vcyl", **kw)
    def hcyl(self, box, R, **kw):
        cells = {(x, y) for y in range(box[1], box[3] + 1) for x in range(box[0], box[2] + 1)}; self.shade(cells, box, R, shape="hcyl", **kw)
    def box(self, x0, y0, x1, y1, R, top=1, side=1):
        """A box lit from the top-left: light top band, base face, shadow right band and bottom row."""
        self._reg(R); self.rect(x0, y0, x1, y1, R[2])
        if top: self.rect(x0, y0, x1, y0 + top - 1, R[3])
        if side: self.rect(x1 - side + 1, y0 + top, x1, y1, R[1])
        self.hline(x0, x1, y1, R[1]); self.put(x1, y1, R[0])
    def poly(self, pts, R, box=None, **kw):
        cells = self.poly_mask(pts)
        if not cells: return
        xs = [x for x, _ in cells]; ys = [y for _, y in cells]
        self.shade(cells, box or (min(xs), min(ys), max(xs), max(ys)), R, **kw)
    def tri(self, x0, y0, x1, y1, x2, y2, R, **kw): self.poly([(x0, y0), (x1, y1), (x2, y2)], R, **kw)
    # ---- outline
    def selout(self, lit=1, shadow=2, extra=()):
        """Selective outline: an opaque pixel with a transparent 4-neighbour becomes darker: `shadow` steps where the gap is below
        or right of it, `lit` steps where it is above or left. Tones come from the ramps used on this canvas (plus `extra`)."""
        ramps = list(self.ramps) + list(extra); idx = {}
        for R in ramps:
            for i, c in enumerate(R): idx.setdefault(tuple(c[:3]), (R, i))
        src = {(x, y): self.px[x, y] for y in range(self.h) for x in range(self.w) if self.px[x, y][3]}
        for (x, y), c in src.items():
            key = tuple(c[:3])
            if key not in idx: continue
            R, i = idx[key]
            below = self.get(x, y + 1)[3] == 0 or self.get(x + 1, y)[3] == 0
            above = self.get(x, y - 1)[3] == 0 or self.get(x - 1, y)[3] == 0
            if below: self.put(x, y, R[max(0, i - shadow)])
            elif above: self.put(x, y, R[max(0, i - lit)])
    def hardline(self, c=INK):
        """Full 1 px outline in one colour around everything (for things that must read on any background)."""
        src = {(x, y) for y in range(self.h) for x in range(self.w) if self.px[x, y][3]}
        for x, y in src:
            if any(self.get(x + dx, y + dy)[3] == 0 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): self.put(x, y, c)
    # ---- small things
    def sparkle(self, x, y, size, c=(255, 252, 240)):
        """4-point star: size 0 = one dot, 1 = plus, 2 = plus with long arms."""
        self.put(x, y, c)
        if size >= 1:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)): self.put(x + dx, y + dy, c)
        if size >= 2:
            for dx, dy in ((2, 0), (-2, 0), (0, 2), (0, -2)): self.put(x + dx, y + dy, c)
    def paste(self, other, x, y):
        self.im.paste(other.im if isinstance(other, Px) else other, (int(x), int(y)), other.im if isinstance(other, Px) else other); self.px = self.im.load()
    def flip(self):
        self.im = self.im.transpose(Image.FLIP_LEFT_RIGHT); self.px = self.im.load(); return self
    def copy(self):
        q = Px(self.w, self.h); q.im = self.im.copy(); q.px = q.im.load(); q.ramps = list(self.ramps); return q

# ---------------------------------------------------------------- export and checks
def scaled(im, k): return im.resize((im.width * k, im.height * k), Image.NEAREST)
def strip(frames, k=4, gap=4, bg=(0, 0, 0, 0)):
    w = sum(f.width * k for f in frames) + gap * (len(frames) - 1); h = max(f.height * k for f in frames)
    out = Image.new("RGBA", (w, h), bg); x = 0
    for f in frames: s = scaled(f, k); out.paste(s, (x, h - s.height), s); x += s.width + gap
    return out
def data_uri(im, k=1):
    b = io.BytesIO(); (scaled(im, k) if k != 1 else im).save(b, "PNG", optimize=True); return "data:image/png;base64," + base64.b64encode(b.getvalue()).decode()
def gif(frames, ticks, path, k=4):
    """Transparent looping GIF, one drawing per frame, hold = ticks * 100 ms."""
    ims = []
    for f in frames:
        s = scaled(f, k).convert("RGBA"); bg = Image.new("RGBA", s.size, (255, 0, 255, 255)); bg.paste(s, (0, 0), s)
        p = bg.convert("RGB").quantize(colors=255, method=Image.Quantize.MEDIANCUT); pal = p.getpalette()
        # index 255 = transparent key (magenta)
        key = None
        for i in range(256):
            if pal[3 * i:3 * i + 3] == [255, 0, 255]: key = i; break
        if key is None: key = 255
        ims.append((p, key))
    first, key = ims[0]
    first.save(path, save_all=True, append_images=[p for p, _ in ims[1:]], duration=[t * TICK_MS for t in ticks], loop=0, transparency=key, disposal=2, optimize=False)
    return path
def silhouette(im, c=(20, 20, 24, 255)):
    a = im.split()[3].point(lambda v: 255 if v > 0 else 0); out = Image.new("RGBA", im.size, (0, 0, 0, 0)); out.paste(Image.new("RGBA", im.size, c), (0, 0), a); return out
def grayscale(im):
    g = im.convert("LA").convert("RGBA"); g.putalpha(im.split()[3]); return g
def check_sheet(frames, k=4, bg=(60, 64, 70, 255)):
    """1x row, 4x row, silhouette row, grayscale row: the readability check from the skill, as one image to look at."""
    rows = [strip(frames, 1, 2), strip(frames, k, 4), strip([silhouette(f) for f in frames], k, 4), strip([grayscale(f) for f in frames], k, 4)]
    w = max(r.width for r in rows) + 16; h = sum(r.height for r in rows) + 8 * (len(rows) + 1)
    out = Image.new("RGBA", (w, h), bg); y = 8
    for r in rows: out.paste(r, (8, y), r); y += r.height + 8
    return out
def contact(items, k=4, cols=10, cell=None, bg=(14, 16, 22, 255), label=None):
    """Grid of frame-0 stills (items = list of PIL images) for a quick look at a whole family."""
    cw = cell or (max(i.width for i in items) * k + 12); ch = cell or (max(i.height for i in items) * k + 12)
    rows = (len(items) + cols - 1) // cols; out = Image.new("RGBA", (cols * cw, rows * ch), bg)
    for n, im in enumerate(items):
        s = scaled(im, k); x = (n % cols) * cw + (cw - s.width) // 2; y = (n // cols) * ch + (ch - s.height) // 2; out.paste(s, (x, y), s)
    return out
