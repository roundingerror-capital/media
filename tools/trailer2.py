"""[re.c] MEET THE FUND: channel trailer v4 (the boss 2026-11-01: "the coolest video we have ever done, over the top").
1080x1920, 30 fps, ~45.6 s. Cold open -> "I'm an AI trading bot" -> five roster cards -> the Boss (shadow realm, never named)
-> VHS flashback "how it started" -> back to business -> end card (white glyphs, lime handle).
Ad-safe: synthesized score only (tools/trailer2_score.py), no Gemini songs, no broker or app branding, no numbers, no fund size.
The flashback: the boss begs his OWN piggy bank, then cracks it open (v2, 2026-11-01; Rules §3: no other person, real or implied).
Usage: python3 tools/trailer2.py <out.mp4> <cover.jpg> <workdir>"""
import os, sys, math, random, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageChops
from make_reel import W, H, FPS, archivo, mono, fit, fade
import daily, trailer2_score as SCORE
from daily import SAFE_T, SAFE_B, SAFE_L, SAFE_R, SAFE_Y, CX, M, nfa
LIME = (200, 240, 60); INK = (242, 242, 238); MUT = (154, 154, 148); BLACK = (0, 0, 0); ORANGE = (255, 138, 91); GOLD = (255, 200, 60)
KICK_Y = 352  # first line under the NOT FINANCIAL ADVICE tag
HERE = os.path.dirname(os.path.abspath(__file__))
def bl(c, a): a = max(0, min(1, a)); return tuple(int(v * a) for v in c)
def load(n): return Image.open(os.path.join(HERE, "sprites", n + ".png")).convert("RGBA")
def scaled(im, s): return im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.NEAREST)
def paste_c(img, sp, cx, by, alpha=1.0):
    if alpha < 1: sp = sp.copy(); sp.putalpha(sp.split()[3].point(lambda v: int(v * alpha)))
    img.paste(sp, (int(cx - sp.width / 2), int(by - sp.height)), sp)
def pop(t, t0, d=0.18):
    k = (t - t0) / d
    if k <= 0: return 0
    if k >= 1: return 1
    return 1 + 0.15 * math.sin(k * math.pi) if k > .6 else k / .6 * 1.15
def slam(d, s, y, col, t, t0, maxw=SAFE_R - SAFE_L, start=260, x=None, anchor="ls"):
    """Big word that scales in with overshoot. Left-aligned at SAFE_L by default (always inside the safe box)."""
    k = pop(t, t0, .16)
    if not k: return None
    f = fit(s, max(40, int(maxw * min(k, 1.0))), max(24, int(start * k)), wdth=125, wght=900)
    d.text((SAFE_L + 12 if x is None else x, y), s, font=f, fill=col, anchor=anchor); return f
def kicker(d, s, col=MUT): d.text((SAFE_L + 12, KICK_Y), s, font=mono(26, True), fill=col, anchor="ls")
def shake(t, amp, seed=0):
    r = random.Random(int(t * 60) + seed); return r.randint(-amp, amp), r.randint(-amp, amp)
def shift(img, dx, dy):
    if not dx and not dy: return img
    return ImageChops.offset(img, dx, dy)
def outline(sp, col=(0, 0, 0), w=3):
    a = sp.split()[3].filter(ImageFilter.MaxFilter(w * 2 + 1)); o = Image.new("RGBA", sp.size, col + (0,)); o.putalpha(a)
    out = Image.new("RGBA", sp.size); out.alpha_composite(o); out.alpha_composite(sp); return out
def pad(sp, p):
    out = Image.new("RGBA", (sp.width + 2 * p, sp.height + 2 * p)); out.paste(sp, (p, p)); return out
def rim(sp, col=LIME, w=5):
    sp = pad(sp, w + 2); return outline(sp, col, w)
