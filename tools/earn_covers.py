"""Earnings cover variety (the boss 2026-11-01: "all earnings videos have the same cover, please make them look different").
Four layouts x four backgrounds, chosen per video from the casting ledger so no two videos in a month share a (layout, background)
pair, and the cover shows the video's own opening cast (not Penny + Theo every time). Same ticker + month -> same cover on a re-render.
Every number on the cover is a field of the Theo sheet; the leading +/- is drawn smaller and apart from the digits (OCR).
Pixel art (sprites, buildings) is scaled by whole numbers with NEAREST only (rec-marketing-pixel-art); rotated elements are text, never sprites.
  layouts: stack (ticker + figure + cast) · bignum (the figure fills the frame, a sticker, one big face) · band (diagonal lime band,
           cast talking in bubbles) · coaster (the rollercoaster track from the video with Kit in the cart)
  backgrounds: black · office (standup plate, dimmed) · lime (inverted: lime paper, black ink) · skyline (asset-library buildings at night)
"""
import os, json, random, math
from PIL import Image, ImageDraw
import daily, earn_charts as EC
from make_reel import W, H, archivo, mono, fit
M, LIME, INK, MUT = daily.M, daily.LIME, daily.INK, daily.MUT
LAYOUTS = ["stack", "bignum", "band", "coaster"]
BGS = ["black", "office", "lime", "skyline"]
PLATE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "work", "interest", "plate_standup_clean.png"))

def pick(T, month, ledger_month):
    """(layout, bg) for this video; recorded in the casting ledger month under "covers" so the batch never repeats a pair."""
    cov = ledger_month.setdefault("covers", {})
    if T in cov: return cov[T]["layout"], cov[T]["bg"]
    r = random.Random(f"cover-{T}-{month}")
    used = [(c["layout"], c["bg"]) for c in cov.values()]
    lay_count = {l: sum(1 for a, _ in used if a == l) for l in LAYOUTS}; bg_count = {b: sum(1 for _, a in used if a == b) for b in BGS}
    lays = [l for l in LAYOUTS if lay_count[l] == min(lay_count.values())]; bgs = [b for b in BGS if bg_count[b] == min(bg_count.values())]
    for _ in range(50):
        L, B = r.choice(lays), r.choice(bgs)
        if (L, B) not in used: break
    cov[T] = {"layout": L, "bg": B}
    return L, B

def sprite(name, k, flip=False):
    s = daily.sprite_state(name, False, 0)
    if flip: s = s.transpose(Image.FLIP_LEFT_RIGHT)
    return s.resize((s.width * k, s.height * k), Image.NEAREST)

def paste(img, s, x, y):
    img.paste(s, (int(x), int(y)), s)

def bubble(img, text, cx, y_bottom, tail_x, size=46, fill="#FFFFFF", ink="#0B0B0B"):
    """White meme bubble, dark text, tail toward (tail_x, below). Returns top y."""
    d = ImageDraw.Draw(img); f = fit(text, W - 2 * M - 60, size, wdth=110, wght=800); tw = d.textlength(text, font=f); pw, ph = 28, 22
    x0, x1 = cx - tw / 2 - pw, cx + tw / 2 + pw; y1 = y_bottom; y0 = y1 - f.size - 2 * ph
    d.rounded_rectangle([x0 + 6, y0 + 8, x1 + 6, y1 + 8], radius=26, fill=(0, 0, 0, 160))
    d.rounded_rectangle([x0, y0, x1, y1], radius=26, fill=fill)
    tx = max(x0 + 40, min(x1 - 40, tail_x)); d.polygon([(tx - 22, y1 - 4), (tx + 22, y1 - 4), (tail_x, y1 + 42)], fill=fill)
    d.text((cx, y1 - ph - 4), text, font=f, fill=ink, anchor="ms"); return y0

def sticker(img, text, cx, cy, ang, size=120, fill=LIME, ink="#0B0B0B"):
    """Rotated text sticker (text only; sprites are never rotated)."""
    f = archivo(size, 125, 900); tmp = Image.new("RGBA", (W, 400), (0, 0, 0, 0)); d = ImageDraw.Draw(tmp)
    tw = d.textlength(text, font=f); d.rounded_rectangle([W / 2 - tw / 2 - 30, 60, W / 2 + tw / 2 + 30, 60 + size + 50], radius=22, fill=fill)
    d.text((W / 2, 60 + size + 10), text, font=f, fill=ink, anchor="ms")
    tmp = tmp.rotate(ang, resample=Image.BICUBIC, expand=True)
    img.paste(tmp, (int(cx - tmp.width / 2), int(cy - tmp.height / 2)), tmp)

