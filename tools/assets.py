"""ASSET LIBRARY (the boss 2026-11-01): "work on assets... save them somewhere they can be reused... pull building 3 from the asset list".
Every asset has a stable ID (PIG-01, BLD-03...). Each one is a generator here, rendered at its native pixel size, saved to
tools/assets/lib/<ID>.png and listed in tools/assets/lib/registry.json. Videos pull them with:

    import assets; im = assets.get("BLD-02")            # RGBA PIL image at native size
    im = assets.get("BLD-02", t=1.3)                     # animated assets take a time (TVs, vacuums, tails)

The Mascot Designs canvas page "Asset library" shows every version as a vector artboard (python3 tools/assets.py canvas <dir>).
Iterate on ONE asset without re-rendering a video: bump its version (e.g. BLD-02 v2) and keep the old one on the canvas.

Scale (to keep everything consistent): the mascots are the 64x64 standard (figure ~45 px). In buildings, floors are 56 px
(12 ft, ~4.7 px/ft) and characters are the 0.5x "minis" (~23 px, about 5 ft). Windows are tall and set edge to edge."""
import os, sys, json, math, random
from PIL import Image, ImageDraw, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(HERE, "assets", "lib")
OUTLINE = (20, 14, 18, 255)

# ---------------------------------------------------------------- helpers
def ramp(base, n=5):
    """deep shade, shade, base, light, highlight from one colour (light from the top-left)."""
    r, g, b = base[:3]
    def mix(t, to): return tuple(int(c + (o - c) * t) for c, o in zip((r, g, b), to))
    return [mix(.5, (36, 16, 30)), mix(.26, (60, 30, 44)), (r, g, b), mix(.3, (255, 244, 226)), mix(.6, (255, 252, 244))]

def sphere(im, box, rp, shape="ellipse", light=(-.55, -.7, .5), bands=(.16, .4, .7, .9), rim=True, poly=None):
    """Sphere shading inside a shape: per-pixel normal from the ellipse box, lambert term picks one of 5 tones; rim light low right."""
    x0, y0, x1, y1 = box; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; rx, ry = max(1, (x1 - x0) / 2), max(1, (y1 - y0) / 2)
    m = Image.new("L", im.size, 0); md = ImageDraw.Draw(m)
    if poly: md.polygon(poly, fill=255)
    else: getattr(md, shape)(box, fill=255)
    mp = m.load(); px = im.load(); lx, ly, lz = light; ln = (lx * lx + ly * ly + lz * lz) ** .5; lx, ly, lz = lx / ln, ly / ln, lz / ln
    for y in range(max(0, int(y0)), min(im.height, int(y1) + 1)):
        for x in range(max(0, int(x0)), min(im.width, int(x1) + 1)):
            if not mp[x, y]: continue
            nx, ny = (x + .5 - cx) / rx, (y + .5 - cy) / ry; r2 = min(1.0, nx * nx + ny * ny); nz = (1 - r2) ** .5
            lam = max(0.0, nx * lx + ny * ly + nz * lz) ** 1.3
            k = 0 if lam < bands[0] else 1 if lam < bands[1] else 2 if lam < bands[2] else 3 if lam < bands[3] else 4
            if rim and r2 > .8 and nx > .3 and ny > -.1 and k < 2: k = 2
            px[x, y] = rp[k] + (255,)

def outline(im, w=2, col=OUTLINE):
    a = im.split()[3].point(lambda v: 255 if v > 0 else 0)
    big = a.filter(ImageFilter.MaxFilter(2 * w + 1))
    out = Image.new("RGBA", im.size, (0, 0, 0, 0)); out.paste(Image.new("RGBA", im.size, col), (0, 0), big)
    return Image.alpha_composite(out, im)

def eye(d, x, y, big=True):
    """Mascot standard eye: black, white catchlight dot."""
    if big: d.rectangle([x, y, x + 3, y + 4], fill=(18, 12, 16)); d.rectangle([x + 1, y + 1, x + 1, y + 1], fill=(255, 255, 255))
    else: d.rectangle([x, y, x + 1, y + 2], fill=(18, 12, 16)); d.point((x, y), fill=(255, 255, 255))

# ---------------------------------------------------------------- PIGGY BANKS (64x64 standard grid)
PIGS = {
    "PIG-01": dict(name="Classic pink", base=(244, 150, 178), snout=(255, 186, 204), ear_in=(255, 196, 212), hoof=(150, 70, 96), slot=(84, 26, 48), deco=None),
    "PIG-02": dict(name="Lucky gold", base=(236, 184, 60), snout=(250, 214, 120), ear_in=(255, 230, 150), hoof=(150, 100, 30), slot=(90, 56, 10), deco="sparkle"),
    "PIG-03": dict(name="Ceramic blue-and-white", base=(236, 236, 230), snout=(246, 246, 242), ear_in=(214, 226, 246), hoof=(60, 86, 150), slot=(40, 50, 90), deco="delft"),
}
def piggy(pid="PIG-01", t=0.0, coin=True):
    """64x64 piggy bank on the mascot standard: ~52x40 body with sphere shading, snout, two ears, big black eye with a white dot,
    blush, four stub legs, curly tail, coin slot (a gold coin peeking out), 2 px near-black outline."""
    v = PIGS[pid]; im = Image.new("RGBA", (64, 64)); d = ImageDraw.Draw(im)
    rp = ramp(v["base"]); sp = ramp(v["snout"])
    for x in (13, 22, 36, 45):                                                 # legs (behind)
        d.rounded_rectangle([x, 44, x + 6, 53], radius=2, fill=rp[1] + (255,)); d.rectangle([x, 51, x + 6, 53], fill=v["hoof"] + (255,))
    d.arc([3, 24, 11, 32], 60, 340, fill=rp[1] + (255,), width=2)              # tail curl
    sphere(im, (7, 17, 55, 51), rp)                                            # body
    d.polygon([(34, 20), (36, 13), (39, 10), (42, 11), (44, 15), (44, 21)], fill=rp[2] + (255,)); d.polygon([(37, 19), (38, 14), (40, 13), (42, 16), (42, 20)], fill=v["ear_in"] + (255,))   # near ear, soft and floppy
    d.point((43, 11), fill=rp[1] + (255,)); d.point((44, 12), fill=rp[1] + (255,))                                                       # tip folds over
    d.polygon([(26, 20), (28, 14), (31, 12), (33, 15), (33, 20)], fill=rp[1] + (255,))            # far ear
    sphere(im, (48, 27, 61, 41), sp)                                           # snout
    d.rectangle([52, 32, 53, 35], fill=rp[0] + (255,)); d.rectangle([56, 32, 57, 35], fill=rp[0] + (255,))   # nostrils
    eye(d, 42, 24)
    d.ellipse([40, 32, 46, 35], fill=(255, 120, 150, 170))                    # blush
    d.rounded_rectangle([22, 17, 32, 19], radius=1, fill=v["slot"] + (255,))   # coin slot
    if coin:
        bob = int(1.5 * math.sin(t * 6))
        d.rectangle([24, 13 + bob, 30, 18], fill=(240, 196, 60, 255)); d.rectangle([25, 13 + bob, 26, 15 + bob], fill=(255, 238, 170, 255)); d.rectangle([29, 13 + bob, 30, 17], fill=(186, 130, 30, 255))
    if v["deco"] == "delft":   # hand-painted blue flowers and a band
        for cx, cy in ((18, 30), (30, 40), (24, 26), (38, 44)):
            for dx, dy in ((0, -2), (2, 0), (0, 2), (-2, 0)): d.point((cx + dx, cy + dy), fill=(60, 90, 170, 255))
            d.point((cx, cy), fill=(30, 50, 120, 255))
        d.line([(9, 37), (54, 37)], fill=(60, 90, 170, 255), width=1)
        for x in range(11, 52, 4): d.point((x, 36), fill=(60, 90, 170, 255))
    if v["deco"] == "sparkle":
        k = int(t * 4) % 3
        for i, (sx, sy) in enumerate(((14, 22), (50, 16), (20, 46))):
            if i == k or t == 0.0:
                d.point([(sx, sy - 2), (sx, sy - 1), (sx, sy + 1), (sx, sy + 2), (sx - 2, sy), (sx - 1, sy), (sx + 1, sy), (sx + 2, sy)], fill=(255, 252, 230, 255)); d.point((sx, sy), fill=(255, 255, 255, 255))
    return outline(im, 2)

