"""DESK · Desk & office. Desk items 24 px, hand-held items 16 px, floor items 32-48 px, next to the ~45 px mascot.
Method (rec-marketing-pixel-art): hand-drawn grids at final size, 3-4 tone hue-shifted ramps shared across the set,
light from the top-left, sel-out outlines in each material's own darkest tone (never black), chunky highlights on shiny
things. The boss asked for the whole office board to move: every item has a small loop, each frame its own drawing
(full grids, hand-drawn part poses layered with stamp(), or pixel overrides). Calculator, ID badge and whiteboards carry
no digits, letters or words. Mugs, coffee pot and water bottles live in FOOD (lib/food_drinks.py)."""
from lib import sprite
from lib.food import FROST_PINK

# ---- shared ramps (outline, shadow, base, light[, highlight]) ------------------------------------------------------------
SHELL = {  # painted metal / plastic shells: lamps, stapler, folders, notebooks, backpacks
    "red":   {"K": "#5e1426", "k": "#a8243a", "c": "#de4048", "C": "#ff7a68"},
    "lime":  {"K": "#34461a", "k": "#6c8a22", "c": "#a8c83a", "C": "#e2f27a"},
    "blue":  {"K": "#1c2e5e", "k": "#3456a0", "c": "#4f86cf", "C": "#8cc2f0"},
    "ink":   {"K": "#1e1c2c", "k": "#34324a", "c": "#4e4c66", "C": "#7c7a96"},
    "manila":{"K": "#6a4318", "k": "#b87a2a", "c": "#e0a945", "C": "#fbd77a"},
    "brown": {"K": "#3e1e14", "k": "#6e3a22", "c": "#9c5a34", "C": "#c8844c"},
    "yellow":{"K": "#7a5212", "k": "#d29a22", "c": "#f6cf3e", "C": "#fff19a"},
    "pink":  {"K": "#7d2f5f", "k": "#c04f87", "c": "#ee82b0", "C": "#ffc8dc"},
}
METAL = {"A": "#3e4256", "a": "#7d8299", "i": "#bfc4d4", "I": "#f2f4fa"}
PAPERS = {"O": "#5b4f63", "o": "#b9b0bb", "p": "#ece6e0", "P": "#fffbf2"}          # outline, shadow, sheet, lit
CLAY = {"M": "#4e1f14", "m": "#8e3c1e", "n": "#c8642c", "N": "#f09a52"}
POT_BLUE = {"M": "#1c2e5e", "m": "#3456a0", "n": "#4f86cf", "N": "#8cc2f0"}
LEAF = {"G": "#1f4630", "g": "#2f7a3a", "e": "#4fa83e", "E": "#9ad65a"}
CACTUS = {"H": "#1e4436", "h": "#2f7050", "v": "#4a9e5e", "V": "#8ccf6e", "w": "#f4f0d0"}
BULB = {"o": "#b87a2a", "y": "#ffd86a", "Y": "#fff8d8"}
INK = {"x": "#2c3a8c", "X": "#c8364a", "z": "#2f8a4a"}      # marker / pen inks: blue, red, green


def blank(w, h): return ["." * w for _ in range(h)]

def stamp(grid, part, x0, y0):
    """Layer a hand-drawn part onto a grid ('.' in the part is transparent). Parts are separate drawings per pose
    (skill section 10, layered parts); this only places them, it never scales or rotates."""
    g = [list(r) for r in grid]
    for dy, row in enumerate(part):
        for dx, ch in enumerate(row):
            x, y = x0 + dx, y0 + dy
            if ch != "." and 0 <= y < len(g) and 0 <= x < len(g[0]): g[y][x] = ch
    return ["".join(r) for r in g]

def recolor(grid, mapping):
    return ["".join(mapping.get(c, c) for c in r) for r in grid]


# ======================================================================================================================
# DESK LAMP (24) - head bobs (nod down, back up), bulb flickers once
# ======================================================================================================================
LAMP = [
    "........................",
    "........................",
    "..............KKKK......",
    ".............KCCckK.....",
    "..........aAKCCccckK....",
    ".........aAKCcccccckK...",
    "........aAKCcccccccckK..",
    ".......aA.KccccccccckK..",
    "......aA..KkkkkkkkkkkK..",
    ".....aA.....oYYYyyo.....",
    "...KCcK......oyyyo......",
    "...KckK.......ooo.......",
    "....KK..................",
    "......aA................",
    ".......aA...............",
    "........aA..............",
    ".........aA.............",
    "..........aA............",
    "..........KCkK..........",
    "......KCCCcccccckkK.....",
    ".....KCCcccccccckkkK....",
    ".....KckkkkkkkkkkkkK....",
    "......KKKKKKKKKKKKK.....",
    "........................",
]
def _lamp_nod(g):
    """Head drawn one pixel lower and leaning forward: the shade's top row squashes in, the arm bends to meet it."""
    rows = [list(r) for r in g]
    out = [list(r) for r in g]
    for y in range(2, 12):
        for x in range(10, 24):
            if rows[y][x] in "KkcCYyo": out[y][x] = "."
    for y in range(2, 12):
        for x in range(10, 24):
            if rows[y][x] in "KkcCYyo": out[y + 1][x] = rows[y][x]
    out[4][10] = "."; out[4][11] = "."; out[5][11] = "A"
    out[3][14] = "."; out[3][17] = "."           # cap squashes on the nod
    out[4][14] = "K"; out[4][17] = "K"; out[4][15] = "C"; out[4][16] = "c"
    return ["".join(r) for r in out]
LAMP_NOD = _lamp_nod(LAMP)
LAMP_DIM = {(13, 9): "y", (14, 9): "y", (15, 9): "y", (16, 9): "o", (17, 9): "o", (14, 10): "o", (15, 10): "y", (16, 10): "o"}
for sid, title, shell, old in [("DESK-LAMP-RED", "Desk lamp, red", "red", ["PROP-013"]),
                               ("DESK-LAMP-LIME", "Desk lamp, lime", "lime", ["PROP-014"])]:
    sprite(sid, title, "Desk", {**SHELL[shell], **METAL, **BULB}, LAMP,
           frames=[None, LAMP_NOD, None, LAMP_DIM, None], ticks=[10, 4, 6, 1, 6], old=old)


