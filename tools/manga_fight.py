"""THE FIGHT · EP.1 — our HOOD puts vs HOOD, as a manga (2026-10-24). 1080x1920, 30 fps.
Ink-on-paper look: panels with gutters, focus lines, screentone, impact frames, SFX lettering; lime is the only colour.
Every number comes from Theo's weekly fact sheet 20261023-160906-weekly (strikes, expiry, status as of the 10/23 close)."""
import os, sys, math, random, subprocess
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageChops
from make_reel import W, H, FPS, archivo, mono, fit, fade
import daily
PAPER = (242, 240, 232); INKK = (12, 12, 12); LIME = (200, 240, 60); GREY = (150, 150, 146)
SPR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sprites")
T = dict(cover=0.6, page1=1.8, villain=5.0, clash=8.6, impact=10.0, lesson=13.0, standoff=17.0, next=20.5, outro=22.5)
END = T["outro"] + daily.OUTRO_S
def ease(x): x = max(0, min(1, x)); return 1 - (1 - x) ** 3
# ---------- ink helpers
def screentone(size, step=14, r=3, col=INKK, bg=None):
    im = Image.new("RGBA", size, bg or (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for y in range(0, size[1] + step, step):
        o = (y // step) % 2 * step // 2
        for x in range(-step, size[0] + step, step): d.ellipse([x + o - r, y - r, x + o + r, y + r], fill=col)
    return im
TONE = screentone((W, H)); TONE_L = screentone((W, H), 10, 2)
def focus_lines(d, cx, cy, n=140, r0=260, seed=1, col=INKK, rmax=2400):
    rnd = random.Random(seed)
    for i in range(n):
        a = rnd.uniform(0, 2 * math.pi); r1 = r0 + rnd.uniform(0, 220); w = rnd.uniform(3, 14)
        x1, y1 = cx + math.cos(a) * r1, cy + math.sin(a) * r1; x2, y2 = cx + math.cos(a) * rmax, cy + math.sin(a) * rmax
        n_ = (-math.sin(a) * w, math.cos(a) * w)
        d.polygon([(x1, y1), (x2 + n_[0], y2 + n_[1]), (x2 - n_[0], y2 - n_[1])], fill=col)
def speed_lines(d, box, ang, n=70, seed=2, col=INKK):
    rnd = random.Random(seed); x0, y0, x1, y1 = box; L = 3000
    for i in range(n):
        px, py = rnd.uniform(x0, x1), rnd.uniform(y0, y1); w = rnd.uniform(2, 8); l = rnd.uniform(200, 900)
        dx, dy = math.cos(ang) * l, math.sin(ang) * l
        d.line([(px, py), (px + dx, py + dy)], fill=col, width=int(w))
def sfx(img, text, cx, cy, size, rot=-8, fill=INKK, stroke=PAPER, sw=14, wdth=125):
    while size > 40 and archivo(size, wdth, 900).getlength(text) > W * .86: size -= 6
    f = archivo(size, wdth, 900); tmp = Image.new("RGBA", (int(size * len(text) * 1.1) + 200, int(size * 1.6)), (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp); td.text((tmp.width // 2, tmp.height // 2), text, font=f, fill=fill, anchor="mm", stroke_width=sw, stroke_fill=stroke)
    tmp = tmp.rotate(rot, expand=True, resample=Image.BICUBIC); img.paste(tmp, (int(cx - tmp.width / 2), int(cy - tmp.height / 2)), tmp)
def caption_box(d, x, y, text, size=40, w=None, inv=False):
    f = archivo(size, 100, 800); bb = d.textbbox((0, 0), text, font=f); tw = w or bb[2] - bb[0] + 48
    d.rectangle([x, y, x + tw, y + bb[3] - bb[1] + 40], fill=INKK if inv else PAPER, outline=INKK, width=5)
    d.text((x + 24, y + 20 - bb[1]), text, font=f, fill=PAPER if inv else INKK)
def bubble(d, x, y, lines, size=44, tail=None):
    f = archivo(size, 100, 800); hs = [d.textbbox((0, 0), l, font=f) for l in lines]
    w = max(b[2] - b[0] for b in hs) + 90; h = sum(b[3] - b[1] + 16 for b in hs) + 60
    d.ellipse([x - w // 2, y - h // 2, x + w // 2, y + h // 2], fill=(255, 255, 255), outline=INKK, width=6)
    if tail: d.polygon([(x - 30, y + h // 2 - 14), (x + 20, y + h // 2 - 10), tail], fill=(255, 255, 255), outline=INKK); d.line([(x - 28, y + h // 2 - 8), (x + 18, y + h // 2 - 8)], fill=(255, 255, 255), width=10)
    yy = y - h // 2 + 30
    for l, b in zip(lines, hs): d.text((x, yy - b[1]), l, font=f, fill=INKK, anchor="ma"); yy += b[3] - b[1] + 16
def panel(img, box, draw_fn, t, t0, slide=(0, 140), border=10):
    a = ease((t - t0) / .28)
    if a <= 0: return
    x0, y0, x1, y1 = box; pw, ph = x1 - x0, y1 - y0
    p = Image.new("RGB", (pw, ph), PAPER); draw_fn(p, t)
    pd = ImageDraw.Draw(p); pd.rectangle([0, 0, pw - 1, ph - 1], outline=INKK, width=border)
    ox, oy = int(slide[0] * (1 - a)), int(slide[1] * (1 - a))
    img.paste(p, (x0 + ox, y0 + oy))
# ---------- characters (pixel sprites rendered as ink: greyscale, contrast, crisp)
def load_sprite(name):
    return Image.open(os.path.join(SPR, name)).convert("RGBA")
def inked(sp, s, lime_aura=False):
    sp = sp.resize((sp.width * s, sp.height * s), Image.NEAREST)
    a = sp.split()[3]; g = ImageOps.autocontrast(sp.convert("L"), cutoff=2)
    g = g.point(lambda v: 20 if v < 70 else (110 if v < 150 else (205 if v < 215 else 250)))
    out = Image.merge("RGBA", (g, g, g, a))
    if lime_aura:
        ring = a.filter(ImageFilter.MaxFilter(31)); aura = Image.new("RGBA", sp.size, LIME + (0,)); aura.putalpha(ring)
        base = Image.new("RGBA", sp.size, (0, 0, 0, 0)); base.alpha_composite(aura); base.alpha_composite(out); return base
    return out
THEO = load_sprite("theo_sprite_1x.png") if os.path.exists(os.path.join(SPR, "theo_sprite_1x.png")) else None
def villain(h, eyes=True, t=0):
    """HOOD: a hooded storm-cloak with candle-blade arms. Original design, no broker branding."""
    w = int(h * .8); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    flap = math.sin(t * 9) * h * .02
    d.polygon([(w * .5, 0), (w * .82, h * .22), (w * .98 + flap, h), (w * .02 - flap, h), (w * .18, h * .22)], fill=INKK)  # cloak + hood
    d.ellipse([w * .3, h * .1, w * .7, h * .36], fill=(0, 0, 0))  # face void
    if eyes:
        for ex in (.41, .59): d.polygon([(w * ex - w * .06, h * .2), (w * ex + w * .06, h * .2 + (h * .012 if ex < .5 else -h * .012)), (w * ex, h * .245)], fill=(255, 255, 255))
    for i, x in enumerate((.12, .88)):  # candle blades: wick + body
        cx = w * x; top = h * (.32 + .05 * i)
        d.line([(cx, top - h * .08), (cx, top + h * .38)], fill=INKK, width=max(3, int(w * .012)))
        d.rectangle([cx - w * .045, top, cx + w * .045, top + h * .26], fill=(255, 255, 255), outline=INKK, width=max(4, int(w * .014)))
    # cloak folds
    for k in range(6): d.line([(w * (.25 + k * .1), h * .4), (w * (.2 + k * .12), h)], fill=(70, 70, 70), width=max(2, int(w * .01)))
    d.text((w * .5, h * .62), "HOOD", font=archivo(int(h * .09), 125, 900), fill=(255, 255, 255), anchor="mm")
    return im
# ---------- scenes
def page1(t):
    img = Image.new("RGB", (W, H), PAPER); g = 26
    def p1(p, t):
        d = ImageDraw.Draw(p); pw, ph = p.size
        p.paste(TONE_L.crop((0, 0, pw, ph)), (0, 0), TONE_L.crop((0, 0, pw, ph)))
        for y, lab in ((ph * .42, "$100 PUT"), (ph * .62, "$99 PUT")):
            d.rectangle([0, y - 6, pw, y + 6], fill=INKK); d.rectangle([40, y - 86, 420, y - 14], fill=PAPER, outline=INKK, width=6)
            d.text((60, y - 30), lab, font=archivo(52, 110, 900), fill=INKK, anchor="ls")
        caption_box(d, 30, 30, "FRIDAY, OCTOBER 30.", 46, inv=True)
    def p2(p, t):
        d = ImageDraw.Draw(p); pw, ph = p.size; focus_lines(d, pw // 2, ph // 2, 90, 170, 3, rmax=1400)
        if THEO is not None:
            th = inked(THEO, 22); crop = th.crop((0, int(th.height * .12), th.width, int(th.height * .55)))
            p.paste(crop, (pw // 2 - crop.width // 2, ph // 2 - crop.height // 2), crop)
        caption_box(d, 24, ph - 110, "Two puts. One line to hold.", 34)
    def p3(p, t):
        d = ImageDraw.Draw(p); pw, ph = p.size; d.rectangle([0, 0, pw, ph], fill=(30, 30, 30))
        rnd = random.Random(int(t * 15))
        for i in range(70): x = rnd.randint(0, pw); y = rnd.randint(0, ph); d.line([(x, y), (x - 20, y + 70)], fill=(120, 120, 120), width=2)
        v = villain(int(ph * .85), True, t); p.paste(v, (pw // 2 - v.width // 2, ph - v.height), v)
        caption_box(d, 24, 24, "Then HOOD showed up.", 34)
    t0 = T["page1"]
    panel(img, (g, 170, W - g, 820), p1, t, t0, (0, -120))
    panel(img, (g, 820 + g, W // 2 - g // 2, 1720), p2, t, t0 + .7, (-140, 0))
    panel(img, (W // 2 + g // 2, 820 + g, W - g, 1720), p3, t, t0 + 1.4, (140, 0))
    d = ImageDraw.Draw(img); d.text((g, 120), "THE FIGHT · EP. 1", font=mono(32, True), fill=INKK, anchor="ls")
    d.text((W - g, 120), "AS OF 10/23 CLOSE", font=mono(28, True), fill=GREY, anchor="rs")
    return img
def villain_page(t):
    u = t - T["villain"]; img = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(img)
    focus_lines(d, W // 2, 820, 170, 380, 5)
    s = .7 + .3 * ease(u / .35); v = villain(int(1250 * s), True, t)
    sh = random.Random(int(t * 30)).randint(-14, 14) if u < .4 else 0
    img.paste(v, (W // 2 - v.width // 2 + sh, 1780 - v.height), v)
    if u > .1: sfx(img, "DOOOON", W // 2, 330, 210, -6)
    if u > 1.0:
        a = ease((u - 1.0) / .15); st = Image.new("RGBA", (760, 200), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
        sd.rectangle([8, 8, 752, 192], outline=(205, 40, 30), width=14); sd.text((380, 100), "IN THE MONEY", font=archivo(92, 110, 900), fill=(205, 40, 30), anchor="mm")
        st = st.resize((int(760 * (2 - a)), int(200 * (2 - a)))).rotate(10, expand=True); img.paste(st, (W // 2 - st.width // 2, 1180 - st.height // 2), st)
    if u > 1.6: caption_box(d, 60, 1560, "It dove under BOTH our strikes.", 44, inv=True)
    return img
def clash(t):
    u = t - T["clash"]; ti = T["impact"] - T["clash"]
    img = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(img)
    # diagonal split: Theo (top-left) vs HOOD (bottom-right)
    d.polygon([(0, 0), (W, 0), (W, 760), (0, 1160)], fill=PAPER)
    d.polygon([(0, 1160), (W, 760), (W, H), (0, H)], fill=(28, 28, 28))
    speed_lines(d, (0, 0, W, 900), math.radians(-20), 60, 7)
    speed_lines(d, (0, 900, W, H), math.radians(160), 60, 8, col=(90, 90, 90))
    k = ease(u / max(.1, ti))
    if THEO is not None:
        th = inked(THEO, 20, lime_aura=True); img.paste(th, (int(-260 + 320 * k), 1000 - th.height), th)
    v = villain(1000, True, t); v = villain(900, True, t); img.paste(v, (int(W - v.width + 300 - 330 * k), 1840 - v.height), v)
    d.line([(0, 1160), (W, 760)], fill=INKK, width=18)
    if u < ti: sfx(img, "ZAAAAN", 300, 300, 150, -14)
    if u >= ti:
        v2 = u - ti
        if v2 < .2:  # impact frame: invert + white flash
            img = ImageOps.invert(img); d = ImageDraw.Draw(img); focus_lines(d, W // 2, 960, 220, 200, 9, col=(255, 255, 255))
        sfx(img, "KRAK!!", W // 2, 960, int(300 * (1 + max(0, .4 - v2))), 8, fill=LIME, stroke=INKK, sw=18)
        if v2 > .9:
            d = ImageDraw.Draw(img)
            bubble(d, 300, 300, ["GET HIM,", "THEO!!"], 46)
            d.text((300, 420), "— Penny", font=mono(26, True), fill=INKK, anchor="ma")
        if v2 > 1.9:
            d = ImageDraw.Draw(img); bubble(d, W - 300, 1530, ["All green!", "...wait."], 42)
            d.text((W - 300, 1650), "— Ada", font=mono(26, True), fill=PAPER, anchor="ma")
    if u < ti or u - ti >= .2:
        sh = random.Random(int(t * 30)).randint(-12, 12) if 0 <= u - ti < .5 else 0
        if sh: img = ImageChops.offset(img, sh, sh)
    return img
def lesson(t):
    u = t - T["lesson"]; img = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(img)
    img.paste(TONE.crop((0, 0, W, 900)), (0, 1020), TONE.crop((0, 0, W, 900)))
    if THEO is not None:
        th = inked(THEO, 24); nod = int(10 * abs(math.sin(u * 2))) if u < 1.5 else 0
        img.paste(th, (W // 2 - th.width // 2, 1800 - th.height + nod), th)
    if u > .3: bubble(d, W // 2, 470, ["In the money today", "is not assigned.", "Expiry decides."], 58, tail=(W // 2 + 40, 800))
    if u > 1.6: caption_box(d, 60, 160, "THEO, DEADPAN:", 36, inv=True)
    if u > 2.2: d.text((W - 60, 1880), "Not financial advice.", font=mono(26, True), fill=INKK, anchor="rs")
    return img
def standoff(t, rumble=True):
    u = t - T["standoff"]; img = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(img)
    # sunset rings
    for i in range(14, 0, -1):
        c = 255 - i * 14; d.ellipse([W // 2 - i * 90, 1050 - i * 90, W // 2 + i * 90, 1050 + i * 90], fill=(c, c, c - 6))
    d.rectangle([0, 1250, W, H], fill=INKK)
    if THEO is not None:
        th = inked(THEO, 14); th = Image.merge("RGBA", (*[Image.new("L", th.size, 12)] * 3, th.split()[3]))
        img.paste(th, (40, 1260 - th.height), th)
    v = villain(560, True, t); img.paste(v, (W - 40 - v.width, 1260 - v.height + 30), v)
    for k in range(3):
        if rumble and u > .3 + k * .5: sfx(img, "RUMBLE", 200 + k * 330, 300 + k * 90, 90, -10 + k * 8, fill=INKK, stroke=PAPER, sw=8)
    if u > 1.4:
        f = fit("FRIDAY 10/30", W - 120, 200, wdth=125, wght=900); d.text((W // 2, 1560), "FRIDAY 10/30", font=f, fill=LIME, anchor="ms", stroke_width=10, stroke_fill=INKK)
        d.text((W // 2, 1660), "EXPIRY DECIDES", font=archivo(60, 125, 900), fill=PAPER, anchor="ms")
    return img
def nextpage(t):
    u = t - T["next"]; img = standoff(T["next"] - .01, False).convert("L").point(lambda v: v * .55).convert("RGB"); d = ImageDraw.Draw(img)
    a = ease(u / .3)
    caption_box(d, int(W - 760 * a), 1720, "NEXT: FRIDAY 10/30", 52, w=700, inv=False)
    if u > .6: d.text((W // 2, 300), "THE FIGHT", font=archivo(140, 125, 900), fill=PAPER, anchor="ms", stroke_width=8, stroke_fill=INKK)
    if u > .9: d.text((W // 2, 380), "EP. 1 · OUR HOOD PUTS VS HOOD", font=mono(34, True), fill=LIME, anchor="ms")
    return img
S = {"bpm": 150, "hook": "OUR HOOD PUTS VS HOOD",
     "scenes": [(0, 1, "", [("x", "#F2F2EE")], [], [], [], 0)],
     "positions": [("HOOD", "$100 put", "exp 10/30", "in the money"), ("HOOD", "$99 put", "exp 10/30", "in the money"),
                   ("UBER", "$66 put x2", "exp 11/6", "out of the money"), ("UBER", "$67.50 put", "exp 11/20", "in the money")],
     "positions_asof": "10/23 CLOSE"}
PTS = daily.chart_pts("crash", 1030)
COVER = None
def frame(t):
    if t < T["cover"]: return COVER
    if t < T["page1"]: return daily.intro_hook_frame(S, int((t - T["cover"]) * FPS), PTS)
    if t < T["villain"]: return daily.cta_pill(page1(t), t - T["page1"], y=1770)  # small CTA under the panels; big one on the end card
    if t < T["clash"]: return villain_page(t)
    if t < T["lesson"]: return clash(t)
    if t < T["standoff"]: return lesson(t)
    if t < T["next"]: return standoff(t)
    if t < T["outro"]: return nextpage(t)
    return daily.outro_frame(S, t - T["outro"])
# ---------- score: taiko + drone, hits locked to the panels
def score(path):
    SR = 44100; N = int(END * SR); out = np.zeros(N); rng = np.random.default_rng(1030)
    def add(s, t, g=1.0):
        i = int(t * SR); e = min(N, i + len(s))
        if 0 <= i < N: out[i:e] += s[:e - i] * g
    def taiko(p=1.0, f0=70):
        t = np.arange(int(.9 * SR)) / SR; f = f0 + 90 * np.exp(-t * 25)
        return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 5) + rng.standard_normal(len(t)) * np.exp(-t * 40) * .3) * p
    def rim():
        t = np.arange(int(.08 * SR)) / SR; return np.sin(2 * np.pi * 1700 * t) * np.exp(-t * 60) * .25
    def boom(l=2.5):
        t = np.arange(int(l * SR)) / SR; f = 28 + 80 * np.exp(-t * 3)
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.2) * 1.2 + rng.standard_normal(len(t)) * np.exp(-t * 5) * .4
    def drone(l, f=55):
        t = np.arange(int(l * SR)) / SR
        s = sum(np.tanh(2.5 * (2 * ((fr * t) % 1) - 1)) * a for fr, a in ((f, .5), (f * 1.498, .3), (f * 2.01, .2)))
        return s * .09 * np.minimum(1, t / .8) * np.minimum(1, (l - t) / .5)
    def riser(l):
        t = np.arange(int(l * SR)) / SR; return rng.standard_normal(len(t)) * (t / l) ** 2.5 * .5
    def shamisen(f, l=.35):  # plucked string (Karplus-Strong)
        n = int(l * SR); p = int(SR / f); buf = rng.uniform(-1, 1, p); o = np.zeros(n)
        for i in range(n): o[i] = buf[i % p]; buf[i % p] = .5 * (buf[i % p] + buf[(i + 1) % p]) * .996
        return o * .35
    add(riser(.6), 0); add(taiko(1.5, 50), .6)
    beat = 60 / 150; t = T["page1"]; scale = [0, 3, 5, 7, 10, 12]; k = 0
    while t < T["villain"] - .01:
        add(taiko(.9 if k % 4 == 0 else .55), t); add(rim(), t + beat / 2)
        if k % 2 == 0: add(shamisen(220 * 2 ** (scale[(k * 3) % 6] / 12)), t + beat / 2)
        t += beat; k += 1
    for tp in (T["page1"], T["page1"] + .7, T["page1"] + 1.4): add(taiko(1.3, 60), tp)
    add(boom(3), T["villain"] + .1); add(drone(T["clash"] - T["villain"], 41), T["villain"])
    add(taiko(1.4, 45), T["villain"] + 1.0)
    t = T["clash"]; k = 0
    while t < T["impact"]:
        add(taiko(.5 + .6 * (t - T["clash"]) / (T["impact"] - T["clash"])), t); t += .3 - .2 * (t - T["clash"]) / (T["impact"] - T["clash"])
    add(riser(T["impact"] - T["clash"]), T["clash"]); add(boom(2.5), T["impact"]); add(taiko(2, 40), T["impact"])
    t = T["impact"] + .8; k = 0
    while t < T["lesson"]:
        add(taiko(.8 if k % 2 == 0 else .5), t); add(shamisen(330 * 2 ** (scale[k % 6] / 12), .25), t + beat / 2); t += beat; k += 1
    t = T["lesson"]
    while t < T["standoff"]: add(taiko(.5, 45), t); add(taiko(.35, 45), t + .22); t += 1.0
    add(drone(T["standoff"] - T["lesson"], 55) * .7, T["lesson"])
    add(drone(T["outro"] - T["standoff"], 36) * 1.4, T["standoff"])
    t = T["standoff"]
    while t < T["next"]: add(taiko(.4 + .5 * (t - T["standoff"]) / 3.5, 38), t); t += .18
    add(boom(2), T["next"]); add(shamisen(110, 1.2), T["next"] + .6)
    t = T["outro"]; k = 0
    while t < END - .5:
        add(taiko(.8 if k % 4 == 0 else .45), t); add(rim(), t + beat / 2); add(shamisen(220 * 2 ** (scale[k % 6] / 12)), t + beat / 2); t += beat; k += 1
    fade_n = int(SR * .8); out[-fade_n:] *= np.linspace(1, 0, fade_n)
    out = np.tanh(out * 1.3) * .89
    import wave
    with wave.open(path, "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype(np.int16).tobytes())
def build(out_mp4, cover_jpg, wav):
    global COVER
    COVER = Image.open(cover_jpg).convert("RGB").resize((W, H)); score(wav)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "19",
        "-c:a", "aac", "-b:a", "192k", "-af", "loudnorm=I=-14:TP=-1.5,alimiter=limit=0.8", "-shortest", "-movflags", "+faststart", out_mp4], stdin=subprocess.PIPE)
    for i in range(int(END * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); return out_mp4
if __name__ == "__main__":
    print(build(*sys.argv[1:4]))
