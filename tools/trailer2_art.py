"""Original pixel art for MEET THE FUND v3 (tools/trailer2.py): the piggy bank (redrawn) and THE REAL BOSS, a shadow-realm fawn.
The fawn is a character, never named and never labeled with a relationship on screen or in captions."""
from PIL import Image, ImageDraw, ImageFilter

def _outline(im, col, w=1):
    a = im.split()[3].filter(ImageFilter.MaxFilter(w * 2 + 1))
    o = Image.new("RGBA", im.size, col + (0,)); o.putalpha(a)
    out = Image.new("RGBA", im.size); out.alpha_composite(o); out.alpha_composite(im); return out

def _pad(im, p):
    out = Image.new("RGBA", (im.width + 2 * p, im.height + 2 * p)); out.paste(im, (p, p)); return out

def piggy():
    """80x62 shaded piggy bank: body with belly shadow and top shine, snout with nostrils, two ears, a sparkly eye,
    blush, four hooves, curly tail and a dark coin slot on top."""
    im = Image.new("RGBA", (80, 62)); d = ImageDraw.Draw(im)
    B, BD, BDD, BL, BLL = (246, 158, 182, 255), (222, 120, 152, 255), (186, 86, 122, 255), (255, 196, 212, 255), (255, 232, 240, 255)
    # legs (behind the body)
    for x in (16, 28, 46, 58):
        d.rectangle([x, 44, x + 8, 56], fill=BD); d.rectangle([x, 54, x + 8, 58], fill=(120, 60, 80, 255))
    # tail curl
    d.arc([0, 20, 10, 30], 90, 360, fill=BDD, width=2); d.arc([3, 23, 8, 28], 180, 450, fill=BDD, width=2)
    # body, belly shade, top shine
    d.ellipse([6, 12, 70, 52], fill=B)
    d.chord([6, 12, 70, 52], 20, 160, fill=BD)
    d.ellipse([14, 16, 44, 28], fill=BL); d.ellipse([18, 18, 30, 23], fill=BLL)
    # ears
    d.polygon([(46, 16), (52, 4), (58, 16)], fill=BD); d.polygon([(49, 15), (52, 8), (55, 15)], fill=BL)
    d.polygon([(38, 16), (42, 6), (48, 16)], fill=BDD)
    # snout
    d.ellipse([62, 24, 78, 40], fill=BD); d.ellipse([63, 25, 76, 37], fill=BL)
    d.ellipse([66, 29, 69, 33], fill=(140, 50, 80, 255)); d.ellipse([71, 29, 74, 33], fill=(140, 50, 80, 255))
    # eye + sparkle, blush
    d.ellipse([54, 20, 60, 27], fill=(30, 18, 24, 255)); d.rectangle([55, 21, 56, 22], fill=(255, 255, 255, 255))
    d.ellipse([52, 30, 60, 35], fill=(255, 120, 150, 200))
    # coin slot
    d.rounded_rectangle([26, 11, 42, 14], radius=1, fill=(90, 30, 50, 255))
    return _outline(_pad(im, 2), (60, 24, 40), 1)