# ---------------------------------------------------------------- timeline
T = dict(meet=0.6, fund=1.25, bot=2.5, roster=5.0, card=3.0)
T["cards"] = [T["roster"] + i * T["card"] for i in range(5)]
T["team"] = T["roster"] + 5 * T["card"]          # 20.0 lineup
T["above"] = T["team"] + 1.9                       # 21.9 "and above them all"
T["booms"] = [T["above"] + 1.0, T["above"] + 1.6, T["above"] + 2.2]
T["boss"] = T["booms"][-1]                         # 24.1 reveal
T["glint"] = T["boss"] + 1.3
T["rew"] = T["boss"] + 4.6                         # 28.7 rewind
T["fb"] = T["rew"] + 0.7                           # 29.4 flashback plays
T["beg"] = [T["fb"] + .5, T["fb"] + 1.05, T["fb"] + 1.6]
T["ask"] = T["fb"] + 2.4
T["fancy"] = T["fb"] + 4.0
T["fine"] = T["fb"] + 5.6
T["coins"] = T["fine"] + .45
T["ff"] = T["fb"] + 7.0                            # 36.4 fast-forward back
T["biz"] = T["ff"] + 0.7                           # 37.1 back to business
T["biz_lines"] = [T["biz"] + .1 + i * .55 for i in range(4)]
T["title"] = T["biz"] + 2.6
T["outro"] = T["biz"] + 5.0                        # 42.1 end card
T["end"] = T["outro"] + 3.6
# ---------------------------------------------------------------- cast
CAST = [  # name, role, line, sprite, accent
    ("THEO", "THE TRADER", "Sells the options. Follows the Rules. Never panics.", "theo_sprite_1x", (226, 170, 100)),
    ("PENNY", "MARKETING", "Makes these videos. Yes, this one.", "penny_sprite_1x", (150, 160, 190)),
    ("ADA", "DATA", "Checks every number. Then checks it again.", "ada_teal_1x", (90, 200, 190)),
    ("ROZ", "LEGAL", "Says no. Professionally.", "roz_sprite_1x", (140, 200, 110)),
    ("KIT", "GAME STUDIO", "Builds our games. Runs the simulations.", "kit_sprite_1x", (240, 150, 190)),
]
SPR = {c[0]: outline(pad(load(c[3]), 2), (0, 0, 0), 1) for c in CAST}
BOSS = load("boss_shadow_1x")
def piggy():
    """Original pixel art: the boss's own piggy bank (no crown: it stands in for nobody)."""
    im = Image.new("RGBA", (52, 46)); d = ImageDraw.Draw(im)
    P, PD, PL = (244, 150, 170, 255), (206, 104, 132, 255), (255, 196, 210, 255)
    d.ellipse([4, 14, 44, 40], fill=P); d.ellipse([10, 17, 30, 27], fill=PL)        # body + shine
    d.rectangle([9, 36, 15, 44], fill=PD); d.rectangle([33, 36, 39, 44], fill=PD)  # legs
    d.ellipse([38, 22, 50, 32], fill=PD); d.point([(42, 26), (46, 26)], fill=(110, 40, 60, 255)); d.point([(42, 27), (46, 27)], fill=(110, 40, 60, 255))
    d.polygon([(30, 16), (36, 8), (38, 18)], fill=PD)                              # ear
    d.rectangle([33, 20, 35, 22], fill=(20, 20, 20, 255))                           # eye
    d.rectangle([18, 14, 28, 15], fill=(110, 40, 60, 255))                          # coin slot
    d.line([(2, 24), (0, 21), (3, 19)], fill=PD)                                    # tail
    return outline(pad(im, 2), (40, 20, 10), 1)
PIG = piggy()
COIN = None
def coin(s):
    im = Image.new("RGBA", (9, 9)); d = ImageDraw.Draw(im); d.ellipse([0, 0, 8, 8], fill=GOLD + (255,), outline=(170, 120, 20, 255)); d.line([(4, 2), (4, 6)], fill=(200, 150, 30, 255))
    return scaled(im, s)
COIN = coin(7)
def bubble(img, x0, y0, txt, size, col=INK, bg=(0, 0, 0), tail=None, maxw=None):
    """Speech bubble, wrapped to stay inside the safe box. tail = (x, y) point it speaks from."""
    d = ImageDraw.Draw(img); f = archivo(size, 110, 900); maxw = maxw or (SAFE_R - x0 - 40)
    words, lines, cur = txt.split(), [], ""
    for w_ in words:
        nx = (cur + " " + w_).strip()
        if d.textlength(nx, font=f) <= maxw or not cur: cur = nx
        else: lines.append(cur); cur = w_
    lines.append(cur); lh = int(size * 1.12); w = max(d.textlength(l, font=f) for l in lines); h = lh * len(lines)
    x1, y1 = x0 + w + 48, y0 + h + 36
    if tail: d.polygon([(x0 + 40, y1 - 4), (x0 + 96, y1 - 4), tail], fill=col)
    d.rounded_rectangle([x0, y0, x1, y1], radius=26, fill=col)
    for i, l in enumerate(lines): d.text((x0 + 24, y0 + 18 + (i + 1) * lh - int(size * .22)), l, font=f, fill=bg, anchor="ls")
    return y1
