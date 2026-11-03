"""LOOPING SCENES (the boss 2026-11-01: "10-20 custom scenes with loops ... for background of videos, at our resolution").
Pixel backgrounds drawn at 135x240 and shown at 8x = 1080x1920 (NEAREST), each a loop of 8 frames x 3 ticks (2.4 s), every frame
its own drawing (pixkit; rec-marketing-pixel-art). The cast stands on the floor line (scene y ~212 = video y ~1700); the top third
stays calm because the video's headline lives there. daily.py: spec["bg"] = "SCN-03" plays the loop behind a scene, dimmed like a plate.

    import scenes; im = scenes.frame("SCN-03", t)      # 1080x1920 RGB for time t (seconds)
    scenes.SCENES -> [(id, title, note)];  scenes.frames_1x("SCN-03") -> (list of 135x240 RGBA, ticks)
"""
import math, random
from PIL import Image
from pixkit import *
import holiday_assets as HA
from holiday_assets import R, _rng, NAVY, CRIMSON, FOREST, SNOW, ICE, CHOC, CARAMEL, WHEAT, STEEL, PAPER, LEATHER, GRASS, SPARK, FLAME, INK, PASTEL_BLUE, LILAC, SUMMER_BLUE
from props import SCREEN, GLOW, LIMEG, TAXI, ASPHALT

W1, H1 = 135, 240; SCALE = 8; FLOOR = 212; NF = 8; TICKS = [3] * NF
WALL_WARM = R((110, 82, 70)); WALL_COOL = R((70, 78, 96)); WALL_PAPER = R((168, 150, 128), dark=.7); BRICK_W = R((130, 70, 54)); PLASTER = R((196, 184, 164), dark=.72)
FLOOR_WOOD = R((112, 76, 48)); FLOOR_TILE = R((94, 100, 112), dark=.66); FLOOR_CARPET = R((70, 60, 90)); NIGHT = R((22, 26, 48), dark=.6, light=.5); DUSK = R((60, 40, 80))
GLASS_NIGHT = R((30, 38, 64), dark=.6); CITY = R((40, 44, 60), dark=.6); WIN_LIT = (240, 210, 140); WIN_DIM = (120, 110, 90)

def wall(P, ramp, y0=0, y1=FLOOR, base=None):
    P.rect(0, y0, W1 - 1, y1, ramp[2]); P.hline(0, W1 - 1, y1 - 1, ramp[1]); P.hline(0, W1 - 1, y1, ramp[0])
    if base: P.rect(0, y1 - 8, W1 - 1, y1 - 1, base[2]); P.hline(0, W1 - 1, y1 - 8, base[3])