def figure(d, big, x, y, size, col, anchor_mid=False, maxw=None):
    """Draw '+/-13.3%?' with the sign smaller and apart (OCR reads a joined +/- as '4'). Shrinks to maxw. Returns the width."""
    maxw = maxw or (W - 2 * M)
    while True:
        if big.startswith("\u00b1"):
            pf = archivo(int(size * .58), 125, 900); nf = archivo(size, 125, 900); num = big[1:]
            pw = d.textlength("\u00b1", font=pf); nw = d.textlength(num, font=nf); gap = int(size * .14); tot = pw + gap + nw
        else:
            nf = archivo(size, 125, 900); tot = d.textlength(big, font=nf)
        if tot <= maxw or size <= 60: break
        size -= 8
    x0 = x - tot / 2 if anchor_mid else x
    if big.startswith("\u00b1"):
        d.text((x0, y - int(size * .12)), "\u00b1", font=pf, fill=col, anchor="ls"); d.text((x0 + pw + gap, y), num, font=nf, fill=col, anchor="ls")
    else: d.text((x0, y), big, font=nf, fill=col, anchor="ls")
    return tot

def background(kind):
    if kind == "black": return Image.new("RGB", (W, H), "#000000"), INK, LIME, MUT
    if kind == "lime": return Image.new("RGB", (W, H), LIME), "#0B0B0B", "#0B0B0B", "#3A4A10"
    if kind == "office":
        im = daily.office_bg({"bg": PLATE, "bg_dim": 0.30, "bg_blur": 1.5}); return im, INK, LIME, MUT
    # skyline: night sky, stars, asset-library buildings along the bottom (pixel art x3, NEAREST)
    import assets
    im = Image.new("RGB", (W, H), (6, 8, 18)); d = ImageDraw.Draw(im); r = random.Random(7)
    for _ in range(90): x, y = r.randrange(W), r.randrange(0, 1300); d.rectangle([x, y, x + 2, y + 2], fill=(r.choice([120, 180, 230]),) * 3)
    x = -40
    for aid in ("BLD-01", "BLD-06", "BLD-03-F5", "BLD-04", "BLD-02", "BLD-05"):
        b = assets.get(aid); k = 3 if b.height < 400 else 2; b = b.resize((b.width * k, b.height * k), Image.NEAREST)
        im.paste(b, (x, H - b.height + 40), b); x += b.width - 30
        if x > W: break
    dim = Image.new("RGB", (W, H), (0, 0, 0)); im = Image.blend(im, dim, 0.35)
    return im, INK, LIME, MUT

