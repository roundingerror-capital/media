"""[re.c] MEET THE FUND: channel trailer v4 (the boss 2026-11-01: "the coolest video we have ever done, over the top").
1080x1920, 30 fps, ~45.6 s. Cold open -> "I'm an AI trading bot" -> five roster cards -> the Boss (shadow realm, never named)
-> VHS flashback "how it started" -> back to business -> end card (white glyphs, lime handle).
Ad-safe: synthesized score only (tools/trailer2_score.py), no Gemini songs, no broker or app branding, no numbers, no fund size.
v3 (the boss 2026-11-01): THE BOSS IS #1 -> "yet there is always one above" -> THE REAL BOSS (a shadow fawn, never named or labeled) breaks the power bar -> flashback back-and-forth.
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
T = dict(meet=0.6, fund=1.25, bot=2.5, roster=5.4, card=3.6)
T["cards"] = [T["roster"] + i * T["card"] for i in range(5)]
T["team"] = T["roster"] + 5 * T["card"]          # 20.0 lineup
T["above"] = T["team"] + 1.9                       # 21.9 "and above them all"
T["booms"] = [T["above"] + 1.0, T["above"] + 1.6, T["above"] + 2.2]
T["boss"] = T["booms"][-1]                         # 24.1 reveal
T["glint"] = T["boss"] + 1.3
T["no1"] = T["boss"] + 3.2                         # 27.3 "THE BOSS IS #1."
T["yet"] = T["no1"] + 1.5                          # 28.8 "YET... THERE IS ALWAYS ONE ABOVE."
T["rank"] = T["yet"] + 2.4                         # 31.2 power rankings: a new #1 appears
T["slide"] = T["rank"] + .45                       # new row drops in, the boss moves to #2
T["fill"] = T["rank"] + 1.0                        # her bar starts filling
T["crack"] = T["rank"] + 2.1                       # the bar cracks
T["shatter"] = T["rank"] + 2.45                    # ...and breaks
T["rew"] = T["rank"] + 3.6                         # 34.8 rewind
T["fb"] = T["rew"] + 0.7                           # 35.5 flashback plays
T["beg"] = [T["fb"] + .5, T["fb"] + 1.0, T["fb"] + 1.5]
T["what"] = T["fb"] + 2.3                          # her: "...what now?"
T["ask"] = T["fb"] + 3.2                           # him: the money
T["why"] = T["fb"] + 5.0                           # her: "Why? So you can look online for fake points?"
T["hypo"] = T["fb"] + 6.9                          # him: "They're not fake. They're... hypothetical."
T["askbots"] = T["fb"] + 8.6                       # her: "Did you ask the bots?"
T["botsaid"] = T["fb"] + 9.8                       # him: "The bots said to ask you."
T["fine"] = T["fb"] + 11.4                         # her: "...fine."
T["honey"] = T["fb"] + 12.5                        # her: "ok honey, here..."
T["coins"] = T["honey"] + .5
T["ff"] = T["fb"] + 14.6                           # fast-forward back
T["ledge2"] = T["ff"] + 0.7                        # lightning callback: THE BOSS. #1.*
T["biz"] = T["ledge2"] + 2.2                       # back to business
T["biz_lines"] = [T["biz"] + .1 + i * .55 for i in range(4)]
T["title"] = T["biz"] + 2.6
T["outro"] = T["biz"] + 5.0                        # 50.8 end card
T["end"] = T["outro"] + 3.6
# ---------------------------------------------------------------- cast
CAST = [  # name, role, line, sprite, accent
    ("THEO", "THE TRADER", "Sells the options. Follows the Rules. Never panics.", "theo_sprite_1x", (226, 170, 100)),
    ("PENNY", "MARKETING", "Makes these videos. Yes, this one.", "penny_sprite_1x", (150, 160, 190)),
    ("ADA", "DATA", "Checks every number. Then checks it again.", "ada_teal_1x", (90, 200, 190)),
    ("ROZ", "LEGAL", "Says no. Professionally.", "roz_sprite_1x", (140, 200, 110)),
    ("KIT", "DECISION LOG", "Logs every decision. Spots the patterns.", "kit_sprite_1x", (240, 150, 190)),
]
SPR = {c[0]: outline(pad(load(c[3]), 2), (0, 0, 0), 1) for c in CAST}
BOSS = load("boss_shadow_1x")
import trailer2_art as ART
ROSE = (255, 150, 190)
FAWN = ART.fawn()
FAWNS = ART.fawn(True)
PIG = ART.piggy()
COIN = None
def coin(s):
    im = Image.new("RGBA", (9, 9)); d = ImageDraw.Draw(im); d.ellipse([0, 0, 8, 8], fill=GOLD + (255,), outline=(170, 120, 20, 255)); d.point([(3, 2), (2, 3)], fill=(255, 240, 180, 255))  # plain coin: no marks the OCR reads as digits
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
    # bars marching under the line, lime up / orange down, then the zigzag line draws over them (illustration; it carries no numbers)
    rb = random.Random(5); n = int(min(1, u / 1.6) * len(CHART))
    for i in range(26):
        x = SAFE_L + i * 38 - int(u * 90) % 38; hgt = int(80 + abs(rb.gauss(0, 1)) * 230 * (0.6 + 0.4 * math.sin(u * 3 + i)))
        up = rb.random() > .45; col = LIME if up else ORANGE
        d.rectangle([x, 1680 - hgt, x + 24, 1680], fill=bl(col, .28)); d.line([(x + 12, 1680 - hgt - 40), (x + 12, 1680 + 30)], fill=bl(col, .28), width=3)
    if n > 1:
        lo, hi = min(CHART), max(CHART); pts = [(SAFE_L + i * (W - 2 * SAFE_L) / 59, 1600 - (v - lo) / (hi - lo) * 520) for i, v in enumerate(CHART[:n])]
        glow = Image.new("RGB", (W, H), BLACK); ImageDraw.Draw(glow).line(pts, fill=LIME, width=26)
        img = Image.blend(img, Image.composite(glow, img, glow.convert("L").point(lambda v: 90 if v else 0)).filter(ImageFilter.GaussianBlur(18)), .6)
        d = ImageDraw.Draw(img); d.line(pts, fill=LIME, width=9); x, y = pts[-1]
        d.ellipse([x - 16, y - 16, x + 16, y + 16], fill=(255, 255, 255)); d.ellipse([x - 10, y - 10, x + 10, y + 10], fill=LIME)
    kicker(d, "WHO ARE WE?")
    k = min(1, u / .5); lineup(img, W // 2, 1860 + int((1 - k) ** 3 * 400), 4, alpha=min(1, u / .4))
    if u > .05: d.text((SAFE_L + 12, 520), "I'M AN", font=archivo(110, 125, 900), fill=INK, anchor="ls")
    slam(d, "AI TRADING", 700, LIME, t, T["bot"] + .25, start=240)
    slam(d, "BOT.", 900, LIME, t, T["bot"] + .45, start=240)
    a = fade(u, 1.3, 1.6)
    d.text((SAFE_L + 12, 1010), "Well… five of them.", font=mono(40, True), fill=bl(INK, a), anchor="ls")
    a2 = fade(u, 1.8, 2.1)
    d.text((SAFE_L + 12, 1070), "And one human.", font=mono(40, True), fill=bl(MUT, a2), anchor="ls")
    return img
def anim(name, t, u, pose, s=11):
    """One character, alive: blink (Theo/Penny/Ada), beat bounce, squash & stretch, tilt, and a pose that fits the line."""
    base = daily.sprite_state(name.lower(), ((t + hash(name) % 7) % 3.1) < .12, t) if name.lower() in daily.SP else load(dict((c[0], c[3]) for c in CAST)[name])
    base = outline(pad(base, 2), (0, 0, 0), 1)
    ph = t * 140 / 60; sx = 1 - .04 * math.sin(2 * math.pi * ph / 2); sy = 1 + .05 * math.sin(2 * math.pi * ph / 2)
    hop = 14 * abs(math.sin(math.pi * ph)); ang = 0; flip = False
    if pose == "nod": hop = -10 * abs(math.sin(2 * math.pi * u * 1.5)); ang = 4 * math.sin(u * 6)
    elif pose == "point": ang = -12; hop += 10
    elif pose == "thumbs": hop += 50 * abs(math.sin(math.pi * u * 3)); ang = 8
    elif pose == "deadpan": hop = 0; sx, sy = 1, 1; ang = 0
    elif pose == "jump": hop += 70 * abs(math.sin(math.pi * u * 2.5))
    elif pose == "spin":
        if u < .8: sx *= math.cos(2 * math.pi * u / .8)
        hop += 30 * abs(math.sin(math.pi * u * 2))
    elif pose == "shake": ang = 10 * math.sin(u * 14)
    w = max(2, int(abs(base.width * s * sx))); h = int(base.height * s * sy)
    im = base.resize((w, h), Image.NEAREST)
    if sx < 0: im = im.transpose(Image.FLIP_LEFT_RIGHT)
    if abs(ang) > .5: im = im.rotate(ang, resample=Image.NEAREST, expand=True)
    return im, int(hop)
def stamp(d, cx, cy, txt, col, k, size=120, ang=-12):
    """Rubber stamp slamming in: scale overshoot, thick outline box."""
    if k <= 0: return
    f = archivo(int(size * k), 125, 900); tw = d.textlength(txt, font=f)
    box = Image.new("RGBA", (int(tw + 80), int(size * k * 1.3)), (0, 0, 0, 0)); bd = ImageDraw.Draw(box)
    bd.rounded_rectangle([0, 0, box.width - 1, box.height - 1], radius=18, outline=col, width=10)
    bd.text((box.width // 2, int(box.height * .78)), txt, font=f, fill=col, anchor="ms")
    box = box.rotate(ang, resample=Image.BICUBIC, expand=True)
    d._image.paste(box, (int(cx - box.width / 2), int(cy - box.height / 2)), box)
def candles(d, u, y0, seed=9, alpha=.9):
    r = random.Random(seed)
    for i in range(24):
        x = SAFE_L + i * 40 - int(u * 160) % 40; o = r.uniform(-1, 1); c = o + r.uniform(-.8, .8); hi_ = max(o, c) + r.uniform(0, .5); lo_ = min(o, c) - r.uniform(0, .5)
        col = LIME if c >= o else ORANGE; sc = 110
        d.line([(x + 12, y0 - hi_ * sc), (x + 12, y0 - lo_ * sc)], fill=bl(col, alpha), width=4)
        d.rectangle([x, y0 - max(o, c) * sc, x + 24, y0 - min(o, c) * sc + 2], fill=bl(col, alpha))
GIMMICK = {
    "THEO": "candles", "PENNY": "confetti", "ADA": "checks", "ROZ": "no", "KIT": "log"}
POSES = {"THEO": "nod", "PENNY": "point", "ADA": "thumbs", "ROZ": "deadpan", "KIT": "spin"}
LOGLINES = ["decision 0412 · logged", "decision 0413 · logged", "pattern: same mistake, 3rd time", "decision 0414 · logged", "pattern found · flagged"]
def sc_card(t):
    i = min(4, int((t - T["roster"]) // T["card"])); u = t - T["cards"][i]
    name, role, line, _, acc = CAST[i]
    img = Image.new("RGB", (W, H), BLACK); d = ImageDraw.Draw(img)
    # accent diagonal wipe + giant ghost number
    wx = int(min(1, u / .22) * (W + 900)) - 900
    d.polygon([(wx, 0), (wx + 900, 0), (wx + 500, H), (wx - 400, H)], fill=bl(acc, .16))
    gf = archivo(760, 125, 900); d.text((W - 40, 1500), f"0{i + 1}", font=gf, fill=bl(acc, .10), anchor="rs")
    g = GIMMICK[name]
    # the character's own thing, behind
    if g == "candles" and u > .5: candles(d, u, 1500, alpha=.75)
    if g == "checks" and u > .5:
        for j in range(18):
            r = random.Random(j); x = r.randint(SAFE_L, W - 80); y = int((u * 700 + r.randint(0, 1000)) % 1000) + 900
            d.line([(x, y), (x + 20, y + 20), (x + 56, y - 28)], fill=bl(LIME, .9), width=12)
    if g == "confetti" and u > .6:
        for j in range(60):
            r = random.Random(j); x = r.randint(60, W - 60); y = int((u * r.randint(500, 900) + r.randint(0, 1200)) % 1300) + 600
            d.rectangle([x, y, x + 14, y + 22], fill=[LIME, ROSE, INK, (120, 200, 255)][j % 4])
    if g == "log" and u > .5:
        f = mono(30, True)
        for j, ln in enumerate(LOGLINES):
            tj = .5 + j * .45
            if u < tj: continue
            shown = ln[:int((u - tj) / .45 * len(ln)) + 1]
            d.text((SAFE_L + 12, 1180 + j * 48), "> " + shown + ("_" if int(u * 6) % 2 else ""), font=f, fill=LIME if "pattern" in ln else INK, anchor="ls")
        for j in range(5):  # pattern dots connecting
            if u > 1.2 + j * .2: d.ellipse([SAFE_R - 240 + j * 48 - 6, 1000 + (j % 2) * 60 - 6, SAFE_R - 240 + j * 48 + 6, 1000 + (j % 2) * 60 + 6], fill=ROSE)
            if j and u > 1.3 + j * .2: d.line([(SAFE_R - 240 + (j - 1) * 48, 1000 + ((j - 1) % 2) * 60), (SAFE_R - 240 + j * 48, 1000 + (j % 2) * 60)], fill=ROSE, width=4)
    kicker(d, f"MEET THE FUND · 0{i + 1}/05")
    slam(d, name, 600, INK, t, T["cards"][i] + .08, start=300)
    if u > .3:
        f = archivo(54, 125, 900); w = d.textlength(role, font=f); x0, x1 = SAFE_L + 12, SAFE_L + 12 + int(w) + 72
        d.rounded_rectangle([x0 + 4, 648, x1 + 4, 752], radius=26, fill=(0, 0, 0))
        img = daily.button(img, x0, 640, x1, 744, fill=LIME, radius=26); d = ImageDraw.Draw(img)
        d.text((SAFE_L + 48, 714), role, font=f, fill=BLACK, anchor="ls")
    a = fade(u, .55, .8)
    if a:
        f = mono(38, True); y = 810; cur = ""
        for w_ in line.split():
            nx = (cur + " " + w_).strip()
            if d.textlength(nx, font=f) <= SAFE_R - SAFE_L - 24: cur = nx
            else: d.text((SAFE_L + 12, y), cur, font=f, fill=bl(INK, a), anchor="ls"); y += 52; cur = w_
        d.text((SAFE_L + 12, y), cur, font=f, fill=bl(INK, a), anchor="ls")
    # the character slides in and performs
    pose = POSES[name] if u > .9 else None
    sp, hop = anim(name, t, u - .9, pose, s=11); k = min(1, u / .3); ease = 1 - (1 - k) ** 3
    cx = int(W + 300 - (W + 300 - 640) * ease); by = 1820 - hop
    d.ellipse([cx - 160, by - 14, cx + 160, by + 26], fill=(26, 26, 26))
    paste_c(img, sp, cx, by); d = ImageDraw.Draw(img)
    # the character's own thing, in front
    if g == "candles" and u > 1.6: stamp(d, 360, 1300, "SOLD", LIME, min(1, pop(t, T["cards"][i] + 1.6, .2)), size=110)
    if g == "confetti" and u > 1.4:
        kk = min(1, pop(t, T["cards"][i] + 1.4, .2)); img = daily.button(img, 330 - int(230 * kk), 1250, 330 + int(230 * kk), 1250 + int(96 * kk), fill=LIME, radius=44); d = ImageDraw.Draw(img)
        if kk > .6: d.text((330, 1250 + int(66 * kk)), "LIKE + FOLLOW", font=archivo(int(44 * kk), 118, 900), fill=BLACK, anchor="ms")
    if g == "checks" and u > 1.6: stamp(d, 330, 1240, "CHECKED", LIME, min(1, pop(t, T["cards"][i] + 1.6, .2)), size=90, ang=8)
    if g == "no":
        for j, (tx, ty) in enumerate([(300, 1120), (560, 1300), (330, 1480)]):
            tj = .9 + j * .45
            if u > tj: stamp(d, tx, ty, "NO", (255, 92, 70), min(1, pop(t, T["cards"][i] + tj, .18)), size=130, ang=[-14, 9, -6][j])
        if u > 2.6: stamp(d, 820, 1040, "yes", LIME, min(1, pop(t, T["cards"][i] + 2.6, .2)), size=70, ang=4)
    if g == "log" and u > 2.8: stamp(d, 330, 1620, "PATTERN", ROSE, min(1, pop(t, T["cards"][i] + 2.8, .2)), size=90, ang=-8)
    if u > T["card"] - .12: img = img.filter(ImageFilter.BoxBlur(10))
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
        k = min(1.0, (t - T["glint"] - .3) / .9)
        if k > 0:
            x0, y0, x1 = SAFE_L + 12, 700, SAFE_L + 560
            d.rectangle([x0, y0, x1, y0 + 44], outline=INK, width=4)
            d.rectangle([x0 + 8, y0 + 8, x0 + 8 + int((x1 - x0 - 16) * k), y0 + 36], fill=LIME)
            d.text((x1 + 24, y0 + 38), "POWER: %d%%" % int(k * 100) if k < 1 else "POWER: MAX", font=mono(30, True), fill=LIME, anchor="ls")
    return img
FAWNL = rim(scaled(FAWNS, 10), ROSE, 6)
def bolt(d, x0, y0, x1, y1, seed, w=10, col=(255, 255, 255)):
    r = random.Random(seed); pts = [(x0, y0)]; n = 7
    for k in range(1, n):
        pts.append((x0 + (x1 - x0) * k / n + r.randint(-70, 70), y0 + (y1 - y0) * k / n))
    pts.append((x1, y1)); d.line(pts, fill=col, width=w)
    for k in range(2, n - 1, 2):  # branches
        px, py = pts[k]; d.line([(px, py), (px + r.randint(-160, 160), py + r.randint(80, 200))], fill=col, width=max(3, w // 2))
def window_scene(d, x, y, w, h, kind, u, r):
    """Tiny things happening in the building's windows."""
    d.rectangle([x, y, x + w, y + h], fill=(255, 220, 130) if kind != "dark" else (20, 20, 30))
    if kind == "party":
        for k in range(5): d.rectangle([x + 6 + k * (w // 5), y + 6 + int(8 * abs(math.sin(u * 7 + k))), x + 6 + k * (w // 5) + 6, y + 6 + int(8 * abs(math.sin(u * 7 + k))) + 6], fill=[LIME, ROSE, (120, 200, 255), GOLD][k % 4])
        for k in range(3): d.rectangle([x + 10 + k * 20, y + h - 24 + int(6 * abs(math.sin(u * 9 + k))), x + 20 + k * 20, y + h - 2], fill=(40, 30, 20))
    elif kind == "desk":
        d.rectangle([x + 8, y + h - 20, x + w - 8, y + h - 14], fill=(90, 60, 30)); d.rectangle([x + w // 2 - 8, y + h - 36, x + w // 2 + 8, y + h - 20], fill=(40, 30, 20))
        d.rectangle([x + 10, y + h - 34, x + 26, y + h - 22], fill=(120, 200, 255) if int(u * 4) % 2 else (60, 120, 200))
    elif kind == "cat":
        d.ellipse([x + w // 2 - 10, y + h - 18, x + w // 2 + 10, y + h - 4], fill=(30, 20, 20)); d.polygon([(x + w // 2 - 8, y + h - 16), (x + w // 2 - 6, y + h - 26), (x + w // 2 - 2, y + h - 16)], fill=(30, 20, 20))
        d.polygon([(x + w // 2 + 2, y + h - 16), (x + w // 2 + 6, y + h - 26), (x + w // 2 + 8, y + h - 16)], fill=(30, 20, 20))
        d.line([(x + w // 2 + 10, y + h - 10), (x + w // 2 + 18 + int(4 * math.sin(u * 5)), y + h - 20)], fill=(30, 20, 20), width=3)
    elif kind == "plant":
        d.rectangle([x + w // 2 - 6, y + h - 14, x + w // 2 + 6, y + h - 4], fill=(150, 80, 50)); d.ellipse([x + w // 2 - 12, y + h - 34, x + w // 2 + 12, y + h - 12], fill=(60, 140, 70))
    elif kind == "tv":
        d.rectangle([x + 8, y + 8, x + w - 8, y + h - 14], fill=[(60, 120, 220), (220, 80, 80), (80, 200, 120)][int(u * 3 + r) % 3])
def ledge(t, t0, text_fn, dur_flash=(0.0, 0.9, 1.4)):
    """Four quadrants: Q1 (top right) the boss on the roof edge, Q4 (bottom right) his building with life in the windows,
    Q2 + Q3 (the left half) the city far behind, with the words left-aligned and lightning timed to them."""
    u = t - t0; img = Image.new("RGB", (W, H), (6, 8, 14)); d = ImageDraw.Draw(img)
    fl = max([max(0, 1 - (u - f) / .25) for f in dur_flash if u >= f] + [0])
    sky = tuple(int(c + (190 - c) * fl * .9) for c in (12, 14, 28))
    d.rectangle([0, 0, W, H], fill=sky)
    r = random.Random(3)
    for i in range(12):  # far city, left half and behind
        bx = i * 96 - 60; bh = r.randint(220, 560); d.rectangle([bx, 1700 - bh, bx + 76, 1700], fill=(9, 9, 16) if fl < .3 else (26, 26, 40))
        for wy in range(1700 - bh + 30, 1680, 44):
            for wx in range(bx + 10, bx + 66, 22):
                if r.random() < .3: d.rectangle([wx, wy, wx + 8, wy + 14], fill=(255, 220, 120) if r.random() < .8 else (120, 200, 255))
    d.rectangle([0, 1700, W, H], fill=(8, 8, 12))
    for i in range(60):  # rain
        rr = random.Random(i + int(u * 40)); x = rr.randint(0, W); y = rr.randint(0, H); d.line([(x, y), (x - 10, y + 60)], fill=(70, 80, 110), width=2)
    if fl > 0:
        bolt(d, 420, 0, 300, 560, int(t0 * 10) + int(u * 4), w=12)
        bolt(d, 130, 0, 200, 420, int(t0 * 10) + 7 + int(u * 4), w=6, col=(220, 230, 255))
    # the building: Q4, with the roof at y 960
    BX, BY = 560, 960
    d.rectangle([BX, BY, W, H], fill=(18, 18, 24)); d.rectangle([BX, BY, W, BY + 30], fill=(44, 44, 52)); d.rectangle([BX - 16, BY - 14, W, BY + 4], fill=(60, 60, 70))
    kinds = ["party", "desk", "cat", "dark", "plant", "tv", "desk", "dark", "party", "cat", "tv", "plant", "dark", "desk", "party", "cat"]
    k = 0
    for wy in range(BY + 90, H - 60, 200):
        for wx in range(BX + 50, W - 110, 130):
            window_scene(d, wx, wy, 100, 120, kinds[k % len(kinds)], u + k, k); k += 1
    cape = rim(scaled(BOSS, 7), LIME if fl < .4 else (255, 255, 255), 4)
    paste_c(img, cape, 830, BY - 8)   # Q1: on the edge
    text_fn(d, u, fl); return img
def sc_no1(t):
    def txt(d, u, fl):
        kicker(d, "OFFICIAL RANKING", col=INK if fl > .3 else MUT)
        slam(d, "THE", 620, INK, t, T["no1"] + .05, start=200, maxw=460)
        slam(d, "BOSS", 820, INK, t, T["no1"] + .25, start=200, maxw=460)
        slam(d, "IS #1.", 1180, GOLD, t, T["no1"] + .75, start=200, maxw=460)
    img = ledge(t, T["no1"], txt, dur_flash=(0.05, 0.75, 1.4))
    u = t - T["no1"]
    return shift(img, *shake(t, 8)) if .45 < u < .8 else img
def sc_ledge2(t):
    def txt(d, u, fl):
        kicker(d, "BACK TO BUSINESS", col=INK if fl > .3 else MUT)
        slam(d, "THE", 620, INK, t, T["ledge2"] + .05, start=200, maxw=460)
        slam(d, "BOSS.", 820, INK, t, T["ledge2"] + .2, start=200, maxw=460)
        slam(d, "#1.*", 1180, GOLD, t, T["ledge2"] + .6, start=220, maxw=460)
        if u > 1.1: d.text((SAFE_L + 12, 1260), "*at the office", font=mono(30, True), fill=INK, anchor="ls")
    img = ledge(t, T["ledge2"], txt, dur_flash=(0.0, 0.6, 1.3))
    return shift(img, *shake(t, 10)) if .5 < t - T["ledge2"] < .85 else img
def sc_yet(t):
    u = t - T["yet"]; img = Image.new("RGB", (W, H), BLACK); d = ImageDraw.Draw(img)
    a = fade(u, .1, .4)
    d.text((SAFE_L + 12, 700), "YET…", font=archivo(180, 125, 900), fill=bl(INK, a), anchor="ls")
    a2 = fade(u, .9, 1.3)
    for i, ln in enumerate(("THERE IS ALWAYS", "ONE ABOVE.")):
        f = fit(ln, SAFE_R - SAFE_L, 140, wdth=125, wght=900)
        d.text((SAFE_L + 12, 900 + i * 160), ln, font=f, fill=bl(ROSE if i else INK, a2), anchor="ls")
    return img
def _row(img, d, y, rank, name, k, col, crack=0.0):
    x0, x1 = SAFE_L + 12, W - M
    d.rounded_rectangle([x0, y, x1, y + 150], radius=14, outline=col, width=4)
    d.text((x0 + 24, y + 62), rank, font=archivo(56, 125, 900), fill=col, anchor="ls")
    d.text((x0 + 150, y + 62), name, font=archivo(52, 120, 900), fill=INK, anchor="ls")
    bx0, by0, bx1 = x0 + 24, y + 86, x1 - 170
    d.rectangle([bx0, by0, bx1, by0 + 40], outline=INK, width=3)
    fw = int((bx1 - bx0 - 12) * min(k, 1.0))
    if fw > 0: d.rectangle([bx0 + 6, by0 + 6, bx0 + 6 + fw, by0 + 34], fill=col)
    if k > 1.0:  # overflow: the fill pushes out past the frame
        d.rectangle([bx1, by0 + 6, bx1 + int((k - 1) * 600), by0 + 34], fill=col)
    if crack > 0:
        r = random.Random(7)
        for j in range(int(6 * crack) + 1):
            cx = r.randint(bx0 + 40, bx1 - 40); pts = [(cx, by0 - 10)]
            for _ in range(4): pts.append((pts[-1][0] + r.randint(-26, 26), pts[-1][1] + 16))
            d.line(pts, fill=(255, 255, 255), width=4)
    return bx0, by0, bx1
def sc_rank(t):
    u = t - T["rank"]; img = Image.new("RGB", (W, H), BLACK); d = ImageDraw.Draw(img)
    # her spotlight + rising silhouette (rose), under the rankings
    if t >= T["slide"]:
        v = t - T["slide"]
        cone = Image.new("L", (W, H), 0); cd = ImageDraw.Draw(cone)
        cd.polygon([(W // 2 - 70, 900), (W // 2 + 70, 900), (W // 2 + 420, 1880), (W // 2 - 420, 1880)], fill=int(90 * min(1, v / .4)))
        img = Image.composite(Image.new("RGB", (W, H), (80, 40, 60)), img, cone.filter(ImageFilter.GaussianBlur(40))); d = ImageDraw.Draw(img)
        e = 1 - (1 - min(1, v / 1.0)) ** 3
        paste_c(img, FAWNL, W // 2, int(2700 - (2700 - 1880) * e))
    kicker(d, "POWER RANKINGS · UPDATED")
    # rows: the boss starts at #1; the new #1 drops in and pushes him to #2
    sl = 0 if t < T["slide"] else min(1, (t - T["slide"]) / .35)
    e = 1 - (1 - sl) ** 3
    by_boss = int(420 + 190 * e)
    _row(img, d, by_boss, "#1" if sl < .5 else "#2", "THE BOSS", 1.0, LIME)
    if sl > 0:
        k = 0 if t < T["fill"] else (t - T["fill"]) / (T["crack"] - T["fill"]) * 1.0
        if t >= T["crack"]: k = 1.0 + min(.5, (t - T["crack"]) / .35 * .5)
        crack = 0 if t < T["crack"] else min(1, (t - T["crack"]) / .3)
        yr = int(420 - 400 * (1 - e))
        if t < T["shatter"]:
            bx0, by0, bx1 = _row(img, d, yr, "#1", "THE REAL BOSS", k, ROSE, crack)
            if T["fill"] <= t < T["shatter"]:
                d.text((W - M - 20, yr + 122), "POWER" if k < 1 else "OVER", font=mono(30, True), fill=ROSE, anchor="rs")
        else:  # shards fly out of where the bar was
            v = t - T["shatter"]; r = random.Random(11)
            for j in range(40):
                sx = r.randint(SAFE_L + 40, W - 200); sy = yr + 100 + r.randint(-10, 30)
                vx, vy = r.uniform(-900, 900), r.uniform(-1300, 200); g = 2400
                x = sx + vx * v; y = sy + vy * v + g * v * v / 2; s_ = r.randint(10, 34); a = r.uniform(0, 6.28) + v * r.uniform(-8, 8)
                pts = [(x + math.cos(a + q) * s_, y + math.sin(a + q) * s_) for q in (0, 2.3, 4.1)]
                d.polygon(pts, fill=ROSE if j % 3 else (255, 255, 255))
            d.rounded_rectangle([SAFE_L + 12, yr, W - M, yr + 150], radius=14, outline=ROSE, width=4)
            d.text((SAFE_L + 36, yr + 62), "#1", font=archivo(56, 125, 900), fill=ROSE, anchor="ls")
            d.text((SAFE_L + 162, yr + 62), "THE REAL BOSS", font=archivo(52, 120, 900), fill=INK, anchor="ls")
            d.text((SAFE_L + 36, yr + 128), "POWER: UNMEASURABLE", font=mono(32, True), fill=ROSE, anchor="ls")
            if v < .12: img = Image.blend(img, Image.new("RGB", (W, H), (255, 230, 240)), .7 * (1 - v / .12))
    if t >= T["crack"] and t < T["shatter"] + .4: img = shift(img, *shake(t, 14))
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
    src = sc_rank(T["shatter"] + 1.0) if not forward else sc_flash(T["coins"] + .8)
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
LINES = [  # the back and forth: (start, who, text, size)
    (T["beg"][0], "him", "please.", 44), (T["beg"][1], "him", "please.", 62), (T["beg"][2], "him", "PLEASE.", 92),
    (T["what"], "her", "…what now?", 60),
    (T["ask"], "him", "Can I have the money so the bots can trade for real?", 54),
    (T["why"], "her", "Why? So you can look online for fake points?", 50),
    (T["hypo"], "him", "They're not fake. They're… hypothetical.", 54),
    (T["askbots"], "her", "Did you ask the bots?", 56),
    (T["botsaid"], "him", "The bots said to ask you.", 58),
    (T["fine"], "her", "…fine.", 90),
    (T["honey"], "her", "ok honey, here…", 60)]
def sc_flash(t):
    u = t - T["fb"]; img = Image.new("RGB", (W, H), (120, 96, 70)); d = ImageDraw.Draw(img)
    d.rectangle([0, 1500, W, H], fill=(80, 60, 40))                         # floor
    for i in range(9): d.line([(i * 140, 1500), (i * 140 - 300, H)], fill=(66, 48, 30), width=4)
    d.rectangle([330, 1330, 630, 1520], fill=(150, 120, 90)); d.rectangle([310, 1310, 650, 1345], fill=(175, 145, 110))  # little table
    pig = scaled(PIG, 5); pb = 1312 - (int(10 * abs(math.sin(u * 14))) if T["fine"] <= t < T["coins"] + .4 else 0)
    if t < T["coins"]: paste_c(img, pig, 480, pb)
    else:  # the piggy pops open: two halves fly apart
        v = t - T["coins"]; hw = pig.width // 2
        lh, rh = pig.crop((0, 0, hw, pig.height)), pig.crop((hw, 0, pig.width, pig.height))
        img.paste(lh.rotate(v * 40, expand=True, resample=Image.NEAREST), (int(480 - hw - v * 160), int(pb - pig.height - 30 * v + 300 * v * v)), lh.rotate(v * 40, expand=True, resample=Image.NEAREST))
        img.paste(rh.rotate(-v * 40, expand=True, resample=Image.NEAREST), (int(480 + v * 160), int(pb - pig.height - 30 * v + 300 * v * v)), rh.rotate(-v * 40, expand=True, resample=Image.NEAREST))
        for i in range(30):  # coins burst up, then fall
            r = random.Random(i); vx, vy = r.uniform(-700, 700), r.uniform(-1500, -700)
            x = 480 + vx * v; y = pb - 140 + vy * v + 2200 * v * v
            if 0 < y < 1700 and 0 < x < W: img.paste(COIN, (int(x), int(y)), COIN)
    # her: the fawn stands tall on the right; him: kneeling on the left
    lvl = sum(t >= b for b in T["beg"])
    fz = rim(scaled(FAWN, 7), ROSE, 4); paste_c(img, fz, 880, 1580 - (int(6 * abs(math.sin(u * 2))) if t < T["fine"] else 0))
    boss = rim(scaled(BOSS, 8), LIME, 4)   # full body, legs and all (the boss 11/1: "I have no legs")
    paste_c(img, boss, 220, 1580 - int((6 + lvl * 6) * abs(math.sin(u * (6 + lvl * 3)))))
    shown = [x for x in LINES if t >= x[0]]
    him = [x for x in shown if x[1] == "him"]; her = [x for x in shown if x[1] == "her"]
    if him:
        if him[-1][0] in T["beg"] and t < T["what"] + .6:  # the three pleases stack
            for i, x in enumerate([h for h in him if h[0] in T["beg"]]):
                bubble(img, SAFE_L + 12 + i * 24, 450 + i * 100, x[2], max(8, int(x[3] * min(1, pop(t, x[0], .15) or .01))), tail=(230, 1130))
        else:
            x = him[-1]; bubble(img, SAFE_L + 12, 450, x[2], max(8, int(x[3] * min(1, pop(t, x[0], .15) or .01))), tail=(230, 1130), maxw=470)
    img = vhs(img, t, "HOW IT STARTED")
    if her:  # her bubble is drawn after the tape look so the pink stays pink
        x = her[-1]; sz = max(8, int(x[3] * min(1, pop(t, x[0], .15) or .01)))
        y1 = bubble(img, 600, 600, x[2], sz, col=(255, 182, 210), bg=(120, 30, 70), tail=(840, 1000), maxw=350)
        d = ImageDraw.Draw(img); hx, hy = 600 + 24, y1 - 10
        d.ellipse([hx, hy - 10, hx + 12, hy + 2], fill=(255, 90, 140)); d.ellipse([hx + 10, hy - 10, hx + 22, hy + 2], fill=(255, 90, 140)); d.polygon([(hx, hy - 2), (hx + 22, hy - 2), (hx + 11, hy + 12)], fill=(255, 90, 140))
    d = ImageDraw.Draw(img)
    d.text((SAFE_L + 12, 1440), "THE BOSS  vs.  THE REAL BOSS", font=fit("THE BOSS  vs.  THE REAL BOSS", SAFE_R - SAFE_L - 24, 40, wdth=110, wght=900), fill=(255, 240, 200), anchor="ls")
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
        hit = [tb for tb in T["biz_lines"] if 0 <= t - tb < .1]
        if hit: img = Image.blend(img, Image.new("RGB", (W, H), (255, 255, 255)), .5 * (1 - (t - hit[0]) / .1))
        if any(0 <= t - tb < .3 for tb in T["biz_lines"]): img = shift(img, *shake(t, 12))
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
    elif t < T["no1"]: img = sc_boss(t)
    elif t < T["yet"]: img = sc_no1(t)
    elif t < T["rank"]: img = sc_yet(t)
    elif t < T["rew"]: img = sc_rank(t)
    elif t < T["fb"]: img = sc_rewind(t)
    elif t < T["ff"]: img = sc_flash(t)
    elif t < T["ledge2"]: img = sc_rewind(t, forward=True)
    elif t < T["biz"]: img = sc_ledge2(t)
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
