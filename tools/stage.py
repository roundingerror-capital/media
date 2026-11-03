"""Kit's OFF stages (Assets Designs, Offices page) as composable sets for the video tools (the boss 2026-11-03: rooms are
assets in depth layers, not a painted background; people in the back, the lead in the middle, a big one up front).

A stage board (OFF-<NAME>-<n>.dc.html) holds a 192x128 world: symbols (one <g id="<prefix><ASSET>"> of 1 px rects per kit
piece), layers <g id="<prefix>L<n>"> of <use href x y> placements (wall tiles, five floor bands for depth, trim and shadows,
then the furniture from the back of the room to the front), a luminance mask on the wall layer, and four camera framings.

    import stage
    st = stage.load("project/OFF-ADA-01.dc.html")
    st.layers                      -> [(name, [(asset_id, x, y), ...]), ...]   in draw order
    im = st.render(skip={"DSK", "MON", "TEC08", "CHR"})   # RGBA 192x128 without the desk set (a rig brings its own desk)
    st.frames                      -> {"wide": (x, y, w, h), "portrait": ..., "tight": ...}  Kit's camera windows
    stage.piece(st, "DEC03")       -> RGBA of one kit piece (a wall clock) at native size, to place anywhere
The renderer draws rects itself (no browser): every pixel is exactly the board's."""
import os, re
from PIL import Image, ImageDraw

W, H = 192, 128
FLOOR_TOP = 88          # the wall ends and the floor starts (y, native): a standing character's feet go from 92 (back) to 124 (front)

def _rgba(fill, opacity=1.0):
    fill = fill.strip()
    if fill.startswith("#"):
        h = fill[1:]
        if len(h) == 3: h = "".join(c * 2 for c in h)
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        a = int(h[6:8], 16) if len(h) == 8 else 255
        return (r, g, b, int(a * opacity))
    m = re.match(r"rgba?\(([^)]+)\)", fill)
    if m:
        p = [float(v) for v in m.group(1).split(",")]
        return (int(p[0]), int(p[1]), int(p[2]), int((p[3] if len(p) > 3 else 1) * 255 * opacity))
    return (0, 0, 0, 0)

_RECT = re.compile(r'<rect\s+([^>]*?)/?>')
_ATTR = re.compile(r'([\w:-]+)="([^"]*)"')
def _rects(body):
    out = []
    for m in _RECT.finditer(body):
        a = dict(_ATTR.findall(m.group(1)))
        if a.get("fill", "").lower() == "none": continue
        out.append((int(float(a.get("x", 0))), int(float(a.get("y", 0))), int(float(a.get("width", 1))), int(float(a.get("height", 1))),
                    _rgba(a.get("fill", "#000"), float(a.get("opacity", a.get("fill-opacity", 1))))))
    return out