# ======================================================================================================================
# POTTED PLANT and CACTUS (24) - they dance: lean left, centre, lean right, squash on the beat; the pot stays planted
# ======================================================================================================================
POT = [  # rows 14..23
    ".....MNNnnnnnnnnnmM.....",
    ".....MnnnnnnnnnnmmM.....",
    "......MmmmmmmmmmmM......",
    "......MNNnnnnnnmmM......",
    "......MNNnnnnnnmmM......",
    "......MNnnnnnnnmmM......",
    "......MNnnnnnnnmmM......",
    ".......MNnnnnnmmM.......",
    ".......MnnnnnnmmM.......",
    "........MMMMMMMM........",
]
LEAVES = {
    "rest": [
        "........................",
        ".........ggggGG.........",
        "........gEEEeeeG........",
        "........gEEeeeeG........",
        ".......gEEeeeeegG.......",
        "........geeeeggG........",
        ".....ggggGGegggggGG.....",
        "....gEEEeeGGggEEeeeG....",
        "...gEEEeeeeGgEEeeeeGG...",
        "...gEEeeeegggGeeeeegG...",
        "...gEeeeegEEeeGeeeggG...",
        "....GeeeggEeeeGGeggG....",
        ".....GGggGeeegGggGG.....",
        "......GGGGGGGGGGGG......",
    ],
    "left": [
        "........................",
        "........ggggGG..........",
        ".......gEEEeeeG.........",
        ".......gEEeeeeG.........",
        "......gEEeeeeegG........",
        ".......geeeeggG.........",
        "....ggggGGeggggggGG.....",
        "...gEEEeeGGggEEEeeGG....",
        "...gEEeeeeegEEEeeeeG....",
        "...gEeeeegggGGeeeegG....",
        "...geeeeggEeeGGeeggG....",
        "...GGeeegEeeeeGeggGG....",
        "....GGeggGeeggGggGG.....",
        "......GGGGGGGGGGGG......",
    ],
    "right": [
        "........................",
        "..........ggggGG........",
        ".........gEEEeeeG.......",
        ".........gEEeeeeG.......",
        "........gEEeeeeegG......",
        ".........geeeeggG.......",
        ".....ggggGGeegggggGG....",
        "....gEEEeeGGgEEEeeeGG...",
        "....gEEeeeeegEEEeeeeG...",
        "....gEeeeegggGGeeeegG...",
        "....geeeeggEeeGGeeggG...",
        "....GGeeegEeeeeGeggGG...",
        ".....GGegGeeegGGggGG....",
        "......GGGGGGGGGGGG......",
    ],
    "squash": [
        "........................",
        "........................",
        "........................",
        "........ggggGGGG........",
        ".......gEEEEeeeGG.......",
        ".......gEEeeeeegG.......",
        ".......gEeeeeeggG.......",
        "....ggggGGGeggggggGG....",
        "...gEEEeeeGGggEEEeeeG...",
        "..gEEEeeeeeGgEEeeeeeGG..",
        "..geeeeeegggGGGeeeegGG..",
        "...GeeeeggEeeeGGeeggG...",
        "...GGGeggGeeegGGggGGG...",
        "......GGGGGGGGGGGG......",
    ],
}
DANCE = ["left", "rest", "right", "squash"]
DANCE_TICKS = [4, 2, 4, 3]
for sid, title, pot, old in [("DESK-PLANT", "Desk plant", CLAY, ["PROP-015"]),
                             ("DESK-PLANT-BLUE", "Desk plant, blue pot", POT_BLUE, ["PROP-016"])]:
    fr = [LEAVES[k] + POT for k in DANCE]
    sprite(sid, title, "Plants", {**LEAF, **pot}, fr[1], frames=fr, ticks=DANCE_TICKS, old=old)

CACTI = {
    "rest": [
        "........................",
        "...........HH...........",
        "..........HVvH..........",
        ".........HVVvhH.........",
        ".....HH..HVvvhH.........",
        "....HVvH.HVvvhH.........",
        "....HVvH.HVwvhH..HH.....",
        "....HVhH.HVvvhH.HVhH....",
        "....HwhH.HVvvhH.HVhH....",
        "....HVvHHHVvvhH.HwhH....",
        "....HVvVVVVvvhHHHVhH....",
        "....HvhhhVVvvhvvvVhH....",
        ".....HHHHHVvvhhhhhhH....",
        ".........HVvvhHHHHH.....",
    ],
    "left": [
        "........................",
        "..........HH............",
        ".........HVvH...........",
        ".....HH..HVVvhH.........",
        "....HVvH.HVvvhH.........",
        "....HVvH.HVvvhH.........",
        "....HwhH.HVwvhH.........",
        "....HVhH.HVvvhH..HH.....",
        "....HVvH.HVvvhH.HVhH....",
        "....HVvHHHVvvhH.HwhH....",
        "....HVvVVVVvvhHHHVhH....",
        "....HvhhhVVvvhvvvVhH....",
        ".....HHHHHVvvhhhhhhH....",
        ".........HVvvhHHHHH.....",
    ],
    "right": [
        "........................",
        "............HH..........",
        "...........HVvH.........",
        ".........HVVvhH.........",
        ".........HVvvhH.........",
        ".........HVvvhH..HH.....",
        ".....HH..HVwvhH.HVvH....",
        "....HVvH.HVvvhH.HVhH....",
        "....HwhH.HVvvhH.HVhH....",
        "....HVvHHHVvvhH.HwhH....",
        "....HVvVVVVvvhHHHVhH....",
        "....HvhhhVVvvhvvvVhH....",
        ".....HHHHHVvvhhhhhhH....",
        ".........HVvvhHHHHH.....",
    ],
    "squash": [
        "........................",
        "........................",
        "..........HHHH..........",
        ".........HVVvhH.........",
        "....HH...HVvvhH.........",
        "...HVvH..HVwvhH...HH....",
        "...HVhH..HVvvhH..HVvH...",
        "...HwhH..HVvvhH..HVhH...",
        "...HVvHHHHVvvhH..HwhH...",
        "...HVvVVVVVvvhHHHHVhH...",
        "...HvhhhhVVvvhvvvvVhH...",
        "....HHHHHHVvvhhhhhhhH...",
        ".........HVvvhHHHHHH....",
        ".........HVvvhH.........",
    ],
}
BLOOM = {  # flower on the tip of each pose
    "rest":   {(10, 0): "P", (11, 0): "q", (12, 0): "Q", (13, 0): "P", (11, 1): "p", (12, 1): "P"},
    "left":   {(9, 0): "P", (10, 0): "q", (11, 0): "Q", (12, 0): "P", (10, 1): "p", (11, 1): "P"},
    "right":  {(11, 0): "P", (12, 0): "q", (13, 0): "Q", (14, 0): "P", (12, 1): "p", (13, 1): "P"},
    "squash": {(10, 1): "P", (11, 1): "q", (12, 1): "Q", (13, 1): "P", (11, 2): "p", (12, 2): "P"},
}
def _bloom(g, pts):
    g = [list(r) for r in g]
    for (x, y), ch in pts.items(): g[y][x] = ch
    return ["".join(r) for r in g]
fr = [CACTI[k] + POT for k in DANCE]
sprite("DESK-CACTUS", "Cactus", "Plants", {**CACTUS, **CLAY}, fr[1], frames=fr, ticks=DANCE_TICKS, old=["PROP-017"])
fr = [_bloom(CACTI[k], BLOOM[k]) + POT for k in DANCE]
sprite("DESK-CACTUS-BLOOM", "Cactus in bloom", "Plants", {**CACTUS, **CLAY, **FROST_PINK}, fr[1], frames=fr,
       ticks=DANCE_TICKS, old=["PROP-018"])