# ---------------------------------------------------------------- characters at building scale ("minis")
_SPR = {}
MINI_SCALE = .52
def mini(name, t=0.0, flip=False):
    """0.5x mascot (about 5 ft against a 12 ft floor): downscaled smoothly, alpha snapped, so eyes stay readable.
    MINI_SCALE sets the size (V2.01 buildings use ~0.26: about 11-12 px tall)."""
    key = (name, MINI_SCALE)
    if key not in _SPR:
        f = {"theo": "theo_sprite_1x", "penny": "penny_sprite_1x", "ada": "ada_teal_1x", "roz": "roz_sprite_1x", "kit": "kit_sprite_1x", "boss": "boss_shadow_1x"}[name]
        im = Image.open(os.path.join(HERE, "sprites", f + ".png")).convert("RGBA"); bb = im.getbbox(); im = im.crop(bb)
        sm = im.resize((max(1, round(im.width * MINI_SCALE)), max(1, round(im.height * MINI_SCALE))), Image.LANCZOS)
        r, g, b, a = sm.split(); a = a.point(lambda v: 255 if v > 110 else 0); _SPR[key] = Image.merge("RGBA", (r, g, b, a))
    s = _SPR[key]
    return s.transpose(Image.FLIP_LEFT_RIGHT) if flip else s
def put(im, sp, x, floor_y):
    """paste a mini with its feet on floor_y, centred on x."""
    im.alpha_composite(sp, (int(x - sp.width / 2), int(floor_y - sp.height)))

