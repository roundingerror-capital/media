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
    """60x80 fawn, real deer colours: warm chestnut coat, cream belly and muzzle, big dark doe eyes with long lashes and
    two catchlights, soft rosy inner ears, white dapples, a tiny black nose, a pink flower by one ear and a pink bow collar.
    shadow=True gives the shadow-realm version (same shapes, near-black palette), for the reveal before the flashback."""
    im = Image.new("RGBA", (60, 80)); d = ImageDraw.Draw(im)
    if shadow:
        C, CD, CL, CR, BE = (34, 24, 30, 255), (22, 14, 20, 255), (48, 36, 44, 255), (60, 44, 54, 255), (44, 32, 40, 255)
        SPOT, EYEW, EYE, NOSE = (70, 56, 66, 255), (210, 196, 214, 255), (20, 10, 18, 255), (10, 6, 10, 255)
    else:
        C, CD, CL, CR, BE = (176, 112, 66, 255), (132, 80, 44, 255), (206, 146, 92, 255), (236, 176, 150, 255), (246, 226, 196, 255)
        SPOT, EYEW, EYE, NOSE = (250, 240, 220, 255), (255, 255, 255, 255), (48, 30, 26, 255), (26, 16, 14, 255)
    PINK, PINK2, GOLD = (255, 140, 180, 255), (255, 190, 215, 255), (255, 220, 120, 255)
    v = v or {}
    if v.get("coat") and not shadow: C, CD, CL, CR, BE = v["coat"]
    if v.get("acc_col"): PINK, PINK2 = v["acc_col"]
    if v.get("eye"): EYE = v["eye"]
    # legs (slim) + hooves
    for x in (22, 34):
        d.rectangle([x, 62, x + 4, 76], fill=CD); d.rectangle([x, 75, x + 4, 78], fill=(40, 26, 22, 255))
    # body + cream belly + dapples
    d.ellipse([15, 40, 45, 66], fill=C); d.ellipse([21, 48, 39, 65], fill=BE)
    if v.get("spots", True):
        for e in ([19, 46, 22, 49], [38, 44, 41, 47], [23, 42, 25, 44], [40, 52, 42, 54], [17, 54, 19, 56]): d.ellipse(e, fill=SPOT)
    # neck
    d.rectangle([26, 32, 34, 42], fill=C)
    acc = v.get("acc", "bow")
    if acc == "bow":      # pink bow on the chest
        d.rectangle([23, 43, 37, 45], fill=PINK)
        d.polygon([(30, 44), (24, 40), (24, 49)], fill=PINK); d.polygon([(30, 44), (36, 40), (36, 49)], fill=PINK)
        d.rectangle([29, 43, 31, 45], fill=PINK2)
    elif acc == "pearls":
        for k in range(7): d.ellipse([22 + k * 2.6 - 1, 43 + abs(k - 3) * -1 + 2, 22 + k * 2.6 + 1, 43 + abs(k - 3) * -1 + 4], fill=(240, 236, 230, 255))
    elif acc == "scarf":
        d.rectangle([23, 42, 37, 47], fill=PINK); d.rectangle([33, 47, 37, 56], fill=PINK); d.rectangle([34, 44, 36, 46], fill=PINK2)
    elif acc == "bell":
        d.rectangle([23, 43, 37, 45], fill=PINK); d.ellipse([27, 45, 33, 51], fill=GOLD); d.point([(30, 50)], fill=(120, 80, 20, 255))
    # ears: big soft leaves, rosy inside, tilted out
    for cx, ang in ((11, -40), (49, 40)):
        e = Image.new("RGBA", (24, 13)); ed = ImageDraw.Draw(e)
        ed.ellipse([0, 1, 23, 11], fill=CD); ed.ellipse([1, 2, 22, 10], fill=C); ed.ellipse([5, 4, 19, 9], fill=CR)
        e = e.rotate(ang, resample=Image.NEAREST, expand=True)
        im.alpha_composite(e, (cx - e.width // 2, 10 - e.height // 2))
    d = ImageDraw.Draw(im)
    # head (round) + forehead highlight + long cream muzzle
    d.ellipse([13, 6, 47, 38], fill=C); d.ellipse([18, 8, 34, 18], fill=CL)
    d.ellipse([22, 22, 38, 41], fill=BE)
    d.ellipse([27, 32, 33, 37], fill=NOSE); d.point([(28, 33)], fill=(120, 100, 110, 255))     # glossy nose
    if v.get("spots", True):
        for e in ([24, 8, 27, 11], [34, 10, 36, 12], [20, 13, 22, 15], [38, 15, 40, 17]): d.ellipse(e, fill=SPOT)
    # eyes: big doe eyes, two catchlights, lashes, blush
    big_eyes = v.get("eyes", "big")
    for x0, side in ((16, -1), (34, 1)):
        if big_eyes == "big":
            d.ellipse([x0, 16, x0 + 10, 27], fill=EYEW); d.ellipse([x0 + 1, 17, x0 + 9, 26], fill=EYE)
            d.rectangle([x0 + 3, 18, x0 + 5, 20], fill=(255, 255, 255, 255)); d.point([(x0 + 7, 23)], fill=(255, 255, 255, 255))
        elif big_eyes == "sleepy":  # half-lidded, calm
            d.ellipse([x0, 18, x0 + 10, 27], fill=EYEW); d.ellipse([x0 + 1, 19, x0 + 9, 26], fill=EYE)
            d.rectangle([x0, 16, x0 + 10, 20], fill=C); d.rectangle([x0 + 3, 21, x0 + 4, 22], fill=(255, 255, 255, 255))
        else:  # "button": smaller, rounder
            d.ellipse([x0 + 1, 18, x0 + 9, 26], fill=EYE); d.rectangle([x0 + 3, 19, x0 + 4, 20], fill=(255, 255, 255, 255))
        lx = x0 if side < 0 else x0 + 10
        for k in range(3): d.line([(lx, 17 + k * 2), (lx + side * 3, 14 + k * 2)], fill=NOSE)
    d.ellipse([15, 27, 21, 30], fill=(255, 150, 160, 150)); d.ellipse([39, 27, 45, 30], fill=(255, 150, 160, 150))
    head = v.get("head", "flower")
    if head == "flower":
        fx, fy = 44, 7
        for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2)): d.ellipse([fx + dx - 2, fy + dy - 2, fx + dx + 2, fy + dy + 2], fill=PINK)
        d.ellipse([fx - 1, fy - 1, fx + 1, fy + 1], fill=GOLD)
    elif head == "crown":
        d.polygon([(23, 8), (23, 1), (26, 5), (30, 0), (34, 5), (37, 1), (37, 8)], fill=GOLD); d.point([(30, 4), (26, 6), (34, 6)], fill=PINK)
    elif head == "headbow":
        d.polygon([(30, 6), (24, 2), (24, 10)], fill=PINK); d.polygon([(30, 6), (36, 2), (36, 10)], fill=PINK); d.rectangle([29, 5, 31, 7], fill=PINK2)
    elif head == "crownflowers":
        for fx in (22, 30, 38):
            for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2)): d.ellipse([fx + dx - 1, 5 + dy - 1, fx + dx + 1, 5 + dy + 1], fill=PINK if fx != 30 else (255, 255, 255, 255))
            d.point([(fx, 5)], fill=GOLD)
    return _outline(_pad(im, 2), (40, 24, 20) if not shadow else (10, 6, 10), 1)