# ======================================================================================================================
# NOTEBOOKS (24) - spiral-bound, blank label; the ribbon bookmark sways
# ======================================================================================================================
NOTEBOOK = [
    "........................",
    "......KKKKKKKKKKKKK.....",
    "......KCCCCCCCCCCkK.....",
    "....iaKCccccccccckK.....",
    "....A.KCccccccccckK.....",
    "....iaKCcPPPPPPockK.....",
    "....A.KCcPooooPockK.....",
    "....iaKCcPPPPPPockK.....",
    "....A.KCcooooooockK.....",
    "....iaKCccccccccckK.....",
    "....A.KCccccccccckK.....",
    "....iaKCccccccccckK.....",
    "....A.KCccccccccckK.....",
    "....iaKCccccccccckK.....",
    "....A.KCccccccccckK.....",
    "....iaKCccccccccckK.....",
    "....A.KCccccccccckK.....",
    "....iaKCccccccccckK.....",
    "....A.KCccccccccckK.....",
    "....iaKCccccccccckK.....",
    "....A.KCckkkkkkkkkK.....",
    "......KkkkkkkkkkkkK.....",
    "......KKKKKKKKrKKKK.....",
    "..............rR........",
]
RIBBON_SWAY = {(14, 23): "R", (13, 23): "r", (15, 23): "."}
RIBBON = {"r": "#ffd86a", "R": "#b87a2a"}
for sid, title, shell, old in [("DESK-NOTEBOOK-BLUE", "Notebook, blue", "blue", ["PROP-019"]),
                               ("DESK-NOTEBOOK-RED", "Notebook, red", "red", ["PROP-020"]),
                               ("DESK-NOTEBOOK-LIME", "Notebook, lime", "lime", ["PROP-021"])]:
    sprite(sid, title, "Paper", {**SHELL[shell], **METAL, **PAPERS, **RIBBON}, NOTEBOOK,
           frames=[None, RIBBON_SWAY, None, RIBBON_SWAY], ticks=[8, 6, 9, 5], old=old)


# ======================================================================================================================
# PENS and PENCIL (16) - a glint runs down the barrel
# ======================================================================================================================
PEN = [
    "................",
    "............KK..",
    "...........KCcK.",
    "..........KicK..",
    ".........KicK...",
    "........KicK....",
    ".......KCcK.....",
    "......KCcK......",
    ".....KCcK.......",
    "....KCcK........",
    "...KkkK.........",
    "..AiaA..........",
    ".AaA............",
    "xA..............",
    "................",
    "................",
]
PENCIL = [
    "................",
    "............PP..",
    "...........PQqP.",
    "..........AiaA..",
    ".........AiaA...",
    "........KCcK....",
    ".......KCcK.....",
    "......KCcK......",
    ".....KCcK.......",
    "....KCcK........",
    "...DBbD.........",
    "..DBbD..........",
    ".DbD............",
    "TD..............",
    "................",
    "................",
]
GLINT = [None, {(8, 6): "I", (7, 7): "I"}, {(7, 7): "I", (6, 8): "I"}, {(6, 8): "I", (5, 9): "I"}]
for sid, title, shell, ink, old in [("DESK-PEN-BLUE", "Pen, blue", "blue", "#2c3a8c", ["PROP-022"]),
                                    ("DESK-PEN-BLACK", "Pen, black", "ink", "#1e1c2c", ["PROP-023"])]:
    sprite(sid, title, "Desk", {**SHELL[shell], **METAL, "x": ink}, PEN, frames=GLINT, ticks=[18, 1, 1, 1], old=old)
DOUGH_ = {"D": "#6b3a1f", "b": "#d89a52", "B": "#f2c47e", "T": "#3e4256"}
sprite("DESK-PENCIL", "Pencil", "Desk", {**SHELL["yellow"], **METAL, **FROST_PINK, **DOUGH_}, PENCIL,
       frames=GLINT, ticks=[20, 1, 1, 1], old=["PROP-024"])


# ======================================================================================================================
# STICKY NOTES (16) - the free corner curls up and flutters (each curl is redrawn: the corner is cut off along the fold
# and its back is drawn folded over, lighter)
# ======================================================================================================================
STICKY = [
    "................",
    ".KKKKKKKKKKKKKK.",
    ".KCCCCCCCCCCCkK.",
    ".KCcccccccccckK.",
    ".KCcccccccccckK.",
    ".KCckkkcckkcckK.",
    ".KCcccccccccckK.",
    ".KCcccccccccckK.",
    ".KCckkcckkkcckK.",
    ".KCcccccccccckK.",
    ".KCcccccccccckK.",
    ".KCcccccccccckK.",
    ".KCcccccccccckK.",
    ".KkkkkkkkkkkkkK.",
    ".KKKKKKKKKKKKKK.",
    "................",
]
def curl(grid, t):
    """Fold the bottom-right corner up along the line x + y = t: cut it off, draw its back folded over (C, edged k)."""
    g = [list(r) for r in grid]; n = len(g)
    cut = [(x, y) for y in range(n) for x in range(n) if x + y > t and g[y][x] != "."]
    for x, y in cut: g[y][x] = "."
    flap = {(t - y, t - x) for x, y in cut}
    for x, y in flap:
        if 0 <= x < n and 0 <= y < n: g[y][x] = "P"
    for x, y in flap:
        edge = any((x + dx, y + dy) not in flap and x + dx + y + dy <= t for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1)))
        if edge and 0 <= x < n and 0 <= y < n: g[y][x] = "k"
    for y in range(n):       # the fold line itself, a crisp dark crease
        x = t - y
        if 0 <= x < n and g[y][x] in "Pk": g[y][x] = "K"
    return ["".join(r) for r in g]
for sid, title, shell, t0, old in [("DESK-STICKY", "Sticky note", "yellow", 24, ["PROP-025"]),
                                   ("DESK-STICKY-PINK", "Sticky note, pink", "pink", 24, ["PROP-026"]),
                                   ("DESK-STICKY-PEEL", "Sticky note, peeling", "lime", 22, ["PROP-027"])]:
    pal = {**SHELL[shell], "P": SHELL[shell]["C"]}
    pal["P"] = {"yellow": "#fffbe0", "pink": "#ffe6ef", "lime": "#f4fbc8"}[shell]
    sprite(sid, title, "Paper", pal, curl(STICKY, t0),
           frames=[curl(STICKY, t0), curl(STICKY, t0 - 1), curl(STICKY, t0 - 2), curl(STICKY, t0 - 1)],
           ticks=[12, 2, 3, 2], old=old)


# ======================================================================================================================
# STAPLER (24x16) - chomps: the arm hinges down at the nose
# ======================================================================================================================
STAPLER = [
    "........................",
    "........................",
    "........................",
    "........................",
    "....KKKKKKKKKKKKKKK.....",
    "..KKCCCCCCCCCCCCCCCKK...",
    ".KCCcccccccccccccccckK..",
    ".KkkkkkkkkkkkkkkkkkkkK..",
    "..KKKKKKKKKKKKKKKKKKKK..",
    "...AiiiiiiiiiiiiiaAiA...",
    "..DDDDDDDDDDDDDDDDDDDDD.",
    ".DBBBBBBBBBBBBBBBBBBBbD.",
    ".DbbbbbbbbbbbbbbbbbbbbD.",
    "..DDDDDDDDDDDDDDDDDDDD..",
    "........................",
    "........................",
]
STAPLER_CHOMP = STAPLER[:4] + [
    "........KKKKKKKKKKK.....",
    "....KKKKCCCCCCCCCCCKK...",
    "..KKCCCCcccccccccccckK..",
    ".KCCcccckkkkkkkkkkkkkK..",
    ".KkkkkkkKKKKKKKKKKKKKK..",
    "..KKKKKKiiiiiiiiiaAiA...",
] + STAPLER[10:]
BASE_INK = {"D": "#1e1c2c", "d": "#34324a", "b": "#4e4c66", "B": "#7c7a96"}
sprite("DESK-STAPLER", "Stapler", "Desk", {**SHELL["red"], **METAL, **BASE_INK}, STAPLER,
       frames=[None, STAPLER_CHOMP, None], ticks=[14, 2, 4], old=["PROP-028"])


