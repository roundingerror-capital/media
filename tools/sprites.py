import re, glob, os
from PIL import Image
def sprite(path):
    s = open(path).read(); m = re.search(r'<svg.*?</svg>', s, re.S)
    if not m: return None
    svg = m.group(0)
    rs = [(float(a), float(b), float(c), float(d), e) for a, b, c, d, e in re.findall(r'<rect x="(-?[\d.]+)" y="(-?[\d.]+)" width="([\d.]+)" height="([\d.]+)" fill="(#\w+)"', svg)]
    if not rs: return None
    x0 = int(min(r[0] for r in rs)); y0 = int(min(r[1] for r in rs)); x1 = int(max(r[0] + r[2] for r in rs)); y1 = int(max(r[1] + r[3] for r in rs))
    im = Image.new("RGBA", (x1 - x0, y1 - y0), (0, 0, 0, 0))
    for x, y, w, h, c in rs:
        col = tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
        for i in range(int(w)):
            for j in range(int(h)): im.putpixel((int(x) - x0 + i, int(y) - y0 + j), col)
    return im
if __name__ == "__main__":
    import sys
    S = sys.argv[1]; out = sys.argv[2]
    srcs = glob.glob(S + "drafts/project/*.html") + glob.glob(S + "finals/project/*.html") + glob.glob(S + "canvasroz2/project/V17*.html") + \
           glob.glob(S + "canvasroz4/project/V17RozSagePixel.html") + glob.glob(S + "canvasroz/project/V17Roz*Pixel.dc.html") + glob.glob(S + "canvasroz3/project/V18*.html") + glob.glob(S + "canvasroz4/project/V19*.html")
    n = 0
    for p in srcs:
        im = sprite(p)
        if im is None or im.width < 20: continue
        im.save(os.path.join(out, os.path.basename(p).replace(".dc.html", ".png"))); n += 1
    print(n)
