"""HOLIDAY ASSETS (the boss 2026-11-01): one set per day the market is closed, 50 animated props each, for the videos.
Sets (NYSE closures): NYD New Year's Day · MLK Martin Luther King Jr. Day · PRES Washington's Birthday · GF Good Friday (spring
weekend) · MEM Memorial Day · JUN Juneteenth · IND Independence Day · LAB Labor Day · TG Thanksgiving · XMAS Christmas.
IDs: HOL-<SET>-NN (01..50). Every asset is drawn by a generator here at its final pixel size (16, 24 or 32 px on the mascot grid),
and every animation frame is its own drawing (pixkit; rec-marketing-pixel-art). Signs are blank, nothing carries digits, no brands,
no copyrighted characters.

    import holiday_assets as HA
    frames, ticks = HA.frames("HOL-XMAS-07")      # list of RGBA PIL images at native size + hold per frame (ticks of 100 ms)
    im = HA.still("HOL-XMAS-07")                   # frame 0
    im = HA.at("HOL-XMAS-07", t_seconds)           # the frame showing at time t (loops)
    HA.ids("XMAS") -> the 50 ids of a set;  HA.SETS -> set codes and names
"""
import math, random
from pixkit import *

# ---------------------------------------------------------------- palettes (5-tone hue-shifted ramps)
def R(c, **k): return ramp(c, **k)
NAVY = R((48, 64, 140)); CRIMSON = R((190, 40, 48)); FLAG_WHITE = R((236, 234, 226), dark=.72); FOREST = R((40, 120, 64)); HOLLY = R((34, 100, 52))
SNOW = R((232, 238, 246), dark=.74); ICE = R((150, 200, 240)); CHOC = R((110, 68, 40)); CARAMEL = R((200, 140, 80)); BERRY = R((200, 40, 70))
PUMPKIN = R((230, 120, 40)); MAPLE = R((200, 80, 36)); MUSTARD = R((214, 160, 44)); WHEAT = R((222, 190, 110)); PLUM = R((120, 60, 120))
PAN_RED = R((200, 30, 40)); PAN_GREEN = R((20, 130, 60)); PAN_BLACK = R((50, 48, 56), dark=.6, light=.4); PAN_GOLD = R((232, 180, 50))
PASTEL_PINK = R((246, 170, 200)); PASTEL_BLUE = R((160, 200, 240)); PASTEL_YEL = R((248, 230, 140)); PASTEL_GRN = R((170, 220, 160)); LILAC = R((190, 160, 230))
SAFETY = R((250, 170, 30)); HIVIS = R((230, 240, 60), light=.3); DENIM = R((70, 100, 160)); STEEL = R((160, 170, 184), dark=.68); RUBBER = R((60, 60, 68), dark=.6, light=.4)
PAPER = R((240, 232, 210), dark=.72); PARCH = R((226, 206, 160)); LEATHER = R((130, 80, 50)); SKY = R((120, 180, 240)); GRASS = R((90, 170, 70))
SPARK = (255, 250, 220); EMBER = R((250, 150, 40)); FLAME = R((250, 180, 50), light=.6); BLUSH = (240, 150, 160)

SETS = {"NYD": "New Year's Day", "MLK": "Martin Luther King Jr. Day", "PRES": "Washington's Birthday", "GF": "Good Friday (spring weekend)",
        "MEM": "Memorial Day", "JUN": "Juneteenth", "IND": "Independence Day", "LAB": "Labor Day", "TG": "Thanksgiving", "XMAS": "Christmas"}

DRAW = {}
STILL = {"firework": 2, "popper": 3, "sparkler": 1, "butterfly": 2, "ball_drop": 1}
def drawer(name, size=(24, 24), frames=4, ticks=None):
    def deco(fn):
        DRAW[name] = {"fn": fn, "size": size, "frames": frames, "ticks": ticks or ([8, 2, 8, 2] if frames == 4 else [6] * frames), "still": STILL.get(name, 0)}
        return fn
    return deco

def _rng(seed): return random.Random(seed)
def _bob(f, nf): return [0, -1, 0, 1][f % 4] if nf == 4 else int(round(math.sin(2 * math.pi * f / nf)))
def _sw(f, nf): return [0, 1, 0, -1][f % 4] if nf == 4 else int(round(math.sin(2 * math.pi * f / nf)))

# ---------------------------------------------------------------- party and decor
@drawer("balloon")
def balloon(P, v, f, nf):
    c = v["ramp"]; dy = _bob(f, nf); shape = v.get("shape", "round")
    if shape == "heart":
        P.sphere((4, 3 + dy, 12, 11 + dy), c); P.sphere((11, 3 + dy, 19, 11 + dy), c); P.poly([(4, 8 + dy), (19, 8 + dy), (12, 16 + dy)], c, box=(4, 3 + dy, 19, 16 + dy)); P.sphere((5, 4 + dy, 18, 15 + dy), c)
    elif shape == "long": P.sphere((7, 1 + dy, 16, 17 + dy), c, rim=True)
    else: P.sphere((5, 1 + dy, 18, 15 + dy), c, rim=True)
    P.put(11, 17 + dy, c[1]); P.put(12, 17 + dy, c[1]); P.put(11, 16 + dy, c[2]); P.put(12, 16 + dy, c[2])
    P.selout(); P.sparkle(9, 4 + dy, 0, SPARK); P.put(8, 6 + dy, c[4])
    s = _sw(f, nf)
    for y in range(18 + dy, 24): P.put(12 + (s if y > 20 else 0), y, (210, 210, 206))

