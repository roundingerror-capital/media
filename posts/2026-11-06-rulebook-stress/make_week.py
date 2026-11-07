"""MY WEEK (the boss 2026-11-06): timeless, no real numbers. Each weekday the boss (shadow chimp, never the real-boss sprites)
lives his week; MEANWHILE the whole fund fights the market as a raid, with only the rulebook as battle cries.
Family per Rules §3 rule 4 (decision 20261106-family-general-1): kids are never drawn, only speech bubbles from off-screen.
No trade-approval claim (Roz 11/6: the boss approves posts, not trades). No numbers anywhere -> no fact sheet.
Art: Kit's 11/6 library (V2_08BossMyWeek, V2_08TheoRaid/AdaRaid/RozRaid, V2_06PennyGear/KitGear, RAID-01..03, FXRAID,
ROOMKITWEEK, ROOM-21..24). Scale: home scenes 1:1 with Kit's rooms at x12 (90x128 crop -> 1080x1536 under a 384 px text band);
raid at x8 (135x240 arena), same as the WoW video. Song: Rules Stay Sober (set_rulebook_stress), 0-40 s.
    python3 make_week.py <out.mp4> | --panels <sheet.png> | --cover <out.jpg>"""
import os, sys, math, subprocess, random
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); TOOLS = os.path.join(HERE, "..", "..", "tools"); sys.path.insert(0, TOOLS)
S_ = "/tmp/claude-0/-home-claude/97ad6b31-1277-5795-987d-0d7c1b8393c4/scratchpad/"
os.environ.setdefault("RE_ASSETS_DIR", S_ + "assets3/project")
from PIL import Image, ImageDraw
import musicvideo as MV, newwave, kitpieces as K, sfx
from musicvideo import W, H, FPS, LIME, INK, RED, GREEN, GOLD, stamp, fit, mono

M4 = S_ + "mascot4/project/"; M3 = S_ + "mascot3/project/"
BOSS = M4 + "V2_08BossMyWeek.dc.html"
g = MV.Grid(143.55, 0.163); BAR = 4 * 60 / 143.55; END = 40.0
SKY = "#9FD4FF"

# ---------------------------------------------------------------- helpers
def up(im, k): return im.resize((im.width * k, im.height * k), Image.NEAREST)
def P(board, name, t): return K.piece(board, t, name)
def once(board, name, u, fps=10):                       # one-shot animation that holds its last frame
    fr = K.frames(board, name); return fr[min(len(fr) - 1, int(u * fps))]

def home(room, x0, t):
    """Kit's room at 1:1 x12: a 90x128 crop of the stage under a black 384 px text band."""
    big = newwave.room_big(room, t); k = newwave.K
    crop = big.crop((x0 * k, 0, (x0 + 90) * k, 128 * k)).resize((1080, 1536), Image.NEAREST)
    img = Image.new("RGB", (W, H), "#05060A"); img.paste(crop, (0, 384)); return img

def place(img, im, x, feet, k=12):                      # x = centre, feet = bottom y on the 1080x1920 frame
    b = up(im, k); img.paste(b, (int(x - b.width / 2), int(feet - b.height)), b); return img

def water_out(im):
    """Kit's top-down float comes on its own square of water; drop the water colours (sampled from its border) so it sits in the pool."""
    a = np.array(im.convert("RGBA")); edge = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]])
    cols = {tuple(c[:3]) for c in edge if c[3] > 0}
    m = np.zeros(a.shape[:2], bool)
    for c in cols: m |= (a[..., 0] == c[0]) & (a[..., 1] == c[1]) & (a[..., 2] == c[2])
    a[m, 3] = 0; return Image.fromarray(a)

