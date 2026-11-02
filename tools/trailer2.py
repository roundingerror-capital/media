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
T = dict(meet=0.5, fund=1.1, bot=2.2, roster=4.7, card=2.9)   # v7: 60 s cut
T["cards"] = [T["roster"] + i * T["card"] for i in range(5)]
T["team"] = T["roster"] + 5 * T["card"]          # 20.0 lineup
T["above"] = T["team"] + 1.6                       # 21.9 "and above them all"
T["booms"] = [T["above"] + .8, T["above"] + 1.3, T["above"] + 1.8]
T["boss"] = T["booms"][-1]                         # 24.1 reveal
T["glint"] = T["boss"] + 1.1
T["no1"] = T["boss"] + 2.7                         # 27.3 "THE BOSS IS #1."
T["yet"] = T["no1"] + 1.4                          # 28.8 "YET... THERE IS ALWAYS ONE ABOVE."
T["rank"] = T["yet"] + 2.0                         # 31.2 power rankings: a new #1 appears
T["slide"] = T["rank"] + .45                       # new row drops in, the boss moves to #2
T["fill"] = T["rank"] + 1.0                        # her bar starts filling
T["crack"] = T["rank"] + 2.1                       # the bar cracks
T["shatter"] = T["rank"] + 2.45                    # ...and breaks
T["rew"] = T["rank"] + 3.1                         # 34.8 rewind
T["fb"] = T["rew"] + 0.6                           # 35.5 flashback plays
T["beg"] = [T["fb"] + .4, T["fb"] + .8, T["fb"] + 1.2]
T["what"] = T["fb"] + 1.9                          # her: "...what now?"
T["ask"] = T["fb"] + 2.7                           # him: the money
T["why"] = T["fb"] + 4.3                           # her: "Why? So you can look online for fake points?"
T["hypo"] = T["fb"] + 5.9                          # him: "They're not fake. They're... hypothetical."
T["askbots"] = T["fb"] + 7.3                       # her: "Did you ask the bots?"
T["botsaid"] = T["fb"] + 8.3                       # him: "The bots said to ask you."
T["fine"] = T["fb"] + 9.6                         # her: "...fine."
T["honey"] = T["fb"] + 10.2                        # her: "ok honey, here..."
T["coins"] = T["honey"] + .5
T["ff"] = T["fb"] + 11.8                           # fast-forward back
T["ledge2"] = T["ff"] + 0.6                        # lightning callback: THE BOSS. #1.*
T["biz"] = T["ledge2"] + 1.9                       # back to business
T["biz_lines"] = [T["biz"] + .1 + i * .55 for i in range(4)]   # REAL TRADES / REAL MONEY hurled at the screen (v6)
T["care"] = T["biz"] + 2.6                          # v6 (the boss 11/1): "so much care is going into this"
T["care_lines"] = [T["care"] + i * .8 for i in range(4)]
T["yolo"] = T["care"] + 3.5                         # WE ARE NOT YOLOING.
T["power"] = T["yolo"] + 1.1                        # WE TRADE WITH THE POWER OF AI. the boss returns
T["glare"] = T["power"] + .9                       # anime glare on the aviators
T["title"] = T["power"] + 1.9
T["outro"] = T["title"] + 2.0                      # end card
T["end"] = T["outro"] + 3.0
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
FAWN = ART.fawn_v27()   # the 64x64 standard (V22/V23), V27 cream
FAWNS = ART.fawn_v27(True)
import assets as ASSETS
PIG = ASSETS.get("PIG-02")   # v7 (the boss 11/2): the lucky gold piggy from the asset library
BLDG = ASSETS.get("BLD-03-F5", 1.0)   # BLD-03 flavor 5, the gothic one (umber brick, pediments, crenellated parapet, night)
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
    k = min(1, u / .5); lineup(img, W // 2, 1860 + int((1 - k) ** 3 * 400), 4, alpha=min(1, u / .4), t=t, u=u - .6)
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
    base = BOSS if name == "BOSS" else daily.sprite_state(name.lower(), ((t + hash(name) % 7) % 3.1) < .12, t) if name.lower() in daily.SP else load(dict((c[0], c[3]) for c in CAST)[name])
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
    elif pose == "brow_tap": hop = 0; sx, sy = 1, 1; ang = -6 if int(u * 1.5) % 2 else 3   # Roz: side-eye, tiny head tilt
    elif pose == "lookdown": hop = 0; sx, sy = 1.08, .82; ang = -9          # crouched at the edge, leaning over
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
def lineup(img, cx, by, s, alpha=1.0, gap=16, t=None, u=0.0):
    """The five together. With t, nobody stands still (the boss 11/1: "they look constipated"): each one runs their own pose
    on their own phase, staggered a beat apart, and the row breathes (slight height stagger, Kit a step forward)."""
    if t is None:
        sps = [scaled(SPR[c[0]], s) for c in CAST]; tw = sum(p.width for p in sps) + gap * 4; x = cx - tw // 2
        for p in sps: paste_c(img, p, x + p.width // 2, by, alpha); x += p.width + gap
        return
    n = len(CAST); step = min(int(SPR["THEO"].width * s) + gap, (W - 120 - int(SPR["THEO"].width * s)) // (n - 1)); x = max(60 + int(SPR["THEO"].width * s) // 2, cx - (step * (n - 1)) // 2)
    for i, c in enumerate(CAST):
        ui = u - i * .22; pose = POSES[c[0]] if ui > 0 else None
        if pose == "deadpan": pose = "brow_tap"   # Roz: a slow side-eye instead of a statue
        sp, hop = anim(c[0], t + i * .9, max(0, ui), pose, s=s)
        dy = [0, -10, 0, -6, 12][i]
        paste_c(img, sp, x + i * step, by - hop + dy, alpha)
def sc_team(t):
    u = t - T["team"]; img = Image.new("RGB", (W, H), BLACK); d = ImageDraw.Draw(img)
    kicker(d, "THE TEAM")
    slam(d, "FIVE BOTS.", 620, INK, t, T["team"] + .05, start=250)
    slam(d, "ONE JOB.", 820, LIME, t, T["team"] + .4, start=250)
    k = min(1, u / .4); lineup(img, W // 2, 1700 + int((1 - k) ** 3 * 500), 5, t=t, u=u - .4)
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
TEMPS = {"2700K": (255, 176, 96), "3500K": (255, 208, 150), "5000K": (222, 232, 255), "red": (235, 70, 70), "purple": (175, 95, 225), "teal": (80, 200, 190), "dark": (16, 16, 26)}
def window_scene(d, img, x, y, w, h, kind, temp, u, r):
    """To scale (the boss 11/1): a high-rise window is floor-to-ceiling, about 12 ft, set edge to edge with its neighbours.
    The room is drawn on a 180x300 canvas where a character or a pet is life-size against that height, then shrunk into the window."""
    tmp = Image.new("RGB", (180, 300)); _interior(ImageDraw.Draw(tmp), tmp, 0, 0, 180, 300, kind, temp, u, r)
    img.paste(tmp.resize((w, h), Image.LANCZOS), (x, y))
    d.rectangle([x - 3, y - 3, x + w + 3, y + h + 3], outline=(30, 30, 40), width=3); d.line([(x + w // 2, y), (x + w // 2, y + h)], fill=(30, 30, 40), width=2)
def _interior(d, img, x, y, w, h, kind, temp, u, r):
    """One apartment window, 110x130 (v6, the boss 11/1: "the windows look super cheap"): its own light temperature, a curtain or a
    blind, something alive inside (a TV flickering, a cat, a dog, a fish tank, a plant, a desk lamp, a party) and cameos of our five."""
    base = TEMPS[temp]; rr = random.Random(r)
    d.rectangle([x, y, x + w, y + h], fill=tuple(int(c * .9) for c in base))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=tuple(int(c * .55) for c in base))          # darker floor
    if kind == "tv":
        tvc = [(70, 130, 240), (240, 90, 90), (90, 230, 140), (250, 250, 250), (200, 120, 255)][int(u * 4 + r) % 5]
        d.rectangle([x, y, x + w, y + h], fill=tuple(int(b * .35 + c * .45) for b, c in zip(base, tvc)))  # the screen lights the room
        d.rectangle([x + w // 2 - 30, y + h - 62, x + w // 2 + 30, y + h - 26], fill=(8, 8, 10)); d.rectangle([x + w // 2 - 26, y + h - 58, x + w // 2 + 26, y + h - 30], fill=tvc)
        d.rectangle([x + w // 2 - 36, y + h - 24, x + w // 2 + 36, y + h - 16], fill=(30, 26, 22))  # stand
    elif kind == "cat":
        cx_ = x + w // 2 + int(6 * math.sin(u * .7)); cy_ = y + h - 20
        d.ellipse([cx_ - 16, cy_ - 12, cx_ + 14, cy_ + 2], fill=(22, 18, 18)); d.ellipse([cx_ + 6, cy_ - 22, cx_ + 22, cy_ - 8], fill=(22, 18, 18))
        d.polygon([(cx_ + 8, cy_ - 20), (cx_ + 10, cy_ - 30), (cx_ + 14, cy_ - 20)], fill=(22, 18, 18)); d.polygon([(cx_ + 15, cy_ - 20), (cx_ + 19, cy_ - 30), (cx_ + 21, cy_ - 20)], fill=(22, 18, 18))
        d.line([(cx_ - 16, cy_ - 6), (cx_ - 30 + int(5 * math.sin(u * 3)), cy_ - 24)], fill=(22, 18, 18), width=4)
        d.point([(cx_ + 11, cy_ - 15), (cx_ + 17, cy_ - 15)], fill=(120, 255, 120))             # eyes catch the light
    elif kind == "dog":
        cx_ = x + w // 2; cy_ = y + h - 18; wag = int(10 * math.sin(u * 12))
        d.rounded_rectangle([cx_ - 24, cy_ - 22, cx_ + 18, cy_], radius=8, fill=(150, 100, 50)); d.rounded_rectangle([cx_ + 10, cy_ - 36, cx_ + 34, cy_ - 16], radius=6, fill=(150, 100, 50))
        d.polygon([(cx_ + 12, cy_ - 36), (cx_ + 8, cy_ - 46), (cx_ + 20, cy_ - 36)], fill=(110, 70, 35)); d.line([(cx_ - 24, cy_ - 16), (cx_ - 40, cy_ - 30 + wag)], fill=(150, 100, 50), width=5)
        for lx in (cx_ - 18, cx_ - 6, cx_ + 4, cx_ + 14): d.rectangle([lx, cy_, lx + 5, cy_ + 8], fill=(120, 80, 40))
    elif kind == "fish":
        d.rectangle([x + 14, y + h - 70, x + w - 14, y + h - 22], fill=(40, 120, 200)); d.rectangle([x + 14, y + h - 70, x + w - 14, y + h - 66], fill=(120, 200, 255))
        for k in range(3):
            fx = x + 24 + int(((u * (18 + 9 * k) + k * 37) % (w - 52))); fy = y + h - 60 + int(8 * math.sin(u * 2 + k)) + k * 12
            d.ellipse([fx, fy, fx + 12, fy + 7], fill=[(255, 140, 40), (255, 220, 60), (255, 90, 120)][k]); d.polygon([(fx, fy + 3), (fx - 6, fy - 1), (fx - 6, fy + 8)], fill=[(255, 140, 40), (255, 220, 60), (255, 90, 120)][k])
    elif kind == "plant":
        d.rectangle([x + w // 2 - 10, y + h - 30, x + w // 2 + 10, y + h - 14], fill=(170, 90, 55))
        for k in range(5):
            a = -1.4 + k * .7; lx = x + w // 2 + int(math.cos(a) * 26); ly = y + h - 50 + int(math.sin(a) * 14) - 10
            d.ellipse([lx - 10, ly - 20, lx + 10, ly + 6], fill=(50 + k * 8, 140 + k * 10, 70))
    elif kind == "desk":
        d.rectangle([x + 10, y + h - 40, x + w - 10, y + h - 32], fill=(100, 70, 40)); d.rectangle([x + w // 2 - 14, y + h - 62, x + w // 2 + 14, y + h - 40], fill=(30, 30, 36))
        d.rectangle([x + w // 2 - 12, y + h - 60, x + w // 2 + 12, y + h - 44], fill=(150, 220, 255) if int(u * 2) % 2 else (90, 150, 230))
        d.ellipse([x + w - 40, y + h - 76, x + w - 16, y + h - 60], fill=(255, 240, 200)); d.line([(x + w - 28, y + h - 60), (x + w - 28, y + h - 40)], fill=(60, 60, 60), width=3)
    elif kind == "party":
        for k in range(6):
            px = x + 8 + k * (w // 6); py = y + 8 + int(10 * abs(math.sin(u * 7 + k)))
            d.ellipse([px, py, px + 10, py + 10], fill=[LIME, ROSE, (120, 200, 255), GOLD, (255, 255, 255), (255, 120, 60)][k])
        for k in range(4): d.rectangle([x + 10 + k * 24, y + h - 40 + int(8 * abs(math.sin(u * 9 + k * 1.3))), x + 24 + k * 24, y + h - 14], fill=(40, 30, 30))
    elif kind == "cameo":   # one of us, home for the night
        who = CAST[r % 5][0]; sp = daily.sprite_state(who.lower(), False, u) if who.lower() in daily.SP else load(dict((c[0], c[3]) for c in CAST)[who])
        sp = scaled(sp, 1.6); img.paste(sp, (x + w // 2 - sp.width // 2, y + h - 14 - sp.height + int(3 * abs(math.sin(u * 3)))), sp)
    # curtains / blinds (every other window)
    if rr.random() < .5:
        cc = [(120, 40, 50), (60, 70, 120), (200, 190, 170), (70, 110, 80)][rr.randint(0, 3)]
        d.polygon([(x, y), (x + 34, y), (x + 22, y + h), (x, y + h)], fill=cc); d.polygon([(x + w, y), (x + w - 34, y), (x + w - 22, y + h), (x + w, y + h)], fill=cc)
    elif rr.random() < .5:
        for by_ in range(y + 6, y + int(h * rr.uniform(.3, .7)), 9): d.line([(x, by_), (x + w, by_)], fill=tuple(int(c * .45) for c in base), width=4)
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
    # moon behind the clouds, Q2
    d.ellipse([600, 380, 760, 540], fill=(230, 232, 240) if fl > .3 else (200, 204, 220)); d.ellipse([560, 460, 840, 560], fill=sky)
    # the building: Q4 = the top 3-4 floors of BLD-03-F5 from the asset library (the boss 11/2: "use only the top levels")
    BX, BY = 560, 960
    sc_ = 1.9; crop = BLDG.crop((0, 84, 300, 84 + 30 + 58 * 4))   # the parapet and the top four floors only
    bld = crop.resize((int(crop.width * sc_), int(crop.height * sc_)), Image.NEAREST)
    img.paste(bld, (BX - 30, BY - 46), bld)
    fog = Image.new("RGBA", (W, H), (0, 0, 0, 0)); fd = ImageDraw.Draw(fog); fy0 = BY - 46 + bld.height - 110
    for yy in range(fy0, H, 4): fd.rectangle([BX - 30, yy, W, yy + 4], fill=(6, 8, 14, int(255 * min(1, (yy - fy0) / 200))))   # the floors below vanish into the night: we are way up
    img.paste(fog, (0, 0), fog); d = ImageDraw.Draw(img)
    if fl > .3:   # lightning flash brightens the facade
        fl_ = Image.new("RGBA", bld.size, (200, 210, 255, int(90 * fl))); fl_.putalpha(Image.composite(fl_.split()[3], Image.new("L", bld.size, 0), bld.split()[3])); img.paste(fl_, (BX - 30, BY - 46), fl_); d = ImageDraw.Draw(img)
    # the boss, crouched at the corner of the roof, looking down over the edge (the boss 11/1: Batman animated series, not a statue)
    sp, _ = anim("BOSS", t, u, "lookdown", s=4)   # foreground perspective, but to scale with the 12 ft windows below
    sp = sp.transpose(Image.FLIP_LEFT_RIGHT)   # faces the street below, right edge of the roof
    cape = rim(sp, LIME if fl < .4 else (255, 255, 255), 4)
    if fl > .3:   # lightning: his long shadow thrown back across the roof
        d.polygon([(W - 260, BY - 14), (W - 120, BY - 14), (BX + 160, BY + 30), (BX + 20, BY + 30)], fill=(12, 12, 18))
    paste_c(img, cape, W - 150, BY - 2)
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
def cloaked(img, cx, by, v):
    """THE REAL BOSS, first appearance (the boss 11/1): a hooded cloak, nobody can see who is inside, a pink-purple aura glowing
    behind her. Emperor energy. No face, no name, no relationship on screen."""
    aura = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ad = ImageDraw.Draw(aura); pulse = 1 + .08 * math.sin(v * 5)
    for i, (col, rad) in enumerate(((ROSE, 520), ((200, 90, 255), 400), ((255, 120, 220), 280))):
        rr = int(rad * pulse); ad.ellipse([cx - rr, by - 560 - rr // 2, cx + rr, by - 560 + rr // 2 + 300], fill=col + (70 + 40 * i,))
    img = Image.alpha_composite(img.convert("RGBA"), aura.filter(ImageFilter.GaussianBlur(70))).convert("RGB"); d = ImageDraw.Draw(img)
    r = random.Random(4)
    for i in range(40):   # sparks drifting up through the glow
        x = cx + r.randint(-420, 420); y = (by - r.randint(0, 900) - int(v * r.randint(120, 320))) % 1900
        if y < by: d.rectangle([x, y, x + 5, y + 5], fill=[ROSE, (220, 140, 255), (255, 255, 255)][i % 3])
    top = by - 720; hw = 330
    cloak = Image.new("RGBA", (W, H), (0, 0, 0, 0)); cd = ImageDraw.Draw(cloak)
    body = [(cx - 150, top + 230), (cx - 190, top + 300), (cx - 230, top + 470), (cx - hw, by), (cx + hw, by), (cx + 230, top + 470), (cx + 190, top + 300), (cx + 150, top + 230)]
    cd.polygon(body, fill=(255, 120, 210, 255)); cd.ellipse([cx - 150, top + 10, cx + 150, top + 300], fill=(255, 120, 210, 255))   # rim light shape
    rimmed = cloak.split()[3].filter(ImageFilter.MaxFilter(13))
    img.paste(Image.new("RGB", (W, H), (255, 130, 215)), (0, 0), rimmed); d = ImageDraw.Draw(img)
    for (ax, sgn) in ((cx - 60, -1), (cx + 60, 1)):   # two hairline antler tips poke through the hood: a hint, nothing more
        d.line([(ax, top + 40), (ax + sgn * 18, top - 30), (ax + sgn * 10, top - 70)], fill=(232, 206, 168), width=7)
        d.line([(ax + sgn * 16, top - 22), (ax + sgn * 44, top - 46)], fill=(232, 206, 168), width=6)
    d.polygon(body, fill=(44, 16, 62)); d.ellipse([cx - 150, top + 10, cx + 150, top + 300], fill=(54, 20, 76))
    d.polygon([(cx, top - 10), (cx - 80, top + 60), (cx + 80, top + 60)], fill=(54, 20, 76))                         # the hood's peak
    d.ellipse([cx - 92, top + 110, cx + 92, top + 300], fill=(4, 1, 8))                                                  # the hollow: nothing to see
    d.arc([cx - 98, top + 100, cx + 98, top + 306], 200, 340, fill=(120, 60, 160), width=6)                              # hood edge catches the aura
    for i in range(6): d.line([(cx - 150 + i * 60, top + 330), (cx - 260 + i * 104, by)], fill=(66, 28, 92), width=7)  # folds
    d.polygon([(cx - 130, top + 300), (cx + 130, top + 300), (cx + 60, top + 420), (cx - 60, top + 420)], fill=(36, 12, 52))   # mantle shadow
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
        img = cloaked(img, W // 2, int(2700 - (2700 - 1880) * e), v); d = ImageDraw.Draw(img)
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
    boss = rim(scaled(BOSS, 8), ROSE if t >= T["what"] else LIME, 4)   # v7: his rim turns rose the moment she answers; he is in love
    by_ = 1580 - int((6 + lvl * 6) * abs(math.sin(u * (6 + lvl * 3)))); paste_c(img, boss, 220, by_)

    shown = [x for x in LINES if t >= x[0]]
    him = [x for x in shown if x[1] == "him"]; her = [x for x in shown if x[1] == "her"]
    if him:
        if him[-1][0] in T["beg"] and t < T["what"] + .6:  # the three pleases stack
            for i, x in enumerate([h for h in him if h[0] in T["beg"]]):
                bubble(img, SAFE_L + 12 + i * 24, 450 + i * 100, x[2], max(8, int(x[3] * min(1, pop(t, x[0], .15) or .01))), tail=(230, 1130))
        else:
            x = him[-1]; bubble(img, SAFE_L + 12, 450, x[2], max(8, int(x[3] * min(1, pop(t, x[0], .15) or .01))), tail=(230, 1130), maxw=470)
    img = vhs(img, t, "HOW IT STARTED"); d = ImageDraw.Draw(img)
    if t >= T["what"]:   # v7: he is in love. Drawn after the tape look so the pink stays pink: hearts drift from him to her, rose glints in the aviators, blush
        for i in range(10):
            ph = (u * .45 + i * .31) % 1.0; hx = 260 + int(ph * 520) + int(30 * math.sin(u * 3 + i)); hy = int(1200 - ph * 560 - 40 * math.sin(ph * 3.14)); hs = 14 + (i % 3) * 6
            daily._heart(d, hx, hy, hs, (255, 110, 165) if i % 2 else (255, 165, 200))
        for gx in (190, 250): d.ellipse([gx - 9, by_ - 312, gx + 9, by_ - 294], fill=(255, 130, 185)); d.point((gx - 3, by_ - 307), fill=(255, 255, 255))   # rose glints in the aviators
        d.ellipse([140, by_ - 266, 192, by_ - 246], fill=(255, 120, 150)); d.ellipse([252, by_ - 266, 304, by_ - 246], fill=(255, 120, 150))   # blush
    if her:  # her bubble is drawn after the tape look so the pink stays pink
        x = her[-1]; sz = max(8, int(x[3] * min(1, pop(t, x[0], .15) or .01)))
        y1 = bubble(img, 600, 600, x[2], sz, col=(255, 182, 210), bg=(120, 30, 70), tail=(840, 1000), maxw=350)
        d = ImageDraw.Draw(img); hx, hy = 600 + 24, y1 - 10
        d.ellipse([hx, hy - 10, hx + 12, hy + 2], fill=(255, 90, 140)); d.ellipse([hx + 10, hy - 10, hx + 22, hy + 2], fill=(255, 90, 140)); d.polygon([(hx, hy - 2), (hx + 22, hy - 2), (hx + 11, hy + 12)], fill=(255, 90, 140))
    d = ImageDraw.Draw(img)
    d.text((SAFE_L + 12, 1440), "THE BOSS  vs.  THE REAL BOSS", font=fit("THE BOSS  vs.  THE REAL BOSS", SAFE_R - SAFE_L - 24, 40, wdth=110, wght=900), fill=(255, 240, 200), anchor="ls")
    return img
def hurl(d, img, s_, y, col, t, t0, start=150):
    """A line thrown at the viewer: starts huge and blurry from beyond the screen, slams to size with a trail and a flash."""
    u = t - t0
    if u < 0: return img
    k = min(1, u / .22); e = 1 - (1 - k) ** 3; sc = 1 + 2.6 * (1 - e); a = min(1, u / .08)
    f0 = fit(s_, SAFE_R - SAFE_L, start, wdth=125, wght=900)
    for g, ga in ((1.9, .12), (1.45, .22), (1.15, .35)):   # the trail
        if k < 1:
            f = archivo(int(f0.size * min(sc * g, 4.5)), 125, 900); d.text((SAFE_L + 12 - int((sc * g - 1) * 180), y + int((sc * g - 1) * 60)), s_, font=f, fill=bl(col, ga * (1 - k)), anchor="ls")
    f = archivo(int(f0.size * sc), 125, 900)
    d.text((SAFE_L + 12 - int((sc - 1) * 180), y + int((sc - 1) * 60)), s_, font=f, fill=bl(col, a), anchor="ls")
    if k >= 1 and u < .9: d.text((SAFE_L + 12, y), s_, font=f0, fill=col, anchor="ls")
    return img
def dash_bg(d, u, seed):
    """Procedural dashboards and charts flipping past (illustrations: no axis numbers), plus tally marks piling up: iteration after iteration."""
    r = random.Random(int(u * 6) + seed)
    for p in range(4):
        x0 = SAFE_L + (p % 2) * 420; y0 = 1190 + (p // 2) * 196; x1, y1 = x0 + 380, y0 + 180
        d.rectangle([x0, y0, x1, y1], fill=(10, 12, 10), outline=(40, 46, 30), width=2)
        kind = r.randint(0, 2)
        if kind == 0:
            pts = [(x0 + 16 + i * (x1 - x0 - 32) / 11, y1 - 20 - r.randint(0, 120)) for i in range(12)]; d.line(pts, fill=bl(LIME, .8), width=4)
        elif kind == 1:
            for i in range(9): hh = r.randint(10, 130); d.rectangle([x0 + 16 + i * 40, y1 - 16 - hh, x0 + 44 + i * 40, y1 - 16], fill=bl(LIME if r.random() > .4 else ORANGE, .8))
        else:
            for i in range(4): d.rounded_rectangle([x0 + 16, y0 + 16 + i * 40, x0 + 16 + r.randint(80, 330), y0 + 44 + i * 40], radius=6, fill=bl(INK, .35))
    n = int(u * 46)   # tally marks
    for i in range(min(n, 240)):
        g, j = divmod(i, 5); gx = SAFE_L + 12 + (g % 12) * 70; gy = 1600 + (g // 12) * 56
        if j < 4: d.line([(gx + j * 12, gy), (gx + j * 12, gy + 40)], fill=bl(INK, .7), width=4)
        else: d.line([(gx - 6, gy + 34), (gx + 44, gy + 6)], fill=bl(LIME, .9), width=4)
def sc_biz(t):
    u = t - T["biz"]; img = Image.new("RGB", (W, H), BLACK); d = ImageDraw.Draw(img)
    if t < T["care"]:
        kicker(d, "BACK TO BUSINESS")
        rows = [("REAL TRADES.", INK), ("REAL MONEY.", LIME), ("EVERY NUMBER CHECKED.", INK), ("EVERY POST AUDITED.", INK)]
        y = 600
        for (s_, c), tb in zip(rows, T["biz_lines"]):
            img = hurl(d, img, s_, y, c, t, tb, start=170 if "REAL" in s_ else 120); y += 230 if "REAL" in s_ else 170
        hit = [tb for tb in T["biz_lines"] if 0 <= t - tb < .12]
        if hit: img = Image.blend(img, Image.new("RGB", (W, H), (255, 255, 255)), .6 * (1 - (t - hit[0]) / .12))
        if any(0 <= t - tb < .35 for tb in T["biz_lines"]): img = shift(img, *shake(t, 22))
        return img
    if t < T["power"]:
        v = t - T["care"]; kicker(d, "A PASSION PROJECT")
        dash_bg(d, v, 3)
        lines = [("HUNDREDS OF ITERATIONS.", INK), ("DASHBOARDS. RULES. PIXELS.", INK), ("POWERED BY AI.", LIME), ("MADE BY A HUMAN WHO LOVES THIS.", ROSE)]
        y = 500
        for (s_, c), tb in zip(lines, T["care_lines"]):
            if t >= tb: slam(d, s_, y, c, t, tb, start=96)
            y += 124
        if t >= T["yolo"]:
            k = min(1, pop(t, T["yolo"], .2)); d.text((SAFE_L + 12, 975), "WE ARE", font=archivo(64, 125, 900), fill=INK, anchor="ls")
            stamp(d, (SAFE_L + SAFE_R) // 2 + 20, 1095, "NOT YOLOING.", (255, 92, 70), k, size=96, ang=-6)
            if t - T["yolo"] < .12: img = Image.blend(img, Image.new("RGB", (W, H), (255, 60, 40)), .5 * (1 - (t - T["yolo"]) / .12))
            if t - T["yolo"] < .3: img = shift(img, *shake(t, 16))
        return img
    if t < T["title"]:
        v = t - T["power"]; kicker(d, "A PASSION PROJECT")
        cone = Image.new("L", (W, H), 0); ImageDraw.Draw(cone).polygon([(W // 2 - 80, 0), (W // 2 + 80, 0), (W // 2 + 470, 1860), (W // 2 - 470, 1860)], fill=int(120 * min(1, v / .35)))
        img = Image.composite(Image.new("RGB", (W, H), (70, 78, 44)), img, cone.filter(ImageFilter.GaussianBlur(40))); d = ImageDraw.Draw(img)
        slam(d, "WE TRADE", 560, INK, t, T["power"] + .05, start=190)
        slam(d, "WITH THE", 740, INK, t, T["power"] + .2, start=190)
        slam(d, "POWER OF AI.", 940, LIME, t, T["power"] + .4, start=190)
        e = 1 - (1 - min(1, v / .9)) ** 3; by = int(2700 - (2700 - 1880) * e); sp = rim(scaled(BOSS, 13), LIME, 6)
        paste_c(img, sp, W // 2, by); d = ImageDraw.Draw(img)
        g = t - T["glare"]   # anime glare: a white sheen sweeps the aviators, then a four-point sparkle
        if 0 <= g < .8:
            gy = by - int(sp.height * .69); lw = int(sp.width * .34)
            sweep = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sweep); sx = W // 2 - lw - 60 + int((2 * lw + 120) * min(1, g / .45))
            sd.polygon([(sx, gy - 34), (sx + 40, gy - 34), (sx + 10, gy + 34), (sx - 30, gy + 34)], fill=(255, 255, 255, 230))
            lens = Image.new("L", (W, H), 0); ImageDraw.Draw(lens).rectangle([W // 2 - lw, gy - 36, W // 2 + lw, gy + 36], fill=255)
            sweep.putalpha(ImageChops.multiply(sweep.split()[3], lens)); img = Image.alpha_composite(img.convert("RGBA"), sweep).convert("RGB"); d = ImageDraw.Draw(img)
            if g > .3:
                r_ = int(110 * max(0, 1 - abs(g - .5) / .3)); gx = W // 2 + int(sp.width * .12)
                if r_ > 0:
                    d.polygon([(gx, gy - r_), (gx + 14, gy - 14), (gx + r_, gy), (gx + 14, gy + 14), (gx, gy + r_), (gx - 14, gy + 14), (gx - r_, gy), (gx - 14, gy - 14)], fill=(255, 255, 255))
                    d.polygon([(gx, gy - r_ // 2), (gx + 8, gy - 8), (gx + r_ // 2, gy), (gx + 8, gy + 8), (gx, gy + r_ // 2), (gx - 8, gy + 8), (gx - r_ // 2, gy), (gx - 8, gy - 8)], fill=LIME)
            if g < .1: img = Image.blend(img, Image.new("RGB", (W, H), (255, 255, 255)), .4 * (1 - g / .1))
        return img
    v = t - T["title"]
    kicker(d, "ROUNDING ERROR CAPITAL")
    a = fade(v, 0, .2)
    d.text((SAFE_L + 12, 560), "OPTIONS,", font=fit("OPTIONS,", SAFE_R - SAFE_L, 160, wdth=125, wght=900), fill=bl(INK, a), anchor="ls")
    d.text((SAFE_L + 12, 720), "EXPLAINED BY", font=fit("EXPLAINED BY", SAFE_R - SAFE_L, 160, wdth=125, wght=900), fill=bl(INK, a), anchor="ls")
    slam(d, "THE BOTS THAT TRADE THEM.", 860, LIME, t, T["title"] + .35, start=120)
    paste_c(img, scaled(BOSS, 7), W - 150, 1780, alpha=0.10)  # Easter egg: the boss at 10%, as always
    lineup(img, W // 2 - 60, 1780, 4, t=t, u=v)
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
    lineup(img, W // 2, 1420, 4, t=1.3, u=1.3); paste_c(img, scaled(BOSS, 6), W - 120, 1420, alpha=0.10)
    nfa(img).save(path, quality=92); return path
def build(out_mp4, cover_jpg, workdir):
    global COVER_IMG
    if not os.path.exists(cover_jpg): make_cover(cover_jpg)
    COVER_IMG = Image.open(cover_jpg).convert("RGB").resize((W, H))
    wav = os.path.join(workdir, "trailer2.wav"); SCORE.render(wav, T)
    n = int(T["end"] * FPS)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "slow", "-crf", "17", "-tune", "animation",
        "-c:a", "aac", "-b:a", "192k", "-af", "loudnorm=I=-14:TP=-1.5", "-shortest", "-movflags", "+faststart", out_mp4], stdin=subprocess.PIPE)
    for i in range(n): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); return out_mp4
if __name__ == "__main__":
    print(build(sys.argv[1], sys.argv[2], sys.argv[3]))