class Stage:
    def __init__(self, path):
        html = open(path, encoding="utf-8").read(); self.path = path
        self.prefix = re.search(r'<g id="(\w+?)L0"', html).group(1)
        defs = re.search(r'<svg width="0" height="0"[^>]*>(.*?)</svg>', html, re.S).group(1)
        self.symbols = {}; self.masks = {}
        for m in re.finditer(r'<(g|mask)\s+id="' + self.prefix + r'(\w+)"([^>]*)>(.*?)</\1>', defs, re.S):
            kind, name, attrs, body = m.groups()
            if name.startswith("L") and name[1:].isdigit(): continue
            if kind == "mask": self.masks[name] = _rects(body)
            elif "<use" in body: self.symbols[name] = ("uses", self._uses(body), _rects(body))
            else: self.symbols[name] = ("rects", _rects(body), None)
        self.layers = []
        for m in re.finditer(r'<g id="' + self.prefix + r'(L\d+)"[^>]*>(.*?)</g>\s*(?=<g id=|<mask|$)', defs, re.S):
            name, body = m.groups(); mask = re.search(r'mask="url\(#' + self.prefix + r'(\w+)\)"', body)
            self.layers.append((name, self._uses(body), mask.group(1) if mask else None))
        self.layers.sort(key=lambda l: int(l[0][1:]))
        self.frames = {}
        for lab, vb in re.findall(r'<svg[^>]*viewBox="([^"]+)"[^>]*aria-label="([^"]+)"', html):
            pass
        for vb, lab in re.findall(r'<svg[^>]*viewBox="([^"]+)"[^>]*aria-label="([^"]+)"[^>]*>', html):
            x, y, w, h = [int(float(v)) for v in vb.split()]
            key = "wide" if "wide" in lab else "stage" if "whole stage" in lab else "tight" if "tight" in lab else "portrait" if "portrait" in lab else "pan" if "pan" in lab else lab
            self.frames.setdefault(key, (x, y, w, h))
        sw = self.frames.get("stage", (0, 0, W, H)); self.w, self.h = sw[2], sw[3]      # ROOM stages are 320 wide (V3.01)
        self.title = (re.search(r"<title>(.*?)</title>", html) or [None, os.path.basename(path)])[1]
        self.note = (re.search(r'<p[^>]*>([^<]*)', html) or [None, ""])[1]

    def _uses(self, body):
        return [(m.group(1), int(float(m.group(2) or 0)), int(float(m.group(3) or 0)))
                for m in re.finditer(r'<use href="#' + self.prefix + r'(\w+)"(?:[^>]*?\bx="(-?[\d.]+)")?(?:[^>]*?\by="(-?[\d.]+)")?[^>]*>', body)]

    def draw_symbol(self, im, name, x0, y0):
        kind, a, b = self.symbols[name]; px = im.load()
        if kind == "uses":
            for sid, x, y in a: self.draw_symbol(im, sid, x0 + x, y0 + y)
            rects = b
        else: rects = a
        for x, y, w, h, col in rects:
            if col[3] == 0: continue
            for yy in range(max(0, y0 + y), min(im.height, y0 + y + h)):
                for xx in range(max(0, x0 + x), min(im.width, x0 + x + w)):
                    if col[3] == 255: px[xx, yy] = col
                    else:
                        r, g, bb, a0 = px[xx, yy]; k = col[3] / 255
                        px[xx, yy] = (int(r + (col[0] - r) * k), int(g + (col[1] - g) * k), int(bb + (col[2] - bb) * k), max(a0, col[3]))

    def mask_image(self, name):
        m = Image.new("L", (self.w, self.h), 0); d = ImageDraw.Draw(m)
        for x, y, w, h, col in self.masks[name]:
            lum = int((0.2126 * col[0] + 0.7152 * col[1] + 0.0722 * col[2]) * col[3] / 255)
            d.rectangle([x, y, x + w - 1, y + h - 1], fill=lum)
        return m

    def render(self, skip=(), only=None, layers=None, extra=None, wall=None):
        """RGBA 192x128. skip: asset-id prefixes left out (e.g. "DSK", "MON", "CHR"); only: the asset-id prefixes drawn;
        layers: layer names to draw (default all); extra: {layer name: [(RGBA image, x, y), ...]} drawn after that layer;
        wall: another WALL tile (RGBA, from component()) in place of the stage's own, under the same light mask."""
        W, H = self.w, self.h
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); extra = extra or {}
        for name, uses, mask in self.layers:
            if layers is not None and name not in layers: continue
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            if wall is not None and any(sid.startswith("WALL") for sid, _, _ in uses):
                for y in range(0, FLOOR_TOP, wall.height):
                    for x in range(0, W, wall.width): lay.paste(wall.crop((0, 0, wall.width, min(wall.height, FLOOR_TOP - y))), (x, y))
            for sid, x, y in uses:
                if wall is not None and sid.startswith("WALL"): continue
                if any(sid.startswith(s) for s in skip): continue
                if only and not any(sid.startswith(s) for s in only): continue
                self.draw_symbol(lay, sid, x, y)
            if mask: lay.putalpha(Image.eval(Image.composite(lay.getchannel("A"), Image.new("L", (W, H), 0), self.mask_image(mask)), lambda v: v))
            im.alpha_composite(lay)
            for sp, x, y in extra.get(name, []):
                if 0 <= x and 0 <= y and x + sp.width <= W and y + sp.height <= H: im.alpha_composite(sp, (int(x), int(y)))
                else: im.paste(sp, (int(x), int(y)), sp)
        return im

FURNITURE = ("DSK", "CHR", "DEC", "PLT", "TEC", "MON", "PET", "FOD")   # pieces that stand in the room (wall art is above the floor anyway)
FLAT = ("WALL", "fbFLR", "FLR", "SHL", "RUG", "WIN")                     # always behind whoever stands on the floor

