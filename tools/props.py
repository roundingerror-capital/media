"""RANDOM PROPS (the boss 2026-11-01): 500 props for the cast's shenanigans, PROP-001..PROP-500, ten families of 50:
OFFICE · FOOD (NYC) · TECH · TOOLS · SPORTS & GAMES · TOYS · STREET (NYC) · FANTASY (Kit's studio) · MUSIC & PARTY · FINANCE DESK.
Same rules as holiday_assets (pixkit; rec-marketing-pixel-art): final size first, one light, ramps, form shading, selective outline,
one drawing per frame. Nothing carries digits or a brand; screens and signs are blank; finance props show symbols, never figures.

    import props; frames, ticks = props.frames("PROP-042"); im = props.still("PROP-042"); props.FAMILIES
"""
import math, random
from pixkit import *
import holiday_assets as HA
from holiday_assets import drawer, DRAW, R, V, render, _rng, _bob, _sw, GOLDY, SILV, MIDNIGHT, CREAMW, BRICK, COPPER, TURQ, CORAL_R, SUMMER_BLUE, SPRING_GRN
from holiday_assets import NAVY, CRIMSON, FOREST, HOLLY, SNOW, ICE, CHOC, CARAMEL, BERRY, PUMPKIN, MAPLE, MUSTARD, WHEAT, PLUM, PASTEL_PINK, PASTEL_BLUE, PASTEL_YEL, PASTEL_GRN, LILAC
from holiday_assets import SAFETY, HIVIS, DENIM, STEEL, RUBBER, PAPER, PARCH, LEATHER, SKY, GRASS, SPARK, EMBER, FLAME, INK

SCREEN = R((40, 60, 80), dark=.6); GLOW = R((120, 200, 230), light=.4); LIMEG = R((200, 240, 60), light=.3); TAXI = R((240, 190, 40)); ASPHALT = R((70, 70, 78), dark=.6, light=.4)
PIZZA = R((230, 170, 70)); CHEESE = R((246, 210, 110)); TOMATO = R((210, 60, 50)); DOUGH = R((226, 190, 130)); AVO = R((130, 170, 70)); SALMON = R((240, 130, 100)); RICE = R((240, 236, 220), dark=.74)

# ---------------------------------------------------------------- office
@drawer("laptop", size=(32, 24), frames=4, ticks=[6, 6, 6, 6])
def laptop(P, v, f, nf):
    c = v.get("ramp", STEEL); P.box(5, 2, 27, 16, c, top=1, side=1); P.rect(7, 3, 25, 14, SCREEN[2]); P.rect(7, 3, 25, 3, SCREEN[3])
    for i, y in enumerate((5, 8, 11)): P.hline(9, 9 + [8, 12, 6][i] + (f % 2) * 2, y, LIMEG[3] if i == 0 else GLOW[2])
    if f % 2 == 0: P.rect(9 + [8, 12, 6][2] + 1, 11, 9 + [8, 12, 6][2] + 1, 11, GLOW[4])
    P.box(2, 17, 30, 21, c, top=1, side=1); P.rect(12, 18, 20, 19, c[1])
    for x in range(4, 29, 2): P.put(x, 18, c[3]) if x % 4 == 0 else None
    P.selout()

@drawer("monitor", frames=4, ticks=[6, 6, 6, 6])
def monitor(P, v, f, nf):
    c = v.get("ramp", BLACK); P.box(2, 2, 21, 16, c, top=1, side=1); P.rect(3, 3, 20, 14, SCREEN[2]); P.rect(10, 17, 13, 20, c[2]); P.hcyl((6, 20, 17, 22), c)
    if v.get("chart"):
        pts = [(4, 12), (7, 9), (10, 11), (13, 6), (16, 8), (19, 4)]
        for a, b in zip(pts, pts[1:]): P.line(a[0], a[1], b[0], b[1], LIMEG[3])
    else:
        for i, y in enumerate((5, 8, 11)): P.hline(5, 5 + [9, 6, 11][i], y, GLOW[2])
        if f % 2 == 0: P.put(5 + 11 + 1, 11, GLOW[4])
    P.selout()

@drawer("keyboard", size=(32, 16))
def keyboard(P, v, f, nf):
    c = v.get("ramp", STEEL); P.box(1, 4, 30, 13, c, top=1, side=1)
    for y in (6, 8, 10):
        for x in range(3, 29, 3): P.rect(x, y, x + 1, y, c[0])
    P.rect(9, 12, 22, 12, c[0]); P.selout()

@drawer("mouse", size=(16, 24), frames=4, ticks=[8, 2, 8, 2])
def mouse(P, v, f, nf):
    c = v.get("ramp", SNOW); P.sphere((3, 6, 12, 22), c, rim=True); P.vline(7, 7, 12, c[1]); P.hline(4, 11, 12, c[1]); P.rect(7, 0, 8, 5, STEEL[1]); P.put(8, 1 + f % 2, STEEL[3]); P.selout()

@drawer("phone", size=(16, 24), frames=4, ticks=[8, 2, 2, 8])
def phone(P, v, f, nf):
    c = v.get("ramp", BLACK); P.box(3, 1, 12, 22, c, top=1, side=1); P.rect(4, 3, 11, 19, SCREEN[2]); P.rect(6, 1, 9, 2, c[0]); P.rect(6, 20, 9, 21, c[1])
    if f in (1, 2): P.rect(5, 5, 10, 8, LIMEG[2]); P.put(6, 6, INK)
    for y in (11, 14): P.hline(5, 10, y, GLOW[1])
    P.selout()

@drawer("headphones", frames=4, ticks=[8, 2, 8, 2])
def headphones(P, v, f, nf):
    c = v.get("ramp", BLACK); pad = v.get("pad", CRIMSON); arc = P.ell_mask((3, 2, 20, 20)) - P.ell_mask((6, 5, 17, 20)) - set((x, y) for x in range(24) for y in range(12, 24)); P.shade(arc, (3, 2, 20, 20), c)
    P.box(2, 11, 7, 20, pad, top=1, side=1); P.box(16, 11, 21, 20, pad, top=1, side=1); P.rect(3, 13, 5, 18, c[2]); P.rect(17, 13, 19, 18, c[2]); P.selout()
    if f == 1: P.put(1, 10, SPARK); P.put(22, 10, SPARK)

@drawer("desk_lamp", frames=4, ticks=[8, 2, 8, 2])
def desk_lamp(P, v, f, nf):
    c = v.get("ramp", CRIMSON); on = f != 2
    P.hcyl((3, 20, 14, 23), c); P.line(8, 19, 12, 8, c[1]); P.line(9, 19, 13, 8, c[2]); P.poly([(8, 2), (20, 2), (22, 10), (12, 10)], c, box=(8, 2, 22, 10), shape="hcyl")
    if on: P.rect(13, 10, 21, 10, FLAME[4]); P.poly([(13, 11), (21, 11), (23, 16), (11, 16)], R((255, 240, 180), dark=.8), box=(11, 11, 23, 16), bands=(.0, .05, .1, .2))
    P.selout()

@drawer("plant", frames=4, ticks=[8, 2, 8, 2])
def plant(P, v, f, nf):
    pot = v.get("ramp", R((190, 110, 70))); g = v.get("leaf", GRASS); s = _sw(f, nf)
    P.poly([(6, 15), (17, 15), (16, 23), (7, 23)], pot, box=(6, 15, 17, 23), shape="vcyl"); P.hcyl((5, 13, 18, 16), pot)
    for (x, y, fl) in [(4, 6, -1), (16, 5, 1), (8, 2, -1), (13, 1, 1)]: P.sphere((x + s * fl, y, x + 6 + s * fl, y + 7), g, rim=True)
    P.rect(11, 6, 12, 13, g[1]); P.selout()

@drawer("cactus", frames=4, ticks=[8, 2, 8, 2])
def cactus(P, v, f, nf):
    pot = v.get("ramp", R((200, 120, 60))); g = R((80, 150, 80))
    P.poly([(6, 16), (17, 16), (16, 23), (7, 23)], pot, box=(6, 16, 17, 23), shape="vcyl"); P.hcyl((5, 14, 18, 17), pot)
    P.vcyl((9, 2, 14, 14), g); P.sphere((9, 1, 14, 4), g); P.vcyl((3, 6, 6, 11), g); P.hcyl((3, 10, 9, 12), g); P.vcyl((17, 4, 20, 9), g); P.hcyl((14, 8, 20, 10), g)
    for x, y in [(10, 4), (13, 7), (11, 10), (4, 7), (18, 5)]: P.put(x, y, SNOW[3])
    if v.get("flower") and f != 3: P.sphere((10, 0, 13, 2), PINK)
    P.selout()

@drawer("notebook")
def notebook(P, v, f, nf):
    c = v.get("ramp", BLUE); P.box(4, 2, 19, 22, c, top=1, side=2); P.rect(4, 2, 6, 22, c[1])
    for y in range(4, 22, 3): P.put(5, y, SILV[3])
    P.rect(9, 7, 16, 8, PAPER[2]); P.rect(9, 10, 14, 10, PAPER[1]); P.selout()

@drawer("pen", size=(24, 24), frames=4, ticks=[8, 2, 8, 2])
def pen(P, v, f, nf):
    c = v.get("ramp", BLUE); s = _sw(f, nf); P.line(5, 21, 18 + s, 3, c[2]); P.line(6, 21, 19 + s, 3, c[3]); P.line(4, 21, 17 + s, 3, c[1]); P.rect(3, 21, 5, 23, STEEL[2]); P.put(3, 23, INK); P.rect(17 + s, 1, 19 + s, 3, STEEL[3]); P.selout()

@drawer("pencil", size=(24, 24), frames=4, ticks=[8, 2, 8, 2])
def pencil(P, v, f, nf):
    c = v.get("ramp", YELLOW); s = _sw(f, nf); P.line(5, 20, 18 + s, 4, c[2]); P.line(6, 20, 19 + s, 4, c[3]); P.line(4, 20, 17 + s, 4, c[1])
    P.poly([(3, 20), (6, 22), (2, 23)], WHEAT, box=(2, 20, 6, 23)); P.put(2, 23, INK); P.rect(17 + s, 2, 20 + s, 4, PINK[2]); P.rect(16 + s, 4, 19 + s, 5, STEEL[2]); P.selout()

@drawer("sticky", size=(16, 16), frames=4, ticks=[8, 2, 8, 2])
def sticky(P, v, f, nf):
    c = v.get("ramp", YELLOW); s = _sw(f, nf) if v.get("peel") else 0
    P.rect(2, 2, 13, 13, c[2]); P.rect(2, 2, 13, 3, c[3]); P.poly([(13 - 3 - s, 13), (13, 13), (13, 10 - s)], c, box=(9, 9, 13, 13), bands=(.0, .05, .1, .2)) if s else P.rect(11, 11, 13, 13, c[1])
    for y in (6, 9): P.hline(4, 10, y, c[0])
    P.selout()