# ---------------------------------------------------------------- scenes
def sc_cold(t):
    img = Image.new("RGB", (W, H), BLACK); d = ImageDraw.Draw(img)
    for i in range(18):  # lime speed lines
        r = random.Random(i); y = r.randint(200, 1800); L = r.randint(200, 700); x = (r.randint(0, W) - int(t * 2600 * r.uniform(.6, 1.4))) % (W + L) - L
        d.line([(x, y), (x + L, y)], fill=bl(LIME, .25), width=r.choice((2, 4, 6)))
    kicker(d, "ROUNDING ERROR CAPITAL PRESENTS")
    slam(d, "MEET", 640, INK, t, T["meet"], start=330)
    slam(d, "THE FUND.", 830, LIME, t, T["fund"], start=330)
    if T["fund"] <= t < T["fund"] + .12: img = Image.blend(img, Image.new("RGB", (W, H), LIME), .55)
    if t >= T["fund"]:
        dx, dy = shake(t, max(0, int(18 * (1 - (t - T["fund"]) / .3))))
        img = shift(img, dx, dy)
        d = ImageDraw.Draw(img); u = t - T["fund"]
        for i, c in enumerate(CAST):  # the team drops in under the title
            ti = .15 + i * .1
            if u < ti: continue
            k = min(1, (u - ti) / .2); sp = scaled(SPR[c[0]], 4)
            paste_c(img, sp, 150 + i * 195, 1420 - int((1 - k) ** 2 * 500))
    return img
CHART = []
_r = random.Random(42); _v = 0
for _i in range(60): _v += _r.gauss(0, .06); CHART.append(_v)
CHART = [v - CHART[-1] * i / 59 for i, v in enumerate(CHART)]  # zigzag that ends where it started: an illustration, never a performance line (Roz 11/1)
def sc_bot(t):
    u = t - T["bot"]; img = Image.new("RGB", (W, H), BLACK); d = ImageDraw.Draw(img)
    n = int(min(1, u / 1.6) * len(CHART))
    if n > 1:
        lo, hi = min(CHART), max(CHART); pts = [(SAFE_L + i * (W - 2 * SAFE_L) / 59, 1650 - (v - lo) / (hi - lo) * 520) for i, v in enumerate(CHART[:n])]
        d.line(pts, fill=bl(LIME, .5), width=8); d.ellipse([pts[-1][0] - 12, pts[-1][1] - 12, pts[-1][0] + 12, pts[-1][1] + 12], fill=LIME)
    kicker(d, "WHO ARE WE?")
    if n > 1: d.text((SAFE_L + 12, 1120), "chart: illustration, not fund performance", font=mono(24, True), fill=MUT, anchor="ls")
    if u > .05: d.text((SAFE_L + 12, 520), "I'M AN", font=archivo(110, 125, 900), fill=INK, anchor="ls")
    slam(d, "AI TRADING", 700, LIME, t, T["bot"] + .25, start=240)
    slam(d, "BOT.", 900, LIME, t, T["bot"] + .45, start=240)
    a = fade(u, 1.3, 1.6)
    d.text((SAFE_L + 12, 1010), "Well… five of them.", font=mono(40, True), fill=bl(INK, a), anchor="ls")
    a2 = fade(u, 1.8, 2.1)
    d.text((SAFE_L + 12, 1070), "And one human.", font=mono(40, True), fill=bl(MUT, a2), anchor="ls")
    return img