def fawn(shadow=False, v=None):
    """48x58, drawn in the cast's own style (Roz/Theo/Kit): one simple pear silhouette with a 2 px dark outline, big head,
    small body, no stick limbs, two big dark eyes with a 2x2 catchlight, a cream muzzle patch, leaf ears pointing up and out,
    a few dapples and one accessory. Colour takes via v: coat (C, CD, BE), eyes, spots, head, acc, acc_col."""
    v = v or {}
    im = Image.new("RGBA", (48, 60)); d = ImageDraw.Draw(im)
    if shadow:
        C, CD, BE, IN = (34, 24, 30, 255), (22, 14, 20, 255), (46, 34, 42, 255), (54, 36, 48, 255)
        OUT, EYE, EYEW, SPOT = (8, 4, 8, 255), (14, 8, 14, 255), (220, 206, 224, 255), (62, 48, 58, 255)
    else:
        C, CD, BE = v.get("coat", ((184, 122, 72, 255), (134, 82, 44, 255), (246, 228, 200, 255)))[:3]
        IN = v.get("inner", (238, 178, 160, 255))
        OUT, EYE, EYEW, SPOT = (46, 26, 20, 255), (38, 22, 20, 255), (255, 255, 255, 255), (250, 242, 226, 255)
    PINK, PINK2, GOLD = v.get("acc_col", ((255, 140, 180, 255), (255, 196, 216, 255)))[0], v.get("acc_col", ((255, 140, 180, 255), (255, 196, 216, 255)))[1], (255, 220, 120, 255)
    # silhouette: ears, head, body (filled with the coat; the outline is added around the union at the end)
    body = Image.new("RGBA", im.size); bd = ImageDraw.Draw(body)
    bd.polygon([(16, 18), (1, 10), (3, 5), (10, 5), (22, 12)], fill=C); bd.polygon([(32, 18), (47, 10), (45, 5), (38, 5), (26, 12)], fill=C)   # deer ears: out to the sides
    bd.polygon([(15, 15), (5, 9), (6, 7), (18, 12)], fill=IN); bd.polygon([(33, 15), (43, 9), (42, 7), (30, 12)], fill=IN)                       # inner ears
    bd.ellipse([7, 7, 41, 39], fill=C); bd.ellipse([11, 9, 37, 22], fill=CL) if False else None                                                  # head
    bd.chord([7, 7, 41, 39], 20, 160, fill=CD); bd.ellipse([9, 9, 39, 35], fill=C)                                                                # jaw shade
    bd.ellipse([13, 32, 35, 56], fill=C); bd.chord([13, 32, 35, 56], 30, 150, fill=CD); bd.ellipse([14, 33, 34, 52], fill=C)   # body + shade
    bd.ellipse([17, 38, 31, 55], fill=BE)                                                                                   # belly
    bd.ellipse([17, 24, 31, 37], fill=BE)                                                                                   # muzzle patch
    bd.rectangle([15, 54, 20, 58], fill=CD); bd.rectangle([28, 54, 33, 58], fill=CD)                                        # feet
    if v.get("spots", True):
        for p in ((12, 14), (22, 10), (34, 13), (30, 18), (14, 20), (15, 42), (32, 44), (12, 36)): bd.rectangle([p[0], p[1], p[0] + 1, p[1] + 1], fill=SPOT)
    # outline around the whole silhouette (2 px, like the roster sprites)
    a = body.split()[3].filter(ImageFilter.MaxFilter(3)); o = Image.new("RGBA", im.size, OUT); o.putalpha(a)
    im.alpha_composite(o); im.alpha_composite(body); d = ImageDraw.Draw(im)
    # face
    eyes = v.get("eyes", "big")
    for x0 in (12, 27):
        if eyes == "big":
            d.ellipse([x0, 17, x0 + 8, 26], fill=EYE); d.rectangle([x0 + 2, 19, x0 + 3, 20], fill=EYEW); d.point([(x0 + 6, 23)], fill=EYEW)
        elif eyes == "sleepy":
            d.ellipse([x0, 19, x0 + 8, 26], fill=EYE); d.rectangle([x0, 17, x0 + 8, 20], fill=C); d.rectangle([x0 + 2, 21, x0 + 3, 22], fill=EYEW)
        else:
            d.ellipse([x0 + 1, 18, x0 + 7, 25], fill=EYE); d.rectangle([x0 + 3, 20, x0 + 4, 21], fill=EYEW)
    d.line([(11, 16), (13, 15)], fill=OUT); d.line([(37, 16), (35, 15)], fill=OUT)                                           # lashes
    d.rectangle([22, 28, 25, 30], fill=OUT); d.point([(22, 28)], fill=(120, 100, 110, 255))                                 # nose
    d.ellipse([9, 26, 13, 29], fill=(236, 150, 160, 180)); d.ellipse([35, 26, 39, 29], fill=(236, 150, 160, 180))           # blush
    # accessory on the chest
    acc = v.get("acc", "bow")
    if acc == "bow":
        d.polygon([(24, 36), (18, 33), (18, 40)], fill=PINK); d.polygon([(24, 36), (30, 33), (30, 40)], fill=PINK); d.rectangle([23, 35, 25, 37], fill=PINK2)
    elif acc == "pearls":
        for k in range(6): d.rectangle([17 + k * 3, 34 + (1 if k in (0, 5) else 2 if k in (1, 4) else 3), 18 + k * 3, 35 + (1 if k in (0, 5) else 2 if k in (1, 4) else 3)], fill=(246, 242, 236, 255))
    elif acc == "scarf":
        d.rectangle([17, 33, 31, 36], fill=PINK); d.rectangle([27, 36, 31, 44], fill=PINK); d.point([(28, 34), (30, 42)], fill=PINK2)
    elif acc == "bell":
        d.rectangle([17, 33, 31, 35], fill=PINK); d.ellipse([22, 35, 26, 39], fill=GOLD); d.point([(24, 38)], fill=OUT)
    # headpiece
    head = v.get("head", "flower")
    if head == "flower":
        fx, fy = 36, 8
        for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2)): d.rectangle([fx + dx - 1, fy + dy - 1, fx + dx + 1, fy + dy + 1], fill=PINK)
        d.point([(fx, fy)], fill=GOLD)
    elif head == "crown":
        d.polygon([(18, 9), (18, 3), (21, 6), (24, 2), (27, 6), (30, 3), (30, 9)], fill=GOLD); d.point([(24, 6), (20, 7), (28, 7)], fill=PINK)
    elif head == "headbow":
        d.polygon([(24, 7), (19, 4), (19, 10)], fill=PINK); d.polygon([(24, 7), (29, 4), (29, 10)], fill=PINK); d.rectangle([23, 6, 25, 8], fill=PINK2)
    elif head == "crownflowers":
        for fx in (16, 24, 32):
            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)): d.point([(fx + dx, 7 + dy)], fill=PINK if fx != 24 else (255, 255, 255, 255))
            d.point([(fx, 7)], fill=GOLD)
    return _pad(im, 1)