# ======================================================================================================================
# SCISSORS (16) - snip: open, shut
# ======================================================================================================================
RING = [".KKKK.", "KC..kK", "Kc..kK", ".KkkK."]       # finger loop, 2x2 hole
SCISSORS_OPEN = stamp(stamp([
    "............iA..",
    "...........iA...",
    "...........iA.iA",
    "..........iA.iA.",
    "..........iAiA..",
    ".........iAiA...",
    ".........iIaA...",
    "........AIaA....",
    ".......KkAK.....",
    "......KkKcK.....",
    "......K..KcK....",
    "................",
    "................",
    "................",
    "................",
    "................",
], RING, 1, 9), RING, 7, 11)
SCISSORS_SHUT = stamp(stamp([
    "..............iA",
    ".............iIA",
    "............iIaA",
    "...........iIaA.",
    "..........iIaA..",
    ".........iIaA...",
    "........iIaA....",
    ".......AIaA.....",
    "......KkAK......",
    ".....KkKcK......",
    ".....K..KcK.....",
    "................",
    "................",
    "................",
    "................",
    "................",
], RING, 1, 9), RING, 6, 11)
sprite("DESK-SCISSORS", "Scissors", "Desk", {**SHELL["red"], **METAL}, SCISSORS_OPEN,
       frames=[SCISSORS_OPEN, SCISSORS_SHUT, SCISSORS_OPEN, SCISSORS_SHUT], ticks=[10, 2, 2, 2], old=["PROP-029"])


# ======================================================================================================================
# CALCULATOR (16x20, blank) - keys get pressed, the screen stays blank
# ======================================================================================================================
CALC = [
    "..DDDDDDDDDDDD..",
    ".DBBBBBBBBBBBdD.",
    ".DBSSSSSSSSSSdD.",
    ".DBSTTssssssSdD.",
    ".DBSTsssssssSdD.",
    ".DBSSSSSSSSSSdD.",
    ".DBbbbbbbbbbbdD.",
    ".DBbiibiibiibdD.",
    ".DBbaAbaAbaAbdD.",
    ".DBbbbbbbbbbbdD.",
    ".DBbiibiibiibdD.",
    ".DBbaAbaAbaAbdD.",
    ".DBbbbbbbbbbbdD.",
    ".DBbiibiibiibdD.",
    ".DBbaAbaAbaAbdD.",
    ".DBbbbbbbbbbbdD.",
    ".DBbiibiibyybdD.",
    ".DBbaAbaAboobdD.",
    ".DddddddddddddD.",
    "..DDDDDDDDDDDD..",
]
SCREEN = {"S": "#3e5a46", "s": "#a8c8a0", "T": "#e0f0c8"}
def _press(x, y, top="a", bot="A"): return {(x, y): top, (x + 1, y): top, (x, y + 1): bot, (x + 1, y + 1): bot}
sprite("DESK-CALCULATOR", "Calculator (blank)", "Desk", {**BASE_INK, **METAL, **SCREEN, **BULB}, CALC,
       frames=[None, _press(7, 10), None, _press(4, 13), None, _press(10, 16, "o", "o")], ticks=[8, 2, 3, 2, 6, 2],
       old=["PROP-030"])


# ======================================================================================================================
# STACK OF PAPER (24x16) - the loose top sheet rustles (slides a pixel and its lifted corner flips)
# ======================================================================================================================
PAPER_STACK = [
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    ".OPpppppppppppppppppoO..",
    ".OooooooooooooooooooooO.",
    ".OPppppppppppppppppppoO.",
    "..OoooooooooooooooooooO.",
    ".OPpppppppppppppppppoO..",
    ".OooooooooooooooooooooO.",
    "..OOOOOOOOOOOOOOOOOOOO..",
    "........................",
]
TOP_SHEET = [
    "......OOOOOOOOOOOOOOO",
    ".....OPPPPPPPPPPPPPpO",
    "....OPPPPPPPPPPPPPPpO",
    "...OPPPPPPPPPPPPPPPpO",
    "..OPPPPPPPPPPPPPPPppO",
    ".OOOOOOOOOOOOOOOOOOOO",
]
TOP_SHEET_LIFT = [   # front-left corner lifted off the stack
    "......OOOOOOOOOOOOOOO",
    ".....OPPPPPPPPPPPPPpO",
    "..OOOPPPPPPPPPPPPPPpO",
    ".OPPPPPPPPPPPPPPPPPpO",
    "..OOPPPPPPPPPPPPPPppO",
    "....OOOOOOOOOOOOOOOOO",
]
PAPER_STACK_REST = stamp(PAPER_STACK, TOP_SHEET, 0, 3)
sprite("DESK-PAPER-STACK", "Stack of paper", "Paper", PAPERS, PAPER_STACK_REST,
       frames=[None, stamp(PAPER_STACK, TOP_SHEET_LIFT, 0, 3), stamp(PAPER_STACK, TOP_SHEET, 1, 3), None],
       ticks=[14, 2, 2, 3], old=["PROP-034"])


# ======================================================================================================================
# FOLDERS (24x20) - the front cover falls open a little and swings back, papers peek out
# ======================================================================================================================
FOLDER_BACK = [
    "........................",
    "........................",
    "...KKKKKK...............",
    "..KCCCCCCK..............",
    "..KCcccccKKKKKKKKKKKK...",
    "..KCccccccccccccccckK...",
    "..KCcOOOOOOOOOOOOOckK...",
    "..KCcOPPPPPPPPPPPpOkK...",
    "..KCcOPPPPPPPPPPPpOkK...",
    "..KCcOPPPPPPPPPPPpOkK...",
    "..KCcOPPPPPPPPPPPpOkK...",
    "..KCcOPPPPPPPPPPPpOkK...",
    "..KCcOPPPPPPPPPPPpOkK...",
    "..KCcOPPPPPPPPPPPpOkK...",
    "..KCcOPPPPPPPPPPPpOkK...",
    "..KCcOPPPPPPPPPPPpOkK...",
    "..KCcOPPPPPPPPPPPpOkK...",
    "..KCcOPPPPPPPPPPPpOkK...",
    "..KKKKKKKKKKKKKKKKKKK...",
    "........................",
]
FRONT = [  # front cover, 13 rows
    ".KKKKKKKKKKKKKKKKKKKKK.",
    "KCCCCCCCCCCCCCCCCCCCCkK",
    "KCcccccccccccccccccccKK",
    "KCcccccccccccccccccckK.",
    "KCcccccccccccccccccckK.",
    "KCcccccccccccccccccckK.",
    "KCcccccccccccccccccckK.",
    "KCcccccccccccccccccckK.",
    "KCcccccccccccccccccckK.",
    "KCcccccccccccccccccckK.",
    "KCcccccccccccccccccckK.",
    "KkkkkkkkkkkkkkkkkkkkkK.",
    "KKKKKKKKKKKKKKKKKKKKKK.",
]
FRONT_OPEN = [  # tipped forward: foreshortened two rows, top edge pushed out and lit
    "KKKKKKKKKKKKKKKKKKKKKKK",
    "KCCCCCCCCCCCCCCCCCCCCCK",
    "KCcccccccccccccccccccKK",
    "KCcccccccccccccccccckK.",
    "KCcccccccccccccccccckK.",
    "KCcccccccccccccccccckK.",
    "KCcccccccccccccccccckK.",
    "KCcccccccccccccccccckK.",
    "KCcccccccccccccccccckK.",
    "KkkkkkkkkkkkkkkkkkkkkK.",
    "KKKKKKKKKKKKKKKKKKKKKK.",
]
FOLDER = stamp(FOLDER_BACK, FRONT, 1, 7)
for sid, title, shell, old in [("DESK-FOLDER", "Folder", "manila", ["PROP-035"]),
                               ("DESK-FOLDER-RED", "Folder, red", "red", ["PROP-036"])]:
    sprite(sid, title, "Paper", {**SHELL[shell], **PAPERS}, FOLDER,
           frames=[None, stamp(FOLDER_BACK, FRONT, 1, 8)[:19] + [FOLDER[19]], stamp(FOLDER_BACK, FRONT_OPEN, 1, 9),
                   stamp(FOLDER_BACK, FRONT, 1, 8)[:19] + [FOLDER[19]]],
           ticks=[14, 2, 5, 2], old=old)