DEER = [  # 8 takes for the boss to pick from (V25)
    ("Chestnut", dict()),
    ("Honey", dict(coat=((214, 160, 96, 255), (168, 116, 60, 255), (236, 196, 140, 255), (246, 196, 170, 255), (252, 238, 212, 255)), head="headbow")),
    ("Cream", dict(coat=((232, 206, 168, 255), (190, 156, 112, 255), (246, 230, 204, 255), (246, 200, 190, 255), (255, 248, 236, 255)), acc="pearls", eyes="sleepy")),
    ("Cocoa", dict(coat=((112, 70, 44, 255), (76, 44, 28, 255), (150, 100, 66, 255), (220, 150, 140, 255), (236, 214, 190, 255)), acc="scarf", head="crown", acc_col=((255, 120, 150, 255), (255, 180, 200, 255)))),
    ("Rosewood", dict(coat=((190, 120, 110, 255), (140, 80, 76, 255), (220, 160, 150, 255), (250, 190, 190, 255), (252, 232, 226, 255)), head="crownflowers", acc="bell")),
    ("Dun", dict(coat=((160, 142, 120, 255), (112, 96, 80, 255), (196, 180, 156, 255), (230, 190, 180, 255), (240, 232, 220, 255)), eyes="button", spots=False, acc_col=((120, 200, 255, 255), (190, 230, 255, 255)))),
    ("Snow", dict(coat=((236, 236, 240, 255), (190, 190, 200, 255), (250, 250, 252, 255), (250, 200, 210, 255), (255, 255, 255, 255)), spots=False, head="headbow", acc="pearls", acc_col=((200, 160, 255, 255), (230, 210, 255, 255)))),
    ("Sunset", dict(coat=((226, 134, 78, 255), (178, 92, 46, 255), (246, 176, 120, 255), (250, 200, 170, 255), (255, 238, 210, 255)), head="crown", acc="bow", acc_col=((255, 100, 140, 255), (255, 170, 190, 255)), eyes="big")),
]

if __name__ == "__main__":
    import sys
    p, f, g = piggy(), fawn(), fawn(True)
    sh = Image.new("RGB", (p.width * 6 + f.width * 16 + 80, max(p.height * 6, f.height * 8) + 20), (60, 60, 60))
    sh.paste(p.resize((p.width * 6, p.height * 6), Image.NEAREST), (10, 10), p.resize((p.width * 6, p.height * 6), Image.NEAREST))
    fb = f.resize((f.width * 8, f.height * 8), Image.NEAREST); sh.paste(fb, (p.width * 6 + 40, 10), fb)
    gb = g.resize((g.width * 8, g.height * 8), Image.NEAREST); sh.paste(gb, (p.width * 6 + f.width * 8 + 60, 10), gb)
    sh.save(sys.argv[1])