V26 = dict(slim=True, antlers=True, head="crown", acc="bow")   # the boss 2026-11-01: slimmer body, thin antlers, a real crown
DEER = [  # 8 takes for the boss to pick from (V25)
    ("Chestnut", dict()),
    ("Honey", dict(coat=((214, 160, 96, 255), (168, 116, 60, 255), (252, 238, 212, 255)), head="headbow")),
    ("Cream", dict(coat=((232, 206, 168, 255), (190, 156, 112, 255), (255, 248, 236, 255)), acc="pearls")),
    ("Cocoa", dict(coat=((112, 70, 44, 255), (76, 44, 28, 255), (236, 214, 190, 255)), acc="scarf", head="crown", acc_col=((255, 120, 150, 255), (255, 180, 200, 255)))),
    ("Rosewood", dict(coat=((190, 120, 110, 255), (140, 80, 76, 255), (252, 232, 226, 255)), head="crownflowers", acc="bell")),
    ("Dun", dict(coat=((160, 142, 120, 255), (112, 96, 80, 255), (240, 232, 220, 255)), eyes="button", spots=False, acc_col=((120, 200, 255, 255), (190, 230, 255, 255)))),
    ("Snow", dict(coat=((236, 236, 240, 255), (190, 190, 200, 255), (255, 255, 255, 255)), spots=False, head="headbow", acc="pearls", acc_col=((200, 160, 255, 255), (230, 210, 255, 255)), inner=(250, 200, 210, 255))),
    ("Sunset", dict(coat=((226, 134, 78, 255), (178, 92, 46, 255), (255, 238, 210, 255)), head="crown", acc="bow", acc_col=((255, 100, 140, 255), (255, 170, 190, 255)), eyes="big")),
]

# ---------------------------------------------------------------- HD fawn (2026-11-01, the boss: "higher rez and shade it way way better")
def _ramp(base, n=5):
    """5 tones from one base colour: deep shade, shade, base, light, highlight (light from the top-left)."""
    r, g, b = base[:3]
    def mix(c, t, to): return tuple(int(c[i] + (to[i] - c[i]) * t) for i in range(3))
    deep = mix((r, g, b), .45, (40, 18, 30)); sh = mix((r, g, b), .25, (60, 30, 40))
    li = mix((r, g, b), .28, (255, 240, 220)); hi = mix((r, g, b), .55, (255, 250, 240))
    return [deep, sh, (r, g, b), li, hi]