# ======================================================================================================================
# TRASH CAN (24) - the lid bobs; the full one is stuffed so the lid rides on crumpled paper
# ======================================================================================================================
LID = [
    "..........AAAA..........",
    "..........A..A..........",
    "......AAAAAAAAAAAA......",
    ".....AIiiiiiiiiiaaA.....",
    "....AiiaaaaaaaaaaaaA....",
    "....AAAAAAAAAAAAAAAA....",
]
CAN = [
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    "........................",
    ".....AddddddddddddA.....",
    ".....AiIiAiiaAaaaaA.....",
    ".....AiIiAiiaAaaaaA.....",
    ".....AiIiAiiaAaaaaA.....",
    ".....AiIiAiiaAaaaaA.....",
    ".....AiIiAiiaAaaaaA.....",
    ".....AiIiAiiaAaaaaA.....",
    ".....AiIiAiiaAaaaaA.....",
    "......AIiAiiaAaaaA......",
    "......AIiAiiaAaaaA......",
    "......AIiAiiaAaaaA......",
    "......AIiAiiaAaaaA......",
    "......AiiAaaaAaaAA......",
    "......AAAAAAAAAAAA......",
    "........................",
    "........................",
]
CAN_FULL = stamp(CAN, [
    ".......OOO....OOO.......",
    "......OPPpO..OPPpO......",
    ".....AOPpoOOOPpPoOA.....",
], 0, 6)
TRASH_METAL = {**METAL, "d": "#262838"}
sprite("DESK-TRASH", "Trash can", "Office furniture", TRASH_METAL, stamp(CAN, LID, 0, 3),
       frames=[stamp(CAN, LID, 0, 3), stamp(CAN, LID, 0, 2), stamp(CAN, LID, 0, 1), stamp(CAN, LID, 0, 2)],
       ticks=[16, 2, 3, 2], old=["PROP-037"])
sprite("DESK-TRASH-FULL", "Trash can, full", "Office furniture", {**TRASH_METAL, **PAPERS}, stamp(CAN_FULL, LID, 0, 0),
       frames=[stamp(CAN_FULL, LID, 0, 0), stamp(CAN_FULL, LID, 0, 1), stamp(CAN_FULL, LID, 0, 0), stamp(CAN_FULL, LID, 0, 1)],
       ticks=[8, 2, 5, 2], old=["PROP-038"])


# ======================================================================================================================
# GLOBE (24) - spins: eight hand-placed longitudes on the same sphere (the land moves, the shading stays put)
# ======================================================================================================================
GLOBE_STAND = [
    "...........iaAA.........",
    "..............aA........",
    "................aA......",
    ".................aA.....",
    "..................aA....",
    "...................aA...",
    "....................aA..",
    "....................aA..",
    "....................aA..",
    "....................aA..",
    "....................aA..",
    "....................aA..",
    "...................aA...",
    "..................aA....",
    ".................aA.....",
    "...............aaA......",
    "...........iAaaA........",
    "...........iA...........",
    "...........iA...........",
    ".......KKKKKKKKKK.......",
    "......KCCCcccccckK......",
    "......KkkkkkkkkkkK......",
    ".......KKKKKKKKKK.......",
    "........................",
]
GLOBE_SPIN = [
    [
        "........................",
        ".........wwwww..........",
        ".......gwwwwwwgN........",
        "......lbbwwwwwwwN.......",
        ".....gbbwwwwwwwwwN......",
        ".....gbwwwwwwwwwwG......",
        "....gwwwwwwwwwwwwWN.....",
        "....gwwwwwwwwwwwwWN.....",
        "....ggwwwwwwwwwwWWN.....",
        "....wgwwwwwwwwwWWWN.....",
        "....ggwwwwwwwwWWWWN.....",
        ".....ggwwwwwwWWWWW......",
        ".....NgwwwwwWWWWWN......",
        "......NwwwwWWWWWN.......",
        ".......NWWWWWWWN........",
        ".........NNNNN..........",
        "........................",
    ],
    [
        "........................",
        ".........wwggg..........",
        ".......wwwwggggN........",
        "......bbbwwgggggN.......",
        ".....wbbwwwwwggggN......",
        ".....wbwwwwwwggggW......",
        "....wwwwwwwwwwgggGN.....",
        "....wwwwwwwwwwwwgGN.....",
        "....wwwwwwwwwwwwWGN.....",
        "....wwwwwwwwwwwWWGN.....",
        "....wwwwwwwwwwWWWWN.....",
        ".....wwwwwwwwWWWWG......",
        ".....NwwwwwwWWWWWN......",
        "......NwwwwWWWWWN.......",
        ".......NWWWWWWWN........",
        ".........NNNNN..........",
        "........................",
    ],
    [
        "........................",
        ".........ggggw..........",
        ".......wgggggwwN........",
        "......bllggggwwwN.......",
        ".....wbbgggggwwwwN......",
        ".....wbwgggggwwwwW......",
        "....wwwwwgggggwwwWN.....",
        "....wwwwwwgggwwwwWN.....",
        "....wwwwwwwgggggGWN.....",
        "....wwwwwwwggggGGWN.....",
        "....wwwwwwwwwgGGGWN.....",
        ".....wwwwwwwwGGWWW......",
        ".....NwwwwwwWGGWWN......",
        "......NwwwwGGGWWN.......",
        ".......NWWWGWWWN........",
        ".........NNNNN..........",
        "........................",
    ],
    [
        "........................",
        ".........gwwwg..........",
        ".......gggwwgggN........",
        "......llbwwwwwggN.......",
        ".....gllwwwwwwwggN......",
        ".....glgwwwwwwwggG......",
        "....wggggwwwwwwwgGN.....",
        "....wggwwwwwwwwwwGN.....",
        "....wwgggggwwwwwWGN.....",
        "....wwgggggwwwwWWGN.....",
        "....wwwggggwwwWWWGN.....",
        ".....wwwggwwwWWWGG......",
        ".....NwwggwwWWWWGN......",
        "......NggwwWWWWWN.......",
        ".......NGWWWWWWN........",
        ".........NNNNN..........",
        "........................",
    ],
    [
        "........................",
        ".........wgggg..........",
        ".......wwggggggN........",
        "......bbbgggggggN.......",
        ".....wbbwwgggggwwN......",
        ".....wbwwwgggggwwW......",
        "....gwwwwwgggggggWN.....",
        "....wwwwwwwggggggWN.....",
        "....ggwwwwwgggggGWN.....",
        "....ggwwwwwggggGGWN.....",
        "....ggwwwwwgggWWWWN.....",
        ".....gwwwwwggGWWWW......",
        ".....NwwwwwgGGWWWN......",
        "......NwwwwWWGWWN.......",
        ".......NWWWWWWWN........",
        ".........NNNNN..........",
        "........................",
    ],
    [
        "........................",
        ".........ggggg..........",
        ".......gggggggwN........",
        "......lllggggwggN.......",
        ".....wllggwwwwgggN......",
        ".....wlgggwwwwgggG......",
        "....wggggggwwwwwgGN.....",
        "....wwgggggwwwwwwGN.....",
        "....wwgggggwwwwwWWN.....",
        "....wwgggggwwwwWWWN.....",
        "....wwgggwwwwwWWWWN.....",
        ".....wwggwwwwWWWGG......",
        ".....NwggwwwWWWWGN......",
        "......NwgwwWWWWWN.......",
        ".......NWWWWWWWN........",
        ".........NNNNN..........",
        "........................",
    ],
    [
        "........................",
        ".........gwggw..........",
        ".......ggggggggN........",
        "......llbgggggggN.......",
        ".....gbbwggggggwwN......",
        ".....gbwwggggggwwW......",
        "....ggwwwwggggwwwWN.....",
        "....ggwwwwwgggwwwWN.....",
        "....ggwwwwwwwwggGWN.....",
        "....ggwwwwwwwwgGGWN.....",
        "....gwwwwwwwwgGGGWN.....",
        ".....wwwwwwggGGGWW......",
        ".....NwwwwwgGGGGWN......",
        "......NwwwwWWGGWN.......",
        ".......NWWWWWWWN........",
        ".........NNNNN..........",
        "........................",
    ],
    [
        "........................",
        ".........gwwww..........",
        ".......ggggwwwwN........",
        "......lllggwwwwwN.......",
        ".....wllggwwwwwwwN......",
        ".....glgggwwwwwwwW......",
        "....wggggwwwwwwwwWN.....",
        "....wwgggwwwwwwwwWN.....",
        "....wwwwwggwwwwwWWN.....",
        "....wwwwwggwwwwWWWN.....",
        "....wwwggggwwwWWWWN.....",
        ".....wwggggwwWWWWW......",
        ".....NwggggwWWWWWN......",
        "......NwggwWWWWWN.......",
        ".......NWWWWWWWN........",
        ".........NNNNN..........",
        "........................",
    ],
]
SEA_LAND = {"N": "#1c2e5e", "W": "#3456a0", "w": "#4f86cf", "b": "#8cc2f0", "G": "#2c7044", "g": "#48a058", "l": "#8cd27a"}
GLOBE_FR = [stamp(GLOBE_STAND, f, 0, 0) for f in GLOBE_SPIN[2:] + GLOBE_SPIN[:2]]   # open on the land side
sprite("DESK-GLOBE", "Globe", "Desk", {**SEA_LAND, **METAL, **SHELL["brown"]}, GLOBE_FR[0], frames=GLOBE_FR,
       ticks=[3] * 8, old=["PROP-046"])