def floor(P, ramp, kind="wood", y0=FLOOR):
    P.rect(0, y0, W1 - 1, H1 - 1, ramp[2])
    if kind == "wood":
        for y in range(y0 + 3, H1, 6): P.hline(0, W1 - 1, y, ramp[1])
        for y in range(y0, H1, 6):
            for x in range(((y // 6) % 2) * 14, W1, 28): P.vline(x, y, min(H1 - 1, y + 5), ramp[1])
    elif kind == "tile":
        for y in range(y0, H1, 8): P.hline(0, W1 - 1, y, ramp[1])
        for x in range(0, W1, 12): P.vline(x, y0, H1 - 1, ramp[1])
        for y in range(y0 + 1, H1, 8):
            for x in range(1, W1, 12): P.put(x, y, ramp[3])
    elif kind == "carpet":
        for y in range(y0 + 1, H1, 3):
            for x in range((y % 2) * 2, W1, 4): P.put(x, y, ramp[1])
    P.hline(0, W1 - 1, y0, ramp[3])

def window_panes(P, x, y, w, h, frame, glass, cols=2, rows=2, sill=True):
    P.rect(x, y, x + w, y + h, frame[2]); P.rect(x + 1, y + 1, x + w - 1, y + h - 1, glass[2])
    for i in range(1, cols): P.vline(x + i * w // cols, y + 1, y + h - 1, frame[2])
    for j in range(1, rows): P.hline(x + 1, x + w - 1, y + j * h // rows, frame[2])
    P.hline(x + 1, x + w - 1, y + 1, glass[3])
    if sill: P.rect(x - 2, y + h, x + w + 2, y + h + 1, frame[3])

def skyline(P, y_base, x0, x1, rr, f, ramp=CITY, lit=0.35, twinkle=True):
    x = x0
    while x < x1:
        w = rr.randrange(8, 20); h = rr.randrange(18, 70); P.rect(x, y_base - h, min(x1, x + w - 1), y_base, ramp[2]); P.vline(x, y_base - h, y_base, ramp[3]); P.vline(min(x1, x + w - 1), y_base - h, y_base, ramp[1])
        for wy in range(y_base - h + 3, y_base - 2, 4):
            for wx in range(x + 2, min(x1, x + w - 2), 3):
                r = rr.random(); on = r < lit; blink = twinkle and r > 0.97 and (f + wx) % 4 == 0
                P.put(wx, wy, WIN_LIT if (on and not blink) else WIN_DIM if r < lit + .1 else ramp[1])
        x += w + rr.randrange(1, 4)

def stars(P, rr, f, y1=120, n=60):
    for i in range(n):
        x = rr.randrange(W1); y = rr.randrange(0, y1); k = rr.random()
        if k > .9: P.put(x, y, SNOW[4] if (f + i) % 4 else SNOW[2])
        else: P.put(x, y, (150, 160, 190) if (f + i) % 8 != 0 else (90, 100, 130))

def ticker(P, x, y, w, f, col=LIMEG):
    """a blank ticker: bars sliding left (never a figure)"""
    rr = _rng(x + y)
    for i in range(6):
        bx = x + (i * 9 - f * 2) % (w + 6) - 3; bw = rr.randrange(3, 7)
        if x <= bx and bx + bw <= x + w: P.hline(bx, bx + bw, y, col[2] if i % 3 else R((240, 110, 90))[2])

def monitor(P, x, y, w, h, f, kind="chart"):
    P.rect(x, y, x + w, y + h, BLACK[1]); P.rect(x + 1, y + 1, x + w - 1, y + h - 1, SCREEN[2])
    if kind == "chart":
        rr = _rng(x * 7 + y); pts = []; px = x + 2
        while px < x + w - 1: pts.append((px, y + 2 + rr.randrange(h - 4))); px += 3
        for a, b in zip(pts, pts[1:]): P.line(a[0], a[1], b[0], b[1], LIMEG[3] if b[1] <= a[1] else R((240, 110, 90))[3])
        P.put(pts[-1][0], pts[-1][1], SNOW[4] if f % 2 else LIMEG[4])
    elif kind == "bars":
        for i, bx in enumerate(range(x + 2, x + w - 1, 3)):
            bh = 2 + ((bx * 3 + f * (1 if i % 2 else -1)) % (h - 3)); P.rect(bx, y + h - 1 - bh, bx, y + h - 2, LIMEG[2] if i % 3 else R((240, 110, 90))[2])
    elif kind == "text":
        for i, ly in enumerate(range(y + 2, y + h - 1, 2)): P.hline(x + 2, x + 2 + ((ly * 5 + f) % max(2, w - 5)), ly, GLOW[1] if i % 3 else GLOW[3])
    P.rect(x + w // 2 - 1, y + h + 1, x + w // 2 + 1, y + h + 3, BLACK[1]); P.rect(x + w // 2 - 3, y + h + 4, x + w // 2 + 3, y + h + 4, BLACK[2])

def desk(P, x, y, w, ramp=FLOOR_WOOD):
    P.rect(x, y, x + w, y + 2, ramp[3]); P.rect(x, y + 3, x + w, y + 4, ramp[2]); P.rect(x + 1, y + 5, x + 2, y + 16, ramp[1]); P.rect(x + w - 2, y + 5, x + w - 1, y + 16, ramp[1])

def plant_pot(P, x, y, f=0):
    P.rect(x + 1, y - 4, x + 6, y, R((190, 110, 70))[2]); P.hline(x, x + 7, y - 5, R((190, 110, 70))[3]); s = [0, 1, 0, -1][f % 4]
    for dx, dy in ((2 + s, -9), (5 + s, -11), (0 + s, -12), (4 + s, -14)): P.rect(x + dx, y + dy, x + dx + 2, y + dy + 2, GRASS[2]); P.put(x + dx, y + dy, GRASS[3])

SCENES = []
def scene(sid, title, note):
    def deco(fn): SCENES.append((sid, title, note, fn)); return fn
    return deco

@scene("SCN-01", "Trading floor", "A wall of blank charts and sliding tickers, desks in a row, the big clock. Lime and coral only.")
def trading_floor(P, f):
    wall(P, WALL_COOL, base=R((50, 56, 70)))
    for x in range(6, 130, 42): monitor(P, x, 96, 34, 20, f, kind="chart" if x % 84 == 6 else "bars")
    P.rect(4, 122, 130, 128, BLACK[1]); ticker(P, 6, 125, 122, f)
    for x in range(10, 130, 44): monitor(P, x, 136, 30, 18, f, kind="text" if x > 60 else "chart")
    for x in range(10, 130, 44): desk(P, x - 4, 164, 38)
    for y in range(26, 90, 16): P.hline(0, W1 - 1, y, WALL_COOL[1])
    P.sphere((58, 6, 76, 24), SNOW, bands=(.05, .2, .6, .96)); P.line(67, 15, 67, 9, INK); P.line(67, 15, 67 + [3, 4, 4, 3, 2, 1, 1, 2][f % 8], 15 + [2, 0, -2, -3, -3, -2, 0, 2][f % 8], CRIMSON[2])
    for x in range(0, W1, 27): P.vline(x, 30, FLOOR - 9, WALL_COOL[1])
    floor(P, FLOOR_CARPET, "carpet"); plant_pot(P, 120, FLOOR - 2, f); plant_pot(P, 4, FLOOR - 2, f + 2)

@scene("SCN-02", "Server room", "Racks of blinking LEDs in cold blue light, a cable tray overhead, the one red light that is always on.")
def server_room(P, f):
    wall(P, R((34, 40, 56), dark=.6), base=R((26, 30, 42), dark=.6))
    P.rect(0, 14, W1 - 1, 18, STEEL[1]); P.hline(0, W1 - 1, 14, STEEL[3])
    for x in range(10, 130, 3): P.vline(x, 15, 17, STEEL[0]) if x % 9 == 1 else None
    rr = _rng(2)
    for rx in range(6, 126, 32):
        P.rect(rx, 28, rx + 26, FLOOR - 2, BLACK[2]); P.vline(rx, 28, FLOOR - 2, BLACK[3])
        for i, y in enumerate(range(32, FLOOR - 8, 7)):
            P.rect(rx + 2, y, rx + 24, y + 4, (34, 34, 42)); P.hline(rx + 2, rx + 24, y, (54, 54, 62))
            for k in range(4): on = (i + k + f + rx) % 3; P.put(rx + 4 + k * 2, y + 2, LIMEG[3] if on else LIMEG[1] if on == 1 else (40, 60, 40))
            P.put(rx + 22, y + 2, CRIMSON[3] if (i + rx) % 5 == 0 else (60, 40, 40))
            P.rect(rx + 13, y + 1, rx + 20, y + 3, (26, 26, 32))
    floor(P, FLOOR_TILE, "tile")
    for x in range(0, W1, 2): P.put(x, 20 + (f % 2 if x % 4 == 0 else 0), (90, 110, 150)) if x % 8 == 0 else None

@scene("SCN-03", "Rooftop at night", "The skyline blinking, a water tower, the moon, one plane crossing. Stars twinkle.")
def rooftop(P, f):
    P.rect(0, 0, W1 - 1, H1 - 1, NIGHT[2]); rr = _rng(3); stars(P, rr, f, 110, 70)
    P.sphere((104, 14, 124, 34), R((240, 232, 200), dark=.75), bands=(.1, .3, .7, .97)); P.sphere((108, 16, 118, 26), R((240, 232, 200), dark=.75), bands=(.9, .95, .97, .99))
    px = (10 + f * 15) % (W1 + 20) - 10; P.put(px, 40, CRIMSON[3] if f % 2 else SNOW[3]); P.put(px + 3, 40, SNOW[4]) if f % 2 == 0 else None
    skyline(P, 150, 0, W1, _rng(31), f, lit=.4)
    skyline(P, 172, 0, W1, _rng(32), f, ramp=R((28, 30, 44), dark=.6), lit=.3)
    # the roof we stand on
    P.rect(0, FLOOR - 10, W1 - 1, FLOOR, R((60, 56, 66), dark=.6)[2]); P.hline(0, W1 - 1, FLOOR - 10, R((60, 56, 66))[3])
    for x in range(0, W1, 7): P.vline(x, FLOOR - 9, FLOOR - 1, R((60, 56, 66), dark=.6)[1])
    # water tower
    P.poly([(26, 118), (14, 130), (38, 130)], R((70, 60, 70)), box=(14, 118, 38, 130), shape="vcyl"); P.vcyl((16, 130, 36, 160), FLOOR_WOOD); P.hline(16, 36, 140, STEEL[1]); P.hline(16, 36, 152, STEEL[1])
    P.hcyl((15, 159, 37, 163), FLOOR_WOOD); P.line(18, 163, 14, FLOOR - 10, STEEL[2]); P.line(34, 163, 38, FLOOR - 10, STEEL[2]); P.line(26, 163, 26, FLOOR - 10, STEEL[2]); P.hline(14, 38, 190, STEEL[1])
    floor(P, R((50, 46, 56), dark=.6), "tile"); P.rect(0, FLOOR, W1 - 1, H1 - 1, R((50, 46, 56), dark=.6)[2])
    for x in range(0, W1, 10): P.vline(x, FLOOR + 1, H1 - 1, R((50, 46, 56), dark=.6)[1])
    P.rect(100, FLOOR - 24, 128, FLOOR - 10, STEEL[1]); P.rect(102, FLOOR - 22, 126, FLOOR - 12, (30, 34, 40)); P.hline(104, 124, FLOOR - 16 + (f % 3 == 0), STEEL[2])  # the AC unit, fan blur

@scene("SCN-04", "Break room", "Coffee machine steaming, the fridge hum, a microwave light, snack shelf and the cereal nobody owns.")
def break_room(P, f):
    wall(P, R((206, 196, 170), dark=.72), base=R((150, 140, 120)))
    for y in range(28, 120, 12):
        for x in range(0, W1, 12): P.hline(x + 1, x + 10, y, R((190, 180, 156))[1]); P.vline(x + (6 if (y // 12) % 2 else 0), y + 1, y + 11, R((190, 180, 156))[1])
    # counter
    P.rect(0, 150, 90, 154, R((80, 86, 96))[3]); P.rect(0, 155, 90, FLOOR - 1, R((96, 72, 50))[2]); P.hline(0, 90, 155, R((96, 72, 50))[3])
    for x in range(0, 90, 22): P.vline(x, 156, FLOOR - 2, R((96, 72, 50))[1]); P.put(x + 11, 170, STEEL[3])
    # coffee machine
    P.rect(10, 126, 32, 150, BLACK[2]); P.rect(12, 128, 30, 134, R((60, 60, 70))[2]); P.put(28, 131, LIMEG[3] if f % 2 else CRIMSON[3]); P.rect(16, 138, 26, 149, (30, 30, 36)); P.rect(18, 143, 24, 149, SNOW[2]); P.rect(19, 141, 23, 143, CHOC[1])
    for i in range(3): y = 122 - ((f * 2 + i * 3) % 9); P.put(17 + i * 3, y, (225, 225, 220)) if y > 112 else None
    # microwave
    P.rect(44, 130, 76, 150, STEEL[2]); P.rect(46, 132, 66, 148, (40, 40, 48) if f % 4 else (120, 110, 70)); P.rect(68, 132, 74, 148, BLACK[1]); P.put(71, 136, LIMEG[3]); P.hline(48, 64, 140, (70, 70, 80)) if f % 4 else None
    # fridge
    P.rect(98, 90, 130, FLOOR - 1, SNOW[2]); P.rect(98, 90, 130, 92, SNOW[3]); P.hline(98, 130, 136, SNOW[1]); P.rect(126, 100, 127, 128, STEEL[2]); P.rect(126, 142, 127, 170, STEEL[2]); P.vline(130, 90, FLOOR - 1, SNOW[1])
    for i, (x, y, c) in enumerate([(104, 100, CRIMSON), (110, 104, LIMEG), (116, 98, SUMMER_BLUE), (106, 116, PAPER)]): P.rect(x, y, x + 4, y + 4, c[2])  # magnets, a blank note
    # shelf
    P.rect(40, 100, 90, 102, FLOOR_WOOD[3]); P.rect(44, 92, 50, 99, CRIMSON[2]); P.rect(54, 90, 62, 99, R((230, 190, 60))[2]); P.rect(66, 94, 72, 99, SUMMER_BLUE[2]); P.rect(76, 91, 84, 99, PAPER[2]); P.rect(77, 93, 83, 95, CRIMSON[1])
    floor(P, FLOOR_TILE, "tile")

@scene("SCN-05", "Legal library", "Roz's room: shelves of books, the green lamp, the scales, rain on a tall window.")
def legal_library(P, f):
    wall(P, R((92, 60, 44)), base=R((70, 44, 32)))
    rr = _rng(5)
    for sx in (4, 96):
        P.rect(sx, 24, sx + 34, FLOOR - 1, R((70, 44, 32))[2])
        for y in range(28, FLOOR - 10, 22):
            P.rect(sx, y + 18, sx + 34, y + 19, R((110, 76, 50))[3]); x = sx + 2
            while x < sx + 32:
                bw = rr.randrange(2, 5); bh = rr.randrange(12, 17); c = rr.choice([CRIMSON, NAVY, FOREST, LEATHER, R((120, 80, 120)), R((180, 150, 90))]); P.rect(x, y + 18 - bh, x + bw - 1, y + 17, c[2]); P.vline(x, y + 18 - bh, y + 17, c[3]); P.put(x + bw // 2, y + 18 - bh + 3, R((220, 190, 120))[3]); x += bw
    # tall window with rain
    window_panes(P, 50, 20, 34, 90, R((70, 44, 32)), GLASS_NIGHT, cols=2, rows=3)
    for i in range(14):
        x = 52 + (i * 7 + f * 3) % 32; y = 22 + (i * 13 + f * 9) % 86; P.put(x, y, (120, 140, 180)); P.put(x, y + 1, (90, 110, 150)) if y + 1 < 109 else None
    skyline_rr = _rng(55); x = 52
    while x < 82:
        w = rr.randrange(4, 9); h = rr.randrange(10, 40); P.rect(x, 108 - h, min(82, x + w), 108, (26, 28, 40)); P.put(x + 1, 108 - h + 4, WIN_LIT) if rr.random() < .5 else None; x += w + 1
    # desk with the lamp and the scales
    desk(P, 44, 150, 46, R((70, 44, 32))); P.rect(50, 138, 54, 150, R((40, 90, 60))[1]); P.poly([(44, 138), (60, 138), (58, 132), (46, 132)], R((40, 120, 70)), box=(44, 132, 60, 138), shape="hcyl"); P.rect(46, 139, 58, 139, FLAME[4] if f % 8 != 5 else FLAME[2])
    P.rect(76, 136, 77, 150, GOLD[1]); P.hline(68, 85, 138 + (f % 4 == 1), GOLD[2]); P.hcyl((65, 143, 71, 145), GOLD); P.hcyl((82, 142, 88, 144), GOLD)
    P.rect(60, 144, 68, 149, PAPER[2]); P.rect(60, 144, 68, 144, PAPER[3])
    floor(P, FLOOR_CARPET, "carpet"); P.rect(20, FLOOR + 6, 114, H1 - 1, R((120, 40, 50))[2]); P.hline(20, 114, FLOOR + 6, R((120, 40, 50))[3])
    for x in range(24, 114, 10): P.put(x, FLOOR + 12, R((160, 120, 60))[2]); P.put(x + 5, FLOOR + 20, R((160, 120, 60))[2])

@scene("SCN-06", "Game studio", "Kit's room: an arcade cabinet playing itself, blank posters, a bean bag, a neon glyph that flickers.")
def game_studio(P, f):
    wall(P, R((50, 40, 72)), base=R((36, 30, 52)))
    for y in range(26, 120, 10):
        for x in range(0, W1, 10): P.put(x + (y // 10) % 2 * 5, y, R((70, 58, 100))[2])
    # posters, blank
    for (x, y, c) in [(10, 30, CRIMSON), (34, 36, SUMMER_BLUE), (104, 30, LIMEG)]:
        P.rect(x, y, x + 18, y + 24, c[1]); P.rect(x + 2, y + 2, x + 16, y + 22, c[2]); P.rect(x + 4, y + 16, x + 14, y + 20, c[0]); P.sphere((x + 5, y + 5, x + 13, y + 13), c, bands=(.3, .5, .75, .95))
    # neon glyph (a lightning bolt, Penny's)
    on = f % 8 not in (3, 6); nc = (255, 120, 200) if on else (120, 60, 100)
    for a, b in [((64, 30), (58, 42)), ((58, 42), (66, 42)), ((66, 42), (60, 56))]: P.line(a[0], a[1], b[0], b[1], nc); P.line(a[0] + 1, a[1], b[0] + 1, b[1], nc)
    # arcade cabinet
    P.rect(90, 96, 126, FLOOR - 1, R((40, 36, 48))[2]); P.rect(90, 96, 126, 100, R((255, 120, 200))[2]); P.rect(94, 104, 122, 128, BLACK[1]); P.rect(96, 106, 120, 126, SCREEN[1])
    rr = _rng(f)
    for i in range(6): P.rect(98 + (i * 4 + f * 2) % 20, 108 + (i * 7) % 16, 99 + (i * 4 + f * 2) % 20, 109 + (i * 7) % 16, [LIMEG, CRIMSON, SUMMER_BLUE, GOLD][i % 4][3])
    P.rect(100, 120 - (f % 3), 103, 122 - (f % 3), SNOW[3]); P.rect(92, 134, 124, 140, R((60, 54, 70))[2]); P.sphere((100, 131, 104, 135), CRIMSON); P.rect(110, 132, 113, 134, SUMMER_BLUE[3]); P.rect(116, 132, 119, 134, GOLD[3])
    P.rect(94, 150, 122, 162, R((255, 120, 200))[1]); P.rect(96, 152, 120, 160, BLACK[0])
    # bean bag + console
    P.sphere((10, 168, 50, 206), R((230, 90, 60)), rim=True); P.sphere((16, 170, 40, 184), R((230, 90, 60)), bands=(.3, .5, .75, .95))
    P.rect(56, 186, 80, 196, BLACK[2]); P.rect(58, 188, 78, 194, (40, 40, 48)); P.put(76, 190, LIMEG[3] if f % 2 else LIMEG[1])
    floor(P, FLOOR_CARPET, "carpet")

@scene("SCN-07", "Lounge", "A couch, the TV cycling colors, a lava lamp, a plant swaying, a window at dusk.")
def lounge(P, f):
    wall(P, R((80, 100, 90)), base=R((60, 74, 68)))
    window_panes(P, 84, 26, 40, 50, R((60, 74, 68)), DUSK, cols=2, rows=2); rr = _rng(7)
    P.rect(86, 60, 122, 74, R((60, 40, 80))[1]); skyline(P, 74, 86, 122, _rng(71), f, ramp=R((34, 26, 50), dark=.6), lit=.4); P.sphere((110, 32, 116, 38), R((255, 230, 160), dark=.8))
    # tv
    P.rect(14, 56, 66, 94, BLACK[2]); cols = [R((40, 80, 160)), R((200, 60, 80)), R((60, 160, 100)), R((220, 180, 60))]; c = cols[f // 2 % 4]; P.rect(16, 58, 64, 92, c[2]); P.rect(16, 58, 64, 60, c[3])
    P.sphere((30 + (f % 4) * 4, 66, 46 + (f % 4) * 4, 84), c, bands=(.6, .75, .9, .97)); P.rect(36, 94, 44, 98, BLACK[1]); P.rect(10, 98, 70, 101, FLOOR_WOOD[3]); P.rect(12, 102, 68, 118, FLOOR_WOOD[2]); P.rect(14, 104, 38, 116, FLOOR_WOOD[1]); P.rect(42, 104, 66, 116, FLOOR_WOOD[1])
    # couch
    P.rect(8, 160, 92, 170, R((60, 90, 150))[3]); P.rect(6, 170, 94, FLOOR - 1, R((60, 90, 150))[2]); P.rect(6, 166, 14, FLOOR - 1, R((60, 90, 150))[3]); P.rect(86, 166, 94, FLOOR - 1, R((60, 90, 150))[3]); P.rect(16, 186, 84, 188, R((60, 90, 150))[1])
    for x in (20, 50): P.rect(x, 172, x + 28, 184, R((60, 90, 150))[3]); P.hline(x, x + 28, 184, R((60, 90, 150))[1])
    P.rect(24, 164, 36, 176, R((230, 180, 60))[2]); P.rect(60, 164, 72, 176, R((230, 90, 60))[2])
    # lava lamp
    P.poly([(108, 140), (120, 140), (118, 172), (110, 172)], R((80, 40, 120)), box=(108, 140, 120, 172), shape="vcyl"); P.rect(112, 136, 116, 140, STEEL[2]); P.rect(110, 172, 118, 176, STEEL[1])
    for i in range(3): y = 146 + ((f * 3 + i * 9) % 24); P.sphere((111, y, 116, y + 4), R((250, 120, 60)), bands=(.3, .5, .75, .95))
    plant_pot(P, 100, FLOOR - 2, f); floor(P, FLOOR_WOOD, "wood")

@scene("SCN-08", "Lobby", "Marble, the elevator light climbing, a reception desk with a bell, the revolving door catching light.")
def lobby(P, f):
    wall(P, R((190, 180, 164), dark=.72), base=R((120, 110, 100)))
    for y in range(20, FLOOR - 10, 16): P.hline(0, W1 - 1, y, R((170, 160, 146))[1])
    # elevators
    for ex in (10, 48):
        P.rect(ex, 70, ex + 28, FLOOR - 1, STEEL[1]); P.rect(ex + 2, 72, ex + 26, FLOOR - 2, R((150, 160, 170))[2]); P.vline(ex + 14, 72, FLOOR - 2, STEEL[0]); P.rect(ex + 8, 60, ex + 20, 66, BLACK[1])
        for k in range(5): P.put(ex + 10 + k * 2, 63, LIMEG[3] if k == ((f + ex // 10) % 5) else (60, 60, 60))
        P.put(ex + 30, 120, LIMEG[3] if (f + ex) % 6 == 0 else CRIMSON[2])
    # desk
    P.rect(84, 150, 130, 154, R((60, 44, 40))[3]); P.rect(86, 155, 130, FLOOR - 1, R((60, 44, 40))[2]); P.hline(86, 130, 170, R((60, 44, 40))[1]); P.rect(90, 158, 126, 162, R((200, 190, 160))[2])
    P.sphere((100, 142, 108, 149), SILVER); P.rect(103, 140, 105, 142, SILVER[2]); P.put(97, 145, SPARK) if f % 8 == 2 else None
    P.rect(114, 140, 126, 149, PAPER[2]); P.rect(114, 140, 126, 140, PAPER[3])
    # revolving door glint
    P.rect(100, 40, 130, 110, R((120, 150, 180), dark=.7)[2]); P.vline(115, 40, 110, STEEL[2]); P.line(102 + (f * 3) % 26, 42, 102 + (f * 3) % 26, 108, (220, 235, 250)); P.rect(100, 40, 130, 41, STEEL[3])
    floor(P, R((200, 196, 186), dark=.72), "tile")
    for x in range(6, W1, 24): P.put(x, FLOOR + 6, R((160, 150, 140))[2]); P.put(x + 12, FLOOR + 18, R((160, 150, 140))[2])

@scene("SCN-09", "Subway platform", "Tiled wall, a blank station sign, a train streaking through every loop, one pigeon.")
def subway(P, f):
    wall(P, R((206, 200, 180), dark=.72), base=R((60, 60, 66)))
    for y in range(20, 150, 8):
        for x in range(0, W1, 8): P.hline(x + 1, x + 7, y, R((180, 174, 156))[1]); P.vline(x + (4 if (y // 8) % 2 else 0), y + 1, y + 7, R((180, 174, 156))[1])
    P.rect(0, 60, W1 - 1, 68, R((40, 80, 60))[2]); P.hline(0, W1 - 1, 60, R((40, 80, 60))[3]); P.rect(40, 54, 94, 76, BLACK[1]); P.rect(42, 56, 92, 74, SNOW[2]); P.sphere((48, 59, 60, 71), R((40, 150, 70))); P.rect(64, 60, 88, 62, BLACK[1]); P.rect(64, 66, 84, 68, BLACK[1])
    # the train window band: a train passes through the dark gap
    P.rect(0, 150, W1 - 1, 190, BLACK[0])
    tx = -60 + f * 30
    for cx in range(tx, tx + 200, 46):
        P.rect(cx, 154, cx + 42, 186, STEEL[1]); P.rect(cx, 154, cx + 42, 156, STEEL[3])
        for wx in range(cx + 4, cx + 40, 9): P.rect(wx, 160, wx + 6, 172, R((250, 230, 170), dark=.8)[2])
        P.hline(cx, cx + 42, 180, R((240, 120, 40))[2]); P.rect(cx + 43, 160, cx + 45, 186, BLACK[1])
    P.rect(0, 190, W1 - 1, 196, R((230, 200, 60))[2]); P.hline(0, W1 - 1, 196, R((230, 200, 60))[1])
    for x in range(0, W1, 6): P.put(x + 2, 193, R((230, 200, 60))[0])
    floor(P, R((120, 116, 110), dark=.66), "tile"); P.sphere((110, FLOOR - 10, 120, FLOOR - 2), GREY); P.sphere((117, FLOOR - 13 + (f % 2), 122, FLOOR - 8 + (f % 2)), GREY); P.put(122, FLOOR - 11 + (f % 2), R((230, 140, 40))[2])
    P.rect(8, 100, 12, FLOOR - 1, R((40, 80, 60))[2]); P.rect(122, 100, 126, FLOOR - 1, R((40, 80, 60))[2])

@scene("SCN-10", "Rain on the window", "A desk by the big window: rain streaks, city lights behind, a mug steaming, the lamp on.")
def rain_window(P, f):
    wall(P, R((70, 76, 92)), base=R((50, 54, 66)))
    P.rect(8, 16, 126, 136, R((50, 54, 66))[2]); P.rect(10, 18, 124, 134, GLASS_NIGHT[2]); P.vline(67, 18, 134, R((50, 54, 66))[3]); P.hline(10, 124, 76, R((50, 54, 66))[3])
    skyline(P, 134, 10, 124, _rng(10), f, ramp=R((30, 34, 50), dark=.6), lit=.45)
    rr = _rng(f)
    for i in range(40):
        x = 10 + (i * 11 + f * 2) % 114; y = 18 + (i * 29 + f * 13) % 116; L = 2 + (i % 3)
        for k in range(L): P.put(x, y + k, (140, 160, 200) if k == 0 else (100, 120, 160)) if y + k < 134 else None
    for i in range(8): x = 12 + (i * 17) % 110; y = 20 + (i * 23 + f * 5) % 110; P.put(x, y, (190, 205, 235))
    desk(P, 10, 150, 114, FLOOR_WOOD); P.rect(14, 136, 44, 150, BLACK[2]); P.rect(16, 138, 42, 148, SCREEN[2]); P.hline(18, 30 + f % 4, 141, GLOW[2]); P.hline(18, 36, 144, GLOW[1])
    P.rect(100, 128, 104, 150, R((60, 60, 70))[1]); P.poly([(92, 128), (112, 128), (110, 120), (94, 120)], R((230, 180, 60)), box=(92, 120, 112, 128), shape="hcyl"); P.rect(94, 129, 110, 129, FLAME[4])
    P.rect(60, 142, 70, 150, CRIMSON[2]); P.rect(71, 144, 73, 148, CRIMSON[1]); P.hline(61, 69, 142, CHOC[1])
    for i in range(2): y = 139 - ((f * 2 + i * 3) % 8); P.put(63 + i * 4, y, (215, 215, 210)) if y > 130 else None
    floor(P, FLOOR_CARPET, "carpet")

@scene("SCN-11", "Bodega at night", "The corner store: awning, a flickering neon glyph, hydrant, headlights sweeping past.")
def bodega(P, f):
    P.rect(0, 0, W1 - 1, H1 - 1, NIGHT[2]); stars(P, _rng(11), f, 40, 20)
    P.rect(0, 40, W1 - 1, FLOOR, BRICK_W[2])
    for y in range(44, FLOOR - 2, 4):
        for x in range(0, W1, 8): P.hline(x + ((y // 4) % 2) * 4, x + ((y // 4) % 2) * 4 + 6, y, BRICK_W[1])
    # storefront window and door
    P.rect(10, 90, 84, 170, R((40, 40, 60))[2]); P.rect(12, 92, 82, 168, R((250, 220, 150), dark=.8)[2])
    for sy in (110, 130, 150):
        P.rect(14, sy, 80, sy + 1, FLOOR_WOOD[3])
        for sx in range(16, 80, 8): P.rect(sx, sy - 8, sx + 5, sy - 1, [CRIMSON, SUMMER_BLUE, LIMEG, GOLD, R((200, 100, 180))][(sx // 8 + sy // 10) % 5][2])
    P.rect(92, 110, 122, FLOOR - 1, R((60, 50, 40))[2]); P.rect(96, 114, 118, 160, R((250, 220, 150), dark=.8)[1]); P.put(116, 150, GOLD[3])
    # awning
    P.rect(4, 74, 128, 90, CRIMSON[2])
    for x in range(4, 128, 10): P.rect(x, 74, x + 4, 90, SNOW[2])
    P.hline(4, 128, 74, CRIMSON[3]); P.hline(4, 128, 90, CRIMSON[0])
    # neon glyph: a coffee cup
    on = f % 8 not in (2, 5); nc = (255, 90, 160) if on else (120, 50, 90)
    P.rect(40, 50, 56, 66, None); P.line(40, 52, 40, 64, nc); P.line(56, 52, 56, 64, nc); P.line(40, 64, 56, 64, nc); P.line(57, 55, 60, 55, nc); P.line(60, 55, 60, 61, nc); P.line(57, 61, 60, 61, nc); P.line(44, 46, 44, 50, nc) if on else None; P.line(50, 45, 50, 49, nc) if on else None
    # hydrant and headlights
    P.vcyl((4, FLOOR - 16, 10, FLOOR - 2), CRIMSON); P.sphere((4, FLOOR - 20, 10, FLOOR - 15), CRIMSON); P.hcyl((1, FLOOR - 12, 5, FLOOR - 10), CRIMSON); P.hcyl((9, FLOOR - 12, 13, FLOOR - 10), CRIMSON)
    floor(P, ASPHALT, "tile"); P.rect(0, FLOOR, W1 - 1, FLOOR + 6, R((120, 116, 110), dark=.66)[2]); P.hline(0, W1 - 1, FLOOR + 6, R((120, 116, 110), dark=.66)[1])
    hx = (f * 22) % (W1 + 40) - 20; P.rect(max(0, hx), FLOOR + 10, min(W1 - 1, hx + 30), FLOOR + 14, (90, 86, 70)); P.rect(max(0, hx + 8), FLOOR + 9, min(W1 - 1, hx + 22), FLOOR + 15, (130, 124, 100))

@scene("SCN-12", "Beach day", "Waves rolling in, the sun on the water, a striped umbrella and a towel. End-of-summer evergreens.")
def beach(P, f):
    P.rect(0, 0, W1 - 1, 120, R((120, 190, 240), dark=.7)[2]); P.rect(0, 0, W1 - 1, 40, R((140, 200, 245), dark=.7)[3])
    P.sphere((100, 20, 124, 44), R((255, 240, 180), dark=.8), bands=(.3, .5, .8, .97))
    for (cx, cy, w) in [(20, 30, 22), (60, 50, 28), (110, 70, 20)]: P.sphere((cx, cy, cx + w, cy + 8), SNOW, bands=(.1, .3, .7, .97)); P.sphere((cx + 6, cy - 5, cx + w - 4, cy + 5), SNOW, bands=(.1, .3, .7, .97))
    P.rect(0, 120, W1 - 1, 170, R((50, 130, 190))[2]); P.hline(0, W1 - 1, 120, R((80, 170, 220))[3])
    for i, y in enumerate((128, 140, 152, 164)):
        off = (f * (2 + i) + i * 7) % 24
        for x in range(-24 + off, W1, 24): P.hline(max(0, x), min(W1 - 1, x + 10), y, R((150, 210, 240))[3]); P.hline(max(0, x + 4), min(W1 - 1, x + 7), y - 1, SNOW[4]) if i % 2 == 0 else None
    for x in range(96, 128, 6): P.put(x + (f % 3), 125 + (x % 5), SPARK)
    edge = 170 + [0, 1, 2, 3, 3, 2, 1, 0][f % 8]; P.rect(0, 170, W1 - 1, edge, R((200, 230, 240))[3]); P.rect(0, edge, W1 - 1, H1 - 1, WHEAT[2]); P.hline(0, W1 - 1, edge, SNOW[3])
    rr = _rng(12)
    for i in range(60): P.put(rr.randrange(W1), rr.randrange(edge + 1, H1), WHEAT[3] if i % 2 else WHEAT[1])
    # umbrella and towel
    P.line(100, 150, 102, 206, FLOOR_WOOD[2]); dome = P.ell_mask((78, 130, 124, 166)) - set((x, y) for x in range(W1) for y in range(150, H1)); P.shade(dome, (78, 130, 124, 166), CRIMSON, bands=(.1, .3, .6, .9))
    for (x, y) in dome:
        if ((x - 78) // 8) % 2: P.put(x, y, SNOW[2] if P.get(x, y)[:3] == CRIMSON[2] else SNOW[3] if P.get(x, y)[:3] == CRIMSON[3] else SNOW[1])
    P.rect(70, 200, 120, 214, R((60, 150, 200))[2])
    for y in range(201, 214, 3): P.hline(70, 120, y, SNOW[2])
    P.sphere((8, 196, 26, 214), R((240, 110, 90)), rim=True); P.sphere((12, 200, 22, 210), SNOW, bands=(.3, .5, .75, .95))

@scene("SCN-13", "To the moon", "Deep space: the earth below, stars, the moon ahead and a little rocket exhaust. For the memes.")
def space(P, f):
    P.rect(0, 0, W1 - 1, H1 - 1, R((8, 10, 24), dark=.5)[2]); rr = _rng(13); stars(P, rr, f, H1, 140)
    P.sphere((90, 20, 130, 60), R((200, 200, 190), dark=.7), rim=True)
    for (x, y, r) in [(100, 30, 3), (116, 44, 4), (106, 50, 2), (120, 28, 2)]: P.sphere((x - r, y - r, x + r, y + r), R((160, 160, 150), dark=.7), bands=(.5, .7, .9, .97))
    # earth, lower left
    P.sphere((-30, 150, 70, 250), R((50, 110, 200)), rim=True)
    for (x, y, w, h) in [(0, 170, 20, 12), (20, 190, 26, 18), (6, 214, 18, 10), (40, 160, 14, 8)]: P.sphere((x, y, x + w, y + h), R((60, 150, 80)), bands=(.1, .3, .6, .9))
    for (x, y, w) in [(10, 160, 16), (30, 200, 20), (48, 180, 10)]: P.sphere((x, y, x + w, y + 4), SNOW, bands=(.0, .1, .5, .97))
    glow = P.ell_mask((-32, 148, 72, 252)) - P.ell_mask((-30, 150, 70, 250)); P.fill(glow, (120, 180, 255))
    # the rocket exhaust trail (the rocket itself is a prop)
    for i in range(10): y = 120 + i * 9 + (f % 3); x = 76 + int(round(2 * math.sin(i + f))); P.put(x, y, [FLAME[4], FLAME[3], FLAME[2], (120, 90, 70)][min(3, i // 3)]); P.put(x + 1, y, FLAME[2]) if i < 4 else None
    for i in range(6): x = (i * 23 + f * 5) % W1; y = (i * 41 + f * 2) % 150; P.put(x, y, SNOW[4]); P.put(x - 1, y, (150, 160, 190))

@scene("SCN-14", "Campfire", "A forest clearing at night: fire flickering, fireflies, a tent and the log we sit on.")
def campfire(P, f):
    P.rect(0, 0, W1 - 1, H1 - 1, R((14, 18, 36), dark=.6)[2]); stars(P, _rng(14), f, 100, 50); P.sphere((20, 14, 34, 28), R((240, 236, 210), dark=.75), bands=(.1, .3, .7, .97))
    rr = _rng(41)
    for x in range(-6, W1 + 6, 11):
        h = rr.randrange(50, 90); P.poly([(x, 150), (x + 6, 150 - h), (x + 12, 150)], R((20, 40, 36), dark=.6), box=(x, 150 - h, x + 12, 150), shape="vcyl")
    P.rect(0, 150, W1 - 1, FLOOR, R((34, 52, 40), dark=.6)[2])
    # tent
    P.poly([(104, 150), (84, 190), (124, 190)], R((80, 110, 70)), box=(84, 150, 124, 190), shape="vcyl"); P.poly([(104, 158), (96, 190), (112, 190)], R((40, 60, 40)), box=(96, 158, 112, 190), bands=(.0, .05, .1, .2)); P.put(104, 149, R((80, 110, 70))[3])
    # fire
    P.hcyl((30, 194, 60, 200), FLOOR_WOOD); P.hcyl((44, 194, 72, 200), FLOOR_WOOD)
    shapes = [[(50, 160), (62, 176), (60, 194), (42, 194), (38, 178)], [(52, 158), (64, 178), (60, 194), (42, 194), (40, 174)], [(48, 162), (62, 174), (62, 194), (40, 194), (36, 180)], [(51, 156), (60, 176), (58, 194), (44, 194), (38, 176)]]
    P.poly(shapes[f % 4], FLAME, box=(36, 156, 64, 194)); P.poly([(51, 176), (56, 186), (54, 194), (46, 194), (44, 186)], R((255, 236, 160)), box=(44, 176, 56, 194))
    for i in range(4): P.put(44 + (i * 5 + f * 3) % 16, 154 - ((f * 2 + i * 4) % 14), R((255, 160, 60))[3])
    for i in range(7): x = (i * 19 + f * 3) % W1; y = 100 + (i * 13 + f * (1 if i % 2 else -1)) % 70; P.put(x, y, LIMEG[4] if (f + i) % 3 else LIMEG[1])
    floor(P, R((60, 72, 50), dark=.6), "carpet"); P.hcyl((6, FLOOR - 6, 30, FLOOR + 2), FLOOR_WOOD)
    # glow on the ground
    for x in range(26, 76):
        for y in range(196, FLOOR + 8):
            if (x + y + f) % 3 == 0 and abs(x - 50) + abs(y - 200) < 30: P.put(x, y, R((120, 90, 50))[2])

@scene("SCN-15", "Boardroom", "The long table, a big screen with a blank line drawing itself, the city through glass.")
def boardroom(P, f):
    wall(P, R((60, 66, 80)), base=R((44, 48, 58)))
    P.rect(0, 14, W1 - 1, 110, GLASS_NIGHT[2]); skyline(P, 110, 0, W1, _rng(15), f, lit=.4)
    for x in range(0, W1, 34): P.vline(x, 14, 110, R((44, 48, 58))[3])
    P.hline(0, W1 - 1, 14, R((44, 48, 58))[3]); P.hline(0, W1 - 1, 110, R((44, 48, 58))[3])
    P.rect(40, 116, 94, 150, BLACK[2]); P.rect(42, 118, 92, 148, SCREEN[2])
    pts = [(44, 142), (52, 134), (60, 138), (68, 126), (76, 130), (84, 122), (90, 120)]; n = 2 + (f % 7)
    for a, b in zip(pts[:n], pts[1:n]): P.line(a[0], a[1], b[0], b[1], LIMEG[3])
    P.put(pts[min(n, 6)][0], pts[min(n, 6)][1], SNOW[4]) if f % 2 else None
    for y in (126, 134, 142): P.hline(44, 90, y, (46, 60, 76)) if y not in [p[1] for p in pts] else None
    P.rect(10, 164, 124, 170, R((50, 36, 30))[3]); P.rect(12, 170, 122, 180, R((50, 36, 30))[2]); P.rect(20, 180, 26, FLOOR - 1, R((50, 36, 30))[1]); P.rect(108, 180, 114, FLOOR - 1, R((50, 36, 30))[1])
    for x in range(16, 120, 26): P.rect(x, 160, x + 10, 162, PAPER[2]); P.put(x + 4, 158, STEEL[3])
    for x in range(10, 128, 28): P.rect(x, 184, x + 14, 194, BLACK[2]); P.rect(x + 2, 194, x + 12, FLOOR - 1, BLACK[1])
    P.sphere((66, 150, 70, 158), R((250, 120, 60)), bands=(.3, .5, .75, .95)) if f % 8 < 4 else None
    floor(P, FLOOR_CARPET, "carpet")

@scene("SCN-16", "The vault", "Steel walls, the round door, coins glinting and a red laser that sweeps. For the Receipts.")
def vault(P, f):
    wall(P, R((80, 86, 100), dark=.66), base=R((60, 64, 74), dark=.66))
    for y in range(20, FLOOR - 8, 24): P.hline(0, W1 - 1, y, R((110, 116, 130))[3]); P.hline(0, W1 - 1, y + 1, R((60, 64, 74))[1])
    for x in range(0, W1, 30): P.vline(x, 20, FLOOR - 8, R((110, 116, 130))[3])
    for y in range(26, FLOOR - 8, 24):
        for x in range(6, W1, 30): P.put(x, y, R((130, 136, 150))[4]); P.put(x + 1, y + 1, R((40, 44, 54))[1])
    P.sphere((70, 60, 126, 116), R((120, 126, 140), dark=.66), rim=True); P.sphere((80, 70, 116, 106), R((100, 106, 120), dark=.66), bands=(.3, .5, .75, .95)); rot = f * math.pi / 8
    for i in range(6): a = i * math.pi / 3 + rot; P.line(98, 88, int(98 + 12 * math.cos(a)), int(88 + 12 * math.sin(a)), STEEL[3])
    P.sphere((94, 84, 102, 92), STEEL); P.rect(60, 84, 68, 92, STEEL[2]); P.rect(62, 86, 66, 90, (60, 64, 74))
    # coin stacks and a chest
    for (x, h) in [(14, 12), (22, 18), (30, 9), (40, 15)]:
        for i in range(h // 3): P.hcyl((x, FLOOR - 4 - i * 3, x + 7, FLOOR - 2 - i * 3), GOLD); P.hline(x + 1, x + 6, FLOOR - 4 - i * 3, GOLD[3])
    P.put(24, FLOOR - 24, SPARK) if f % 8 == 1 else None; P.put(42, FLOOR - 20, SPARK) if f % 8 == 5 else None
    P.rect(100, FLOOR - 22, 126, FLOOR - 2, FLOOR_WOOD[2]); P.hcyl((100, FLOOR - 28, 126, FLOOR - 20), FLOOR_WOOD); P.rect(100, FLOOR - 21, 126, FLOOR - 20, GOLD[2]); P.rect(111, FLOOR - 22, 115, FLOOR - 18, GOLD[3])
    ly = 130 + [0, 6, 12, 18, 24, 18, 12, 6][f % 8]; P.hline(0, W1 - 1, ly, (255, 60, 60)); P.hline(0, W1 - 1, ly + 1, (120, 30, 30))
    floor(P, FLOOR_TILE, "tile")

def frames_1x(sid):
    fn = next(fn for s, _, _, fn in SCENES if s == sid); out = []
    for f in range(NF):
        P = Px(W1, H1); fn(P, f); out.append(P.im)
    return out, list(TICKS)

_CACHE = {}
def frame(sid, t):
    """1080x1920 RGB frame of scene sid at time t (loops)."""
    import approved; approved.check("scene", sid)   # the star gate (the boss 2026-11-02)
    if sid not in _CACHE: _CACHE[sid] = frames_1x(sid)
    fr, tk = _CACHE[sid]; total = sum(tk); u = (t * 10) % total; acc = 0; im = fr[-1]
    for im_, k in zip(fr, tk):
        acc += k
        if u < acc: im = im_; break
    return scaled(im, SCALE).convert("RGB")

def titles(): return [(s, t, n) for s, t, n, _ in SCENES]