def _sphere(mask_draw_fn, box, ramp, px, light=(-.5, -.65, .58), bands=(.18, .42, .72, .9), rim=True):
    """Fill the shape with sphere shading: a surface normal per pixel (z from the ellipse), lit from the top-left; the lambert
    term picks one of 5 tones, so highlights sit where a real sphere's would. Thin rim light on the shadow side."""
    x0, y0, x1, y1 = box; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; rx, ry = (x1 - x0) / 2, (y1 - y0) / 2
    m = Image.new("L", px.size, 0); mask_draw_fn(ImageDraw.Draw(m)); mp = m.load(); out = px.load()
    lx, ly, lz = light; ln = (lx * lx + ly * ly + lz * lz) ** .5; lx, ly, lz = lx / ln, ly / ln, lz / ln
    for y in range(px.height):
        for x in range(px.width):
            if not mp[x, y]: continue
            nx, ny = (x - cx) / rx, (y - cy) / ry; r2 = min(1.0, nx * nx + ny * ny); nz = (1 - r2) ** .5
            lam = max(0.0, nx * lx + ny * ly + nz * lz)            # 0..1
            lam = lam ** 1.4
            k = 0 if lam < bands[0] else 1 if lam < bands[1] else 2 if lam < bands[2] else 3 if lam < bands[3] else 4
            if rim and r2 > .78 and nx > .25 and ny > -.2 and k < 2: k = 2      # rim light bottom-right
            c = ramp[k]; out[x, y] = (c[0], c[1], c[2], 255)