# ======================================================================================================================
# WHITEBOARDS (32x24) - marker strokes only: a rising zig-zag arrow, or squiggle notes. Never digits or words.
# The stroke draws itself in, holds, and is wiped.
# ======================================================================================================================
BOARD = [
    "................................",
    ".AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA.",
    ".AiiiiiiiiiiiiiiiiiiiiiiiiiiiaA.",
    ".AiWWWWWWWWWWWWWWWWWWWWWWWWWwaA.",
    ".AiWWWWWWWWWWWWWWWWWWWWWWWWWwaA.",
    ".AiWWWWWWWWWWWWWWWWWWWWWWWWWwaA.",
    ".AiWWWWWWWWWWWWWWWWWWWWWWWWWwaA.",
    ".AiWWWWWWWWWWWWWWWWWWWWWWWWWwaA.",
    ".AiWWWWWWWWWWWWWWWWWWWWWWWWWwaA.",
    ".AiWWWWWWWWWWWWWWWWWWWWWWWWWwaA.",
    ".AiWWWWWWWWWWWWWWWWWWWWWWWWWwaA.",
    ".AiWWWWWWWWWWWWWWWWWWWWWWWWWwaA.",
    ".AiWWWWWWWWWWWWWWWWWWWWWWWWWwaA.",
    ".AiWWWWWWWWWWWWWWWWWWWWWWWWWwaA.",
    ".AiWWWWWWWWWWWWWWWWWWWWWWWWWwaA.",
    ".AiWWWWWWWWWWWWWWWWWWWWWWWWWwaA.",
    ".AiwwwwwwwwwwwwwwwwwwwwwwwwwwaA.",
    ".AaaaaaaaaaaaaaaaaaaaaaaaaaaaaA.",
    ".AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA.",
    ".....Aa.XXXr..xxxq........Aa....",
    "....AiiiiiiiiiiiiiiiiiiiiiiiaA..",
    "....AAAAAAAAAAAAAAAAAAAAAAAAAA..",
    ".....Aa...................Aa....",
    ".....AA...................AA....",
]
BOARD_INK = {"W": "#f6fcff", "w": "#d8e2ee", "q": "#1a2460", "r": "#7a1a2a", **INK}

def ink(grid, pts, ch):
    g = [list(r) for r in grid]
    for x, y in pts: g[y][x] = ch
    return ["".join(r) for r in g]

def line(pts):
    """Hand-placed corner points -> the marker pixels between them (one pixel wide, no doubled corners)."""
    out = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = max(abs(x1 - x0), abs(y1 - y0))
        for i in range(n + (1 if (x1, y1) == pts[-1] else 0)):
            p = (x0 + round((x1 - x0) * i / n), y0 + round((y1 - y0) * i / n))
            if not out or out[-1] != p: out.append(p)
    return out

