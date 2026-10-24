"""Channel trailer (2026-10-24): "AI trades it. A human built it." 1080x1920, 30 fps, ~34.5 s.
Real build counts from the Mascot Designs canvas; the boss stays in the shadow realm (10% visible) for his reveal."""
import os, sys, math, random, glob, subprocess, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFilter
from make_reel import W, H, FPS, archivo, mono, fit, fade, blend
import daily, cover as COVER, trailer_score as SCORE
LIME = (200, 240, 60); INK = (242, 242, 238); MUT = (154, 154, 148); BLACK = (0, 0, 0); DIM = (40, 48, 20)
M = 72
def blend(c, a):
    if isinstance(c, str): c = tuple(int(c.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
    return tuple(int(v * max(0, min(1, a))) for v in c)
T = dict(punch=0.6, ai0=1.8, but=7.2, cnt0=8.4, no0=16.4, dark=19.2, reveal=23.0, team=27.4, outro=31.4, end=34.9)
T["counters"] = [8.4, 10.4, 12.4, 14.4]
T["booms"] = [20.8, 21.9, 23.0]
T["glint"] = 24.5
T["stamps"] = [T["no0"] + 0.35 + 0.085 * i for i in range(21)]
SPR = sys.argv[1] if len(sys.argv) > 1 else "spr"
def load(name):
    return Image.open(os.path.join(SPR, name + ".png")).convert("RGBA")
def scaled(im, s):
    return im.resize((im.width * s, im.height * s), Image.NEAREST)
def paste_c(img, sp, cx, by, alpha=1.0):  # centre x, bottom y
    if alpha < 1:
        a = sp.split()[3].point(lambda v: int(v * alpha)); sp = sp.copy(); sp.putalpha(a)
    img.paste(sp, (int(cx - sp.width / 2), int(by - sp.height)), sp)
def text(d, xy, s, size, col, wdth=125, wght=900, anchor="ls"):
    d.text(xy, s, font=archivo(size, wdth, wght), fill=col, anchor=anchor)
def big(d, s, y, col, maxw=W - 2 * M, start=260, wdth=125, anchor="ms", x=W // 2):
    f = fit(s, maxw, start, wdth=wdth, wght=900); d.text((x, y), s, font=f, fill=col, anchor=anchor); return f
def chrome(d, label):
    d.text((M, 120), "≈ Rounding Error", font=archivo(40, 110, 800), fill=INK, anchor="ls")
    d.text((W - M, 120), label, font=mono(24), fill=MUT, anchor="rs")
    d.line([(M, 150), (W - M, 150)], fill=(38, 38, 38), width=2)
    d.text((M, 1816), "@ROUNDINGERROR.CAPITAL", font=mono(22), fill=MUT, anchor="ls")
def pop(t, t0, d=0.18):  # scale-in overshoot 0..1.15..1
    k = (t - t0) / d
    if k <= 0: return 0
    if k >= 1: return 1
    return 1 + 0.15 * math.sin(k * math.pi) if k > .6 else k / .6 * 1.15
# ---------------- assets
THEO, PENNY, ADA, KIT, ROZ, BOSS = (load(n) for n in ("V7TheoGoldenPixel", "V7PennyStormPixel", "V11AdaRiverPixel", "V16KitBlossomPixel", "V19RozBow", "V15BossAllBlack"))
DRAFTS = [load(os.path.basename(p)[:-4]) for p in sorted(glob.glob(os.path.join(SPR, "*.png"))) if "Boss" not in p and "Lineup" not in p]
REJECTS = [load(n) for n in ["V17RozSagePixel", "V17RozJadePixel", "V17RozOlivePixel", "V17RozBoxPixel", "V17RozCounselTurtle", "V17RozSageTurtle",
           "V17RozSliderTurtle", "V17RozSeaTurtle", "V17RozTortoiseTurtle", "V17RozStarTurtle", "V17RozPaintedTurtle", "V17RozRidgebackTurtle",
           "V18RozBlazerTie", "V18RozBlazerBow", "V18RozCardigan", "V18RozTrench", "V18RozSeaBlazer", "V18RozSagePlain", "V19RozPearls", "V19RozPlain", "V19RozPin"]]
rnd = random.Random(8349)
CANDLES = [(rnd.uniform(-1, 1)) for _ in range(40)]
PATHS = []
for k in range(26):
    r = random.Random(k); v = 0; pts = []
    for i in range(30): v += r.gauss(0.01, 0.06); pts.append(v)
    PATHS.append(pts)
NOTES = ["TikTok?", "loop test", "end card", "a turtle", "three-way", "AI TRADING BOT", "Reddit?", "covers!!", "standby x2", "6 PM IG", "faster intro", "story first", "the wall", "lime bow", "$100K?", "ask a question"]
RULES = ["§1 The fund", "§3 The boss's rules", "§4 Orders", "§5 No-fly list", "§7 Sizing", "§8 Covered calls", "§11 Scorecard", "§15 Changing a rule", "§16 Channels", "The firm", "The wall", "No rolls. No buybacks.", "Hold to expiry.", "Not financial advice."]
# ---------------- scenes
def sc_ai(t):
    img = Image.new("RGB", (W, H), BLACK); d = ImageDraw.Draw(img); chrome(d, "CHANNEL TRAILER")
    k = int((t - T["ai0"]) // 1.8); u = (t - T["ai0"]) - k * 1.8
    lines = [("AI", "TRADES OUR", "MONEY."), ("AI", "RUNS THE", "SIMULATIONS."), ("AI", "CHECKS EVERY", "NUMBER.")][min(k, 2)]
    s = pop(t, T["ai0"] + k * 1.8)
    y = 470
    for i, ln in enumerate(lines):
        a = fade(u, .05 + i * .1, .2 + i * .1)
        col = LIME if i == 0 else INK
        f = fit(ln, int((W - 2 * M) * (0.6 if i == 0 else 1)), 300 if i == 0 else 190, wdth=125, wght=900)
        bb = d.textbbox((0, 0), ln, font=f, anchor="ls")
        y += -bb[1] if i else 0
        d.text((M, y), ln, font=f, fill=blend(col, a), anchor="ls"); y += 40
    if k == 0:  # Theo + candles marching
        for i, c in enumerate(CANDLES[:22]):
            x = M + i * 44 - int(u * 60) % 44; h = int(60 + abs(c) * 160); col = LIME if c > 0 else (255, 138, 91)
            d.rectangle([x, 1380 - h, x + 22, 1380], fill=blend(col, .55))
        paste_c(img, scaled(THEO, 9), W // 2 + 150, 1700 - int(12 * abs(math.sin(u * 7))))
    elif k == 1:  # a fan of simulated paths, one lime
        n = min(len(PATHS), int(4 + u * 30))
        for j in range(n):
            pts = PATHS[j]; col = LIME if j == 0 else (70, 70, 70)
            xy = [(M + i * 32, 1350 - p * 500) for i, p in enumerate(pts)]
            d.line(xy, fill=col, width=8 if j == 0 else 3)
        paste_c(img, scaled(KIT, 7), W - 240, 1720 - int(10 * abs(math.sin(u * 6))))
    else:  # Ada and checkmarks raining
        for j in range(14):
            r = random.Random(j); x = r.randint(M, W - M); y0 = (u * 900 + r.randint(0, 900)) % 900 + 950
            d.line([(x, y0), (x + 18, y0 + 18), (x + 50, y0 - 24)], fill=LIME, width=10)
        paste_c(img, scaled(ADA, 9), W // 2, 1720 - int(12 * abs(math.sin(u * 7))))
    return img
def sc_but(t):
    u = t - T["but"]
    img = sc_ai(T["but"] - 0.02)
    if u < 0.4:  # freeze + RGB glitch tear
        r, g, b = img.split(); off = int(30 * (1 - u / .4)) + 6
        img = Image.merge("RGB", (r.transform(img.size, Image.AFFINE, (1, 0, off, 0, 1, 0)), g, b.transform(img.size, Image.AFFINE, (1, 0, -off, 0, 1, 0))))
        d = ImageDraw.Draw(img)
        for i in range(9):
            y = random.Random(i + int(u * 30)).randint(200, 1700); d.rectangle([0, y, W, y + 14], fill=(0, 0, 0))
        return img
    img = Image.new("RGB", (W, H), BLACK); d = ImageDraw.Draw(img)
    a = fade(u, .4, .55)
    big(d, "BUT…", 1060, blend(INK, a), start=420)
    return img
def sc_counter(t):
    k = min(3, int((t - T["cnt0"]) // 2.0)); u = t - T["counters"][k]
    img = Image.new("RGB", (W, H), BLACK); d = ImageDraw.Draw(img); chrome(d, "BEHIND THE BOT")
    if k == 0:  # mascot drafts wall, flickering
        cell = 150; cols = 7
        for i in range(cols * 11):
            r = random.Random(i * 31 + int(t * 12)); sp = DRAFTS[r.randrange(len(DRAFTS))]
            s = max(1, min(cell // max(sp.width, sp.height), 3)); im = scaled(sp, s)
            x = 30 + (i % cols) * cell + cell // 2; y = 190 + (i // cols) * cell + cell
            paste_c(img, im, x, y, alpha=0.28)
    elif k == 1:  # dashboards: panel wireframes flipping versions
        for i in range(12):
            x = M + (i % 3) * 320; y = 220 + (i // 3) * 380
            d.rectangle([x, y, x + 290, y + 340], outline=(60, 60, 60), width=3)
            r = random.Random(i + int(t * 10))
            for j in range(5): d.rectangle([x + 20, y + 50 + j * 56, x + 20 + r.randint(60, 250), y + 80 + j * 56], fill=(40, 40, 40) if j else (70, 90, 30))
            d.text((x + 20, y + 32), f"v{r.randint(1, 200)}", font=mono(22, True), fill=(110, 110, 110), anchor="ls")
    elif k == 2:  # rules scrolling
        for i in range(40):
            y = 200 + i * 52 - int(u * 600) % 52
            d.text((M, y), RULES[(i + int(u * 11)) % len(RULES)], font=mono(34, True), fill=(58, 58, 58), anchor="ls")
    else:  # idea sticky notes popping
        for i, nt in enumerate(NOTES):
            ti = T["counters"][3] + i * .09
            if t < ti: continue
            r = random.Random(i); x = r.randint(M, W - 400); y = r.randint(220, 1500)
            d.rectangle([x, y, x + 330, y + 120], fill=(48, 58, 22)); d.text((x + 20, y + 74), nt, font=archivo(40, 100, 800), fill=(170, 200, 70), anchor="ls")
    val, lab, sub = [("136", "MASCOT DRAFTS", "on our design canvas"), ("200+", "DASHBOARD VERSIONS", "and counting"),
                     ("#938,749*", "RULES EDIT", "this week"), ("#8,349*", "IDEA", "today, probably")][k]
    s = pop(t, T["counters"][k], .22)
    d.rectangle([0, 760, W, 1260], fill=(0, 0, 0))
    f = fit(val, int((W - 2 * M) * s) if s else 1, 380, wdth=125, wght=900) if s else None
    if f: d.text((W // 2, 1060), val, font=f, fill=LIME, anchor="ms")
    a = fade(u, .12, .3)
    d.text((W // 2, 1150), lab, font=archivo(64, 125, 900), fill=blend(INK, a), anchor="ms")
    d.text((W // 2, 1210), sub, font=mono(30, True), fill=blend(MUT, a), anchor="ms")
    if k >= 2: d.text((W // 2, 1700), "*he lost count", font=mono(28, True), fill=blend(MUT, a), anchor="ms")
    return img
def sc_no(t):
    u = t - T["no0"]
    img = Image.new("RGB", (W, H), BLACK); d = ImageDraw.Draw(img); chrome(d, "BEHIND THE BOT")
    d.text((M, 320), "SOMEBODY SAID NO", font=fit("SOMEBODY SAID NO", W - 2 * M, 150, wdth=125, wght=900), fill=INK, anchor="ls")
    d.text((M, 450), "TO 21 TURTLES.", font=fit("TO 21 TURTLES.", W - 2 * M, 150, wdth=125, wght=900), fill=LIME, anchor="ls")
    cols, cell = 6, 160
    for i, sp in enumerate(REJECTS):
        ts = T["stamps"][i]
        if t < ts - .25: continue
        s = max(1, min(cell // max(sp.width, sp.height), 3)); im = scaled(sp, s)
        x = M + 10 + (i % cols) * cell + cell // 2; y = 560 + (i // cols + 1) * (cell + 20)
        paste_c(img, im, x, y, alpha=0.55 if t >= ts else 1.0)
        if t >= ts:
            sz = 1 + max(0, .6 * (1 - (t - ts) / .12))
            f = archivo(int(44 * sz), 110, 900)
            d.text((x, y - cell // 2), "NO", font=f, fill=(255, 92, 70), anchor="mm")
    tf = T["stamps"][-1] + .35
    if t >= tf:
        s = pop(t, tf, .25); fin = scaled(ROZ, 6)
        if s: fin = fin.resize((max(1, int(fin.width * s)), max(1, int(fin.height * s))), Image.NEAREST)
        d.rectangle([0, 1330, W, H], fill=(0, 0, 0))
        paste_c(img, fin, W // 2, 1790)
        d.text((W // 2, 1440), "…AND YES TO ONE.", font=archivo(64, 125, 900), fill=blend(LIME, fade(t, tf, tf + .2)), anchor="ms")
    return img
def boss_layer(scale):
    sp = scaled(BOSS, scale)
    # lime rim light: dilate the silhouette, keep the ring
    a = sp.split()[3]; ring = a.filter(ImageFilter.MaxFilter(5))
    rim = Image.new("RGBA", sp.size, LIME + (0,)); rim.putalpha(ring)
    out = Image.new("RGBA", sp.size, (0, 0, 0, 0)); out.alpha_composite(rim); out.alpha_composite(sp)
    return out
BOSSL = boss_layer(14)
def sc_reveal(t):
    u = t - T["dark"]
    img = Image.new("RGB", (W, H), BLACK); d = ImageDraw.Draw(img)
    if t < T["booms"][0]:
        a = fade(u, .2, .5)
        d.text((W // 2, 820), "AI TRADES IT.", font=archivo(90, 125, 900), fill=blend(INK, a), anchor="ms")
        a2 = fade(u, .9, 1.2)
        d.text((W // 2, 960), "BUT BEHIND EVERY AI…", font=fit("BUT BEHIND EVERY AI…", W - 2 * M, 110, wdth=125, wght=900), fill=blend(INK, a2), anchor="ms")
        return img
    words = [("THERE'S", T["booms"][0]), ("A", T["booms"][1])]
    if t < T["reveal"]:
        y = 760
        for w_, tb in words:
            if t >= tb:
                s = pop(t, tb, .15); f = archivo(int(170 * max(s, .01)), 125, 900)
                d.text((W // 2, y), w_, font=f, fill=INK, anchor="ms")
            y += 220
        return img
    v = t - T["reveal"]
    # spotlight cone from the top
    cone = Image.new("L", (W, H), 0); cd = ImageDraw.Draw(cone)
    op = int(110 * min(1, v / .4))
    cd.polygon([(W // 2 - 70, 0), (W // 2 + 70, 0), (W // 2 + 430, 1760), (W // 2 - 430, 1760)], fill=op)
    cone = cone.filter(ImageFilter.GaussianBlur(40))
    img = Image.composite(Image.new("RGB", (W, H), (60, 66, 40)), img, cone)
    d = ImageDraw.Draw(img)
    d.ellipse([W // 2 - 420, 1720, W // 2 + 420, 1800], fill=(28, 30, 20))
    # MONKEY. slam
    s = pop(t, T["reveal"], .18)
    if s:
        f = fit("MONKEY.", int((W - 2 * M) * s), 360, wdth=125, wght=900)
        d.text((W // 2, 520), "MONKEY.", font=f, fill=LIME, anchor="ms")
    d.text((W // 2, 300), "THERE'S A", font=archivo(110, 125, 900), fill=INK, anchor="ms")
    # the boss rises into the light, still in the shadow realm (sprite is the 10% final)
    rise = min(1, v / 1.2); ease = 1 - (1 - rise) ** 3
    by = int(2400 - (2400 - 1760) * ease)
    shake = (random.Random(int(t * 30)).randint(-6, 6) if v < .25 else 0)
    paste_c(img, BOSSL, W // 2 + shake, by)
    # aviator glint
    g = t - T["glint"]
    if 0 <= g < .5:
        gx = W // 2 + int(BOSSL.width * 0.14); gy = by - int(BOSSL.height * 0.58)
        r = int(70 * (1 - abs(g - .15) / .35)) if g < .5 else 0
        if r > 0:
            d.line([(gx - r, gy), (gx + r, gy)], fill=(255, 255, 255), width=6); d.line([(gx, gy - r), (gx, gy + r)], fill=(255, 255, 255), width=6)
            d.ellipse([gx - 10, gy - 10, gx + 10, gy + 10], fill=(255, 255, 255))
    if t >= T["glint"] + .5:
        a = fade(t, T["glint"] + .5, T["glint"] + .8)
        d.text((W // 2, 1880 - 50), "THE BOSS", font=mono(28, True), fill=blend(MUT, a), anchor="ms")
        # one line, as always
        bx, byy = W // 2 + 250, by - BOSSL.height + 60
        d.rectangle([bx, byy, bx + 290, byy + 80], fill=INK); d.polygon([(bx + 20, byy + 80), (bx + 50, byy + 80), (bx - 10, byy + 110)], fill=INK)
        d.text((bx + 22, byy + 54), "Carry on.", font=mono(36, True), fill=(0, 0, 0), anchor="ls")
    return img
LINEUP = None
def lineup():
    global LINEUP
    if LINEUP is None: LINEUP = load("V20TeamLineup")
    return LINEUP
def sc_team(t):
    u = t - T["team"]
    img = Image.new("RGB", (W, H), BLACK); d = ImageDraw.Draw(img); chrome(d, "ROUNDING ERROR CAPITAL")
    a1 = fade(u, .05, .3); a2 = fade(u, .6, .9)
    d.text((M, 420), "AI TRADES IT.", font=fit("AI TRADES IT.", W - 2 * M, 170, wdth=125, wght=900), fill=blend(INK, a1), anchor="ls")
    d.text((M, 600), "A HUMAN", font=fit("A HUMAN", W - 2 * M, 230, wdth=125, wght=900), fill=blend(LIME, a2), anchor="ls")
    d.text((M, 800), "BUILT IT.", font=fit("BUILT IT.", W - 2 * M, 230, wdth=125, wght=900), fill=blend(LIME, a2), anchor="ls")
    ln = lineup(); s = 3; im = scaled(ln, s)
    off = int((1 - min(1, u / .6)) ** 3 * 600)
    paste_c(img, im, W // 2, 1450 + off)
    a3 = fade(u, 1.4, 1.7)
    d.text((W // 2, 1660), "Real trades. Real money. Real humans behind the bots.", font=mono(30, True), fill=blend(INK, a3), anchor="ms")
    d.text((W // 2, 1710), "Not financial advice.", font=mono(26), fill=blend(MUT, a3), anchor="ms")
    return img
def frame(t):
    if t < T["punch"]: return COVER_IMG
    if t < T["ai0"]: return daily.intro_hook_frame(S, int((t - T["punch"]) * FPS), PTS)
    if t < T["but"]: return sc_ai(t)
    if t < T["cnt0"]: return sc_but(t)
    if t < T["no0"]: return sc_counter(t)
    if t < T["dark"]: return sc_no(t)
    if t < T["team"]: return sc_reveal(t)
    if t < T["outro"]: return sc_team(t)
    return daily.outro_frame(S, t - T["outro"])
S = {"bpm": 140, "hook": "WHO'S BEHIND THE BOT?", "scenes": [(0, 1, "", [("x", INK)], [], [], [], 0)], "positions": []}
PTS = daily.chart_pts("spike", 8349)
COVER_IMG = None
def build(out_mp4, cover_jpg, workdir):
    global COVER_IMG
    COVER_IMG = Image.open(cover_jpg).convert("RGB").resize((W, H))
    wav = os.path.join(workdir, "trailer.wav"); SCORE.render(wav, T)
    n = int(T["end"] * FPS)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "19",
        "-c:a", "aac", "-b:a", "192k", "-af", "loudnorm=I=-14:TP=-1.5", "-shortest", "-movflags", "+faststart", out_mp4], stdin=subprocess.PIPE)
    for i in range(n): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); return out_mp4
if __name__ == "__main__":
    print(build(sys.argv[2], sys.argv[3], sys.argv[4]))
