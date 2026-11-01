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

def fawn():
    """64x84 shadow-realm fawn: big soft ears with a flower, long lashes and glowing eyes, dappled spots,
    a little bow-tied scarf. Shadow body like the boss's; the light comes from the rim and the eyes."""
    im = Image.new("RGBA", (64, 84)); d = ImageDraw.Draw(im)
    S, S2, SP, IN = (30, 22, 32, 255), (50, 40, 54, 255), (104, 90, 112, 255), (66, 44, 62, 255)
    # legs + hooves
    for x in (24, 35):
        d.rectangle([x, 66, x + 4, 80], fill=S); d.rectangle([x, 78, x + 4, 82], fill=(14, 10, 16, 255))
    # body
    d.ellipse([19, 42, 45, 72], fill=S); d.ellipse([24, 48, 40, 70], fill=S2)
    for e in ([24, 48, 27, 51], [36, 52, 39, 55], [27, 58, 30, 61], [38, 62, 40, 64], [20, 56, 22, 58]): d.ellipse(e, fill=SP)
    # scarf with a bow
    d.rectangle([22, 40, 42, 44], fill=(110, 40, 70, 255))
    d.polygon([(32, 42), (26, 38), (26, 47)], fill=(150, 60, 95, 255)); d.polygon([(32, 42), (38, 38), (38, 47)], fill=(150, 60, 95, 255))
    d.rectangle([31, 41, 33, 43], fill=(190, 90, 130, 255))
    # neck
    d.rectangle([27, 34, 37, 42], fill=S)
    # ears: big soft leaves, tilted out (drawn flat, rotated, pasted)
    for cx, ang in ((11, -38), (53, 38)):
        e = Image.new("RGBA", (26, 14)); ed = ImageDraw.Draw(e)
        ed.ellipse([0, 1, 25, 12], fill=S); ed.ellipse([5, 4, 21, 9], fill=IN); ed.rectangle([0, 0, 3, 13], fill=(0, 0, 0, 0)) if False else None
        e = e.rotate(ang, resample=Image.NEAREST, expand=True)
        im.alpha_composite(e, (cx - e.width // 2, 10 - e.height // 2))
    d = ImageDraw.Draw(im)
    # head
    d.ellipse([14, 6, 50, 38], fill=S)
    d.ellipse([24, 24, 40, 43], fill=S2)                       # long muzzle
    d.ellipse([29, 36, 35, 40], fill=(10, 6, 12, 255)); d.point([(30, 37)], fill=(140, 130, 150, 255))  # glossy nose
    for e in ([28, 9, 31, 12], [34, 11, 36, 13], [24, 12, 26, 14]): d.ellipse(e, fill=SP)
    # eyes: big, glowing, lashes
    for x0, side in ((18, -1), (36, 1)):
        d.ellipse([x0, 17, x0 + 10, 27], fill=(236, 228, 240, 255))
        d.ellipse([x0 + 2, 18, x0 + 9, 26], fill=(40, 22, 44, 255))
        d.rectangle([x0 + 3, 19, x0 + 4, 20], fill=(255, 255, 255, 255)); d.point([(x0 + 7, 24)], fill=(255, 255, 255, 255))
        ox = x0 if side < 0 else x0 + 10
        d.line([(ox, 18), (ox + 3 * side, 15)], fill=(10, 6, 12, 255)); d.line([(ox + 2 * (-side) + (0 if side < 0 else 0), 17), (ox - side, 13)], fill=(10, 6, 12, 255))
        d.line([(x0 + 5, 16), (x0 + 5 + side, 13)], fill=(10, 6, 12, 255))
    # flower behind the right ear
    fx, fy = 47, 8
    for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2)): d.ellipse([fx + dx - 2, fy + dy - 2, fx + dx + 2, fy + dy + 2], fill=(255, 150, 190, 255))
    d.ellipse([fx - 1, fy - 1, fx + 1, fy + 1], fill=(255, 220, 120, 255))
    return _pad(im, 2)

if __name__ == "__main__":
    import sys
    p, f = piggy(), fawn()
    sh = Image.new("RGB", (p.width * 6 + f.width * 8 + 60, max(p.height * 6, f.height * 8) + 20), (60, 60, 60))
    sh.paste(p.resize((p.width * 6, p.height * 6), Image.NEAREST), (10, 10), p.resize((p.width * 6, p.height * 6), Image.NEAREST))
    fb = f.resize((f.width * 8, f.height * 8), Image.NEAREST); sh.paste(fb, (p.width * 6 + 40, 10), fb)
    sh.save(sys.argv[1])
