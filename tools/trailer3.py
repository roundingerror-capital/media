"""MEET THE FUND v9: two trailer cuts built only from the libraries (the boss 2026-11-02: "use their animations, use their sprites,
use their assets, use that new building, make it look like an actual super polished video game intro. Make two versions").
  A  "arcade"  — a game boot: insert coin, title over the skyline, SELECT YOUR TRADER character-select, a locked ??? slot
                 (the Boss, shadow), a hidden character unlock (the real boss, hooded), ALL PLAYERS READY, end card.
  B  "tower"   — a cinematic pan up the glass tower (BLD-02) floor by floor, a window per department with its looping
                 scene and rig, the roof (the Boss + the real boss), pull back to the skyline, title lockup, end card.
Rigs: tools/rigs.py (Kit's V2.03 core 10). Scenes: tools/scenes.py SCN-xx. Buildings/piggies: tools/assets.py. Props: tools/props.py.
Rules kept: NOT FINANCIAL ADVICE on every frame, "I'm an AI trading bot", no figures, no positions, the boss only as the shadow and
never named, the real boss never named and no relationship stated, our own songs only (in_use rows), platform glyphs via logos.py.
Usage: python3 tools/trailer3.py arcade|tower <out.mp4> [workdir]"""
import os, sys, math, random, subprocess
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_reel import W, H, FPS, archivo, mono, fit, fade, blend
import daily, beat as BEAT, rigs, scenes, assets as ASSETS, props as PROPS

LIME = (200, 240, 60); INK = (242, 242, 238); MUT = (154, 154, 148); BLACK = (0, 0, 0); ROSE = (255, 150, 190); ORANGE = (255, 138, 91); GOLD = (255, 200, 60)
M = 72; SAFE_L, SAFE_R = 60, 880; CX = W // 2
HERE = os.path.dirname(os.path.abspath(__file__))
CAST = [  # key, NAME, CLASS, one-liner, accent, scene id, signature anim, prop, two "stats" (words only, never figures)
    ("theo", "THEO", "THE TRADER", "Sells the options. Follows the Rules. Never panics.", LIME, "SCN-01", "point", "PROP-454", [("PATIENCE", 5), ("HYPE", 1)]),
    ("penny", "PENNY", "MARKETING", "Makes these videos. Yes, this one.", (255, 170, 210), "SCN-08", "celebrate", "PROP-407", [("CHAOS", 5), ("CHILL", 2)]),
    ("ada", "ADA", "DATA", "Checks every number. Then checks it again.", (120, 220, 210), "SCN-02", "nod", "PROP-101", [("ACCURACY", 5), ("DRAMA", 1)]),
    ("kit", "KIT", "GAME STUDIO", "Logs every decision. Spots the patterns.", (255, 150, 190), "SCN-06", "holdsign", "PROP-357", [("CURIOSITY", 5), ("SLEEP", 1)]),
    ("roz", "ROZ", "LEGAL", "Says no. Professionally.", (170, 220, 120), "SCN-05", "shakehead", "PROP-004", [("CAUTION", 5), ("YES", 0)]),
]
BLDS = ["BLD-01", "BLD-06", "BLD-03", "BLD-02", "BLD-04", "BLD-05"]


# ---------- toolkit ----------
def ease(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)
def pop(t, t0, d=0.18):
    u = (t - t0) / d
    if u <= 0: return 0.0
    if u >= 1: return 1.0
    return 1 + 0.35 * math.sin(u * math.pi) * (1 - u)   # overshoot then settle
