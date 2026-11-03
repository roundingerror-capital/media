"""Readability checks for library sprites (rec-marketing-pixel-art section 6), one strip per sprite:
1x · 4x (+frames) · silhouette · grayscale · next to Theo at true scale (both x4) · phone size (both x2 on a dark scene).
    python3 tools/lib_check.py <out.png> [ID ...]   (no ids = every sprite of the given genre prefix, e.g. FOOD)"""
import os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib
THEO = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sprites", "theo_sprite_1x.png")).convert("RGBA")
BG = (30, 32, 44)

def sil(im):
    out = Image.new("RGBA", im.size); px = out.load(); s = im.load()
    for y in range(im.height):
        for x in range(im.width):
            if s[x, y][3]: px[x, y] = (20, 20, 24, 255)
    return out

def gray(im):
    g = im.convert("LA").convert("RGBA"); g.putalpha(im.split()[3]); return g

def up(im, k): return im.resize((im.width * k, im.height * k), Image.NEAREST)

def strip(sid):
    fr, tk = lib.frames(sid); still = fr[0]; s = lib.info(sid); w, h = s["size"]
    cells = [up(still, 1), *[up(f, 4) for f in fr[:4]], up(sil(still), 4), up(gray(still), 4)]
    # next to Theo: both share the same ground line, same scale
    pair = Image.new("RGBA", (THEO.width + w + 4, max(THEO.height, h)), (0, 0, 0, 0))
    pair.paste(THEO, (0, pair.height - THEO.height), THEO); pair.paste(still, (THEO.width + 4, pair.height - h), still)
    cells += [up(pair, 4), up(pair, 2)]
    H = max(c.height for c in cells) + 30; W = sum(c.width + 16 for c in cells) + 16
    out = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(out); x = 16
    for c in cells:
        out.paste(c, (x, H - 24 - c.height), c); x += c.width + 16
    d.text((16, H - 18), f"{sid} · {s['title']} · {w}x{h} · {len(fr)}f · 1x | 4x frames | silhouette | grayscale | with Theo x4 | phone x2", fill=(200, 240, 60))
    return out

if __name__ == "__main__":
    out = sys.argv[1]; ids = sys.argv[2:]
    if len(ids) == 1 and "-" not in ids[0]: ids = lib.ids(ids[0])
    ims = [strip(i) for i in ids]; W = max(i.width for i in ims); H = sum(i.height for i in ims)
    sheet = Image.new("RGB", (W, H), BG); y = 0
    for i in ims: sheet.paste(i, (0, y)); y += i.height
    sheet.save(out); print(out, len(ims))
