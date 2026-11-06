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

def nfa(img):
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

# ---------------------------------------------------------------- shots (times in seconds, cut on bars of the 143.6 BPM grid)
T = lambda bars: round(bars * BAR, 3)

def s_open(t, u):
    img = home("ROOM-23", 95, t); place(img, P(BOSS, "Sip · coffee mug", t), 540, 1700)
    stamp(img, "MY WEEK.", LIME, 150, 150)
    if u > 0.9: stamp(img, "(my fund runs on rules)", INK, 268, 52)
    return nfa(img)

def s_mon(t, u):
    s = u
    img = home("ROOM-21", 25, t)                     # the boss 11/6: cook at the range against the wall, under the cabinets
    place(img, P(BOSS, "Cook · pancake flip", t), (30 - 25) * 12 + 78 * 6, 384 + 88 * 12)
    day(img, "MONDAY.", "9:30 AM")
    if s > 1.3: bubble(img, "large, tail down", "WHO WANTS\nCHOCOLATE CHIPS?", 470, 640, s - 1.3, 11, size=56)
    for i, (kind, x, y, at) in enumerate((("small, tail left", 930, 1000, 3.4), ("medium, tail right", 150, 1120, 3.9), ("small, tail left", 960, 1260, 4.3), ("small, tail right", 130, 1400, 4.7))):
        bubble(img, kind, "ME!", x, y, s - at, 9 if "small" in kind else 8, size=78)
    return nfa(img)

def s_wipe(t, u):
    fr = K.frames("FXRAID", "FX-WIPE-TALL"); im = fr[min(len(fr) - 1, int(u / T(0.5) * len(fr)))]
    img = Image.new("RGB", (W, H), "#05060A"); b = im.resize((W, H), Image.NEAREST); img.paste(b, (0, 0), b)
    stamp(img, "MEANWHILE…", INK, 960, 130); stamp(img, "IN THE MARKET", RED, 1100, 70)
    return nfa(img)

def s_raid_mon(t, u):
    d = T(3.5); s = u
    img = raid(t, u, d, 1, [("theo", 30), ("penny", 66)], "MONDAY · THE CANDLE DRAGON", [(0.2, "theo", "shout"), (1.5, "penny", "shout"), (2.9, "theo", "shout"), (4.4, "theo", "atk"), (4.4, "penny", "atk")])
    if s < 1.5: warcry(img, "IT'S DROPPING!", 360, 820, s - 0.2)
    elif s < 2.9: warcry(img, "HOLD THE LINE!", 520, 820, s - 1.5)
    elif s < 4.4: warcry(img, "WHAT DOES THE\nRULEBOOK SAY?", 400, 820, s - 2.9)
    else: stamp(img, "HOLD TO EXPIRY!", LIME, 780, 120)
    return nfa(img)

def s_tue(t, u):
    s = u
    img = home("ROOM-22", 20, t)
    fl = up(water_out(P(BOSS, "Float · top-down, donut pool float", t)), 6); img.paste(fl, (540 - fl.width // 2 + int(math.sin(t * 0.7) * 30), 1000 - fl.height // 2 + int(math.sin(t * 2.2) * 10)), fl)   # zoomed out (the boss 11/6)
    rp = up(P("ROOMKITWEEK", "Water ripple ring", t), 10); img.paste(rp, (200, 1600), rp); img.paste(rp, (800, 560), rp)
    day(img, "TUESDAY.")
    return nfa(img)

def s_raid_tue(t, u):
    d = T(2.5); s = u
    img = raid(t, u, d, 2, [("ada", 30), ("roz", 64)], "TUESDAY · THE HEADLINE HYDRA", [(0.1, "roz", "block"), (0.1, "ada", "shout"), (1.9, "ada", "atk"), (1.9, "roz", "shout")])
    if s < 1.9: warcry(img, "NO PANIC!", 360, 820, s - 0.1)
    else: warcry(img, "PUTS ARE\nNEVER ROLLED!", 520, 820, s - 1.9)
    return nfa(img)

def s_wed(t, u):
    s = u
    img = home("ROOM-24", 190, t); place(img, once(BOSS, "Desk · type, phone, one tap", s), 520, 1800)
    day(img, "WEDNESDAY.", "at work")
    if s > 1.6: bubble(img, "medium, tail down", "QUICK CHECK.", 560, 760, s - 1.6, 10, size=54)
    if s > 2.6: stamp(img, "BY THE RULES. BACK TO WORK.", LIME, 900, 56)
    return nfa(img)

def s_raid_thu(t, u):
    d = T(2); s = u
    img = raid(t, u, d, 3, [("theo", 24), ("ada", 50), ("roz", 76), ("penny", 100)], "THURSDAY · THE STORM GOLEM",
               [(0.0, "theo", "shout"), (0.0, "ada", "shout"), (0.0, "roz", "shout"), (0.0, "penny", "shout"), (1.4, "theo", "atk"), (1.4, "ada", "atk"), (1.4, "roz", "block")], retreat_at=1.6)
    if s < 1.6: warcry(img, "STICK TO\nTHE RULES!", 540, 800, s)
    else: stamp(img, "HELD THE LINE.", LIME, 780, 130)
    return nfa(img)

def s_fri(t, u):
    s = u
    img = home("ROOM-23", 95, t); place(img, once(BOSS, "Play · blocks on the rug", s), 540, 1780)
    day(img, "FRIDAY.")
    for i, (kind, x, y, at) in enumerate((("medium, tail left", 900, 900, 1.5), ("medium, tail right", 180, 1060, 1.9), ("small, tail left", 930, 1200, 2.3))):
        bubble(img, kind, "AGAIN!", x, y, s - at, 9, size=64)
    return nfa(img)

def s_end(t, u):
    s = u
    img = Image.new("RGB", (W, H), "#05060A")
    lines = [(0.0, "WHY STRESS?", INK, 480, 120), (0.6, "KNOW YOUR RULES.", INK, 630, 100), (1.2, "LET THE BOT", LIME, 800, 120), (1.45, "DO THE GRIND.", LIME, 930, 120), (1.9, "YOU DO THE LIVING.", INK, 1090, 100)]
    for at, txt, col, y, sz in lines:
        if s >= at: stamp(img, txt, col, y, sz)
    if s > 2.5:                                      # Kit's LIKE + FOLLOW neon (DEC-59), the closer the boss loves (WoW video)
        n = K.piece("DEC-59", t); k = max(1, min(820 // n.width, 420 // n.height)); sg = up(n, k)
        if int(s * 6) % 7: img.paste(sg, (W // 2 - sg.width // 2, 1300), sg)
        stamp(img, "An AI-run fund, learning in public.", INK, 1300 + sg.height + 70, 40)
    else:
        place(img, P(BOSS, "Sip · coffee mug", t), 300, 1840, 6); place(img, K.piece(M4 + "V2_08TheoRaid.dc.html", t, "In gear · idle"), 760, 1840, 6)
    return nfa(img)

SHOTS = [(0.0, s_open), (T(2), s_mon), (T(6), s_wipe), (T(6.5), s_raid_mon), (T(10), s_tue), (T(12), s_raid_tue), (T(14.5), s_wed),
         (T(16.5), s_raid_thu), (T(18.5), s_fri), (T(21.5), s_end)]

def mix(out_mp3):
    import librosa
    y, sr = librosa.load(MV.song_path("set_rulebook_stress"), sr=sfx.SR, mono=False, duration=END + 0.5)
    y = y.T if y.ndim == 2 else y
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
        MV.build(a[0] if a else "/home/claude/out/my_week_v1.mp4", "_week_mix", SHOTS, [], g, END, **KW)