# ---------------------------------------------------------------- room interiors (shared by every building)
LIGHT = {"2700K": (255, 184, 110), "3000K": (255, 200, 140), "3500K": (255, 214, 168), "4000K": (255, 232, 204), "5000K": (226, 236, 255), "red": (232, 82, 76), "purple": (178, 104, 226), "teal": (90, 206, 196), "tv": (110, 150, 230)}
def room(w, h, kind, temp="3000K", t=0.0, seed=0, who=None):
    """One room, w x h, floor at the bottom, lit by `temp`. kinds: living, kitchen, vacuum, trading, studio, bedroom, gym, cat, dog,
    plant, party, dark. `who` = a mini to put in it. Returns RGBA (opaque)."""
    r = random.Random(seed); L = LIGHT[temp]
    im = Image.new("RGBA", (w, h), L + (255,)); d = ImageDraw.Draw(im)
    if kind == "dark":
        d.rectangle([0, 0, w, h], fill=(16, 16, 26, 255)); return im
    wall2 = tuple(int(c * .82) for c in L); d.rectangle([0, 0, w, int(h * .18)], fill=wall2 + (255,))            # ceiling shade
    d.rectangle([0, h - 6, w, h], fill=tuple(int(c * .5) for c in L) + (255,))                                      # floor
    lamp = (w // 2 + r.randint(-w // 4, w // 4)); d.line([(lamp, 0), (lamp, 6)], fill=(40, 36, 40, 255)); d.rectangle([lamp - 3, 6, lamp + 3, 9], fill=(255, 250, 230, 255))
    fy = h - 6
    if kind == "living":
        tvc = [(70, 130, 240), (240, 100, 90), (90, 220, 140), (250, 250, 250)][int(t * 3 + seed) % 4]
        d.rectangle([w - 22, fy - 22, w - 4, fy - 10], fill=(10, 10, 12, 255)); d.rectangle([w - 21, fy - 21, w - 5, fy - 11], fill=tvc + (255,)); d.rectangle([w - 18, fy - 10, w - 8, fy - 7], fill=(40, 34, 30, 255))
        d.rounded_rectangle([4, fy - 14, 30, fy - 2], radius=3, fill=(150, 70, 60, 255)); d.rectangle([4, fy - 20, 10, fy - 2], fill=(130, 58, 50, 255))
        if who: put(im, mini(who), 18, fy - 4)
    elif kind == "kitchen":
        d.rectangle([0, fy - 12, w, fy], fill=(230, 230, 228, 255)); d.rectangle([0, fy - 13, w, fy - 12], fill=(60, 60, 64, 255))
        d.rectangle([4, 10, 22, 18], fill=(200, 196, 190, 255)); d.rectangle([w - 14, fy - 30, w - 2, fy - 12], fill=(210, 214, 220, 255))   # cabinet, fridge
        d.rectangle([20, fy - 16, 30, fy - 13], fill=(40, 40, 44, 255))                                                                       # pan
        for i in range(3):   # steam
            sy = int((t * 18 + i * 6) % 14); d.point((24 + i * 2, fy - 18 - sy), fill=(255, 255, 255, 200))
        if who: put(im, mini(who, flip=True), 34, fy)
    elif kind == "vacuum":
        d.rectangle([w - 16, fy - 18, w - 2, fy], fill=(120, 80, 60, 255))                                             # dresser
        vx = 8 + int((math.sin(t * 2.2) * .5 + .5) * (w - 40))
        if who: put(im, mini(who), vx + 10, fy)
        d.line([(vx + 4, fy - 14), (vx, fy - 1)], fill=(60, 60, 70, 255), width=1); d.rectangle([vx - 4, fy - 3, vx + 4, fy], fill=(220, 60, 60, 255))   # upright vacuum
        for i in range(3): d.point((vx - 6 - i * 3, fy - 1), fill=(255, 255, 255, 160))                                 # dust puffs
    elif kind == "trading":
        d.rectangle([4, fy - 12, w - 4, fy - 10], fill=(90, 64, 40, 255))
        for i, mx in enumerate((8, 22, 36)):
            if mx + 12 > w - 4: break
            d.rectangle([mx, fy - 26, mx + 12, fy - 16], fill=(12, 12, 14, 255)); col = (200, 240, 60) if (i + int(t * 2)) % 2 else (255, 138, 91)
            pts = [(mx + 1 + k * 2, fy - 18 - r.randint(0, 6)) for k in range(6)]; d.line(pts, fill=col + (255,))
        if who: put(im, mini(who), w // 2, fy)
    elif kind == "studio":
        d.ellipse([6, fy - 30, 20, fy - 16], outline=(255, 255, 255, 255), width=2); d.line([(13, fy - 16), (13, fy)], fill=(50, 50, 50, 255))   # ring light
        d.rectangle([w - 18, fy - 22, w - 10, fy - 16], fill=(20, 20, 24, 255)); d.line([(w - 14, fy - 16), (w - 14, fy)], fill=(50, 50, 50, 255))   # camera
        if int(t * 2) % 2: d.point((w - 12, fy - 21), fill=(255, 40, 40, 255))
        if who: put(im, mini(who), w // 2 - 2, fy - int(3 * abs(math.sin(t * 6))))
    elif kind == "bedroom":
        d.rectangle([4, fy - 10, 36, fy], fill=(240, 236, 228, 255)); d.rectangle([4, fy - 12, 12, fy - 8], fill=(255, 255, 255, 255)); d.rectangle([12, fy - 10, 36, fy - 6], fill=(120, 150, 210, 255))
        d.rectangle([w - 12, fy - 14, w - 4, fy], fill=(140, 96, 60, 255)); d.rectangle([w - 10, fy - 22, w - 6, fy - 14], fill=(255, 230, 160, 255))   # nightstand lamp
        if who: put(im, mini(who), 26, fy - 8)
    elif kind == "gym":
        d.polygon([(6, fy), (36, fy), (36, fy - 4), (10, fy - 4)], fill=(40, 40, 46, 255)); d.line([(34, fy - 4), (32, fy - 22)], fill=(80, 80, 90, 255), width=2)
        if who: put(im, mini(who), 22, fy - 4 - int(2 * abs(math.sin(t * 10))))
    elif kind == "cat":
        cx = w // 2 + int(4 * math.sin(t * .8)); d.ellipse([cx - 6, fy - 6, cx + 4, fy], fill=(30, 24, 24, 255)); d.ellipse([cx + 2, fy - 9, cx + 8, fy - 3], fill=(30, 24, 24, 255))
        d.point([(cx + 3, fy - 10), (cx + 7, fy - 10)], fill=(30, 24, 24, 255)); d.point([(cx + 4, fy - 7), (cx + 6, fy - 7)], fill=(140, 255, 140, 255))
        d.line([(cx - 6, fy - 3), (cx - 10, fy - 8 + int(2 * math.sin(t * 3)))], fill=(30, 24, 24, 255))
    elif kind == "dog":
        cx = w // 2; wag = int(2 * math.sin(t * 12)); d.rectangle([cx - 8, fy - 7, cx + 4, fy - 2], fill=(160, 110, 60, 255)); d.rectangle([cx + 2, fy - 11, cx + 9, fy - 5], fill=(160, 110, 60, 255))
        d.point((cx + 7, fy - 9), fill=(20, 14, 10, 255)); d.line([(cx - 8, fy - 6), (cx - 12, fy - 10 + wag)], fill=(160, 110, 60, 255))
        for lx in (cx - 7, cx - 3, cx + 1, cx + 3): d.line([(lx, fy - 2), (lx, fy)], fill=(130, 86, 44, 255))
    elif kind == "plant":
        d.rectangle([w // 2 - 4, fy - 8, w // 2 + 4, fy], fill=(176, 96, 60, 255))
        for k in range(5): a = -2.6 + k * .55; d.ellipse([w // 2 + int(math.cos(a) * 8) - 4, fy - 14 + int(math.sin(a) * 6) - 4, w // 2 + int(math.cos(a) * 8) + 4, fy - 14 + int(math.sin(a) * 6) + 4], fill=(60 + k * 10, 150 + k * 8, 80, 255))
    elif kind == "party":
        for k in range(7): d.point((4 + k * (w // 7), 12 + int(3 * abs(math.sin(t * 7 + k)))), fill=[(200, 240, 60), (255, 150, 190), (120, 200, 255), (255, 210, 80)][k % 4] + (255,))
        for k, n in enumerate(("penny", "kit")):
            put(im, mini(n, flip=k == 1), 12 + k * 22, fy - int(3 * abs(math.sin(t * 8 + k * 1.7))))
    if r.random() < .45:   # curtains
        cc = [(130, 40, 54), (60, 74, 130), (214, 204, 184), (70, 120, 86)][r.randint(0, 3)] + (255,)
        d.polygon([(0, 0), (6, 0), (3, h), (0, h)], fill=cc); d.polygon([(w, 0), (w - 6, 0), (w - 3, h), (w, h)], fill=cc)
    return im

# ---------------------------------------------------------------- BUILDINGS
def _bricks(d, x0, y0, x1, y1, base, mortar, rh=3, seed=1):
    r = random.Random(seed); d.rectangle([x0, y0, x1, y1], fill=base)
    for y in range(y0, y1, rh):
        d.line([(x0, y), (x1, y)], fill=mortar); off = 0 if (y // rh) % 2 else 3
        for x in range(x0 + off, x1, 7): d.point((x, y + 1), fill=mortar)
    for _ in range((x1 - x0) * (y1 - y0) // 40):   # weathering speckle
        x = r.randint(x0, x1 - 1); y = r.randint(y0, y1 - 1); d.point((x, y), fill=tuple(max(0, c - 14) for c in base[:3]) + (255,))

def _window(im, x, y, w, h, kind, temp, t, seed, who=None, frame=(30, 26, 30, 255), arch=False, mullion=True):
    rm = room(w, h, kind, temp, t, seed, who); m = None
    if arch:
        m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rectangle([0, w // 2, w, h], fill=255); ImageDraw.Draw(m).ellipse([0, 0, w - 1, w], fill=255)
    im.paste(rm, (x, y), m)
    d = ImageDraw.Draw(im)
    if arch: d.arc([x - 1, y - 1, x + w, y + w + 1], 180, 360, fill=frame, width=2); d.line([(x - 1, y + w // 2), (x - 1, y + h)], fill=frame, width=2); d.line([(x + w, y + w // 2), (x + w, y + h)], fill=frame, width=2); d.line([(x - 1, y + h), (x + w, y + h)], fill=frame, width=2)
    else: d.rectangle([x - 1, y - 1, x + w, y + h], outline=frame, width=2)
    if mullion: d.line([(x + w // 2, y + (w // 2 if arch else 0)), (x + w // 2, y + h)], fill=frame); d.line([(x, y + int(h * .55)), (x + w, y + int(h * .55))], fill=frame)

def brownstone(t=0.0):
    """BLD-01 · Brownstone: four storeys over a garden level, high stoop with iron railings, carved door hood, bay of tall windows,
    bracketed cornice, flower boxes, a tree pit and gas lamp. Warm light, a cat, Theo reading, Penny cooking."""
    Wd, Hd = 220, 360; im = Image.new("RGBA", (Wd, Hd)); d = ImageDraw.Draw(im)
    BR = (118, 70, 52, 255); BRL = (140, 88, 66, 255); BRD = (86, 48, 36, 255); TRIM = (160, 112, 86, 255)
    _bricks(d, 10, 40, 210, 330, BR, (100, 58, 42, 255), rh=4, seed=3)
    for y in range(40, 330, 56): d.rectangle([10, y, 210, y + 2], fill=BRL)           # rustication bands
    # cornice with brackets
    d.rectangle([4, 26, 216, 40], fill=(70, 46, 36, 255)); d.rectangle([4, 26, 216, 28], fill=(150, 104, 80, 255)); d.rectangle([4, 38, 216, 40], fill=BRD)
    for x in range(12, 210, 20): d.rectangle([x, 40, x + 5, 48], fill=(70, 46, 36, 255)); d.point((x + 1, 41), fill=(150, 104, 80, 255))
    # windows: 4 floors x 3 bays, tall (about 9 ft of a 12 ft floor), stone lintels and sills
    temps = ["3000K", "2700K", "3500K", "4000K", "2700K", "3000K", "dark", "3500K", "2700K", "3000K", "2700K", "4000K"]
    kinds = ["bedroom", "cat", "plant", "living", "kitchen", "plant", "dark", "living", "plant", "studio", "trading", "dog"]
    who = {3: "theo", 4: "penny", 9: "ada", 10: "roz"}
    k = 0
    for fl, y in enumerate((60, 116, 172, 228)):
        for bx in (34, 92, 150):
            _window(im, bx, y, 36, 44, kinds[k], temps[k] if kinds[k] != "dark" else "3000K", t, k + 10, who.get(k), arch=(fl == 0))
            d.rectangle([bx - 4, y - 5, bx + 40, y - 2], fill=TRIM); d.rectangle([bx - 4, y - 5, bx + 40, y - 5], fill=(190, 150, 120, 255))   # lintel
            d.rectangle([bx - 3, y + 45, bx + 39, y + 47], fill=TRIM)                                                                          # sill
            if fl == 3 or (fl == 2 and bx != 150):                                                                                              # flower boxes
                d.rectangle([bx - 2, y + 47, bx + 38, y + 51], fill=(80, 50, 34, 255))
                for fx in range(bx, bx + 37, 3): d.point((fx, y + 46 - (fx % 2)), fill=[(230, 80, 110, 255), (250, 210, 80, 255), (90, 170, 80, 255)][(fx // 3) % 3])
            k += 1
    # garden level + stoop
    d.rectangle([10, 288, 210, 330], fill=BRD); _bricks(d, 10, 290, 120, 330, (98, 58, 44, 255), (80, 46, 34, 255), rh=4, seed=8)
    _window(im, 30, 296, 30, 26, "kitchen", "3000K", t, 31, None)
    d.rectangle([28, 294, 62, 296], fill=TRIM)
    for i in range(8): d.rectangle([140 - i * 6, 288 + i * 6, 210, 294 + i * 6], fill=(150, 104, 80, 255) if i % 2 == 0 else (128, 86, 64, 255))   # stoop steps
    d.line([(134, 280), (92, 334)], fill=(24, 22, 24, 255), width=2); d.line([(206, 280), (206, 334)], fill=(24, 22, 24, 255), width=2)            # railings
    for i in range(8): d.line([(134 - i * 5, 280 + i * 6), (134 - i * 5, 286 + i * 6)], fill=(24, 22, 24, 255))
    d.ellipse([131, 276, 137, 282], fill=(24, 22, 24, 255))                                                                                         # newel ball
    # front door with hood
    d.rectangle([156, 240, 196, 288], fill=(70, 40, 30, 255)); d.rectangle([152, 232, 200, 240], fill=TRIM); d.polygon([(150, 232), (202, 232), (198, 226), (154, 226)], fill=(176, 130, 100, 255))
    d.rectangle([160, 246, 174, 284], fill=(58, 34, 26, 255)); d.rectangle([178, 246, 192, 284], fill=(58, 34, 26, 255)); d.rectangle([160, 242, 192, 246], fill=(255, 214, 150, 255))   # double doors, transom glow
    d.point([(174, 266), (178, 266)], fill=(240, 200, 90, 255))
    # sidewalk, tree pit, lamp
    d.rectangle([0, 330, Wd, Hd], fill=(80, 80, 86, 255)); d.rectangle([0, 330, Wd, 332], fill=(120, 120, 126, 255))
    for x in range(0, Wd, 24): d.line([(x, 332), (x, Hd)], fill=(66, 66, 72, 255))
    d.rectangle([2, 312, 6, 330], fill=(30, 30, 34, 255)); d.rectangle([0, 304, 8, 312], fill=(255, 226, 150, 255)); d.rectangle([-1, 302, 9, 304], fill=(30, 30, 34, 255))   # gas lamp
    return outline(im, 1)

def glass_tower(t=0.0):
    """BLD-02 · Glass skyscraper cutaway: a slim all-glass tower, 7 residential floors you can see into, each one a room where
    the cast lives: Ada vacuuming, Roz cooking, Theo at his screens, Penny filming, Kit asleep, the boss's gym (shadow), a party.
    Blue-teal glass with diagonal reflections, thin mullions, floor slabs, a crown with a beacon, a lit lobby."""
    Wd, Hd = 260, 520; im = Image.new("RGBA", (Wd, Hd)); d = ImageDraw.Draw(im)
    X0, X1 = 20, 240; FH = 56
    # crown
    d.polygon([(X0 + 20, 70), (X1 - 20, 70), (X1 - 50, 30), (X0 + 50, 30)], fill=(60, 84, 110, 255)); d.line([(Wd // 2, 30), (Wd // 2, 6)], fill=(180, 190, 200, 255), width=2)
    if int(t * 2) % 2 == 0: d.ellipse([Wd // 2 - 3, 2, Wd // 2 + 3, 8], fill=(255, 60, 60, 255))
    d.rectangle([X0, 70, X1, 80], fill=(40, 52, 66, 255))
    floors = [  # (kind, light, who) per bay, 3 bays per floor
        [("party", "purple", None), ("living", "3500K", "kit"), ("plant", "4000K", None)],
        [("trading", "5000K", "theo"), ("trading", "5000K", None), ("cat", "3000K", None)],
        [("kitchen", "3500K", "roz"), ("living", "2700K", None), ("dog", "3000K", None)],
        [("vacuum", "4000K", "ada"), ("bedroom", "2700K", None), ("plant", "3500K", None)],
        [("studio", "5000K", "penny"), ("living", "tv", None), ("dark", "3000K", None)],
        [("gym", "4000K", "boss"), ("kitchen", "3000K", None), ("bedroom", "2700K", "kit")],
        [("living", "red", None), ("cat", "2700K", None), ("vacuum", "3500K", "penny")],
    ]
    bw = (X1 - X0) // 3
    for fi, row in enumerate(floors):
        y = 82 + fi * FH
        for bi, (kd, tp, who) in enumerate(row):
            rm = room(bw, FH - 4, kd, tp, t, fi * 3 + bi + 40, who); im.paste(rm, (X0 + bi * bw, y))
        d.rectangle([X0, y + FH - 4, X1, y + FH], fill=(34, 40, 50, 255))           # slab
        d.rectangle([X0, y + FH - 4, X1, y + FH - 4], fill=(90, 104, 120, 255))
    # glass: tint + diagonal reflections + mullions
    tint = Image.new("RGBA", (Wd, Hd), (0, 0, 0, 0)); td = ImageDraw.Draw(tint)
    td.rectangle([X0, 82, X1, 82 + 7 * FH], fill=(60, 150, 190, 46))
    for k, (x, wdt) in enumerate(((X0 - 40, 30), (X0 + 60, 12), (X0 + 120, 40), (X0 + 210, 16))):
        td.polygon([(x, 82 + 7 * FH), (x + wdt, 82 + 7 * FH), (x + wdt + 180, 82), (x + 180, 82)], fill=(220, 240, 255, 34 + 8 * (k % 2)))
    clip = Image.new("L", (Wd, Hd), 0); ImageDraw.Draw(clip).rectangle([X0, 82, X1, 82 + 7 * FH], fill=255)
    tint.putalpha(Image.composite(tint.split()[3], Image.new("L", (Wd, Hd), 0), clip)); im.alpha_composite(tint)
    for x in range(X0, X1 + 1, bw // 2): d.line([(x, 80), (x, 82 + 7 * FH)], fill=(150, 176, 196, 255) if (x - X0) % bw == 0 else (100, 124, 146, 255))
    d.line([(X0, 80), (X0, 82 + 7 * FH)], fill=(200, 216, 230, 255), width=2); d.line([(X1, 80), (X1, 82 + 7 * FH)], fill=(70, 86, 104, 255), width=2)
    # lobby
    ly = 82 + 7 * FH
    d.rectangle([X0 - 6, ly, X1 + 6, ly + 6], fill=(50, 58, 70, 255)); d.rectangle([X0, ly + 6, X1, Hd - 14], fill=(255, 232, 196, 255))
    d.rectangle([X0, ly + 6, X1, ly + 10], fill=(210, 190, 160, 255)); d.rectangle([Wd // 2 - 20, ly + 20, Wd // 2 + 20, Hd - 14], fill=(200, 230, 240, 255))
    d.line([(Wd // 2, ly + 20), (Wd // 2, Hd - 14)], fill=(120, 140, 150, 255)); put(im, mini("theo"), X0 + 30, Hd - 14)
    for x in range(X0, X1, 36): d.line([(x, ly + 6), (x, Hd - 14)], fill=(150, 140, 120, 255))
    d.rectangle([0, Hd - 14, Wd, Hd], fill=(78, 78, 84, 255)); d.rectangle([0, Hd - 14, Wd, Hd - 13], fill=(120, 120, 126, 255))
    return outline(im, 1)

def prewar(t=0.0):
    """BLD-03 · Prewar high-rise (the trailer building, refined): red-brown brick, limestone base, fire escape zigzag, water tank,
    floor-to-ceiling-ish tall windows in mixed light temperatures, curtains, a TV, pets, cameos."""
    Wd, Hd = 220, 420; im = Image.new("RGBA", (Wd, Hd)); d = ImageDraw.Draw(im)
    _bricks(d, 10, 60, 210, 380, (128, 58, 44, 255), (104, 46, 34, 255), rh=3, seed=11)
    d.rectangle([4, 52, 216, 62], fill=(186, 170, 150, 255)); d.rectangle([4, 52, 216, 53], fill=(220, 208, 190, 255))     # parapet
    d.rectangle([150, 14, 196, 50], fill=(110, 80, 56, 255)); d.polygon([(146, 14), (200, 14), (173, 2)], fill=(80, 60, 46, 255))   # water tank
    for x in range(152, 196, 6): d.line([(x, 14), (x, 50)], fill=(90, 64, 44, 255))
    for x in (154, 166, 180, 192): d.line([(x, 50), (x, 54)], fill=(40, 34, 30, 255), width=2)
    kinds = ["living", "cat", "kitchen", "dark", "plant", "vacuum", "trading", "living", "bedroom", "dog", "studio", "party", "plant", "living", "cat", "kitchen", "dark", "gym", "living", "bedroom"]
    temps = ["5000K", "2700K", "3500K", "3000K", "teal", "4000K", "5000K", "tv", "2700K", "3000K", "5000K", "purple", "3500K", "red", "2700K", "3000K", "3000K", "4000K", "tv", "2700K"]
    who = {2: "roz", 5: "ada", 6: "theo", 10: "penny", 13: "kit"}
    k = 0
    for y in range(70, 330, 56):
        d.rectangle([10, y + 48, 210, y + 50], fill=(150, 120, 100, 255))
        for x in (22, 70, 118, 166):
            _window(im, x, y, 34, 46, kinds[k % 20], temps[k % 20], t, k + 70, who.get(k)); k += 1
    # fire escape on the right two bays
    FE = (24, 22, 26, 255)
    for i, y in enumerate(range(116, 330, 56)):
        d.rectangle([112, y, 206, y + 2], fill=FE); d.line([(112, y - 8), (206, y - 8)], fill=FE)
        for x in range(112, 207, 6): d.line([(x, y - 8), (x, y)], fill=FE)
        a, b = (120, 198) if i % 2 == 0 else (198, 120); d.line([(a, y + 2), (b, y + 54)], fill=FE, width=2)
    # limestone base, shop, entrance
    d.rectangle([4, 330, 216, 392], fill=(196, 182, 162, 255))
    for y in range(334, 392, 8): d.line([(4, y), (216, y)], fill=(170, 156, 136, 255))
    d.rectangle([20, 344, 90, 384], fill=(255, 220, 160, 255)); d.rectangle([16, 338, 94, 344], fill=(40, 90, 70, 255))     # shop + awning
    for x in range(16, 95, 8): d.polygon([(x, 344), (x + 8, 344), (x + 4, 348)], fill=(40, 90, 70, 255))
    put(im, mini("penny"), 40, 384); d.rectangle([60, 360, 86, 376], fill=(230, 210, 170, 255))
    d.rectangle([140, 344, 180, 392], fill=(60, 40, 30, 255)); d.rectangle([136, 338, 184, 344], fill=(140, 110, 80, 255)); d.rectangle([146, 350, 174, 392], fill=(255, 210, 140, 255))
    d.rectangle([0, 392, Wd, Hd], fill=(80, 80, 86, 255))
    return outline(im, 1)

def deco_tower(t=0.0):
    """BLD-04 · Art deco tower at night: setbacks, a stepped crown with sunburst arches lit gold, vertical piers, spandrel ornament."""
    Wd, Hd = 220, 520; im = Image.new("RGBA", (Wd, Hd)); d = ImageDraw.Draw(im)
    ST = (196, 188, 170, 255); STD = (150, 142, 126, 255); GOLD = (232, 190, 90, 255)
    d.line([(110, 0), (110, 40)], fill=(200, 200, 210, 255), width=2)
    for i, (w, y) in enumerate(((20, 40), (34, 60), (50, 84), (64, 108))):                                     # stepped crown
        d.rectangle([110 - w, y, 110 + w, y + 24], fill=STD)
        for k in range(-w + 6, w - 4, 10): d.arc([110 + k - 4, y + 4, 110 + k + 4, y + 16], 180, 360, fill=GOLD, width=2)
        for k in range(-w + 6, w - 4, 10):
            if (i + k // 10 + int(t * 3)) % 3: d.rectangle([110 + k - 1, y + 10, 110 + k + 1, y + 20], fill=(255, 226, 140, 255))
    d.rectangle([30, 132, 190, 470], fill=ST)                                                                     # shaft
    for x in range(30, 191, 20): d.rectangle([x, 132, x + 3, 470], fill=(220, 214, 198, 255))                     # piers
    k = 0
    for y in range(140, 460, 30):
        for x in range(34, 186, 20):
            tp = ["3000K", "2700K", "5000K", "dark", "3500K", "tv", "2700K", "dark", "4000K"][(k * 5) % 9]
            kd = "dark" if tp == "dark" else ["living", "plant", "cat", "bedroom", "kitchen", "trading"][(k * 7) % 6]
            _window(im, x, y, 15, 24, kd, "3000K" if tp == "dark" else tp, t, k + 120, None, frame=STD, mullion=False); k += 1
            d.rectangle([x, y + 25, x + 15, y + 28], fill=(170, 160, 140, 255))
            for zx in range(x + 1, x + 15, 4): d.line([(zx, y + 26), (zx + 2, y + 27)], fill=GOLD)                  # chevron spandrel
    for sx, sw in ((14, 16), (190, 16)): d.rectangle([sx, 300, sx + sw, 470], fill=STD)                          # lower setbacks
    d.rectangle([10, 470, 210, 506], fill=(60, 54, 48, 255)); d.rectangle([80, 476, 140, 506], fill=(255, 220, 150, 255))
    d.polygon([(76, 476), (144, 476), (110, 456)], fill=GOLD); put(im, mini("roz"), 100, 506); put(im, mini("kit"), 122, 506)
    d.rectangle([0, 506, Wd, Hd], fill=(80, 80, 86, 255))
    return outline(im, 1)

def loft(t=0.0):
    """BLD-05 · SoHo cast-iron loft: tall arched windows between fluted columns, painted cream iron, fire escapes, a studio inside."""
    Wd, Hd = 220, 360; im = Image.new("RGBA", (Wd, Hd)); d = ImageDraw.Draw(im)
    IR = (226, 216, 196, 255); IRD = (180, 168, 146, 255)
    d.rectangle([8, 30, 212, 330], fill=IR); d.rectangle([4, 20, 216, 32], fill=IRD); d.rectangle([4, 20, 216, 21], fill=(250, 244, 230, 255))
    who = {1: "penny", 5: "theo", 6: "ada", 9: "roz"}
    k = 0
    for y in (44, 116, 188, 260):
        for x in (20, 70, 120, 170):
            kd = ["studio", "studio", "plant", "living", "party", "trading", "vacuum", "cat", "kitchen", "kitchen", "dog", "bedroom", "living", "plant", "dark", "gym"][k]
            tp = ["5000K", "4000K", "3000K", "2700K", "purple", "5000K", "3500K", "2700K", "3000K", "3500K", "3000K", "2700K", "tv", "3500K", "3000K", "4000K"][k]
            _window(im, x, y, 32, 60, kd, tp, t, k + 200, who.get(k), frame=IRD, arch=True); k += 1
        for x in (12, 62, 112, 162, 206):
            d.rectangle([x, y - 4, x + 4, y + 64], fill=IRD)
            for fy in range(y, y + 62, 3): d.point((x + 2, fy), fill=(150, 140, 120, 255))                         # fluting
        d.rectangle([8, y + 62, 212, y + 68], fill=IRD)
    FE = (24, 22, 26, 255)
    for y in (108, 180, 252):
        d.rectangle([60, y, 160, y + 2], fill=FE)
        for x in range(60, 161, 5): d.line([(x, y - 7), (x, y)], fill=FE)
        d.line([(60, y - 7), (160, y - 7)], fill=FE)
    d.rectangle([0, 330, Wd, Hd], fill=(80, 80, 86, 255))
    return outline(im, 1)

def bodega(t=0.0):
    """BLD-06 · Corner walk-up with a bodega: three floors over the shop, green awning, stacked produce, a shop cat on the counter,
    neon glow in the window (no words), a cameo on the stoop."""
    Wd, Hd = 220, 300; im = Image.new("RGBA", (Wd, Hd)); d = ImageDraw.Draw(im)
    _bricks(d, 10, 30, 210, 210, (196, 170, 120, 255), (170, 146, 100, 255), rh=3, seed=21)
    d.rectangle([4, 22, 216, 32], fill=(120, 96, 70, 255))
    k = 0
    for y in (42, 98, 154):
        for x in (24, 74, 124, 174):
            kd = ["living", "plant", "kitchen", "cat", "bedroom", "living", "dog", "plant", "trading", "dark", "living", "studio"][k]
            tp = ["tv", "3000K", "3500K", "2700K", "2700K", "red", "3000K", "4000K", "5000K", "3000K", "purple", "5000K"][k]
            _window(im, x, y, 26, 42, kd, tp, t, k + 300, {2: "roz", 8: "theo", 11: "penny"}.get(k)); k += 1
            d.rectangle([x - 2, y - 4, x + 28, y - 2], fill=(150, 120, 90, 255))
    # shop
    d.rectangle([10, 210, 210, 280], fill=(30, 30, 36, 255)); d.rectangle([4, 204, 216, 218], fill=(26, 110, 70, 255))
    for x in range(4, 216, 10): d.polygon([(x, 218), (x + 10, 218), (x + 5, 224)], fill=(26, 110, 70, 255))
    d.rectangle([18, 226, 120, 272], fill=(255, 236, 196, 255))
    glow = (255, 70, 140) if int(t * 2) % 2 else (255, 120, 180); d.rounded_rectangle([28, 232, 70, 246], radius=6, outline=glow + (255,), width=2)
    for i, c in enumerate(((230, 60, 40), (250, 200, 40), (90, 180, 60), (240, 130, 40))):                          # produce crates
        d.rectangle([20 + i * 24, 262, 40 + i * 24, 272], fill=(140, 96, 50, 255))
        for fx in range(22 + i * 24, 39 + i * 24, 4): d.ellipse([fx, 258, fx + 4, 262], fill=c + (255,))
    d.rectangle([84, 250, 118, 256], fill=(120, 80, 50, 255)); d.ellipse([96, 243, 106, 250], fill=(240, 160, 60, 255)); d.point([(98, 243), (104, 243)], fill=(240, 160, 60, 255))   # shop cat on the counter
    d.rectangle([134, 222, 170, 280], fill=(70, 50, 40, 255)); d.rectangle([140, 228, 164, 276], fill=(255, 214, 150, 255))
    put(im, mini("ada"), 190, 280)
    d.rectangle([0, 280, Wd, Hd], fill=(80, 80, 86, 255)); d.rectangle([0, 280, Wd, 281], fill=(120, 120, 126, 255))
    return outline(im, 1)


# ---------------------------------------------------------------- BLD-03 flavors, V2.02 (the boss 2026-11-01)
# "Windows not that close to the edge: invert it (thick wall on the open left side). No ground level, no street: from way up in
#  the air. Some at night. Decorative edges on top. Ornate window framing on the older brick ones; some not brick, solid facades."
FLAVORS = [  # name, facade kind, wall colour, trim colour, window head, top, time, fire escape, water tank
    ("Red brick · keystones", "brick", (150, 62, 46), (214, 200, 176), "keystone", "bracketed", "day", True, True),
    ("Red brick · keystones · night", "brick", (150, 62, 46), (214, 200, 176), "keystone", "bracketed", "night", True, True),
    ("Limestone · arched hoods", "stone", (222, 208, 182), (238, 228, 206), "hood", "balustrade", "day", False, False),
    ("Limestone · arched hoods · night", "stone", (222, 208, 182), (238, 228, 206), "hood", "balustrade", "night", False, False),
    ("Umber brick · pediments · night", "brick", (104, 58, 42), (196, 140, 98), "pediment", "crenel", "night", False, True),
    ("Sage stucco · dusk", "stucco", (148, 168, 140), (232, 226, 206), "simple", "copper", "dusk", True, False),
    ("Buff brick · copper crown · night", "brick", (204, 172, 120), (240, 230, 206), "segment", "copper", "night", True, True),
    ("Granite · deco · night", "stone", (92, 96, 108), (214, 178, 96), "deco", "deco", "night", False, False),
]
def _tone(c, k): return tuple(max(0, min(255, int(v * k))) for v in c[:3])
def _sky(d, Wd, Hd, time, r):
    bands = {"day": [(150, 196, 236), (164, 206, 240), (180, 216, 244), (196, 226, 246)],
             "dusk": [(70, 64, 120), (130, 86, 140), (214, 120, 120), (248, 176, 120)],
             "night": [(10, 14, 34), (14, 20, 46), (20, 28, 60), (28, 38, 74)]}[time]
    bh = Hd // len(bands)
    for i, c in enumerate(bands): d.rectangle([0, i * bh, Wd, (i + 1) * bh + 1], fill=c + (255,))
    if time == "night":
        for _ in range(40): x, y = r.randint(0, Wd - 1), r.randint(0, Hd // 2); d.point((x, y), fill=(250, 248, 230, 255) if r.random() < .3 else (170, 180, 210, 255))
        d.ellipse([Wd - 70, 26, Wd - 52, 44], fill=(246, 240, 214, 255)); d.ellipse([Wd - 64, 24, Wd - 48, 40], fill=bands[0] + (255,))   # crescent
    if time == "day":
        for cx, cy in ((40, 40), (180, 24), (250, 70)): d.rounded_rectangle([cx, cy, cx + 34, cy + 6], radius=3, fill=(248, 250, 252, 255)); d.rounded_rectangle([cx + 8, cy - 4, cx + 24, cy + 2], radius=3, fill=(248, 250, 252, 255))
    # far skyline (behind, lower), lit windows at night
    sk = {"day": (196, 212, 228), "dusk": (88, 70, 112), "night": (22, 28, 52)}[time]
    for i in range(14):
        bx = i * 26 - 10; top = 120 + r.randint(-40, 60); d.rectangle([bx, top, bx + 22, Hd], fill=sk + (255,))
        if time != "day":
            for wy in range(top + 6, Hd, 9):
                for wx in range(bx + 4, bx + 20, 6):
                    if r.random() < .22: d.point((wx, wy), fill=(255, 214, 140, 255) if r.random() < .8 else (180, 210, 255, 255))
def _frame(d, x, y, w, h, style, trim, wall):
    T, TD, TL = trim, _tone(trim, .72), _tone(trim, 1.12)
    d.rectangle([x - 2, y - 2, x + w + 1, y + h + 1], fill=TD + (255,))                                             # reveal
    d.rectangle([x - 3, y + h + 1, x + w + 2, y + h + 3], fill=T + (255,)); d.line([(x - 3, y + h + 1), (x + w + 2, y + h + 1)], fill=TL + (255,))   # sill
    if style in ("keystone", "pediment", "hood"):
        for bx in (x - 2, x + w - 1): d.rectangle([bx, y + h + 4, bx + 2, y + h + 5], fill=TD + (255,))          # sill corbels
    if style == "keystone":
        d.rectangle([x - 4, y - 7, x + w + 3, y - 3], fill=T + (255,)); d.line([(x - 4, y - 7), (x + w + 3, y - 7)], fill=TL + (255,))
        kx = x + w // 2; d.polygon([(kx - 4, y - 9), (kx + 3, y - 9), (kx + 2, y - 2), (kx - 3, y - 2)], fill=TL + (255,)); d.line([(kx + 3, y - 9), (kx + 2, y - 2)], fill=TD + (255,))
        for vx in range(x - 3, x + w + 3, 4): d.point((vx, y - 4), fill=TD + (255,))                               # voussoir joints
    elif style == "hood":
        d.chord([x - 5, y - 12, x + w + 4, y + 8], 180, 360, fill=T + (255,)); d.chord([x - 2, y - 8, x + w + 1, y + 6], 180, 360, fill=_tone(wall, .9) + (255,))
        d.arc([x - 5, y - 12, x + w + 4, y + 8], 180, 360, fill=TL + (255,))
        kx = x + w // 2; d.rectangle([kx - 2, y - 12, kx + 1, y - 6], fill=TL + (255,)); d.point((kx + 1, y - 7), fill=TD + (255,))
        d.rectangle([x - 6, y - 2, x - 3, y + 1], fill=T + (255,)); d.rectangle([x + w + 2, y - 2, x + w + 5, y + 1], fill=T + (255,))   # imposts
    elif style == "pediment":
        d.rectangle([x - 5, y - 5, x + w + 4, y - 3], fill=T + (255,)); d.polygon([(x - 5, y - 5), (x + w + 4, y - 5), (x + w // 2, y - 13)], fill=T + (255,))
        d.polygon([(x - 1, y - 6), (x + w, y - 6), (x + w // 2, y - 11)], fill=_tone(trim, .86) + (255,)); d.line([(x - 5, y - 5), (x + w // 2, y - 13)], fill=TL + (255,))
        d.point((x + w // 2, y - 8), fill=TL + (255,))                                                                  # rosette
    elif style == "segment":
        d.chord([x - 3, y - 7, x + w + 2, y + 4], 180, 360, fill=_tone(wall, .78) + (255,))
        for vx in range(x - 2, x + w + 2, 3): d.line([(vx, y - 5 + abs(vx - (x + w // 2)) // 8), (vx, y - 2)], fill=_tone(wall, .6) + (255,))
        kx = x + w // 2; d.rectangle([kx - 1, y - 8, kx + 1, y - 3], fill=T + (255,))
    elif style == "deco":
        for px in (x - 5, x + w + 2): d.rectangle([px, y - 4, px + 2, y + h + 6], fill=T + (255,)); d.point((px + 1, y - 4), fill=TL + (255,))
        d.rectangle([x - 2, y + h + 4, x + w + 1, y + h + 9], fill=_tone(wall, .8) + (255,))
        for zx in range(x, x + w, 6): d.line([(zx, y + h + 8), (zx + 3, y + h + 5), (zx + 6, y + h + 8)], fill=T + (255,))   # chevrons
    else:  # simple stucco band
        d.rectangle([x - 3, y - 4, x + w + 2, y - 3], fill=T + (255,))
def _top(d, x0, x1, y, kind, trim, wall, r):
    T, TD, TL = trim, _tone(trim, .72), _tone(trim, 1.12)
    if kind == "bracketed":
        d.rectangle([x0 - 6, y, x1, y + 10], fill=T + (255,)); d.line([(x0 - 6, y), (x1, y)], fill=TL + (255,)); d.line([(x0 - 6, y + 10), (x1, y + 10)], fill=TD + (255,))
        for dx in range(x0 - 4, x1, 4): d.rectangle([dx, y + 11, dx + 1, y + 13], fill=T + (255,))                 # dentils
        for bx in range(x0, x1, 18): d.polygon([(bx, y + 11), (bx + 5, y + 11), (bx + 5, y + 20), (bx + 2, y + 16)], fill=T + (255,)); d.line([(bx + 5, y + 11), (bx + 5, y + 20)], fill=TD + (255,))
        d.rectangle([x0 - 2, y - 8, x1, y - 1], fill=_tone(wall, .9) + (255,))                                         # parapet
        d.rectangle([x0 - 3, y - 10, x1, y - 8], fill=T + (255,))
    elif kind == "balustrade":
        d.rectangle([x0 - 4, y + 2, x1, y + 8], fill=T + (255,)); d.line([(x0 - 4, y + 2), (x1, y + 2)], fill=TL + (255,))
        for dx in range(x0 - 2, x1, 3): d.point((dx, y + 9), fill=TD + (255,))
        d.rectangle([x0 - 4, y - 16, x1, y - 14], fill=T + (255,)); d.rectangle([x0 - 4, y - 1, x1, y + 1], fill=T + (255,))
        for bx in range(x0, x1, 5): d.rectangle([bx + 1, y - 13, bx + 2, y - 2], fill=T + (255,)); d.point((bx + 1, y - 9), fill=TL + (255,))   # balusters
        for px in range(x0 - 4, x1, 46):
            d.rectangle([px, y - 18, px + 6, y + 1], fill=TL + (255,)); d.ellipse([px, y - 26, px + 6, y - 19], fill=T + (255,)); d.rectangle([px + 2, y - 28, px + 4, y - 26], fill=T + (255,))   # urns on piers
    elif kind == "crenel":
        d.rectangle([x0 - 4, y - 2, x1, y + 6], fill=T + (255,)); d.line([(x0 - 4, y - 2), (x1, y - 2)], fill=TL + (255,))
        for mx in range(x0 - 4, x1, 12): d.rectangle([mx, y - 12, mx + 6, y - 2], fill=_tone(wall, .95) + (255,)); d.rectangle([mx, y - 13, mx + 6, y - 12], fill=T + (255,))
        for dx in range(x0, x1, 6): d.rectangle([dx, y + 7, dx + 2, y + 9], fill=TD + (255,))
    elif kind == "copper":
        CU, CUL, CUD = (92, 160, 140), (140, 200, 176), (54, 104, 92)
        d.rectangle([x0 - 6, y - 2, x1, y + 8], fill=CU + (255,)); d.line([(x0 - 6, y - 2), (x1, y - 2)], fill=CUL + (255,)); d.line([(x0 - 6, y + 8), (x1, y + 8)], fill=CUD + (255,))
        for dx in range(x0 - 4, x1, 5): d.rectangle([dx, y + 9, dx + 2, y + 11], fill=CUD + (255,))
        for fx in range(x0, x1, 30):
            d.polygon([(fx, y - 2), (fx + 8, y - 2), (fx + 4, y - 16)], fill=CU + (255,)); d.line([(fx + 4, y - 16), (fx + 4, y - 22)], fill=CUD + (255,)); d.point((fx + 4, y - 23), fill=(240, 210, 120, 255))   # finials
        d.rectangle([x0 - 2, y - 6, x1, y - 3], fill=_tone(wall, .9) + (255,))
    elif kind == "deco":
        for i, (inset, hh) in enumerate(((0, 8), (20, 18), (44, 30))):
            d.rectangle([x0 + inset, y - hh, x1, y - hh + 8], fill=_tone(wall, 1.0 - .08 * i) + (255,)); d.line([(x0 + inset, y - hh), (x1, y - hh)], fill=T + (255,))
        for fx in range(x0 + 50, x1, 16):
            for k in range(3): d.line([(fx, y - 22), (fx - 6 + k * 6, y - 30)], fill=T + (255,))                      # sunbursts
            d.point((fx, y - 31), fill=(255, 240, 180, 255))
def prewar_v3(n=0, t=0.0):
    """BLD-03 flavor n (0..7), 300x600, upper floors only (no street, no ground floor), thick wall on the visible left side."""
    global MINI_SCALE
    name, facade, wall, trim, head, top, time, fe, tank = FLAVORS[n]
    old = MINI_SCALE; MINI_SCALE = .27
    Wd, Hd = 300, 600; r = random.Random(300 + n)
    im = Image.new("RGBA", (Wd, Hd)); d = ImageDraw.Draw(im); _sky(d, Wd, Hd, time, r)
    X0, ROOF = 26, 96
    F = Image.new("RGBA", (Wd, Hd)); fd = ImageDraw.Draw(F)
    if facade == "brick": _bricks(fd, X0, ROOF, Wd, Hd, wall + (255,), _tone(wall, .82) + (255,), rh=3, seed=n)
    else:
        fd.rectangle([X0, ROOF, Wd, Hd], fill=wall + (255,))
        if facade == "stone":
            for y in range(ROOF + 14, Hd, 14): fd.line([(X0, y), (Wd, y)], fill=_tone(wall, .9) + (255,))          # ashlar courses
            for y in range(ROOF + 14, Hd, 28):
                for x in range(X0 + 18, Wd, 36): fd.line([(x, y), (x, y + 13)], fill=_tone(wall, .9) + (255,))
    fd.rectangle([X0, ROOF, X0 + 3, Hd], fill=_tone(wall, 1.12) + (255,))                                            # lit corner (light from the left)
    for y in range(ROOF + 8, Hd, 10): fd.rectangle([X0, y, X0 + 8, y + 7], fill=_tone(trim, .95) + (255,)) if facade == "brick" else None   # quoins on the corner
    if tank:
        tx = 160; fd.rectangle([tx, 28, tx + 46, 74], fill=(104, 74, 52, 255))
        for x in range(tx + 4, tx + 46, 6): fd.line([(x, 28), (x, 74)], fill=(84, 58, 40, 255))
        for yy in (38, 56): fd.line([(tx, yy), (tx + 46, yy)], fill=(60, 50, 44, 255))
        fd.polygon([(tx - 4, 28), (tx + 50, 28), (tx + 23, 10)], fill=(70, 52, 40, 255)); fd.line([(tx + 23, 10), (tx + 23, 6)], fill=(60, 50, 44, 255))
        for lx in (tx + 2, tx + 16, tx + 30, tx + 44): fd.line([(lx, 74), (lx, ROOF - 12)], fill=(40, 36, 36, 255), width=2)
    _top(fd, X0, Wd, ROOF, top, trim, wall, r)
    COLS = [64, 120, 176, 232]; WW, WH = 36, 46; ROWS = list(range(ROOF + 32, Hd, 58))
    for y in ROWS:
        for x in COLS: _frame(fd, x, y, WW, WH, head, trim, wall)
        if facade != "brick": fd.line([(X0, y + WH + 12), (Wd, y + WH + 12)], fill=_tone(wall, .88) + (255,))     # string course
    if time != "day":
        k = .56 if time == "night" else .74; tint = (.66, .74, 1.0) if time == "night" else (.92, .82, .92)
        px = F.load()
        for yy in range(Hd):
            for xx in range(Wd):
                c = px[xx, yy]
                if c[3]: px[xx, yy] = (int(c[0] * k * tint[0]), int(c[1] * k * tint[1]), int(c[2] * k * tint[2]), 255)
    im.alpha_composite(F)
    if time == "night":   # uplights wash the crown so the ornament reads at night (three stepped bands, no gradient)
        U = Image.new("RGBA", (Wd, Hd)); ud = ImageDraw.Draw(U)
        for i, (a, h0) in enumerate(((70, 34), (44, 22), (24, 12))): ud.rectangle([X0, ROOF - 30 + i * 0, Wd, ROOF + h0], fill=(255, 196, 120, a // 2))
        U.putalpha(Image.composite(U.split()[3], Image.new("L", (Wd, Hd), 0), F.split()[3])); im.alpha_composite(U)
        for lx in range(X0 + 30, Wd, 56): ImageDraw.Draw(im).rectangle([lx, ROOF + 22, lx + 2, ROOF + 24], fill=(255, 226, 160, 255))   # the lamps
    # windows: no two alike; the five residents once each, pets and empty rooms between
    kinds = ["living", "kitchen", "bedroom", "plant", "cat", "trading", "studio", "vacuum", "gym", "dog", "living", "bedroom", "plant", "kitchen", "cat", "living"]
    temps = ["2700K", "3000K", "3500K", "4000K", "5000K", "tv", "purple", "teal", "red"]
    cast = {3: "theo", 9: "penny", 14: "ada", 21: "roz", 27: "kit"}
    slots = [(x, y) for y in ROWS for x in COLS]; rr = random.Random(900 + n)
    order = list(range(len(slots))); rr.shuffle(order)
    for i, (x, y) in enumerate(slots):
        j = order[i]
        dark = (j % 8 == 5) or (time == "day" and j % 5 == 1) or (time != "day" and j % 3 == 0)   # nights: about a third of the windows dark
        if dark:
            rm = Image.new("RGBA", (WW, WH), ((22, 26, 44) if time != "day" else (60, 74, 96)) + (255,)); dd = ImageDraw.Draw(rm)
            dd.line([(4, WH - 6), (WW - 6, 6)], fill=((44, 52, 84) if time != "day" else (120, 140, 168)) + (255,))   # glass reflection
        else:
            who = cast.get(i); kd = kinds[(j * 7) % len(kinds)]
            if who and kd in ("cat", "dog", "plant"): kd = "living"
            rm = room(WW, WH, kd, temps[(j * 5) % len(temps)], t, 500 + n * 40 + j, who)
        im.alpha_composite(rm, (x, y))
        dd = ImageDraw.Draw(im); fc = _tone(trim, .55 if time == "day" else .3)
        dd.line([(x + WW // 2, y), (x + WW // 2, y + WH - 1)], fill=fc + (255,)); dd.line([(x, y + 20), (x + WW - 1, y + 20)], fill=fc + (255,))   # sash
        if time != "day" and not dark: dd.line([(x - 3, y + WH + 1), (x + WW + 2, y + WH + 1)], fill=(255, 210, 150, 255))  # warm light on the sill
    if fe:   # fire escape on the right two bays (away from the visible edge)
        E = Image.new("RGBA", (Wd, Hd)); ed = ImageDraw.Draw(E); FE = (28, 26, 30, 255) if time == "day" else (12, 12, 18, 255)
        for i, y in enumerate(ROWS):
            py = y + WH + 6; ed.rectangle([168, py, 276, py + 2], fill=FE); ed.line([(168, py - 9), (276, py - 9)], fill=FE)
            for x in range(168, 277, 4): ed.line([(x, py - 9), (x, py)], fill=FE)
            a, b = (180, 262) if i % 2 == 0 else (262, 180); ed.line([(a, py + 2), (b, py + 58)], fill=FE, width=2)
        im.alpha_composite(E)
    MINI_SCALE = old
    return outline(im.crop((0, 0, Wd, Hd)), 0) if False else im

REG = {
    "PIG-01": dict(kind="prop", v=1, fn=lambda t=0.0: piggy("PIG-01", t), title="Piggy bank · classic pink", grid="64x64 standard", scale=6),
    "PIG-02": dict(kind="prop", v=1, fn=lambda t=0.0: piggy("PIG-02", t), title="Piggy bank · lucky gold", grid="64x64 standard", scale=6),
    "PIG-03": dict(kind="prop", v=1, fn=lambda t=0.0: piggy("PIG-03", t), title="Piggy bank · ceramic blue-and-white", grid="64x64 standard", scale=6),
    "BLD-01": dict(kind="building", v=1, fn=brownstone, title="Brownstone", grid="220x360 · 56 px floors", scale=2),
    "BLD-02": dict(kind="building", v=1, fn=glass_tower, title="Glass tower · the cast at home", grid="260x520 · 56 px floors", scale=1.5),
    "BLD-03": dict(kind="building", v=1, fn=prewar, title="Prewar high-rise · fire escape + water tank", grid="220x420 · 56 px floors", scale=1.75),
    "BLD-04": dict(kind="building", v=1, fn=deco_tower, title="Art deco tower · lit crown", grid="220x520", scale=1.5),
    "BLD-05": dict(kind="building", v=1, fn=loft, title="SoHo cast-iron loft", grid="220x360 · 72 px floors", scale=2),
    "BLD-06": dict(kind="building", v=1, fn=bodega, title="Corner walk-up + bodega", grid="220x300 · 56 px floors", scale=2),
}
for _i, _f in enumerate(FLAVORS):
    REG[f"BLD-03-F{_i + 1}"] = dict(kind="building", v="2.02", fn=(lambda t=0.0, n=_i: prewar_v3(n, t)), title=f"BLD-03 · flavor {_i + 1} · {_f[0]}", grid="300x600 · upper floors only · 58 px floors", scale=1.5)
def get(aid, t=0.0):
    """The asset as RGBA at native size. Pass t for animated bits (TVs, vacuums, steam, tails, the beacon)."""
    import approved; approved.check("asset", aid)   # the star gate (the boss 2026-11-02)
    return REG[aid]["fn"](t)

# ---------------------------------------------------------------- canvas artboards (vector: one <rect> per same-colour run)
def svg(im, scale):
    px = im.load(); out = []
    for y in range(im.height):
        x = 0
        while x < im.width:
            c = px[x, y]
            if c[3] == 0: x += 1; continue
            x2 = x
            while x2 + 1 < im.width and px[x2 + 1, y] == c: x2 += 1
            out.append(f'<rect x="{x}" y="{y}" width="{x2 - x + 1}" height="1" fill="#{c[0]:02X}{c[1]:02X}{c[2]:02X}"/>'); x = x2 + 1
    return f'<svg width="{int(im.width * scale)}" height="{int(im.height * scale)}" style="display: block" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {im.width} {im.height}" shape-rendering="crispEdges">' + "".join(out) + "</svg>"
def artboard(aid, im, w, h, note, bg="#0E1018", accent="#C8F03C"):
    r = REG[aid]
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{aid} {r["title"]}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&amp;family=IBM+Plex+Mono:wght@400;500;600;700&amp;display=swap">
<style>body{{margin:0;background:#000000}}</style>
</helmet>
<div style="width: {w}px; height: {h}px; box-sizing: border-box; padding: 32px; outline: 10px solid {accent}; outline-offset: -10px; background: #000000; color: #F2F2EE; font-family: 'Archivo', 'Helvetica Neue', sans-serif; display: flex; flex-direction: column; gap: 14px">
<div style="display: flex; justify-content: space-between; font-family: 'IBM Plex Mono', monospace; font-size: 12px; letter-spacing: 1px; color: #9A9A94"><span>&#8776; ROUNDING ERROR &#183; ASSET LIBRARY</span><span>{aid} &#183; V{r["v"]}</span></div>
<div style="flex: 1; display: flex; justify-content: center; align-items: center; background: {bg}">{svg(im, r["scale"])}</div>
<div style="display: flex; align-items: baseline; gap: 14px"><h1 style="margin: 0; font-size: 34px; font-weight: 900; font-stretch: 125%; letter-spacing: -1px">{aid}</h1><span style="font-size: 20px; font-weight: 800">{r["title"]}</span></div>
<p style="margin: 0; font-size: 15px; line-height: 1.3; font-weight: 600; color: #C9C9C2">{note}</p>
<div style="display: flex; justify-content: space-between; font-family: 'IBM Plex Mono', monospace; font-size: 10px; letter-spacing: 1px; color: #9A9A94"><span>{r["grid"]} &#183; pull with assets.get("{aid}")</span><span>@roundingerror.capital</span></div>
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{w},"height":{h}}}}}'>
class Component extends DCLogic {{
renderVals() {{ return {{}}; }}
}}
</script>
</body>
</html>
'''

def build_lib(t=0.0):
    os.makedirs(LIB, exist_ok=True); reg = {}
    for aid, r in REG.items():
        im = get(aid, t); im.save(os.path.join(LIB, f"{aid}.png"))
        reg[aid] = {"title": r["title"], "kind": r["kind"], "version": r["v"], "size": list(im.size), "grid": r["grid"], "file": f"{aid}.png", "fn": r["fn"].__name__ if r["fn"].__name__ != "<lambda>" else "piggy"}
    json.dump(reg, open(os.path.join(LIB, "registry.json"), "w"), indent=1)
    return reg

if __name__ == "__main__":
    if sys.argv[1:2] == ["lib"]: print(json.dumps(build_lib(), indent=1))
    elif sys.argv[1:2] == ["preview"]:
        ims = [get(a, 1.0) for a in REG]; Wt = sum(int(i.width * REG[a]["scale"]) + 20 for a, i in zip(REG, ims)); Ht = max(int(i.height * REG[a]["scale"]) for a, i in zip(REG, ims))
        sheet = Image.new("RGB", (Wt, Ht + 20), (12, 14, 20)); x = 10
        for a, i in zip(REG, ims):
            s = REG[a]["scale"]; j = i.resize((int(i.width * s), int(i.height * s)), Image.NEAREST); sheet.paste(j, (x, Ht + 10 - j.height), j); x += j.width + 20
        sheet.save(sys.argv[2])