def depth_layer(st, feet_y):
    """The layer name after which something whose feet are at feet_y is drawn: before the first layer holding a piece that
    stands in front of it (its bottom edge lower on screen), after everything flat."""
    prev = None
    for name, uses, _ in st.layers:
        for sid, x, y in uses:
            if sid.startswith(FLAT) or not sid.startswith(FURNITURE): continue
            if y + piece(st, sid).height > feet_y: return prev or name
        prev = name
    return prev

def component(path):
    """A kit component board (CHR-01.dc.html ...) as RGBA at native size (its viewBox)."""
    html = open(path, encoding="utf-8").read()
    m = re.search(r'<svg[^>]*viewBox="([^"]+)"[^>]*>(.*?)</svg>', html, re.S)
    x0, y0, w, h = [int(float(v)) for v in m.group(1).split()]
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); px = im.load()
    for x, y, rw, rh, col in _rects(m.group(2)):
        for yy in range(max(0, y), min(h, y + rh)):
            for xx in range(max(0, x), min(w, x + rw)):
                if col[3] == 255: px[xx, yy] = col
                else:
                    r, g, b, a0 = px[xx, yy]; k = col[3] / 255
                    px[xx, yy] = (int(r + (col[0] - r) * k), int(g + (col[1] - g) * k), int(b + (col[2] - b) * k), max(a0, col[3]))
    return im

class Set:
    """A room built from kit components in code (same depth rules as a Stage): wall tiles, floor tiles, then pieces in layers.
    Pieces are placed by their bottom edge; a piece that stands on the floor gets a floor shadow if you pass one."""
    def __init__(self, w=W, h=H): self.w, self.h = w, h; self.layers = []; self.title = "set"
    def layer(self, name): self.layers.append((name, [])); return self
    def add(self, name, im, x, bottom):
        for n, items in self.layers:
            if n == name: items.append((im, x, bottom - im.height)); return self
        self.layers.append((name, [(im, x, bottom - im.height)])); return self
    def tile(self, name, im, y0, y1, x0=0):
        for n, items in self.layers:
            if n == name: lst = items; break
        else: lst = []; self.layers.append((name, lst))
        for y in range(y0, y1, im.height):
            for x in range(x0 - im.width, self.w + im.width, im.width): lst.append((im.crop((0, 0, im.width, min(im.height, y1 - y))), x, y))
        return self
    def render(self, extra=None):
        im = Image.new("RGBA", (self.w, self.h), (0, 0, 0, 0)); extra = extra or {}
        for name, items in self.layers:
            for sp, x, y in items: im.alpha_composite(sp, (int(x), int(y))) if x >= 0 and y >= 0 and x + sp.width <= self.w and y + sp.height <= self.h else im.paste(sp, (int(x), int(y)), sp)
            for sp, x, y in extra.get(name, []): im.alpha_composite(sp, (int(x), int(y))) if x >= 0 and y >= 0 and x + sp.width <= self.w and y + sp.height <= self.h else im.paste(sp, (int(x), int(y)), sp)
        return im
    def bottoms(self):
        return [(n, max([y + sp.height for sp, x, y in items] or [0])) for n, items in self.layers]

def load(path):
    key = os.path.abspath(path)
    if key not in _CACHE: _CACHE[key] = Stage(path)
    return _CACHE[key]
_CACHE = {}

def piece(st, name):
    """One kit piece (symbol) at native size, cropped to its drawing."""
    kind, a, b = st.symbols[name]; rects = (b or []) if kind == "uses" else a
    if kind == "uses":
        im = Image.new("RGBA", (W * 2, H * 2)); st.draw_symbol(im, name, 0, 0); return im.crop(im.getbbox())
    x0 = min(r[0] for r in rects); y0 = min(r[1] for r in rects); x1 = max(r[0] + r[2] for r in rects); y1 = max(r[1] + r[3] for r in rects)
    im = Image.new("RGBA", (x1, y1)); st.draw_symbol(im, name, 0, 0); return im.crop((x0, y0, x1, y1))

def camera(im, x, y, w, h, k):
    """Crop a w x h native window at (x, y), padding with the edge colour where the window leaves the stage, and enlarge by k (NEAREST)."""
    pad = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    pad.alpha_composite(im.crop((x, y, x + w, y + h))) if 0 <= x and 0 <= y and x + w <= im.width and y + h <= im.height else pad.paste(im, (-x, -y), im)
    return pad.resize((w * k, h * k), Image.NEAREST)
