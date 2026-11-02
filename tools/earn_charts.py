"""Earnings chart styles (the boss 2026-11-02: "4 different chart styles... integrated... MEME IT UP").
Each style draws the last-N next-day moves into the scene at y and returns the new y. Every number comes from the spec (Theo sheet).
Styles: scoreboard (LED board on the office wall) · coaster (a rollercoaster track, Kit riding the cart) · cards (six report cards
slammed down, stamped UP/DOWN) · monitor (Theo's CRT trading screen with scanlines and a ticker)."""
import math, random
from PIL import Image, ImageDraw, ImageFilter
import daily
from make_reel import W, archivo, mono, fade
M, SAFE_R, INK, MUT = daily.M, daily.SAFE_R, daily.INK, daily.MUT
LIME = (200, 240, 60); CORAL = (255, 107, 91); LED_OFF = (26, 34, 24); PAPER = (244, 236, 214)
def _lab(v): return daily.pctlab(v).lstrip("+")
def _ease(k): return 1 - (1 - max(0, min(1, k))) ** 3

def scoreboard(img, d, u, y, vals, labels, avg):
    """A stadium LED scoreboard bolted to the wall: segmented lime/coral LED bars light up one by one, a blinking LIVE dot."""
    x0, x1 = M - 24, SAFE_R + 24; top = y + 40; h = 480; bot = top + h
    d.rounded_rectangle([x0 - 10, top - 10, x1 + 10, bot + 10], radius=18, fill=(36, 38, 42)); d.rounded_rectangle([x0, top, x1, bot], radius=12, fill=(8, 12, 8))
    for bx, by in ((x0 + 10, top + 10), (x1 - 10, top + 10), (x0 + 10, bot - 10), (x1 - 10, bot - 10)): d.ellipse([bx - 6, by - 6, bx + 6, by + 6], fill=(90, 94, 100)); d.ellipse([bx - 3, by - 3, bx + 3, by + 3], fill=(140, 144, 150))
    d.text((x0 + 36, top + 54), "LAST 6 REPORTS", font=mono(26, True), fill=LIME, anchor="ls")
    if int(u * 2) % 2 == 0: d.ellipse([x1 - 150, top + 32, x1 - 130, top + 52], fill=CORAL)
    d.text((x1 - 118, top + 54), "LIVE", font=mono(24, True), fill=INK, anchor="ls")
    n = len(vals); hi = max(max(abs(v) for v in vals), avg or 0) or 1; zero = top + 290; unit = 24; gap = 6
    cw = (x1 - x0 - 72) / n
    for i, (v, lab) in enumerate(zip(vals, labels)):
        cx = x0 + 36 + (i + .5) * cw; k = _ease(u * 1.6 - i * .18); segs = int(round(abs(v) / hi * 7 * k)); col = LIME if v >= 0 else CORAL
        for sgn_seg in range(7):   # dim grid both ways
            for sgn in (1, -1):
                yy = zero - sgn * (sgn_seg + 1) * unit + (0 if sgn > 0 else unit - 4)
                d.rectangle([cx - 30, yy, cx + 30, yy + unit - gap], fill=LED_OFF)
        for sidx in range(segs):
            yy = zero - (sidx + 1) * unit if v >= 0 else zero + sidx * unit + 4
            d.rectangle([cx - 30, yy, cx + 30, yy + unit - gap], fill=col)
        if k > .95: d.text((cx, zero - 7 * unit - 20 if v >= 0 else zero + 7 * unit + 44), _lab(v), font=mono(26, True), fill=col, anchor="ms")
        d.text((cx, bot - 28), lab, font=mono(20, True), fill=(160, 200, 90), anchor="ms")
    d.line([(x0 + 24, zero), (x1 - 24, zero)], fill=(70, 90, 50), width=2)
    return bot + 20