def fawn_hd(shadow=False, v=None):
    """96x120 fawn with real shading: 5-tone ramps per material, sphere shading on head, body and muzzle, rim light,
    layered eyes (iris ring, pupil, two catchlights), inner-ear gradient, dithered belly edge, hoof shine, 3 px outline."""
    v = v or {}
    Wd, Hd = 96, 120; im = Image.new("RGBA", (Wd, Hd))
    coat = v.get("coat", ((184, 122, 72, 255), (134, 82, 44, 255), (246, 228, 200, 255)))
    C = coat[0][:3]; BE = coat[2][:3]; IN = v.get("inner", (238, 178, 160, 255))[:3]
    if shadow:
        C, BE, IN = (40, 28, 36), (54, 42, 50), (62, 40, 56)
    RC, RB, RI = _ramp(C), _ramp(BE), _ramp(IN)
    if shadow:
        RC = [(14, 8, 12), (24, 16, 22), (40, 28, 36), (58, 44, 54), (78, 62, 74)]; RB = [(22, 14, 20), (34, 24, 32), (54, 42, 50), (70, 56, 66), (90, 74, 86)]; RI = [(24, 12, 20), (40, 22, 34), (62, 40, 56), (84, 58, 76), (104, 76, 96)]
    OUT = (46, 26, 20) if not shadow else (8, 4, 8)
    acc_col = v.get("acc_col", ((255, 140, 180, 255), (255, 196, 216, 255)))
    PINK, PINK2 = acc_col[0][:3], acc_col[1][:3]; GOLD = (255, 220, 120)
    body = Image.new("RGBA", (Wd, Hd))
    # ears (outer), head, body as shaded spheres; drawn back to front
    for (poly, box, ramp) in (([(32, 36), (2, 20), (6, 10), (20, 10), (44, 24)], (2, 10, 44, 36), RC), ([(64, 36), (94, 20), (90, 10), (76, 10), (52, 24)], (52, 10, 94, 36), RC)):
        _sphere(lambda d, p=poly: d.polygon(p, fill=255), box, ramp, body, bands=(.3, .5, .78, .95), rim=False)
    for (poly, box, ramp) in (([(30, 30), (10, 18), (12, 14), (36, 24)], (10, 14, 36, 30), RI), ([(66, 30), (86, 18), (84, 14), (60, 24)], (60, 14, 86, 30), RI)):
        _sphere(lambda d, p=poly: d.polygon(p, fill=255), box, ramp, body, bands=(.35, .6, .9, 1.1), rim=False)
    _sphere(lambda d: d.ellipse([26, 64, 70, 112], fill=255), (26, 64, 70, 112), RC, body, bands=(.22, .45, .74, .92))   # body
    _sphere(lambda d: d.ellipse([14, 14, 82, 78], fill=255), (14, 14, 82, 78), RC, body, bands=(.22, .45, .74, .92))     # head
    _sphere(lambda d: d.ellipse([34, 76, 62, 108], fill=255), (34, 76, 62, 108), RB, body, bands=(.3, .55, .85, 1.1), rim=False)   # belly
    _sphere(lambda d: d.ellipse([34, 48, 62, 74], fill=255), (34, 48, 62, 74), RB, body, bands=(.3, .55, .85, 1.1), rim=False)     # muzzle
    bd = ImageDraw.Draw(body)
    for x in (30, 56):  # feet with a shine
        bd.rounded_rectangle([x, 106, x + 10, 116], radius=3, fill=RC[1]); bd.rectangle([x, 112, x + 10, 116], fill=OUT if not shadow else (10, 6, 10)); bd.rectangle([x + 2, 113, x + 4, 114], fill=(120, 100, 110))
    bp = body.load()
    for x in range(36, 60):  # dithered belly edge
        for y in (75, 76, 77):
            if (x + y) % 2 == 0 and bp[x, y][3]: bp[x, y] = RB[2] + (255,)
    if v.get("spots", True):
        SP = RC[4] if not shadow else (84, 70, 82)
        for (x, y) in ((24, 28), (44, 20), (68, 26), (60, 36), (28, 40), (30, 84), (64, 88), (24, 72), (70, 74)):
            bd.ellipse([x, y, x + 3, y + 3], fill=SP)
    # outline around the union
    a = body.split()[3].filter(ImageFilter.MaxFilter(5)); o = Image.new("RGBA", (Wd, Hd), OUT + (255,)); o.putalpha(a)
    im.alpha_composite(o); im.alpha_composite(body); d = ImageDraw.Draw(im)
    # eyes: white, iris ring, pupil, two catchlights, lid line, lashes
    eyes = v.get("eyes", "big"); IRIS = (96, 60, 48) if not shadow else (40, 26, 38); PUP = (30, 16, 16) if not shadow else (12, 6, 12)
    for x0 in (24, 54):
        if eyes == "big":
            d.ellipse([x0, 34, x0 + 18, 54], fill=(250, 246, 244)); d.ellipse([x0 + 2, 35, x0 + 17, 53], fill=IRIS); d.ellipse([x0 + 4, 38, x0 + 15, 52], fill=PUP)
            d.ellipse([x0 + 5, 38, x0 + 9, 42], fill=(255, 255, 255)); d.ellipse([x0 + 12, 47, x0 + 14, 49], fill=(255, 255, 255))
            d.arc([x0 - 1, 33, x0 + 19, 55], 190, 350, fill=OUT, width=2)
        elif eyes == "sleepy":
            d.ellipse([x0, 38, x0 + 18, 54], fill=(250, 246, 244)); d.ellipse([x0 + 3, 39, x0 + 16, 53], fill=PUP); d.ellipse([x0 + 5, 41, x0 + 8, 44], fill=(255, 255, 255))
            d.chord([x0 - 1, 33, x0 + 19, 47], 180, 360, fill=RC[2]); d.arc([x0 - 1, 33, x0 + 19, 47], 180, 360, fill=OUT, width=2)
        else:
            d.ellipse([x0 + 2, 37, x0 + 16, 52], fill=PUP); d.ellipse([x0 + 5, 39, x0 + 8, 42], fill=(255, 255, 255))
        lx = x0 - 1 if x0 < 48 else x0 + 19; sd = -1 if x0 < 48 else 1
        for k in range(3): d.line([(lx, 36 + k * 3), (lx + sd * 4, 32 + k * 3)], fill=OUT, width=2)
    d.ellipse([44, 56, 52, 62], fill=PUP); d.ellipse([45, 57, 47, 58], fill=(140, 120, 130))                       # nose with a shine
    d.line([(48, 62), (48, 65)], fill=OUT, width=1); d.arc([42, 62, 54, 70], 10, 170, fill=OUT, width=1)           # tiny smile
    d.ellipse([18, 54, 30, 60], fill=(240, 150, 160) if not shadow else (90, 50, 70)); d.ellipse([66, 54, 78, 60], fill=(240, 150, 160) if not shadow else (90, 50, 70))   # blush
    # accessory
    acc = v.get("acc", "bow")
    if acc == "bow":
        for pts in ([(48, 78), (34, 72), (34, 86)], [(48, 78), (62, 72), (62, 86)]): d.polygon(pts, fill=PINK); d.polygon([(p[0], p[1]) for p in pts], outline=tuple(int(c * .7) for c in PINK))
        d.polygon([(38, 75), (44, 77), (40, 82)], fill=PINK2); d.polygon([(58, 75), (52, 77), (56, 82)], fill=PINK2)
        d.rounded_rectangle([45, 75, 51, 81], radius=2, fill=PINK2); d.point([(46, 76)], fill=(255, 255, 255))
    elif acc == "pearls":
        for k in range(8):
            x = 32 + k * 4.6; y = 76 + (abs(k - 3.5) ** 1.6) * -1.1 + 4
            d.ellipse([x, y, x + 3, y + 3], fill=(246, 242, 236)); d.point([(int(x) + 1, int(y) + 1)], fill=(255, 255, 255))
    elif acc == "scarf":
        d.rounded_rectangle([32, 72, 64, 80], radius=3, fill=PINK); d.rectangle([54, 80, 62, 96], fill=PINK); d.rectangle([34, 73, 62, 75], fill=PINK2); d.rectangle([56, 82, 58, 94], fill=PINK2)
    elif acc == "bell":
        d.rounded_rectangle([32, 72, 64, 77], radius=2, fill=PINK); d.ellipse([43, 76, 53, 86], fill=GOLD); d.ellipse([45, 78, 48, 81], fill=(255, 248, 200)); d.point([(48, 84)], fill=OUT)
    head = v.get("head", "flower")
    if head == "flower":
        fx, fy = 72, 16
        for dx, dy in ((-4, 0), (4, 0), (0, -4), (0, 4)): d.ellipse([fx + dx - 3, fy + dy - 3, fx + dx + 3, fy + dy + 3], fill=PINK)
        d.ellipse([fx - 2, fy - 2, fx + 2, fy + 2], fill=GOLD); d.point([(fx - 4, fy - 4)], fill=PINK2)
    elif head == "crown":
        d.polygon([(36, 18), (36, 6), (42, 12), (48, 4), (54, 12), (60, 6), (60, 18)], fill=GOLD); d.line([(37, 17), (59, 17)], fill=(200, 150, 40), width=2)
        for x in (42, 48, 54): d.ellipse([x - 1, 13, x + 1, 15], fill=PINK)
    elif head == "headbow":
        d.polygon([(48, 14), (38, 8), (38, 20)], fill=PINK); d.polygon([(48, 14), (58, 8), (58, 20)], fill=PINK); d.rounded_rectangle([45, 11, 51, 17], radius=2, fill=PINK2)
    elif head == "crownflowers":
        for fx in (32, 48, 64):
            col = PINK if fx != 48 else (255, 255, 255)
            for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2)): d.ellipse([fx + dx - 2, 14 + dy - 2, fx + dx + 2, 14 + dy + 2], fill=col)
            d.ellipse([fx - 1, 13, fx + 1, 15], fill=GOLD)
    return _pad(im, 2)