AXES = line([(5, 4), (5, 14), (26, 14)])
ZIG = line([(6, 13), (10, 9), (13, 12), (18, 7), (21, 9), (25, 5)])
ARROWHEAD = [(23, 5), (24, 5), (25, 5), (25, 6), (25, 7), (24, 4)]
chart = ink(BOARD, AXES, "q")
n = len(ZIG)
CHART_FR = [chart, ink(chart, ZIG[:n // 3], "X"), ink(chart, ZIG[:2 * n // 3], "X"),
            ink(ink(chart, ZIG, "X"), ARROWHEAD, "X")]
sprite("DESK-WHITEBOARD-CHART", "Whiteboard, chart", "Office furniture", {**METAL, **BOARD_INK}, CHART_FR[3],
       frames=CHART_FR[3:] + CHART_FR[:3], ticks=[24, 4, 2, 2], old=["PROP-039"])

def squiggle(x0, x1, y):
    """A handwriting-like wave: 2 px up, 2 px down - reads as notes, says nothing."""
    return [(x, y + (0 if (x - x0) % 4 < 2 else 1)) for x in range(x0, x1)]
S1, S2, S3 = squiggle(5, 21, 4), squiggle(5, 17, 8), squiggle(5, 19, 12)
CIRCLE = [(23, 9), (24, 9), (25, 9), (26, 10), (26, 11), (26, 12), (25, 13), (24, 13), (23, 13), (22, 12), (22, 11), (22, 10)]
ARROW = line([(18, 11), (21, 11)]) + [(20, 10), (20, 12)]
notes = ink(ink(ink(ink(BOARD, S1, "x"), S2, "x"), CIRCLE, "X"), ARROW, "z")
NOTES_FR = [notes, ink(notes, S3[:6], "x"), ink(notes, S3[:11], "x"), ink(notes, S3, "x")]
sprite("DESK-WHITEBOARD-NOTES", "Whiteboard, notes", "Office furniture", {**METAL, **BOARD_INK}, NOTES_FR[3],
       frames=NOTES_FR[3:] + NOTES_FR[:3], ticks=[20, 6, 2, 2], old=["PROP-040"])


# ======================================================================================================================
# BRIEFCASE (24) - the brass clasps glint
# ======================================================================================================================
BRIEFCASE = [
    "........................",
    "........................",
    "........................",
    ".........KKKKKK.........",
    "........KCccccckK.......",
    "........KcK..KkK........",
    "..KKKKKKKKKKKKKKKKKKKK..",
    ".KCCCCCCCCCCCCCCCCCCCkK.",
    ".KCcccccccccccccccccckK.",
    ".KCccccYyccccccYycccckK.",
    ".KkkkkkyokkkkkkyokkkkkK.",
    ".KCcccccccccccccccccckK.",
    ".KCcccccccccccccccccckK.",
    ".KCcccccccccccccccccckK.",
    ".KCcccccccccccccccccckK.",
    ".KCcccccccccccccccccckK.",
    ".KCcccccccccccccccccckK.",
    ".KCcccccccccccccccccckK.",
    ".KCcccccccccccccccccckK.",
    ".KkkkkkkkkkkkkkkkkkkkkK.",
    "..KKKKKKKKKKKKKKKKKKKK..",
    "........................",
    "........................",
    "........................",
]
sprite("DESK-BRIEFCASE", "Briefcase", "Bags", {**SHELL["brown"], **BULB}, BRIEFCASE,
       frames=[None, {(8, 9): "Y", (7, 10): "Y"}, None, {(16, 9): "Y", (15, 10): "Y"}], ticks=[14, 2, 6, 2],
       old=["PROP-041"])


# ======================================================================================================================
# BACKPACKS (24) - the zipper pull swings
# ======================================================================================================================
BACKPACK = [
    "........................",
    "..........KKKK..........",
    ".........KK..KK.........",
    ".......KKKKKKKKKK.......",
    ".....KKCCCCCcccckKK.....",
    "....KCCCccccccccckkK....",
    "....KCCcccccccccckkK....",
    "....KCCcccccccccckkK....",
    "....KCCcccccccccckkK....",
    "....KCCcccccccccckkK....",
    "....KCCcccccccccckkK....",
    "....KCKKKKKKKKKKKKkK....",
    "....KCKiiiiiiiiiiKkK....",
    "....KCKCCCCCcccckKkK....",
    "....KCKCcccccccckKkK....",
    "....KCKCcccccccckKkK....",
    "....KCKCcccccccckKkK....",
    "....KCKCcccccccckKkK....",
    "....KCKCcccccccckKkK....",
    "....KCKkkkkkkkkkkKkK....",
    "....KCKKKKKKKKKKKKkK....",
    "....KkkkkkkkkkkkkkkK....",
    ".....KKKKKKKKKKKKKK.....",
    "........................",
]
PULL = [{(12, 13): "I", (12, 14): "A"}, {(12, 13): "I", (13, 14): "A"}, {(12, 13): "I", (12, 14): "A"},
        {(12, 13): "I", (11, 14): "A"}]
for sid, title, shell, old in [("DESK-BACKPACK", "Backpack", "blue", ["PROP-042"]),
                               ("DESK-BACKPACK-RED", "Backpack, red", "red", ["PROP-043"])]:
    sprite(sid, title, "Bags", {**SHELL[shell], **METAL}, ink(BACKPACK, [(12, 13)], "I"),
           frames=[ink(ink(BACKPACK, [(12, 13)], "I"), [p for p, c in f.items() if c == "A"], "A") for f in PULL],
           ticks=[10, 3, 4, 3], old=old)


# ======================================================================================================================
# ID BADGE (16x24, blank) - swings on its lanyard; photo is a plain silhouette, no name, no number
# ======================================================================================================================
CARD = [
    ".AA...........",
    "AiaA..........",
    ".AA...........",
    "OOOOOOOOOOOOOO",
    "OCCCCK..KccckO",
    "OCcccKKKKccckO",
    "OkkkkkkkkkkkkO",
    "OPPPPPPPPPPPpO",
    "OPsssssPPPPPpO",
    "OPsuuusPPPPPpO",
    "OPsuuusPPPPPpO",
    "OPssussPPPPPpO",
    "OPuuuuuPPPPPpO",
    "OPuuuuuPPPPPpO",
    "OPPPPPPPPPPPpO",
    "OPPPPPPPPPPPpO",
    "OppppppppppppO",
    "OOOOOOOOOOOOOO",
]
def _clip(card):   # the clip sits centred on the card's top edge
    return [r if i > 2 else "......" + r[:3] + "....." for i, r in enumerate(card)]
CARD = _clip(CARD)
STRAP = {
    0:  ["....lL....lL....", ".....lL..lL.....", "......lLlL......"],
    -1: ["....lL....lL....", "....lL...lL.....", ".....lL.lL......"],
    1:  ["....lL....lL....", ".....lL...lL....", "......lL.lL....."],
}
def badge(dx):
    g = blank(16, 24)
    g = stamp(g, STRAP[dx], 0, 0)
    return stamp(g, CARD, 1 + dx, 3)
BADGE_PAL = {**SHELL["blue"], **PAPERS, **METAL, "l": "#c8364a", "L": "#7a1a2a", "s": "#c8dcec", "u": "#6e7898"}
sprite("DESK-BADGE", "ID badge (blank)", "Desk", BADGE_PAL, badge(0),
       frames=[badge(0), badge(1), badge(0), badge(-1)], ticks=[6, 4, 3, 4], old=["PROP-044"])


# ======================================================================================================================
# RUBBER DUCK (16) - squeak-bob: the head dips, eyes squeeze shut, a squeak sparkle pops
# ======================================================================================================================
DUCK_HEAD = [
    ".........KKKK...",
    "........KCCccK..",
    ".......KCCcecK..",
    ".......KCccccBBr",
    ".......Kcccckbbr",
]
DUCK_BODY = [
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    ".KK.....KkcK....",
    ".KCKKKKKCcccckK.",
    ".KCCCCCcccccckK.",
    ".KCCkCCCkcccckK.",
    ".KCcckkkccccckK.",
    ".KcccccccccckkK.",
    "..KkkcccccckkK..",
    "...KKKKKKKKKK...",
    "................",
]
DUCK = stamp(DUCK_BODY, DUCK_HEAD, 0, 2)
DUCK_SQ = ink(ink(stamp(DUCK_BODY, DUCK_HEAD, 0, 3), [(11, 5)], "k"), [(14, 1), (15, 0), (13, 0)], "w")
DUCK_SQ = ink(DUCK_SQ, [(9, 2), (10, 2), (11, 2), (12, 2)], ".")
sprite("DESK-DUCK", "Rubber duck", "Desk", {**SHELL["yellow"], "B": "#ffa848", "b": "#e8742a", "r": "#9a3a1a",
       "e": "#2a1c2c", "w": "#fffbe0"}, DUCK, frames=[DUCK, DUCK_SQ, DUCK, DUCK_SQ, DUCK], ticks=[10, 2, 2, 2, 8],
       old=["PROP-045"])


# ======================================================================================================================
# PRINTER (32x24) - a sheet feeds out of the slot, the status light blinks
# ======================================================================================================================
PRINTER = [
    "................................",
    "...........OOOOOOOOOO...........",
    "...........OPPPPPPPpO...........",
    "...........OPPPPPPPpO...........",
    "....AAAAAAAAAAAAAAAAAAAAAAAA....",
    "...AIiiiiiiiiiiiiiiiiiiiiiaaA...",
    "...AiiiiiiiiiiiiiiiiiiiiiiaaA...",
    "...AAAAAAAAAAAAAAAAAAAAAAAAAA...",
    "...AiaaaaaaaaaaaaaaaaaaaaaaaA...",
    "...AiaaaddddddddddddddddddaaA...",
    "...AiaaaiiiiiiiiiiiiiiiiiiaaA...",
    "...AiaaaaaaaaaaaaaaaaaaaaaaaA...",
    "...AiaaaaaaaaaaaaaaaaaaaAAaaA...",
    "...AiaaaaaaaaaaaaaaaaaaaAgaaA...",
    "...AiaaaaaaaaaaaaaaaaaaaaaaaA...",
    "...AAAAAAAAAAAAAAAAAAAAAAAAAA...",
    "....AA....................AA....",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
]
SHEET_OUT = ["OPPPPPPPPPpO", "OPooPoooPPpO", "OPPPPPPPPPpO", "OPoooPooPPpO", "OPPPPPPPPPpO", "OOOOOOOOOOOO"]
def printing(n, light):
    g = PRINTER if n == 0 else stamp(PRINTER, SHEET_OUT[-n:], 10, 10)
    return ink(g, [(25, 13)], light)
PRINTER_PAL = {**METAL, **PAPERS, "d": "#262838", "g": "#7cf05a", "G": "#2c7044"}
sprite("DESK-PRINTER", "Printer", "Office furniture", PRINTER_PAL, printing(0, "g"),
       frames=[printing(0, "g"), printing(0, "G"), printing(2, "g"), printing(4, "G"), printing(6, "g"), printing(6, "g")],
       ticks=[6, 4, 3, 3, 3, 10], old=["PROP-047"])


# ======================================================================================================================
# OFFICE CHAIR (24x36, floor) - swivels a little: back turns left, faces front, turns right
# ======================================================================================================================
FABRIC = {"F": "#1e2236", "f": "#2e3450", "u": "#454c70", "U": "#6a7298"}
CHAIR_BACK = {
    0: [
        "...FFFFFFFF...",
        ".FFUUUUuuuuFF.",
        "FUUUuuuuuuuufF",
        "FUUuuuuuuuuufF",
        "FUUuuuuuuuuufF",
        "FUUuuuuuuuuufF",
        "FUUuuuuuuuuufF",
        "FUUuuuuuuuuufF",
        "FUUuuuuuuuuufF",
        "FUUuuuuuuuuufF",
        "FUUuuuuuuuuufF",
        "FUuuuuuuuuuffF",
        ".FfffffffffffF",
        "..FFFFFFFFFF..",
    ],
    1: [   # turned: narrower, the far edge darker, the near side edge shows
        "...FFFFFFF....",
        "..FUUUuuuFF...",
        ".FUUuuuuuffF..",
        ".FUuuuuuuufFF.",
        ".FUuuuuuuufFF.",
        ".FUuuuuuuufFF.",
        ".FUuuuuuuufFF.",
        ".FUuuuuuuufFF.",
        ".FUuuuuuuufFF.",
        ".FUuuuuuuufFF.",
        ".FUuuuuuuufFF.",
        ".FuuuuuuuffFF.",
        "..FffffffffF..",
        "...FFFFFFFF...",
    ],
    -1: [  # turned the other way: hand-drawn again so the light still comes from the top-left
        "....FFFFFFF...",
        "...FFUUUuuuF..",
        "..FUUUuuuuufF.",
        ".FFUUuuuuuufF.",
        ".FFUUuuuuuufF.",
        ".FFUUuuuuuufF.",
        ".FFUUuuuuuufF.",
        ".FFUUuuuuuufF.",
        ".FFUUuuuuuufF.",
        ".FFUUuuuuuufF.",
        ".FFUUuuuuuufF.",
        ".FFUuuuuuuffF.",
        "..FfffffffffF.",
        "...FFFFFFFF...",
    ],
}
CHAIR_BASE = [
    ".FFFF......aA......FFFF.",
    ".FUuF......aA......FufF.",
    "..AA.......aA.......AA..",
    "...FFFFFFFFFFFFFFFFFF...",
    "..FUUUUUUUUUuuuuuuuufF..",
    "..FUuuuuuuuuuuuuuuuufF..",
    "..FffffffffffffffffffF..",
    "...FFFFFFFFFFFFFFFFFF...",
    "..........AiaA..........",
    "..........AiaA..........",
    "..........AiaA..........",
    "..........AiaA..........",
    "........AAiiaaAA........",
    "......AAiiAAAAaaAA......",
    "....AAiiAA.AA.AAaaAA....",
    "..AAiiAA...AA...AAaaAA..",
    ".FfF......FffF......FfF.",
    ".FFF......FFFF......FFF.",
]
def chair(pose):
    g = blank(24, 36)
    g = stamp(g, CHAIR_BASE, 0, 18)
    if pose == 0: return stamp(g, CHAIR_BACK[0], 5, 6)
    return stamp(g, CHAIR_BACK[pose], 5, 6)
sprite("DESK-CHAIR", "Office chair", "Office furniture", {**FABRIC, **METAL}, chair(0),
       frames=[chair(0), chair(1), chair(0), chair(-1)], ticks=[12, 4, 6, 4], old=["PROP-048"])


# ======================================================================================================================
# CLIPBOARD (24) - a tick lands in the first box, then the sheet resets
# ======================================================================================================================
CLIPBOARD = [
    "........................",
    "..........AAAA..........",
    ".........AiiaaA.........",
    "....KKKKAiiiiaaAKKKK....",
    "...KCcccAAAAAAAAccckK...",
    "...KCcOOOOOOOOOOOOckK...",
    "...KCcOPPPPPPPPPpOckK...",
    "...KCcOPoooPPPPPpOckK...",
    "...KCcOPoPoPoooopOckK...",
    "...KCcOPoooPPPPPpOckK...",
    "...KCcOPPPPPPPPPpOckK...",
    "...KCcOPoooPPPPPpOckK...",
    "...KCcOPoPoPoooppOckK...",
    "...KCcOPoooPPPPPpOckK...",
    "...KCcOPPPPPPPPPpOckK...",
    "...KCcOPoooPPPPPpOckK...",
    "...KCcOPoPoPoooopOckK...",
    "...KCcOPoooPPPPPpOckK...",
    "...KCcOPPPPPPPPPpOckK...",
    "...KCcOPPPPPPPPPpOckK...",
    "...KCcOppppppppppOckK...",
    "...KCcOOOOOOOOOOOOckK...",
    "...KCkkkkkkkkkkkkkkkK...",
    "....KKKKKKKKKKKKKKKK....",
]
TICK1 = [(8, 8), (9, 9)]
TICK2 = TICK1 + [(10, 8), (11, 7), (12, 6)]
sprite("DESK-CLIPBOARD", "Clipboard", "Paper", {**SHELL["brown"], **PAPERS, **METAL, **INK}, ink(CLIPBOARD, TICK2, "z"),
       frames=[ink(CLIPBOARD, TICK2, "z"), CLIPBOARD, ink(CLIPBOARD, TICK1, "z")], ticks=[16, 8, 1], old=["PROP-049"])