@drawer("stapler", size=(24, 16), frames=4, ticks=[8, 2, 8, 2])
def stapler(P, v, f, nf):
    c = v.get("ramp", CRIMSON); up = 3 if f in (1, 3) else 0
    P.box(2, 11, 21, 14, BLACK, top=1, side=1); P.rect(3, 9, 20, 10, STEEL[2])
    P.poly([(3, 4 - up), (17, 3 - up // 2), (21, 6), (21, 9), (3, 9 - up)], c, box=(3, 1, 21, 9), shape="hcyl"); P.hline(4, 16, 4 - up, c[3]); P.selout()

@drawer("scissors", frames=4, ticks=[8, 2, 8, 2])
def scissors(P, v, f, nf):
    c = v.get("ramp", CRIMSON); o = 1 if f in (1, 3) else 0
    P.line(12, 11, 22, 1 + o, STEEL[2]); P.line(13, 11, 23, 1 + o, STEEL[3]); P.line(12, 11, 22 + o, 3, STEEL[1]); P.line(11, 12, 22, 5, STEEL[1])
    ring1 = P.ell_mask((1, 11 - o, 9, 17 - o)) - P.ell_mask((3, 13 - o, 7, 15 - o)); ring2 = P.ell_mask((5, 15, 13, 21)) - P.ell_mask((7, 17, 11, 19)); P.shade(ring1 | ring2, (1, 11, 13, 21), c); P.put(12, 11, GOLD[3]); P.selout()

@drawer("calculator", size=(16, 24))
def calculator(P, v, f, nf):
    c = v.get("ramp", BLACK); P.box(2, 1, 13, 22, c, top=1, side=1); P.rect(3, 3, 12, 6, R((150, 170, 150))[2]); P.rect(3, 3, 12, 3, R((150, 170, 150))[3])
    for y in range(9, 21, 3):
        for x in (3, 6, 9): P.rect(x, y, x + 1, y + 1, SNOW[2] if (x, y) != (9, 18) else SAFETY[2])
    P.selout()

@drawer("coffee_pot", frames=4, ticks=[6, 6, 6, 6])
def coffee_pot(P, v, f, nf):
    P.vcyl((5, 8, 17, 21), ICE, bands=(.02, .1, .6, .95)); P.vcyl((6, 14, 16, 20), CHOC); P.hcyl((5, 6, 17, 9), BLACK); P.rect(9, 4, 13, 6, BLACK[2]); P.rect(17, 10, 20, 11, BLACK[2]); P.rect(19, 11, 20, 17, BLACK[1]); P.rect(17, 17, 20, 18, BLACK[2])
    P.hcyl((4, 21, 18, 23), BLACK); P.put(7, 15, CHOC[4])
    y = 2 - (f % 3); P.put(8, y, (215, 215, 210)); P.put(12, y - 1, (215, 215, 210)) if y > 0 else None; P.selout()

@drawer("water_bottle", size=(16, 24))
def water_bottle(P, v, f, nf):
    c = v.get("ramp", TURQ); P.vcyl((4, 6, 11, 22), c); P.hcyl((4, 3, 11, 7), c); P.rect(5, 0, 10, 3, BLACK[2]); P.rect(5, 0, 10, 0, BLACK[3]); P.rect(5, 10, 10, 15, SNOW[2]); P.vline(5, 7, 21, c[3]); P.selout()

@drawer("papers", size=(24, 16))
def papers(P, v, f, nf):
    for i in range(4): P.rect(3 + i, 12 - i * 3, 19 + i, 14 - i * 3, PAPER[2] if i % 2 else PAPER[3]); P.hline(3 + i, 19 + i, 14 - i * 3, PAPER[1])
    for y in (5, 7): P.hline(8, 16, y, (170, 160, 140))
    P.selout()

@drawer("folder", size=(24, 20))
def folder(P, v, f, nf):
    c = v.get("ramp", MUSTARD); P.box(2, 5, 21, 18, c, top=1, side=1); P.rect(2, 3, 10, 5, c[3]); P.rect(4, 9, 19, 16, PAPER[2]); P.rect(3, 10, 21, 18, c[2]); P.rect(3, 10, 21, 10, c[3]); P.selout()

@drawer("trash", frames=4, ticks=[8, 2, 8, 2])
def trash(P, v, f, nf):
    c = v.get("ramp", STEEL); P.poly([(5, 6), (18, 6), (17, 22), (6, 22)], c, box=(5, 6, 18, 22), shape="vcyl"); P.hcyl((4, 4, 19, 7), c); P.rect(9, 2, 14, 4, c[2])
    for x in (8, 11, 14): P.vline(x, 8, 20, c[1])
    if v.get("full"): P.rect(7, 2, 10, 5, PAPER[2]); P.sphere((12, 1, 16, 5), GRASS)
    P.selout()

@drawer("whiteboard", size=(32, 24))
def whiteboard(P, v, f, nf):
    P.box(1, 1, 30, 20, SILV, top=1, side=1); P.rect(2, 2, 29, 19, SNOW[3]); P.rect(2, 2, 29, 2, SNOW[4])
    if v.get("chart"):
        pts = [(5, 15), (10, 11), (14, 13), (19, 7), (24, 9), (27, 5)]
        for a, b in zip(pts, pts[1:]): P.line(a[0], a[1], b[0], b[1], CRIMSON[2])
    else:
        for i, y in enumerate((6, 10, 14)): P.hline(5, 5 + [14, 20, 10][i], y, [BLUE, CRIMSON, GRASS][i][2])
    P.rect(1, 20, 30, 22, SILV[2]); P.rect(6, 19, 10, 20, CRIMSON[2]); P.rect(12, 19, 16, 20, BLUE[2]); P.selout()

@drawer("briefcase", frames=4, ticks=[8, 2, 8, 2])
def briefcase(P, v, f, nf):
    c = v.get("ramp", LEATHER); P.box(2, 8, 21, 21, c, top=1, side=2); P.rect(8, 4, 15, 8, c[1]); P.rect(9, 5, 14, 7, None); P.rect(2, 13, 21, 14, c[1]); P.rect(10, 12, 13, 15, GOLD[2]); P.put(10, 12, GOLD[4]); P.selout()

@drawer("backpack", frames=4, ticks=[8, 2, 8, 2])
def backpack(P, v, f, nf):
    c = v.get("ramp", BLUE); P.sphere((4, 3, 19, 22), c, rim=True); P.rect(4, 12, 19, 22, c[2]); P.hline(5, 18, 22, c[1]); P.box(7, 13, 16, 20, c, top=1, side=1); P.rect(7, 13, 16, 13, c[0]); P.rect(10, 1, 13, 3, c[1]); P.rect(11, 2, 12, 2, None); P.rect(11, 15, 12, 16, GOLD[3]); P.selout()

@drawer("badge", size=(16, 24), frames=4, ticks=[8, 2, 8, 2])
def badge(P, v, f, nf):
    c = v.get("ramp", BLUE); s = _sw(f, nf); P.rect(7, 0, 8, 5, BLACK[1]); P.rect(5, 5, 10, 7, BLACK[2]); P.box(2 + s, 7, 13 + s, 22, SNOW, top=1, side=1); P.rect(2 + s, 7, 13 + s, 10, c[2]); P.rect(4 + s, 12, 8 + s, 16, GREY[2])
    for y in (18, 20): P.hline(4 + s, 11 + s, y, (170, 160, 140))
    P.selout()

@drawer("duck", size=(16, 16), frames=4, ticks=[8, 2, 8, 2])
def duck(P, v, f, nf):
    c = v.get("ramp", YELLOW); dy = _bob(f, nf) if f % 2 else 0; P.sphere((2, 8 + dy, 13, 15), c, rim=True); P.sphere((7, 2 + dy, 14, 9 + dy), c); P.rect(13, 5 + dy, 15, 6 + dy, PUMPKIN[2]); P.put(11, 4 + dy, INK); P.put(10, 4 + dy, SNOW[4]) if False else None
    P.poly([(2, 10 + dy), (0, 8 + dy), (3, 13 + dy)], c, box=(0, 8, 3, 13)); P.selout(); P.put(9, 4 + dy, c[4])

@drawer("globe", frames=4, ticks=[4, 4, 4, 4])
def globe(P, v, f, nf):
    P.sphere((3, 2, 20, 19), SUMMER_BLUE, rim=True); rr = _rng(5)
    land = [(6, 6, 10, 9), (12, 5, 17, 8), (8, 11, 13, 15), (15, 12, 18, 16)]
    for (x0, y0, x1, y1) in land:
        x0 = (x0 + f * 3); x1 = (x1 + f * 3)
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                xx = 4 + (x - 4) % 16
                if P.get(xx, y)[:3] in (SUMMER_BLUE[2], SUMMER_BLUE[3], SUMMER_BLUE[1]): P.put(xx, y, GRASS[2])
    P.rect(11, 19, 12, 21, STEEL[1]); P.hcyl((6, 21, 17, 23), STEEL); P.line(20, 3, 22, 10, STEEL[2]); P.line(22, 10, 20, 19, STEEL[2]); P.selout(); P.put(7, 5, SNOW[4])

@drawer("printer", size=(32, 24), frames=4, ticks=[6, 6, 6, 6])
def printer(P, v, f, nf):
    c = v.get("ramp", SILV); P.box(3, 8, 28, 20, c, top=1, side=2); P.box(7, 4, 24, 9, c, top=1, side=1); P.rect(9, 2, 22, 4, PAPER[2])
    out = 10 + f * 2; P.rect(8, 14, 22, 14 + min(6, out - 10), PAPER[3]) if f else None; P.rect(6, 13, 25, 13, BLACK[1]); P.put(25, 10, LIMEG[3] if f % 2 else LIMEG[1]); P.selout()

@drawer("office_chair", size=(24, 32))
def office_chair(P, v, f, nf):
    c = v.get("ramp", BLACK); P.box(5, 2, 18, 14, c, top=1, side=2); P.rect(6, 4, 17, 12, c[3]) if False else None; P.hcyl((3, 15, 20, 20), c); P.rect(11, 20, 12, 26, STEEL[2])
    for dx in (-7, -3, 3, 7): P.line(11, 26, 11 + dx, 30, STEEL[1]); P.put(11 + dx, 31, STEEL[2])
    P.rect(2, 12, 4, 17, c[2]); P.rect(19, 12, 21, 17, c[2]); P.selout()

# ---------------------------------------------------------------- food (NYC)
@drawer("pizza", frames=4, ticks=[8, 2, 8, 2])
def pizza(P, v, f, nf):
    whole = v.get("whole")
    if whole:
        P.sphere((2, 2, 21, 21), DOUGH, bands=(.1, .3, .6, .9)); P.sphere((3, 3, 20, 20), CHEESE, bands=(.1, .3, .6, .9))
        for x, y in [(7, 7), (13, 6), (10, 12), (15, 13), (7, 15), (12, 17)]: P.sphere((x, y, x + 2, y + 2), TOMATO)
        P.line(12, 2, 12, 21, DOUGH[1]); P.line(2, 12, 21, 12, DOUGH[1])
    else:
        P.poly([(3, 2), (21, 2), (12, 22)], CHEESE, box=(3, 2, 21, 22), bands=(.1, .3, .6, .9)); P.poly([(3, 2), (21, 2), (20, 5), (4, 5)], DOUGH, flat=True); P.hline(3, 21, 2, DOUGH[3])
        for x, y in [(7, 7), (14, 7), (11, 12), (12, 17)]: P.sphere((x, y, x + 2, y + 2), TOMATO)
        if f == 1: P.put(16, 11, CHEESE[4])
    P.selout()

@drawer("bagel", frames=4, ticks=[8, 2, 8, 2])
def bagel(P, v, f, nf):
    ring = P.ell_mask((2, 4, 21, 20)) - P.ell_mask((9, 10, 14, 14)); P.shade(ring, (2, 4, 21, 20), CARAMEL, rim=True)
    if v.get("seeds"):
        for x, y in [(6, 8), (12, 6), (17, 9), (8, 15), (16, 16), (4, 12)]: P.put(x, y, CREAMW[3])
    if v.get("cream"): P.hcyl((4, 11, 19, 13), SNOW)
    P.selout()

@drawer("pretzel", frames=4, ticks=[8, 2, 8, 2])
def pretzel(P, v, f, nf):
    c = R((170, 100, 50)); ring = P.ell_mask((3, 2, 20, 16)) - P.ell_mask((8, 6, 15, 12)); P.shade(ring, (3, 2, 20, 16), c)
    P.poly([(6, 10), (9, 10), (17, 22), (14, 22)], c, box=(6, 10, 17, 22), shape="hcyl"); P.poly([(15, 10), (18, 10), (10, 22), (7, 22)], c, box=(7, 10, 18, 22), shape="hcyl")
    for x, y in [(6, 5), (15, 4), (11, 15), (9, 19), (16, 18)]: P.put(x, y, SNOW[4])
    P.selout()

@drawer("taco", size=(24, 20))
def taco(P, v, f, nf):
    shell = R((230, 190, 90)); half = P.ell_mask((2, 2, 21, 19)) - set((x, y) for x in range(24) for y in range(0, 10)); P.shade(half, (2, 2, 21, 19), shell, bands=(.1, .3, .6, .9))
    P.hcyl((4, 7, 19, 11), CHOC); P.hcyl((5, 5, 18, 8), GRASS); P.sphere((7, 6, 10, 9), TOMATO); P.sphere((14, 5, 17, 8), TOMATO); P.hline(5, 18, 10, CHEESE[3]); P.selout()

@drawer("sushi", size=(24, 16), frames=4, ticks=[8, 2, 8, 2])
def sushi(P, v, f, nf):
    kind = v.get("kind", "nigiri")
    if kind == "nigiri": P.hcyl((3, 7, 20, 14), RICE); P.hcyl((2, 3, 21, 9), SALMON); P.hline(4, 19, 5, SALMON[4]); P.rect(10, 3, 13, 14, FOREST[2])
    else:
        P.sphere((4, 1, 19, 15), BLACK, bands=(.2, .4, .7, .95)); P.sphere((7, 4, 16, 12), RICE, bands=(.1, .3, .6, .9)); P.sphere((10, 6, 13, 9), SALMON); P.put(10, 7, GRASS[2])
    P.selout()

@drawer("ramen", frames=4, ticks=[6, 6, 6, 6])
def ramen(P, v, f, nf):
    bowl = v.get("ramp", CRIMSON); P.poly([(2, 11), (21, 11), (18, 22), (5, 22)], bowl, box=(2, 11, 21, 22), shape="vcyl"); P.hcyl((2, 9, 21, 12), R((230, 180, 110))); P.hline(4, 19, 10, YELLOW[3]); P.hline(6, 17, 11, YELLOW[2])
    P.sphere((6, 7, 10, 10), SNOW); P.rect(7, 8, 9, 8, PINK[2]); P.rect(13, 7, 17, 9, R((190, 70, 50))[2]); P.rect(11, 6, 12, 10, GRASS[2])
    P.line(15, 1, 19, 10, WOOD[1]); P.line(17, 0, 20, 9, WOOD[2]); P.hline(3, 20, 13, bowl[4])
    for i in range(2): P.put(8 + i * 6, 4 - ((f + i * 2) % 5), (215, 215, 210))
    P.selout()

@drawer("donut", size=(20, 20))
def donut(P, v, f, nf):
    ice = v.get("ramp", PINK); ring = P.ell_mask((1, 2, 18, 18)) - P.ell_mask((7, 8, 12, 12)); P.shade(ring, (1, 2, 18, 18), CARAMEL, rim=True)
    top = {(x, y) for x, y in ring if y < 12}; P.shade(top, (1, 2, 18, 14), ice, bands=(.1, .3, .6, .9))
    for i, (x, y) in enumerate([(4, 6), (8, 4), (13, 5), (15, 9), (6, 10)]): P.put(x, y, [SNOW, BLUE, YELLOW, GRASS][i % 4][3])
    P.selout()

@drawer("sandwich", size=(24, 20))
def sandwich(P, v, f, nf):
    P.hcyl((2, 2, 21, 7), CARAMEL); P.hcyl((2, 7, 21, 9), GRASS); P.hcyl((3, 9, 20, 11), TOMATO); P.hcyl((3, 11, 20, 13), CHEESE); P.hcyl((3, 13, 20, 15), PINK); P.hcyl((2, 15, 21, 18), CARAMEL)
    for x in (6, 11, 16): P.put(x, 4, CREAMW[3])
    P.selout()

@drawer("apple", size=(16, 16))
def apple(P, v, f, nf):
    c = v.get("ramp", CRIMSON); P.sphere((2, 4, 13, 15), c, rim=True); P.rect(7, 1, 8, 4, WOOD[1]); P.poly([(8, 3), (12, 1), (11, 4)], GRASS, box=(8, 1, 12, 4)); P.put(4, 6, c[4]); P.put(5, 7, c[4]); P.selout()

@drawer("banana", frames=4, ticks=[8, 2, 8, 2])
def banana(P, v, f, nf):
    c = YELLOW; arc = P.ell_mask((1, 6, 22, 22)) - P.ell_mask((2, 0, 23, 15)); P.shade(arc, (1, 6, 22, 22), c, shape="hcyl", rim=False)
    P.hline(6, 17, 17, c[3]); P.put(1, 11, CHOC[1]); P.put(2, 10, CHOC[2]); P.put(22, 11, CHOC[1]); P.selout()

@drawer("avocado", size=(20, 24))
def avocado(P, v, f, nf):
    P.sphere((2, 1, 17, 22), R((60, 100, 40)), rim=True); P.sphere((4, 4, 15, 20), AVO, bands=(.1, .3, .6, .9)); P.sphere((7, 10, 12, 16), R((140, 90, 50)), rim=True); P.selout(); P.put(8, 11, CARAMEL[4])

@drawer("chips", size=(20, 24), frames=4, ticks=[8, 2, 8, 2])
def chips(P, v, f, nf):
    c = v.get("ramp", CRIMSON); P.box(3, 4, 16, 21, c, top=1, side=2); P.rect(2, 2, 17, 4, c[3]); P.rect(2, 21, 17, 23, c[1])
    for x in range(3, 17, 3): P.put(x, 3, c[1]); P.put(x, 22, c[0])
    P.sphere((6, 9, 13, 16), YELLOW, bands=(.1, .3, .6, .9)); P.rect(5, 7, 14, 8, PAPER[2]); P.selout()

@drawer("wine", size=(16, 24), frames=4, ticks=[8, 2, 8, 2])
def wine(P, v, f, nf):
    liq = v.get("liq", R((140, 30, 60))); P.sphere((2, 1, 13, 13), ICE, bands=(.02, .1, .5, .95)); P.rect(2, 7, 13, 13, ICE[2]); P.sphere((3, 6, 12, 13), liq); P.rect(3, 9, 12, 13, liq[2]); P.hline(3, 12, 13, ICE[1])
    P.rect(7, 14, 8, 20, ICE[2]); P.hcyl((3, 20, 12, 22), ICE); P.selout(); P.put(4, 3, SNOW[4])

@drawer("cocktail", frames=4, ticks=[8, 2, 8, 2])
def cocktail(P, v, f, nf):
    liq = v.get("liq", R((240, 120, 80))); P.poly([(2, 2), (21, 2), (12, 13)], ICE, box=(2, 2, 21, 13), bands=(.02, .1, .5, .95)); P.poly([(4, 4), (19, 4), (12, 12)], liq, box=(4, 4, 19, 12), bands=(.1, .3, .6, .9))
    P.rect(11, 13, 12, 20, ICE[2]); P.hcyl((5, 20, 18, 22), ICE); P.line(14, 0, 19, 4, SNOW[3]); P.sphere((17, 0, 20, 3), CRIMSON); P.sphere((15, 3, 18, 5), YELLOW); P.selout()
    if f == 1: P.put(6, 6, SNOW[4])

@drawer("candy", size=(24, 16), frames=4, ticks=[8, 2, 8, 2])
def candy(P, v, f, nf):
    c = v.get("ramp", PINK); P.sphere((7, 3, 16, 12), c, rim=True); P.poly([(7, 6), (2, 2), (2, 12), (7, 9)], c, box=(2, 2, 7, 12), shape="hcyl"); P.poly([(16, 6), (21, 2), (21, 12), (16, 9)], c, box=(16, 2, 21, 12), shape="hcyl")
    for x in (9, 12, 15): P.vline(x, 4, 11, SNOW[3]) if P.get(x, 7)[3] else None
    P.selout()

@drawer("chocolate", size=(16, 24))
def chocolate(P, v, f, nf):
    P.box(2, 1, 13, 22, CHOC, top=1, side=1)
    for y in range(2, 22, 5):
        for x in range(3, 13, 5): P.box(x, y, x + 3, y + 3, CHOC, top=1, side=1)
    P.rect(2, 9, 13, 14, PURPLE[2]); P.rect(2, 9, 13, 9, PURPLE[3]); P.rect(4, 11, 11, 12, SILV[3]); P.selout()

@drawer("popcorn", frames=4, ticks=[8, 2, 8, 2])
def popcorn(P, v, f, nf):
    P.poly([(5, 10), (18, 10), (16, 23), (7, 23)], CRIMSON, box=(5, 10, 18, 23), shape="vcyl")
    for x in range(6, 18, 3): P.vline(x, 11, 22, SNOW[3]) if P.get(x, 15)[3] else None
    for (x, y) in [(5, 6), (9, 4), (13, 5), (17, 7), (7, 8), (11, 7), (15, 9)]: P.sphere((x - 2, y - 2, x + 2, y + 2), CREAMW)
    if f == 1: P.sphere((10, 0, 13, 3), CREAMW)
    P.selout()

@drawer("hot_sauce", size=(16, 24))
def hot_sauce(P, v, f, nf):
    P.vcyl((4, 8, 11, 22), CRIMSON); P.poly([(6, 2), (9, 2), (11, 9), (4, 9)], CRIMSON, box=(4, 2, 11, 9), shape="vcyl"); P.hcyl((5, 0, 10, 2), GRASS); P.rect(5, 12, 10, 17, PAPER[2]); P.rect(6, 13, 9, 14, FLAME[2]); P.put(7, 14, FLAME[4]); P.selout()

@drawer("coffee_cup", size=(16, 24), frames=4, ticks=[5, 5, 5, 5])
def coffee_cup(P, v, f, nf):
    c = v.get("ramp", SNOW); P.poly([(3, 7), (12, 7), (11, 22), (4, 22)], c, box=(3, 7, 12, 22), shape="vcyl"); P.hcyl((2, 5, 13, 8), BLACK); P.rect(6, 3, 9, 5, BLACK[2]); P.rect(4, 11, 11, 15, v.get("band", CARAMEL)[2])
    for i in range(2): P.put(6 + i * 3, 2 - ((f + i * 2) % 4), (215, 215, 210)) if 2 - ((f + i * 2) % 4) >= 0 else None
    P.selout()

# ---------------------------------------------------------------- tech
@drawer("server", size=(24, 32), frames=4, ticks=[3, 3, 3, 3])
def server(P, v, f, nf):
    P.box(3, 1, 20, 30, BLACK, top=1, side=2)
    for i, y in enumerate(range(3, 29, 5)):
        P.rect(4, y, 18, y + 3, (40, 40, 46)); P.hline(4, 18, y, (60, 60, 66))
        for k in range(3): P.put(5 + k * 2, y + 1, (LIMEG[3] if (i + k + f) % 3 else LIMEG[1]) if k < 2 else (CRIMSON[3] if (i + f) % 4 == 0 else CRIMSON[1]))
        P.rect(11, y + 1, 17, y + 2, (28, 28, 32))
    P.selout()

@drawer("router", size=(24, 16), frames=4, ticks=[4, 4, 4, 4])
def router(P, v, f, nf):
    P.box(2, 8, 21, 14, SNOW, top=1, side=1); P.rect(5, 2, 5, 8, BLACK[2]); P.rect(18, 1, 18, 8, BLACK[2])
    for k in range(4): P.put(6 + k * 3, 11, LIMEG[3] if (k + f) % 2 else LIMEG[1])
    P.selout()

@drawer("usb", size=(24, 12))
def usb(P, v, f, nf):
    c = v.get("ramp", BLUE); P.box(8, 3, 21, 9, c, top=1, side=1); P.box(2, 4, 8, 8, SILV, top=1, side=0); P.rect(3, 5, 4, 5, BLACK[1]); P.rect(3, 7, 4, 7, BLACK[1]); P.selout()

@drawer("battery", size=(24, 12), frames=4, ticks=[5, 5, 5, 5])
def battery(P, v, f, nf):
    P.box(2, 2, 20, 10, BLACK, top=1, side=1); P.rect(21, 4, 22, 8, STEEL[2])
    for k in range(4):
        if k <= f: P.rect(4 + k * 4, 4, 6 + k * 4, 8, LIMEG[2] if f == 3 else GOLDY[2])
    P.selout()

@drawer("bulb", frames=4, ticks=[8, 2, 8, 2])
def bulb(P, v, f, nf):
    on = f != 2; g = R((255, 230, 140), dark=.8) if on else ICE
    P.sphere((5, 1, 18, 14), g, bands=(.02, .1, .5, .95) if not on else (.0, .05, .4, .95), rim=not on); P.rect(8, 14, 15, 16, g[2]); P.rect(8, 17, 15, 20, STEEL[2]); P.hline(8, 15, 18, STEEL[1]); P.rect(10, 21, 13, 22, STEEL[1])
    if on: P.line(10, 10, 12, 6, FLAME[2]); P.line(12, 6, 14, 10, FLAME[2]); P.put(2, 4, SPARK); P.put(21, 4, SPARK); P.put(12, -1 + 1, SPARK)
    else: P.line(10, 10, 12, 6, STEEL[1]); P.line(12, 6, 14, 10, STEEL[1])
    P.selout()

@drawer("magnet", frames=4, ticks=[8, 2, 8, 2])
def magnet(P, v, f, nf):
    arc = P.ell_mask((3, 2, 20, 19)) - P.ell_mask((8, 7, 15, 19)) - set((x, y) for x in range(24) for y in range(12, 24)); P.shade(arc, (3, 2, 20, 19), CRIMSON)
    P.box(3, 11, 7, 18, CRIMSON, top=0, side=1); P.box(16, 11, 20, 18, CRIMSON, top=0, side=1); P.box(3, 18, 7, 22, SILV, top=1, side=1); P.box(16, 18, 20, 22, SILV, top=1, side=1); P.selout()
    if f == 1: P.put(2, 23, SPARK); P.put(21, 23, SPARK)

@drawer("camera", size=(24, 20), frames=4, ticks=[8, 2, 8, 2])
def camera(P, v, f, nf):
    c = v.get("ramp", BLACK); P.box(2, 5, 21, 18, c, top=1, side=2); P.rect(7, 3, 13, 5, c[2]); P.sphere((7, 6, 16, 15), SILV); P.sphere((9, 8, 14, 13), SCREEN, bands=(.3, .5, .7, .95)); P.put(10, 9, SNOW[4]); P.rect(17, 7, 19, 8, CRIMSON[3] if f == 1 else CRIMSON[1]); P.rect(3, 7, 5, 10, c[3]); P.selout()
    if f == 1: P.sparkle(11, 10, 2, SPARK)

@drawer("speaker", size=(16, 24), frames=4, ticks=[3, 3, 3, 3])
def speaker(P, v, f, nf):
    c = v.get("ramp", BLACK); P.box(2, 1, 13, 22, c, top=1, side=1); k = f % 2
    P.sphere((4 - k, 11 - k, 11 + k, 18 + k), GREY, rim=True); P.sphere((6, 13, 9, 16), BLACK); P.sphere((5, 4, 10, 9), GREY); P.sphere((7, 6, 8, 7), BLACK); P.selout()
    if k: P.put(0, 14, SPARK); P.put(15, 14, SPARK)

@drawer("controller", size=(24, 16), frames=4, ticks=[8, 2, 8, 2])
def controller(P, v, f, nf):
    c = v.get("ramp", BLACK); P.sphere((1, 3, 10, 14), c); P.sphere((13, 3, 22, 14), c); P.rect(5, 3, 18, 11, c[2]); P.hline(6, 17, 3, c[3])
    P.rect(4, 6, 6, 8, GREY[2]); P.put(5, 7, GREY[0]); P.rect(16, 5, 17, 6, CRIMSON[3] if f == 1 else CRIMSON[2]); P.rect(18, 7, 19, 8, BLUE[2]); P.rect(16, 9, 17, 10, GRASS[2]); P.rect(14, 7, 15, 8, YELLOW[2]); P.rect(10, 7, 11, 8, GREY[1]); P.rect(12, 7, 13, 8, GREY[1]); P.selout()

@drawer("joystick", frames=4, ticks=[8, 2, 8, 2])
def joystick(P, v, f, nf):
    s = _sw(f, nf); P.box(3, 15, 20, 22, BLACK, top=1, side=2); P.rect(11 + s // 2, 6, 12 + s // 2, 15, STEEL[2]); P.sphere((8 + s, 1, 15 + s, 8), CRIMSON, rim=True); P.rect(5, 17, 7, 18, CRIMSON[3]); P.rect(16, 17, 18, 18, CRIMSON[3]); P.selout(); P.put(10 + s, 3, CRIMSON[4])

@drawer("robot", frames=4, ticks=[8, 2, 8, 2])
def robot(P, v, f, nf):
    c = v.get("ramp", STEEL); dy = [0, -1, 0, 0][f % 4]; P.box(6, 4 + dy, 17, 12 + dy, c, top=1, side=2); P.rect(11, 1 + dy, 12, 4 + dy, c[1]); P.put(11, 0 + dy, CRIMSON[3] if f % 2 else CRIMSON[1])
    P.rect(8, 6 + dy, 9, 8 + dy, LIMEG[3]); P.rect(14, 6 + dy, 15, 8 + dy, LIMEG[3]); P.hline(9, 14, 10 + dy, BLACK[1]); P.box(7, 13 + dy, 16, 19 + dy, c, top=0, side=2); P.rect(10, 14 + dy, 13, 16 + dy, BLACK[2]); P.put(11, 15 + dy, LIMEG[3])
    P.rect(3, 13 + dy, 5, 18 + dy, c[2]); P.rect(18, 13 + dy, 20, 18 + dy, c[2]); P.rect(8, 20, 10, 23, c[1]); P.rect(13, 20, 15, 23, c[1]); P.selout()

@drawer("drone", size=(32, 16), frames=4, ticks=[2, 2, 2, 2])
def drone(P, v, f, nf):
    c = v.get("ramp", STEEL); P.box(12, 6, 19, 11, c, top=1, side=1)
    for (hx, hy) in [(5, 5), (26, 5), (5, 12), (26, 12)]:
        sx, sy = (12 if hx < 16 else 19), (7 if hy < 8 else 10); P.line(sx, sy, hx, hy, c[2]); P.line(sx, sy + 1, hx, hy + 1, c[1])
        P.rect(hx - 1, hy - 1, hx + 1, hy + 1, BLACK[2]); w = 4 if f % 2 else 2; P.hline(hx - w, hx + w, hy - 2, GREY[3]); P.put(hx, hy - 2, GREY[4])
    P.sphere((14, 8, 16, 10), SCREEN); P.put(17, 7, LIMEG[3] if f % 2 else CRIMSON[3]); P.selout()

@drawer("vr", size=(24, 16))
def vr(P, v, f, nf):
    P.box(2, 4, 21, 13, BLACK, top=1, side=1); P.rect(3, 5, 20, 5, BLACK[3]); P.rect(5, 7, 9, 10, SCREEN[2]); P.rect(14, 7, 18, 10, SCREEN[2]); P.hcyl((0, 6, 2, 11), GREY); P.hcyl((21, 6, 23, 11), GREY); P.rect(10, 11, 13, 13, BLACK[0]); P.selout(); P.put(6, 8, GLOW[4]); P.put(15, 8, GLOW[4])

@drawer("tablet", size=(24, 20))
def tablet(P, v, f, nf):
    P.box(2, 1, 21, 18, BLACK, top=1, side=1); P.rect(3, 3, 20, 16, SCREEN[2]); P.rect(3, 3, 20, 3, SCREEN[3])
    for i, y in enumerate((6, 9, 12)): P.hline(5, 5 + [10, 6, 12][i], y, GLOW[2])
    P.selout()

@drawer("tv", size=(32, 24), frames=4, ticks=[2, 2, 2, 2])
def tv(P, v, f, nf):
    c = v.get("ramp", WOOD); P.box(1, 3, 30, 21, c, top=1, side=2); P.rect(3, 5, 22, 18, SCREEN[2]); rr = _rng(f)
    for y in range(5, 19):
        for x in range(3, 23):
            if rr.random() < .25: P.put(x, y, (120 + rr.randrange(100),) * 3)
    P.sphere((24, 7, 28, 11), BLACK); P.sphere((24, 13, 28, 17), BLACK); P.line(8, 3, 4, 0, GREY[2]); P.line(10, 3, 14, 0, GREY[2]); P.rect(6, 21, 9, 23, c[1]); P.rect(22, 21, 25, 23, c[1]); P.selout()

@drawer("floppy", size=(16, 16))
def floppy(P, v, f, nf):
    c = v.get("ramp", BLUE); P.box(1, 1, 14, 14, c, top=1, side=1); P.rect(4, 1, 11, 6, SILV[2]); P.rect(8, 2, 10, 5, BLACK[1]); P.rect(3, 9, 12, 14, PAPER[2]); P.rect(3, 9, 12, 9, PAPER[3]); P.selout()

@drawer("cd", size=(16, 16), frames=4, ticks=[3, 3, 3, 3])
def cd(P, v, f, nf):
    ring = P.ell_mask((1, 1, 14, 14)) - P.ell_mask((6, 6, 9, 9)); P.shade(ring, (1, 1, 14, 14), SILV, rim=True)
    for i in range(3):
        a = f * .5 + i * 2.1; x = int(round(7.5 + 4.5 * math.cos(a))); y = int(round(7.5 + 4.5 * math.sin(a))); P.put(x, y, [PINK, TURQ, GOLDY][i][3]); P.put(x + 1, y, [PINK, TURQ, GOLDY][i][4])
    P.selout()

@drawer("dish", frames=4, ticks=[8, 2, 8, 2])
def dish(P, v, f, nf):
    P.sphere((2, 2, 19, 19), SILV, rim=True); P.sphere((5, 5, 16, 16), GREY, bands=(.0, .05, .3, .9)); P.line(10, 10, 18, 4, STEEL[2]); P.sphere((17, 2, 20, 5), CRIMSON); P.rect(11, 19, 12, 22, STEEL[2]); P.hcyl((6, 22, 17, 23), STEEL); P.selout()
    if f == 1: P.put(21, 1, SPARK); P.put(22, 3, SPARK)

@drawer("chip", size=(16, 16))
def chip(P, v, f, nf):
    P.box(4, 4, 11, 11, BLACK, top=1, side=1); P.rect(6, 6, 9, 9, GREY[1]); P.put(6, 6, GOLD[3])
    for k in range(4): P.put(5 + k * 2, 2, GOLD[2]); P.put(5 + k * 2, 3, GOLD[1]); P.put(5 + k * 2, 12, GOLD[2]); P.put(5 + k * 2, 13, GOLD[1]); P.put(2, 5 + k * 2, GOLD[2]); P.put(3, 5 + k * 2, GOLD[1]); P.put(12, 5 + k * 2, GOLD[1]); P.put(13, 5 + k * 2, GOLD[2])
    P.selout()

@drawer("keycap", size=(16, 16), frames=4, ticks=[8, 2, 8, 2])
def keycap(P, v, f, nf):
    c = v.get("ramp", SNOW); d = 1 if f == 1 else 0; P.box(2, 2 + d, 13, 12 + d, c, top=1, side=1); P.rect(2, 12 + d, 13, 13, c[0]); P.rect(5, 5 + d, 7, 7 + d, c[1]) if v.get("mark") else None; P.selout()

@drawer("smartwatch", size=(16, 24), frames=4, ticks=[8, 2, 8, 2])
def smartwatch(P, v, f, nf):
    band = v.get("ramp", BLACK); P.rect(5, 0, 10, 6, band[2]); P.rect(5, 18, 10, 23, band[2]); P.box(2, 6, 13, 18, BLACK, top=1, side=1); P.rect(3, 7, 12, 17, SCREEN[2]); P.put(14, 10, STEEL[3])
    if f % 2: P.hline(5, 10, 10, LIMEG[3]); P.hline(5, 8, 13, GLOW[2])
    else: P.sphere((6, 9, 9, 12), CRIMSON)
    P.selout()

@drawer("cable", size=(24, 16), frames=4, ticks=[8, 2, 8, 2])
def cable(P, v, f, nf):
    c = v.get("ramp", BLACK)
    for x in range(3, 21): P.put(x, 8 + int(round(3 * math.sin(x / 2.5 + f * .3))), c[2]); P.put(x, 9 + int(round(3 * math.sin(x / 2.5 + f * .3))), c[1])
    P.box(0, 5, 4, 11, SILV, top=1, side=0); P.box(20, 5, 23, 11, SILV, top=1, side=0); P.selout()

# ---------------------------------------------------------------- tools (extra)
@drawer("pliers", frames=4, ticks=[8, 2, 8, 2])
def pliers(P, v, f, nf):
    c = v.get("ramp", CRIMSON); o = 1 if f in (1, 3) else 0
    P.line(4, 22, 11, 11, c[2]); P.line(5, 22, 12, 11, c[2]); P.line(11, 22, 13, 11, c[2]); P.line(12, 22, 14, 11, c[2])
    P.poly([(9, 11), (15, 11), (17, 4 - o), (13, 2 - o), (9, 5)], STEEL, box=(9, 2, 17, 11), bands=(.1, .3, .6, .95)); P.put(12, 11, STEEL[0]); P.selout()

@drawer("paintbrush", frames=4, ticks=[8, 2, 8, 2])
def paintbrush(P, v, f, nf):
    c = v.get("ramp", BLUE); s = _sw(f, nf); P.line(6, 22, 15 + s, 8, WOOD[2]); P.line(7, 22, 16 + s, 8, WOOD[1]); P.poly([(13 + s, 6), (18 + s, 6), (18 + s, 9), (13 + s, 9)], SILV, box=(13, 6, 18, 9), shape="hcyl")
    P.poly([(13 + s, 1), (19 + s, 1), (18 + s, 6), (13 + s, 6)], c, box=(13, 1, 19, 6), shape="vcyl"); P.put(14 + s, 2, c[4]); P.selout()
    if f == 1: P.put(20 + s, 0, c[3])

@drawer("nail", size=(8, 24))
def nail(P, v, f, nf):
    P.rect(1, 1, 6, 2, STEEL[3]); P.rect(3, 3, 4, 20, STEEL[2]); P.vline(3, 3, 20, STEEL[3]); P.put(3, 21, STEEL[1]); P.put(4, 21, STEEL[1]); P.put(3, 22, STEEL[0]); P.selout()

@drawer("gear", frames=4, ticks=[3, 3, 3, 3])
def gear(P, v, f, nf):
    c = v.get("ramp", STEEL); rot = f * math.pi / 16
    for i in range(8):
        a = i * math.pi / 4 + rot; x = 11.5 + 9 * math.cos(a); y = 11.5 + 9 * math.sin(a); P.sphere((int(x) - 1, int(y) - 1, int(x) + 1, int(y) + 1), c)
    ring = P.ell_mask((3, 3, 20, 20)) - P.ell_mask((9, 9, 14, 14)); P.shade(ring, (3, 3, 20, 20), c, rim=True); P.selout()

@drawer("anvil", size=(24, 16))
def anvil(P, v, f, nf):
    c = BLACK; P.box(2, 3, 21, 8, c, top=1, side=1); P.poly([(2, 3), (0, 4), (0, 6), (2, 8)], c, box=(0, 3, 2, 8)); P.rect(7, 9, 16, 11, c[2]); P.box(5, 12, 18, 15, c, top=1, side=1); P.hline(3, 20, 3, STEEL[3]); P.selout()

@drawer("pickaxe", frames=4, ticks=[8, 2, 8, 2])
def pickaxe(P, v, f, nf):
    s = _sw(f, nf); P.line(7, 22, 15 + s, 6, WOOD[2]); P.line(8, 22, 16 + s, 6, WOOD[1])
    arc = P.ell_mask((5 + s, 2, 23 + s, 12)) - P.ell_mask((7 + s, 5, 21 + s, 16)); P.shade(arc, (5 + s, 2, 23 + s, 12), STEEL); P.selout()

@drawer("blowtorch", frames=3, ticks=[3, 2, 3])
def blowtorch(P, v, f, nf):
    P.vcyl((6, 8, 13, 22), BLUE); P.hcyl((6, 7, 13, 9), STEEL); P.rect(9, 3, 10, 7, STEEL[2]); P.rect(10, 1, 14, 3, STEEL[1])
    fl = [[(14, 2), (20, 0), (22, 2), (16, 4)], [(14, 2), (21, 1), (21, 3), (16, 4)], [(14, 2), (19, 0), (23, 2), (16, 4)]][f % 3]; P.poly(fl, R((120, 180, 255), light=.5), box=(14, 0, 23, 4)); P.put(15, 2, SNOW[4]); P.selout()

@drawer("level", size=(32, 12))
def level(P, v, f, nf):
    P.box(1, 3, 30, 9, YELLOW, top=1, side=1); P.rect(12, 4, 19, 8, ICE[2]); P.rect(14, 5, 17, 7, R((180, 230, 120))[3]); P.vline(13, 4, 8, INK); P.vline(18, 4, 8, INK); P.selout()

@drawer("toolbelt", size=(32, 16))
def toolbelt(P, v, f, nf):
    P.hcyl((1, 2, 30, 6), LEATHER); P.rect(13, 2, 18, 6, GOLD[2]); P.rect(14, 3, 17, 5, LEATHER[1]); P.box(3, 6, 12, 14, LEATHER, top=1, side=1); P.box(19, 6, 28, 14, LEATHER, top=1, side=1)
    P.rect(5, 3, 6, 9, STEEL[2]); P.rect(9, 4, 10, 8, WOOD[2]); P.rect(22, 3, 23, 9, YELLOW[2]); P.selout()

# ---------------------------------------------------------------- sports and games
@drawer("basketball", frames=4, ticks=[8, 2, 8, 2])
def basketball(P, v, f, nf):
    c = R((230, 120, 50)); dy = _bob(f, nf); P.sphere((3, 3 + dy, 20, 20 + dy), c, rim=True); P.vline(11, 4 + dy, 19 + dy, c[0]); P.hline(4, 19, 11 + dy, c[0])
    for x in range(4, 20):
        y = 11 + dy + int(round(4 * math.sin((x - 4) / 15 * math.pi))); P.put(x, y - 7, c[0]) if P.get(x, y - 7)[3] else None; P.put(x, y + 7 - 2 * int(round(4 * math.sin((x - 4) / 15 * math.pi))) + 0, c[0]) if False else None
    P.selout()

@drawer("soccer", frames=4, ticks=[8, 2, 8, 2])
def soccer(P, v, f, nf):
    dy = _bob(f, nf); P.sphere((3, 3 + dy, 20, 20 + dy), SNOW, rim=True)
    for (x, y) in [(11, 7), (6, 11), (16, 11), (8, 17), (14, 17)]: P.sphere((x - 1, y - 1 + dy, x + 1, y + 1 + dy), BLACK)
    P.selout()

@drawer("football", size=(24, 16), frames=4, ticks=[8, 2, 8, 2])
def football(P, v, f, nf):
    c = R((150, 80, 40)); P.sphere((1, 3, 22, 12), c, rim=True); P.hline(7, 16, 7, SNOW[3])
    for x in (8, 10, 12, 14): P.vline(x, 6, 8, SNOW[3])
    P.put(1, 7, SNOW[2]); P.put(22, 7, SNOW[2]); P.selout()

@drawer("baseball", frames=4, ticks=[8, 2, 8, 2])
def baseball(P, v, f, nf):
    s = _sw(f, nf); P.line(4, 22, 18 + s, 4, WOOD[2]); P.line(5, 22, 19 + s, 4, WOOD[1]); P.line(6, 22, 20 + s, 4, WOOD[2]); P.rect(3, 21, 6, 23, WOOD[1])
    P.sphere((1, 1, 9, 9), SNOW, rim=True); P.line(3, 2, 7, 8, CRIMSON[2]); P.line(2, 7, 8, 3, CRIMSON[2]) if False else None; P.selout()

@drawer("racket", frames=4, ticks=[8, 2, 8, 2])
def racket(P, v, f, nf):
    c = v.get("ramp", BLUE); s = _sw(f, nf); ring = P.ell_mask((5 + s, 1, 18 + s, 14)) - P.ell_mask((7 + s, 3, 16 + s, 12)); P.shade(ring, (5 + s, 1, 18 + s, 14), c)
    for y in range(3, 12, 2): P.hline(7 + s, 16 + s, y, (210, 210, 206))
    for x in range(7, 17, 2): P.vline(x + s, 3, 12, (190, 190, 186))
    P.rect(11, 14, 12, 22, BLACK[2]); P.rect(11, 20, 12, 23, c[1]); P.sphere((17, 15, 21, 19), LIME); P.selout()

@drawer("dumbbell", size=(24, 16), frames=4, ticks=[8, 2, 8, 2])
def dumbbell(P, v, f, nf):
    dy = [0, -1, -2, -1][f % 4] if v.get("lift") else 0; P.hcyl((8, 7 + dy, 15, 9 + dy), STEEL); P.box(2, 3 + dy, 7, 13 + dy, BLACK, top=1, side=1); P.box(16, 3 + dy, 21, 13 + dy, BLACK, top=1, side=1); P.box(0, 5 + dy, 2, 11 + dy, BLACK, top=1, side=0); P.box(21, 5 + dy, 23, 11 + dy, BLACK, top=1, side=1); P.selout()

@drawer("skateboard", size=(32, 16), frames=4, ticks=[8, 2, 8, 2])
def skateboard(P, v, f, nf):
    c = v.get("ramp", CRIMSON); P.hcyl((2, 4, 29, 9), c); P.poly([(2, 5), (0, 3), (2, 8)], c, box=(0, 3, 2, 8)); P.poly([(29, 5), (31, 3), (29, 8)], c, box=(29, 3, 31, 8)); P.rect(7, 9, 10, 10, STEEL[2]); P.rect(21, 9, 24, 10, STEEL[2])
    for x in (6, 11, 20, 25): P.sphere((x, 10, x + 3, 13), BLACK); P.put(x + 1, 11, GREY[3])
    P.selout()

@drawer("bicycle", size=(32, 24), frames=4, ticks=[4, 4, 4, 4])
def bicycle(P, v, f, nf):
    c = v.get("ramp", CRIMSON)
    for cx in (7, 24):
        ring = P.ell_mask((cx - 6, 10, cx + 6, 22)) - P.ell_mask((cx - 5, 11, cx + 5, 21)); P.shade(ring, (cx - 6, 10, cx + 6, 22), BLACK); P.put(cx, 16, STEEL[2])
        for i in range(4):
            a = i * math.pi / 4 + f * .3; P.line(cx, 16, int(cx + 5 * math.cos(a)), int(16 + 5 * math.sin(a)), GREY[2])
    P.line(7, 16, 13, 6, c[2]); P.line(13, 6, 20, 6, c[2]); P.line(20, 6, 24, 16, c[2]); P.line(13, 6, 17, 16, c[2]); P.line(17, 16, 7, 16, c[2]); P.line(17, 16, 24, 16, c[2]) if False else None
    P.rect(11, 4, 15, 5, BLACK[2]); P.rect(19, 3, 23, 4, STEEL[2]); P.sphere((16, 15, 18, 17), STEEL); P.selout()

@drawer("whistle", size=(16, 16), frames=4, ticks=[8, 2, 8, 2])
def whistle(P, v, f, nf):
    c = v.get("ramp", SILV); P.sphere((1, 6, 10, 15), c, rim=True); P.box(8, 7, 15, 10, c, top=1, side=1); P.rect(4, 7, 6, 8, BLACK[1]); P.selout()
    if f == 1: P.put(15, 5, SPARK); P.put(16 - 1, 12, SPARK)

@drawer("stopwatch", frames=4, ticks=[3, 3, 3, 3])
def stopwatch(P, v, f, nf):
    P.rect(10, 0, 13, 2, STEEL[2]); P.rect(11, 2, 12, 4, STEEL[1]); P.sphere((2, 4, 21, 23), SILV, rim=True); P.sphere((4, 6, 19, 21), PAPER, bands=(.05, .2, .6, .96))
    for i in range(12):
        a = i * math.pi / 6; P.put(int(11.5 + 6.5 * math.cos(a)), int(13.5 + 6.5 * math.sin(a)), INK if i % 3 == 0 else (150, 140, 130))
    a = -math.pi / 2 + f * math.pi / 2; P.line(11, 13, int(11.5 + 6 * math.cos(a)), int(13.5 + 6 * math.sin(a)), CRIMSON[2]); P.put(11, 13, INK); P.selout()

@drawer("trophy", frames=4, ticks=[8, 2, 8, 2])
def trophy(P, v, f, nf):
    c = v.get("ramp", GOLD); P.poly([(5, 2), (18, 2), (16, 12), (7, 12)], c, box=(5, 2, 18, 12), shape="vcyl"); P.hcyl((4, 1, 19, 3), c); P.rect(10, 12, 13, 16, c[2]); P.hcyl((6, 16, 17, 18), c); P.box(5, 18, 18, 22, WOOD, top=1, side=1)
    for x, y0 in ((3, 4), (19, 4)): P.rect(x, y0, x + 1, y0 + 5, c[1]); P.hline(x, x + 2, y0, c[2]); P.hline(x, x + 2, y0 + 5, c[2])
    P.selout(); P.put(7, 4, c[4])
    if f == 1: P.sparkle(16, 3, 1, SPARK)

@drawer("dice", size=(16, 16), frames=4, ticks=[8, 2, 2, 8])
def dice(P, v, f, nf):
    c = v.get("ramp", SNOW); P.box(2, 2, 13, 13, c, top=1, side=2); pips = [[(7, 7)], [(4, 4), (10, 10)], [(4, 4), (7, 7), (10, 10)], [(4, 4), (10, 4), (4, 10), (10, 10)], [(4, 4), (10, 4), (7, 7), (4, 10), (10, 10)], [(4, 4), (10, 4), (4, 7), (10, 7), (4, 10), (10, 10)]]
    for x, y in pips[(v.get("face", 5) - 1 + f) % 6]: P.put(x, y, INK)
    P.selout()

@drawer("cards", size=(24, 24), frames=4, ticks=[8, 2, 8, 2])
def cards(P, v, f, nf):
    back = v.get("ramp", CRIMSON)
    for i in range(3): x = 3 + i * 4; P.box(x, 4 + (2 - i), x + 11, 20, back if i < 2 else SNOW, top=1, side=1)
    P.rect(5, 7, 12, 17, back[1]); P.rect(9, 9, 16, 17, back[1]) if False else None
    P.sphere((15, 10, 18, 13), CRIMSON); P.sphere((17, 10, 20, 13), CRIMSON); P.poly([(15, 12), (20, 12), (17.5, 16)], CRIMSON, box=(15, 10, 20, 16)); P.selout()

@drawer("dartboard", frames=4, ticks=[8, 2, 8, 2])
def dartboard(P, v, f, nf):
    for i, (r, c) in enumerate([(10, BLACK), (8, SNOW), (6, CRIMSON), (4, SNOW), (2, GRASS)]): P.sphere((11 - r, 11 - r, 12 + r, 12 + r), c, bands=(.1, .3, .6, .9) if i == 0 else (.0, .05, .5, .95))
    P.sphere((11, 11, 12, 12), CRIMSON); P.line(12, 11, 20, 3, STEEL[2]); P.rect(19, 2, 21, 4, GOLD[3]); P.selout()

@drawer("chess", size=(16, 24))
def chess(P, v, f, nf):
    c = v.get("ramp", BLACK); kind = v.get("kind", "king")
    P.hcyl((3, 20, 12, 23), c); P.vcyl((5, 12, 10, 20), c)
    if kind == "king": P.hcyl((4, 10, 11, 13), c); P.rect(6, 4, 9, 10, c[2]); P.rect(7, 1, 8, 5, c[3]); P.rect(6, 2, 9, 2, c[3])
    elif kind == "knight": P.sphere((4, 4, 11, 12), c); P.poly([(9, 4), (13, 1), (12, 7)], c, box=(9, 1, 13, 7)); P.put(6, 6, SNOW[4])
    elif kind == "pawn": P.sphere((5, 4, 10, 10), c); P.hcyl((4, 10, 11, 12), c)
    else: P.box(4, 4, 11, 12, c, top=1, side=1); P.rect(4, 2, 5, 4, c[2]); P.rect(7, 2, 8, 4, c[2]); P.rect(10, 2, 11, 4, c[2])
    P.selout()

@drawer("token", size=(16, 16), frames=4, ticks=[4, 4, 4, 4])
def token(P, v, f, nf):
    c = v.get("ramp", COPPER); w = [12, 8, 4, 8][f % 4]; x0 = 8 - w // 2
    if w >= 8: P.sphere((x0, 2, x0 + w - 1, 13), c, rim=True); P.sphere((x0 + 2, 4, x0 + w - 3, 11), c, bands=(.3, .5, .75, .95)) if w == 12 else None; P.put(x0 + 3, 5, c[4])
    else: P.vcyl((x0, 2, x0 + w - 1, 13), c)
    P.selout()

@drawer("bowling", frames=4, ticks=[8, 2, 8, 2])
def bowling(P, v, f, nf):
    P.sphere((1, 10, 13, 22), BLACK, rim=True); P.put(5, 13, GREY[2]); P.put(7, 12, GREY[2]); P.put(6, 15, GREY[2])
    for x in (13, 18): P.vcyl((x, 2, x + 4, 10), SNOW); P.sphere((x, 0, x + 4, 4), SNOW); P.sphere((x - 1, 9, x + 5, 20), SNOW, rim=True); P.hline(x, x + 4, 7, CRIMSON[2])
    P.selout()

@drawer("golf", frames=4, ticks=[8, 2, 8, 2])
def golf(P, v, f, nf):
    s = _sw(f, nf); P.line(14 + s, 1, 8, 19, STEEL[2]); P.line(15 + s, 1, 9, 19, STEEL[1]); P.rect(13 + s, 0, 16 + s, 3, BLACK[2]); P.box(3, 18, 10, 22, STEEL, top=1, side=1); P.sphere((15, 17, 20, 22), SNOW, rim=True); P.rect(16, 22, 19, 23, GRASS[2]); P.selout()

@drawer("hockey", frames=4, ticks=[8, 2, 8, 2])
def hockey(P, v, f, nf):
    s = _sw(f, nf); P.line(16 + s, 1, 8, 18, WOOD[2]); P.line(17 + s, 1, 9, 18, WOOD[1]); P.rect(15 + s, 0, 18 + s, 2, BLACK[2]); P.poly([(7, 17), (10, 17), (3, 23), (0, 22)], WOOD, box=(0, 17, 10, 23), shape="hcyl"); P.hcyl((14, 19, 21, 23), BLACK); P.selout()

@drawer("boxing", frames=4, ticks=[8, 2, 8, 2])
def boxing(P, v, f, nf):
    c = v.get("ramp", CRIMSON); dx = [0, 2, 0, 0][f % 4]; P.sphere((3 + dx, 3, 18 + dx, 17), c, rim=True); P.sphere((12 + dx, 8, 21 + dx, 16), c); P.box(6 + dx, 15, 15 + dx, 22, c, top=0, side=1); P.hline(7 + dx, 14 + dx, 17, SNOW[2]); P.hline(7 + dx, 14 + dx, 22, c[1]); P.put(7 + dx, 6, c[4]); P.selout()

@drawer("frisbee", size=(24, 12), frames=4, ticks=[8, 2, 8, 2])
def frisbee(P, v, f, nf):
    c = v.get("ramp", TURQ); P.sphere((1, 2, 22, 10), c, rim=True); P.sphere((5, 3, 18, 7), c, bands=(.3, .5, .75, .95)); P.hline(2, 21, 10, c[0]); P.selout()

@drawer("yoyo", size=(16, 24), frames=4, ticks=[4, 4, 4, 4])
def yoyo(P, v, f, nf):
    c = v.get("ramp", CRIMSON); dy = [0, 3, 6, 3][f % 4]; P.vline(7, 0, 8 + dy, (210, 210, 206)); P.sphere((2, 8 + dy, 13, 19 + dy), c, rim=True); P.sphere((6, 12 + dy, 9, 15 + dy), SNOW); P.selout()

@drawer("puzzle", size=(16, 16))
def puzzle(P, v, f, nf):
    c = v.get("ramp", BLUE); P.box(2, 4, 11, 13, c, top=1, side=1); P.sphere((5, 1, 8, 4), c); P.sphere((11, 7, 14, 10), c); P.rect(5, 13, 8, 14, None); P.selout()

@drawer("cube", size=(16, 16), frames=4, ticks=[8, 2, 8, 2])
def cube(P, v, f, nf):
    cols = [CRIMSON, SNOW, BLUE, GRASS, YELLOW, PUMPKIN]; rr = _rng(f + 3)
    P.box(2, 2, 13, 13, BLACK, top=0, side=0)
    for i in range(3):
        for j in range(3): c = cols[(i * 3 + j + f) % 6]; P.rect(3 + i * 4, 3 + j * 4, 5 + i * 4, 5 + j * 4, c[2]); P.put(3 + i * 4, 3 + j * 4, c[3])
    P.selout()

@drawer("domino", size=(16, 24), frames=4, ticks=[8, 2, 8, 2])
def domino(P, v, f, nf):
    P.box(3, 1, 12, 22, SNOW, top=1, side=1); P.hline(4, 11, 11, INK)
    for x, y in [(5, 4), (10, 8), (5, 8), (10, 4), (5, 14), (10, 19), (7, 16)][: 3 + (f % 2) * 2]: P.put(x, y, INK)
    P.selout()

# ---------------------------------------------------------------- toys
@drawer("teddy", frames=4, ticks=[8, 2, 8, 2])
def teddy(P, v, f, nf):
    c = v.get("ramp", CARAMEL); dy = [0, 0, -1, 0][f % 4]; P.sphere((4, 11 + dy, 19, 23), c, rim=True); P.sphere((6, 2 + dy, 17, 13 + dy), c, rim=True); P.sphere((4, 1 + dy, 8, 5 + dy), c); P.sphere((15, 1 + dy, 19, 5 + dy), c)
    P.sphere((9, 7 + dy, 14, 11 + dy), CREAMW); P.put(11, 8 + dy, INK); P.put(9, 5 + dy, INK); P.put(14, 5 + dy, INK); P.sphere((7, 14 + dy, 16, 21), CREAMW, bands=(.3, .5, .75, .95)); P.sphere((1, 13, 5, 17), c); P.sphere((18, 13, 22, 17), c); P.put(11, 12 + dy, CRIMSON[2]) if v.get("bow") else None; P.selout()

@drawer("toy_car", size=(24, 16), frames=4, ticks=[8, 2, 8, 2])
def toy_car(P, v, f, nf):
    c = v.get("ramp", CRIMSON); P.box(2, 7, 21, 12, c, top=1, side=1); P.poly([(6, 7), (17, 7), (15, 2), (8, 2)], c, box=(6, 2, 17, 7), shape="hcyl"); P.rect(9, 3, 14, 6, ICE[2]); P.put(9, 3, ICE[4])
    for x in (4, 15): P.sphere((x, 10, x + 4, 14), BLACK); P.put(x + 2, 12, GREY[3])
    P.put(21, 9, YELLOW[3]); P.put(2, 9, CRIMSON[4]); P.selout()

@drawer("toy_train", size=(32, 20), frames=4, ticks=[4, 4, 4, 4])
def toy_train(P, v, f, nf):
    c = v.get("ramp", BLUE); P.box(10, 6, 29, 14, c, top=1, side=1); P.box(2, 2, 10, 14, c, top=1, side=1); P.rect(4, 4, 8, 7, ICE[2]); P.rect(14, 1, 17, 6, BLACK[2]); P.rect(13, 0, 18, 1, BLACK[3]); P.hcyl((10, 8, 29, 12), CRIMSON) if False else None
    for x in (4, 13, 23): P.sphere((x, 13, x + 4, 17), BLACK); P.put(x + 2, 15, GREY[3])
    P.put(12 + (f % 3), 0 - 0, (215, 215, 210)) if f % 3 else None; P.rect(29, 8, 31, 10, c[1]); P.selout()

@drawer("blocks", size=(24, 24))
def blocks(P, v, f, nf):
    for i, (x, y, c) in enumerate([(2, 12, CRIMSON), (12, 12, BLUE), (7, 2, YELLOW)]): P.box(x, y, x + 9, y + 9, c, top=1, side=2); P.rect(x + 3, y + 3, x + 5, y + 5, c[3])
    P.selout()

@drawer("rocking_horse", size=(24, 24), frames=4, ticks=[8, 2, 8, 2])
def rocking_horse(P, v, f, nf):
    c = v.get("ramp", WOOD); t = [0, 1, 0, -1][f % 4]
    P.sphere((5, 8 + t, 18, 16 - t), c, rim=True); P.sphere((15, 3 + t, 22, 10 + t), c); P.rect(17, 1 + t, 18, 3 + t, c[1]); P.put(19, 5 + t, INK); P.rect(14, 2 + t, 15, 6 + t, CRIMSON[2])
    P.rect(7, 15, 8, 20, c[2]); P.rect(15, 15, 16, 20, c[2]); arc = P.ell_mask((1, 12, 22, 26)) - P.ell_mask((2, 12, 21, 24)); arc = {(x, y) for x, y in arc if y >= 20}; P.shade(arc, (1, 12, 22, 26), c, shape="hcyl"); P.selout()

@drawer("bubbles", frames=4, ticks=[4, 4, 4, 4])
def bubbles(P, v, f, nf):
    P.rect(11, 12, 12, 23, PINK[2]); ring = P.ell_mask((8, 7, 15, 14)) - P.ell_mask((10, 9, 13, 12)); P.shade(ring, (8, 7, 15, 14), PINK)
    for i, (x, y, r) in enumerate([(5, 6, 2), (17, 3, 3), (14, 9, 1), (3, 1, 1)]):
        yy = (y - f * 2) % 14; ring = P.ell_mask((x - r, yy - r, x + r, yy + r)) - (P.ell_mask((x - r + 1, yy - r + 1, x + r - 1, yy + r - 1)) if r > 1 else set()); P.fill(ring, ICE[3]); P.put(x - r + 1, yy - r + 1, SNOW[4]) if r > 1 else None
    P.selout()

@drawer("water_gun", size=(24, 16), frames=4, ticks=[8, 2, 8, 2])
def water_gun(P, v, f, nf):
    c = v.get("ramp", TURQ); P.box(3, 4, 18, 9, c, top=1, side=1); P.rect(18, 5, 22, 7, PUMPKIN[2]); P.poly([(5, 9), (10, 9), (9, 15), (5, 15)], c, box=(5, 9, 10, 15), shape="vcyl"); P.rect(11, 9, 12, 11, c[1]); P.sphere((9, 1, 15, 5), ICE, bands=(.02, .1, .5, .95))
    if f == 1: P.put(23, 5, ICE[3]); P.put(23, 7, ICE[3])
    P.selout()

@drawer("jack_box", frames=4, ticks=[8, 2, 2, 8])
def jack_box(P, v, f, nf):
    c = v.get("ramp", CRIMSON); P.box(4, 12, 19, 22, c, top=1, side=2); P.rect(6, 15, 17, 19, GOLD[2]); P.rect(20, 15, 22, 16, STEEL[2]); P.rect(22, 13, 22, 16, STEEL[1])
    if f in (1, 2): P.box(4, 9, 19, 12, c, top=1, side=2); P.rect(10, 1, 13, 9, GREY[2]); P.sphere((8, 0, 15, 6), SNOW); P.put(10, 2, INK); P.put(13, 2, INK); P.hline(10, 13, 4, CRIMSON[2]); P.poly([(11, 0), (13, 0), (12, -2 + 2)], GOLD, box=(11, 0, 13, 2))
    else: P.box(4, 10, 19, 12, c, top=1, side=2)
    P.selout()

@drawer("top", frames=4, ticks=[2, 2, 2, 2])
def top(P, v, f, nf):
    c = v.get("ramp", CRIMSON); c2 = YELLOW; P.rect(11, 0, 12, 4, WOOD[1]); P.poly([(4, 6), (19, 6), (12, 20)], c, box=(4, 6, 19, 20), shape="vcyl"); P.hcyl((4, 4, 19, 8), c)
    for y in range(8, 18, 3): w = (20 - y) * 7 // 14; P.hline(12 - w + (f % 2), 12 + w - 1, y, c2[3])
    P.put(12, 21, STEEL[2]); P.selout()

@drawer("marbles", size=(24, 16))
def marbles(P, v, f, nf):
    for (x, y, c) in [(3, 6, BLUE), (10, 4, CRIMSON), (16, 7, GRASS), (7, 10, GOLD), (14, 11, PURPLE)]: P.sphere((x, y, x + 5, y + 5), c, rim=True); P.put(x + 1, y + 1, SNOW[4])
    P.selout()

@drawer("paper_plane", size=(24, 16), frames=4, ticks=[8, 2, 8, 2])
def paper_plane(P, v, f, nf):
    dy = _bob(f, nf); P.poly([(1, 8 + dy), (22, 2 + dy), (12, 14 + dy), (10, 9 + dy)], PAPER, box=(1, 2, 22, 14), bands=(.1, .3, .6, .9)); P.poly([(1, 8 + dy), (22, 2 + dy), (10, 9 + dy)], PAPER, box=(1, 2, 22, 14), bands=(.0, .05, .3, .9)); P.line(1, 8 + dy, 22, 2 + dy, PAPER[1]); P.selout()

@drawer("sand_pail", frames=4, ticks=[8, 2, 8, 2])
def sand_pail(P, v, f, nf):
    c = v.get("ramp", CRIMSON); P.poly([(4, 8), (19, 8), (17, 22), (6, 22)], c, box=(4, 8, 19, 22), shape="vcyl"); P.hcyl((4, 6, 19, 9), c); P.hcyl((5, 7, 18, 8), WHEAT)
    ring = P.ell_mask((5, 0, 18, 10)) - P.ell_mask((7, 2, 16, 10)) - set((x, y) for x in range(24) for y in range(7, 24)); P.shade(ring, (5, 0, 18, 10), YELLOW); P.line(20, 12, 23, 22, YELLOW[2]); P.poly([(19, 20), (23, 20), (23, 23), (19, 23)], YELLOW, flat=True); P.selout()

@drawer("crayons", size=(24, 24), frames=4, ticks=[8, 2, 8, 2])
def crayons(P, v, f, nf):
    P.box(3, 10, 20, 22, R((220, 190, 60)), top=1, side=1); P.rect(3, 13, 20, 14, GRASS[2])
    for i, c in enumerate([CRIMSON, BLUE, GRASS, YELLOW, PURPLE]):
        x = 5 + i * 3; P.vcyl((x, 4 + (i % 2), x + 1, 11), c); P.poly([(x, 4 + (i % 2)), (x + 1, 4 + (i % 2)), (x, 2 + (i % 2))], c, box=(x, 2, x + 1, 4))
    P.selout()

@drawer("palette", frames=4, ticks=[8, 2, 8, 2])
def palette(P, v, f, nf):
    P.sphere((1, 4, 22, 21), WOOD, rim=True); P.sphere((13, 12, 17, 16), (20, 14, 18, 0) and BLACK, bands=(.9, .95, .97, .99)); P.rect(13, 12, 17, 16, None)
    for (x, y, c) in [(4, 7, CRIMSON), (9, 5, YELLOW), (15, 6, BLUE), (5, 13, GRASS), (9, 16, PURPLE)]: P.sphere((x, y, x + 3, y + 3), c); P.put(x, y, c[4])
    P.line(19, 2, 23, 10, WOOD[1]); P.rect(22, 9, 23, 12, BLUE[2]); P.selout()

@drawer("brick_toy", size=(16, 12))
def brick_toy(P, v, f, nf):
    c = v.get("ramp", CRIMSON); P.box(1, 4, 14, 11, c, top=1, side=1)
    for x in (2, 6, 10): P.hcyl((x, 1, x + 3, 4), c)
    P.selout()

@drawer("kazoo", size=(24, 12), frames=4, ticks=[8, 2, 8, 2])
def kazoo(P, v, f, nf):
    c = v.get("ramp", YELLOW); P.poly([(1, 4), (18, 3), (22, 5), (22, 8), (18, 10), (1, 8)], c, box=(1, 3, 22, 10), shape="hcyl"); P.rect(8, 1, 11, 3, c[1]); P.put(9, 0, c[3]); P.selout()
    if f == 1: P.put(23, 4, SPARK); P.put(23, 8, SPARK)

@drawer("slinky", size=(24, 16), frames=4, ticks=[3, 3, 3, 3])
def slinky(P, v, f, nf):
    c = v.get("ramp", SILV); k = f % 4
    for i in range(8):
        x0 = 2 + i * (2 + (k if i > 3 else 0)); 
        if x0 > 20: break
        ring = P.ell_mask((x0, 2, x0 + 3, 13)) - P.ell_mask((x0 + 1, 3, x0 + 2, 12)); P.fill(ring, c[3] if i % 2 else c[2])
    P.selout()

# ---------------------------------------------------------------- street (NYC)
@drawer("traffic_light", size=(16, 32), frames=4, ticks=[8, 2, 2, 8])
def traffic_light(P, v, f, nf):
    P.box(3, 1, 12, 24, BLACK, top=1, side=1); P.rect(7, 24, 8, 31, STEEL[1])
    on = [0, 1, 2, 2][f % 4]
    for i, c in enumerate([CRIMSON, YELLOW, GRASS]): P.sphere((5, 3 + i * 7, 10, 8 + i * 7), c if i == on else R(tuple(int(x * .35) for x in c[2])), bands=(.3, .5, .7, .95))
    P.rect(2, 2 + on * 7, 2, 4 + on * 7, BLACK[1]); P.selout()

@drawer("street_lamp", size=(16, 32), frames=4, ticks=[8, 2, 8, 2])
def street_lamp(P, v, f, nf):
    on = f != 2; P.rect(7, 6, 8, 29, BLACK[2]); P.vline(7, 6, 29, BLACK[3]); P.hcyl((4, 29, 11, 31), BLACK); P.poly([(4, 2), (11, 2), (12, 7), (3, 7)], BLACK, box=(3, 2, 12, 7), shape="vcyl"); P.rect(7, 0, 8, 2, BLACK[2])
    P.rect(5, 4, 10, 6, FLAME[4] if on else GREY[1]); P.selout()
    if on: P.put(2, 5, SPARK); P.put(13, 5, SPARK)

@drawer("hydrant", size=(16, 24), frames=4, ticks=[8, 2, 8, 2])
def hydrant(P, v, f, nf):
    c = v.get("ramp", CRIMSON); P.vcyl((5, 6, 10, 22), c); P.hcyl((4, 21, 11, 23), c); P.hcyl((4, 5, 11, 8), c); P.sphere((5, 1, 10, 6), c); P.hcyl((1, 10, 5, 13), c); P.hcyl((10, 10, 14, 13), c); P.sphere((11, 13, 14, 16), SILV); P.selout(); P.put(6, 3, c[4])
    if v.get("spray") and f % 2: P.put(0, 11, ICE[3]); P.put(15, 12, ICE[3])

@drawer("mailbox", size=(16, 32))
def mailbox(P, v, f, nf):
    c = v.get("ramp", BLUE); P.box(2, 8, 13, 20, c, top=0, side=1); P.sphere((2, 3, 13, 12), c, rim=True); P.rect(2, 8, 13, 10, c[2]); P.rect(4, 11, 11, 13, c[1]); P.put(5, 12, c[0]); P.rect(3, 20, 12, 23, c[1]); P.rect(5, 23, 10, 31, c[2]); P.vline(5, 23, 31, c[3]); P.selout()

@drawer("bench", size=(32, 20))
def bench(P, v, f, nf):
    c = v.get("ramp", WOOD); P.hcyl((2, 2, 29, 4), c); P.hcyl((2, 6, 29, 8), c); P.hcyl((1, 11, 30, 14), c)
    for x in (4, 26): P.rect(x, 8, x + 1, 19, STEEL[1]); P.rect(x - 2, 19, x + 3, 19, STEEL[2]); P.rect(x, 4, x + 1, 6, STEEL[1])
    P.selout()

@drawer("pigeon", size=(16, 16), frames=4, ticks=[8, 2, 8, 2])
def pigeon(P, v, f, nf):
    dy = [0, 1, 0, 0][f % 4]; P.sphere((2, 6, 12, 14), GREY, rim=True); P.sphere((8, 2 + dy, 14, 8 + dy), GREY); P.put(13, 5 + dy, PUMPKIN[2]); P.put(14, 5 + dy, PUMPKIN[3]); P.put(11, 4 + dy, INK)
    P.sphere((9, 7 + dy, 12, 10 + dy), R((100, 150, 120))); P.poly([(2, 9), (0, 7), (3, 11)], GREY, box=(0, 7, 3, 11)); P.put(5, 14, CRIMSON[1]); P.put(8, 14, CRIMSON[1]); P.selout()

@drawer("rat", size=(24, 16), frames=4, ticks=[8, 2, 8, 2])
def rat(P, v, f, nf):
    c = GREY; s = _sw(f, nf); P.sphere((4, 5, 17, 14), c, rim=True); P.sphere((14, 6, 21, 12), c); P.sphere((15, 3, 18, 6), c); P.rect(16, 4, 17, 5, PINK[3]); P.put(19, 8, INK); P.put(22, 9, PINK[2])
    for x in range(0, 5): P.put(x, 9 + int(round(math.sin((x + s) / 1.5))), PINK[2])
    P.put(7, 14, PINK[1]); P.put(12, 14, PINK[1])
    if v.get("pizza"): P.poly([(10, 0), (16, 0), (13, 7)], CHEESE, box=(10, 0, 16, 7)); P.hline(10, 16, 0, DOUGH[3]); P.put(13, 2, TOMATO[2])
    P.selout()

@drawer("subway_sign", size=(16, 24))
def subway_sign(P, v, f, nf):
    c = v.get("ramp", GRASS); P.rect(7, 12, 8, 23, STEEL[1]); P.sphere((1, 1, 14, 14), c, rim=True); P.sphere((4, 4, 11, 11), c, bands=(.3, .5, .75, .95)); P.selout()

@drawer("taxi", size=(32, 16), frames=4, ticks=[8, 2, 8, 2])
def taxi(P, v, f, nf):
    c = TAXI; P.box(2, 7, 29, 12, c, top=1, side=1); P.poly([(8, 7), (23, 7), (21, 2), (10, 2)], c, box=(8, 2, 23, 7), shape="hcyl"); P.rect(11, 3, 14, 6, ICE[2]); P.rect(17, 3, 20, 6, ICE[2]); P.rect(14, 0, 17, 2, BLACK[2]); P.rect(15, 1, 16, 1, c[3])
    for x in range(3, 29, 2): P.put(x, 9 + (x // 2) % 2, BLACK[2])
    for x in (5, 21): P.sphere((x, 10, x + 5, 15), BLACK); P.put(x + 2, 12, GREY[3])
    P.put(29, 8, YELLOW[4] if f % 2 else YELLOW[2]); P.put(2, 8, CRIMSON[3]); P.selout()

@drawer("hotdog_cart", size=(32, 24), frames=4, ticks=[6, 6, 6, 6])
def hotdog_cart(P, v, f, nf):
    P.box(4, 8, 27, 18, STEEL, top=1, side=2); P.rect(5, 9, 26, 10, STEEL[3]); P.rect(8, 11, 14, 16, BLACK[2]); P.rect(17, 11, 23, 16, BLACK[2])
    for x in range(6, 26):
        P.rect(x, 1, x, 4, YELLOW[2] if (x // 4) % 2 else BLUE[2])
    P.rect(5, 4, 26, 5, STEEL[1]); P.rect(5, 5, 5, 8, STEEL[2]); P.rect(26, 5, 26, 8, STEEL[2]); P.hcyl((9, 10, 13, 11), R((190, 70, 50)))
    P.sphere((6, 17, 11, 22), BLACK); P.sphere((20, 17, 25, 22), BLACK); P.rect(27, 12, 31, 13, STEEL[2])
    P.put(10 + (f % 2), 6 - (f % 3), (215, 215, 210)); P.selout()

@drawer("news_box", size=(16, 24))
def news_box(P, v, f, nf):
    c = v.get("ramp", BLUE); P.box(2, 4, 13, 22, c, top=1, side=1); P.rect(3, 6, 12, 12, SCREEN[2]); P.rect(4, 7, 11, 10, PAPER[2]); P.hline(5, 10, 8, (170, 160, 140)); P.rect(3, 14, 12, 15, c[1]); P.rect(6, 14, 9, 15, STEEL[3]); P.rect(2, 2, 13, 4, c[3]); P.selout()

@drawer("manhole", size=(24, 12))
def manhole(P, v, f, nf):
    P.sphere((1, 1, 22, 11), STEEL, rim=True)
    for y in range(3, 10, 2): P.hline(4 + (y % 4 == 3), 19, y, STEEL[1])
    P.selout()

@drawer("water_tower", size=(24, 32), frames=4, ticks=[8, 2, 8, 2])
def water_tower(P, v, f, nf):
    c = WOOD; P.poly([(12, 1), (3, 9), (20, 9)], R((90, 80, 90)), box=(3, 1, 20, 9), shape="vcyl"); P.vcyl((4, 9, 19, 22), c)
    for y in (12, 18): P.hline(4, 19, y, STEEL[1])
    P.hcyl((3, 21, 20, 24), c); P.line(6, 24, 4, 31, STEEL[2]); P.line(17, 24, 19, 31, STEEL[2]); P.line(4, 27, 19, 27, STEEL[1]); P.rect(11, 24, 12, 31, STEEL[2]); P.selout()
    if f == 1: P.put(12, 0, SPARK)

@drawer("parking_meter", size=(16, 32), frames=4, ticks=[8, 2, 8, 2])
def parking_meter(P, v, f, nf):
    P.rect(7, 14, 8, 31, STEEL[1]); P.box(3, 2, 12, 14, STEEL, top=1, side=1); P.sphere((3, 0, 12, 6), STEEL); P.rect(5, 5, 10, 9, SCREEN[2]); P.rect(6, 6, 9, 7, CRIMSON[3] if f % 2 else LIMEG[3]); P.rect(6, 11, 9, 12, BLACK[1]); P.selout()

@drawer("fire_escape", size=(24, 32))
def fire_escape(P, v, f, nf):
    c = BLACK
    for y in (6, 20): P.hline(2, 21, y, c[2]); P.hline(2, 21, y + 4, c[2])
    for x in range(3, 22, 3): P.vline(x, 2, 10, c[1]); P.vline(x, 16, 24, c[1])
    P.hline(2, 21, 10, c[3]); P.hline(2, 21, 24, c[3]); P.line(18, 10, 10, 24, c[2]); P.line(19, 10, 11, 24, c[2]); P.vline(2, 2, 31, c[2]); P.vline(21, 2, 31, c[2]); P.selout()

@drawer("payphone", size=(16, 24))
def payphone(P, v, f, nf):
    c = v.get("ramp", STEEL); P.box(3, 1, 12, 20, c, top=1, side=1); P.rect(4, 3, 11, 6, SCREEN[2]); P.rect(5, 9, 10, 14, BLACK[2]); P.rect(1, 2, 2, 16, BLACK[2]); P.rect(0, 1, 2, 3, BLACK[2]); P.rect(0, 15, 2, 17, BLACK[2]); P.rect(5, 16, 10, 17, GOLD[2]); P.selout()

@drawer("dumpster", size=(32, 24))
def dumpster(P, v, f, nf):
    c = v.get("ramp", GRASS); P.box(2, 8, 29, 20, c, top=0, side=2); P.box(1, 4, 30, 8, c, top=1, side=2); P.rect(12, 5, 19, 6, c[3]); P.rect(4, 10, 27, 12, c[1])
    P.sphere((5, 19, 9, 23), BLACK); P.sphere((22, 19, 26, 23), BLACK); P.selout()

@drawer("stoop", size=(32, 24))
def stoop(P, v, f, nf):
    c = R((140, 100, 80)); 
    for i in range(4): P.box(4 + i * 0, 4 + i * 5, 27, 8 + i * 5, c, top=1, side=1); P.rect(4, 4 + i * 5, 27, 4 + i * 5, c[3])
    P.rect(2, 2, 3, 23, BLACK[2]); P.rect(28, 2, 29, 23, BLACK[2]); P.rect(1, 2, 4, 2, BLACK[3]); P.rect(27, 2, 30, 2, BLACK[3]); P.selout()

@drawer("bollard", size=(8, 24))
def bollard(P, v, f, nf):
    c = v.get("ramp", BLACK); P.vcyl((2, 3, 5, 22), c); P.sphere((2, 1, 5, 4), c); P.hcyl((1, 21, 6, 23), c); P.hline(2, 5, 8, YELLOW[3]); P.selout()

@drawer("crosswalk_sign", size=(16, 24), frames=4, ticks=[8, 2, 8, 2])
def crosswalk_sign(P, v, f, nf):
    P.rect(7, 14, 8, 23, STEEL[1]); P.box(1, 1, 14, 14, BLACK, top=1, side=1)
    if f % 2: P.rect(6, 3, 9, 5, SNOW[3]); P.rect(5, 6, 10, 10, SNOW[3]); P.rect(5, 10, 6, 12, SNOW[3]); P.rect(9, 10, 10, 12, SNOW[3])
    else: P.rect(5, 4, 10, 11, PUMPKIN[2]); P.rect(6, 5, 9, 10, BLACK[1])
    P.selout()

@drawer("scaffold", size=(24, 32))
def scaffold(P, v, f, nf):
    c = STEEL
    for x in (2, 21): P.rect(x, 1, x + 1, 31, c[2]); P.vline(x, 1, 31, c[3])
    for y in (6, 18, 30): P.hline(2, 22, y, c[2]); P.hline(2, 22, y - 1, WOOD[2]) if y != 30 else None
    P.line(3, 7, 21, 17, c[1]); P.line(21, 19, 3, 29, c[1]); P.selout()

@drawer("bike_rack", size=(24, 16))
def bike_rack(P, v, f, nf):
    c = STEEL; arc = P.ell_mask((3, 2, 20, 18)) - P.ell_mask((6, 5, 17, 18)); arc = {(x, y) for x, y in arc if y < 13}; P.shade(arc, (3, 2, 20, 18), c); P.rect(3, 12, 5, 15, c[1]); P.rect(18, 12, 20, 15, c[1]); P.selout()

# ---------------------------------------------------------------- fantasy (the game studio)
@drawer("sword", frames=4, ticks=[8, 2, 8, 2])
def sword(P, v, f, nf):
    s = _sw(f, nf); P.line(12 + s, 1, 12 + s, 15, STEEL[3]); P.line(13 + s, 1, 13 + s, 15, STEEL[2]); P.put(12 + s, 0, STEEL[4]); P.rect(8 + s, 15, 17 + s, 16, GOLD[2]); P.rect(12, 17, 13, 21, LEATHER[2]); P.sphere((11, 21, 14, 23), GOLD); P.selout()
    if f == 1: P.sparkle(12 + s, 3, 1, SPARK)

@drawer("shield", frames=4, ticks=[8, 2, 8, 2])
def shield(P, v, f, nf):
    c = v.get("ramp", BLUE); emb = v.get("emblem", GOLD); P.poly([(3, 2), (20, 2), (20, 12), (12, 22), (4, 12)], c, box=(3, 2, 20, 22), bands=(.1, .3, .6, .9)); P.hline(4, 19, 2, c[3]); P.poly([(11.5, 6), (16, 11), (11.5, 16), (7, 11)], emb, box=(7, 6, 16, 16), bands=(.2, .4, .7, .9)); P.put(10, 9, emb[4]); P.selout()
    if f == 1: P.put(5, 4, SPARK)

@drawer("potion", frames=4, ticks=[4, 4, 4, 4])
def potion(P, v, f, nf):
    liq = v.get("ramp", PURPLE); P.sphere((4, 8, 19, 22), ICE, bands=(.02, .1, .5, .95)); P.rect(9, 3, 14, 9, ICE[2]); P.hcyl((8, 1, 15, 4), WOOD); P.sphere((5, 12, 18, 21), liq); P.rect(5, 15, 18, 21, liq[2]); P.hline(5, 18, 21, liq[1])
    for i in range(3): P.put(8 + i * 3, 20 - ((f * 2 + i * 3) % 7), liq[4])
    P.selout(); P.put(6, 10, SNOW[4])

@drawer("chest", frames=4, ticks=[8, 2, 2, 8])
def chest(P, v, f, nf):
    c = v.get("ramp", WOOD); open_ = f in (1, 2); P.box(2, 11, 21, 21, c, top=0, side=2); P.rect(2, 11, 21, 12, GOLD[2]); P.rect(10, 11, 13, 14, GOLD[3]); P.rect(5, 12, 5, 21, GOLD[1]); P.rect(18, 12, 18, 21, GOLD[1])
    if open_: P.box(2, 2, 21, 7, c, top=1, side=2); P.rect(3, 7, 20, 10, GOLD[3]); P.sparkle(8, 9, 1, SPARK); P.sparkle(15, 8, 0, SPARK)
    else: P.hcyl((2, 5, 21, 12), c); P.rect(5, 6, 5, 11, GOLD[1]); P.rect(18, 6, 18, 11, GOLD[1])
    P.selout()

@drawer("wand", frames=4, ticks=[4, 4, 4, 4])
def wand(P, v, f, nf):
    P.line(5, 22, 15, 6, BLACK[2]); P.line(6, 22, 16, 6, BLACK[1]); P.rect(14, 3, 17, 7, SNOW[3]); st = [0, 1, 2, 1][f % 4]; P.sparkle(18, 4, st, GOLD[4]); P.sparkle(12, 1, [1, 0, 1, 2][f % 4], SPARK); P.selout()

@drawer("crystal", frames=4, ticks=[8, 2, 8, 2])
def crystal(P, v, f, nf):
    c = v.get("ramp", PURPLE); P.poly([(12, 1), (18, 8), (16, 22), (8, 22), (6, 8)], c, box=(6, 1, 18, 22), shape="vcyl"); P.poly([(12, 1), (14, 8), (13, 22), (11, 22), (10, 8)], c, box=(6, 1, 18, 22), bands=(.6, .75, .9, .97)); P.vline(9, 6, 20, c[4]); P.hcyl((5, 21, 19, 23), BLACK); P.selout()
    if f == 1: P.sparkle(16, 5, 1, SPARK)

@drawer("key", size=(24, 16), frames=4, ticks=[8, 2, 8, 2])
def key(P, v, f, nf):
    c = v.get("ramp", GOLD); ring = P.ell_mask((1, 3, 10, 12)) - P.ell_mask((4, 6, 7, 9)); P.shade(ring, (1, 3, 10, 12), c); P.rect(10, 7, 22, 8, c[2]); P.hline(10, 22, 7, c[3]); P.rect(18, 9, 19, 11, c[2]); P.rect(21, 9, 22, 11, c[2]); P.selout()
    if f == 1: P.put(3, 2, SPARK)

@drawer("lock", frames=4, ticks=[8, 2, 8, 2])
def lock(P, v, f, nf):
    c = v.get("ramp", GOLD); P.box(4, 10, 19, 22, c, top=1, side=2); arc = P.ell_mask((6, 1, 17, 13)) - P.ell_mask((9, 4, 14, 13)) - set((x, y) for x in range(24) for y in range(10, 24)); P.shade(arc, (6, 1, 17, 13), STEEL); P.sphere((10, 13, 13, 16), BLACK); P.rect(11, 16, 12, 18, BLACK[2]); P.selout()

@drawer("map", size=(24, 20))
def map_(P, v, f, nf):
    P.box(2, 2, 21, 17, PARCH, top=1, side=1); P.rect(2, 2, 3, 17, PARCH[1]); P.rect(20, 2, 21, 17, PARCH[1])
    for (x, y) in [(5, 5), (8, 7), (12, 6), (15, 10), (17, 13)]: P.put(x, y, (170, 150, 110))
    P.line(5, 5, 8, 7, (170, 150, 110)); P.line(8, 7, 12, 6, (170, 150, 110)); P.line(12, 6, 15, 10, (170, 150, 110)); P.line(15, 10, 17, 13, (170, 150, 110)); P.put(17, 13, CRIMSON[2]); P.put(18, 12, CRIMSON[2]); P.put(16, 12, CRIMSON[2]); P.put(18, 14, CRIMSON[2]); P.put(16, 14, CRIMSON[2])
    P.sphere((5, 11, 9, 15), SUMMER_BLUE); P.selout()

@drawer("compass", frames=4, ticks=[4, 4, 4, 4])
def compass(P, v, f, nf):
    P.sphere((2, 2, 21, 21), GOLD, rim=True); P.sphere((4, 4, 19, 19), PAPER, bands=(.05, .2, .6, .96))
    for i in range(4): a = i * math.pi / 2; P.put(int(11.5 + 6 * math.cos(a)), int(11.5 + 6 * math.sin(a)), INK)
    a = -math.pi / 2 + [0, .2, 0, -.2][f % 4]; P.line(11, 11, int(11.5 + 6 * math.cos(a)), int(11.5 + 6 * math.sin(a)), CRIMSON[2]); P.line(11, 11, int(11.5 - 5 * math.cos(a)), int(11.5 - 5 * math.sin(a)), GREY[2]); P.put(11, 11, GOLD[3]); P.selout()

@drawer("bomb", frames=4, ticks=[3, 3, 3, 3])
def bomb(P, v, f, nf):
    P.sphere((3, 7, 18, 22), BLACK, rim=True); P.rect(9, 4, 12, 7, GREY[1]); P.line(12, 4, 17, 1, WOOD[1]); k = f % 4; P.sparkle(17, 1, [1, 2, 1, 0][k], GOLD[4]); P.put(16, 0, SPARK) if k % 2 else None; P.put(6, 10, GREY[3]); P.put(7, 9, GREY[3]); P.selout()

@drawer("heart_box", size=(16, 16), frames=4, ticks=[8, 2, 2, 8])
def heart_box(P, v, f, nf):
    full = f in (0, 3); c = CRIMSON if full else GREY
    P.sphere((1, 2, 8, 9), c); P.sphere((7, 2, 14, 9), c); P.poly([(1, 7), (14, 7), (7.5, 14)], c, box=(1, 2, 14, 14)); P.sphere((2, 3, 13, 13), c); P.selout()
    if full: P.put(4, 5, c[4]); P.put(5, 4, c[4])

@drawer("gem", size=(16, 16), frames=4, ticks=[8, 2, 8, 2])
def gem(P, v, f, nf):
    c = v.get("ramp", TURQ); P.poly([(3, 5), (12, 5), (14, 8), (7.5, 14), (1, 8)], c, box=(1, 5, 14, 14), bands=(.1, .3, .6, .9)); P.poly([(5, 5), (10, 5), (12, 8), (3, 8)], c, box=(1, 5, 14, 14), bands=(.3, .5, .75, .95)); P.put(5, 6, c[4]); P.selout()
    if f == 1: P.sparkle(12, 4, 1, SPARK)

@drawer("mushroom", size=(16, 16), frames=4, ticks=[8, 2, 8, 2])
def mushroom(P, v, f, nf):
    c = v.get("ramp", CRIMSON); dy = [0, -1, 0, 0][f % 4]; P.sphere((1, 1 + dy, 14, 10 + dy), c, rim=True); P.rect(1, 6 + dy, 14, 9 + dy, c[2]); P.hline(2, 13, 9 + dy, c[1]); P.vcyl((5, 9 + dy, 10, 15), CREAMW)
    for x, y in [(4, 4), (9, 3), (11, 7), (6, 7)]: P.put(x, y + dy, SNOW[4])
    P.selout()

@drawer("spellbook", frames=4, ticks=[8, 2, 8, 2])
def spellbook(P, v, f, nf):
    c = v.get("ramp", PURPLE); P.box(4, 3, 19, 21, c, top=1, side=2); P.rect(18, 4, 19, 20, PAPER[2]); P.rect(5, 20, 19, 21, PAPER[1]); P.sparkle(11, 11, 2 if f == 1 else 1, GOLD[4]); P.rect(4, 3, 19, 4, GOLD[1]); P.rect(4, 20, 19, 20, GOLD[1]) if False else None; P.selout()

@drawer("ring", size=(16, 16), frames=4, ticks=[8, 2, 8, 2])
def ring(P, v, f, nf):
    ring_ = P.ell_mask((2, 4, 13, 15)) - P.ell_mask((5, 7, 10, 12)); P.shade(ring_, (2, 4, 13, 15), GOLD); P.poly([(5, 4), (10, 4), (7.5, 1)], GOLD, box=(5, 1, 10, 4)); P.rect(6, 1, 9, 3, CRIMSON[2]); P.put(6, 1, CRIMSON[4]); P.selout()
    if f == 1: P.sparkle(10, 1, 1, SPARK)

@drawer("bow_arrow", frames=4, ticks=[8, 2, 8, 2])
def bow_arrow(P, v, f, nf):
    pull = 2 if f in (1, 3) else 0; arc = P.ell_mask((8, 1, 22, 22)) - P.ell_mask((9, 2, 21, 21)); arc = {(x, y) for x, y in arc if x > 15}; P.fill(arc, WOOD[2]); P.line(16, 2, 9 - pull, 11, (210, 210, 206)); P.line(16, 21, 9 - pull, 12, (210, 210, 206))
    P.hline(3 - pull, 18 - pull, 11, WOOD[1]); P.put(19 - pull, 11, STEEL[3]); P.put(20 - pull, 11, STEEL[3]); P.rect(3 - pull, 10, 4 - pull, 12, CRIMSON[2]); P.selout()

@drawer("helmet", frames=4, ticks=[8, 2, 8, 2])
def helmet(P, v, f, nf):
    c = v.get("ramp", STEEL); P.sphere((4, 3, 19, 17), c, rim=True); P.rect(4, 11, 19, 19, c[2]); P.hline(4, 19, 19, c[1]); P.rect(6, 12, 17, 14, BLACK[1]); P.vline(11, 11, 19, c[3]); P.rect(10, 0, 13, 4, CRIMSON[2]); P.selout()

@drawer("cauldron", frames=4, ticks=[4, 4, 4, 4])
def cauldron(P, v, f, nf):
    P.sphere((2, 6, 21, 22), BLACK, rim=True); P.hcyl((2, 5, 21, 9), BLACK); P.hcyl((3, 6, 20, 8), GRASS); P.rect(5, 22, 7, 23, BLACK[1]); P.rect(16, 22, 18, 23, BLACK[1]); P.rect(1, 9, 2, 12, BLACK[2]); P.rect(21, 9, 22, 12, BLACK[2])
    for i in range(3): P.put(7 + i * 4 + (f % 2), 4 - ((f + i * 2) % 4), GRASS[3])
    P.selout()

@drawer("dragon_egg", frames=4, ticks=[8, 2, 8, 2])
def dragon_egg(P, v, f, nf):
    c = v.get("ramp", PURPLE); P.sphere((5, 1, 18, 20), c, rim=True)
    for y in range(3, 19, 3):
        for x in range(6, 18, 3): P.put(x + (y // 3) % 2, y, c[3]) if P.get(x + (y // 3) % 2, y)[3] else None
    P.hcyl((4, 19, 19, 23), WHEAT); P.selout()
    if f == 1: P.sparkle(16, 3, 1, SPARK)

@drawer("staff", size=(16, 32), frames=4, ticks=[8, 2, 8, 2])
def staff(P, v, f, nf):
    P.rect(7, 8, 8, 31, WOOD[2]); P.vline(7, 8, 31, WOOD[3]); P.poly([(5, 8), (10, 8), (12, 4), (8, 0), (3, 4)], WOOD, box=(3, 0, 12, 8), bands=(.1, .3, .6, .9)); P.sphere((5, 2, 10, 7), TURQ); P.put(6, 3, SNOW[4]); P.selout()
    if f == 1: P.sparkle(12, 1, 1, SPARK)

@drawer("rune", size=(16, 16))
def rune(P, v, f, nf):
    P.sphere((2, 1, 13, 14), GREY, rim=True); P.vline(7, 4, 11, TURQ[3]); P.line(7, 4, 10, 7, TURQ[3]); P.line(7, 8, 10, 11, TURQ[3]); P.selout()

@drawer("slingshot", frames=4, ticks=[8, 2, 8, 2])
def slingshot(P, v, f, nf):
    P.rect(11, 12, 12, 23, WOOD[2]); P.line(11, 12, 5, 4, WOOD[2]); P.line(12, 12, 18, 4, WOOD[2]); pull = 3 if f in (1, 3) else 0; P.line(5, 4, 12, 8 + pull, (190, 190, 186)); P.line(18, 4, 12, 8 + pull, (190, 190, 186)); P.sphere((10, 7 + pull, 13, 10 + pull), GREY); P.selout()

@drawer("treasure_bag", frames=4, ticks=[8, 2, 8, 2])
def treasure_bag(P, v, f, nf):
    c = v.get("ramp", WHEAT); P.sphere((3, 8, 20, 23), c, rim=True); P.poly([(8, 2), (15, 2), (17, 9), (6, 9)], c, box=(6, 2, 17, 9), shape="vcyl"); P.hcyl((7, 7, 16, 9), LEATHER); P.sphere((9, 0, 12, 3), GOLD); P.sphere((12, 0, 14, 2), GOLD)
    for x, y in [(9, 13), (13, 12), (11, 17)]: P.put(x, y, GOLD[3])
    P.selout()

# ---------------------------------------------------------------- music and party
@drawer("guitar", size=(24, 32), frames=4, ticks=[8, 2, 8, 2])
def guitar(P, v, f, nf):
    c = v.get("ramp", R((200, 90, 50))); P.sphere((3, 16, 20, 31), c, rim=True); P.sphere((5, 10, 18, 22), c, rim=True); P.rect(5, 16, 18, 22, c[2]); P.sphere((9, 19, 14, 24), BLACK); P.rect(10, 0, 13, 16, WOOD[2]); P.rect(9, 0, 14, 3, BLACK[2])
    for x in range(10, 14): P.vline(x, 3, 25, (210, 210, 206)) if x % 2 == 0 else None
    P.rect(8, 26, 15, 27, BLACK[2]); P.selout()
    if f == 1: P.put(21, 18, SPARK)

@drawer("synth", size=(32, 16), frames=4, ticks=[4, 4, 4, 4])
def synth(P, v, f, nf):
    P.box(1, 3, 30, 13, BLACK, top=1, side=1); P.rect(2, 7, 29, 12, SNOW[3])
    for x in range(2, 30, 3): P.vline(x, 7, 12, GREY[1])
    for x in range(4, 28, 3): P.rect(x, 7, x + 1, 10, BLACK[2]) if (x // 3) % 7 not in (2, 6) else None
    for k in range(5): P.put(4 + k * 5, 5, [CRIMSON, LIMEG, BLUE, YELLOW, PINK][(k + f) % 5][3])
    P.rect(24, 4, 29, 5, SCREEN[2]); P.selout()

@drawer("vinyl", frames=4, ticks=[3, 3, 3, 3])
def vinyl(P, v, f, nf):
    P.sphere((1, 1, 22, 22), BLACK, rim=True); ring = P.ell_mask((4, 4, 19, 19)) - P.ell_mask((5, 5, 18, 18)); P.fill(ring, (60, 60, 66)); ring2 = P.ell_mask((7, 7, 16, 16)) - P.ell_mask((8, 8, 15, 15)); P.fill(ring2, (60, 60, 66))
    P.sphere((8, 8, 15, 15), v.get("ramp", CRIMSON)); a = f * math.pi / 2; P.put(int(11.5 + 2 * math.cos(a)), int(11.5 + 2 * math.sin(a)), SNOW[3]); P.put(11, 11, BLACK[1]); P.selout()

@drawer("cassette", size=(24, 16))
def cassette(P, v, f, nf):
    c = v.get("ramp", BLACK); P.box(1, 1, 22, 14, c, top=1, side=1); P.rect(3, 3, 20, 7, PAPER[2]); P.rect(3, 3, 20, 3, PAPER[3]); P.sphere((5, 8, 9, 12), SNOW); P.sphere((14, 8, 18, 12), SNOW); P.rect(10, 9, 13, 11, CHOC[1]); P.put(7, 10, c[1]); P.put(16, 10, c[1]); P.selout()

@drawer("radio", size=(24, 20), frames=4, ticks=[6, 6, 6, 6])
def radio(P, v, f, nf):
    c = v.get("ramp", CRIMSON); P.box(2, 5, 21, 18, c, top=1, side=2); P.sphere((4, 7, 11, 16), BLACK); P.sphere((6, 9, 9, 14), GREY); P.rect(13, 7, 19, 10, PAPER[2]); P.vline(14 + f, 7, 10, CRIMSON[2]); P.sphere((13, 12, 15, 14), SILV); P.sphere((17, 12, 19, 14), SILV); P.line(16, 5, 22, 0, STEEL[2]); P.selout()

@drawer("metronome", frames=4, ticks=[4, 4, 4, 4])
def metronome(P, v, f, nf):
    c = v.get("ramp", WOOD); P.poly([(12, 2), (4, 22), (19, 22)], c, box=(4, 2, 19, 22), shape="vcyl"); P.rect(10, 5, 13, 18, PAPER[2]); k = [-3, 0, 3, 0][f % 4]; P.line(11, 18, 11 + k, 5, STEEL[2]); P.rect(10 + k, 7, 12 + k, 8, STEEL[3]); P.hcyl((3, 21, 20, 23), c); P.selout()

@drawer("maracas", frames=4, ticks=[3, 3, 3, 3])
def maracas(P, v, f, nf):
    c = v.get("ramp", CRIMSON); s = [0, 1, 0, -1][f % 4]
    for (x, fl) in ((4, 1), (13, -1)):
        P.sphere((x + s * fl, 2, x + 7 + s * fl, 10), c, rim=True); P.rect(x + 3 + s * fl, 10, x + 4 + s * fl, 22, WOOD[2]); P.put(x + 1 + s * fl, 4, c[4]); P.hline(x + s * fl, x + 7 + s * fl, 6, YELLOW[3])
    P.selout()
    if f % 2: P.put(1, 1, SPARK); P.put(22, 1, SPARK)

@drawer("cowbell", frames=4, ticks=[6, 2, 6, 2])
def cowbell(P, v, f, nf):
    c = v.get("ramp", R((120, 110, 100))); s = [0, -1, 0, 1][f % 4]; P.poly([(8 + s, 3), (15 + s, 3), (18 + s, 20), (5 + s, 20)], c, box=(5, 3, 18, 20), shape="vcyl"); P.rect(10 + s, 0, 13 + s, 3, BLACK[2]); P.hline(5 + s, 18 + s, 20, c[0]); P.selout()
    if f in (1, 3): P.put(2 + s, 10, SPARK); P.put(21 + s, 10, SPARK)

@drawer("harmonica", size=(24, 12))
def harmonica(P, v, f, nf):
    P.box(1, 3, 22, 9, SILV, top=1, side=1); P.rect(2, 5, 21, 7, BLACK[1])
    for x in range(3, 21, 2): P.vline(x, 5, 7, SILV[2])
    P.selout()

@drawer("ukulele", size=(16, 32), frames=4, ticks=[8, 2, 8, 2])
def ukulele(P, v, f, nf):
    c = v.get("ramp", CARAMEL); P.sphere((2, 17, 13, 31), c, rim=True); P.sphere((3, 11, 12, 22), c, rim=True); P.rect(3, 17, 12, 22, c[2]); P.sphere((6, 20, 9, 23), BLACK); P.rect(7, 0, 8, 17, WOOD[2]); P.rect(6, 0, 9, 3, BLACK[2]); P.vline(7, 3, 25, (210, 210, 206)); P.vline(8, 3, 25, (210, 210, 206)) if False else None; P.rect(6, 26, 9, 27, BLACK[2]); P.selout()

@drawer("saxophone", size=(16, 32), frames=4, ticks=[8, 2, 8, 2])
def saxophone(P, v, f, nf):
    c = GOLD; P.poly([(8, 2), (11, 2), (12, 22), (7, 22)], c, box=(7, 2, 12, 22), shape="vcyl"); arc = P.ell_mask((2, 16, 15, 31)) - P.ell_mask((5, 16, 12, 28)); arc = {(x, y) for x, y in arc if y > 22 or x < 7}; P.shade(arc, (2, 16, 15, 31), c)
    P.sphere((1, 18, 6, 23), c); P.rect(9, 0, 12, 2, BLACK[2]); 
    for y in range(6, 20, 3): P.put(9, y, c[4])
    P.selout()

@drawer("violin", size=(16, 32), frames=4, ticks=[8, 2, 8, 2])
def violin(P, v, f, nf):
    c = v.get("ramp", R((170, 90, 50))); P.sphere((2, 12, 13, 22), c, rim=True); P.sphere((2, 20, 13, 31), c, rim=True); P.rect(3, 17, 12, 25, c[2]); P.rect(7, 0, 8, 20, WOOD[1]); P.rect(6, 0, 9, 3, BLACK[2]); P.vline(7, 3, 26, (210, 210, 206)); P.rect(5, 26, 10, 27, BLACK[2]); P.put(4, 20, BLACK[1]); P.put(11, 20, BLACK[1]); P.selout()

@drawer("stage_light", size=(24, 24), frames=4, ticks=[4, 4, 4, 4])
def stage_light(P, v, f, nf):
    cols = [CRIMSON, BLUE, LIMEG, PURPLE]; c = cols[f % 4]; P.rect(2, 1, 21, 2, BLACK[2]); P.rect(11, 2, 12, 5, BLACK[1]); P.poly([(6, 5), (17, 5), (19, 13), (4, 13)], BLACK, box=(4, 5, 19, 13), shape="vcyl"); P.rect(5, 13, 18, 14, c[3]); P.poly([(5, 15), (18, 15), (22, 23), (1, 23)], c, box=(1, 15, 22, 23), bands=(.0, .05, .1, .2)); P.selout()

@drawer("amp", frames=4, ticks=[6, 6, 6, 6])
def amp(P, v, f, nf):
    P.box(2, 4, 21, 22, BLACK, top=1, side=2); P.rect(3, 5, 20, 8, GREY[1]); P.sphere((6, 10, 17, 21), GREY); P.sphere((9, 13, 14, 18), BLACK); P.put(9, 6, LIMEG[3] if f % 2 else LIMEG[1])
    for x in (12, 15, 18): P.put(x, 6, SILV[3])
    P.rect(8, 2, 15, 4, BLACK[2]); P.selout()

@drawer("boombox", size=(32, 20), frames=4, ticks=[4, 4, 4, 4])
def boombox(P, v, f, nf):
    c = v.get("ramp", SILV); P.box(1, 5, 30, 18, c, top=1, side=1); k = f % 2; P.sphere((3 - k, 7 - k, 11 + k, 16 + k), BLACK); P.sphere((20 - k, 7 - k, 28 + k, 16 + k), BLACK); P.sphere((5, 9, 9, 13), GREY); P.sphere((22, 9, 26, 13), GREY)
    P.rect(13, 7, 18, 10, PAPER[2]); P.rect(13, 12, 18, 15, BLACK[2]); P.rect(14, 13, 15, 14, SNOW[3]); P.rect(16, 13, 17, 14, SNOW[3]); P.rect(10, 2, 21, 4, c[2]); P.line(26, 5, 31, 0, STEEL[2]); P.selout()

@drawer("ticket", size=(24, 12), frames=4, ticks=[8, 2, 8, 2])
def ticket(P, v, f, nf):
    c = v.get("ramp", GOLD); P.box(1, 2, 22, 9, c, top=1, side=1); P.rect(16, 2, 16, 9, c[0])
    for y in (4, 6): P.hline(3, 13, y, c[1])
    P.put(1, 5, None); P.put(22, 5, None); P.selout()

@drawer("triangle_inst", size=(16, 16), frames=4, ticks=[8, 2, 8, 2])
def triangle_inst(P, v, f, nf):
    P.line(8, 1, 2, 13, SILV[3]); P.line(8, 1, 14, 13, SILV[3]); P.line(3, 13, 13, 13, SILV[3]); P.put(8, 0, (190, 190, 186)); P.line(10, 6, 14, 2, SILV[2]) if f % 2 else P.line(11, 8, 15, 4, SILV[2]); P.selout()
    if f % 2: P.put(1, 6, SPARK); P.put(15, 15, SPARK)

# ---------------------------------------------------------------- finance desk (symbols, never figures)
@drawer("chart_board", size=(32, 24), frames=4, ticks=[6, 6, 6, 6])
def chart_board(P, v, f, nf):
    up = v.get("up", True); P.box(1, 1, 30, 22, BLACK, top=1, side=1); P.rect(2, 2, 29, 21, (18, 18, 22))
    for y in (6, 11, 16): P.hline(3, 28, y, (36, 36, 40))
    pts = [(4, 17), (8, 14), (12, 15), (16, 10), (20, 12), (24, 6), (28, 4)] if up else [(4, 5), (8, 8), (12, 7), (16, 12), (20, 10), (24, 16), (28, 18)]
    n = min(len(pts), 3 + f + 1)
    for a, b in zip(pts[:n], pts[1:n]): P.line(a[0], a[1], b[0], b[1], LIMEG[3] if up else CORAL_R[3])
    P.put(pts[n - 1][0], pts[n - 1][1], SNOW[4]); P.selout()

@drawer("ticker_tape", size=(32, 16), frames=4, ticks=[4, 4, 4, 4])
def ticker_tape(P, v, f, nf):
    P.hcyl((22, 3, 30, 13), PAPER); P.sphere((24, 5, 28, 11), PAPER, bands=(.3, .5, .75, .95)); P.put(26, 8, PAPER[0]); P.rect(1, 6, 23, 10, PAPER[2]); P.rect(1, 6, 23, 6, PAPER[3]); P.hline(1, 23, 10, PAPER[1])
    for x in range(2 - f, 22, 3): P.rect(x, 8, x + 1, 8, (120, 110, 100)) if x >= 2 else None
    P.selout()

@drawer("bull", frames=4, ticks=[8, 2, 8, 2])
def bull(P, v, f, nf):
    c = v.get("ramp", R((150, 90, 50))); dy = [0, -1, 0, 0][f % 4]; P.sphere((3, 9 + dy, 18, 20 + dy), c, rim=True); P.sphere((13, 4 + dy, 22, 13 + dy), c); P.rect(19, 9 + dy, 22, 12 + dy, PINK[2]); P.put(18, 7 + dy, INK)
    P.line(14, 5 + dy, 11, 1 + dy, CREAMW[3]); P.line(20, 4 + dy, 23, 1 + dy, CREAMW[3]); P.put(11, 1 + dy, CREAMW[4]); P.put(23, 1 + dy, CREAMW[4])
    for x in (5, 9, 13, 16): P.rect(x, 20, x + 1, 23, c[1])
    P.line(3, 12 + dy, 0, 8 + dy, c[1]); P.selout()

@drawer("bear", frames=4, ticks=[8, 2, 8, 2])
def bear(P, v, f, nf):
    c = v.get("ramp", R((90, 70, 60))); dy = [0, 0, -1, 0][f % 4]; P.sphere((2, 8 + dy, 17, 20 + dy), c, rim=True); P.sphere((12, 5 + dy, 21, 13 + dy), c); P.sphere((12, 3 + dy, 15, 6 + dy), c); P.put(19, 8 + dy, INK); P.put(21, 10 + dy, BLACK[0])
    for x in (4, 8, 12, 15): P.rect(x, 20, x + 1, 23, c[1])
    P.selout()

@drawer("mini_pig", size=(16, 16), frames=4, ticks=[8, 2, 8, 2])
def mini_pig(P, v, f, nf):
    c = v.get("ramp", PINK); P.sphere((1, 4, 13, 13), c, rim=True); P.sphere((10, 7, 15, 11), c); P.put(13, 8, c[1]); P.put(13, 9, c[1]); P.put(10, 6, INK); P.rect(6, 3, 8, 3, c[0]); P.poly([(3, 4), (5, 1), (6, 5)], c, box=(3, 1, 6, 5))
    for x in (3, 6, 9): P.rect(x, 13, x + 1, 15, c[1])
    P.selout()
    if f == 1: P.put(7, 1, GOLD[3])

@drawer("money_bag", frames=4, ticks=[8, 2, 8, 2])
def money_bag(P, v, f, nf):
    c = v.get("ramp", WHEAT); P.sphere((3, 8, 20, 23), c, rim=True); P.poly([(8, 2), (15, 2), (17, 9), (6, 9)], c, box=(6, 2, 17, 9), shape="vcyl"); P.hcyl((7, 7, 16, 9), LEATHER)
    P.rect(11, 12, 12, 19, GOLD[2]); P.hline(9, 14, 13, GOLD[2]); P.hline(9, 14, 15, GOLD[2]); P.hline(9, 14, 18, GOLD[2]); P.put(9, 14, GOLD[2]); P.put(14, 17, GOLD[2]); P.rect(11, 11, 12, 11, GOLD[3]); P.rect(11, 20, 12, 20, GOLD[3]); P.selout()

@drawer("coin_stack", frames=4, ticks=[8, 2, 8, 2])
def coin_stack(P, v, f, nf):
    c = GOLD
    for i in range(5): P.hcyl((4, 18 - i * 3, 15, 21 - i * 3), c); P.hline(5, 14, 18 - i * 3, c[3])
    P.hcyl((13, 15 - (f % 2), 22, 18 - (f % 2)), c); P.hcyl((14, 19, 23, 22), c); P.hline(14, 22, 19, c[3]); P.selout()
    if f == 1: P.sparkle(6, 4, 1, SPARK)

@drawer("stamp", frames=4, ticks=[8, 2, 2, 8])
def stamp(P, v, f, nf):
    down = f in (1, 2); dy = 4 if down else 0; P.rect(10, 1 + dy, 13, 8 + dy, WOOD[2]); P.sphere((9, 0 + dy, 14, 3 + dy), WOOD); P.box(4, 8 + dy, 19, 13 + dy, CRIMSON, top=1, side=1); P.rect(4, 13 + dy, 19, 14 + dy, BLACK[1])
    if down: P.rect(6, 19, 17, 22, CRIMSON[2]); P.rect(8, 20, 15, 21, CRIMSON[4])
    P.selout()

@drawer("abacus", frames=4, ticks=[6, 6, 6, 6])
def abacus(P, v, f, nf):
    P.box(1, 1, 22, 22, WOOD, top=1, side=1); P.rect(3, 3, 20, 20, (20, 16, 18))
    for i, y in enumerate((5, 9, 13, 17)):
        P.hline(3, 20, y + 1, STEEL[1]); n = [3, 1, 4, 2][i]; shift = (f + i) % 3
        for k in range(n): x = 4 + k * 3 + shift * 2; P.sphere((x, y, x + 2, y + 2), [CRIMSON, GOLD, BLUE, GRASS][i])
    P.selout()

@drawer("safe", frames=4, ticks=[8, 2, 8, 2])
def safe(P, v, f, nf):
    c = v.get("ramp", STEEL); P.box(2, 2, 21, 21, c, top=1, side=2); P.rect(4, 4, 17, 19, c[1]); P.sphere((8, 8, 14, 14), SILV); a = f * math.pi / 2; P.put(int(11 + 2 * math.cos(a)), int(11 + 2 * math.sin(a)), INK); P.rect(16, 9, 17, 13, BLACK[2]); P.rect(5, 21, 7, 23, c[1]); P.rect(16, 21, 18, 23, c[1]); P.selout()

@drawer("receipt", size=(16, 24), frames=4, ticks=[8, 2, 8, 2])
def receipt(P, v, f, nf):
    s = _sw(f, nf); P.rect(3 + s, 1, 12 + s, 20, PAPER[2]); P.rect(3 + s, 1, 12 + s, 1, PAPER[3])
    for x in range(3, 13, 2): P.put(x + s, 21, PAPER[2])
    for y in (4, 7, 10, 13): P.hline(5 + s, 10 + s, y, (170, 160, 140))
    P.hline(5 + s, 10 + s, 16, (120, 110, 100)); P.selout()

@drawer("wallet", frames=4, ticks=[8, 2, 8, 2])
def wallet(P, v, f, nf):
    c = v.get("ramp", LEATHER); P.box(2, 6, 21, 20, c, top=1, side=2); P.rect(2, 10, 21, 11, c[1]); P.rect(16, 12, 19, 14, GOLD[2]); P.rect(5, 3, 12, 6, R((200, 60, 60))[2]); P.rect(13, 4, 18, 6, R((60, 120, 200))[2]); P.selout()

@drawer("card", size=(24, 16))
def card(P, v, f, nf):
    c = v.get("ramp", BLUE); P.box(1, 2, 22, 13, c, top=1, side=1); P.rect(1, 5, 22, 6, BLACK[1]); P.rect(3, 8, 7, 10, GOLD[2]); P.put(3, 8, GOLD[3])
    for x in range(9, 20, 3): P.hline(x, x + 1, 11, c[3])
    P.selout()

@drawer("arrow", frames=4, ticks=[8, 2, 8, 2])
def arrow(P, v, f, nf):
    up = v.get("up", True); c = LIMEG if up else CORAL_R; dy = [0, -1, 0, 0][f % 4] * (1 if up else -1)
    if up: P.poly([(12, 2 + dy), (21, 11 + dy), (15, 11 + dy), (15, 21 + dy), (9, 21 + dy), (9, 11 + dy), (3, 11 + dy)], c, box=(3, 2, 21, 21), shape="vcyl")
    else: P.poly([(12, 21 + dy), (21, 12 + dy), (15, 12 + dy), (15, 2 + dy), (9, 2 + dy), (9, 12 + dy), (3, 12 + dy)], c, box=(3, 2, 21, 21), shape="vcyl")
    P.selout()

@drawer("magnifier", frames=4, ticks=[8, 2, 8, 2])
def magnifier(P, v, f, nf):
    ring = P.ell_mask((2, 2, 15, 15)) - P.ell_mask((4, 4, 13, 13)); P.shade(ring, (2, 2, 15, 15), BLACK); P.shade(P.ell_mask((4, 4, 13, 13)), (4, 4, 13, 13), ICE, bands=(.02, .1, .5, .95)); P.line(13, 13, 21, 21, WOOD[2]); P.line(14, 13, 22, 21, WOOD[1]); P.put(6, 6, SNOW[4]); P.put(7, 6, SNOW[4]); P.selout()
    if f == 1: P.sparkle(9, 9, 1, SPARK)

@drawer("telescope", frames=4, ticks=[8, 2, 8, 2])
def telescope(P, v, f, nf):
    P.poly([(2, 12), (2, 16), (16, 6), (16, 1)], STEEL, box=(2, 1, 16, 16), shape="hcyl"); P.poly([(15, 1), (22, -2 + 2), (22, 4), (15, 6)], BLACK, box=(15, 0, 22, 6), shape="hcyl"); P.line(10, 12, 7, 22, WOOD[1]); P.line(10, 12, 13, 22, WOOD[1]); P.line(10, 12, 10, 22, WOOD[1]); P.selout()
    if f == 1: P.put(23, 1, SPARK)

@drawer("binoculars", size=(24, 16))
def binoculars(P, v, f, nf):
    c = BLACK
    for x in (1, 13): P.vcyl((x, 3, x + 9, 13), c); P.hcyl((x, 1, x + 9, 4), c); P.sphere((x + 2, 2, x + 7, 4), ICE, bands=(.02, .1, .5, .95)) if False else None
    P.rect(10, 6, 13, 10, c[2]); P.rect(11, 5, 12, 6, c[3]); P.put(3, 6, GREY[3]); P.put(15, 6, GREY[3]); P.selout()

@drawer("newspaper", size=(24, 20))
def newspaper(P, v, f, nf):
    P.box(2, 2, 21, 17, PAPER, top=1, side=1); P.rect(4, 4, 19, 6, (90, 86, 80)); P.rect(4, 8, 10, 15, (160, 150, 130))
    for y in (8, 10, 12, 14): P.hline(12, 19, y, (170, 160, 140))
    P.selout()

@drawer("target", frames=4, ticks=[8, 2, 8, 2])
def target(P, v, f, nf):
    for i, (r, c) in enumerate([(10, CRIMSON), (7, SNOW), (4, CRIMSON), (1, SNOW)]): P.sphere((11 - r, 11 - r, 12 + r, 12 + r), c, bands=(.1, .3, .6, .9) if i == 0 else (.0, .05, .5, .95))
    if f == 1: P.line(12, 11, 20, 3, STEEL[2]); P.rect(19, 2, 21, 4, GOLD[3])
    P.selout()

@drawer("parachute", size=(24, 32), frames=4, ticks=[8, 2, 8, 2])
def parachute(P, v, f, nf):
    cols = [CRIMSON, SNOW]; s = _sw(f, nf); dome = P.ell_mask((1, 1, 22, 17)) - set((x, y) for x in range(24) for y in range(10, 32)); P.shade(dome, (1, 1, 22, 17), cols[0], bands=(.1, .3, .6, .9))
    for (x, y) in dome:
        if ((x - 1) // 6) % 2: P.put(x, y, cols[1][2] if P.get(x, y)[:3] == cols[0][2] else cols[1][3] if P.get(x, y)[:3] == cols[0][3] else cols[1][1])
    for x in (2, 9, 15, 21): P.line(x, 10, 12 + s, 24, (190, 190, 186))
    P.box(9 + s, 24, 14 + s, 30, WOOD, top=1, side=1); P.selout()

@drawer("extinguisher", size=(16, 24))
def extinguisher(P, v, f, nf):
    P.vcyl((4, 6, 11, 21), CRIMSON); P.hcyl((4, 20, 11, 23), CRIMSON); P.hcyl((4, 4, 11, 7), CRIMSON); P.rect(6, 1, 9, 4, BLACK[2]); P.rect(9, 0, 12, 1, BLACK[1]); P.rect(1, 6, 4, 7, BLACK[1]); P.rect(1, 7, 2, 13, BLACK[2]); P.rect(5, 10, 10, 14, PAPER[2]); P.vline(5, 7, 20, CRIMSON[3]); P.selout()

@drawer("first_aid")
def first_aid(P, v, f, nf):
    P.box(2, 6, 21, 21, SNOW, top=1, side=2); P.rect(8, 3, 15, 6, SNOW[1]); P.rect(9, 4, 14, 5, None); P.rect(10, 9, 13, 18, GRASS[2]); P.rect(7, 12, 16, 15, GRASS[2]); P.put(10, 9, GRASS[3]); P.selout()

@drawer("crystal_ball", frames=4, ticks=[4, 4, 4, 4])
def crystal_ball(P, v, f, nf):
    P.sphere((3, 1, 20, 18), R((150, 120, 220)), bands=(.02, .1, .5, .95), rim=True); P.hcyl((5, 17, 18, 21), GOLD); P.hcyl((7, 20, 16, 23), GOLD)
    rr = _rng(f)
    for i in range(4): x = 6 + rr.randrange(12); y = 3 + rr.randrange(12); P.put(x, y, SNOW[4]) if P.get(x, y)[3] else None
    P.put(6, 4, SNOW[4]); P.put(7, 4, SNOW[4]); P.selout()

@drawer("rolodex", frames=4, ticks=[6, 6, 6, 6])
def rolodex(P, v, f, nf):
    P.box(2, 14, 21, 21, BLACK, top=1, side=2); P.rect(3, 8, 20, 14, PAPER[2]); P.rect(3, 8, 20, 8, PAPER[3]); P.rect(5 + (f % 3) * 4, 6, 8 + (f % 3) * 4, 8, PAPER[3])
    for y in (10, 12): P.hline(5, 18, y, (170, 160, 140))
    P.sphere((0, 15, 3, 18), STEEL); P.sphere((20, 15, 23, 18), STEEL); P.selout()

@drawer("desk_bell", frames=4, ticks=[8, 2, 8, 2])
def desk_bell(P, v, f, nf):
    c = v.get("ramp", SILV); P.sphere((4, 6, 19, 19), c, rim=True); P.rect(4, 13, 19, 19, c[2]); P.hcyl((3, 19, 20, 22), BLACK); P.rect(10, 3, 13, 6, c[2]); P.sphere((9, 1, 14, 4), c); P.selout()
    if f == 1: P.put(2, 8, SPARK); P.put(21, 8, SPARK); P.put(11, 0, SPARK)


# ---------------------------------------------------------------- the ten families (50 each) -> PROP-001..PROP-500
FAMILIES = [("OFFICE", "Office · desk life"), ("FOOD", "Food & drink · NYC"), ("TECH", "Tech & gadgets"), ("TOOLS", "Tools & work"), ("SPORT", "Sports & games"),
            ("TOYS", "Toys & fun"), ("STREET", "Street · NYC"), ("FANTASY", "Fantasy · the game studio"), ("MUSIC", "Music & party"), ("FINANCE", "The finance desk (symbols, never figures)")]
SCREENS = R((40, 60, 80), dark=.6)
FAMILY_ITEMS = {
"OFFICE": [
    V("laptop", "Laptop"), V("laptop", "Laptop, black", ramp=BLACK), V("monitor", "Monitor, chart", chart=True), V("monitor", "Monitor, text"), V("keyboard", "Keyboard"), V("keyboard", "Keyboard, black", ramp=BLACK), V("mouse", "Mouse"), V("mouse", "Mouse, black", ramp=BLACK),
    V("phone", "Phone"), V("phone", "Phone, white", ramp=SNOW), V("headphones", "Headphones"), V("headphones", "Headphones, white", ramp=SNOW, pad=BLACK), V("desk_lamp", "Desk lamp, red"), V("desk_lamp", "Desk lamp, lime", ramp=LIMEG),
    V("plant", "Desk plant"), V("plant", "Desk plant, blue pot", ramp=PASTEL_BLUE), V("cactus", "Cactus"), V("cactus", "Cactus in bloom", flower=True), V("notebook", "Notebook, blue"), V("notebook", "Notebook, red", ramp=CRIMSON), V("notebook", "Notebook, lime", ramp=LIMEG),
    V("pen", "Pen, blue"), V("pen", "Pen, black", ramp=BLACK), V("pencil", "Pencil"), V("sticky", "Sticky note"), V("sticky", "Sticky note, pink", ramp=PINK), V("sticky", "Sticky note, peeling", ramp=LIMEG, peel=True), V("stapler", "Stapler"), V("scissors", "Scissors"),
    V("calculator", "Calculator (blank)"), V("coffee_pot", "Coffee pot"), V("water_bottle", "Water bottle"), V("water_bottle", "Water bottle, pink", ramp=PINK), V("papers", "Stack of paper"), V("folder", "Folder"), V("folder", "Folder, red", ramp=CRIMSON),
    V("trash", "Trash can"), V("trash", "Trash can, full", full=True), V("whiteboard", "Whiteboard, chart", chart=True), V("whiteboard", "Whiteboard, notes"), V("briefcase", "Briefcase"), V("backpack", "Backpack"), V("backpack", "Backpack, red", ramp=CRIMSON),
    V("badge", "ID badge (blank)"), V("duck", "Rubber duck"), V("globe", "Globe"), V("printer", "Printer"), V("office_chair", "Office chair"), V("clipboard", "Clipboard"), V("mug", "Coffee mug", ramp=SNOW, liq=CHOC),
],
"FOOD": [
    V("pizza", "Pizza slice"), V("pizza", "Whole pizza", whole=True), V("bagel", "Bagel"), V("bagel", "Bagel, everything, cream cheese", seeds=True, cream=True), V("pretzel", "Pretzel"), V("taco", "Taco"), V("sushi", "Nigiri", kind="nigiri"), V("sushi", "Maki roll", kind="maki"),
    V("ramen", "Ramen"), V("ramen", "Ramen, black bowl", ramp=BLACK), V("donut", "Donut, pink"), V("donut", "Donut, chocolate", ramp=CHOC), V("sandwich", "Sandwich"), V("apple", "Apple"), V("apple", "Green apple", ramp=GRASS), V("banana", "Banana"), V("avocado", "Avocado"),
    V("chips", "Bag of chips"), V("chips", "Chips, blue bag", ramp=BLUE), V("wine", "Glass of red"), V("wine", "Glass of white", liq=R((240, 220, 150))), V("cocktail", "Cocktail"), V("cocktail", "Cocktail, blue", liq=SUMMER_BLUE), V("candy", "Candy, pink"), V("candy", "Candy, blue", ramp=BLUE),
    V("chocolate", "Chocolate bar"), V("popcorn", "Popcorn"), V("hot_sauce", "Hot sauce"), V("coffee_cup", "Coffee to go"), V("coffee_cup", "Coffee to go, blue cup", ramp=SUMMER_BLUE, band=SNOW), V("burger", "Burger", tomato=True), V("hotdog", "Hot dog", mustard=True),
    V("cupcake", "Cupcake", sprinkles=True), V("ice_cream", "Ice cream", ramps=[PINK, SNOW], cherry=True), V("can", "Soda can"), V("can", "Soda can, blue", ramp=BLUE), V("mug", "Cocoa", ramp=CRIMSON, liq=CHOC, marsh=True), V("pie", "Pie", fill=BERRY, lattice=True), V("watermelon", "Watermelon"),
    V("corn", "Corn", butter=True), V("cookie", "Cookie"), V("glass", "Beer mug", kind="mug", liq=R((230, 170, 60))), V("glass", "Lemonade", kind="pitcher", lemon=True), V("bottle", "Soda bottle"), V("teapot", "Teapot", ramp=TEAL), V("cherries", "Cherries"), V("carrot", "Carrot"),
    V("bun", "Bun"), V("lollipop", "Lollipop"), V("candy_cane", "Candy cane"),
],
"TECH": [
    V("server", "Server rack"), V("router", "Router"), V("usb", "USB stick"), V("usb", "USB stick, red", ramp=CRIMSON), V("battery", "Battery charging"), V("bulb", "Light bulb"), V("magnet", "Magnet"), V("camera", "Camera"), V("camera", "Camera, silver", ramp=SILV),
    V("speaker", "Speaker"), V("speaker", "Speaker, white", ramp=SNOW), V("controller", "Game controller"), V("controller", "Controller, white", ramp=SNOW), V("joystick", "Joystick"), V("robot", "Robot toy"), V("robot", "Robot toy, blue", ramp=BLUE), V("drone", "Drone"),
    V("vr", "VR headset"), V("tablet", "Tablet"), V("tv", "Old TV, static"), V("floppy", "Floppy disk"), V("floppy", "Floppy disk, black", ramp=BLACK), V("cd", "CD"), V("dish", "Satellite dish"), V("chip", "Microchip"), V("keycap", "Keycap"), V("keycap", "Keycap, marked", mark=True, ramp=LIMEG),
    V("smartwatch", "Smartwatch"), V("cable", "Cable"), V("cable", "Cable, white", ramp=SNOW), V("laptop", "Laptop, silver"), V("monitor", "Monitor"), V("phone", "Phone"), V("headphones", "Headphones, lime", ramp=LIMEG, pad=BLACK), V("mouse", "Mouse"), V("keyboard", "Keyboard"),
    V("desk_lamp", "Desk lamp, black", ramp=BLACK), V("printer", "Printer"), V("calculator", "Calculator"), V("radio", "Radio"), V("cassette", "Cassette"), V("boombox", "Boombox"), V("stage_light", "Stage light"), V("amp", "Amp"), V("microphone", "Microphone"),
    V("clock", "Wall clock"), V("stopwatch", "Stopwatch"), V("bulb", "Light bulb (idea)"), V("vinyl", "Vinyl record"), V("synth", "Synth"),
],
"TOOLS": [
    V("toolbox", "Toolbox"), V("toolbox", "Toolbox, blue", ramp=BLUE), V("wrench", "Wrench"), V("hammer", "Hammer"), V("screwdriver", "Screwdriver, red"), V("screwdriver", "Screwdriver, yellow", ramp=YELLOW), V("pliers", "Pliers"), V("drill", "Drill"), V("tape", "Tape measure"), V("saw", "Hand saw"),
    V("ladder", "Ladder"), V("paint_roller", "Paint roller"), V("paintbrush", "Paintbrush, blue"), V("paintbrush", "Paintbrush, red", ramp=CRIMSON), V("bucket", "Bucket"), V("bucket", "Bucket of paint", liq=LIMEG), V("gloves", "Work gloves"), V("cone", "Cone"), V("barrier", "Barrier", light=True),
    V("shovel", "Shovel"), V("wheelbarrow", "Wheelbarrow", load=True), V("hat", "Hard hat", kind="hardhat", ramp=YELLOW), V("vest", "Hi-vis vest"), V("boots", "Work boots", ramp=LEATHER, work=True), V("clipboard", "Clipboard"), V("lunchpail", "Lunch pail"), V("thermos", "Thermos", steam=True),
    V("nail", "Nail"), V("gear", "Gear"), V("gear", "Gear, brass", ramp=GOLD), V("anvil", "Anvil"), V("pickaxe", "Pickaxe"), V("blowtorch", "Blowtorch"), V("level", "Spirit level"), V("toolbelt", "Tool belt"), V("axe", "Axe"), V("ladder", "Ladder, aluminium", ramp=SILV),
    V("watering_can", "Watering can"), V("lantern", "Work lantern", ramp=STEEL, shape="metal"), V("extinguisher", "Fire extinguisher"), V("first_aid", "First aid kit"), V("scissors", "Scissors", ramp=BLUE), V("key", "Key"), V("lock", "Padlock"), V("magnet", "Magnet"), V("bulb", "Bulb"),
    V("cable", "Cable"), V("duck", "Debugging duck"), V("coffee_cup", "Coffee to go"), V("stapler", "Stapler, black", ramp=BLACK),
],
"SPORT": [
    V("basketball", "Basketball"), V("soccer", "Soccer ball"), V("football", "Football"), V("baseball", "Bat and ball"), V("racket", "Tennis racket"), V("racket", "Racket, red", ramp=CRIMSON), V("dumbbell", "Dumbbell"), V("dumbbell", "Dumbbell, lifting", lift=True), V("skateboard", "Skateboard"), V("skateboard", "Skateboard, lime", ramp=LIMEG),
    V("bicycle", "Bicycle"), V("bicycle", "Bicycle, blue", ramp=BLUE), V("whistle", "Whistle"), V("stopwatch", "Stopwatch"), V("trophy", "Trophy"), V("trophy", "Trophy, silver", ramp=SILV), V("medal", "Medal"), V("dice", "Dice"), V("dice", "Dice, red", ramp=CRIMSON, face=3), V("cards", "Playing cards"),
    V("dartboard", "Dartboard"), V("chess", "Chess king", kind="king"), V("chess", "Chess knight", kind="knight"), V("chess", "Chess pawn, white", kind="pawn", ramp=SNOW), V("chess", "Chess rook", kind="rook"), V("token", "Arcade token"), V("bowling", "Bowling"), V("golf", "Golf"), V("hockey", "Hockey"),
    V("boxing", "Boxing glove"), V("boxing", "Boxing glove, blue", ramp=BLUE), V("frisbee", "Frisbee"), V("yoyo", "Yo-yo"), V("puzzle", "Puzzle piece"), V("puzzle", "Puzzle piece, red", ramp=CRIMSON), V("cube", "Puzzle cube"), V("domino", "Domino"), V("controller", "Controller"), V("joystick", "Joystick"),
    V("kite", "Kite", ramp=CRIMSON), V("beach_ball", "Beach ball"), V("float", "Pool float"), V("pinwheel", "Pinwheel"), V("target", "Target"), V("sunglasses", "Sunglasses"), V("hat", "Cap", kind="cap", ramp=BLUE), V("water_bottle", "Water bottle", ramp=LIMEG), V("rosette", "Rosette", ramp=BLUE), V("confetti", "Confetti", ramps=[GOLD, CRIMSON, BLUE, LIME]), V("flag", "Pennant flag", ramps=[CRIMSON, SNOW], style="stripes"),
],
"TOYS": [
    V("teddy", "Teddy bear"), V("teddy", "Teddy bear, with bow", bow=True), V("teddy", "Teddy bear, grey", ramp=GREY), V("robot", "Robot toy"), V("duck", "Rubber duck"), V("duck", "Rubber duck, pink", ramp=PINK), V("toy_car", "Toy car"), V("toy_car", "Toy car, blue", ramp=BLUE), V("toy_train", "Toy train"),
    V("blocks", "Building blocks"), V("rocking_horse", "Rocking horse"), V("bubbles", "Bubble wand"), V("water_gun", "Water gun"), V("jack_box", "Jack-in-the-box"), V("top", "Spinning top"), V("top", "Spinning top, blue", ramp=BLUE), V("marbles", "Marbles"), V("paper_plane", "Paper plane"),
    V("sand_pail", "Sand pail"), V("crayons", "Crayons"), V("palette", "Paint palette"), V("brick_toy", "Toy brick"), V("brick_toy", "Toy brick, blue", ramp=BLUE), V("brick_toy", "Toy brick, yellow", ramp=YELLOW), V("kazoo", "Kazoo"), V("slinky", "Slinky"), V("yoyo", "Yo-yo, blue", ramp=BLUE),
    V("kite", "Kite", ramp=SUMMER_BLUE, ramp2=YELLOW), V("pinwheel", "Pinwheel"), V("balloon", "Balloon, red", ramp=CRIMSON), V("balloon", "Balloon, blue", ramp=BLUE), V("balloon", "Balloon, lime", ramp=LIME), V("bunny", "Plush bunny", ramp=GREY), V("lamb", "Plush lamb"), V("chick", "Plush chick"),
    V("dice", "Dice"), V("cards", "Cards"), V("puzzle", "Puzzle piece", ramp=GRASS), V("cube", "Puzzle cube"), V("rocket", "Toy rocket"), V("popper", "Party popper", ramp=BLUE), V("confetti", "Confetti", ramps=[PINK, BLUE, YELLOW]), V("lollipop", "Lollipop"), V("candy", "Candy"),
    V("snowglobe", "Snow globe"), V("ball_drop", "Light-up ball on a pole"), V("sparkler", "Sparkler"), V("float", "Pool float", ramps=[YELLOW, SNOW]), V("beach_ball", "Beach ball"), V("frisbee", "Frisbee", ramp=PINK),
],
"STREET": [
    V("traffic_light", "Traffic light"), V("street_lamp", "Street lamp"), V("hydrant", "Fire hydrant"), V("hydrant", "Hydrant, spraying", spray=True), V("mailbox", "Mailbox"), V("bench", "Park bench"), V("trash", "Trash can"), V("cone", "Traffic cone"), V("barrier", "Barrier", light=True),
    V("pigeon", "Pigeon"), V("rat", "Rat"), V("rat", "Rat with a pizza slice", pizza=True), V("subway_sign", "Subway globe, green"), V("subway_sign", "Subway globe, red", ramp=CRIMSON), V("taxi", "Taxi"), V("hotdog_cart", "Hot dog cart"), V("news_box", "Newspaper box"), V("news_box", "Newspaper box, red", ramp=CRIMSON),
    V("manhole", "Manhole cover"), V("water_tower", "Water tower"), V("parking_meter", "Parking meter"), V("fire_escape", "Fire escape"), V("payphone", "Payphone"), V("dumpster", "Dumpster"), V("dumpster", "Dumpster, blue", ramp=BLUE), V("stoop", "Stoop"), V("bollard", "Bollard"),
    V("crosswalk_sign", "Crosswalk sign"), V("scaffold", "Scaffolding"), V("bike_rack", "Bike rack"), V("bicycle", "Bicycle, delivery", ramp=BLACK), V("umbrella", "Umbrella, black", ramp=BLACK, ramp2=BLACK), V("coffee_cup", "Coffee to go"), V("pizza", "Pizza slice"), V("pretzel", "Street pretzel"), V("bagel", "Bagel", seeds=True),
    V("newspaper", "Newspaper"), V("sign", "Blank street sign", shape="rect", ramp=GRASS), V("sign", "Blank round sign", shape="round", ramp=SNOW), V("lantern", "Lantern", ramp=STEEL, shape="metal"), V("skateboard", "Skateboard"), V("dove", "Pigeon's cousin: dove"), V("plant", "Sidewalk planter", ramp=GREY, leaf=GRASS), V("tree", "Street tree", ramp=GRASS),
    V("raincloud", "Rain cloud"), V("boots", "Rain boots", ramp=YELLOW), V("kite", "Kite", ramp=CRIMSON), V("bollard", "Bollard, yellow", ramp=YELLOW), V("mailbox", "Mailbox, green", ramp=GRASS), V("bench", "Bench, green", ramp=GRASS),
],
"FANTASY": [
    V("sword", "Sword"), V("shield", "Shield"), V("shield", "Shield, red", ramp=CRIMSON, emblem=SNOW), V("potion", "Potion, purple"), V("potion", "Potion, red", ramp=CRIMSON), V("potion", "Potion, green", ramp=GRASS), V("chest", "Treasure chest"), V("wand", "Magic wand"), V("crystal", "Crystal"), V("crystal", "Crystal, teal", ramp=TURQ),
    V("key", "Key"), V("key", "Key, silver", ramp=SILV), V("lock", "Lock"), V("map", "Treasure map"), V("compass", "Compass"), V("bomb", "Bomb"), V("heart_box", "Heart container"), V("gem", "Gem, teal"), V("gem", "Gem, red", ramp=CRIMSON), V("gem", "Gem, purple", ramp=PURPLE), V("mushroom", "Mushroom"), V("mushroom", "Mushroom, green", ramp=GRASS),
    V("spellbook", "Spellbook"), V("ring", "Ring"), V("bow_arrow", "Bow and arrow"), V("helmet", "Helmet"), V("cauldron", "Cauldron"), V("dragon_egg", "Dragon egg"), V("dragon_egg", "Dragon egg, red", ramp=CRIMSON), V("staff", "Staff"), V("rune", "Rune stone"), V("slingshot", "Slingshot"), V("treasure_bag", "Loot bag"),
    V("crown", "Crown"), V("hat", "Wizard hat", kind="wizard", ramp=PURPLE), V("torch", "Torch"), V("lantern", "Lantern", ramp=STEEL, shape="metal"), V("scroll", "Scroll", seal=True), V("coin", "Gold coin"), V("dice", "Dice"), V("hourglass", "Hourglass"), V("anvil", "Anvil"), V("pickaxe", "Pickaxe"),
    V("book", "Tome", ramp=LEATHER, ribbon=True), V("candle", "Candle", ramp=CREAMW, holder=True), V("campfire", "Campfire"), V("tent", "Tent"), V("boots", "Adventurer's boots", ramp=LEATHER), V("bell", "Bell"), V("star", "Star"),
],
"MUSIC": [
    V("guitar", "Guitar"), V("guitar", "Guitar, black", ramp=BLACK), V("synth", "Synth"), V("drum", "Drum", ramp=CRIMSON), V("drum", "Drum, blue", ramp=BLUE), V("headphones", "Headphones", pad=CRIMSON), V("microphone", "Microphone"), V("microphone", "Hand mic", stand=False), V("speaker", "Speaker"),
    V("vinyl", "Vinyl record"), V("vinyl", "Vinyl, blue label", ramp=BLUE), V("cassette", "Cassette"), V("radio", "Radio"), V("metronome", "Metronome"), V("bugle", "Trumpet-ish bugle"), V("maracas", "Maracas"), V("tambourine", "Tambourine"), V("cowbell", "Cowbell"), V("harmonica", "Harmonica"),
    V("ukulele", "Ukulele"), V("saxophone", "Saxophone"), V("violin", "Violin"), V("stage_light", "Stage light"), V("amp", "Amp"), V("boombox", "Boombox"), V("ticket", "Concert ticket (blank)"), V("triangle_inst", "Triangle"), V("disco", "Disco ball"),
    V("balloon", "Balloon, pink", ramp=PINK), V("balloon", "Balloon, gold", ramp=GOLDY), V("confetti", "Confetti", ramps=[GOLD, CRIMSON, BLUE, LIME]), V("streamer", "Streamer", ramp=PINK), V("party_hat", "Party hat", ramp=BLUE, stripes=True), V("popper", "Party popper", ramp=CRIMSON), V("horn", "Party horn", ramp=BLUE),
    V("champagne", "Champagne"), V("glass", "Flute", kind="flute"), V("cake", "Cake", ramp=CHOC, candle=True), V("cupcake", "Cupcake", sprinkles=True), V("candle", "Candle", ramp=CRIMSON), V("bunting", "Bunting", ramps=[PINK, GOLDY, BLUE]), V("lights", "String lights", ramps=[CRIMSON, GOLDY, BLUE, LIME]),
    V("sparkle", "Twinkle"), V("star", "Star"), V("glasses", "Party shades", shape="star", ramp=GOLDY), V("bow_tie", "Bow tie"), V("hat", "Top hat", kind="top", ramp=BLACK), V("gift", "Gift", ramp=PINK, ribbon=GOLDY), V("kazoo", "Kazoo"), V("bell", "Bell"),
],
"FINANCE": [
    V("chart_board", "Chart, up (no figures)", up=True), V("chart_board", "Chart, down (no figures)", up=False), V("ticker_tape", "Ticker tape (blank)"), V("bull", "Bull"), V("bear", "Bear"), V("mini_pig", "Piggy bank, mini"), V("mini_pig", "Piggy bank, gold", ramp=GOLDY), V("money_bag", "Money bag"),
    V("coin_stack", "Coin stack"), V("coin", "Coin"), V("calculator", "Calculator (blank)"), V("book", "Ledger", ramp=LEATHER, ribbon=True), V("bell", "Opening bell", ramp=COPPER), V("desk_bell", "Desk bell"), V("gavel", "Gavel"), V("scales", "Scales"), V("stamp", "Rubber stamp"), V("abacus", "Abacus"),
    V("safe", "Safe"), V("receipt", "Receipt (blank)"), V("wallet", "Wallet"), V("card", "Card (blank)"), V("arrow", "Arrow up", up=True), V("arrow", "Arrow down", up=False), V("magnifier", "Magnifying glass"), V("telescope", "Telescope"), V("binoculars", "Binoculars"), V("newspaper", "Newspaper"),
    V("target", "Target"), V("dartboard", "Dartboard"), V("rocket", "Rocket"), V("parachute", "Parachute"), V("extinguisher", "Fire extinguisher"), V("first_aid", "First aid kit"), V("crystal_ball", "Crystal ball (for jokes only)"), V("hourglass", "Hourglass"), V("clock", "Clock"), V("stopwatch", "Stopwatch"), V("calendar", "Calendar"),
    V("briefcase", "Briefcase"), V("umbrella", "Umbrella, black", ramp=BLACK, ramp2=BLACK), V("anchor", "Anchor"), V("float", "Life ring", ramps=[CRIMSON, SNOW]), V("shield", "Shield", ramp=NAVY, emblem=GOLD), V("rolodex", "Rolodex"), V("trophy", "Trophy"), V("medal", "Medal"), V("duck", "Debugging duck"), V("coffee_cup", "Desk coffee"), V("paper_plane", "Paper plane"),
],
}
PROP_IDS = []
for code, _ in FAMILIES:
    for i, _ in enumerate(FAMILY_ITEMS[code]): PROP_IDS.append((f"PROP-{len(PROP_IDS) + 1:03d}", code, i))
PROP_INDEX = {pid: (code, i) for pid, code, i in PROP_IDS}
def ids(code=None): return [pid for pid, c, i in PROP_IDS if code is None or c == code]
def entry(pid):
    code, i = PROP_INDEX[pid]; return FAMILY_ITEMS[code][i]
def frames(pid):
    d, p, _ = entry(pid); return render(d, p)
def still(pid):
    d, p, _ = entry(pid); fr, _ = render(d, p); return fr[DRAW[d]["still"]]
def title(pid): return entry(pid)[2]
def at(pid, t):
    fr, tk = frames(pid); total = sum(tk); u = (t * 10) % total; acc = 0
    for im, k in zip(fr, tk):
        acc += k
        if u < acc: return im
    return fr[-1]