# ---------------------------------------------------------------- the 64x64 STANDARD (V22/V23: every official avatar is a 64x64 pixel grid, ~45x56 figure,
# 2 px near-black outline, soft 3-4 tone shading, big black eyes with a white dot, small arms and stub legs). The fawn must match it.
def fawn64(shadow=False, v=None):
    v = v or {}
    im = Image.new("RGBA", (64, 64))
    coat = v.get("coat", ((184, 122, 72, 255), (134, 82, 44, 255), (246, 228, 200, 255)))
    C, BE = coat[0][:3], coat[2][:3]; IN = v.get("inner", (238, 178, 160, 255))[:3]
    if shadow: C, BE, IN = (40, 28, 36), (54, 42, 50), (62, 40, 56)
    RC, RB, RI = _ramp(C), _ramp(BE), _ramp(IN)
    if shadow:
        RC = [(14, 8, 12), (24, 16, 22), (40, 28, 36), (58, 44, 54), (78, 62, 74)]; RB = [(22, 14, 20), (34, 24, 32), (54, 42, 50), (70, 56, 66), (90, 74, 86)]; RI = RB
    OUT = (34, 22, 18) if not shadow else (6, 3, 6)
    acc_col = v.get("acc_col", ((255, 140, 180, 255), (255, 196, 216, 255))); PINK, PINK2 = acc_col[0][:3], acc_col[1][:3]; GOLD = (255, 220, 120)
    body = Image.new("RGBA", (64, 64)); B = (.3, .5, .8, .97)   # gentle: mostly base, light on top-left, shade at the bottom edge
    # ears out to the sides, inner ear
    for poly, box in (([(22, 24), (8, 14), (11, 8), (20, 9), (30, 17)], (8, 8, 30, 24)), ([(42, 24), (56, 14), (53, 8), (44, 9), (34, 17)], (34, 8, 56, 24))):
        _sphere(lambda d, p=poly: d.polygon(p, fill=255), box, RC, body, bands=B, rim=False)
    for poly, box in (([(21, 20), (12, 14), (14, 11), (26, 17)], (12, 11, 26, 20)), ([(43, 20), (52, 14), (50, 11), (38, 17)], (38, 11, 52, 20))):
        _sphere(lambda d, p=poly: d.polygon(p, fill=255), box, RI, body, bands=(.35, .6, .9, 1.1), rim=False)
    slim = v.get("slim", False)
    bx0, bx1 = (22, 42) if slim else (19, 45)
    bd = ImageDraw.Draw(body)
    _sphere(lambda d: d.ellipse([bx0, 36, bx1, 58], fill=255), (bx0, 36, bx1, 58), RC, body, bands=B)          # body
    _sphere(lambda d: d.ellipse([13, 10, 51, 44], fill=255), (13, 10, 51, 44), RC, body, bands=B)          # head
    _sphere(lambda d: d.ellipse([bx0 + 5, 42, bx1 - 5, 57], fill=255), (bx0 + 5, 42, bx1 - 5, 57), RB, body, bands=(.35, .6, .9, 1.1), rim=False)   # belly
    _sphere(lambda d: d.ellipse([25, 29, 39, 42], fill=255), (25, 29, 39, 42), RB, body, bands=(.35, .6, .9, 1.1), rim=False)   # muzzle
    bd = ImageDraw.Draw(body)
    ax = 3 if slim else 0
    bd.ellipse([15 + ax, 42, 21 + ax, 50], fill=RC[2]); bd.ellipse([43 - ax, 42, 49 - ax, 50], fill=RC[2]); bd.rectangle([16 + ax, 48, 20 + ax, 49], fill=RC[1]); bd.rectangle([44 - ax, 48, 48 - ax, 49], fill=RC[1])   # arms
    for x in ((26, 33) if slim else (25, 34)): bd.rounded_rectangle([x, 56, x + 5, 61], radius=1, fill=RC[1]); bd.rectangle([x, 60, x + 5, 61], fill=RC[0])   # legs + hooves
    if v.get("spots", True):
        SP = RC[4] if not shadow else (84, 70, 82)
        for (x, y) in ((19, 16), (31, 13), (44, 18), (40, 24), (20, 26), (22, 46), (41, 48)): bd.rectangle([x, y, x + 1, y + 1], fill=SP)
    a = body.split()[3].filter(ImageFilter.MaxFilter(3)); o = Image.new("RGBA", (64, 64), OUT + (255,)); o.putalpha(a)
    im.alpha_composite(o); im.alpha_composite(body); d = ImageDraw.Draw(im)
    if v.get("antlers"):   # thin antlers, drawn after the outline so they stay 1 px: a beam up from behind each ear, two tines, lighter tips
        AN, AT = ((96, 62, 30), (150, 108, 60)) if not shadow else ((70, 56, 66), (104, 88, 100))
        for sx, x0 in ((-1, 21), (1, 43)):
            d.line([(x0, 12), (x0 + sx, 8), (x0 + sx * 2, 4), (x0 + sx * 3, 1)], fill=AN)
            d.line([(x0 + sx, 8), (x0 + sx * 4, 6)], fill=AN); d.line([(x0 + sx * 2, 4), (x0 + sx * 5, 2)], fill=AN)
            d.point([(x0 + sx * 3, 1), (x0 + sx * 4, 6), (x0 + sx * 5, 2)], fill=AT)
    # eyes: big black, white dot (the roster look), lashes; nose; blush
    EYE = (26, 16, 16) if not shadow else (8, 4, 8); eyes = v.get("eyes", "big")
    for x0 in (19, 36):
        if eyes == "sleepy":
            d.ellipse([x0, 23, x0 + 8, 31], fill=EYE); d.rectangle([x0, 21, x0 + 8, 25], fill=RC[2]); d.rectangle([x0 + 2, 26, x0 + 3, 27], fill=(255, 255, 255))
        elif eyes == "button":
            d.ellipse([x0 + 1, 22, x0 + 7, 29], fill=EYE); d.rectangle([x0 + 2, 23, x0 + 3, 24], fill=(255, 255, 255))
        else:
            d.ellipse([x0, 20, x0 + 8, 30], fill=EYE); d.rectangle([x0 + 2, 22, x0 + 3, 23], fill=(255, 255, 255)); d.point([(x0 + 6, 27)], fill=(255, 255, 255))
        lx = x0 - 1 if x0 < 32 else x0 + 9; sd = -1 if x0 < 32 else 1
        d.line([(lx, 21), (lx + sd * 2, 19)], fill=OUT); d.line([(lx, 24), (lx + sd * 2, 23)], fill=OUT)
    d.rectangle([30, 33, 33, 35], fill=EYE); d.point([(30, 33)], fill=(120, 100, 110))
    d.point([(31, 36), (32, 36), (30, 37), (33, 37)], fill=OUT)   # tiny smile
    d.rectangle([15, 31, 19, 33], fill=(236, 150, 160) if not shadow else (80, 44, 62)); d.rectangle([45, 31, 49, 33], fill=(236, 150, 160) if not shadow else (80, 44, 62))
    acc = v.get("acc", "bow")
    if acc == "bow":
        d.polygon([(32, 42), (26, 39), (26, 46)], fill=PINK); d.polygon([(32, 42), (38, 39), (38, 46)], fill=PINK); d.rectangle([31, 41, 33, 43], fill=PINK2); d.point([(27, 40), (37, 40)], fill=PINK2)
    elif acc == "pearls":
        for k in range(6): d.rectangle([24 + k * 3, 40 + (1 if k in (0, 5) else 2 if k in (1, 4) else 3), 25 + k * 3, 41 + (1 if k in (0, 5) else 2 if k in (1, 4) else 3)], fill=(246, 242, 236))
    elif acc == "scarf":
        d.rectangle([24, 39, 40, 42], fill=PINK); d.rectangle([36, 42, 40, 50], fill=PINK); d.rectangle([25, 39, 39, 39], fill=PINK2)
    elif acc == "bell":
        d.rectangle([24, 39, 40, 41], fill=PINK); d.ellipse([29, 41, 35, 47], fill=GOLD); d.point([(30, 42)], fill=(255, 248, 200)); d.point([(32, 46)], fill=OUT)
    head = v.get("head", "flower")
    if head == "flower":
        fx, fy = 47, 11
        for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2)): d.rectangle([fx + dx - 1, fy + dy - 1, fx + dx + 1, fy + dy + 1], fill=PINK)
        d.point([(fx, fy)], fill=GOLD)
    elif head == "crown":
        # a real crown: dark-gold outline, five points with pearl tips, a jewel band, a highlight down the left, shadow on the right
        G0, G1, G2, G3 = (120, 82, 18), (196, 146, 36), (244, 200, 72), (255, 236, 160)
        crown = [(24, 15), (24, 5), (27, 9), (30, 3), (32, 7), (34, 3), (37, 9), (40, 5), (40, 15)]
        d.polygon(crown, fill=G1); d.polygon([(p[0], p[1]) for p in crown], outline=G0)
        d.polygon([(25, 14), (25, 7), (27, 10), (29, 6), (30, 8), (30, 14)], fill=G2)                  # lit left face
        d.polygon([(35, 14), (35, 8), (37, 11), (39, 7), (39, 14)], fill=(170, 120, 28))               # shaded right face
        d.line([(25, 7), (25, 13)], fill=G3); d.point([(30, 4), (34, 4), (24, 6), (40, 6)], fill=(255, 255, 255))   # pearls on the tips
        d.rectangle([24, 12, 40, 13], fill=G0); d.rectangle([25, 12, 39, 12], fill=G2)                 # base band
        for x, col in ((27, (230, 60, 90)), (32, (90, 170, 240)), (37, (230, 60, 90))): d.rectangle([x - 1, 10, x + 1, 11], fill=col); d.point([(x - 1, 10)], fill=(255, 255, 255))
    elif head == "headbow":
        d.polygon([(32, 10), (26, 6), (26, 14)], fill=PINK); d.polygon([(32, 10), (38, 6), (38, 14)], fill=PINK); d.rectangle([31, 9, 33, 11], fill=PINK2)
    elif head == "crownflowers":
        for fx in (23, 32, 41):
            col = PINK if fx != 32 else (255, 255, 255)
            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)): d.point([(fx + dx, 10 + dy)], fill=col)
            d.point([(fx, 10)], fill=GOLD)
    return im

if __name__ == "__main__":
    import sys
    p, f, g = piggy(), fawn(), fawn(True)
    sh = Image.new("RGB", (p.width * 6 + f.width * 16 + 80, max(p.height * 6, f.height * 8) + 20), (60, 60, 60))
    sh.paste(p.resize((p.width * 6, p.height * 6), Image.NEAREST), (10, 10), p.resize((p.width * 6, p.height * 6), Image.NEAREST))
    fb = f.resize((f.width * 8, f.height * 8), Image.NEAREST); sh.paste(fb, (p.width * 6 + 40, 10), fb)
    gb = g.resize((g.width * 8, g.height * 8), Image.NEAREST); sh.paste(gb, (p.width * 6 + f.width * 8 + 60, 10), gb)
    sh.save(sys.argv[1])