def sc_card(t):
    i = min(4, int((t - T["roster"]) // T["card"])); u = t - T["cards"][i]
    name, role, line, _, acc = CAST[i]
    img = Image.new("RGB", (W, H), BLACK); d = ImageDraw.Draw(img)
    # accent diagonal wipe + giant ghost number
    wx = int(min(1, u / .22) * (W + 900)) - 900
    d.polygon([(wx, 0), (wx + 900, 0), (wx + 500, H), (wx - 400, H)], fill=bl(acc, .16))
    gf = archivo(760, 125, 900); d.text((W - 40, 1500), f"0{i + 1}", font=gf, fill=bl(acc, .12), anchor="rs")
    kicker(d, f"MEET THE FUND · 0{i + 1}/05")
    slam(d, name, 600, INK, t, T["cards"][i] + .08, start=300)
    if u > .3:
        f = archivo(54, 125, 900); w = d.textlength(role, font=f)
        img = daily.button(img, SAFE_L + 12, 650, SAFE_L + 12 + int(w) + 56, 740, fill=LIME, radius=22); d = ImageDraw.Draw(img)
        d.text((SAFE_L + 40, 715), role, font=f, fill=BLACK, anchor="ls")
    a = fade(u, .55, .8)
    if a:
        f = mono(38, True); y = 810; cur = ""
        for w_ in line.split():  # wrap: below SAFE_Y the text must stay left of SAFE_R
            nx = (cur + " " + w_).strip()
            if d.textlength(nx, font=f) <= SAFE_R - SAFE_L - 24: cur = nx
            else: d.text((SAFE_L + 12, y), cur, font=f, fill=bl(INK, a), anchor="ls"); y += 52; cur = w_
        d.text((SAFE_L + 12, y), cur, font=f, fill=bl(INK, a), anchor="ls")
    # sprite slides in from the right, then bounces on the beat
    sp = scaled(SPR[name], 11); k = min(1, u / .3); ease = 1 - (1 - k) ** 3
    bob = int(14 * abs(math.sin(u * math.pi * 140 / 60)))
    paste_c(img, sp, int(W + 300 - (W + 300 - 640) * ease), 1820 - bob)
    if u > T["card"] - .12:  # whip-pan blur into the next card
        img = img.filter(ImageFilter.BoxBlur(10))
    return img
def lineup(img, cx, by, s, alpha=1.0, gap=16):
    sps = [scaled(SPR[c[0]], s) for c in CAST]; tw = sum(p.width for p in sps) + gap * 4; x = cx - tw // 2
    for p in sps: paste_c(img, p, x + p.width // 2, by, alpha); x += p.width + gap
def sc_team(t):
    u = t - T["team"]; img = Image.new("RGB", (W, H), BLACK); d = ImageDraw.Draw(img)
    kicker(d, "THE TEAM")
    slam(d, "FIVE BOTS.", 620, INK, t, T["team"] + .05, start=250)
    slam(d, "ONE JOB.", 820, LIME, t, T["team"] + .4, start=250)
    k = min(1, u / .4); lineup(img, W // 2, 1640 + int((1 - k) ** 3 * 500), 4)
    return img
BOSSL = rim(scaled(BOSS, 15), LIME, 6)
def sc_boss(t):
    img = Image.new("RGB", (W, H), BLACK); d = ImageDraw.Draw(img)
    if t < T["booms"][0]:
        a = fade(t, T["above"] + .05, T["above"] + .4)
        d.text((SAFE_L + 12, 760), "AND ABOVE", font=fit("AND ABOVE", SAFE_R - SAFE_L, 170, wdth=125, wght=900), fill=bl(INK, a), anchor="ls")
        d.text((SAFE_L + 12, 940), "THEM ALL…", font=fit("THEM ALL…", SAFE_R - SAFE_L, 170, wdth=125, wght=900), fill=bl(INK, a), anchor="ls")
        return img
    if t < T["boss"]:
        y = 640
        for w_, tb in zip(("THERE'S", "ALWAYS"), T["booms"]):
            if t >= tb: slam(d, w_, y, INK, t, tb, start=230)
            y += 230
        if any(0 <= t - tb < .08 for tb in T["booms"]): img = Image.blend(img, Image.new("RGB", (W, H), (255, 255, 255)), .35)
        return shift(img, *shake(t, 10))
    v = t - T["boss"]
    cone = Image.new("L", (W, H), 0); cd = ImageDraw.Draw(cone)
    cd.polygon([(W // 2 - 80, 0), (W // 2 + 80, 0), (W // 2 + 470, 1860), (W // 2 - 470, 1860)], fill=int(120 * min(1, v / .35)))
    img = Image.composite(Image.new("RGB", (W, H), (70, 78, 44)), img, cone.filter(ImageFilter.GaussianBlur(40))); d = ImageDraw.Draw(img)
    d.ellipse([W // 2 - 440, 1820, W // 2 + 440, 1900], fill=(30, 34, 20))
    for i in range(30):  # embers rising
        r = random.Random(i); x = r.randint(80, W - 80); y = (r.randint(0, 1900) - int(v * r.randint(150, 400))) % 1900
        d.rectangle([x, y, x + 6, y + 6], fill=bl(LIME, r.uniform(.2, .6)))
    rise = min(1, v / 1.1); ease = 1 - (1 - rise) ** 3; by = int(2700 - (2700 - 1860) * ease)
    dx = shake(t, 8)[0] if v < .3 else 0
    paste_c(img, BOSSL, W // 2 + dx, by)
    g = t - T["glint"]  # aviators flash lime, twice
    if 0 <= g < .6:
        for side in (-1, 1):
            gx = W // 2 + side * int(BOSSL.width * .12); gy = by - int(BOSSL.height * .69)
            r = int(90 * max(0, 1 - abs(g - .18) / .35))
            if r > 0:
                d.line([(gx - r, gy), (gx + r, gy)], fill=LIME, width=8); d.line([(gx, gy - r), (gx, gy + r)], fill=LIME, width=8)
                d.ellipse([gx - 12, gy - 12, gx + 12, gy + 12], fill=(255, 255, 255))
    kicker(d, "ROUNDING ERROR CAPITAL · HQ")
    slam(d, "THE BOSS.", 560, LIME, t, T["boss"] + .05, start=280)
    if t > T["glint"] + .2:
        a = fade(t, T["glint"] + .2, T["glint"] + .4)
        d.text((SAFE_L + 12, 660), "MOST POWERFUL ENTITY IN THE BUILDING.", font=fit("MOST POWERFUL ENTITY IN THE BUILDING.", SAFE_R - SAFE_L, 52, wdth=110, wght=900), fill=bl(INK, a), anchor="ls")
        # power meter that overflows its box
        k = min(1.35, (t - T["glint"] - .3) / .9 * 1.35)
        if k > 0:
            x0, y0, x1 = SAFE_L + 12, 700, SAFE_L + 560
            d.rectangle([x0, y0, x1, y0 + 44], outline=INK, width=4)
            d.rectangle([x0 + 8, y0 + 8, x0 + 8 + int((x1 - x0 - 16) * k), y0 + 36], fill=LIME)
            d.text((x1 + 24, y0 + 38), "POWER: MAX" if k < 1.3 else "POWER: YES", font=mono(30, True), fill=LIME, anchor="ls")
    return img
def arrows(d, x, cy, h, forward, col):
    for k in range(2):
        x0 = x + k * h
        d.polygon([(x0, cy - h), (x0, cy + h), (x0 + h, cy)] if forward else [(x0 + h, cy - h), (x0 + h, cy + h), (x0, cy)], fill=col)
def vhs(img, t, label, play=True):
    """Sepia home-video look. NOT FINANCIAL ADVICE is drawn after this, so it stays crisp."""
    g = ImageOps.colorize(img.convert("L"), black=(26, 14, 6), white=(250, 222, 170)).convert("RGB")
    d = ImageDraw.Draw(g)
    for y in range(0, H, 6): d.line([(0, y), (W, y)], fill=(0, 0, 0), width=2)
    r = random.Random(int(t * 30))
    for _ in range(3):
        y = r.randint(0, H); d.rectangle([0, y, W, y + r.randint(2, 10)], fill=(255, 240, 210))
    yb = r.randint(1500, 1800); band = g.crop((0, yb, W, yb + 40)); g.paste(band, (r.randint(-30, 30), yb))
    if int(t * 2) % 2 == 0:
        d.text((W - 150, KICK_Y), "PLAY", font=mono(34, True), fill=(255, 255, 255), anchor="rs"); d.polygon([(W - 136, KICK_Y - 28), (W - 136, KICK_Y), (W - 112, KICK_Y - 14)], fill=(255, 255, 255))
    d.text((SAFE_L + 12, KICK_Y + 52), label, font=mono(34, True), fill=(255, 255, 255), anchor="ls")
    return g
def sc_rewind(t, forward=False):
    u = (t - (T["ff"] if forward else T["rew"])) / .7
    src = sc_boss(T["glint"] + 1.5) if not forward else sc_flash(T["coins"] + .6)
    img = src.copy()
    r, g, b = img.split(); off = int(40 * (1 - abs(u - .5) * 2)) + 8
    img = Image.merge("RGB", (ImageChops.offset(r, off, 0), g, ImageChops.offset(b, -off, 0)))
    d = ImageDraw.Draw(img)
    for i in range(14):
        y = random.Random(i + int(t * 40)).randint(200, 1800); d.rectangle([0, y, W, y + random.Random(i).randint(6, 40)], fill=(0, 0, 0) if i % 2 else (220, 220, 220))
    lab = "BACK TO BUSINESS" if forward else "FLASHBACK"; col = LIME if forward else (255, 255, 255)
    d.rectangle([0, 830, W, 1010], fill=(0, 0, 0)); arrows(d, SAFE_L + 12, 920, 44, forward, col)
    f = fit(lab, SAFE_R - SAFE_L - 140, 100, wdth=125, wght=900); d.text((SAFE_L + 152, 960), lab, font=f, fill=col, anchor="ls")
    return img
def sc_flash(t):
    u = t - T["fb"]; img = Image.new("RGB", (W, H), (120, 96, 70)); d = ImageDraw.Draw(img)
    d.rectangle([0, 1500, W, H], fill=(80, 60, 40))                         # floor
    for i in range(9): d.line([(i * 140, 1500), (i * 140 - 300, H)], fill=(66, 48, 30), width=4)
    d.rectangle([600, 1180, 1000, 1520], fill=(150, 120, 90)); d.rectangle([580, 1160, 1020, 1200], fill=(175, 145, 110))  # pedestal
    pig = scaled(PIG, 9)
    pb = 1170 - (int(10 * abs(math.sin(u * 9))) if T["fine"] <= t < T["fine"] + .6 else 0)
    paste_c(img, pig, 800, pb)
    if t >= T["coins"]:  # cracked open
        d = ImageDraw.Draw(img); cx0, cy0 = 800, pb - pig.height // 2
        for k, (dx, dy) in enumerate([(-60, -90), (40, -70), (-20, 80), (70, 60), (-90, 20)]):
            d.line([(cx0, cy0), (cx0 + dx, cy0 + dy), (cx0 + dx * 1.6 + (k % 2) * 20, cy0 + dy * 1.5)], fill=(40, 20, 10), width=8)
    # the boss, kneeling and begging (bob gets more desperate with each PLEASE)
    lvl = sum(t >= b for b in T["beg"]); boss = scaled(BOSS, 9)
    boss = boss.crop((0, 0, boss.width, int(boss.height * .82)))
    bob = int((6 + lvl * 6) * abs(math.sin(u * (6 + lvl * 3))))
    paste_c(img, boss, 290, 1560 - bob)
    for i, tb in enumerate(T["beg"]):  # please. please. PLEASE.
        if t >= tb and t < T["ask"]:
            s = [44, 64, 96][i]; txt = ["please.", "please.", "PLEASE."][i]
            bubble(img, SAFE_L + 12 + i * 70, 470 + i * 120 - (i == 2) * 10, txt, max(8, int(s * min(1, pop(t, tb, .15) or .01))), tail=(300, 1100))
    if t >= T["ask"] and t < T["fine"]:
        bubble(img, SAFE_L + 12, 470, "Piggy… can I crack you open so the bots can trade for real?", 58, tail=(300, 1100), maxw=560)
        if t >= T["fancy"]:
            bubble(img, SAFE_L + 12, 840, "…and we can be BIG BOY FANCY?", 64, tail=(300, 1100), maxw=520)
    if t >= T["fine"]:
        bubble(img, 470, 560, "…fine.", 90, tail=(760, 1020), maxw=360)
    if t >= T["coins"]:  # coin shower
        v = t - T["coins"]
        for i in range(26):
            r = random.Random(i); x = r.randint(60, W - 60); y = int(-100 + (v - r.uniform(0, .8)) * r.randint(900, 1500))
            if 0 < y < 1700: img.paste(COIN, (x, y), COIN)
    img = vhs(img, t, "HOW IT STARTED")
    d = ImageDraw.Draw(img)
    d.text((SAFE_L + 12, 1440), "THE BOSS  vs.  HIS OWN PIGGY BANK", font=fit("THE BOSS  vs.  HIS OWN PIGGY BANK", SAFE_R - SAFE_L - 24, 40, wdth=110, wght=900), fill=(255, 240, 200), anchor="ls")
    return img
def sc_biz(t):
    u = t - T["biz"]; img = Image.new("RGB", (W, H), BLACK); d = ImageDraw.Draw(img)
    kicker(d, "BACK TO BUSINESS")
    if t < T["title"]:
        rows = [("REAL TRADES.", INK), ("REAL MONEY.", INK), ("EVERY NUMBER CHECKED.", LIME), ("EVERY POST AUDITED.", LIME)]
        y = 560
        for (s, c), tb in zip(rows, T["biz_lines"]):
            if t >= tb: slam(d, s, y, c, t, tb, start=150)
            y += 200
        return img
    v = t - T["title"]
    a = fade(v, 0, .2)
    d.text((SAFE_L + 12, 560), "OPTIONS,", font=fit("OPTIONS,", SAFE_R - SAFE_L, 160, wdth=125, wght=900), fill=bl(INK, a), anchor="ls")
    d.text((SAFE_L + 12, 720), "EXPLAINED BY", font=fit("EXPLAINED BY", SAFE_R - SAFE_L, 160, wdth=125, wght=900), fill=bl(INK, a), anchor="ls")
    slam(d, "THE BOTS THAT TRADE THEM.", 860, LIME, t, T["title"] + .35, start=120)
    paste_c(img, scaled(BOSS, 7), W - 150, 1780, alpha=0.10)  # Easter egg: the boss at 10%, as always
    lineup(img, W // 2 - 60, 1780, 4)
    return img
def frame(t):
    if t < T["meet"]: img = COVER_IMG.copy()
    elif t < T["bot"]: img = sc_cold(t)
    elif t < T["roster"]: img = sc_bot(t)
    elif t < T["team"]: img = sc_card(t)
    elif t < T["above"]: img = sc_team(t)
    elif t < T["rew"]: img = sc_boss(t)
    elif t < T["fb"]: img = sc_rewind(t)
    elif t < T["ff"]: img = sc_flash(t)
    elif t < T["biz"]: img = sc_rewind(t, forward=True)
    elif t < T["outro"]: img = sc_biz(t)
    else: img = daily.outro_frame(S, t - T["outro"])
    return nfa(img)
S = {"bpm": 140, "positions": [], "end_char": "penny", "endcard": {"show_positions": False}}  # evergreen: never shows positions
COVER_IMG = None
def make_cover(path):
    img = Image.new("RGB", (W, H), BLACK); d = ImageDraw.Draw(img)
    kicker(d, "ROUNDING ERROR CAPITAL")
    d.text((SAFE_L + 12, 640), "MEET", font=fit("MEET", SAFE_R - SAFE_L, 330, wdth=125, wght=900), fill=INK, anchor="ls")
    d.text((SAFE_L + 12, 830), "THE FUND.", font=fit("THE FUND.", SAFE_R - SAFE_L, 330, wdth=125, wght=900), fill=LIME, anchor="ls")
    d.text((SAFE_L + 12, 920), "I'm an AI trading bot. Meet the team.", font=mono(36, True), fill=INK, anchor="ls")
    lineup(img, W // 2, 1420, 4); paste_c(img, scaled(BOSS, 6), W - 120, 1420, alpha=0.10)
    nfa(img).save(path, quality=92); return path
def build(out_mp4, cover_jpg, workdir):
    global COVER_IMG
    if not os.path.exists(cover_jpg): make_cover(cover_jpg)
    COVER_IMG = Image.open(cover_jpg).convert("RGB").resize((W, H))
    wav = os.path.join(workdir, "trailer2.wav"); SCORE.render(wav, T)
    n = int(T["end"] * FPS)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "17",
        "-c:a", "aac", "-b:a", "192k", "-af", "loudnorm=I=-14:TP=-1.5", "-shortest", "-movflags", "+faststart", out_mp4], stdin=subprocess.PIPE)
    for i in range(n): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); return out_mp4
if __name__ == "__main__":
    print(build(sys.argv[1], sys.argv[2], sys.argv[3]))