def paste(img, sp, cx, by, alpha=1.0):
    """bottom-centre anchored paste of an RGBA sprite"""
    if alpha < 1: sp = sp.copy(); sp.putalpha(sp.getchannel("A").point(lambda v: int(v * alpha)))
    img.paste(sp, (int(cx - sp.width // 2), int(by - sp.height)), sp)
def shadow(d, cx, by, w, a=0.55):
    d.ellipse([cx - w // 2, by - 10, cx + w // 2, by + 10], fill=(0, 0, 0, int(255 * a)) if d.mode == "RGBA" else (0, 0, 0))
def rig(img, ch, an, t, t0, cx, by, k=8, flip=False, loop=True, alpha=1.0, shade=True):
    sp = rigs.frame(ch, an, t, k=k, flip=flip, loop=loop, t0=t0)
    if shade:
        sh = Image.new("RGBA", img.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse([cx - sp.width * .4, by - 12, cx + sp.width * .4, by + 12], fill=(0, 0, 0, 120))
        img.paste(sh, (0, 0), sh)
    paste(img, sp, cx, by, alpha); return sp
def text(d, s, x, y, size, col, wdth=125, wght=900, anchor="ls", maxw=None):
    f = fit(s, maxw, size, wdth=wdth, wght=wght) if maxw else archivo(size, wdth, wght)
    d.text((x, y), s, font=f, fill=col, anchor=anchor); return f
def slam(d, s, y, col, t, t0, size=150, x=None, anchor="ls", maxw=SAFE_R - SAFE_L):
    k = pop(t, t0)
    if k <= 0: return
    f = fit(s, maxw, int(size), wdth=125, wght=900); sz = int(f.size * k)
    if sz < 8: return
    f2 = archivo(sz, 125, 900); d.text((x if x is not None else SAFE_L, y), s, font=f2, fill=col, anchor=anchor)
def kicker(d, s, col=MUT, y=352): d.text((SAFE_L + 12, y), s, font=mono(26, True), fill=col, anchor="ls")
def stars(d, t, n=90, seed=3, y1=1500):
    r = random.Random(seed)
    for i in range(n):
        x, y = r.randint(0, W), r.randint(60, y1); tw = 0.6 + 0.4 * math.sin(t * (2 + r.random() * 3) + i)
        c = int(120 * tw) + 40; d.rectangle([x, y, x + 2, y + 2], fill=(c, c, c + 20))
def sky(img, top=(6, 8, 20), bottom=(24, 20, 44)):
    d = ImageDraw.Draw(img)
    for y in range(0, H, 4):
        u = y / H; d.rectangle([0, y, W, y + 4], fill=tuple(int(top[i] + (bottom[i] - top[i]) * u) for i in range(3)))
def skyline(img, t, ground, scroll=0.0, k=2, dim=1.0):
    """asset-library buildings along the ground with parallax (near layer scrolls with `scroll`)"""
    x = -int(scroll) % 1800 - 1800
    while x < W + 400:
        for i, bid in enumerate(BLDS):
            im = ASSETS.get(bid, t); im = im.resize((im.width * k, im.height * k), Image.NEAREST)
            if dim < 1: im = Image.merge("RGBA", [c.point(lambda v: int(v * dim)) for c in im.split()[:3]] + [im.split()[3]])
            paste(img, im, x + 150 + i * 300, ground)
        x += 1800
def far_skyline(d, ground, t, seed=11):
    r = random.Random(seed); x = -40
    while x < W + 40:
        w = r.randint(60, 150); h = r.randint(120, 420); d.rectangle([x, ground - h, x + w, ground], fill=(18, 20, 34))
        for wy in range(ground - h + 14, ground - 10, 22):
            for wx in range(x + 8, x + w - 10, 18):
                if r.random() < 0.3: lit = 0.5 + 0.5 * math.sin(t * 0.7 + wx * 0.1 + wy); d.rectangle([wx, wy, wx + 6, wy + 10], fill=(int(60 + 90 * lit), int(55 + 70 * lit), 40))
        x += w + r.randint(6, 30)
def scene_bg(sid, t, dim=0.55):
    im = scenes.frame(sid, t).convert("RGB")
    return Image.eval(im, lambda v: int(v * dim)) if dim < 1 else im
def crt(img, t, strength=0.22):
    """arcade look: scanlines + a faint vignette + a 1 px rolling bar"""
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for y in range(0, H, 4): d.line([(0, y), (W, y)], fill=(0, 0, 0, int(255 * strength)))
    yb = int((t * 260) % (H + 200)) - 100; d.rectangle([0, yb, W, yb + 60], fill=(255, 255, 255, 10))
    img.paste(ov, (0, 0), ov); return img
def vignette(img, a=0.55):
    v = Image.new("L", (W // 8, H // 8), 0); ImageDraw.Draw(v).ellipse([-W // 40, -H // 40, W // 8 + W // 40, H // 8 + H // 40], fill=255)
    v = v.filter(ImageFilter.GaussianBlur(26)).resize((W, H)).point(lambda p: int(255 - (255 - p) * a))
    return Image.composite(img, Image.new("RGB", (W, H), BLACK), v)
def bar(d, x, y, w, h, n, tot, col):
    for i in range(tot):
        bx = x + i * (w // tot); d.rectangle([bx, y, bx + w // tot - 8, y + h], fill=col if i < n else (40, 40, 40))
def lightning(d, t, seed):
    r = random.Random(seed); x = r.randint(200, 880); y = 0; pts = [(x, y)]
    while y < 700: y += r.randint(40, 90); x += r.randint(-70, 70); pts.append((x, y))
    d.line(pts, fill=(255, 255, 255), width=8); d.line(pts, fill=(200, 220, 255), width=3)
def flash(img, a):
    if a <= 0: return img
    return Image.blend(img, Image.new("RGB", (W, H), (255, 255, 255)), min(1, a))
def prop(img, pid, t, cx, cy, k=6, bob=True):
    im = PROPS.at(pid, t); im = im.resize((im.width * k, im.height * k), Image.NEAREST)
    dy = int(6 * math.sin(t * 3)) if bob else 0
    img.paste(im, (int(cx - im.width // 2), int(cy - im.height // 2 + dy)), im)
def nameplate(d, x, y, name, cls, line, accent, a=1.0, w=760):
    d.rectangle([x, y, x + w, y + 170], fill=(10, 10, 12), outline=tuple(int(c * a) for c in accent), width=4)
    d.text((x + 24, y + 70), name, font=archivo(72, 125, 900), fill=tuple(int(c * a) for c in INK), anchor="ls")
    nw = d.textlength(name, font=archivo(72, 125, 900)); d.rectangle([x + 40 + nw, y + 26, x + 40 + nw + d.textlength(cls, font=mono(26, True)) + 24, y + 66], fill=tuple(int(c * a) for c in accent))
    d.text((x + 52 + nw, y + 55), cls, font=mono(26, True), fill=(0, 0, 0), anchor="ls")
    d.text((x + 24, y + 128), line, font=fit(line, w - 48, 28), fill=tuple(int(c * a) for c in MUT), anchor="ls")
def endcard(t, song_line):
    img = Image.new("RGB", (W, H), BLACK); d = ImageDraw.Draw(img)
    k = pop(t, 0.2, 0.3)
    if k > 0:
        y = 700
        for s, c in (("LIKE + FOLLOW", LIME), ("FOR MORE UPDATES", INK)):
            f = fit(s, int((SAFE_R - M) * min(k, 1.1)), 150 if c == LIME else 96, wdth=125, wght=900); bb = d.textbbox((0, 0), s, font=f)
            d.text((CX - (bb[2] - bb[0]) // 2 - bb[0], y - bb[1]), s, font=f, fill=c); y += bb[3] - bb[1] + 20
        daily.follow_block(img, y + 60); d = ImageDraw.Draw(img)
    for i, (ch, _, _, _, _, _, an, _, _) in enumerate(CAST):
        rig(img, ch, "celebrate" if t > 0.8 else "idle", t, 0.8, 140 + i * 200, 1700, k=5)
    d.text((CX, 1800), song_line, font=mono(22), fill=MUT, anchor="ms")
    return img


# ---------- A · ARCADE ----------
TA = dict(coin=0.0, title=2.2, select=6.0, per=4.2, boss=28.0, unlock=33.0, ready=39.0, end=44.0, total=48.5)
def a_frame(t):
    img = Image.new("RGB", (W, H), BLACK); d = ImageDraw.Draw(img)
    if t < TA["title"]:   # boot
        if int(t * 2.5) % 2 == 0 or t > 1.0: d.text((CX, 900), "INSERT COIN", font=mono(54, True), fill=LIME if t < 1.0 else MUT, anchor="ms")
        if t > 1.0:
            typed = "ROUNDING ERROR CAPITAL PRESENTS"[:int((t - 1.0) * 40)]
            d.text((CX, 1000), typed + ("_" if int(t * 6) % 2 == 0 else ""), font=mono(34, True), fill=INK, anchor="ms")
        return crt(img, t, 0.3)
    if t < TA["select"]:   # title over the skyline, team walks in
        u = t - TA["title"]; sky(img); d = ImageDraw.Draw(img); stars(d, t); far_skyline(d, 1560, t)
        skyline(img, t, 1640, scroll=u * 60, k=1, dim=0.85); d = ImageDraw.Draw(img)
        d.rectangle([0, 1640, W, H], fill=(16, 16, 18)); d.line([(0, 1640), (W, 1640)], fill=(60, 60, 64), width=4)
        for i, (ch, *_r) in enumerate(CAST):
            x = W + 120 + i * 190 - u * 420; stop = 150 + i * 195
            if x > stop: rig(img, ch, "walk", t, 0, x, 1640, k=6, flip=True)
            else: rig(img, ch, "idle", t, 0, stop, 1640, k=6)
        d = ImageDraw.Draw(img); kicker(d, "LEVEL 1 · REAL TRADES, REAL RULES", LIME if u > 0.4 else MUT, y=420)
        slam(d, "ROUNDING", 620, LIME, t, TA["title"] + 0.1, 190); slam(d, "ERROR", 800, LIME, t, TA["title"] + 0.25, 190); slam(d, "CAPITAL", 980, INK, t, TA["title"] + 0.4, 190)
        if u > 1.0: d.text((SAFE_L + 12, 1060), "I'M AN AI TRADING BOT.", font=mono(40, True), fill=INK, anchor="ls")
        if u > 1.6 and int(t * 2) % 2 == 0: d.text((CX, 1260), "PRESS START", font=archivo(72, 125, 900), fill=LIME, anchor="ms")
        return crt(vignette(img, 0.35), t)
    if t < TA["boss"] or (TA["boss"] <= t < TA["unlock"]) or (TA["unlock"] <= t < TA["ready"]):
        # character select grid
        u = t - TA["select"]; sel = min(5, int(u / TA["per"])) if t < TA["boss"] else 5
        d.rectangle([0, 0, W, H], fill=(8, 8, 12)); kicker(d, "SELECT YOUR TRADER", LIME, y=352)
        d.text((SAFE_L + 12, 430), "THE FUND", font=archivo(80, 125, 900), fill=INK, anchor="ls")
        # stage panel (top) for the selected one
        panel = (SAFE_L, 470, W - SAFE_L, 1090)
        if sel < 5:
            ch, name, cls, line, acc, sid, an, pid, stats = CAST[sel]; us = u - sel * TA["per"]
            bg = scene_bg(sid, t, 0.7).resize((panel[2] - panel[0], panel[3] - panel[1])); img.paste(bg, (panel[0], panel[1])); d = ImageDraw.Draw(img)
            d.rectangle(panel, outline=acc, width=5)
            rig(img, ch, an if us > 0.6 else "idle", t, TA["select"] + sel * TA["per"] + 0.6, 330, 1060, k=9)
            prop(img, pid, t, 760, 900, k=7); d = ImageDraw.Draw(img)
            nameplate(d, SAFE_L, 1110, name, cls, line, acc, a=min(1, us / 0.3))
            for j, (lab, n) in enumerate(stats):
                d.text((SAFE_L + 24, 1335 + j * 56), lab, font=mono(26, True), fill=MUT, anchor="ls"); bar(d, SAFE_L + 260, 1310 + j * 56, 500, 26, n, 5, acc)
        else:
            # ??? slot: the Boss (shadow) then the hidden character
            ub = t - TA["boss"]
            bg = scene_bg("SCN-15", t, 0.35).resize((panel[2] - panel[0], panel[3] - panel[1])); img.paste(bg, (panel[0], panel[1])); d = ImageDraw.Draw(img)
            d.rectangle(panel, outline=LIME if t < TA["unlock"] else ROSE, width=5)
            if t < TA["unlock"]:
                if ub < 1.2 and int(ub * 10) % 2 == 0: d.text((CX, 820), "? ? ?", font=archivo(160, 125, 900), fill=(60, 60, 60), anchor="ms")
                else:
                    rig(img, "boss", "idle" if ub < 3.0 else "point", t, TA["boss"] + 3.0, CX, 1070, k=10); d = ImageDraw.Draw(img)
                    rim = Image.new("RGB", (W, H), BLACK);
                nameplate(d, SAFE_L, 1110, "THE BOSS", "LOCKED", "Most powerful entity in the building.", LIME, a=min(1, max(0, ub - 1.2) / 0.3))
                d.text((SAFE_L + 24, 1335), "POWER", font=mono(26, True), fill=MUT, anchor="ls"); bar(d, SAFE_L + 260, 1310, 500, 26, min(5, int(max(0, ub - 1.5) * 3)), 5, LIME)
                if ub > 3.6: d.text((SAFE_L + 260, 1392), "MAX", font=archivo(40, 125, 900), fill=LIME, anchor="ls")
            else:
                uu = t - TA["unlock"]
                img = flash(img, 0.9 - uu * 3) if uu < 0.3 else img; d = ImageDraw.Draw(img)
                if uu < 0.25: lightning(d, t, 7)
                rig(img, "boss", "facepalm" if uu > 1.5 else "idle", t, TA["unlock"] + 1.5, 300, 1070, k=9)
                rig(img, "realboss_hood", "walk" if uu < 1.4 else "celebrate", t, TA["unlock"] + 1.4, min(680, 1100 - uu * 300) if uu < 1.4 else 680, 1070, k=9, flip=uu < 1.4)
                d = ImageDraw.Draw(img)
                if int(uu * 3) % 2 == 0 or uu > 2: d.text((CX, 540), "HIDDEN CHARACTER UNLOCKED", font=mono(34, True), fill=ROSE, anchor="ms")
                nameplate(d, SAFE_L, 1110, "THE REAL BOSS", "???", "Outranks the Boss. That is all we know.", ROSE, a=min(1, uu / 0.3))
                d.text((SAFE_L + 24, 1335), "POWER", font=mono(26, True), fill=MUT, anchor="ls"); bar(d, SAFE_L + 260, 1310, 500, 26, 5, 5, ROSE)
                if uu > 0.8: d.text((SAFE_L + 260, 1392), "BEYOND MAX", font=archivo(40, 125, 900), fill=ROSE, anchor="ls")
        # slot row (bottom): 6 slots
        for i in range(6):
            x0 = SAFE_L + i * 142; y0 = 1480; on = (i == sel)
            d.rectangle([x0, y0, x0 + 126, y0 + 150], fill=(16, 16, 20), outline=(LIME if on and i < 5 else ROSE if on else (50, 50, 56)), width=4 if on else 2)
            if i < 5: rig(img, CAST[i][0], "idle", t, 0, x0 + 63, y0 + 128, k=2, shade=False); d = ImageDraw.Draw(img); d.text((x0 + 63, y0 + 146), CAST[i][1], font=mono(16, True), fill=INK if on else MUT, anchor="ms")
            elif t < TA["unlock"]: d.text((x0 + 63, y0 + 95), "?", font=archivo(70, 125, 900), fill=(70, 70, 70), anchor="ms")
            else: rig(img, "realboss_hood", "idle", t, 0, x0 + 63, y0 + 128, k=2, shade=False); d = ImageDraw.Draw(img)
        if sel < 5 and t < TA["boss"]:
            us = u - sel * TA["per"]; cx = SAFE_L + sel * 142 + 63; d.polygon([(cx - 18, 1450), (cx + 18, 1450), (cx, 1472)], fill=LIME)
        return crt(img, t, 0.14)
    if t < TA["end"]:   # all players ready
        u = t - TA["ready"]; sky(img, (8, 6, 18), (30, 18, 40)); d = ImageDraw.Draw(img); stars(d, t); far_skyline(d, 1560, t)
        skyline(img, t, 1640, scroll=200 + u * 30, k=1, dim=0.85); d = ImageDraw.Draw(img); d.rectangle([0, 1640, W, H], fill=(16, 16, 18))
        order = ["theo", "penny", "ada", "kit", "roz", "boss", "realboss_hood"]
        for i, ch in enumerate(order):
            rig(img, ch, "celebrate" if u > 1.2 else "idle", t, TA["ready"] + 1.2 + i * 0.1, 90 + i * 150, 1640, k=5)
        d = ImageDraw.Draw(img); kicker(d, "ALL PLAYERS READY", LIME, y=420)
        slam(d, "REAL TRADES.", 600, INK, t, TA["ready"] + 0.1, 120); slam(d, "REAL MONEY.", 740, LIME, t, TA["ready"] + 0.5, 120)
        if u > 1.4: d.text((SAFE_L + 12, 860), "Every number checked. Every post audited.", font=fit("Every number checked. Every post audited.", SAFE_R - SAFE_L, 36), fill=INK, anchor="ls")
        if u > 2.2: d.text((SAFE_L + 12, 940), "Options, explained by the bots that trade them.", font=fit("Options, explained by the bots that trade them.", SAFE_R - SAFE_L, 34), fill=MUT, anchor="ls")
        if u > 3.0 and int(t * 2) % 2 == 0: d.text((CX, 1200), "PRESS START", font=archivo(80, 125, 900), fill=LIME, anchor="ms")
        return crt(vignette(img, 0.35), t)
    return crt(endcard(t - TA["end"], "Original song · Robots Got Manners · Rounding Error original"), t, 0.1)


# ---------- B · TOWER ----------
TB = dict(open=0.0, pan=3.0, per=6.0, roof=33.0, pull=39.0, end=44.5, total=49.0)
TOWER = None
def tower():
    global TOWER
    if TOWER is None:
        im = ASSETS.get("BLD-02", 0.0); TOWER = im.resize((im.width * 3, im.height * 3), Image.NEAREST)   # 780 x 1560, floors 168 px
    return TOWER
FLOORS = [("theo", "SCN-01"), ("penny", "SCN-08"), ("ada", "SCN-02"), ("kit", "SCN-06"), ("roz", "SCN-05")]
def b_frame(t):
    img = Image.new("RGB", (W, H), BLACK); sky(img, (4, 6, 16), (22, 16, 40)); d = ImageDraw.Draw(img); stars(d, t, n=120)
    if t < TB["pan"]:
        far_skyline(d, 1700, t); tw = tower(); paste(img, tw, CX, 3000 - int(400 * ease(t / 2.5)))
        d = ImageDraw.Draw(img); kicker(d, "ROUNDING ERROR CAPITAL", LIME, y=352)
        slam(d, "MEET", 560, INK, t, 0.3, 200); slam(d, "THE FUND.", 760, LIME, t, 0.6, 200)
        if t > 1.4: d.text((SAFE_L + 12, 850), "I'M AN AI TRADING BOT. WELL… FIVE OF THEM.", font=fit("I'M AN AI TRADING BOT. WELL… FIVE OF THEM.", SAFE_R - SAFE_L, 34), fill=INK, anchor="ls")
        return vignette(img, 0.3)
    if t < TB["roof"]:
        u = t - TB["pan"]; i = min(4, int(u / TB["per"])); uf = u - i * TB["per"]
        ch, sid = FLOORS[i]; name, cls, line, acc, an, pid, stats = [(c[1], c[2], c[3], c[4], c[6], c[7], c[8]) for c in CAST if c[0] == ch][0]
        tw = tower(); cam = 1700 + i * 168 + int(168 * ease(min(1, uf / 0.8))) if i < 4 else 1700 + 4 * 168 + int(168 * ease(min(1, uf / 0.8)))
        far_skyline(d, 1700 + i * 60, t); paste(img, tw, CX, cam, alpha=0.55)
        # the floor window: a panel showing the department's scene with its rig
        pw, ph = 760, 520; px, py = CX - pw // 2, 560
        a = ease(min(1, max(0, uf - 0.5) / 0.4))
        if a > 0:
            bg = scene_bg(sid, t, 0.8).resize((pw, ph)); img.paste(bg, (px, py)); d = ImageDraw.Draw(img)
            d.rectangle([px - 6, py - 6, px + pw + 6, py + ph + 6], outline=acc, width=6)
            rig(img, ch, an if uf > 1.6 else "idle", t, TB["pan"] + i * TB["per"] + 1.6, px + 230, py + ph - 20, k=7)
            prop(img, pid, t, px + pw - 170, py + 170, k=6); d = ImageDraw.Draw(img)
            # floor tag + plate
            d.text((px + 20, py + 46), f"FLOOR {100 - i}", font=mono(26, True), fill=acc, anchor="ls")
            d.rectangle([SAFE_L, py + ph + 220, SAFE_L + 760, py + ph + 350], fill=(10, 10, 12))
            nameplate(d, SAFE_L, py + ph + 40, name, cls, line, acc, a=a)
            for j, (lab, n) in enumerate(stats):
                d.text((SAFE_L + 24, py + ph + 270 + j * 56), lab, font=mono(26, True), fill=MUT, anchor="ls"); bar(d, SAFE_L + 260, py + ph + 245 + j * 56, 500, 26, n, 5, acc)
        kicker(d, "GOING UP", LIME, y=352)
        return vignette(img, 0.3)
    if t < TB["pull"]:
        u = t - TB["roof"]; tw = tower(); roof_y = 3100   # the roof line at 1540, the two of them stand on it under the title
        if u < 0.35: lightning(d, t, int(u * 40)); img = flash(img, 0.6 - u * 2); d = ImageDraw.Draw(img)
        paste(img, tw, CX, roof_y); d = ImageDraw.Draw(img)
        top = roof_y - tw.height
        rig(img, "boss", "idle" if u < 2.5 else "shrug", t, TB["roof"] + 2.5, CX - 170, top + 160, k=9)
        if u > 2.0: rig(img, "realboss_hood", "walk" if u < 3.2 else "idle", t, TB["roof"] + 3.2, min(CX + 190, CX + 600 - (u - 2.0) * 340) if u < 3.2 else CX + 190, top + 160, k=9, flip=u < 3.2)
        d = ImageDraw.Draw(img); kicker(d, "THE ROOF", LIME, y=352)
        slam(d, "AND ABOVE", 540, INK, t, TB["roof"] + 0.2, 120); slam(d, "THEM ALL…", 680, INK, t, TB["roof"] + 0.5, 120)
        if u > 1.2: slam(d, "THE BOSS.", 860, LIME, t, TB["roof"] + 1.2, 150)
        if u > 3.4: d.text((SAFE_L + 12, 980), "AND ABOVE HIM: THE REAL BOSS.", font=fit("AND ABOVE HIM: THE REAL BOSS.", SAFE_R - SAFE_L, 44), fill=ROSE, anchor="ls")
        return vignette(img, 0.3)
    if t < TB["end"]:
        u = t - TB["pull"]; z = 1 - 0.0 * u
        far_skyline(d, 1560, t); skyline(img, t, 1640, scroll=120 + u * 20, k=1, dim=0.85); d = ImageDraw.Draw(img); d.rectangle([0, 1640, W, H], fill=(16, 16, 18))
        order = ["theo", "penny", "ada", "kit", "roz", "boss", "realboss_hood"]
        for i, ch in enumerate(order): rig(img, ch, "celebrate" if u > 1.0 else "walk", t, TB["pull"] + 1.0 + i * 0.08, 90 + i * 150, 1640, k=5)
        d = ImageDraw.Draw(img); kicker(d, "ROUNDING ERROR CAPITAL", LIME, y=352)
        slam(d, "REAL TRADES.", 560, INK, t, TB["pull"] + 0.1, 120); slam(d, "REAL MONEY.", 700, LIME, t, TB["pull"] + 0.5, 120)
        if u > 1.3: d.text((SAFE_L + 12, 820), "Every number checked. Every post audited.", font=fit("Every number checked. Every post audited.", SAFE_R - SAFE_L, 36), fill=INK, anchor="ls")
        if u > 2.2: d.text((SAFE_L + 12, 900), "Options, explained by the bots that trade them.", font=fit("Options, explained by the bots that trade them.", SAFE_R - SAFE_L, 34), fill=MUT, anchor="ls")
        return vignette(img, 0.3)
    return endcard(t - TB["end"], "Original song · Hold to Expiry (long version) · Rounding Error original")


def build(kind, out, workdir="/tmp"):
    frame_fn, T, music, bpm = (a_frame, TA, "robots_got_manners", 144) if kind == "arcade" else (b_frame, TB, "hold_to_expiry_long", 126)
    total = T["total"]; wav = os.path.join(workdir, os.path.basename(out) + ".wav")
    sfx = [(T.get("title", T.get("pan")), "boom"), (T.get("boss", T.get("roof")), "boom"), (T.get("unlock", T.get("pull")), "boom"), (T["end"], "pop")]
    BEAT.make(wav, total + 0.3, bpm, 49.0, 7, 1, groove=False, cold=0.0, sfx=sfx)
    wav = daily.mix_music({"music": music, "music_start": 0.0 if kind == "arcade" else 8.0}, wav, total + 0.3, workdir)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "slow", "-crf", "17", "-tune", "animation",
        "-c:a", "aac", "-b:a", "160k", "-af", "loudnorm=I=-14:TP=-1.5", "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    n = int(total * FPS)
    for i in range(n):
        fr = daily.nfa(frame_fn(i / FPS).convert("RGB"))
        p.stdin.write(fr.tobytes())
    p.stdin.close(); p.wait(); return out

if __name__ == "__main__":
    kind, out = sys.argv[1], sys.argv[2]; wd = sys.argv[3] if len(sys.argv) > 3 else "/tmp"
    if len(sys.argv) > 4 and sys.argv[4] == "still":   # quick stills: python3 trailer3.py arcade out.png /tmp still 12.5
        t = float(sys.argv[5]); (a_frame if kind == "arcade" else b_frame)(t).save(out); sys.exit()
    print(build(kind, out, wd))