@drawer("gift")
def gift(P, v, f, nf):
    b, rb = v["ramp"], v["ribbon"]; tall = v.get("tall", False); tw = v.get("twinkle", True)
    x0, y0, x1, y1 = (5, 8, 18, 21) if tall else (3, 10, 20, 21)
    P.box(x0, y0, x1, y1, b, top=1, side=2); cx = (x0 + x1) // 2
    P.rect(cx, y0, cx + 1, y1, rb[2]); P.rect(x0, (y0 + y1) // 2, x1, (y0 + y1) // 2 + 1, rb[2]); P.put(cx, (y0 + y1) // 2, rb[3])
    P.rect(x0 - 1, y0 - 3, x1 + 1, y0 - 1, b[3]); P.rect(x0 - 1, y0 - 1, x1 + 1, y0 - 1, b[2]); P.rect(cx, y0 - 3, cx + 1, y0 - 1, rb[3])
    P.sphere((cx - 4, y0 - 7, cx, y0 - 3), rb); P.sphere((cx + 1, y0 - 7, cx + 5, y0 - 3), rb); P.rect(cx, y0 - 5, cx + 1, y0 - 4, rb[1]); P.selout()
    if tw and f == 1: P.sparkle(x1 - 2, y0 + 2, 1, SPARK)
    if tw and f == 3: P.sparkle(x0 + 3, y1 - 3, 0, SPARK)

@drawer("candle", frames=3, ticks=[3, 2, 3])
def candle(P, v, f, nf):
    w = v["ramp"]; h = v.get("h", 12); fl = v.get("flame", FLAME); x0 = 9; y1 = 22; y0 = y1 - h
    if v.get("holder"): P.hcyl((6, 21, 17, 23), GOLD); y1 = 20; y0 = y1 - h
    P.vcyl((x0, y0, x0 + 5, y1), w); P.rect(x0, y0, x0 + 5, y0, w[3]); P.put(x0 + 2, y0 - 1, (80, 60, 50)); P.put(x0 + 3, y0, w[1])
    if v.get("drip"): P.put(x0 + 5, y0 + 2, w[3]); P.put(x0 + 5, y0 + 3, w[3]); P.put(x0, y0 + 4, w[3])
    ty = y0 - 2; shapes = [[(0, -5), (2, -2), (1, 0), (-1, 0), (-2, -2)], [(1, -6), (2, -3), (1, 0), (-1, 0), (-2, -2)], [(-1, -5), (2, -3), (1, 0), (-1, 0), (-2, -1)]]
    sh = shapes[f % 3]; cx = x0 + 2
    P.poly([(cx + dx, ty + dy) for dx, dy in sh], fl); P.put(cx, ty - 1, (255, 244, 200)); P.put(cx, ty - 2, (255, 244, 200)); P.selout()

@drawer("bunting", size=(32, 16))
def bunting(P, v, f, nf):
    cols = v["ramps"]; shape = v.get("shape", "tri"); n = 5
    for i in range(n):
        x = 2 + i * 6; dy = [0, 1, 0, -1][(f + i) % 4] if i % 2 else [0, -1, 0, 1][(f + i) % 4]; c = cols[i % len(cols)]
        if shape == "tri": P.poly([(x, 3 + dy), (x + 5, 3 + dy), (x + 2, 11 + dy), (x + 3, 11 + dy)], c, box=(x, 3 + dy, x + 5, 11 + dy))
        elif shape == "rect": P.box(x, 3 + dy, x + 5, 10 + dy, c, top=1, side=1)
        else: P.poly([(x, 3 + dy), (x + 5, 3 + dy), (x + 5, 8 + dy), (x + 2, 11 + dy), (x, 8 + dy)], c, box=(x, 3 + dy, x + 5, 11 + dy))
        P.put(x + 2, 5 + dy, c[3])
    for x in range(32): P.put(x, 2 + (1 if 6 < x < 26 else 0), (120, 110, 100))
    P.selout()

@drawer("flag")
def flag(P, v, f, nf):
    c = v["ramps"]; style = v.get("style", "stripes"); px = 4
    P.rect(px, 2, px, 22, WOOD[2]); P.put(px, 1, GOLD[3]); P.put(px, 2, GOLD[2]); P.rect(px, 3, px, 22, WOOD[1])
    for x in range(px + 1, px + 16):
        off = int(round(math.sin((x - px) / 3.2 + f * math.pi / 2) * 1.0)) if x > px + 4 else 0
        top = 3 + off; h = 10
        for y in range(top, top + h):
            k = y - top
            if style == "stripes": col = c[(k // 2) % len(c)]
            elif style == "solid": col = c[0]
            elif style == "bands": col = c[min(len(c) - 1, (x - px - 1) // 5)]
            else: col = c[0]
            tone = col[3] if y == top else col[1] if y == top + h - 1 or x == px + 15 else col[2]
            P.put(x, y, tone)
        if style == "stars" and x < px + 7:
            for y in range(top, top + 5): P.put(x, y, NAVY[2] if (x + y) % 2 else NAVY[3] if (x + y) % 4 == 0 else NAVY[2])
    if style == "emblem": P.sphere((px + 6, 6, px + 10, 10), c[1]); P.put(px + 8, 7, c[1][4])
    P.selout()

@drawer("sparkle", size=(16, 16), frames=4, ticks=[4, 3, 2, 3])
def sparkle(P, v, f, nf):
    c = v.get("color", SPARK); sz = [0, 1, 2, 1][f % 4]; P.sparkle(8, 8, sz, c)
    if sz == 2: P.put(6, 6, c); P.put(10, 10, c); P.put(10, 6, c); P.put(6, 10, c)
    if v.get("twin"): P.sparkle(3, 12, [1, 0, 0, 1][f % 4], c)

@drawer("firework", size=(32, 32), frames=4, ticks=[2, 2, 3, 5])
def firework(P, v, f, nf):
    c = v["ramp"]; c2 = v.get("ramp2", GOLD); cx, cy = 16, 14; k = f
    if k == 0: P.put(cx, cy, c[4]); P.rect(cx, cy + 1, cx, 30, c2[1]); P.put(cx, 30, EMBER[3]); return
    r = [0, 5, 10, 13][k]; n = v.get("rays", 8)
    for i in range(n):
        a = 2 * math.pi * i / n + (0.3 if k == 3 else 0)
        if k == 3:
            x = cx + int(round(math.cos(a) * r)); y = cy + int(round(math.sin(a) * r)) + 2; P.put(x, y, c[1]); P.put(x, y + 1, c[0]); P.put(x + 1, y + 2, c2[1])
        else:
            for rr_ in range(max(1, r - 4), r + 1):
                x = cx + int(round(math.cos(a) * rr_)); y = cy + int(round(math.sin(a) * rr_)); P.put(x, y, c[3] if rr_ == r else c[2] if rr_ > r - 3 else c2[3])
            if k == 2:
                a2 = a + math.pi / n; x = cx + int(round(math.cos(a2) * (r - 2))); y = cy + int(round(math.sin(a2) * (r - 2))); P.put(x, y, c2[4])
    if k == 1: P.sparkle(cx, cy, 1, c[4])
    if k == 2: P.sparkle(cx, cy, 0, c2[4])

@drawer("lantern", frames=4, ticks=[6, 2, 6, 2])
def lantern(P, v, f, nf):
    c = v["ramp"]; glow = [FLAME[3], FLAME[4], FLAME[3], FLAME[2]][f % 4]; shape = v.get("shape", "paper")
    if shape == "paper":
        P.sphere((4, 5, 19, 18), c, rim=True); P.rect(7, 3, 16, 4, BLACK[2]); P.rect(7, 19, 16, 20, BLACK[2]); P.rect(11, 0, 12, 2, (120, 110, 100))
        for y in range(7, 17, 3): P.hline(6, 17, y, c[1])
        P.rect(10, 9, 13, 14, glow); P.rect(11, 8, 12, 15, glow); P.rect(11, 21, 12, 23, GOLD[2])
    else:  # metal camping lantern
        P.rect(8, 2, 15, 3, BLACK[2]); P.rect(11, 0, 12, 1, BLACK[1]); P.box(6, 4, 17, 6, BLACK, top=1, side=1)
        P.rect(7, 7, 16, 16, (90, 80, 60)); P.rect(8, 8, 15, 15, glow); P.rect(10, 9, 13, 14, FLAME[4]); P.rect(7, 7, 7, 16, BLACK[1]); P.rect(16, 7, 16, 16, BLACK[1])
        P.box(6, 17, 17, 21, BLACK, top=1, side=1)
    P.selout()

@drawer("wreath", frames=4, ticks=[8, 2, 8, 2])
def wreath(P, v, f, nf):
    g = v.get("ramp", HOLLY); berry = v.get("berry", BERRY); bow = v.get("bow", CRIMSON)
    ring = P.ell_mask((2, 3, 21, 22)) - P.ell_mask((7, 8, 16, 17)); P.shade(ring, (2, 3, 21, 22), g)
    rr = _rng(7)
    for (x, y) in sorted(ring):
        if rr.random() < .12 and (x, y) in ring: P.put(x, y, g[3] if rr.random() < .6 else g[0])
    for (x, y) in [(5, 7), (17, 8), (4, 16), (18, 17), (11, 20)]:
        P.put(x, y, berry[2]); P.put(x + 1, y, berry[1]); P.put(x, y + 1, berry[1]); P.put(x + 1, y + 1, berry[0])
    if f == 1 or f == 3: P.sparkle(18, 8, 0, SPARK)
    if bow: P.sphere((7, 1, 11, 5), bow); P.sphere((12, 1, 16, 5), bow); P.rect(11, 2, 12, 4, bow[1]); P.rect(9, 5, 10, 8, bow[1]); P.rect(13, 5, 14, 8, bow[1])
    P.selout()

@drawer("lights", size=(32, 16), frames=4, ticks=[5, 5, 5, 5])
def lights(P, v, f, nf):
    cols = v["ramps"]
    for x in range(1, 31): P.put(x, 3 + int(round(math.sin(x / 5.0) * 1.5)) + 1, (40, 70, 40))
    for i in range(6):
        x = 3 + i * 5; y = 4 + int(round(math.sin(x / 5.0) * 1.5)) + 1; c = cols[i % len(cols)]; on = (i + f) % 3 != 0
        P.put(x, y + 1, (60, 60, 60));
        if on: P.sphere((x - 1, y + 2, x + 1, y + 5), c); P.put(x, y + 3, c[4])
        else: P.sphere((x - 1, y + 2, x + 1, y + 5), c, bands=(.9, .95, .97, .99))
    P.selout()

@drawer("bauble", frames=4, ticks=[8, 2, 8, 2])
def bauble(P, v, f, nf):
    c = v["ramp"]; sw = _sw(f, nf); P.rect(11 + sw // 2, 0, 12 + sw // 2, 3, (120, 110, 100)); P.rect(10 + sw, 4, 13 + sw, 5, GOLD[2]); P.put(10 + sw, 4, GOLD[3])
    P.sphere((4 + sw, 6, 19 + sw, 21), c, rim=True)
    pat = v.get("pat")
    if pat == "band": P.hline(5 + sw, 18 + sw, 13, c[4]); P.hline(5 + sw, 18 + sw, 14, c[0])
    if pat == "dots":
        for x, y in [(9, 11), (14, 10), (11, 15), (15, 15), (8, 16)]: P.put(x + sw, y, c[4])
    if pat == "zig":
        for x in range(5, 19): P.put(x + sw, 13 + (x % 2), c[4])
    P.selout(); P.sparkle(8 + sw, 9, 0, SPARK)

@drawer("star", size=(16, 16), frames=4, ticks=[8, 2, 4, 2])
def star(P, v, f, nf):
    c = v.get("ramp", GOLD); pts = []
    for i in range(10):
        r = 7 if i % 2 == 0 else 3; a = -math.pi / 2 + i * math.pi / 5; pts.append((8 + r * math.cos(a), 8 + r * math.sin(a)))
    P.poly(pts, c, box=(1, 1, 15, 15), bands=(.2, .45, .7, .9)); P.selout()
    if f == 1: P.sparkle(11, 4, 1, SPARK)
    if f == 3: P.sparkle(5, 11, 0, SPARK)

@drawer("heart", size=(16, 16), frames=4, ticks=[8, 2, 2, 4])
def heart(P, v, f, nf):
    c = v.get("ramp", CRIMSON); g = 1 if f in (1, 2) else 0
    P.sphere((1 - g, 2 - g, 8, 9), c); P.sphere((7, 2 - g, 14 + g, 9), c); P.poly([(1 - g, 7), (14 + g, 7), (7.5, 14 + g)], c, box=(1 - g, 2 - g, 14 + g, 14 + g)); P.sphere((2 - g, 3 - g, 13 + g, 13 + g), c)
    P.selout(); P.put(4, 5, c[4]); P.put(5, 4, c[4])

@drawer("bow", size=(16, 16), frames=4, ticks=[8, 2, 8, 2])
def bow(P, v, f, nf):
    c = v.get("ramp", CRIMSON); s = _sw(f, nf)
    P.sphere((0, 3 + s, 7, 10 + s), c, rim=True); P.sphere((8, 3 - s, 15, 10 - s), c, rim=True); P.poly([(5, 10), (2, 15 + s), (7, 13)], c, box=(2, 10, 7, 15)); P.poly([(10, 10), (13, 15 - s), (8, 13)], c, box=(8, 10, 13, 15))
    P.sphere((6, 5, 9, 9), c, bands=(.3, .5, .75, .95)); P.selout(); P.put(2, 5 + s, c[4]); P.put(13, 5 - s, c[4])

@drawer("rosette")
def rosette(P, v, f, nf):
    c = v["ramp"]; c2 = v.get("ramp2", GOLD)
    for i in range(12):
        a = 2 * math.pi * i / 12 + (f % 2) * .13; x = 12 + 7 * math.cos(a); y = 9 + 7 * math.sin(a); P.sphere((int(x) - 1, int(y) - 1, int(x) + 1, int(y) + 1), c)
    P.sphere((7, 4, 16, 13), c2); P.rect(9, 14, 10, 22, c[2]); P.rect(13, 14, 14, 21, c[2]); P.put(9, 22, c[1]); P.put(14, 21, c[1]); P.selout(); P.put(10, 6, c2[4])

@drawer("sign", frames=4, ticks=[8, 2, 8, 2])
def sign(P, v, f, nf):
    c = v.get("ramp", PAPER); s = _sw(f, nf); shape = v.get("shape", "rect")
    P.rect(11, 12, 12, 23, WOOD[2]); P.rect(12, 12, 12, 23, WOOD[1])
    if shape == "rect": P.box(2 + s, 2, 21 + s, 12, c, top=1, side=1)
    elif shape == "round": P.sphere((3 + s, 1, 20 + s, 13), c, flat=True); P.hline(5 + s, 18 + s, 13, c[1]); P.hline(5 + s, 18 + s, 1, c[3])
    else: P.poly([(2 + s, 2), (21 + s, 2), (18 + s, 7), (21 + s, 12), (2 + s, 12)], c, flat=True)
    P.selout()
    if v.get("tape"):
        P.rect(5 + s, 2, 7 + s, 3, (210, 200, 160)); P.rect(16 + s, 2, 18 + s, 3, (210, 200, 160))

@drawer("confetti", size=(24, 24), frames=4, ticks=[3, 3, 3, 3])
def confetti(P, v, f, nf):
    cols = v["ramps"]; rr = _rng(v.get("seed", 1))
    pts = [(rr.randrange(0, 24), rr.randrange(0, 24), rr.randrange(3)) for _ in range(16)]
    for i, (x, y, k) in enumerate(pts):
        yy = (y + f * 2 + i) % 24; c = cols[i % len(cols)]
        if k == 0: P.put(x, yy, c[2]); P.put(x + 1, yy, c[3])
        elif k == 1: P.put(x, yy, c[2]); P.put(x, yy + 1, c[1])
        else: P.put(x, yy, c[3])

@drawer("streamer", size=(16, 24), frames=4, ticks=[4, 4, 4, 4])
def streamer(P, v, f, nf):
    c = v["ramp"]
    for y in range(0, 24):
        x = 8 + int(round(2.5 * math.sin((y + f * 2) / 2.2))); P.put(x, y, c[2]); P.put(x + 1, y, c[1] if y % 3 else c[3])
    P.selout()

@drawer("party_hat", frames=4, ticks=[8, 2, 8, 2])
def party_hat(P, v, f, nf):
    c = v["ramp"]; c2 = v.get("ramp2", GOLD); s = _sw(f, nf)
    P.poly([(12 + s, 2), (4, 20), (20, 20)], c, box=(4, 2, 20, 20), shape="vcyl")
    if v.get("stripes"):
        for y in range(5, 20, 4):
            w = (y - 2) * 8 // 18; P.hline(12 - w // 2 + s * (20 - y) // 18, 12 + w // 2 + s * (20 - y) // 18, y, c2[2])
    if v.get("dots"):
        for x, y in [(11, 8), (9, 13), (14, 15), (12, 18), (16, 19)]: P.put(x, y, c2[3])
    P.hcyl((3, 20, 20, 21), c2); P.sphere((10 + s, 0, 14 + s, 4), c2); P.selout(); P.put(11 + s, 1, c2[4])

@drawer("hat")
def hat(P, v, f, nf):
    kind = v["kind"]; c = v["ramp"]; band = v.get("band", GOLD)
    if kind == "top":
        P.vcyl((6, 3, 17, 16), c); P.rect(6, 3, 17, 3, c[3]); P.hcyl((2, 16, 21, 19), c); P.rect(6, 13, 17, 15, band[2]); P.put(7, 13, band[3])
    elif kind == "stovepipe":
        P.vcyl((7, 1, 16, 17), c); P.rect(7, 1, 16, 1, c[3]); P.hcyl((3, 17, 20, 19), c); P.rect(7, 14, 16, 16, band[2])
    elif kind == "tricorne":
        P.sphere((6, 6, 17, 16), c, rim=True); P.poly([(1, 10), (6, 15), (12, 17), (18, 15), (23, 10), (21, 17), (12, 20), (3, 17)], c, box=(1, 10, 23, 20), bands=(.1, .3, .6, .9))
        P.hline(3, 21, 17, c[3]); P.put(1, 10, c[3]); P.put(23, 10, c[3]); P.rect(11, 15, 13, 17, band[2])
    elif kind == "hardhat":
        P.sphere((4, 4, 19, 17), c, rim=True); P.rect(4, 14, 19, 17, c[2]); P.hcyl((1, 17, 22, 19), c); P.rect(10, 6, 13, 13, c[3]); P.rect(9, 14, 14, 15, (80, 70, 60))
    elif kind == "pilgrim":
        P.vcyl((7, 2, 16, 15), c); P.rect(7, 2, 16, 2, c[3]); P.hcyl((2, 15, 21, 18), c); P.rect(7, 11, 16, 14, BLACK[1]); P.rect(10, 11, 13, 14, band[2]); P.rect(11, 12, 12, 13, c[1])
    elif kind == "santa":
        P.poly([(4, 15), (20, 15), (18, 4), (22, 2)], c, box=(4, 2, 22, 15)); P.hcyl((2, 14, 21, 18), SNOW); P.sphere((20, 0, 23, 3), SNOW)
    elif kind == "elf":
        P.poly([(4, 15), (20, 15), (14, 4), (10, 1)], v["ramp"], box=(4, 1, 20, 15)); P.hcyl((2, 14, 21, 18), CRIMSON); P.sphere((8, 0, 11, 3), GOLD)
    elif kind == "wizard":
        P.poly([(12, 0), (4, 18), (20, 18)], c, box=(4, 0, 20, 18), shape="vcyl"); P.hcyl((1, 18, 22, 20), c); P.sparkle(12, 10, 1, GOLD[3]); P.sparkle(9, 15, 0, GOLD[4])
    elif kind == "cap":
        P.sphere((4, 6, 17, 17), c, rim=True); P.rect(4, 13, 17, 17, c[2]); P.hcyl((10, 16, 22, 18), c); P.put(10, 6, c[4]); P.vline(10, 6, 12, c[1])
    elif kind == "beanie":
        P.sphere((4, 5, 19, 20), c, rim=True); P.hcyl((3, 16, 20, 21), c); P.hline(4, 19, 17, c[3]); P.hline(4, 19, 19, c[3]); P.sphere((9, 0, 14, 5), band)
    elif kind == "bowler":
        P.sphere((5, 5, 18, 16), c, rim=True); P.rect(5, 12, 18, 16, c[2]); P.hcyl((2, 16, 21, 18), c); P.rect(5, 13, 18, 14, band[2])
    P.selout()

@drawer("crown")
def crown(P, v, f, nf):
    c = v.get("ramp", GOLD); gem = v.get("gem", CRIMSON)
    P.box(4, 12, 19, 20, c, top=1, side=1); P.poly([(4, 12), (4, 4), (8, 10), (12, 2), (16, 10), (20, 4), (19, 12)], c, box=(4, 2, 20, 12), shape="vcyl")
    for x, y in [(4, 4), (12, 2), (19, 4)]: P.put(x, y - 1, c[4])
    P.rect(11, 14, 12, 17, gem[2]); P.put(11, 14, gem[4]); P.put(7, 15, gem[1]); P.put(16, 15, gem[1]); P.selout()

@drawer("bell", frames=4, ticks=[8, 2, 4, 2])
def bell(P, v, f, nf):
    c = v.get("ramp", GOLD); s = [0, -1, 0, 1][f % 4]
    P.rect(11, 1, 12, 3, c[1]); P.sphere((9, 0, 14, 3), c)
    P.poly([(12 + s, 3), (6 + s, 15), (18 + s, 15)], c, box=(6 + s, 3, 18 + s, 15), shape="vcyl"); P.sphere((7 + s, 2, 17 + s, 10), c, rim=True); P.hcyl((4 + s, 15, 19 + s, 17), c)
    P.sphere((10 + 2 * s, 17, 13 + 2 * s, 20), c, bands=(.3, .5, .7, .9)); P.selout(); P.put(9 + s, 6, c[4])
    if f == 2: P.put(3 + s, 10, SPARK); P.put(20 + s, 10, SPARK)

@drawer("dove", frames=4, ticks=[3, 3, 3, 3])
def dove(P, v, f, nf):
    c = v.get("ramp", SNOW); wing = [-4, -1, 2, -1][f % 4]
    P.sphere((6, 10, 19, 17), c, rim=True); P.sphere((15, 6, 21, 11), c); P.put(22, 9, GOLD[2]); P.put(16, 8, INK)
    P.poly([(8, 11), (12, 11), (14, 6 + wing), (6, 7 + wing)], c, box=(6, 4, 14, 12), bands=(.2, .4, .7, .95))
    P.poly([(6, 14), (2, 16), (2, 18), (7, 16)], c, box=(2, 14, 7, 18)); P.selout()
    if v.get("branch"): P.rect(20, 11, 23, 12, FOREST[2]); P.put(23, 10, FOREST[3])

@drawer("torch", frames=3, ticks=[3, 2, 3])
def torch(P, v, f, nf):
    h = v.get("ramp", GOLD); fl = FLAME
    P.poly([(9, 10), (14, 10), (13, 23), (10, 23)], h, box=(9, 10, 14, 23), shape="vcyl"); P.rect(8, 9, 15, 10, h[3]); P.rect(8, 10, 15, 11, h[1])
    shapes = [[(12, 1), (16, 5), (15, 9), (9, 9), (8, 5)], [(13, 0), (16, 4), (15, 9), (9, 9), (8, 6)], [(11, 1), (16, 6), (15, 9), (9, 9), (7, 4)]]
    P.poly(shapes[f % 3], fl, box=(7, 0, 16, 9)); P.rect(11, 5, 12, 8, (255, 246, 200)); P.selout()

@drawer("book")
def book(P, v, f, nf):
    c = v["ramp"]; pg = PAPER; open_ = v.get("open", False)
    if open_:
        P.poly([(2, 8), (12, 10), (12, 20), (2, 18)], pg, flat=True); P.poly([(12, 10), (22, 8), (22, 18), (12, 20)], pg, flat=True)
        P.rect(1, 7, 2, 19, c[2]); P.rect(22, 7, 23, 19, c[2]); P.hline(2, 22, 20, c[1]); P.put(12, 20, c[0])
        for y in (11, 13, 15): P.hline(4, 10, y, (170, 160, 140)); P.hline(14, 20, y, (170, 160, 140))
    else:
        P.box(5, 3, 18, 21, c, top=1, side=2); P.rect(17, 4, 18, 20, pg[2]); P.rect(6, 20, 18, 21, pg[1]); P.rect(7, 6, 14, 7, c[3]); P.rect(7, 9, 12, 9, c[3])
        if v.get("ribbon"): P.rect(14, 3, 15, 23, GOLD[2]); P.put(15, 23, GOLD[1])
    P.selout()

@drawer("scroll", frames=4, ticks=[8, 2, 8, 2])
def scroll(P, v, f, nf):
    c = v.get("ramp", PARCH); s = _sw(f, nf)
    P.rect(5, 4, 18, 19, c[2]); P.rect(5, 4, 18, 4, c[3]); P.rect(17, 5, 18, 19, c[1])
    P.hcyl((3, 1, 20, 5), c); P.hcyl((3, 18, 20, 22), c)
    for y in (8, 11, 14): P.hline(7, 15, y, c[0])
    if v.get("seal"): P.sphere((13, 13, 17, 17), CRIMSON); P.put(14, 14, CRIMSON[4])
    P.selout();
    if f == 1: P.sparkle(19 + s, 2, 0, SPARK)

@drawer("quill", frames=4, ticks=[8, 2, 8, 2])
def quill(P, v, f, nf):
    c = v.get("ramp", SNOW); s = _sw(f, nf)
    pts = [(20 + s, 1), (22 + s, 4), (15, 13), (9, 21), (7, 21), (11, 14)]; P.poly(pts, c, box=(7, 1, 22, 21), bands=(.2, .45, .7, .9))
    P.line(21 + s, 3, 8, 21, c[1]); P.rect(6, 21, 7, 22, INK); P.put(5, 23, INK)
    if v.get("ink"): P.box(14, 15, 22, 22, BLACK, top=1, side=1); P.rect(15, 14, 21, 15, BLACK[3]); P.rect(16, 12, 20, 14, BLACK[2])
    P.selout()

@drawer("podium")
def podium(P, v, f, nf):
    c = v.get("ramp", WOOD)
    P.box(6, 8, 17, 23, c, top=0, side=2); P.box(3, 5, 20, 9, c, top=1, side=2); P.rect(4, 4, 19, 4, c[3])
    P.rect(9, 12, 14, 17, c[3]); P.rect(10, 13, 13, 16, c[1]);
    if v.get("mic"): P.rect(16, 0, 16, 5, STEEL[2]); P.sphere((14, 0, 18, 3), BLACK)
    P.selout()

@drawer("microphone", frames=4, ticks=[8, 2, 8, 2])
def microphone(P, v, f, nf):
    c = v.get("ramp", STEEL); stand = v.get("stand", True); s = _sw(f, nf) if not stand else 0
    if stand: P.rect(11, 12, 12, 21, c[1]); P.hcyl((5, 21, 18, 23), BLACK)
    P.sphere((7 + s, 1, 16 + s, 10), BLACK, rim=True)
    for y in range(3, 9, 2): P.hline(8 + s, 15 + s, y, BLACK[3] if y != 5 else BLACK[1])
    P.poly([(9 + s, 10), (14 + s, 10), (13, 14 if stand else 22), (10, 14 if stand else 22)], c, box=(9, 10, 14, 22), shape="vcyl"); P.selout()
    if f == 1: P.put(5 + s, 4, SPARK); P.put(18 + s, 6, SPARK)

@drawer("megaphone", frames=4, ticks=[8, 2, 8, 2])
def megaphone(P, v, f, nf):
    c = v.get("ramp", CRIMSON)
    P.poly([(6, 9), (6, 14), (20, 20), (20, 3)], c, box=(6, 3, 20, 20), shape="hcyl"); P.vcyl((3, 8, 6, 15), c); P.rect(20, 3, 21, 20, c[3]); P.rect(9, 15, 11, 21, BLACK[2])
    P.selout()
    if f in (1, 3): P.put(22, 6, SPARK); P.put(23, 11, SPARK); P.put(22, 16, SPARK)

@drawer("drum", frames=4, ticks=[6, 2, 6, 2])
def drum(P, v, f, nf):
    c = v["ramp"]; skin = v.get("skin", PAPER); hit = f in (1, 3)
    P.vcyl((3, 8, 20, 20), c); P.hcyl((3, 6, 20, 9), skin); P.hcyl((3, 19, 20, 21), skin)
    for x in range(4, 20, 4): P.line(x, 9, x + 2, 19, c[4] if x % 8 == 4 else c[0])
    P.rect(16, 0 if hit else 1, 21, 5, None)
    P.line(15, 5 if hit else 2, 21, 1 if hit else 0, WOOD[2]); P.sphere((14, 4 if hit else 1, 16, 6 if hit else 3), SNOW)
    P.selout()
    if hit: P.put(11, 4, SPARK); P.put(8, 5, SPARK)

@drawer("tambourine", frames=4, ticks=[6, 2, 6, 2])
def tambourine(P, v, f, nf):
    c = v.get("ramp", WOOD); s = _sw(f, nf)
    ring = P.ell_mask((2 + s, 3, 21 + s, 20)) - P.ell_mask((5 + s, 6, 18 + s, 17)); P.shade(ring, (2 + s, 3, 21 + s, 20), c); P.shade(P.ell_mask((5 + s, 6, 18 + s, 17)), (5 + s, 6, 18 + s, 17), PAPER, bands=(.05, .2, .6, .95))
    for x, y in [(4, 6), (18, 6), (3, 14), (19, 14), (11, 20)]: P.rect(x + s, y, x + s + 1, y + 1, SILVER[3]); P.put(x + s, y, SILVER[4])
    P.selout()

@drawer("horn", frames=4, ticks=[6, 2, 6, 2])
def horn(P, v, f, nf):
    c = v["ramp"]; c2 = v.get("ramp2", GOLD); blow = f in (1, 3)
    P.poly([(3, 12), (3, 14), (19, 20), (19, 4)], c, box=(3, 4, 19, 20), shape="hcyl")
    for y in range(6, 19, 4): P.line(6 + (y - 6) // 3, y, 18, y - 1, c2[3])
    P.vcyl((19, 3, 21, 21), c2)
    if blow:
        P.rect(22, 8, 23, 9, c2[3]); P.rect(22, 14, 23, 15, c2[3]); P.put(23, 11, c2[4])
    P.selout()

@drawer("popper", frames=4, ticks=[8, 2, 3, 3])
def popper(P, v, f, nf):
    c = v["ramp"]; cols = v.get("bits", [GOLD, CRIMSON, LIME])
    P.poly([(5, 20), (8, 23), (19, 9), (16, 6)], c, box=(5, 6, 19, 23), shape="hcyl"); P.sphere((15, 5, 20, 10), c, bands=(.1, .3, .6, .9))
    if f >= 2:
        rr = _rng(f)
        for i in range(9):
            x = 17 + rr.randrange(-6, 7) + (f - 2) * 2; y = 5 - rr.randrange(0, 6) - (f - 2) * 2; cc = cols[i % len(cols)]; P.put(x, y, cc[3]); P.put(x + 1, y, cc[2])
        if f == 2: P.sparkle(20, 3, 1, SPARK)
    P.selout()

@drawer("disco", frames=4, ticks=[4, 4, 4, 4])
def disco(P, v, f, nf):
    c = SILVER; P.rect(11, 0, 12, 2, (120, 120, 120)); P.sphere((3, 3, 20, 20), c, rim=True)
    for y in range(4, 20):
        for x in range(4, 20):
            if P.get(x, y)[3] and (x + y + f) % 3 == 0: P.put(x, y, c[4] if (x * 3 + y + f) % 5 else c[0])
    P.selout(); P.sparkle(7 + f % 2 * 10, 6, 1, SPARK)

@drawer("clock", frames=4, ticks=[5, 5, 5, 5])
def clock(P, v, f, nf):
    c = v.get("ramp", GOLD); P.sphere((1, 1, 22, 22), c, rim=True); P.sphere((3, 3, 20, 20), PAPER, bands=(.05, .2, .6, .96))
    for i in range(12):
        a = i * math.pi / 6; x = 11.5 + 7.5 * math.cos(a); y = 11.5 + 7.5 * math.sin(a); P.put(int(x), int(y), c[0] if i % 3 else INK)
    P.line(11, 11, 11, 5, INK); P.line(12, 11, 12, 5, INK)  # hour hand straight up (midnight)
    a = -math.pi / 2 - 0.35 + f * 0.12; P.line(11, 11, int(11.5 + 7 * math.cos(a)), int(11.5 + 7 * math.sin(a)), (150, 40, 40))
    P.put(11, 11, c[2]); P.put(12, 11, c[2]); P.selout()

@drawer("ball_drop", size=(24, 32), frames=4, ticks=[4, 4, 4, 4])
def ball_drop(P, v, f, nf):
    P.rect(11, 0, 12, 31, STEEL[1]); P.rect(11, 0, 11, 31, STEEL[3]); dy = f * 3
    P.sphere((4, 2 + dy, 19, 17 + dy), SILVER, rim=True)
    for y in range(3 + dy, 17 + dy):
        for x in range(5, 19):
            if P.get(x, y)[3] and (x + y * 2 + f) % 4 == 0: P.put(x, y, GOLD[4])
    P.rect(6, 29, 17, 31, BLACK[2]); P.selout(); P.sparkle(16, 4 + dy, 1, SPARK)

@drawer("hourglass", frames=4, ticks=[6, 6, 6, 6])
def hourglass(P, v, f, nf):
    c = v.get("ramp", WOOD); glass = ICE; P.hcyl((4, 1, 19, 3), c); P.hcyl((4, 20, 19, 22), c); P.rect(4, 3, 4, 20, c[1]); P.rect(19, 3, 19, 20, c[1])
    top = P.poly_mask([(6, 4), (17, 4), (12, 11), (11, 11)]); bot = P.poly_mask([(11, 12), (12, 12), (17, 19), (6, 19)])
    P.shade(top | bot, (6, 4, 17, 19), glass, bands=(.02, .1, .6, .95)); sand = WHEAT
    lvl = 4 + f * 2
    for (x, y) in top:
        if y >= lvl: P.put(x, y, sand[2] if y > lvl else sand[3])
    for (x, y) in bot:
        if y >= 19 - f * 2: P.put(x, y, sand[2])
    P.vline(11, 12, 18 - f * 2, sand[3]); P.selout()

@drawer("champagne", frames=4, ticks=[8, 2, 3, 6])
def champagne(P, v, f, nf):
    g = v.get("ramp", R((40, 90, 60))); foil = GOLD
    P.vcyl((8, 9, 15, 23), g); P.poly([(9, 4), (14, 4), (15, 10), (8, 10)], g, box=(8, 4, 15, 10), shape="vcyl"); P.vcyl((9, 0, 14, 5), foil)
    P.rect(9, 12, 14, 16, PAPER[2]); P.rect(10, 13, 13, 13, g[1]); P.rect(10, 15, 13, 15, g[1]); P.put(8, 12, g[4]); P.vline(9, 10, 22, g[3])
    if f >= 2:
        P.sphere((10, -3 + (f - 2) * -2 + 2, 13, 0 + 2), foil) if False else None
        P.rect(11, 0, 12, 1, SPARK); P.put(10, 1, SPARK); P.put(13, 0, SPARK)
        if f == 2: P.sparkle(16, 2, 1, SPARK)
        P.rect(9, 0, 14, 0, (240, 240, 230))
    P.selout()

@drawer("glass", frames=4, ticks=[6, 6, 6, 6])
def glass(P, v, f, nf):
    kind = v.get("kind", "flute"); liq = v.get("liq", R((240, 210, 120))); gl = ICE
    if kind == "flute":
        P.poly([(8, 2), (15, 2), (14, 14), (9, 14)], gl, box=(8, 2, 15, 14), shape="vcyl", bands=(.02, .1, .6, .95)); P.poly([(9, 5), (14, 5), (13, 13), (10, 13)], liq, box=(9, 5, 14, 13), shape="vcyl")
        P.rect(11, 14, 12, 20, gl[2]); P.hcyl((7, 20, 16, 22), gl);
        for i in range(3): P.put(10 + (i * 2) % 3, 12 - ((f * 2 + i * 3) % 7), liq[4])
    elif kind == "mug":
        P.vcyl((5, 6, 16, 21), gl, bands=(.02, .1, .6, .95)); P.vcyl((6, 8, 15, 20), liq); P.hcyl((6, 6, 15, 9), SNOW); P.rect(17, 9, 19, 17, gl[2]); P.rect(19, 10, 19, 16, gl[1]); P.rect(18, 11, 18, 15, None)
        P.put(7, 9, liq[4])
    elif kind == "cup":
        P.poly([(6, 4), (17, 4), (15, 20), (8, 20)], v.get("ramp", CRIMSON), box=(6, 4, 17, 20), shape="vcyl"); P.hcyl((6, 3, 17, 5), v.get("ramp", CRIMSON)); P.rect(8, 6, 15, 7, PAPER[2])
        s = (f % 2); P.put(10, 1 - s + 1, (200, 200, 200)); P.put(13, 2 - s, (200, 200, 200))
    elif kind == "pitcher":
        P.vcyl((5, 6, 16, 21), gl, bands=(.02, .1, .6, .95)); P.vcyl((6, 10, 15, 20), liq); P.hcyl((4, 4, 17, 7), gl, bands=(.02, .1, .6, .95)); P.rect(17, 8, 19, 16, gl[2]); P.rect(18, 10, 18, 14, None); P.put(3, 5, gl[3])
        for i in range(3): P.put(8 + i * 3, 18 - ((f + i * 2) % 6), liq[4])
        if v.get("lemon"): P.sphere((7, 11, 10, 14), YELLOW); P.sphere((12, 13, 15, 16), YELLOW)
    P.selout()

@drawer("bottle", frames=4, ticks=[8, 2, 8, 2])
def bottle(P, v, f, nf):
    g = v.get("ramp", CRIMSON); cap = v.get("cap", SILVER); s = 0
    P.vcyl((8, 8, 15, 22), g); P.poly([(10, 2), (13, 2), (15, 9), (8, 9)], g, box=(8, 2, 15, 9), shape="vcyl"); P.hcyl((9, 0, 14, 2), cap)
    P.rect(9, 12, 14, 17, PAPER[2]); P.rect(10, 14, 13, 15, g[1]); P.vline(9, 9, 21, g[3])
    P.selout()
    if f == 1: P.put(16, 10, SPARK)

@drawer("mug", frames=4, ticks=[5, 5, 5, 5])
def mug(P, v, f, nf):
    c = v["ramp"]; liq = v.get("liq", CHOC)
    P.vcyl((5, 8, 16, 21), c); P.hcyl((5, 7, 16, 9), c); P.hcyl((6, 8, 15, 9), liq); P.rect(17, 11, 19, 18, c[2]); P.rect(19, 12, 19, 17, c[1]); P.rect(18, 13, 18, 16, None)
    if v.get("marsh"): P.rect(8, 7, 10, 8, SNOW[3]); P.rect(12, 7, 14, 8, SNOW[2])
    if v.get("stripe"): P.hline(5, 16, 14, c[4]); P.hline(5, 16, 16, c[4])
    for i in range(3):
        y = 5 - ((f + i * 2) % 5); x = 8 + i * 3 + ((f + i) % 2); P.put(x, y, (215, 215, 210)); P.put(x, y - 1, (190, 190, 186)) if y > 0 else None
    P.selout()

@drawer("teapot")
def teapot(P, v, f, nf):
    c = v["ramp"]; P.sphere((4, 8, 19, 21), c, rim=True); P.hcyl((8, 6, 15, 8), c); P.sphere((10, 4, 13, 7), c); P.poly([(19, 11), (23, 7), (23, 9), (20, 15)], c, box=(19, 7, 23, 15), shape="hcyl")
    P.rect(1, 9, 3, 10, c[2]); P.rect(1, 10, 1, 17, c[1]); P.rect(2, 17, 4, 18, c[2]); P.put(7, 11, c[4])
    if f % 2: P.put(23, 4, (215, 215, 210)); P.put(22, 2, (190, 190, 186))
    P.selout()

# ---------------------------------------------------------------- food and drink
@drawer("pie", frames=4, ticks=[8, 2, 8, 2])
def pie(P, v, f, nf):
    crust = v.get("ramp", CARAMEL); fill = v.get("fill", PUMPKIN); slice_ = v.get("slice", False)
    if slice_:
        P.poly([(2, 20), (22, 20), (12, 4)], fill, box=(2, 4, 22, 20), bands=(.1, .3, .6, .9)); P.poly([(2, 20), (22, 20), (22, 23), (2, 23)], crust, flat=True); P.hline(2, 22, 23, crust[1])
        P.poly([(2, 20), (12, 4), (14, 6), (5, 20)], crust, box=(2, 4, 14, 20), bands=(.1, .3, .6, .9)); P.sphere((10, 1, 14, 5), SNOW)
    else:
        P.poly([(1, 13), (22, 13), (20, 21), (3, 21)], STEEL, box=(1, 13, 22, 21), shape="vcyl")   # the tin
        P.sphere((2, 7, 21, 17), fill, bands=(.1, .3, .6, .9)); P.rect(2, 13, 21, 15, fill[2]); P.hline(2, 21, 15, fill[1])
        ring = P.ell_mask((1, 10, 22, 17)) - P.ell_mask((3, 11, 20, 16)); P.shade({(x, y) for x, y in ring if y <= 14}, (1, 10, 22, 17), crust)
        for x in range(2, 22, 2): P.put(x, 11 + (x % 4 == 0), crust[3])
        if v.get("lattice"):
            for x in range(5, 19, 4): P.vline(x, 8, 12, crust[3]); P.vline(x + 1, 8, 12, crust[2])
            for y in range(8, 13, 3): P.hline(4, 19, y, crust[3])
        else:
            for x in range(5, 19, 3): P.put(x, 9 + (x % 2), fill[4])
    s = f % 2
    P.put(8, 4 - s, (215, 215, 210)); P.put(14, 3 + s, (215, 215, 210)); P.selout()

@drawer("cake", frames=4, ticks=[8, 2, 8, 2])
def cake(P, v, f, nf):
    c = v["ramp"]; ice = v.get("ice", SNOW); layers = v.get("layers", 2)
    y = 22
    for i in range(layers):
        w = 18 - i * 4; x0 = 12 - w // 2; h = 6; P.box(x0, y - h, x0 + w - 1, y, c, top=0, side=2); P.hcyl((x0, y - h - 1, x0 + w - 1, y - h + 1), ice)
        for x in range(x0 + 1, x0 + w - 1, 3): P.put(x, y - h + 2, ice[2]); P.put(x, y - h + 3, ice[1])
        y -= h + 1
    if v.get("candle"):
        P.rect(11, y - 5, 12, y, CRIMSON[2]); fl = [(11, y - 7), (12, y - 8), (11, y - 8)][f % 3]; P.put(fl[0], fl[1], FLAME[3]); P.put(12, y - 6, FLAME[4]); P.put(11, y - 6, FLAME[3])
    elif v.get("cherry"): P.sphere((10, y - 4, 13, y - 1), CRIMSON); P.put(12, y - 5, FOREST[2])
    P.selout()

@drawer("cupcake", frames=4, ticks=[8, 2, 8, 2])
def cupcake(P, v, f, nf):
    cup = v.get("ramp", PINK); frost = v.get("frost", SNOW)
    P.poly([(5, 13), (18, 13), (16, 22), (7, 22)], cup, box=(5, 13, 18, 22), shape="vcyl")
    for x in range(6, 18, 3): P.vline(x, 14, 21, cup[1])
    P.sphere((4, 8, 19, 15), frost); P.sphere((7, 4, 16, 10), frost); P.sphere((9, 1, 14, 6), frost)
    if v.get("sprinkles"):
        for i, (x, y) in enumerate([(7, 10), (12, 5), (15, 9), (10, 8), (14, 12), (9, 12)]): P.put(x, y, [CRIMSON, BLUE, GOLD][i % 3][3])
    if v.get("cherry"): P.sphere((10, 0, 13, 3), CRIMSON)
    P.selout()

@drawer("cookie")
def cookie(P, v, f, nf):
    kind = v.get("kind", "round"); c = v.get("ramp", CARAMEL)
    if kind == "round":
        P.sphere((3, 3, 20, 20), c, bands=(.08, .25, .6, .92))
        for x, y in [(8, 8), (13, 7), (10, 13), (15, 14), (7, 15)]: P.put(x, y, CHOC[1]); P.put(x + 1, y, CHOC[2])
    elif kind == "ginger":
        g = R((190, 120, 60)); P.sphere((8, 1, 15, 8), g); P.box(8, 8, 15, 15, g, top=0, side=1); P.poly([(2, 8), (8, 9), (8, 12), (3, 12)], g, box=(2, 8, 8, 12)); P.poly([(15, 9), (21, 8), (20, 12), (15, 12)], g, box=(15, 8, 21, 12))
        P.rect(8, 15, 10, 22, g[2]); P.rect(13, 15, 15, 22, g[2]); P.put(10, 4, INK); P.put(13, 4, INK); P.hline(10, 13, 6, SNOW[3]); P.put(11, 10, SNOW[3]); P.put(12, 13, SNOW[3]); P.hline(8, 15, 9, SNOW[2]) if False else None
        P.rect(8, 15, 15, 15, SNOW[2]); P.hline(2, 3, 9, SNOW[2]); P.hline(20, 21, 9, SNOW[2]); P.hline(8, 10, 21, SNOW[2]); P.hline(13, 15, 21, SNOW[2])
    elif kind == "star":
        pts = [(12 + (9 if i % 2 == 0 else 4) * math.cos(-math.pi / 2 + i * math.pi / 5), 12 + (9 if i % 2 == 0 else 4) * math.sin(-math.pi / 2 + i * math.pi / 5)) for i in range(10)]
        P.poly(pts, c, box=(3, 3, 21, 21), bands=(.1, .3, .6, .9)); P.sparkle(12, 10, 0, SNOW[3])
    elif kind == "heart":
        P.sphere((2, 4, 12, 13), c); P.sphere((11, 4, 21, 13), c); P.poly([(2, 10), (21, 10), (11.5, 21)], c, box=(2, 4, 21, 21)); P.sphere((3, 5, 20, 19), c); P.put(7, 8, PINK[3]); P.put(14, 10, PINK[3])
    P.selout()

@drawer("candy_cane")
def candy_cane(P, v, f, nf):
    c = v.get("ramp", CRIMSON); w = SNOW
    cells = set((x, y) for x in range(9, 14) for y in range(8, 23)) | P.ell_mask((9, 1, 19, 11)) - P.ell_mask((13, 5, 15, 11)) - set((x, y) for x in range(14, 20) for y in range(7, 12))
    cells |= set((x, y) for x in range(15, 19) for y in range(6, 11))
    P.shade(cells, (9, 1, 19, 23), w, shape="vcyl")
    for (x, y) in cells:
        if (x + y) % 4 in (0, 1): P.put(x, y, c[2] if P.get(x, y)[:3] != w[3] else c[3])
    P.selout()

@drawer("lollipop", frames=4, ticks=[8, 2, 8, 2])
def lollipop(P, v, f, nf):
    c = v.get("ramp", PINK); c2 = v.get("ramp2", SNOW); s = _sw(f, nf)
    P.rect(11, 14, 12, 23, PAPER[2]); P.sphere((4 + s, 1, 19 + s, 16), c, rim=True)
    for i in range(0, 60, 2):
        a = i / 6.0; r = 1 + i / 9.0; x = int(round(11.5 + s + r * math.cos(a))); y = int(round(8.5 + r * math.sin(a)))
        if P.get(x, y)[3]: P.put(x, y, c2[2])
    P.selout()

@drawer("hotdog", size=(24, 16))
def hotdog(P, v, f, nf):
    bun = v.get("ramp", CARAMEL); sausage = R((200, 72, 52))
    P.hcyl((2, 7, 21, 14), bun); P.hcyl((2, 7, 21, 9), bun, bands=(.0, .1, .3, .9))
    P.hcyl((1, 3, 22, 9), sausage); P.put(3, 5, sausage[4]); P.put(4, 4, sausage[4])
    if v.get("mustard"):
        for x in range(4, 20): P.put(x, 5 + (x // 2) % 2, MUSTARD[3])
    if v.get("ketchup"):
        for x in range(5, 20): P.put(x, 6 - (x // 2) % 2, CRIMSON[3])
    P.selout()

@drawer("burger")
def burger(P, v, f, nf):
    bun = v.get("ramp", CARAMEL)
    P.sphere((3, 2, 20, 12), bun); P.rect(3, 9, 20, 12, bun[2]); P.hline(4, 19, 12, bun[1]); P.hcyl((3, 12, 20, 14), GREEN); P.hcyl((4, 13, 19, 15), MUSTARD); P.hcyl((3, 15, 20, 18), CHOC); P.hcyl((3, 18, 20, 21), bun)
    for x, y in [(8, 5), (13, 4), (16, 7), (6, 8)]: P.put(x, y, bun[4])
    if v.get("tomato"): P.hcyl((4, 14, 19, 15), CRIMSON)
    P.selout()

@drawer("corn", frames=4, ticks=[8, 2, 8, 2])
def corn(P, v, f, nf):
    k = v.get("ramp", YELLOW); husk = GRASS
    P.vcyl((8, 2, 15, 18), k)
    for y in range(3, 18):
        for x in range(8, 16):
            if (x + y) % 2 == 0 and P.get(x, y)[3]: P.put(x, y, k[3] if x < 12 else k[1])
    P.poly([(8, 12), (3, 23), (7, 22), (10, 16)], husk, box=(3, 12, 10, 23)); P.poly([(15, 12), (20, 23), (16, 22), (13, 16)], husk, box=(13, 12, 20, 23)); P.poly([(9, 15), (14, 15), (13, 23), (10, 23)], husk, box=(9, 15, 14, 23), shape="vcyl")
    if v.get("butter"): P.rect(10, 5, 13, 7, SNOW[4]); P.rect(10, 7, 13, 7, GOLD[3])
    P.selout()

@drawer("watermelon")
def watermelon(P, v, f, nf):
    rind = GRASS; flesh = R((230, 70, 90)); whole = v.get("whole", False)
    if whole:
        P.sphere((2, 3, 21, 20), rind, rim=True)
        for x in range(3, 21, 3): P.vline(x + (1 if x % 2 else 0), 4, 19, rind[0]) if P.get(x, 10)[3] else None
    else:
        P.poly([(1, 7), (22, 7), (12, 21)], flesh, box=(1, 7, 22, 21), bands=(.1, .3, .6, .95)); P.poly([(1, 7), (22, 7), (22, 9), (1, 9)], SNOW, flat=True); P.hline(1, 22, 6, rind[2]); P.hline(1, 22, 5, rind[3])
        for x, y in [(7, 11), (12, 12), (16, 11), (10, 15), (14, 16)]: P.put(x, y, INK); P.put(x, y + 1, (50, 40, 44))
    P.selout()

@drawer("popsicle", frames=4, ticks=[8, 2, 8, 2])
def popsicle(P, v, f, nf):
    cols = v.get("ramps", [CRIMSON, SNOW, BLUE]); P.rect(10, 15, 13, 23, WOOD[2]); P.rect(13, 15, 13, 23, WOOD[1])
    P.sphere((6, 1, 17, 8), cols[0]); P.rect(6, 5, 17, 16, cols[0][2]); P.rect(16, 5, 17, 16, cols[0][1])
    n = len(cols); h = 12 // n
    for i, c in enumerate(cols):
        y0 = 4 + i * h; P.rect(6, y0, 17, y0 + h, c[2]); P.rect(16, y0, 17, y0 + h, c[1]); P.vline(7, y0, y0 + h, c[3])
    P.sphere((6, 1, 17, 8), cols[0]); P.put(8, 3, cols[0][4])
    if f == 1: P.put(5, 14, ICE[3]); P.put(6, 17, ICE[3])
    P.selout()

@drawer("ice_cream")
def ice_cream(P, v, f, nf):
    scoops = v.get("ramps", [PINK, SNOW]); cone = CARAMEL
    P.poly([(6, 12), (17, 12), (12, 23)], cone, box=(6, 12, 17, 23), shape="vcyl")
    for y in range(13, 22, 3): P.hline(7 + (y - 12) // 2, 16 - (y - 12) // 2, y, cone[0])
    y = 13
    for c in scoops: P.sphere((4, y - 9, 19, y + 1), c, rim=True); y -= 6
    if v.get("cherry"): P.sphere((10, max(0, y + 1), 13, max(0, y + 1) + 3), CRIMSON)
    P.selout()

@drawer("turkey", size=(32, 24), frames=4, ticks=[8, 2, 8, 2])
def turkey(P, v, f, nf):
    skin = R((200, 120, 60)); plate = v.get("plate", SNOW); steam = f % 2
    P.hcyl((1, 17, 30, 22), plate); P.hline(2, 29, 22, plate[1])
    P.sphere((7, 5, 25, 19), skin, rim=True); P.sphere((21, 8, 28, 15), skin); P.sphere((4, 9, 10, 15), skin)
    P.rect(24, 3, 25, 8, (240, 220, 200)); P.rect(6, 3, 7, 8, (240, 220, 200)); P.rect(23, 2, 26, 3, SNOW[3]); P.rect(5, 2, 8, 3, SNOW[3])
    P.put(12, 8, skin[4]); P.put(13, 7, skin[4]); P.put(16, 10, skin[3])
    if v.get("garnish"):
        for x in (3, 27): P.sphere((x, 15, x + 2, 17), FOREST); P.sphere((x + 1, 14, x + 3, 16), CRIMSON)
    P.put(14, 1 + steam, (215, 215, 210)); P.put(18, 2 - steam, (215, 215, 210)); P.selout()

@drawer("pumpkin", frames=4, ticks=[8, 2, 8, 2])
def pumpkin(P, v, f, nf):
    c = v.get("ramp", PUMPKIN); P.sphere((2, 6, 21, 22), c, rim=True)
    for x in (7, 12, 16): P.vline(x, 8, 20, c[1]) if P.get(x, 14)[3] else None
    P.vline(8, 8, 20, c[3]); P.rect(11, 2, 13, 6, FOREST[2]); P.put(13, 2, FOREST[1]); P.put(11, 3, FOREST[3])
    if v.get("leaf"): P.poly([(14, 3), (19, 1), (18, 5)], GRASS, box=(14, 1, 19, 5))
    P.selout()

@drawer("gravy", frames=4, ticks=[8, 2, 8, 2])
def gravy(P, v, f, nf):
    c = v.get("ramp", SNOW); g = CHOC; P.hcyl((3, 19, 20, 22), c); P.poly([(4, 10), (19, 10), (17, 19), (6, 19)], c, box=(4, 10, 19, 19), shape="vcyl"); P.poly([(2, 8), (5, 10), (5, 13), (2, 11)], c, box=(2, 8, 5, 13))
    P.hcyl((5, 10, 18, 12), g); P.rect(20, 11, 22, 17, c[2]); P.rect(22, 12, 22, 16, c[1]); P.put(7, 11, g[3])
    if f % 2: P.put(10, 7, (215, 215, 210)); P.put(13, 6, (215, 215, 210))
    P.selout()

@drawer("can")
def can(P, v, f, nf):
    c = v.get("ramp", CRIMSON); P.vcyl((6, 4, 17, 21), c); P.hcyl((6, 2, 17, 5), SILVER); P.hcyl((6, 20, 17, 22), SILVER); P.rect(7, 9, 16, 14, PAPER[2]); P.rect(8, 11, 15, 12, c[1]); P.vline(7, 6, 19, c[3]); P.selout()

@drawer("basket", frames=4, ticks=[8, 2, 8, 2])
def basket(P, v, f, nf):
    c = v.get("ramp", WHEAT); goods = v.get("goods", "eggs")
    P.poly([(3, 12), (20, 12), (18, 22), (5, 22)], c, box=(3, 12, 20, 22), shape="vcyl")
    for y in range(13, 22, 2):
        for x in range(4, 20, 2): P.put(x + (y // 2) % 2, y, c[1])
    ring = P.ell_mask((4, 1, 19, 14)) - P.ell_mask((6, 3, 17, 14)) - set((x, y) for x in range(0, 24) for y in range(12, 24)); P.shade(ring, (4, 1, 19, 14), c)
    if goods == "eggs":
        for i, (x, cc) in enumerate([(5, PASTEL_PINK), (10, PASTEL_BLUE), (15, PASTEL_YEL)]): P.sphere((x, 8 + (i % 2), x + 4, 13 + (i % 2)), cc); P.put(x + 1, 9 + (i % 2), cc[4])
    elif goods == "food":
        P.sphere((5, 8, 9, 12), CRIMSON); P.sphere((10, 7, 14, 11), GRASS); P.rect(15, 6, 18, 12, CARAMEL[2]); P.put(16, 6, CARAMEL[3])
    elif goods == "flowers":
        for i, (x, cc) in enumerate([(5, CRIMSON), (10, GOLD), (15, LILAC)]): P.rect(x + 1, 7, x + 1, 11, GRASS[2]); P.sphere((x - 1, 4 + (i % 2), x + 3, 8 + (i % 2)), cc)
    P.hline(4, 19, 12, c[3]); P.selout()

@drawer("egg", size=(16, 16))
def egg(P, v, f, nf):
    c = v["ramp"]; pat = v.get("pat", "dots"); c2 = v.get("ramp2", SNOW)
    P.sphere((3, 1, 12, 14), c, rim=True)
    if pat == "dots":
        for x, y in [(6, 4), (9, 6), (5, 8), (8, 10), (10, 3)]: P.put(x, y, c2[3])
    elif pat == "zig":
        for x in range(4, 12): P.put(x, 7 + (x % 2), c2[3])
    elif pat == "bands": P.hline(4, 11, 5, c2[3]); P.hline(3, 12, 9, c2[3])
    P.selout()

@drawer("bun")
def bun(P, v, f, nf):
    c = v.get("ramp", CARAMEL); P.sphere((3, 5, 20, 20), c, rim=True); P.hline(4, 19, 12, SNOW[3]); P.vline(11, 6, 19, SNOW[3]); P.put(12, 12, SNOW[4]); P.selout()

@drawer("carrot", frames=4, ticks=[8, 2, 8, 2])
def carrot(P, v, f, nf):
    c = v.get("ramp", PUMPKIN); s = _sw(f, nf)
    P.poly([(8, 7), (15, 7), (12, 23)], c, box=(8, 7, 15, 23), shape="vcyl")
    for y in (11, 15, 19): P.hline(10, 13, y, c[1])
    P.poly([(11, 7), (7 + s, 0), (12, 6)], GRASS, box=(7, 0, 12, 7)); P.poly([(12, 7), (16 + s, 0), (13, 6)], GRASS, box=(12, 0, 16, 7)); P.rect(11, 1, 12, 7, GRASS[2]); P.selout()

@drawer("cherries", frames=4, ticks=[8, 2, 8, 2])
def cherries(P, v, f, nf):
    c = v.get("ramp", CRIMSON); s = _sw(f, nf)
    P.line(7 + s, 12, 12, 2, FOREST[2]); P.line(16 - s, 12, 12, 2, FOREST[2]); P.put(12, 2, FOREST[1]); P.poly([(12, 2), (17, 0), (15, 4)], GRASS, box=(12, 0, 17, 4))
    P.sphere((3 + s, 12, 11 + s, 20), c, rim=True); P.sphere((12 - s, 13, 20 - s, 21), c, rim=True); P.put(5 + s, 14, c[4]); P.put(14 - s, 15, c[4]); P.selout()

# ---------------------------------------------------------------- nature and animals
@drawer("tree", size=(32, 32), frames=4, ticks=[5, 5, 5, 5])
def tree(P, v, f, nf):
    g = v.get("ramp", FOREST); lights = v.get("lights"); snow = v.get("snow")
    P.rect(14, 26, 17, 31, WOOD[2]); P.rect(17, 26, 17, 31, WOOD[1])
    for i, (y0, y1, hw) in enumerate([(4, 13, 8), (10, 20, 11), (16, 27, 14)]):
        P.poly([(16, y0), (16 - hw, y1), (16 + hw, y1)], g, box=(16 - hw, y0, 16 + hw, y1), shape="vcyl")
        if snow:
            for x in range(16 - hw + 1, 16 + hw): P.put(x, y1 - (x % 3 == 0), SNOW[2]) if P.get(x, y1)[3] else None
    if lights:
        pts = [(13, 9), (19, 11), (10, 16), (22, 17), (16, 14), (8, 23), (24, 24), (14, 21), (19, 25), (12, 26)]
        for i, (x, y) in enumerate(pts):
            c = lights[i % len(lights)]; on = (i + f) % 3 != 0; P.put(x, y, c[4] if on else c[1])
            if on and f % 2 == 0 and i % 4 == 0: P.sparkle(x, y, 1, c[4])
    if v.get("star"):
        for dx, dy in ((0, 0), (-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1)): P.put(16 + dx, 2 + dy, GOLD[3] if (dx, dy) != (0, 0) else GOLD[4])
    if v.get("baubles"):
        for i, (x, y) in enumerate([(12, 12), (20, 18), (10, 24), (21, 25), (16, 19)]): P.put(x, y, [CRIMSON, GOLD, BLUE][i % 3][2]); P.put(x, y - 1, [CRIMSON, GOLD, BLUE][i % 3][4])
    P.selout()

@drawer("snowman", frames=4, ticks=[8, 2, 8, 2])
def snowman(P, v, f, nf):
    s = _sw(f, nf); P.sphere((3, 12, 20, 23), SNOW, rim=True); P.sphere((6, 3, 17, 14), SNOW, rim=True)
    P.put(9, 7, INK); P.put(13, 7, INK); P.rect(11, 9, 13, 9, PUMPKIN[2]); P.put(14, 9, PUMPKIN[3])
    for y in (16, 19): P.put(11, y, INK)
    scarf = v.get("scarf", CRIMSON); P.hcyl((6, 12, 17, 14), scarf); P.rect(15 + s, 14, 17 + s, 19, scarf[2]); P.put(16 + s, 19, scarf[1])
    if v.get("hat"): P.rect(7, 2, 16, 3, BLACK[2]); P.rect(9, -1 + 1, 14, 2, BLACK[2]); P.rect(9, 0, 14, 0, BLACK[3])
    P.line(3, 16, 0, 12, WOOD[1]); P.line(20, 16, 23, 12 - s, WOOD[1]); P.selout()

@drawer("snowflake", size=(16, 16), frames=4, ticks=[6, 6, 6, 6])
def snowflake(P, v, f, nf):
    c = v.get("color", ICE[4]); k = f % 2
    for i in range(6):
        a = i * math.pi / 3 + k * math.pi / 6
        for r in range(1, 7): P.put(int(round(8 + r * math.cos(a))), int(round(8 + r * math.sin(a))), c if r < 6 else ICE[3])
        for r in (4,):
            for sgn in (-1, 1):
                b = a + sgn * .6; P.put(int(round(8 + r * math.cos(a) + 2 * math.cos(b))), int(round(8 + r * math.sin(a) + 2 * math.sin(b))), c)
    P.put(8, 8, SNOW[4])

@drawer("stocking", frames=4, ticks=[8, 2, 8, 2])
def stocking(P, v, f, nf):
    c = v.get("ramp", CRIMSON); s = _sw(f, nf)
    P.box(7 + s, 4, 15 + s, 15, c, top=0, side=2); P.sphere((5, 13, 19, 22), c, rim=True); P.rect(7, 13, 15, 17, c[2]); P.hcyl((6 + s, 2, 16 + s, 6), SNOW)
    if v.get("stripes"):
        for y in (8, 11): P.hline(8 + s, 14 + s, y, SNOW[2])
    if v.get("gift"): P.rect(9 + s, 0, 13 + s, 3, GREEN[2]); P.rect(11 + s, 0, 11 + s, 3, GOLD[3])
    P.put(8, 19, c[4]) if False else None; P.selout()

@drawer("mistletoe", frames=4, ticks=[8, 2, 8, 2])
def mistletoe(P, v, f, nf):
    g = GRASS; s = _sw(f, nf); P.rect(11, 0, 12, 8, WOOD[1])
    for (x, y, fl) in [(4, 8, False), (14, 9, True), (3, 15, True), (15, 16, False)]:
        pts = [(x, y + 2), (x + 7, y), (x + 8, y + 4), (x + 1, y + 6)] if fl else [(x, y), (x + 7, y + 2), (x + 6, y + 6), (x - 1, y + 4)]
        P.poly([(px + s // 2, py) for px, py in pts], g, box=(x - 1, y, x + 8, y + 6))
    for x, y in [(10, 12), (13, 12), (11, 15)]: P.sphere((x, y, x + 2, y + 2), SNOW); P.put(x, y, SNOW[4])
    P.sphere((8, 1, 11, 4), CRIMSON); P.sphere((12, 1, 15, 4), CRIMSON); P.rect(11, 2, 12, 3, CRIMSON[1]); P.selout()

@drawer("fireplace", size=(32, 32), frames=3, ticks=[3, 2, 3])
def fireplace(P, v, f, nf):
    brick = v.get("ramp", R((150, 70, 50))); P.box(2, 4, 29, 30, brick, top=1, side=1)
    for y in range(6, 30, 3):
        for x in range(3, 29, 6): P.put(x + (3 if (y // 3) % 2 else 0), y, brick[1])
    P.rect(7, 10, 24, 28, (30, 24, 28)); P.rect(0, 2, 31, 4, WOOD[2]); P.rect(0, 2, 31, 2, WOOD[3])
    P.hcyl((9, 24, 22, 27), WOOD); P.hcyl((11, 21, 20, 24), WOOD)
    shapes = [[(15, 11), (19, 15), (18, 22), (12, 22), (11, 16)], [(16, 10), (20, 16), (18, 22), (12, 22), (12, 15)], [(14, 12), (19, 14), (19, 22), (12, 22), (10, 17)]]
    P.poly(shapes[f % 3], FLAME, box=(10, 10, 20, 22)); P.rect(14, 16, 16, 21, (255, 240, 180))
    if v.get("stockings"):
        P.rect(6, 5, 8, 9, CRIMSON[2]); P.rect(5, 9, 9, 10, CRIMSON[1]); P.rect(22, 5, 24, 9, GREEN[2]); P.rect(21, 9, 25, 10, GREEN[1])
    P.selout()

@drawer("snowglobe", frames=4, ticks=[4, 4, 4, 4])
def snowglobe(P, v, f, nf):
    P.sphere((3, 1, 20, 18), ICE, bands=(.02, .1, .5, .9)); P.box(5, 17, 18, 22, WOOD, top=1, side=1)
    P.sphere((8, 8, 15, 15), SNOW); P.sphere((9, 3, 14, 9), SNOW); P.put(10, 5, INK); P.put(13, 5, INK)
    rr = _rng(3)
    for i in range(10):
        x = 4 + rr.randrange(16); y = (2 + rr.randrange(14) + f * 2) % 15 + 2
        if P.get(x, y)[:3] in (ICE[2], ICE[3], ICE[1]): P.put(x, y, SNOW[4])
    P.selout(); P.put(6, 4, SNOW[4]); P.put(7, 4, SNOW[4])

@drawer("flower", frames=4, ticks=[8, 2, 8, 2])
def flower(P, v, f, nf):
    kind = v.get("kind", "tulip"); c = v["ramp"]; s = _sw(f, nf); st = GRASS
    P.rect(11, 12, 12, 23, st[2]); P.rect(12, 12, 12, 23, st[1]); P.poly([(11, 18), (5, 15 + s), (9, 21)], st, box=(5, 15, 11, 21)); P.poly([(12, 16), (18, 12 - s), (15, 19)], st, box=(12, 12, 18, 19))
    if kind == "tulip":
        P.poly([(6 + s, 4), (17 + s, 4), (15 + s, 13), (8 + s, 13)], c, box=(6, 4, 17, 13), shape="vcyl"); P.sphere((6 + s, 2, 11 + s, 7), c); P.sphere((12 + s, 2, 17 + s, 7), c); P.sphere((9 + s, 1, 14 + s, 6), c)
    elif kind == "daffodil":
        for i in range(6):
            a = i * math.pi / 3; P.sphere((int(11.5 + s + 5 * math.cos(a)) - 2, int(7.5 + 5 * math.sin(a)) - 2, int(11.5 + s + 5 * math.cos(a)) + 2, int(7.5 + 5 * math.sin(a)) + 2), c)
        P.vcyl((9 + s, 5, 14 + s, 10), PUMPKIN); P.hline(9 + s, 14 + s, 5, PUMPKIN[3])
    elif kind == "poppy":
        for i in range(4):
            a = i * math.pi / 2 + .4; P.sphere((int(11.5 + s + 4 * math.cos(a)) - 3, int(7.5 + 4 * math.sin(a)) - 3, int(11.5 + s + 4 * math.cos(a)) + 3, int(7.5 + 4 * math.sin(a)) + 3), c)
        P.sphere((10 + s, 6, 13 + s, 9), BLACK)
    elif kind == "sunflower":
        for i in range(10):
            a = i * math.pi / 5; x = int(round(11.5 + s + 6 * math.cos(a))); y = int(round(7.5 + 6 * math.sin(a))); P.sphere((x - 1, y - 2, x + 1, y + 2) if abs(math.sin(a)) > .7 else (x - 2, y - 1, x + 2, y + 1), c)
        P.sphere((8 + s, 4, 15 + s, 11), CHOC)
        for x in range(9, 15, 2): P.put(x + s, 6 + (x % 4) // 2, CHOC[0])
    elif kind == "rose":
        P.sphere((6 + s, 2, 17 + s, 13), c, rim=True); P.sphere((9 + s, 4, 14 + s, 9), c, bands=(.3, .5, .75, .95)); P.put(11 + s, 6, c[0]); P.put(8 + s, 10, c[0]); P.put(14 + s, 8, c[0])
    elif kind == "lily":
        for i in range(6):
            a = -math.pi / 2 + i * math.pi / 3; P.poly([(12 + s, 8), (12 + s + 6 * math.cos(a - .35), 8 + 6 * math.sin(a - .35)), (12 + s + 7 * math.cos(a), 8 + 7 * math.sin(a)), (12 + s + 6 * math.cos(a + .35), 8 + 6 * math.sin(a + .35))], c, box=(5, 1, 19, 15))
        P.put(12 + s, 8, GOLD[3]); P.put(11 + s, 7, GOLD[4])
    elif kind == "hibiscus":
        for i in range(5):
            a = -math.pi / 2 + i * 2 * math.pi / 5; x = int(round(11.5 + s + 5 * math.cos(a))); y = int(round(7.5 + 5 * math.sin(a))); P.sphere((x - 3, y - 3, x + 3, y + 3), c)
        P.line(12 + s, 8, 15 + s, 3, GOLD[3]); P.put(15 + s, 2, GOLD[4])
    P.selout()

@drawer("leaf", size=(16, 16), frames=4, ticks=[6, 6, 6, 6])
def leaf(P, v, f, nf):
    c = v["ramp"]; kind = v.get("kind", "maple"); s = [0, 1, 0, -1][f % 4]
    if kind == "maple":
        pts = [(8, 1), (10, 5), (14, 4), (12, 8), (15, 11), (10, 11), (8, 15), (6, 11), (1, 11), (4, 8), (2, 4), (6, 5)]
        P.poly([(x + s, y) for x, y in pts], c, box=(1, 1, 15, 15), bands=(.1, .3, .6, .9)); P.line(8 + s, 3, 8, 14, c[0])
    elif kind == "oak":
        P.sphere((4 + s, 1, 11 + s, 7), c); P.sphere((3 + s, 5, 12 + s, 11), c); P.sphere((5, 9, 10, 14), c); P.vline(8, 2, 15, c[0])
    else:
        P.poly([(8 + s, 0), (14, 6), (8, 15), (2, 6)], c, box=(2, 0, 14, 15)); P.line(8 + s, 1, 8, 14, c[0])
    P.selout()

@drawer("acorn", size=(16, 16))
def acorn(P, v, f, nf):
    P.sphere((4, 5, 11, 14), CARAMEL, rim=True); P.sphere((3, 2, 12, 8), CHOC); P.rect(3, 6, 12, 7, CHOC[2]); P.rect(7, 0, 8, 2, WOOD[1])
    for x in range(4, 12, 2): P.put(x, 4, CHOC[3])
    P.selout(); P.put(6, 8, CARAMEL[4])

@drawer("wheat", size=(16, 24), frames=4, ticks=[8, 2, 8, 2])
def wheat(P, v, f, nf):
    c = WHEAT; s = _sw(f, nf)
    P.line(8, 23, 8 + s, 8, c[1])
    for i in range(6):
        y = 2 + i * 2; P.sphere((6 + s, y, 8 + s, y + 2), c); P.sphere((8 + s, y + 1, 10 + s, y + 3), c)
    P.put(7 + s, 0, c[3]); P.put(9 + s, 1, c[3]); P.selout()

@drawer("cornucopia", size=(32, 24))
def cornucopia(P, v, f, nf):
    c = WHEAT; P.poly([(2, 6), (10, 2), (20, 6), (24, 12), (20, 20), (10, 22), (3, 16)], c, box=(2, 2, 24, 22), shape="hcyl")
    for y in range(4, 21, 3): P.line(4, y, 22, y + 2, c[1])
    P.sphere((18, 8, 24, 16), (40, 30, 30) and R((60, 44, 40)), bands=(.5, .7, .9, .97))
    P.sphere((22, 10, 27, 15), CRIMSON); P.sphere((25, 13, 30, 18), PUMPKIN); P.sphere((20, 14, 25, 19), PLUM); P.sphere((26, 8, 30, 12), GRASS); P.rect(28, 15, 31, 20, YELLOW[2]); P.put(28, 15, YELLOW[3])
    P.selout()

@drawer("chick", size=(16, 16), frames=4, ticks=[8, 2, 8, 2])
def chick(P, v, f, nf):
    c = YELLOW; dy = [0, -1, 0, 0][f % 4]; P.sphere((3, 6 + dy, 13, 15), c, rim=True); P.sphere((5, 1 + dy, 12, 8 + dy), c); P.put(10, 4 + dy, INK); P.put(12, 5 + dy, PUMPKIN[2]); P.put(13, 5 + dy, PUMPKIN[3])
    P.poly([(3, 9 + dy), (0, 7 + dy), (3, 12 + dy)], c, box=(0, 7, 3, 12)); P.put(6, 15, PUMPKIN[2]); P.put(9, 15, PUMPKIN[2]); P.put(8, 0 + dy, c[3]); P.selout()

@drawer("bunny", frames=4, ticks=[8, 2, 8, 2])
def bunny(P, v, f, nf):
    c = v.get("ramp", SNOW); s = [0, -1, 0, 0][f % 4]
    P.sphere((4, 12, 19, 23), c, rim=True); P.sphere((7, 6, 17, 15), c, rim=True)
    P.sphere((8, 0 + s, 11, 8), c); P.sphere((13, 0, 16, 8), c); P.rect(9, 2 + s, 10, 6, PINK[3]); P.rect(14, 2, 15, 6, PINK[3])
    P.put(10, 9, INK); P.put(14, 9, INK); P.put(12, 11, PINK[2]); P.put(2, 18, c[3]) if False else None; P.sphere((18, 16, 22, 20), c)
    P.put(8, 12, PINK[3]); P.put(16, 12, PINK[3]); P.selout()

@drawer("lamb", frames=4, ticks=[8, 2, 8, 2])
def lamb(P, v, f, nf):
    w = SNOW; dy = [0, 0, -1, 0][f % 4]; P.sphere((3, 7 + dy, 20, 18 + dy), w, rim=True)
    for x, y in [(5, 8), (10, 7), (15, 7), (18, 10), (6, 16), (12, 17)]: P.sphere((x, y + dy, x + 3, y + 3 + dy), w)
    P.sphere((15, 9 + dy, 22, 16 + dy), BLACK); P.put(19, 11 + dy, SNOW[4]); P.put(15, 9 + dy, BLACK[1]); P.put(21, 8 + dy, BLACK[2])
    for x in (6, 10, 14, 17): P.rect(x, 18, x + 1, 22, BLACK[2])
    P.selout()

@drawer("butterfly", frames=4, ticks=[3, 3, 3, 3])
def butterfly(P, v, f, nf):
    c = v["ramp"]; k = [4, 2, 0, 2][f % 4]
    P.sphere((5 + k, 3, 11, 12), c, rim=True); P.sphere((12, 3, 18 - k, 12), c, rim=True); P.sphere((6 + k, 11, 11, 18), c); P.sphere((12, 11, 17 - k, 18), c)
    P.rect(11, 4, 12, 18, BLACK[2]); P.put(11, 4, BLACK[3]); P.line(11, 3, 8, 0, BLACK[1]); P.line(12, 3, 15, 0, BLACK[1])
    for x, y in [(8 + k // 2, 7), (15 - k // 2, 7), (8 + k // 2, 14), (15 - k // 2, 14)]: P.put(x, y, SNOW[4])
    P.selout()

@drawer("bee", size=(16, 16), frames=4, ticks=[2, 2, 2, 2])
def bee(P, v, f, nf):
    k = f % 2; P.sphere((3, 6, 13, 13), YELLOW, rim=True); P.vline(6, 7, 12, BLACK[2]); P.vline(9, 7, 12, BLACK[2]); P.sphere((11, 7, 15, 11), BLACK); P.put(13, 8, SNOW[4]); P.put(2, 10, BLACK[1])
    P.sphere((4, 2 - k, 8, 6 - k), ICE, bands=(.02, .2, .6, .95)); P.sphere((8, 1 + k, 12, 5 + k), ICE, bands=(.02, .2, .6, .95)); P.selout()

@drawer("ladybug", size=(16, 16))
def ladybug(P, v, f, nf):
    P.sphere((2, 4, 13, 14), CRIMSON, rim=True); P.sphere((10, 5, 15, 11), BLACK); P.vline(7, 5, 13, BLACK[1])
    for x, y in [(4, 7), (5, 11), (9, 8), (8, 12)]: P.put(x, y, INK)
    P.put(14, 6, SNOW[4]); P.put(15, 4, BLACK[1]); P.put(14, 3, BLACK[1]); P.selout()

@drawer("raincloud", frames=4, ticks=[4, 4, 4, 4])
def raincloud(P, v, f, nf):
    c = v.get("ramp", GREY); P.sphere((2, 6, 12, 14), c); P.sphere((8, 2, 19, 13), c); P.sphere((13, 7, 22, 14), c); P.rect(4, 11, 20, 14, c[2]); P.hline(5, 19, 14, c[1]); P.selout()
    for i, x in enumerate((5, 9, 13, 17)): y = 16 + ((f * 2 + i * 3) % 7); P.put(x, y, ICE[3]); P.put(x, y + 1, ICE[2])
    if v.get("sun"): P.sphere((15, 0, 23, 8), GOLD)

@drawer("umbrella", frames=4, ticks=[8, 2, 8, 2])
def umbrella(P, v, f, nf):
    c = v["ramp"]; c2 = v.get("ramp2", c)
    P.rect(11, 10, 12, 20, WOOD[2]); P.rect(12, 20, 13, 22, WOOD[2]); P.rect(13, 22, 14, 22, WOOD[1]); P.put(11, 0, STEEL[3])
    dome = P.ell_mask((1, 2, 22, 18)) - set((x, y) for x in range(24) for y in range(11, 24)); P.shade(dome, (1, 2, 22, 18), c, bands=(.1, .3, .6, .9))
    for x in range(2, 22):
        if (x // 5) % 2: 
            for y in range(2, 11):
                if (x, y) in dome: P.put(x, y, c2[2] if P.get(x, y)[:3] == c[2] else c2[1] if P.get(x, y)[:3] == c[1] else c2[3])
    for x in range(1, 23, 5): P.put(x, 11, c[1])
    P.selout()
    if f == 1: P.put(3, 14, ICE[3]); P.put(20, 15, ICE[3])

@drawer("boots")
def boots(P, v, f, nf):
    c = v["ramp"]; work = v.get("work", False)
    for x in (3, 13):
        P.box(x, 4, x + 6, 16, c, top=1, side=2); P.sphere((x, 13, x + 9, 21), c); P.rect(x, 17, x + 9, 21, c[2]); P.hline(x, x + 9, 21, c[1])
        P.hcyl((x, 21, x + 9, 23), RUBBER if work else BLACK)
        if work: P.rect(x + 1, 5, x + 5, 6, CARAMEL[3]); P.hline(x + 1, x + 5, 9, CARAMEL[1]); P.hline(x + 1, x + 5, 12, CARAMEL[1])
        else: P.hline(x + 1, x + 5, 5, c[3])
    P.selout()

@drawer("watering_can", frames=4, ticks=[6, 2, 6, 2])
def watering_can(P, v, f, nf):
    c = v.get("ramp", STEEL); P.box(5, 9, 16, 21, c, top=1, side=2); P.hcyl((5, 7, 16, 10), c); P.rect(8, 4, 13, 7, c[2]); P.poly([(16, 12), (22, 6), (23, 8), (17, 15)], c, box=(16, 6, 23, 15), shape="hcyl"); P.sphere((20, 4, 23, 8), c)
    P.rect(2, 11, 4, 12, c[2]); P.rect(2, 12, 2, 18, c[1]); P.rect(3, 18, 5, 19, c[2])
    if f % 2:
        for i, (x, y) in enumerate([(21, 10), (22, 12), (20, 13)]): P.put(x, y + (f // 2), ICE[3])
    P.selout()

@drawer("sprout", size=(16, 24), frames=4, ticks=[8, 8, 8, 8])
def sprout(P, v, f, nf):
    pot = v.get("ramp", R((190, 110, 70))); P.poly([(3, 14), (12, 14), (11, 23), (4, 23)], pot, box=(3, 14, 12, 23), shape="vcyl"); P.hcyl((2, 12, 13, 15), pot); P.hline(4, 11, 15, CHOC[1])
    h = 3 + f * 2; P.rect(7, 13 - h, 8, 13, GRASS[2])
    if f >= 1: P.sphere((3, 11 - h, 7, 14 - h), GRASS)
    if f >= 2: P.sphere((8, 10 - h, 12, 13 - h), GRASS)
    if f >= 3: P.sphere((6, 8 - h, 9, 11 - h), PASTEL_PINK)
    P.selout()

@drawer("kite", frames=4, ticks=[4, 4, 4, 4])
def kite(P, v, f, nf):
    c = v["ramp"]; c2 = v.get("ramp2", SNOW); s = _sw(f, nf)
    P.poly([(12, 0), (20, 7), (12, 17), (4, 7)], c, box=(4, 0, 20, 17), bands=(.1, .3, .6, .9)); P.poly([(12, 0), (20, 7), (12, 7)], c2, box=(4, 0, 20, 17)); P.poly([(12, 7), (12, 17), (4, 7)], c2, box=(4, 0, 20, 17))
    P.vline(12, 1, 16, c[0]); P.hline(5, 19, 7, c[0])
    for i in range(4): y = 18 + i; x = 12 - i + (s if i > 1 else 0); P.put(x, y, (190, 190, 186)); P.put(x - 1, y, [CRIMSON, GOLD][i % 2][3]) if i % 2 else None
    P.selout()

@drawer("pinwheel", frames=4, ticks=[2, 2, 2, 2])
def pinwheel(P, v, f, nf):
    cols = v.get("ramps", [CRIMSON, SNOW, BLUE, SNOW]); P.rect(11, 12, 12, 23, WOOD[2]); rot = f * math.pi / 8
    for i in range(4):
        a = i * math.pi / 2 + rot; c = cols[i % len(cols)]
        P.poly([(12, 8), (12 + 7 * math.cos(a), 8 + 7 * math.sin(a)), (12 + 7 * math.cos(a + .55), 8 + 7 * math.sin(a + .55)), (12 + 4 * math.cos(a + 1.1), 8 + 4 * math.sin(a + 1.1))], c, box=(4, 0, 20, 16), bands=(.1, .3, .6, .9))
    P.put(12, 8, GOLD[3]); P.selout()

@drawer("sparkler", frames=4, ticks=[2, 2, 2, 2])
def sparkler(P, v, f, nf):
    P.rect(11, 9, 12, 23, STEEL[2]); rr = _rng(f + 10)
    for i in range(10):
        a = 2 * math.pi * i / 10 + f * .4; r = 3 + rr.randrange(4); x = int(round(11.5 + r * math.cos(a))); y = int(round(7.5 + r * math.sin(a))); P.put(x, y, SPARK if i % 2 else GOLD[4])
    P.sparkle(11, 7, 1, SPARK); P.put(12, 8, SPARK)

@drawer("rocket", frames=4, ticks=[3, 3, 3, 3])
def rocket(P, v, f, nf):
    c = v.get("ramp", SNOW); c2 = v.get("ramp2", CRIMSON)
    P.vcyl((8, 6, 15, 17), c); P.poly([(12, 0), (8, 7), (15, 7)], c2, box=(8, 0, 15, 7), shape="vcyl"); P.poly([(8, 13), (4, 20), (8, 18)], c2, box=(4, 13, 8, 20)); P.poly([(15, 13), (19, 20), (15, 18)], c2, box=(15, 13, 19, 20))
    P.sphere((10, 9, 13, 12), ICE); P.put(11, 10, SNOW[4]); P.rect(10, 17, 13, 18, c2[1])
    fl = [FLAME, EMBER, FLAME, R((250, 220, 120))][f % 4]; P.poly([(10, 19), (13, 19), (12, 21 + f % 2 + 1), (11, 21 + f % 2 + 1)], fl, box=(10, 19, 13, 23)); P.selout()

@drawer("liberty", frames=4, ticks=[8, 2, 8, 2])
def liberty(P, v, f, nf):
    kind = v.get("kind", "crown"); c = R((100, 170, 150))
    if kind == "crown":
        P.hcyl((3, 14, 20, 20), c)
        for i, x in enumerate((3, 7, 11, 15, 19)): P.poly([(x, 14), (x + 1, 14), (x + (0 if i == 2 else (-2 if i < 2 else 2)), 3 + abs(i - 2) * 2)], c, box=(1, 3, 22, 14)); 
        P.hline(4, 19, 16, c[3]); P.selout()
    else:
        P.poly([(9, 12), (14, 12), (13, 23), (10, 23)], c, box=(9, 12, 14, 23), shape="vcyl"); P.rect(8, 11, 15, 12, c[3]); P.hcyl((7, 9, 16, 12), c)
        shapes = [[(12, 1), (16, 5), (15, 9), (9, 9), (8, 5)], [(13, 0), (16, 4), (15, 9), (9, 9), (8, 6)], [(11, 1), (16, 6), (15, 9), (9, 9), (7, 4)]]
        P.poly(shapes[f % 3], FLAME, box=(7, 0, 16, 9)); P.rect(11, 5, 12, 8, (255, 246, 200)); P.selout()

@drawer("coin", size=(16, 16), frames=4, ticks=[4, 4, 4, 4])
def coin(P, v, f, nf):
    c = v.get("ramp", GOLD); w = [12, 8, 4, 8][f % 4]; x0 = 8 - w // 2
    if w >= 8: P.sphere((x0, 2, x0 + w - 1, 13), c, rim=True); P.sphere((x0 + 2, 4, x0 + w - 3, 11), c, bands=(.3, .5, .75, .95)) if w == 12 else None; P.put(x0 + 3, 5, c[4])
    else: P.vcyl((x0, 2, x0 + w - 1, 13), c)
    if w == 12: P.sparkle(12, 3, 1, SPARK)
    P.selout()

@drawer("monument", size=(16, 32))
def monument(P, v, f, nf):
    c = R((210, 206, 196), dark=.72); P.poly([(8, 0), (6, 4), (10, 4)], c, box=(6, 0, 10, 4), shape="vcyl"); P.poly([(6, 4), (10, 4), (11, 28), (5, 28)], c, box=(5, 4, 11, 28), shape="vcyl"); P.box(3, 28, 13, 31, c, top=1, side=1); P.vline(6, 5, 27, c[3]); P.selout()

@drawer("columns", size=(24, 24))
def columns(P, v, f, nf):
    c = R((210, 206, 196), dark=.72); P.poly([(12, 1), (1, 7), (23, 7)], c, box=(1, 1, 23, 7), shape="vcyl"); P.box(1, 7, 22, 9, c, top=1, side=1)
    for x in (3, 10, 17): P.vcyl((x, 10, x + 4, 20), c); P.rect(x - 1, 9, x + 5, 10, c[3]); P.rect(x - 1, 20, x + 5, 21, c[2])
    P.box(0, 21, 23, 23, c, top=1, side=1); P.selout()

@drawer("dome", size=(24, 24))
def dome(P, v, f, nf):
    c = R((210, 206, 196), dark=.72); P.sphere((4, 2, 19, 15), c, rim=True); P.rect(11, 0, 12, 2, GOLD[2]); P.put(11, 0, GOLD[4]); P.box(2, 12, 21, 16, c, top=1, side=1)
    for x in (3, 8, 13, 18): P.vcyl((x, 16, x + 2, 22), c)
    P.box(1, 22, 22, 23, c, top=1, side=0); P.selout()

@drawer("axe", frames=4, ticks=[8, 2, 8, 2])
def axe(P, v, f, nf):
    s = _sw(f, nf); P.line(6, 22, 16 + s, 4, WOOD[2]); P.line(7, 22, 17 + s, 4, WOOD[1])
    P.poly([(14 + s, 2), (21 + s, 4), (21 + s, 10), (15 + s, 10), (13 + s, 7)], STEEL, box=(13, 2, 21, 10), bands=(.1, .3, .6, .95)); P.vline(21 + s, 4, 10, SNOW[4]); P.selout()

@drawer("log", size=(24, 16))
def log(P, v, f, nf):
    P.hcyl((3, 3, 20, 13), WOOD); P.sphere((17, 3, 23, 13), CARAMEL, bands=(.1, .3, .6, .9)); P.sphere((19, 6, 21, 10), CARAMEL, bands=(.3, .5, .7, .9)); P.put(20, 8, CARAMEL[0])
    for x in range(4, 18, 4): P.hline(x, x + 2, 6 + (x % 3), WOOD[0])
    P.selout()

@drawer("ballot", frames=4, ticks=[8, 2, 8, 2])
def ballot(P, v, f, nf):
    c = v.get("ramp", WOOD); P.box(3, 8, 20, 22, c, top=1, side=2); P.rect(8, 7, 15, 8, BLACK[1]); P.rect(9, 7, 14, 7, INK)
    dy = [0, -2, -4, -1][f % 4]; P.rect(9, 1 + dy, 14, 6 + dy, PAPER[2]); P.rect(14, 1 + dy, 14, 6 + dy, PAPER[1]); P.hline(10, 13, 3 + dy, (170, 160, 140))
    P.rect(5, 12, 18, 17, c[3]); P.selout()

@drawer("letter", frames=4, ticks=[8, 2, 8, 2])
def letter(P, v, f, nf):
    c = v.get("ramp", PAPER); P.box(2, 6, 21, 19, c, top=1, side=1); P.line(2, 6, 11, 13, c[1]); P.line(21, 6, 12, 13, c[1]); P.line(2, 19, 9, 13, c[1]); P.line(21, 19, 14, 13, c[1])
    P.sphere((9, 11, 14, 16), CRIMSON); P.put(11, 12, CRIMSON[4]); P.selout()
    if f == 1: P.sparkle(19, 8, 0, SPARK)

@drawer("medal", frames=4, ticks=[8, 2, 8, 2])
def medal(P, v, f, nf):
    rb = v.get("ribbon", CRIMSON); c = v.get("ramp", GOLD); s = _sw(f, nf)
    P.poly([(7, 0), (10, 0), (12 + s, 12), (9 + s, 12)], rb, box=(7, 0, 12, 12)); P.poly([(13, 0), (16, 0), (14 + s, 12), (11 + s, 12)], rb, box=(11, 0, 16, 12)); P.vline(8, 0, 10, rb[3])
    P.sphere((5 + s, 10, 18 + s, 23), c, rim=True); P.sphere((8 + s, 13, 15 + s, 20), c, bands=(.3, .5, .75, .95)); P.sparkle(11 + s, 16, 0, c[4]); P.selout()

@drawer("folded_flag", size=(24, 16))
def folded_flag(P, v, f, nf):
    P.poly([(2, 14), (22, 14), (12, 1)], NAVY, box=(2, 1, 22, 14), bands=(.1, .3, .6, .9)); P.poly([(2, 14), (12, 14), (7, 7)], FLAG_WHITE, box=(2, 7, 12, 14), bands=(.1, .3, .6, .9)); P.poly([(12, 14), (22, 14), (17, 7)], CRIMSON, box=(12, 7, 22, 14), bands=(.1, .3, .6, .9))
    for x, y in [(12, 5), (10, 9), (14, 9), (12, 11)]: P.put(x, y, FLAG_WHITE[4])
    P.hline(2, 22, 14, NAVY[0]); P.selout()

@drawer("bugle", frames=4, ticks=[8, 2, 8, 2])
def bugle(P, v, f, nf):
    c = v.get("ramp", GOLD); P.poly([(3, 10), (3, 13), (16, 17), (19, 6)], c, box=(3, 6, 19, 17), shape="hcyl"); P.vcyl((19, 4, 22, 19), c); P.hcyl((5, 8, 15, 10), c); P.hcyl((5, 13, 15, 15), c); P.sphere((1, 10, 4, 13), c); P.selout()
    if f == 1: P.put(23, 8, SPARK); P.put(23, 14, SPARK)

@drawer("poppy_pin", size=(16, 16))
def poppy_pin(P, v, f, nf):
    for i in range(4):
        a = i * math.pi / 2 + .5; x = int(round(7.5 + 3.5 * math.cos(a))); y = int(round(6.5 + 3.5 * math.sin(a))); P.sphere((x - 3, y - 3, x + 3, y + 3), CRIMSON)
    P.sphere((6, 5, 9, 8), BLACK); P.rect(7, 10, 8, 15, GRASS[2]); P.poly([(9, 12), (13, 10), (10, 14)], GRASS, box=(9, 10, 13, 14)); P.selout()

@drawer("laurel", frames=4, ticks=[8, 2, 8, 2])
def laurel(P, v, f, nf):
    g = v.get("ramp", GRASS)
    for side in (-1, 1):
        for i in range(6):
            a = math.pi / 2 + side * (0.25 + i * 0.32); x = 12 + 9 * math.cos(a); y = 13 - 9 * math.sin(a) + 9 - 9
            P.poly([(x, y), (x + side * 3, y - 3), (x + side * 1, y - 5)], g, box=(1, 1, 23, 23)) if False else P.sphere((int(x) - 2, int(y) - 1, int(x) + 2, int(y) + 1), g)
        P.line(12, 22, 12 + side * 9, 9, g[1])
    P.sphere((11, 20, 13, 22), GOLD); P.selout()

@drawer("peace", size=(16, 16))
def peace(P, v, f, nf):
    c = v.get("ramp", SNOW); ring = P.ell_mask((1, 1, 14, 14)) - P.ell_mask((3, 3, 12, 12)); P.shade(ring, (1, 1, 14, 14), c); P.vline(7, 2, 13, c[2]); P.vline(8, 2, 13, c[2]); P.line(7, 8, 3, 12, c[2]); P.line(8, 8, 12, 12, c[2]); P.selout()

@drawer("gavel", frames=4, ticks=[8, 2, 8, 2])
def gavel(P, v, f, nf):
    c = v.get("ramp", WOOD); hit = f in (1, 3)
    P.hcyl((2, 19, 21, 23), c); P.hline(3, 20, 19, c[3])
    if hit: P.hcyl((6, 10, 19, 16), c); P.rect(11, 2, 12, 10, c[1]); P.put(4, 17, SPARK); P.put(21, 17, SPARK)
    else: P.line(12, 18, 19, 6, c[1]); P.line(13, 18, 20, 6, c[2]); P.poly([(14, 2), (23, 6), (20, 11), (11, 7)], c, box=(11, 2, 23, 11), shape="hcyl")
    P.selout()

@drawer("scales", frames=4, ticks=[8, 2, 8, 2])
def scales(P, v, f, nf):
    c = v.get("ramp", GOLD); t = [0, 1, 0, -1][f % 4]
    P.rect(11, 3, 12, 20, c[1]); P.hcyl((5, 20, 18, 23), c); P.line(2, 7 + t, 21, 7 - t, c[2]); P.put(11, 2, c[4])
    for x, dy in ((3, t), (20, -t)):
        P.line(x, 8 + dy, x - 2 if x < 12 else x + 2, 13 + dy, c[1]); P.line(x, 8 + dy, x + 2 if x < 12 else x - 2, 13 + dy, c[1]); P.hcyl((x - 3, 13 + dy, x + 3, 15 + dy), c)
    P.selout()

@drawer("pin", size=(16, 24), frames=4, ticks=[8, 2, 8, 2])
def pin(P, v, f, nf):
    c = v.get("ramp", CRIMSON); dy = [0, -1, 0, 0][f % 4]; P.sphere((2, 1 + dy, 13, 12 + dy), c, rim=True); P.poly([(3, 9 + dy), (12, 9 + dy), (8, 20 + dy), (7, 20 + dy)], c, box=(2, 1, 13, 20), shape="vcyl"); P.sphere((5, 4 + dy, 10, 9 + dy), SNOW); P.hcyl((4, 21, 11, 23), BLACK, bands=(.6, .8, .9, .97)); P.selout()

# ---------------------------------------------------------------- tools and gear
@drawer("toolbox")
def toolbox(P, v, f, nf):
    c = v.get("ramp", CRIMSON); P.box(2, 10, 21, 21, c, top=1, side=2); P.box(2, 7, 21, 10, c, top=1, side=2); P.rect(9, 4, 14, 7, STEEL[2]); P.rect(9, 4, 9, 7, STEEL[3]); P.rect(10, 5, 13, 6, None)
    P.rect(11, 9, 12, 11, STEEL[3]); P.hline(3, 20, 10, c[0]); P.selout()

@drawer("wrench", frames=4, ticks=[8, 2, 8, 2])
def wrench(P, v, f, nf):
    c = STEEL; s = _sw(f, nf); P.line(7, 20, 15 + s, 6, c[2]); P.line(8, 20, 16 + s, 6, c[2]); P.line(6, 20, 14 + s, 6, c[1]); P.sphere((13 + s, 1, 21 + s, 9), c, rim=True); P.rect(16 + s, 1, 18 + s, 5, None); P.sphere((4, 17, 9, 22), c); P.selout()

@drawer("hammer", frames=4, ticks=[8, 2, 8, 2])
def hammer(P, v, f, nf):
    s = _sw(f, nf); P.line(8, 22, 14 + s, 8, WOOD[2]); P.line(9, 22, 15 + s, 8, WOOD[1]); P.box(9 + s, 3, 21 + s, 9, STEEL, top=1, side=2); P.rect(19 + s, 3, 21 + s, 9, STEEL[1]); P.put(10 + s, 4, SNOW[4]); P.selout()

@drawer("screwdriver", frames=4, ticks=[8, 2, 8, 2])
def screwdriver(P, v, f, nf):
    c = v.get("ramp", CRIMSON); s = _sw(f, nf); P.line(10, 23, 13 + s, 12, STEEL[2]); P.line(11, 23, 14 + s, 12, STEEL[3]); P.poly([(10 + s, 1), (16 + s, 1), (17 + s, 12), (11 + s, 12)], c, box=(10, 1, 17, 12), shape="vcyl"); P.hline(11 + s, 16 + s, 1, c[3]); P.vline(12 + s, 2, 11, c[3]); P.selout()

@drawer("lunchpail")
def lunchpail(P, v, f, nf):
    c = v.get("ramp", STEEL); P.box(3, 9, 20, 21, c, top=1, side=2); P.sphere((3, 4, 20, 14), c, rim=True); P.rect(3, 9, 20, 10, c[1]); P.rect(9, 3, 14, 5, BLACK[2]); P.rect(9, 5, 9, 7, BLACK[1]); P.rect(14, 5, 14, 7, BLACK[1]); P.rect(10, 12, 13, 15, BLACK[2]); P.put(11, 13, c[4]); P.selout()

@drawer("thermos", frames=4, ticks=[8, 2, 8, 2])
def thermos(P, v, f, nf):
    c = v.get("ramp", GREEN); P.vcyl((7, 5, 16, 22), c); P.hcyl((7, 2, 16, 6), STEEL); P.hcyl((8, 20, 15, 23), c); P.rect(8, 10, 15, 14, SILVER[2]); P.vline(8, 6, 21, c[3])
    if f % 2 and v.get("steam"): P.put(10, 0, (215, 215, 210)); P.put(13, 1, (215, 215, 210))
    P.selout()

@drawer("vest")
def vest(P, v, f, nf):
    c = v.get("ramp", HIVIS); P.poly([(3, 4), (8, 1), (10, 5), (13, 5), (15, 1), (20, 4), (20, 22), (3, 22)], c, box=(3, 1, 20, 22), shape="vcyl"); P.rect(11, 6, 12, 21, c[1])
    for y in (10, 15): P.hline(4, 19, y, SILVER[3]); P.hline(4, 19, y + 1, SILVER[4])
    P.selout()

@drawer("cone", frames=4, ticks=[8, 2, 8, 2])
def cone(P, v, f, nf):
    c = v.get("ramp", SAFETY); P.poly([(12, 1), (6, 20), (17, 20)], c, box=(6, 1, 17, 20), shape="vcyl"); P.hline(8, 15, 12, SNOW[3]); P.hline(8, 15, 13, SNOW[2]); P.hline(9, 14, 7, SNOW[3]); P.box(3, 20, 20, 23, c, top=1, side=1); P.selout()
    if f == 1: P.put(12, 2, SNOW[4])

@drawer("barrier", size=(32, 24))
def barrier(P, v, f, nf):
    P.box(2, 6, 29, 11, SNOW, top=1, side=1)
    for x in range(3, 28, 6): P.poly([(x, 7), (x + 3, 7), (x + 6, 10), (x + 3, 10)], SAFETY, box=(x, 7, x + 6, 10), flat=True)
    P.rect(4, 11, 6, 23, STEEL[2]); P.rect(25, 11, 27, 23, STEEL[2]); P.rect(2, 22, 8, 23, STEEL[1]); P.rect(23, 22, 29, 23, STEEL[1]); P.selout()
    if v.get("light"): P.sphere((13, 1, 18, 6), SAFETY if f % 2 else R((120, 80, 20)))

@drawer("ladder", size=(16, 32))
def ladder(P, v, f, nf):
    c = v.get("ramp", WOOD); P.rect(3, 0, 4, 31, c[2]); P.rect(11, 0, 12, 31, c[2]); P.vline(3, 0, 31, c[3]); P.vline(12, 0, 31, c[1])
    for y in range(3, 31, 6): P.rect(5, y, 10, y + 1, c[2]); P.hline(5, 10, y, c[3])
    P.selout()

@drawer("paint_roller", frames=4, ticks=[8, 2, 8, 2])
def paint_roller(P, v, f, nf):
    c = v.get("ramp", BLUE); P.hcyl((3, 3, 16, 9), c); P.rect(17, 5, 18, 7, STEEL[2]); P.rect(18, 7, 19, 12, STEEL[2]); P.poly([(17, 12), (22, 12), (21, 23), (18, 23)], WOOD, box=(17, 12, 22, 23), shape="vcyl")
    for x in range(4, 16, 3): P.put(x, 10 + (f + x) % 2, c[2])
    P.selout()

@drawer("bucket", frames=4, ticks=[8, 2, 8, 2])
def bucket(P, v, f, nf):
    c = v.get("ramp", STEEL); liq = v.get("liq"); P.poly([(4, 8), (19, 8), (17, 22), (6, 22)], c, box=(4, 8, 19, 22), shape="vcyl"); P.hcyl((4, 6, 19, 9), c); P.hcyl((5, 7, 18, 8), liq or BLACK)
    s = _sw(f, nf); ring = P.ell_mask((5 + s, 0, 18 + s, 10)) - P.ell_mask((7 + s, 2, 16 + s, 10)) - set((x, y) for x in range(24) for y in range(7, 24)); P.shade(ring, (5, 0, 18, 10), STEEL)
    P.selout()

@drawer("gloves")
def gloves(P, v, f, nf):
    c = v.get("ramp", CARAMEL)
    for x, fl in ((2, 1), (12, -1)):
        P.box(x + 1, 10, x + 9, 20, c, top=0, side=1)
        for i in range(4): P.vcyl((x + 1 + i * 2, 4 + (0 if 1 <= i <= 2 else 2), x + 2 + i * 2, 11), c)
        if fl > 0: P.poly([(x + 9, 12), (x + 11, 8), (x + 11, 14)], c, box=(x + 9, 8, x + 11, 14))
        else: P.poly([(x + 1, 12), (x - 1, 8), (x - 1, 14)], c, box=(x - 1, 8, x + 1, 14))
        P.hcyl((x, 20, x + 10, 23), c, bands=(.3, .5, .7, .9))
    P.selout()

@drawer("clipboard")
def clipboard(P, v, f, nf):
    P.box(4, 3, 19, 22, WOOD, top=1, side=1); P.rect(5, 5, 18, 21, PAPER[2]); P.rect(18, 5, 18, 21, PAPER[1]); P.rect(8, 1, 15, 5, STEEL[2]); P.rect(9, 2, 14, 3, STEEL[3])
    for y in (9, 12, 15, 18): P.hline(7, 15, y, (170, 160, 140))
    P.selout()

@drawer("drill", frames=4, ticks=[2, 2, 2, 2])
def drill(P, v, f, nf):
    c = v.get("ramp", SAFETY); P.box(5, 6, 17, 13, c, top=1, side=2); P.poly([(7, 13), (14, 13), (13, 22), (8, 22)], c, box=(7, 13, 14, 22), shape="vcyl"); P.rect(9, 14, 10, 16, BLACK[2])
    P.rect(17, 8, 19, 11, STEEL[2]); P.rect(20, 9, 23, 10, STEEL[3] if f % 2 else STEEL[1]); P.rect(5, 20, 9, 23, BLACK, ) if False else P.box(6, 20, 15, 23, BLACK, top=1, side=1); P.selout()

@drawer("tape")
def tape(P, v, f, nf):
    c = v.get("ramp", SAFETY); P.sphere((3, 4, 18, 19), c, rim=True); P.sphere((7, 8, 14, 15), BLACK); P.rect(18, 10, 23, 12, YELLOW[3]); P.rect(22, 9, 23, 13, STEEL[2])
    for x in range(19, 23, 2): P.put(x, 11, INK)
    P.selout()

@drawer("saw", frames=4, ticks=[8, 2, 8, 2])
def saw(P, v, f, nf):
    s = _sw(f, nf); P.poly([(2, 8), (16, 6), (17, 14), (3, 13)], STEEL, box=(2, 6, 17, 14), bands=(.1, .3, .6, .95))
    for x in range(3, 17, 2): P.put(x, 14 + (x % 4 == 1), STEEL[1])
    P.box(16 + s, 4, 21 + s, 16, WOOD, top=1, side=1); P.rect(18 + s, 7, 19 + s, 13, None); P.selout()

@drawer("wheelbarrow", size=(32, 24))
def wheelbarrow(P, v, f, nf):
    c = v.get("ramp", GREEN); P.poly([(6, 6), (26, 6), (24, 15), (9, 15)], c, box=(6, 6, 26, 15), shape="vcyl"); P.hline(7, 25, 6, c[3])
    P.sphere((7, 14, 15, 22), BLACK); P.sphere((10, 17, 12, 19), STEEL); P.line(26, 8, 31, 4, WOOD[2]); P.line(25, 15, 29, 22, STEEL[1]); P.line(10, 15, 8, 22, STEEL[1])
    if v.get("load"):
        for x, cc in ((9, CRIMSON), (14, GOLD), (19, GRASS)): P.sphere((x, 2, x + 5, 7), cc)
    P.selout()

@drawer("shovel", size=(16, 32), frames=4, ticks=[8, 2, 8, 2])
def shovel(P, v, f, nf):
    s = _sw(f, nf); P.rect(7, 3, 8, 20, WOOD[2]); P.vline(7, 3, 20, WOOD[3]); P.rect(5, 0, 10, 3, WOOD[2]); P.rect(5, 1, 5, 3, WOOD[1]); P.rect(10, 1, 10, 3, WOOD[1])
    P.poly([(3 + s // 2, 20), (12 + s // 2, 20), (11, 30), (8, 32), (4, 30)], STEEL, box=(3, 20, 12, 31), shape="vcyl"); P.selout()

@drawer("beach_umbrella", size=(24, 32))
def beach_umbrella(P, v, f, nf):
    cols = v.get("ramps", [CRIMSON, SNOW]); P.line(12, 12, 14, 31, WOOD[2])
    dome = P.ell_mask((0, 2, 23, 20)) - set((x, y) for x in range(24) for y in range(12, 32)); P.shade(dome, (0, 2, 23, 20), cols[0], bands=(.1, .3, .6, .9))
    for (x, y) in dome:
        if ((x - 12) // 4) % 2: P.put(x, y, cols[1][2] if P.get(x, y)[:3] == cols[0][2] else cols[1][3] if P.get(x, y)[:3] == cols[0][3] else cols[1][1])
    P.put(12, 1, cols[0][3]); P.selout()

@drawer("flipflops", size=(24, 16))
def flipflops(P, v, f, nf):
    c = v.get("ramp", TEAL)
    for x in (2, 13): P.sphere((x, 1, x + 8, 15), c, bands=(.1, .3, .6, .95)); P.line(x + 4, 3, x + 2, 8, BLACK[2]); P.line(x + 4, 3, x + 6, 8, BLACK[2]); P.put(x + 4, 3, BLACK[1])
    P.selout()

@drawer("float", frames=4, ticks=[8, 2, 8, 2])
def float_(P, v, f, nf):
    cols = v.get("ramps", [CRIMSON, SNOW]); s = _bob(f, nf); ring = P.ell_mask((1, 3 + s, 22, 20 + s)) - P.ell_mask((7, 8 + s, 16, 15 + s)); P.shade(ring, (1, 3 + s, 22, 20 + s), cols[0], rim=True)
    for (x, y) in ring:
        a = math.atan2(y - 11.5 - s, x - 11.5)
        if int((a + math.pi) / (math.pi / 2)) % 2: P.put(x, y, cols[1][2] if P.get(x, y)[:3] == cols[0][2] else cols[1][3] if P.get(x, y)[:3] == cols[0][3] else cols[1][1])
    P.selout()

@drawer("sunglasses", size=(24, 16))
def sunglasses(P, v, f, nf):
    c = v.get("ramp", BLACK); P.sphere((1, 4, 10, 13), c, bands=(.1, .25, .6, .97)); P.sphere((13, 4, 22, 13), c, bands=(.1, .25, .6, .97)); P.rect(10, 6, 13, 7, c[2]); P.hline(1, 22, 4, c[3]); P.put(3, 6, SNOW[3]); P.put(4, 6, SNOW[3]); P.put(15, 6, SNOW[3]); P.put(16, 6, SNOW[3]); P.selout()

@drawer("beach_ball", frames=4, ticks=[8, 2, 8, 2])
def beach_ball(P, v, f, nf):
    cols = v.get("ramps", [CRIMSON, SNOW, BLUE, GOLD]); s = _bob(f, nf); m = P.ell_mask((3, 3 + s, 20, 20 + s)); P.shade(m, (3, 3 + s, 20, 20 + s), cols[0], rim=True)
    for (x, y) in m:
        a = math.atan2(y - 11.5 - s, x - 11.5); k = int((a + math.pi) / (math.pi / 3)) % len(cols); c = cols[k]; cur = P.get(x, y)[:3]
        P.put(x, y, c[2] if cur == cols[0][2] else c[3] if cur == cols[0][3] else c[1] if cur == cols[0][1] else c[4] if cur == cols[0][4] else c[0])
    P.selout(); P.put(8, 6 + s, SNOW[4])

@drawer("bow_tie", size=(16, 16), frames=4, ticks=[8, 2, 8, 2])
def bow_tie(P, v, f, nf):
    c = v.get("ramp", CRIMSON); s = _sw(f, nf)
    P.poly([(7, 6), (7, 10), (1, 13 + s), (1, 3 + s)], c, box=(1, 3, 7, 13), shape="hcyl"); P.poly([(8, 6), (8, 10), (14, 3 - s), (14, 13 - s)], c, box=(8, 3, 14, 13), shape="hcyl")
    P.rect(6, 6, 9, 10, c[1]); P.rect(6, 6, 9, 6, c[3]); P.put(2, 5 + s, c[4]); P.put(13, 5 - s, c[4]); P.selout()

@drawer("glasses", size=(24, 16), frames=4, ticks=[8, 2, 8, 2])
def glasses(P, v, f, nf):
    c = v.get("ramp", GOLD); shape = v.get("shape", "round")
    for x in (1, 13):
        if shape == "round": ring = P.ell_mask((x, 4, x + 9, 13)) - P.ell_mask((x + 2, 6, x + 7, 11)); P.shade(ring, (x, 4, x + 9, 13), c)
        elif shape == "star":
            pts = [(x + 4.5 + (5 if i % 2 == 0 else 2) * math.cos(-math.pi / 2 + i * math.pi / 5), 8.5 + (5 if i % 2 == 0 else 2) * math.sin(-math.pi / 2 + i * math.pi / 5)) for i in range(10)]
            P.poly(pts, c, box=(x, 3, x + 9, 14), bands=(.1, .3, .6, .9))
        else: P.box(x, 4, x + 9, 13, c, top=1, side=1); P.rect(x + 2, 6, x + 7, 11, ICE[2])
    P.rect(10, 7, 13, 8, c[2]); P.selout()
    if f == 1: P.put(3, 6, SNOW[4]); P.put(15, 6, SNOW[4])

@drawer("calendar", frames=4, ticks=[8, 2, 2, 8])
def calendar(P, v, f, nf):
    c = v.get("ramp", CRIMSON); P.box(3, 5, 20, 22, PAPER, top=1, side=1); P.box(3, 3, 20, 8, c, top=1, side=1); P.rect(7, 1, 8, 5, STEEL[2]); P.rect(15, 1, 16, 5, STEEL[2])
    if f in (1, 2): P.poly([(4, 9), (19, 9), (19 - f * 4, 14 + f * 3), (4, 9 + f * 2)], PAPER, flat=True); P.hline(4, 19, 9, PAPER[3])
    for y in (12, 15, 18): 
        for x in range(5, 19, 4): P.put(x, y, (170, 160, 140)) if f not in (1, 2) else None
    P.selout()

@drawer("grill", size=(32, 32), frames=4, ticks=[4, 4, 4, 4])
def grill(P, v, f, nf):
    c = v.get("ramp", BLACK); P.sphere((4, 6, 27, 20), c, rim=True); P.rect(4, 13, 27, 20, c[2]); P.hline(5, 26, 20, c[1]); P.hcyl((3, 12, 28, 14), STEEL)
    for x in range(6, 26, 3): P.put(x, 12, STEEL[1])
    P.rect(14, 1, 17, 6, c[2]); P.rect(13, 0, 18, 1, c[3])
    P.rect(9, 21, 10, 30, STEEL[2]); P.rect(21, 21, 22, 30, STEEL[2]); P.sphere((7, 28, 12, 31), BLACK); P.sphere((19, 28, 24, 31), BLACK)
    if v.get("food"):
        P.hcyl((8, 9, 13, 12), R((190, 70, 50))); P.hcyl((15, 9, 22, 12), CHOC); P.put(16, 10, CHOC[3])
    for i in range(3):
        y = 7 - ((f * 2 + i * 3) % 8); x = 10 + i * 5 + ((f + i) % 2); P.put(x, max(0, y), (190, 190, 186)) if y >= 0 else None
    P.selout()

@drawer("picnic", size=(32, 24))
def picnic(P, v, f, nf):
    P.poly([(1, 10), (30, 10), (31, 23), (0, 23)], CRIMSON, box=(0, 10, 31, 23), flat=True)
    for y in range(11, 23):
        for x in range(0, 32):
            if (x // 4 + y // 3) % 2: P.put(x, y, FLAG_WHITE[2])
    P.box(10, 2, 21, 12, WHEAT, top=1, side=1); P.rect(10, 7, 21, 7, WHEAT[1]); P.sphere((11, 0, 20, 4), WHEAT, bands=(.2, .4, .7, .9)); P.rect(12, 1, 19, 3, None)
    P.sphere((4, 13, 9, 18), CRIMSON); P.rect(23, 12, 28, 19, R((240, 210, 120))[2]); P.rect(23, 12, 28, 12, SNOW[3]); P.selout()

@drawer("cooler", frames=4, ticks=[8, 2, 8, 2])
def cooler(P, v, f, nf):
    c = v.get("ramp", BLUE); P.box(3, 9, 20, 21, c, top=0, side=2); P.box(2, 6, 21, 10, SNOW, top=1, side=1); P.rect(10, 3, 13, 6, c[1]); P.rect(11, 4, 12, 5, None); P.rect(9, 13, 14, 15, SNOW[2])
    if f == 1: P.put(5, 11, ICE[4]); P.put(18, 17, ICE[4])
    P.selout()

@drawer("lawn_chair")
def lawn_chair(P, v, f, nf):
    c = v.get("ramp", TEAL); P.poly([(5, 2), (16, 2), (17, 13), (6, 13)], c, box=(5, 2, 17, 13), shape="vcyl"); P.poly([(5, 13), (20, 13), (20, 17), (5, 17)], c, flat=True)
    for y in (4, 7, 10): P.hline(6, 16, y, c[3])
    P.line(5, 13, 3, 23, STEEL[2]); P.line(20, 17, 22, 23, STEEL[2]); P.line(5, 17, 2, 23, STEEL[2]); P.line(17, 13, 21, 23, STEEL[1]); P.selout()

@drawer("hammock", size=(32, 24), frames=4, ticks=[8, 2, 8, 2])
def hammock(P, v, f, nf):
    c = v.get("ramp", TEAL); s = _sw(f, nf); P.rect(1, 2, 2, 23, WOOD[2]); P.rect(29, 2, 30, 23, WOOD[2])
    pts = [(2, 6), (29, 6)] + [(29 - i * 3, 6 + int(round(8 * math.sin(math.pi * (27 - i * 3) / 27))) + s) for i in range(10)]
    P.poly(pts, c, box=(2, 6, 29, 16), bands=(.1, .3, .6, .9))
    for x in range(5, 27, 4): P.vline(x, 7, 10 + int(round(6 * math.sin(math.pi * x / 31))) + s, c[1])
    P.selout()

@drawer("lemonade_stand", size=(32, 32))
def lemonade_stand(P, v, f, nf):
    P.box(2, 14, 29, 30, WOOD, top=1, side=2); P.rect(2, 12, 29, 14, YELLOW[2]); P.hline(3, 28, 12, YELLOW[3]); P.rect(3, 0, 4, 12, WOOD[2]); P.rect(27, 0, 28, 12, WOOD[2])
    for x in range(4, 28):
        if (x // 4) % 2: P.rect(x, 0, x, 4, YELLOW[2])
        else: P.rect(x, 0, x, 4, SNOW[2])
    P.vcyl((9, 5, 14, 12), ICE, bands=(.02, .1, .6, .95)); P.vcyl((10, 7, 13, 11), YELLOW); P.sphere((18, 8, 21, 11), YELLOW); P.sphere((21, 9, 24, 12), YELLOW); P.rect(6, 18, 25, 25, PAPER[2]); P.selout()

@drawer("tent", size=(32, 24))
def tent(P, v, f, nf):
    c = v.get("ramp", GREEN); P.poly([(16, 2), (2, 22), (30, 22)], c, box=(2, 2, 30, 22), shape="vcyl"); P.poly([(16, 6), (10, 22), (22, 22)], c, box=(10, 6, 22, 22), bands=(.0, .05, .1, .2)); P.rect(16, 7, 16, 21, c[3]); P.put(16, 1, c[3]); P.selout()

@drawer("campfire", size=(24, 24), frames=3, ticks=[3, 2, 3])
def campfire(P, v, f, nf):
    P.hcyl((2, 18, 14, 22), WOOD); P.hcyl((9, 18, 21, 22), WOOD); P.line(5, 22, 18, 17, WOOD[1])
    shapes = [[(12, 3), (17, 10), (16, 18), (8, 18), (7, 10)], [(13, 2), (18, 11), (16, 18), (8, 18), (8, 9)], [(11, 4), (17, 9), (17, 18), (7, 18), (6, 11)]]
    P.poly(shapes[f % 3], FLAME, box=(6, 2, 18, 18)); P.poly([(12, 9), (15, 14), (14, 18), (10, 18), (9, 14)], R((255, 230, 140)), box=(9, 9, 15, 18)); P.put(5, 8 - f, EMBER[3]); P.put(19, 6 + f, EMBER[3]); P.selout()

@drawer("fishing", size=(24, 24), frames=4, ticks=[8, 2, 8, 2])
def fishing(P, v, f, nf):
    s = _sw(f, nf); P.line(3, 23, 16, 2, WOOD[2]); P.line(4, 23, 17, 2, WOOD[1]); P.sphere((5, 17, 9, 21), STEEL); P.line(16, 2, 21, 12 + s, (190, 190, 186)); P.sphere((20, 12 + s, 23, 15 + s), CRIMSON); P.put(21, 12 + s, SNOW[3]); P.selout()

@drawer("anchor", frames=4, ticks=[8, 2, 8, 2])
def anchor(P, v, f, nf):
    c = v.get("ramp", STEEL); ring = P.ell_mask((9, 0, 14, 5)) - P.ell_mask((11, 2, 12, 3)); P.shade(ring, (9, 0, 14, 5), c); P.rect(11, 5, 12, 20, c[2]); P.vline(11, 5, 20, c[3]); P.rect(6, 8, 17, 9, c[2])
    arc = P.ell_mask((3, 10, 20, 23)) - P.ell_mask((6, 10, 17, 20)) - set((x, y) for x in range(24) for y in range(0, 16)); P.shade(arc, (3, 10, 20, 23), c); P.poly([(3, 15), (2, 19), (5, 18)], c, box=(2, 15, 5, 19)); P.poly([(20, 15), (21, 19), (18, 18)], c, box=(18, 15, 21, 19)); P.selout()

# ---------------------------------------------------------------- the ten sets (50 each)
def V(d, title, **p): return (d, p, title)
GOLDY = R((236, 196, 70)); SILV = SILVER; MIDNIGHT = R((40, 44, 90)); CHAMP = R((240, 210, 120)); SPRING_GRN = R((130, 200, 110)); CREAMW = R((238, 232, 214), dark=.72)
BRICK = R((160, 70, 50)); COPPER = R((190, 110, 60)); PATINA = R((100, 170, 150)); SUMMER_BLUE = R((70, 150, 220)); CORAL_R = R((240, 110, 90)); TURQ = R((60, 190, 190))
SET_ITEMS = {
"NYD": [
    V("ball_drop", "The ball drop"), V("clock", "Clock at midnight"), V("champagne", "Bottle, cork popping"), V("glass", "Champagne flute", kind="flute"), V("glass", "Flute, pink", kind="flute", liq=PINK),
    V("confetti", "Confetti, gold and silver", ramps=[GOLDY, SILV, SNOW], seed=1), V("confetti", "Confetti, party mix", ramps=[CRIMSON, BLUE, GOLDY, LIME], seed=2), V("streamer", "Streamer, gold", ramp=GOLDY), V("streamer", "Streamer, pink", ramp=PINK), V("streamer", "Streamer, blue", ramp=BLUE),
    V("party_hat", "Party hat, gold stripes", ramp=MIDNIGHT, ramp2=GOLDY, stripes=True), V("party_hat", "Party hat, dots", ramp=PINK, ramp2=SNOW, dots=True), V("party_hat", "Party hat, silver", ramp=SILV, ramp2=MIDNIGHT), V("hat", "Top hat", kind="top", ramp=BLACK, band=GOLDY), V("bow_tie", "Bow tie, red"), V("bow_tie", "Bow tie, gold", ramp=GOLDY),
    V("glasses", "Novelty glasses, stars", shape="star", ramp=GOLDY), V("glasses", "Novelty glasses, round", shape="round", ramp=SILV), V("glasses", "Party shades, square", shape="square", ramp=MIDNIGHT), V("disco", "Disco ball"),
    V("balloon", "Balloon, gold", ramp=GOLDY), V("balloon", "Balloon, silver", ramp=SILV), V("balloon", "Balloon, midnight blue", ramp=MIDNIGHT), V("balloon", "Balloon, long, pink", ramp=PINK, shape="long"), V("balloon", "Heart balloon, red", ramp=CRIMSON, shape="heart"),
    V("popper", "Party popper, gold", ramp=GOLDY, bits=[CRIMSON, SILV, GOLDY]), V("popper", "Party popper, red", ramp=CRIMSON, bits=[GOLDY, SNOW, BLUE]), V("horn", "Party horn, blue", ramp=BLUE, ramp2=GOLDY), V("horn", "Party horn, pink", ramp=PINK, ramp2=SILV), V("drum", "Snare for the countdown", ramp=MIDNIGHT),
    V("firework", "Firework, gold", ramp=GOLDY, ramp2=SNOW), V("firework", "Firework, red and gold", ramp=CRIMSON, ramp2=GOLDY), V("firework", "Firework, blue", ramp=BLUE, ramp2=SILV, rays=10), V("firework", "Firework, pink", ramp=PINK, ramp2=GOLDY, rays=6), V("sparkler", "Sparkler"),
    V("sparkle", "Twinkle, gold", color=GOLDY[4], twin=True), V("sparkle", "Twinkle, white"), V("star", "Gold star"), V("hourglass", "Hourglass, last grains"), V("calendar", "Calendar, page flip", ramp=MIDNIGHT),
    V("bunting", "Bunting, black and gold", ramps=[BLACK, GOLDY, MIDNIGHT], shape="tri"), V("bunting", "Bunting, scallops", ramps=[GOLDY, SNOW, SILV], shape="scallop"), V("lights", "String lights, warm", ramps=[GOLDY, SNOW, CHAMP]), V("candle", "Tall candle, gold", ramp=GOLDY, h=14), V("candle", "Candle in a holder", ramp=CREAMW, holder=True),
    V("sign", "Blank placard, round", shape="round"), V("sign", "Blank placard", shape="rect", tape=True), V("gift", "Gift, midnight and gold", ramp=MIDNIGHT, ribbon=GOLDY), V("coin", "Lucky coin"), V("bell", "Bell, midnight", ramp=GOLDY),
],
"MLK": [
    V("microphone", "Microphone on a stand"), V("microphone", "Hand mic", stand=False), V("podium", "Podium with mic", mic=True), V("podium", "Podium, oak", ramp=CARAMEL), V("megaphone", "Megaphone, red"), V("megaphone", "Megaphone, blue", ramp=BLUE),
    V("dove", "Dove with a branch", branch=True), V("dove", "Dove in flight"), V("candle", "Vigil candle", ramp=CREAMW, h=10), V("candle", "Vigil candle, tall", ramp=CREAMW, h=14, drip=True), V("candle", "Vigil candle in a holder", ramp=SNOW, holder=True),
    V("bell", "Bell"), V("bell", "Bell, silver", ramp=SILV), V("book", "Book, blue", ramp=BLUE, ribbon=True), V("book", "Book, red", ramp=CRIMSON), V("book", "Open book", ramp=NAVY, open=True), V("scroll", "Scroll"), V("quill", "Quill and ink", ink=True),
    V("laurel", "Laurel wreath"), V("peace", "Peace sign"), V("heart", "Heart, red"), V("heart", "Heart, gold", ramp=GOLDY), V("rosette", "Rosette, blue", ramp=BLUE, ramp2=GOLDY), V("rosette", "Rosette, red", ramp=CRIMSON, ramp2=SNOW), V("medal", "Medal, blue ribbon", ribbon=BLUE),
    V("torch", "Torch"), V("lantern", "Lantern, paper, gold", ramp=GOLDY), V("lantern", "Lantern, metal", ramp=STEEL, shape="metal"), V("sign", "Blank placard", shape="rect"), V("sign", "Blank placard, tall sign", shape="arrow"),
    V("sign", "Blank round sign", shape="round", ramp=SNOW), V("pin", "Map pin, red"), V("pin", "Map pin, blue", ramp=BLUE), V("gavel", "Gavel"), V("scales", "Scales of justice"),
    V("flower", "Rose, red", kind="rose", ramp=CRIMSON), V("flower", "Rose, white", kind="rose", ramp=SNOW), V("balloon", "Balloon, red", ramp=CRIMSON), V("balloon", "Balloon, blue", ramp=BLUE), V("balloon", "Balloon, gold", ramp=GOLDY),
    V("bunting", "Bunting, red, white and blue", ramps=[CRIMSON, SNOW, BLUE]), V("letter", "Sealed letter"), V("clipboard", "Clipboard, blank"), V("star", "Star, gold"), V("sparkle", "Twinkle"),
    V("drum", "Marching drum", ramp=NAVY), V("bugle", "Bugle"), V("tambourine", "Tambourine"), V("hat", "Bowler hat", kind="bowler", ramp=BLACK, band=CRIMSON), V("hat", "Flat cap", kind="cap", ramp=BROWN),
],
"PRES": [
    V("hat", "Stovepipe hat", kind="stovepipe", ramp=BLACK, band=BLACK), V("hat", "Tricorne", kind="tricorne", ramp=BROWN, band=GOLDY), V("hat", "Top hat, navy", kind="top", ramp=NAVY, band=CRIMSON), V("quill", "Quill and ink", ink=True), V("quill", "Quill"),
    V("scroll", "Parchment, sealed", seal=True), V("scroll", "Parchment"), V("letter", "Wax-sealed letter"), V("book", "Ledger, leather", ramp=LEATHER, ribbon=True), V("book", "Open ledger", ramp=LEATHER, open=True),
    V("pie", "Cherry pie", fill=BERRY, lattice=True), V("pie", "Cherry pie slice", fill=BERRY, slice=True), V("cherries", "Cherries"), V("axe", "Hatchet"), V("log", "Log"),
    V("monument", "Obelisk"), V("columns", "Columns"), V("dome", "Dome"), V("flag", "Flag, stripes", ramps=[CRIMSON, SNOW], style="stripes"), V("flag", "Flag, star field", ramps=[CRIMSON, SNOW], style="stars"),
    V("bunting", "Bunting, red, white and blue", ramps=[CRIMSON, SNOW, NAVY]), V("bunting", "Bunting, scallops", ramps=[NAVY, SNOW, CRIMSON], shape="scallop"), V("rosette", "Rosette, blue", ramp=NAVY, ramp2=GOLDY), V("rosette", "Rosette, red", ramp=CRIMSON, ramp2=GOLDY), V("medal", "Medal, red ribbon"),
    V("coin", "Coin"), V("coin", "Silver coin", ramp=SILV), V("ballot", "Ballot box"), V("ballot", "Ballot box, navy", ramp=NAVY), V("podium", "Podium"),
    V("candle", "Candle in a holder", ramp=CREAMW, holder=True), V("lantern", "Lantern, metal", ramp=STEEL, shape="metal"), V("bell", "Bell"), V("star", "Star"), V("laurel", "Laurel wreath"),
    V("gavel", "Gavel"), V("scales", "Scales"), V("glasses", "Spectacles", shape="round", ramp=GOLDY), V("bow_tie", "Bow tie, navy", ramp=NAVY), V("hat", "Powdered-wig day: bowler", kind="bowler", ramp=GREY, band=NAVY),
    V("balloon", "Balloon, navy", ramp=NAVY), V("balloon", "Balloon, red", ramp=CRIMSON), V("balloon", "Balloon, white", ramp=SNOW), V("cake", "Cherry-topped cake", ramp=CREAMW, ice=CRIMSON, cherry=True), V("cupcake", "Cupcake, red white blue", ramp=NAVY, frost=SNOW, sprinkles=True),
    V("sign", "Blank placard", shape="rect"), V("glass", "Cup of cider", kind="mug", liq=R((220, 150, 60))), V("teapot", "Teapot", ramp=SNOW), V("fireplace", "Fireplace", ramp=BRICK), V("hourglass", "Hourglass"),
],
"GF": [
    V("flower", "Tulip, red", kind="tulip", ramp=CRIMSON), V("flower", "Tulip, pink", kind="tulip", ramp=PASTEL_PINK), V("flower", "Tulip, yellow", kind="tulip", ramp=YELLOW), V("flower", "Daffodil", kind="daffodil", ramp=YELLOW), V("flower", "Lily, white", kind="lily", ramp=SNOW),
    V("flower", "Lily, pink", kind="lily", ramp=PASTEL_PINK), V("flower", "Hibiscus", kind="hibiscus", ramp=CORAL_R), V("flower", "Rose, pink", kind="rose", ramp=PINK), V("sprout", "Sprout growing"), V("sprout", "Sprout, blue pot", ramp=PASTEL_BLUE),
    V("egg", "Egg, pink dots", ramp=PASTEL_PINK, pat="dots"), V("egg", "Egg, blue zigzag", ramp=PASTEL_BLUE, pat="zig"), V("egg", "Egg, yellow bands", ramp=PASTEL_YEL, pat="bands"), V("egg", "Egg, green dots", ramp=PASTEL_GRN, pat="dots", ramp2=PASTEL_PINK), V("egg", "Egg, lilac zigzag", ramp=LILAC, pat="zig"),
    V("basket", "Basket of eggs", goods="eggs"), V("basket", "Basket of flowers", goods="flowers"), V("basket", "Picnic basket", goods="food"), V("chick", "Chick"), V("bunny", "Bunny, white"), V("bunny", "Bunny, grey", ramp=GREY), V("lamb", "Lamb"),
    V("butterfly", "Butterfly, purple", ramp=PURPLE), V("butterfly", "Butterfly, orange", ramp=PUMPKIN), V("butterfly", "Butterfly, blue", ramp=SUMMER_BLUE), V("bee", "Bee"), V("ladybug", "Ladybug"),
    V("raincloud", "Rain cloud"), V("raincloud", "Sun after rain", sun=True), V("umbrella", "Umbrella, yellow", ramp=YELLOW, ramp2=YELLOW), V("umbrella", "Umbrella, pink and white", ramp=PASTEL_PINK, ramp2=SNOW), V("boots", "Rain boots, yellow", ramp=YELLOW), V("boots", "Rain boots, blue", ramp=SUMMER_BLUE),
    V("watering_can", "Watering can"), V("watering_can", "Watering can, green", ramp=SPRING_GRN), V("carrot", "Carrot"), V("bun", "Hot cross bun"), V("kite", "Kite, red", ramp=CRIMSON), V("kite", "Kite, blue", ramp=SUMMER_BLUE, ramp2=PASTEL_YEL),
    V("pinwheel", "Pinwheel, pastel", ramps=[PASTEL_PINK, PASTEL_BLUE, PASTEL_YEL, PASTEL_GRN]), V("leaf", "New leaf", kind="simple", ramp=SPRING_GRN), V("candle", "Candle, white", ramp=SNOW, h=12), V("candle", "Candle, tall, in a holder", ramp=CREAMW, holder=True, h=13), V("dove", "Dove with a branch", branch=True),
    V("bell", "Bell"), V("balloon", "Balloon, pastel pink", ramp=PASTEL_PINK), V("balloon", "Balloon, pastel blue", ramp=PASTEL_BLUE), V("bunting", "Bunting, pastel", ramps=[PASTEL_PINK, PASTEL_BLUE, PASTEL_YEL, PASTEL_GRN]), V("cupcake", "Cupcake, spring", ramp=PASTEL_GRN, frost=PASTEL_PINK, sprinkles=True), V("sign", "Blank placard", shape="round", ramp=PASTEL_YEL),
],
"MEM": [
    V("poppy_pin", "Poppy pin"), V("flower", "Poppy", kind="poppy", ramp=CRIMSON), V("flower", "Poppy, second", kind="poppy", ramp=R((220, 60, 50))), V("folded_flag", "Folded flag"), V("flag", "Flag, stripes", ramps=[CRIMSON, SNOW], style="stripes"), V("flag", "Flag, star field", ramps=[CRIMSON, SNOW], style="stars"),
    V("wreath", "Wreath, red ribbon", ramp=FOREST, berry=CRIMSON, bow=CRIMSON), V("wreath", "Wreath, blue ribbon", ramp=HOLLY, berry=SNOW, bow=NAVY), V("laurel", "Laurel"), V("candle", "Candle, white", ramp=SNOW, h=12), V("candle", "Candle in a holder", ramp=CREAMW, holder=True),
    V("bugle", "Bugle"), V("bell", "Bell"), V("medal", "Medal, red ribbon"), V("medal", "Medal, blue ribbon", ribbon=NAVY), V("rosette", "Rosette, red white blue", ramp=NAVY, ramp2=CRIMSON), V("star", "Star"), V("dove", "Dove"),
    V("bunting", "Bunting, red, white and blue", ramps=[CRIMSON, SNOW, NAVY]), V("bunting", "Bunting, rectangles", ramps=[NAVY, SNOW, CRIMSON], shape="rect"), V("balloon", "Balloon, red", ramp=CRIMSON), V("balloon", "Balloon, white", ramp=SNOW), V("balloon", "Balloon, blue", ramp=NAVY),
    V("grill", "Grill, lit", food=True), V("grill", "Grill, cold"), V("hotdog", "Hot dog, mustard", mustard=True), V("hotdog", "Hot dog, ketchup and mustard", mustard=True, ketchup=True), V("burger", "Burger", tomato=True), V("corn", "Corn on the cob", butter=True), V("watermelon", "Watermelon slice"),
    V("glass", "Lemonade pitcher", kind="pitcher", lemon=True), V("glass", "Lemonade", kind="mug", liq=R((240, 220, 120))), V("cooler", "Cooler, blue"), V("cooler", "Cooler, red", ramp=CRIMSON), V("picnic", "Picnic blanket"), V("lawn_chair", "Lawn chair", ramp=NAVY), V("lawn_chair", "Lawn chair, red", ramp=CRIMSON),
    V("pinwheel", "Pinwheel, red white blue", ramps=[CRIMSON, SNOW, NAVY, SNOW]), V("kite", "Kite, red white blue", ramp=CRIMSON, ramp2=NAVY), V("sunglasses", "Sunglasses"), V("sparkler", "Sparkler"), V("boots", "Boots", ramp=LEATHER, work=True),
    V("hat", "Cap, navy", kind="cap", ramp=NAVY), V("sign", "Blank placard", shape="rect"), V("popsicle", "Popsicle, red white blue", ramps=[CRIMSON, SNOW, NAVY]), V("ice_cream", "Ice cream, vanilla", ramps=[SNOW, CREAMW]), V("pie", "Apple pie", fill=CARAMEL, lattice=True),
    V("tent", "Tent, green"), V("campfire", "Campfire"), V("lantern", "Camp lantern", ramp=STEEL, shape="metal"),
],
"JUN": [
    V("flag", "Flag, red black green", ramps=[PAN_RED, PAN_BLACK, PAN_GREEN], style="bands"), V("flag", "Flag, red and green", ramps=[PAN_RED, PAN_GREEN], style="stripes"), V("bunting", "Bunting, red black green", ramps=[PAN_RED, PAN_BLACK, PAN_GREEN]), V("bunting", "Bunting, scallops, gold", ramps=[PAN_GOLD, PAN_RED, PAN_GREEN], shape="scallop"),
    V("balloon", "Balloon, red", ramp=PAN_RED), V("balloon", "Balloon, green", ramp=PAN_GREEN), V("balloon", "Balloon, black", ramp=PAN_BLACK), V("balloon", "Balloon, gold", ramp=PAN_GOLD), V("balloon", "Heart balloon, red", ramp=PAN_RED, shape="heart"),
    V("star", "Star, gold", ramp=PAN_GOLD), V("star", "Star, white", ramp=SNOW), V("sparkle", "Twinkle, gold", color=PAN_GOLD[4], twin=True), V("firework", "Firework, red and gold", ramp=PAN_RED, ramp2=PAN_GOLD), V("firework", "Firework, green", ramp=PAN_GREEN, ramp2=PAN_GOLD, rays=10), V("sparkler", "Sparkler"),
    V("drum", "Drum, red", ramp=PAN_RED), V("drum", "Drum, green", ramp=PAN_GREEN, skin=WHEAT), V("tambourine", "Tambourine"), V("horn", "Horn, gold", ramp=PAN_GOLD, ramp2=PAN_RED), V("bell", "Freedom bell", ramp=PAN_GOLD), V("bell", "Bell, bronze", ramp=COPPER),
    V("cake", "Red velvet cake", ramp=R((160, 36, 48)), ice=SNOW, layers=2), V("cake", "Red velvet, single", ramp=R((160, 36, 48)), ice=SNOW, layers=1, cherry=True), V("cupcake", "Red velvet cupcake", ramp=R((160, 36, 48)), frost=SNOW), V("bottle", "Strawberry soda", ramp=PAN_RED, cap=SILV), V("glass", "Red drink", kind="mug", liq=PAN_RED), V("glass", "Red punch pitcher", kind="pitcher", liq=PAN_RED),
    V("watermelon", "Watermelon slice"), V("watermelon", "Watermelon, whole", whole=True), V("grill", "Grill, lit", food=True), V("hotdog", "Hot dog", mustard=True), V("corn", "Corn", butter=True), V("picnic", "Picnic blanket"), V("cooler", "Cooler, red", ramp=PAN_RED),
    V("lantern", "Lantern, red", ramp=PAN_RED), V("lantern", "Lantern, green", ramp=PAN_GREEN), V("lantern", "Lantern, gold", ramp=PAN_GOLD), V("flower", "Sunflower", kind="sunflower", ramp=YELLOW), V("flower", "Hibiscus, red", kind="hibiscus", ramp=PAN_RED), V("flower", "Rose, red", kind="rose", ramp=PAN_RED),
    V("book", "Book, green", ramp=PAN_GREEN, ribbon=True), V("book", "Open book", ramp=PAN_RED, open=True), V("scroll", "Scroll, sealed", seal=True), V("candle", "Candle, red", ramp=PAN_RED, h=12), V("candle", "Candle, green", ramp=PAN_GREEN, h=12), V("candle", "Candle, gold in holder", ramp=PAN_GOLD, holder=True),
    V("rosette", "Rosette, red black green", ramp=PAN_RED, ramp2=PAN_GREEN), V("medal", "Medal, green ribbon", ribbon=PAN_GREEN, ramp=PAN_GOLD), V("sign", "Blank placard", shape="rect"), V("dove", "Dove"),
],
"IND": [
    V("firework", "Firework, red", ramp=CRIMSON, ramp2=SNOW), V("firework", "Firework, white", ramp=SNOW, ramp2=NAVY), V("firework", "Firework, blue", ramp=NAVY, ramp2=SNOW, rays=10), V("firework", "Firework, gold", ramp=GOLDY, ramp2=CRIMSON, rays=12), V("sparkler", "Sparkler"), V("rocket", "Bottle rocket", ramp=SNOW, ramp2=CRIMSON), V("rocket", "Rocket, blue", ramp=SNOW, ramp2=NAVY),
    V("flag", "Flag, stripes", ramps=[CRIMSON, SNOW], style="stripes"), V("flag", "Flag, star field", ramps=[CRIMSON, SNOW], style="stars"), V("bunting", "Bunting, red white blue", ramps=[CRIMSON, SNOW, NAVY]), V("bunting", "Bunting, scallops", ramps=[NAVY, SNOW, CRIMSON], shape="scallop"), V("bunting", "Bunting, rectangles", ramps=[CRIMSON, SNOW, NAVY], shape="rect"),
    V("star", "Star, white", ramp=SNOW), V("star", "Star, gold"), V("sparkle", "Twinkle"), V("rosette", "Rosette, red white blue", ramp=NAVY, ramp2=CRIMSON), V("liberty", "Liberty crown", kind="crown"), V("liberty", "Liberty torch", kind="torch"),
    V("hat", "Striped top hat", kind="top", ramp=CRIMSON, band=NAVY), V("hat", "Cap, navy", kind="cap", ramp=NAVY), V("sunglasses", "Sunglasses"), V("glasses", "Star shades", shape="star", ramp=NAVY), V("bow_tie", "Bow tie, navy", ramp=NAVY),
    V("balloon", "Balloon, red", ramp=CRIMSON), V("balloon", "Balloon, white", ramp=SNOW), V("balloon", "Balloon, blue", ramp=NAVY), V("balloon", "Star balloon, blue", ramp=NAVY, shape="long"), V("pinwheel", "Pinwheel", ramps=[CRIMSON, SNOW, NAVY, SNOW]), V("kite", "Kite, stars and stripes", ramp=NAVY, ramp2=CRIMSON),
    V("grill", "Grill, lit", food=True), V("hotdog", "Hot dog, the works", mustard=True, ketchup=True), V("burger", "Burger", tomato=True), V("corn", "Corn", butter=True), V("watermelon", "Watermelon slice"), V("popsicle", "Popsicle, red white blue", ramps=[CRIMSON, SNOW, NAVY]), V("ice_cream", "Ice cream, strawberry", ramps=[PINK, SNOW], cherry=True),
    V("glass", "Lemonade pitcher", kind="pitcher", lemon=True), V("glass", "Lemonade", kind="mug", liq=R((240, 220, 120))), V("can", "Soda can, red", ramp=CRIMSON), V("can", "Soda can, blue", ramp=NAVY), V("cooler", "Cooler, red", ramp=CRIMSON), V("picnic", "Picnic blanket"), V("lawn_chair", "Lawn chair, red", ramp=CRIMSON),
    V("beach_ball", "Beach ball"), V("beach_umbrella", "Beach umbrella", ramps=[CRIMSON, SNOW]), V("float", "Pool float", ramps=[CRIMSON, SNOW]), V("drum", "Parade drum", ramp=NAVY), V("bugle", "Bugle"), V("bell", "Liberty-style bell", ramp=COPPER), V("pie", "Apple pie", fill=CARAMEL, lattice=True),
],
"LAB": [
    V("hat", "Hard hat, yellow", kind="hardhat", ramp=YELLOW), V("hat", "Hard hat, white", kind="hardhat", ramp=SNOW), V("hat", "Hard hat, orange", kind="hardhat", ramp=SAFETY), V("vest", "Hi-vis vest"), V("vest", "Hi-vis vest, orange", ramp=SAFETY), V("boots", "Work boots", ramp=LEATHER, work=True), V("gloves", "Work gloves"),
    V("toolbox", "Toolbox, red"), V("toolbox", "Toolbox, blue", ramp=BLUE), V("wrench", "Wrench"), V("hammer", "Hammer"), V("screwdriver", "Screwdriver, red"), V("screwdriver", "Screwdriver, blue", ramp=BLUE), V("drill", "Drill"), V("tape", "Tape measure"), V("saw", "Hand saw"),
    V("lunchpail", "Lunch pail"), V("thermos", "Thermos, steaming", steam=True), V("thermos", "Thermos, red", ramp=CRIMSON), V("mug", "Coffee, black", ramp=SNOW, liq=CHOC), V("mug", "Coffee, red mug", ramp=CRIMSON, liq=CHOC), V("clipboard", "Clipboard"),
    V("cone", "Traffic cone"), V("barrier", "Barrier, light on", light=True), V("ladder", "Ladder"), V("paint_roller", "Paint roller, blue"), V("paint_roller", "Paint roller, lime", ramp=LIME), V("bucket", "Bucket of paint", liq=BLUE), V("bucket", "Bucket, empty"), V("wheelbarrow", "Wheelbarrow, loaded", load=True), V("shovel", "Shovel"),
    V("grill", "Grill, lit", food=True), V("hotdog", "Hot dog", mustard=True), V("burger", "Burger", tomato=True), V("corn", "Corn", butter=True), V("cooler", "Cooler"), V("picnic", "Picnic blanket"), V("lawn_chair", "Lawn chair", ramp=TURQ), V("hammock", "Hammock", ramp=TURQ),
    V("beach_umbrella", "Beach umbrella", ramps=[TURQ, SNOW]), V("flipflops", "Flip-flops"), V("float", "Pool float", ramps=[TURQ, SNOW]), V("beach_ball", "Beach ball", ramps=[TURQ, SNOW, CORAL_R, GOLDY]), V("sunglasses", "Sunglasses"), V("ice_cream", "Ice cream", ramps=[CREAMW, CHOC]), V("popsicle", "Popsicle, lime", ramps=[LIME, SNOW]),
    V("can", "Soda can", ramp=TURQ), V("balloon", "Balloon, lime", ramp=LIME), V("bunting", "Bunting, work colors", ramps=[SAFETY, HIVIS, STEEL]), V("lemonade_stand", "Lemonade stand"),
],
"TG": [
    V("turkey", "Roast turkey", garnish=True), V("turkey", "Roast turkey, plain"), V("pie", "Pumpkin pie", fill=PUMPKIN), V("pie", "Pumpkin pie slice", fill=PUMPKIN, slice=True), V("pie", "Apple pie, lattice", fill=CARAMEL, lattice=True), V("pie", "Pecan pie", fill=CHOC),
    V("pumpkin", "Pumpkin", leaf=True), V("pumpkin", "Pumpkin, small", ramp=R((220, 110, 40))), V("pumpkin", "White pumpkin", ramp=CREAMW), V("corn", "Corn", butter=False), V("corn", "Buttered corn", butter=True), V("cornucopia", "Cornucopia"), V("wheat", "Wheat"),
    V("leaf", "Maple leaf, red", kind="maple", ramp=MAPLE), V("leaf", "Maple leaf, orange", kind="maple", ramp=PUMPKIN), V("leaf", "Maple leaf, gold", kind="maple", ramp=MUSTARD), V("leaf", "Oak leaf", kind="oak", ramp=CARAMEL), V("acorn", "Acorn"),
    V("gravy", "Gravy boat"), V("can", "Cranberry sauce can", ramp=BERRY), V("bun", "Dinner roll"), V("glass", "Cider mug", kind="mug", liq=R((220, 150, 60))), V("mug", "Hot cider", ramp=PUMPKIN, liq=R((220, 150, 60))), V("mug", "Cocoa with marshmallows", ramp=CRIMSON, liq=CHOC, marsh=True), V("teapot", "Teapot", ramp=CREAMW),
    V("hat", "Pilgrim hat", kind="pilgrim", ramp=BLACK, band=GOLDY), V("candle", "Candle, amber", ramp=R((230, 170, 80)), h=12), V("candle", "Candle in a holder", ramp=CREAMW, holder=True), V("lantern", "Lantern, metal", ramp=STEEL, shape="metal"), V("wreath", "Autumn wreath", ramp=R((170, 110, 40)), berry=MAPLE, bow=PUMPKIN),
    V("bunting", "Bunting, autumn", ramps=[MAPLE, PUMPKIN, MUSTARD]), V("balloon", "Balloon, orange", ramp=PUMPKIN), V("balloon", "Balloon, maple", ramp=MAPLE), V("basket", "Harvest basket", goods="food"), V("cake", "Spice cake", ramp=CARAMEL, ice=CREAMW, cherry=False), V("cupcake", "Pumpkin cupcake", ramp=PUMPKIN, frost=CREAMW),
    V("cookie", "Leaf cookie", kind="round", ramp=CARAMEL), V("flower", "Sunflower", kind="sunflower", ramp=YELLOW), V("sign", "Blank placard", shape="rect", ramp=PARCH), V("book", "Recipe book", ramp=MAPLE, open=True), V("letter", "Invitation"),
    V("fireplace", "Fireplace"), V("lawn_chair", "Armchair nap: lawn chair", ramp=MAPLE), V("beach_ball", "Football day: ball", ramps=[CARAMEL, CARAMEL, CARAMEL, CARAMEL]), V("log", "Firewood"), V("campfire", "Campfire"), V("raincloud", "Grey November cloud"), V("umbrella", "Umbrella, maple", ramp=MAPLE, ramp2=MAPLE), V("bell", "Dinner bell", ramp=COPPER), V("star", "Star, amber", ramp=MUSTARD),
],
"XMAS": [
    V("tree", "Tree with lights", lights=[CRIMSON, GOLDY, BLUE, SNOW], star=True, baubles=True), V("tree", "Tree, snowy", snow=True, star=True), V("tree", "Tree, bare", ramp=FOREST), V("bauble", "Bauble, red", ramp=CRIMSON, pat="band"), V("bauble", "Bauble, gold", ramp=GOLDY, pat="dots"), V("bauble", "Bauble, blue zigzag", ramp=BLUE, pat="zig"), V("bauble", "Bauble, green", ramp=HOLLY),
    V("star", "Tree-top star"), V("lights", "String lights", ramps=[CRIMSON, GREEN, GOLDY, BLUE]), V("lights", "String lights, warm white", ramps=[GOLDY, SNOW, CHAMP]), V("wreath", "Wreath"), V("wreath", "Wreath, gold bow", ramp=HOLLY, berry=BERRY, bow=GOLDY), V("mistletoe", "Mistletoe"),
    V("stocking", "Stocking, red", stripes=True), V("stocking", "Stocking with a gift", gift=True), V("stocking", "Stocking, green", ramp=GREEN, stripes=True), V("gift", "Gift, red and gold", ramp=CRIMSON, ribbon=GOLDY), V("gift", "Gift, green and white", ramp=GREEN, ribbon=SNOW), V("gift", "Gift, tall, blue", ramp=BLUE, ribbon=SNOW, tall=True), V("gift", "Gift, gold", ramp=GOLDY, ribbon=CRIMSON),
    V("candy_cane", "Candy cane"), V("cookie", "Gingerbread person", kind="ginger"), V("cookie", "Star cookie", kind="star", ramp=CARAMEL), V("cookie", "Heart cookie", kind="heart", ramp=CARAMEL), V("cake", "Yule log", ramp=CHOC, ice=CHOC, layers=1, cherry=True), V("cupcake", "Peppermint cupcake", ramp=CRIMSON, frost=SNOW, sprinkles=True),
    V("mug", "Cocoa with marshmallows", ramp=CRIMSON, liq=CHOC, marsh=True), V("mug", "Cocoa, green mug", ramp=GREEN, liq=CHOC, marsh=True, stripe=True), V("glass", "Eggnog", kind="mug", liq=CREAMW), V("teapot", "Teapot, red", ramp=CRIMSON),
    V("snowman", "Snowman"), V("snowman", "Snowman with a hat", hat=True, scarf=GREEN), V("snowflake", "Snowflake"), V("snowflake", "Snowflake, white", color=SNOW[4]), V("snowglobe", "Snow globe"), V("fireplace", "Fireplace with stockings", stockings=True),
    V("candle", "Candle, red", ramp=CRIMSON, h=12), V("candle", "Candle in a holder", ramp=CREAMW, holder=True), V("lantern", "Lantern, red", ramp=CRIMSON), V("bell", "Bell"), V("bell", "Bell, silver", ramp=SILV), V("bow", "Bow, red"), V("bow", "Bow, gold", ramp=GOLDY),
    V("hat", "Santa hat", kind="santa", ramp=CRIMSON), V("hat", "Elf hat", kind="elf", ramp=GREEN), V("hat", "Beanie", kind="beanie", ramp=CRIMSON, band=SNOW), V("sparkle", "Twinkle"), V("sparkle", "Twinkle, gold", color=GOLDY[4], twin=True), V("bunting", "Bunting, red and green", ramps=[CRIMSON, GREEN, SNOW]), V("letter", "Card in an envelope"),
],
}

def ids(code): return [f"HOL-{code}-{i + 1:02d}" for i in range(len(SET_ITEMS[code]))]
def entry(aid):
    _, code, n = aid.split("-"); return SET_ITEMS[code][int(n) - 1]
def frames(aid):
    import approved; approved.check("holiday", aid)   # the star gate (the boss 2026-11-02)
    d, p, _ = entry(aid); return render(d, p)
def still(aid):
    d, p, _ = entry(aid); fr, _ = render(d, p); return fr[DRAW[d]["still"]]
def title(aid): return entry(aid)[2]
def at(aid, t):
    fr, tk = frames(aid); total = sum(tk); u = (t * 10) % total; acc = 0
    for im, k in zip(fr, tk):
        acc += k
        if u < acc: return im
    return fr[-1]

# ---------------------------------------------------------------- rendering
def render(name, v):
    """All frames of one drawer with params v -> (frames, ticks)."""
    d = DRAW[name]; out = []
    for f in range(d["frames"]):
        P = Px(*d["size"]); d["fn"](P, v, f, d["frames"]); out.append(P.im)
    return out, list(d["ticks"])