def coaster(img, d, u, y, vals, labels, avg):
    """A rollercoaster: the track rides each report's move (lime climbs, coral drops) on wooden trestles; Kit rides the cart on the
    drawn end, hops at every peak, yells on the drops, then flies off the end, lands on the ground rail and bounces to a stop."""
    x0, x1 = M, SAFE_R; top = y + 60; bot = top + 440; n = len(vals); hi = max(abs(v) for v in vals) or 1
    pts = [(x0 + 40 + i * (x1 - x0 - 80) / (n - 1), top + 200 - v / hi * 160) for i, v in enumerate(vals)]
    DRAW = 2.2; kk = _ease(min(1, u / DRAW)); shown = kk * (n - 1)
    ground = bot - 24
    d.rectangle([x0 - 10, ground, x1 + 10, bot], fill=(70, 50, 40)); d.rectangle([x0 - 10, ground, x1 + 10, ground + 4], fill=(110, 80, 60))
    for i in range(n):
        px, py = pts[i]
        if i <= shown + 1e-6:
            for sx in (-14, 14): d.line([(px + sx, py), (px + sx, ground)], fill=(120, 90, 70), width=5)
            for cy in range(int(py) + 30, int(ground) - 30, 44): d.line([(px - 14, cy), (px + 14, cy + 22)], fill=(100, 72, 56), width=3); d.line([(px + 14, cy), (px - 14, cy + 22)], fill=(100, 72, 56), width=3)
    for i in range(n - 1):
        if i > shown: break
        a, b = pts[i], pts[i + 1]; frac = min(1, shown - i); bx = a[0] + (b[0] - a[0]) * frac; by = a[1] + (b[1] - a[1]) * frac
        col = LIME if vals[i + 1] >= 0 else CORAL
        d.line([(a[0], a[1] + 10), (bx, by + 10)], fill=(50, 40, 36), width=16); d.line([(a[0], a[1]), (bx, by)], fill=col, width=10)
        for s_ in range(0, int(frac * 100), 12):
            tx = a[0] + (b[0] - a[0]) * s_ / 100; ty = a[1] + (b[1] - a[1]) * s_ / 100; d.line([(tx, ty - 6), (tx, ty + 12)], fill=(60, 48, 40), width=3)
    for i, (v, lab) in enumerate(zip(vals, labels)):
        d.text((pts[i][0], bot + 30), lab, font=mono(20), fill=MUT, anchor="ms")
    # value tags last, each on its own black pill so the trestles never run through the digits (OCR read "-6.9%" as "-6%9")
    f = mono(28, True)
    for i, v in enumerate(vals):
        if i > shown + .01: continue
        px, py = pts[i]; col = LIME if v >= 0 else CORAL; txt = _lab(v); tw = d.textlength(txt, font=f)
        ty = py - 44 if v >= 0 else py + 30
        d.rounded_rectangle([px - tw / 2 - 10, ty - 4, px + tw / 2 + 10, ty + 36], radius=8, fill=(0, 0, 0))
        d.text((px, ty + 28), txt, font=f, fill=col, anchor="ms")
    # the cart
    yell = None
    if u <= DRAW:
        i = min(n - 2, int(shown)); frac = shown - i; a, b = pts[i], pts[min(n - 1, i + 1)]
        cx = a[0] + (b[0] - a[0]) * frac; cy = a[1] + (b[1] - a[1]) * frac
        ang = -math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
        hop = 22 * math.sin(math.pi * min(1, frac / .25)) if frac < .25 and i > 0 else 0          # a little hop over every peak/trough
        if vals[i + 1] < 0 and .15 < frac < .95: yell = "WEEEEE!"
        elif vals[i + 1] >= 0 and vals[i + 1] >= hi * .8 and .3 < frac < .95: yell = "TO THE TOP!"
        cy -= hop
    else:   # off the end: a parabola from the last point down to the ground rail, two bounces, a dust puff, then parked
        v = u - DRAW; lx, ly = pts[-1]; vx = 150; g = 1500
        cx = min(x1 - 40, lx + vx * v); cy = ly + .5 * g * v * v
        tland = math.sqrt(max(0, 2 * (ground - 30 - ly) / g))
        if v > tland:
            w = v - tland; cy = ground - 30 - abs(40 * math.sin(w * 7)) * max(0, 1 - w / .9); cx = min(x1 - 40, lx + vx * tland + 60 * min(w, .9))
            if w < .6:
                for k in range(5): d.ellipse([cx - 40 - k * 14 - w * 60, ground - 14 - k * 6, cx - 26 - k * 14 - w * 60, ground - 2 - k * 6], fill=(150, 130, 110))
            if w < 1.2: yell = "AGAIN!"
        ang = -math.degrees(math.atan2(min(vx, g * v), vx)) * .6 if v <= tland else 0
    cart = Image.new("RGBA", (120, 90)); cd = ImageDraw.Draw(cart)
    cd.rounded_rectangle([6, 44, 114, 84], radius=14, fill=(230, 60, 90)); cd.rounded_rectangle([14, 50, 106, 78], radius=10, fill=(255, 110, 140))
    cd.ellipse([18, 72, 42, 90], fill=(30, 30, 30)); cd.ellipse([78, 72, 102, 90], fill=(30, 30, 30)); cd.ellipse([24, 78, 36, 86], fill=(90, 90, 90)); cd.ellipse([84, 78, 96, 86], fill=(90, 90, 90))
    kit = daily.sprite_state("kit", False, u); kit = kit.resize((kit.width * 2, kit.height * 2), Image.NEAREST); cart.alpha_composite(kit, (60 - kit.width // 2, 48 - kit.height))
    cart = cart.rotate(ang, resample=Image.NEAREST, expand=True); img.paste(cart, (int(cx - cart.width / 2), int(cy - cart.height / 2 - 30)), cart)
    if yell:
        f = archivo(30, 110, 900); tw = d.textlength(yell, font=f); bx0 = int(min(max(x0, cx - tw / 2 - 16), x1 - tw - 32)); by0 = int(cy - 150)
        d.rounded_rectangle([bx0, by0, bx0 + tw + 32, by0 + 52], radius=12, fill=(255, 255, 255), outline=(0, 0, 0), width=3)
        d.polygon([(int(cx) - 10, by0 + 52), (int(cx) + 10, by0 + 52), (int(cx), by0 + 70)], fill=(255, 255, 255))
        d.text((bx0 + 16, by0 + 38), yell, font=f, fill=(0, 0, 0), anchor="ls")
    return bot + 50

def cards(img, d, u, y, vals, labels, avg):
    """Six report cards slammed onto the table one by one, each with the date, a giant number and a rubber stamp."""
    x0, x1 = M, SAFE_R; n = len(vals); cw = 240; ch_ = 300; cols = 3; gx = (x1 - x0 - cols * cw) / (cols - 1); top = y + 40
    for i, (v, lab) in enumerate(zip(vals, labels)):
        k = _ease((u - i * .28) / .3)
        if k <= 0: continue
        r, c = divmod(i, cols); cx = x0 + c * (cw + gx) + cw / 2; cy = top + r * (ch_ + 24) + ch_ / 2
        sc = 1.6 - .6 * k; ang = (-6 if i % 2 else 5) * (1 - k * .4)
        card = Image.new("RGBA", (cw + 40, ch_ + 40)); kd = ImageDraw.Draw(card)
        kd.rectangle([26, 26, cw + 26, ch_ + 26], fill=(0, 0, 0, 120)); kd.rectangle([20, 20, cw + 20, ch_ + 20], fill=PAPER); kd.rectangle([20, 20, cw + 20, 56], fill=(60, 56, 50))
        kd.text((cw / 2 + 20, 46), "REPORT  " + lab, font=mono(22, True), fill=PAPER, anchor="ms")
        col = (60, 130, 40) if v >= 0 else (200, 50, 50)
        kd.text((cw / 2 + 20, 180), _lab(v), font=archivo(72 if len(_lab(v)) <= 5 else 60, 110, 900), fill=(40, 36, 34), anchor="ms")
        kd.text((cw / 2 + 20, 215), "next day", font=mono(20), fill=(120, 110, 100), anchor="ms")
        st = Image.new("RGBA", (200, 70)); sd = ImageDraw.Draw(st); sd.rounded_rectangle([2, 2, 197, 67], radius=10, outline=col, width=6); sd.text((100, 52), "UP" if v >= 0 else "DOWN", font=archivo(44, 125, 900), fill=col, anchor="ms")
        st = st.rotate(-12 if v >= 0 else 9, resample=Image.BICUBIC, expand=True); card.alpha_composite(st, (int(cw / 2 + 20 - st.width / 2), 230))
        card = card.rotate(ang, resample=Image.BICUBIC, expand=True); card = card.resize((int(card.width * sc), int(card.height * sc)), Image.BILINEAR) if sc != 1 else card
        img.paste(card, (int(cx - card.width / 2), int(cy - card.height / 2)), card)
    return top + 2 * (ch_ + 24) + 20

def monitor(img, d, u, y, vals, labels, avg):
    """Theo's CRT: a bevelled bezel, a glowing screen with scanlines, bars drawn as candles, a scrolling ticker of the report dates."""
    x0, x1 = M - 20, SAFE_R + 20; top = y + 30; bot = top + 500
    d.rounded_rectangle([x0 - 16, top - 16, x1 + 16, bot + 40], radius=26, fill=(70, 72, 78)); d.rounded_rectangle([x0 - 16, top - 16, x1 + 16, top + 6], radius=26, fill=(96, 98, 104))
    d.rounded_rectangle([x0, top, x1, bot], radius=14, fill=(6, 18, 10))
    glow = Image.new("RGBA", img.size, (0, 0, 0, 0)); ImageDraw.Draw(glow).rounded_rectangle([x0, top, x1, bot], radius=14, fill=(60, 200, 90, 40)); img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(30))) if img.mode == "RGBA" else None
    n = len(vals); hi = max(abs(v) for v in vals) or 1; zero = top + 260; cw = (x1 - x0 - 60) / n
    d.text((x0 + 24, top + 44), "> last_6_reports.next_day_move", font=mono(22, True), fill=(120, 255, 140), anchor="ls")
    for gy in range(top + 70, bot - 60, 40): d.line([(x0 + 20, gy), (x1 - 20, gy)], fill=(14, 40, 22), width=1)
    d.line([(x0 + 20, zero), (x1 - 20, zero)], fill=(60, 120, 70), width=2)
    for i, (v, lab) in enumerate(zip(vals, labels)):
        k = _ease(u * 1.5 - i * .2); cx = x0 + 30 + (i + .5) * cw; yv = zero - v / hi * 170 * k; col = (120, 255, 140) if v >= 0 else (255, 90, 90)
        d.line([(cx, min(zero, yv) - 14 * k), (cx, max(zero, yv) + 14 * k)], fill=col, width=3)
        d.rectangle([cx - 22, min(zero, yv), cx + 22, max(zero, yv)], fill=col)
        if k > .95: d.text((cx, yv - 22 if v >= 0 else yv + 44), _lab(v), font=mono(24, True), fill=col, anchor="ms")
    # scanlines
    sl = Image.new("RGBA", img.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(sl)
    for yy in range(top, bot, 4): sd.line([(x0, yy), (x1, yy)], fill=(0, 0, 0, 70))
    base = img.convert("RGBA"); base.alpha_composite(sl); img.paste(base.convert("RGB")); d = ImageDraw.Draw(img)
    # ticker
    d.rectangle([x0, bot - 50, x1, bot], fill=(4, 10, 6)); tick = "   ".join(("▲ " if v >= 0 else "▼ ") + lab for v, lab in zip(vals, labels)) + "   "
    f = mono(24, True); tw = d.textlength(tick, font=f); off = int(u * 120) % int(tw)
    for rep in range(3): d.text((x1 - 20 - off + rep * tw, bot - 16), tick, font=f, fill=(120, 255, 140), anchor="rs")
    d.rectangle([x0 - 16, bot - 50, x0, bot], fill=(70, 72, 78)); d.rectangle([x1, bot - 50, x1 + 16, bot], fill=(70, 72, 78))
    d.ellipse([x1 - 50, bot + 8, x1 - 36, bot + 22], fill=(120, 255, 140))   # power light
    return bot + 60

STYLES = {"scoreboard": scoreboard, "coaster": coaster, "cards": cards, "monitor": monitor}
def make(style, vals, labels, avg):
    fn = STYLES[style]
    return lambda img, d, u, y: fn(img, d, u, y, vals, labels, avg)