NFA_BADGE = False   # the boss 2026-11-06: no NOT FINANCIAL ADVICE badge on videos with no data or positions (caption keeps the line)
def mixed(img, parts, y, size):
    """One centred line in several colours (white with a lime accent word, the boss 11/6), black stroke like stamp()."""
    d = ImageDraw.Draw(img); full = "".join(p for p, _ in parts); f = fit(full, W - 160, size, wdth=125, wght=900)
    x = W / 2 - f.getlength(full) / 2; sw = max(6, size // 12)
    for txt, col in parts:
        d.text((x, y), txt, font=f, fill=col, anchor="lm", stroke_width=sw, stroke_fill="#000000"); x += f.getlength(txt)
    return img

def no_shadow(im):
    """Drop the dark contact shadow under a standing piece (the boss 11/6: 'looks like I'm on a black skateboard')."""
    a = np.array(im.convert("RGBA")); h = a.shape[0]
    rows = range(max(0, h - 4), h)
    for y in rows:
        dark = (a[y, :, :3].astype(int).sum(1) < 160) & (a[y, :, 3] > 0) & (a[y, :, 3] < 255)
        a[y, dark, 3] = 0
    bb = Image.fromarray(a).getbbox(); return Image.fromarray(a).crop(bb) if bb else im

def nfa(img):
    if not NFA_BADGE: return img
    d = ImageDraw.Draw(img); f = mono(24, True); w = d.textlength("NOT FINANCIAL ADVICE", font=f)
    d.rectangle([60, 300, 60 + w + 24, 340], fill="#000000", outline="#3A3A3A", width=2); d.text((72, 320), "NOT FINANCIAL ADVICE", font=f, fill=INK, anchor="lm"); return img

def day(img, name, sub=None, col=LIME):
    stamp(img, name, col, 150, 120)
    if sub: stamp(img, sub, INK, 250, 50)
    return img

def bubble(img, kind, text, x, y, u, k=8, col="#0B0B0B", size=None):
    k = int(k * (1.6 if "small" in kind else 1.25 if "medium" in kind else 1.05))
    """Kit's empty speech bubble (ROOMKITWEEK) with a pop-in, text set by us."""
    if u < 0: return img
    s = min(1.0, 0.55 + u * 3.0) if u < 0.15 else (1.08 - 0.08 * min(1, (u - 0.15) * 8))
    b = K.frames("ROOMKITWEEK", f"Speech bubble, {kind}")[-1]; kk = max(1, int(round(k * s)))
    bb = up(b, kk); img.paste(bb, (int(x - bb.width / 2), int(y - bb.height / 2)), bb)
    bx, by, bw, bh = body_box(bb); cx = x - bb.width / 2 + bx + bw / 2; cy = y - bb.height / 2 + by + bh / 2
    d = ImageDraw.Draw(img); ls = text.split("\n")
    f = min((fit(l, int(bw * 0.8), size or int(bh * 0.42), wdth=110, wght=900) for l in ls), key=lambda q: q.size)
    for i, l in enumerate(ls): d.text((cx, cy + (i - (len(ls) - 1) / 2) * f.size * 1.08), l, font=f, fill=col, anchor="mm")
    return img

def body_box(im):
    """The bubble's body without its tail: rows at least 85% as wide as the widest row, and their column span."""
    a = np.array(im.split()[-1]) > 0; w = a.sum(1); rows = np.where(w >= 0.85 * w.max())[0]
    cols = np.where(a[rows].any(0))[0]; return int(cols.min()), int(rows.min()), int(cols.max() - cols.min() + 1), int(rows.max() - rows.min() + 1)

def warcry(img, text, x, y, u, k=10):
    if u < 0: return img
    kk = k if u > 0.12 else max(2, int(k * (0.5 + u * 4)))
    b = up(K.frames("FXRAID", "FX-WARCRY")[-1], kk); jx = int(math.sin(u * 60) * 4)
    img.paste(b, (int(x - b.width / 2) + jx, int(y - b.height / 2)), b)
    bx, by, bw, bh = body_box(b); cx = x + jx - b.width / 2 + bx + bw / 2; cy = y - b.height / 2 + by + bh / 2
    d = ImageDraw.Draw(img); ls = text.split("\n")
    f = min((fit(l, int(bw * 0.62), 64, wdth=110, wght=900) for l in ls), key=lambda q: q.size)
    for i, l in enumerate(ls): d.text((cx, cy + (i - (len(ls) - 1) / 2) * f.size * 1.05), l, font=f, fill="#0B0B0B", anchor="mm")
    return img

# ---------------------------------------------------------------- the raid (x8 arena from the WoW video, new party + day bosses)
def arena():
    st = newwave._stage("ROOM-19"); im = newwave.room_big("ROOM-19", 0.0).resize((320, 128), Image.NEAREST)
    c = Image.new("RGBA", (AW, AH), (10, 10, 16, 255))
    wall = K.piece("LIBROOMS6", 0, "Wall, dungeon stone"); flr = K.piece("LIBROOMS6", 0, "Floor, flagstones")
    for y in range(0, RT, wall.height):
        for x in range(0, AW, wall.width): c.alpha_composite(wall.crop((0, 0, min(wall.width, AW - x), min(wall.height, RT - y))), (x, y))
    for y in range(RT + 88, AH, flr.height):
        for x in range(0, AW, flr.width): c.alpha_composite(flr.crop((0, 0, min(flr.width, AW - x), min(flr.height, AH - y))), (x, y))
    c.alpha_composite(im.crop((70, 0, 70 + AW, 128)).convert("RGBA"), (0, RT)); return c
AW, AH, RT, AK = 180, 320, 116, 6; FEET = RT + 136
_AR = None
GEAR = {"theo": (M4 + "V2_08TheoRaid.dc.html", {"idle": "In gear · idle", "atk": "In gear · attack", "shout": "In gear · shout", "block": "In gear · block"}),
        "ada": (M4 + "V2_08AdaRaid.dc.html", {"idle": "In gear · idle", "atk": "In gear · attack", "shout": "In gear · shout", "block": "In gear · block"}),
        "roz": (M4 + "V2_08RozRaid.dc.html", {"idle": "In gear · idle", "atk": "In gear · attack", "shout": "In gear · shout", "block": "In gear · block"}),
        "penny": (M3 + "V2_06PennyGear.dc.html", {"idle": "In gear · idle", "atk": "In gear · block", "shout": "In gear · idle", "block": "In gear · block"}),
        "kit": (M3 + "V2_06KitGear.dc.html", {"idle": "In gear · idle", "atk": "In gear · swing", "shout": "In gear · swing", "block": "In gear · idle"})}

def raid(t, u, dur, boss, party, title, beats, retreat_at=None):
    """party: [(who, x)], beats: [(t0, who, pose)] pose per member over time. The day boss lunges every 2 bars."""
    global _AR
    if _AR is None: _AR = arena()
    c = _AR.copy(); s = u
    lunge = (s % (2 * BAR)) > 2 * BAR - 0.5 and (retreat_at is None or s < retreat_at)
    ph = ((s % (2 * BAR)) - (2 * BAR - 0.5)) / 0.5 if lunge else 0
    if retreat_at is not None and s >= retreat_at:
        bim = once(f"RAID-0{boss}", "Retreat", s - retreat_at); bx = AW - bim.width + 4 + int((s - retreat_at) * 40)
    else:
        bim = K.piece(f"RAID-0{boss}", t, "Attack" if lunge else "Idle"); bx = AW - bim.width + 4 - int(14 * math.sin(ph * math.pi))
    shake = (int(math.sin(t * 70) * 2), int(math.cos(t * 55) * 1)) if lunge and ph > 0.4 else (0, 0)
    c.paste(bim, (bx + shake[0], FEET - bim.height + shake[1]), bim)
    pose = {w: "idle" for w, _ in party}
    for t0, w, p in beats:
        if s >= t0: pose[w] = p
    for i, (w, x) in enumerate(party):
        board, names = GEAR[w]; nm = names[pose[w]]
        im = K.piece(board, t + i * 0.15, nm); dx = 4 if pose[w] == "atk" else 0
        if lunge and ph > 0.4: dx -= 3
        c.paste(im, (x - im.width // 2 + dx + shake[0], FEET - im.height + shake[1]), im)
        if pose[w] == "block" and int(t * 10) % 3 == 0:
            fl = K.piece("FXRAID", t, "FX-BLOCKFLASH"); c.alpha_composite(fl, (x + 6, FEET - im.height // 2 - fl.height // 2))
    if boss == 1 and lunge:
        sh = K.piece("FXRAID", t, "FX-SHARDS"); c.alpha_composite(sh, (bx - 10, FEET - 80))
    img = up(c, AK).convert("RGBA")
    if (s * 8) % 1 < 0.5 and lunge: img = Image.alpha_composite(img, Image.new("RGBA", img.size, (255, 40, 40, 34)))
    d = ImageDraw.Draw(img)
    hp = 0.85 - 0.1 * (s / dur) if retreat_at is None or s < retreat_at else max(0.0, 0.75 - (s - retreat_at) * 0.6)
    d.rectangle([60, 470, W - 60, 520], fill="#000000", outline=INK, width=4); d.rectangle([66, 476, 66 + int((W - 132) * hp), 514], fill=RED)
    d.text((70, 455), title, font=mono(30, True), fill=INK, anchor="ls")
    return img.convert("RGB")

def dialog(img, text, u):
    """Battle text box (classic RPG style): typed out, bottom of the frame."""
    d = ImageDraw.Draw(img); x0, y0, x1, y1 = 50, 1640, W - 50, 1860
    d.rectangle([x0, y0, x1, y1], fill="#0B0B0B", outline=INK, width=8); d.rectangle([x0 + 14, y0 + 14, x1 - 14, y1 - 14], outline="#3A3A3A", width=3)
    n = max(1, int(len(text) * min(1.0, u / 0.3))); txt = text[:n]
    f = fit(text, x1 - x0 - 90, 60, wdth=100, wght=800)
    d.text((x0 + 44, (y0 + y1) // 2), txt, font=f, fill=INK, anchor="lm")
    if n == len(text) and int(u * 3) % 2: d.polygon([(x1 - 70, y1 - 60), (x1 - 40, y1 - 60), (x1 - 55, y1 - 40)], fill=LIME)
    return img

def raid2(t, s, room, x0, name, hp, boss_pose, party, poses, hit=False, huge=False, retreat=None):
    """Kit's day arena at 1:1 x10 (108x128 crop, floor at y88). Party in gear at x6 (Kit's size for them next to the
    huge dragon: about a third of its head). The huge LIQUIDATOR at x10, body cropped by the frame; other bosses at x7."""
    big = newwave.room_big(room, t); k = newwave.K
    lay = big.crop((x0 * k, 0, (x0 + 108) * k, 128 * k)).resize((1080, 1280), Image.NEAREST).convert("RGBA")
    TOP = 330; FEET = TOP + 92 * 10
    if huge:
        b = up(K.piece("RAID-01H", t, boss_pose.replace("#2", "")), 10); bx = 1080 - b.width + 700 - (40 if "Swipe" in boss_pose else 0)
        lay.alpha_composite(b, (bx, 1280 - b.height)) if bx >= 0 else lay.paste(b, (bx, 1280 - b.height), b)
    else:
        bd = {"THE HEADLINE HYDRA": "RAID-02", "THE VOLATILITY STORM": "RAID-03"}[name]
        b = once(bd, boss_pose, retreat) if retreat is not None else K.piece(bd, t, boss_pose); b = up(b, 7)
        bx = 1080 - b.width + 140 + (int(retreat * 500) if retreat is not None else 0) - (60 if boss_pose == "Attack" else 0)
        lay.paste(b, (bx, 92 * 10 - b.height + 30), b)
    pose = {m[0]: "idle" for m in party}
    for t0, w, p in poses:
        if s >= t0: pose[w] = p
    order = sorted(enumerate(party), key=lambda e: (len(e[1]) > 2 and e[1][2]) or 0)   # back row (raised) first
    for i, m in order:
        w, x = m[0], m[1]; lift = m[2] if len(m) > 2 else 0
        board, names = GEAR[w]; im = up(K.piece(board, t + i * 0.15, names[pose[w]]), 6); dx = 18 if pose[w] == "atk" else 0
        lay.paste(im, (x * 10 - im.width // 2 + dx, (92 + lift) * 10 - im.height), im)
        if pose[w] == "block" and int(t * 10) % 3 == 0:
            fl = up(K.piece("FXRAID", t, "FX-BLOCKFLASH"), 6); lay.paste(fl, (x * 10 + 40, 92 * 10 - im.height // 2 - fl.height // 2), fl)
    if hit and int(s * 12) % 2: lay = Image.alpha_composite(lay, Image.new("RGBA", lay.size, (255, 40, 40, 46)))
    shake = (int(math.sin(t * 70) * 12), int(math.cos(t * 55) * 8)) if hit else (0, 0)
    img = Image.new("RGB", (W, H), "#05060A"); img.paste(lay.convert("RGB"), (shake[0], TOP + shake[1]))
    d = ImageDraw.Draw(img)
    d.text((60, 120), name, font=fit(name, W - 120, 88, wdth=125, wght=900), fill=INK, anchor="ls")
    d.rectangle([60, 160, W - 60, 220], fill="#000000", outline=INK, width=5); d.rectangle([68, 168, 68 + int((W - 136) * hp), 212], fill=RED if hp > 0.3 else GOLD)
    d.text((W - 60, 270), "HP", font=mono(30, True), fill=INK, anchor="rs")
    return img

# ---------------------------------------------------------------- shots (times in seconds, cut on bars of the 143.6 BPM grid)
T = lambda bars: round(bars * BAR, 3)

def fan(img, t, x0):
    """Kit's turning ceiling fan (LIBROOMS8) over the room's static one (stage x ~140-195, top of the room)."""
    f = up(K.piece("LIBROOMS8", t, "Ceiling fan, turning"), 12); img.paste(f, (int((167 - x0) * 12 - f.width / 2), 384), f); return img

def s_open(t, u):
    img = fan(home("ROOM-23", 95, t), t, 95); place(img, P(BOSS, "Sip · coffee mug", t), 540, 1700)
    stamp(img, "MY WEEK.", LIME, 150, 150)
    if u > 0.9: stamp(img, "(my fund runs on rules)", INK, 268, 52)
    return nfa(img)

def s_mon(t, u):
    s = u
    img = home("ROOM-21", 25, t)                     # the boss 11/6: cook at the range against the wall, under the cabinets
    place(img, P(BOSS, "Cook · pancake flip", t), (30 - 25) * 12 + 78 * 6, 384 + 94 * 12)   # the boss 11/6: 6 px down, the room is drawn at an angle
    day(img, "MONDAY.", "9:30 AM")
    if s > 1.3: bubble(img, "large, tail down", "WHO WANTS\nCHOCOLATE CHIPS?", 470, 640, s - 1.3, 11, size=56)
    for i, (kind, x, y, at) in enumerate((("small, tail right", 930, 1000, 3.4), ("medium, tail left", 150, 1120, 3.9), ("small, tail right", 960, 1260, 4.3), ("small, tail left", 130, 1400, 4.7))):
        bubble(img, kind, "ME!", x, y, s - at, 9 if "small" in kind else 8, size=78)
    return nfa(img)

def s_wipe(t, u):
    fr = K.frames("FXRAID", "FX-WIPE-TALL"); im = fr[min(len(fr) - 1, int(u / T(0.5) * len(fr)))]
    img = Image.new("RGB", (W, H), "#05060A"); b = im.resize((W, H), Image.NEAREST); img.paste(b, (0, 0), b)
    stamp(img, "MEANWHILE…", INK, 960, 130); stamp(img, "IN THE MARKET", RED, 1100, 70)
    return nfa(img)

def s_raid_mon(t, u):
    s = u
    img = raid2(t, s, "ROOM-25", 20, "THE LIQUIDATOR", huge=True,
                hp=0.95 if s < 4.3 else max(0.55, 0.95 - (s - 4.3) * 0.6),
                boss_pose="Huge · Roar#2" if 0.8 < s < 1.8 else "Huge · Swipe#2" if 1.8 <= s < 2.8 else "Huge · Hurt#2" if s >= 4.3 else "Huge · Idle#2",
                party=[("theo", 18), ("penny", 42)],
                poses=[(0.0, "theo", "idle"), (1.8, "theo", "block"), (1.8, "penny", "block"), (2.9, "theo", "shout"), (4.3, "theo", "atk"), (4.3, "penny", "atk")],
                hit=1.8 <= s < 2.6)
    if s < 0.8: dialog(img, "THE LIQUIDATOR appears!", s)
    elif s < 1.8: dialog(img, "THE LIQUIDATOR casts MARGIN CALL!", s - 0.8)
    elif s < 2.9: dialog(img, "The party takes a big hit!", s - 1.8)
    elif s < 4.3: warcry(img, "WHAT DOES THE\nRULEBOOK SAY?", 420, 760, s - 2.9); dialog(img, "THEO checks the rulebook...", s - 2.9)
    else: stamp(img, "HOLD TO EXPIRY!", LIME, 760, 120); dialog(img, "The party holds the line!", s - 4.3)
    return nfa(img)

def s_tue(t, u):
    s = u
    img = home("ROOM-22", 20, t)
    fl = up(water_out(P(BOSS, "Float · top-down, donut pool float", t)), 9); img.paste(fl, (540 - fl.width // 2 + int(math.sin(t * 0.7) * 30), 1000 - fl.height // 2 + int(math.sin(t * 2.2) * 10)), fl)   # zoomed out (the boss 11/6)
    rp = up(P("ROOMKITWEEK", "Water ripple ring", t), 10); img.paste(rp, (200, 1600), rp); img.paste(rp, (800, 560), rp)
    day(img, "TUESDAY.")
    return nfa(img)

def s_raid_tue(t, u):
    s = u
    img = raid2(t, s, "ROOM-26", 30, "THE HEADLINE HYDRA",
                hp=0.9 if s < 2.6 else max(0.5, 0.9 - (s - 2.6) * 0.5),
                boss_pose="Attack" if 0.7 < s < 1.7 else "Hurt" if s >= 2.6 else "Idle",
                party=[("ada", 18), ("roz", 42)],
                poses=[(0.0, "ada", "idle"), (0.7, "roz", "block"), (1.7, "ada", "shout"), (2.6, "ada", "atk"), (2.6, "roz", "shout")], hit=0.9 <= s < 1.5)
    if s < 0.7: dialog(img, "THE HEADLINE HYDRA appears!", s)
    elif s < 1.7: dialog(img, "THE HEADLINE HYDRA screams BREAKING NEWS!", s - 0.7)
    elif s < 2.6: warcry(img, "NO PANIC!", 380, 760, s - 1.7); dialog(img, "Nobody even flinched.", s - 1.7)
    else: warcry(img, "PUTS ARE\nNEVER ROLLED!", 480, 760, s - 2.6); dialog(img, "ROZ reads the rules out loud!", s - 2.6)
    return nfa(img)

def s_wed(t, u):
    s = u
    img = home("ROOM-24", 190, t); place(img, once(BOSS, "Desk · type, phone, one tap", s), 520, 1800)
    day(img, "WEDNESDAY.", "at work")
    if s > 0.9: bubble(img, "medium, tail down", "QUICK CHECK.", 560, 760, s - 0.9, 10, size=54)
    if s > 1.7: mixed(img, [("ALL BY THE ", INK), ("RULES.", LIME)], 1640, 76)
    if s > 2.3: mixed(img, [("BACK TO ", INK), ("WORK.", LIME)], 1750, 76)
    return nfa(img)

def s_raid_thu(t, u):
    s = u
    ret = s >= 2.2
    img = raid2(t, s, "ROOM-28", 20, "THE VOLATILITY STORM",
                hp=0.8 if s < 1.6 else max(0.0, 0.8 - (s - 1.6) * 0.9),
                boss_pose="Retreat" if ret else "Attack" if 0.5 < s < 1.4 else "Hurt" if s >= 1.6 else "Idle", retreat=s - 2.2 if ret else None,
                party=[("theo", 14), ("roz", 40), ("ada", 22, -16), ("penny", 50, -16)],
                poses=[(0.0, "theo", "block"), (0.0, "roz", "block"), (1.4, "theo", "shout"), (1.4, "ada", "shout"), (1.4, "roz", "shout"), (1.4, "penny", "shout"), (1.9, "theo", "atk"), (1.9, "ada", "atk")],
                hit=0.6 <= s < 1.3)
    if s < 1.4:
        dialog(img, "THE VOLATILITY STORM unleashes BOOM BOOM BOOM!", s)
        if 0.6 <= s < 1.3: stamp(img, ["BOOM!", "BOOM! BOOM!", "BOOM! BOOM! BOOM!"][min(2, int((s - 0.6) / 0.24))], RED, 760, 110)
    elif s < 2.2: warcry(img, "STICK TO\nTHE RULES!", 500, 760, s - 1.4); dialog(img, "The whole fund sticks to the rules!", s - 1.4)
    else: stamp(img, "HELD THE LINE.", LIME, 760, 130); dialog(img, "THE VOLATILITY STORM fled!", s - 2.2)
    return nfa(img)

def s_fri(t, u):
    s = u
    img = fan(home("ROOM-23", 95, t), t, 95); place(img, no_shadow(once(BOSS, "Play · blocks on the rug", s)), 540, 1780)
    day(img, "FRIDAY.")
    for i, (kind, x, y, at) in enumerate((("medium, tail right", 900, 900, 1.5), ("medium, tail left", 180, 1060, 1.9), ("small, tail right", 930, 1200, 2.3))):
        bubble(img, kind, "AGAIN!", x, y, s - at, 9, size=64)
    return nfa(img)

def s_end(t, u):
    s = u
    img = Image.new("RGB", (W, H), "#05060A")
    lines = [(0.0, [("WHY ", INK), ("STRESS?", LIME)], 300, 110), (0.6, [("KNOW YOUR ", INK), ("RULES.", LIME)], 430, 96),
             (1.2, [("LET THE ", INK), ("BOT", LIME)], 580, 110), (1.45, [("DO THE ", INK), ("GRIND.", LIME)], 700, 110), (1.9, [("YOU DO THE ", INK), ("LIVING.", LIME)], 840, 96)]
    for at, parts, y, sz in lines:
        if s >= at: mixed(img, parts, y, sz)
    if s > 2.5:                                      # Kit's LIKE + FOLLOW neon (DEC-59), the closer the boss loves (WoW video)
        n = K.piece("DEC-59", t); k = max(1, min(820 // n.width, 420 // n.height)); sg = up(n, k)
        if int(s * 6) % 7: img.paste(sg, (W // 2 - sg.width // 2, 1000), sg)
        stamp(img, "An AI-run fund, learning in public.", INK, 1000 + sg.height + 70, 40)
    else:
        place(img, no_shadow(P(BOSS, "Sip · coffee mug", t)), 300, 1800, 7); place(img, no_shadow(K.piece(M4 + "V2_08TheoRaid.dc.html", t, "In gear · idle")), 760, 1800, 7)
    return nfa(img)

SHOTS = [(0.0, s_open), (T(2), s_mon), (T(6), s_wipe), (T(6.5), s_raid_mon), (T(10), s_tue), (T(12), s_raid_tue), (T(14.5), s_wed),
         (T(16.5), s_raid_thu), (T(18.5), s_fri), (T(21.5), s_end)]

def mix(out_mp3):
    import librosa
    import numpy as np
    full, sr = librosa.load(MV.song_path("set_rulebook_stress"), sr=sfx.SR, mono=False)
    full = full.T if full.ndim == 2 else full
    # Roz 11/7 (B-20261107-083805-roz-wvi2): verse 1 sings "tap approve", which is false. Keep the intro + first hook (bars 0-15),
    # then jump on the bar line to the last hook (bars 56-63). Verse 1 (bars ~16-27) is never in the cut.
    b = lambda n: int(round((0.163 + n * BAR) * sfx.SR)); xf = int(0.03 * sfx.SR)
    a_, c_ = full[: b(16) + xf].copy(), full[b(56): b(56) + int((END + 0.5) * sfx.SR) - b(16)].copy()
    ramp = np.linspace(0, 1, xf); ramp = ramp[:, None] if a_.ndim == 2 else ramp
    a_[-xf:] = a_[-xf:] * (1 - ramp) + c_[:xf] * ramp
    y = np.concatenate([a_, c_[xf:]])
    bus = sfx.Bus(END + 1)
    bus.add(sfx.whoosh(0.6), T(6) - 0.2, 0.35, duck=6)
    for st, d in ((T(6.5), T(3.5)), (T(12), T(2.5)), (T(16.5), T(2))):
        k = 0.0
        while k < d:
            if (k % (2 * BAR)) > 2 * BAR - 0.5: pass
            k += BAR
        for j in range(int(d / (2 * BAR)) + 1): bus.add(sfx.roar(), st + 2 * BAR * (j + 1) - 0.5, 0.25)
        bus.add(sfx.bonk(), st + d * 0.55, 0.3); bus.add(sfx.zap(), st + d * 0.7, 0.2)
    for at in (T(2) + 3.4, T(2) + 3.9, T(2) + 4.3, T(2) + 4.7, T(18.5) + 1.5, T(18.5) + 1.9, T(18.5) + 2.3): bus.add(sfx.ding(), at, 0.18)
    bus.add(sfx.heal(), T(16.5) + 1.6, 0.2); bus.add(sfx.sparkle(), T(21.5) + 4.4, 0.25)
    m = bus.mix_into(y[: int(END * sfx.SR)])
    import soundfile as sf
    wav = out_mp3.replace(".mp3", ".wav"); sf.write(wav, m, sfx.SR)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", wav, "-b:a", "256k", out_mp3], check=True)

if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    KW = dict(karaoke_on=False, end_fn=s_end)
    if "--panels" in sys.argv: MV.panels(a[0], SHOTS, [], g, END, **KW)
    elif "--cover" in sys.argv: MV.frame_at(T(2) + 4.9, SHOTS, [], g, **KW).save(a[0], quality=92)
    else:
        mix(MV.song_path("_week_mix"))
        MV.build(a[0] if a else "/home/claude/out/my_week_v6.mp4", "_week_mix", SHOTS, [], g, END, **KW)
