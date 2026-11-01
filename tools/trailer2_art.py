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

if __name__ == "__main__":
    import sys
    p, f, g = piggy(), fawn(), fawn(True)
    sh = Image.new("RGB", (p.width * 6 + f.width * 16 + 80, max(p.height * 6, f.height * 8) + 20), (60, 60, 60))
    sh.paste(p.resize((p.width * 6, p.height * 6), Image.NEAREST), (10, 10), p.resize((p.width * 6, p.height * 6), Image.NEAREST))
    fb = f.resize((f.width * 8, f.height * 8), Image.NEAREST); sh.paste(fb, (p.width * 6 + 40, 10), fb)
    gb = g.resize((g.width * 8, g.height * 8), Image.NEAREST); sh.paste(gb, (p.width * 6 + f.width * 8 + 60, 10), gb)
    sh.save(sys.argv[1])