def cover(sheet, out_jpg, cast, layout, bg):
    from earnings import normalize, when, straddle, pct
    sheet = normalize(sheet); n = sheet["numbers"]; T = sheet["ticker"]; day, tm = when(n["report"]); xs = straddle(n, False); N = len(n["last_8_next_day_moves"])
    big = f"±{pct(xs['pct_of_spot'])}?" if xs else f"{pct(n['summary']['average_size_of_move_pct'])}"
    sub = f"what the last {N} reports say"; kick = f"EARNINGS PREVIEW · {day.upper()}"
    img, ink, acc, mut = background(bg); d = ImageDraw.Draw(img)
    a, b = (cast + ["theo", "penny"])[:2]
    r = random.Random(f"{T}-{layout}")
    if layout == "stack":
        d.text((M, 420), kick, font=mono(34, True), fill=acc, anchor="ls")
        d.text((M, 640), T, font=archivo(260, 125, 900), fill=ink, anchor="ls")
        figure(d, big, M, 860, 200, acc, maxw=W - 2 * M)
        d.text((M, 960), sub, font=fit(sub, daily.SAFE_R - M, 64, wdth=110, wght=800), fill=ink, anchor="ls")
        sa = sprite(a, 11); sb = sprite(b, 9, flip=True); paste(img, sa, W // 2 - sa.width // 2 - 120, 1700 - sa.height); paste(img, sb, W // 2 + 160, 1700 - sb.height)
    elif layout == "bignum":
        d.text((W // 2, 430), f"{T} · {kick}", font=fit(f"{T} · {kick}", W - 2 * M, 40), fill=acc, anchor="ms")
        tw = figure(d, big, W // 2, 820, 330, ink, anchor_mid=True, maxw=W - 2 * M)
        d.text((W // 2, 930), sub.upper(), font=fit(sub.upper(), W - 2 * M, 54, wdth=110, wght=800), fill=mut, anchor="ms")
        sa = sprite(a, 16); paste(img, sa, -40, H - sa.height + 160)            # one huge face rising from the corner
        sb = sprite(b, 8, flip=True); paste(img, sb, W - sb.width - 60, 1700 - sb.height)
        sticker(img, r.choice(["BIG ONE?!", "HOLD ON", "WAIT WHAT", "OH BOY"]), W - 300, 1180, r.choice([-14, 12, -9]), size=96, fill=acc if bg != "lime" else "#0B0B0B", ink="#0B0B0B" if bg != "lime" else LIME)
    elif layout == "band":
        band = Image.new("RGBA", (W * 2, 260), (0, 0, 0, 0)); bd = ImageDraw.Draw(band)
        bcol = acc if bg != "lime" else "#0B0B0B"; bd.rectangle([0, 0, W * 2, 260], fill=bcol)
        bd.text((W, 222), f"{T}   {T}   {T}", font=archivo(210, 125, 900), fill="#0B0B0B" if bg != "lime" else LIME, anchor="ms")
        band = band.rotate(-11, resample=Image.BICUBIC, expand=True); img.paste(band, (W // 2 - band.width // 2, 760 - band.height // 2), band); d = ImageDraw.Draw(img)
        d.text((M, 420), kick, font=mono(34, True), fill=acc, anchor="ls"); d.text((M, 540), "EARNINGS", font=archivo(110, 125, 900), fill=ink, anchor="ls")
        figure(d, big, W // 2, 1100, 170, ink, anchor_mid=True)
        d.text((W // 2, 1150), sub.upper(), font=mono(30, True), fill=mut, anchor="ms")
        sa = sprite(a, 8); sb = sprite(b, 8, flip=True); xa = 110; xb = W - 110 - sb.width
        paste(img, sa, xa, 1700 - sa.height); paste(img, sb, xb, 1700 - sb.height)
        la, lb = r.choice([("BIG ONE?!", "numbers first."), ("UP OR DOWN?", "nobody knows."), ("HOLD?", "look back first.")])
        top = 1700 - max(sa.height, sb.height)
        bubble(img, la, xa + sa.width // 2 + 40, top - 20, xa + sa.width // 2, 40)
        bubble(img, lb, xb + sb.width // 2 - 40, top - 20, xb + sb.width // 2, 36)
    else:  # coaster
        d.text((M, 420), kick, font=mono(34, True), fill=acc, anchor="ls")
        d.text((M, 560), T, font=archivo(150, 125, 900), fill=ink, anchor="ls")
        tx = M + d.textlength(T, font=archivo(150, 125, 900)) + 50; figure(d, big, tx, 560, 120, acc, maxw=W - M - tx)
        vals = [m["move_pct"] for m in n["last_8_next_day_moves"]]; labels = [f"{int(m['report'][5:7])}/{m['report'][2:4]}" for m in n["last_8_next_day_moves"]]
        if bg == "lime":   # the track's lime would vanish on lime paper: draw it on a dark card
            d.rounded_rectangle([M - 30, 600, daily.SAFE_R + 30, 1180], radius=24, fill=(14, 14, 14));
        EC.coaster(img, d, 2.19, 580, vals, labels, n["summary"]["average_size_of_move_pct"])
        d.text((M, 1260), sub, font=fit(sub, daily.SAFE_R - M, 56, wdth=110, wght=800), fill=ink, anchor="ls")
        sa = sprite(a, 8); sb = sprite(b, 8, flip=True); paste(img, sa, 90, 1700 - sa.height); paste(img, sb, W - 90 - sb.width, 1700 - sb.height)
        bubble(img, r.choice(["WEEEE!", "AGAIN!", "HOLD ON!"]), W // 2, 1560, W // 2 - 10, 44)
    img = daily.nfa(img); img.save(out_jpg, quality=92); return out_jpg
