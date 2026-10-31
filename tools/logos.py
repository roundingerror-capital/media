"""Platform logos for the end card (the boss 2026-10-31: real Instagram / TikTok / YouTube logos instead of text tags).
Glyphs: simple-icons 13.21.0 (CC0 SVG paths, unaltered). Colors: each brand's own (IG gradient square, TikTok black with
cyan/red offset, YouTube red play button). Used only as "follow us on" marks, never altered or animated beyond scaling."""
import os, io
import cairosvg
from PIL import Image, ImageDraw, ImageChops
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, "logos")
def glyph(name, size, color):
    svg = open(os.path.join(D, name + ".svg")).read().replace("<path ", f'<path fill="{color}" ')
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode(), output_width=size, output_height=size))).convert("RGBA")
def _rounded_mask(s, r):
    m = Image.new("L", (s, s), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, s - 1, s - 1], radius=r, fill=255); return m
def instagram(s):
    import numpy as np
    yy, xx = np.mgrid[0:s, 0:s] / s; t = np.clip(np.sqrt((xx - 0.1) ** 2 + (yy - 1.05) ** 2) / 1.35, 0, 1)
    stops = [(0, (254, 218, 117)), (0.25, (250, 126, 30)), (0.5, (214, 41, 118)), (0.75, (150, 47, 191)), (1, (79, 91, 213))]
    out = np.zeros((s, s, 3))
    for (a, ca), (b, cb) in zip(stops, stops[1:]):
        k = ((t >= a) & (t <= b)); u = ((t - a) / (b - a))[..., None]
        out = np.where(k[..., None], np.array(ca) * (1 - u) + np.array(cb) * u, out)
    im = Image.fromarray(out.astype("uint8"), "RGB").convert("RGBA"); im.putalpha(_rounded_mask(s, int(s * 0.23)))
    g = glyph("instagram", int(s * 0.62), "#FFFFFF"); im.alpha_composite(g, ((s - g.width) // 2, (s - g.height) // 2)); return im
def tiktok(s):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); ImageDraw.Draw(im).rounded_rectangle([0, 0, s - 1, s - 1], radius=int(s * 0.23), fill="#000000")
    n = int(s * 0.58); o = max(2, s // 40); x = (s - n) // 2; y = (s - n) // 2
    im.alpha_composite(glyph("tiktok", n, "#25F4EE"), (x - o, y - o)); im.alpha_composite(glyph("tiktok", n, "#FE2C55"), (x + o, y + o))
    im.alpha_composite(glyph("tiktok", n, "#FFFFFF"), (x, y)); return im
def youtube(s):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); n = int(s * 0.96)
    d = ImageDraw.Draw(im); d.rectangle([s * 0.36, s * 0.34, s * 0.68, s * 0.66], fill="#FFFFFF")  # shows through the play cut-out
    im.alpha_composite(glyph("youtube", n, "#FF0000"), ((s - n) // 2, (s - n) // 2)); return im
MAKERS = {"INSTAGRAM": instagram, "TIKTOK": tiktok, "YOUTUBE": youtube}
_C = {}
def logo(net, size):
    k = (net, size)
    if k not in _C: _C[k] = MAKERS[net](size)
    return _C[k]
if __name__ == "__main__":
    row = Image.new("RGBA", (3 * 200 + 40, 240), (20, 20, 20, 255))
    for i, n in enumerate(MAKERS): row.alpha_composite(logo(n, 180), (20 + i * 200, 30))
    row.save("/tmp/logos_row.png"); print("ok")
