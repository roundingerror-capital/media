"""FOOD · Drinks. 16 px icons, same method as lib/food.py (Kirby Super Star / Stardew / SotN): the vessel fills ~80% of the
box, one main colour + one accent, a 3-4 tone hue-shifted ramp per material, outline in each material's own darkest tone,
light from the top-left. Every glass shares GLASS (chunky 2-3 px highlight, never a dot); every hot drink shares STEAM.
Variants are legend swaps of the same grid (skill section 11)."""
from lib import sprite
from lib.food import *

G_ = "Drinks"

# ---- shared ramps ------------------------------------------------------------------------------------------------------
GLASS = {"G": "#3d5a7a", "g": "#86a9c6", "v": "#c8e4ef", "W": "#f6fcff"}          # outline, shadow, body, highlight
STEAM = {"s": "#9fb0c4", "S": "#e4ecf4"}                                             # wisp shadow, wisp light
PAPER = {"O": "#5b4f63", "o": "#b9b0bb", "c": "#ece6e0", "C": "#fffbf2"}           # paper cup / white ceramic
LIDW = {"L": "#5b4f63", "l": "#b9b0bb", "w": "#ece6e0", "X": "#fffbf2"}            # white lid (same values, own chars)
KRAFT = {"D": DOUGH["D"], "d": DOUGH["d"], "b": DOUGH["b"], "B": DOUGH["B"]}       # sleeve / cork / cinnamon
COFFEE = {"T": PATTY["T"], "t": PATTY["t"], "u": PATTY["u"]}                       # black coffee
COCOA_ = {"T": "#3a1d16", "t": "#6a3a26", "u": "#9a5e3e"}                          # cocoa (milkier)
METAL = {"A": "#3e4256", "a": "#7d8299", "i": "#bfc4d4", "I": "#f2f4fa"}           # cans, wire, stoppers
CERAMIC = {  # mug / pot glazes: outline, shadow, base, light
    "cream": {"M": "#5a4e66", "m": "#b6aec0", "n": "#ebe5e6", "N": "#fffaf2"},
    "red":   {"M": "#5e1426", "m": "#a8243a", "n": "#de4048", "N": "#ff7a68"},
    "blue":  {"M": "#1c2e5e", "m": "#3456a0", "n": "#4f86cf", "N": "#8cc2f0"},
    "green": {"M": "#163e2c", "m": "#2c7044", "n": "#48a058", "N": "#8cd27a"},
    "mint":  {"M": LINER_MINT["L"], "m": LINER_MINT["l"], "n": LINER_MINT["m"], "N": LINER_MINT["M"]},
    "clay":  {"M": "#4e1f14", "m": "#8e3c1e", "n": "#c8642c", "N": "#f09a52"},
}

def over(grid, rows, y0=0):
    """Overlay rows onto grid starting at row y0; '.' in rows leaves the grid pixel alone."""
    g = [list(r) for r in grid]
    for dy, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch != ".": g[y0 + dy][x] = ch
    return ["".join(r) for r in g]

def top(grid, rows):
    """Replace the first len(rows) rows of grid (steam / bubble / cork frames are drawn as their own rows)."""
    return list(rows) + list(grid[len(rows):])


WISP = {  # (frame A, frame B) patterns, top row first: a 1 px wavy line, faint at the tip ('s'), bright at the cup ('S');
    # the two frames lean opposite ways so the steam sways instead of sliding
    4: (["s.", ".s", ".S", "S."], [".s", "s.", "S.", ".S"]),
    3: (["s.", ".S", ".S"], [".s", "S.", "S."]),
    2: (["s.", ".S"], [".s", "S."]),
}
def wisps(n, xs, frame, w=16):
    """n rows of steam: one wisp per left-x in xs, drawn from WISP[n] (frame 0 or 1)."""
    rows = [["."] * w for _ in range(n)]
    for x in xs:
        for y, pat in enumerate(WISP[n][frame]):
            for dx, ch in enumerate(pat):
                if ch != ".": rows[y][x + dx] = ch
    return ["".join(r) for r in rows]

def steam(n, *wisps, w=16):
    """n rows of steam. Each wisp = list of left-x per row (None = gap); a wisp pixel pair is lit-left 'S', shadow-right 's'
    on the upper rows and darker 'ss'/'sS' as it thins, so the curl reads soft rather than as a chevron."""
    rows = [["."] * w for _ in range(n)]
    for xs in wisps:
        for y, x in enumerate(xs):
            if x is None: continue
            rows[y][x], rows[y][x + 1] = ("S", "s") if y < n - 1 else ("s", "s")
    return ["".join(r) for r in rows]


# ---- coffee to go -------------------------------------------------------------------------------------------------------
TOGO = [
    "................",
    "................",
    "......LLLL......",
    "....LXXwwwlL....",
    "..LXXwwwwwwllL..",
    "...LLLLLLLLLL...",
    "...OCCccccooO...",
    "...OCCccccooO...",
    "...OCCccccooO...",
    "...DBBbbbbddD...",
    "...DBBbbbbddD...",
    "....DBBbbbdD....",
    "....DBBbbbdD....",
    "....OCCccooO....",
    "....OCCccooO....",
    ".....OOOOOO.....",
]
TOGO_STEAM = [wisps(2, [7], 0), wisps(2, [7], 1)]
_cupblue = {"O": "#1c2e5e", "o": "#3456a0", "c": "#4f86cf", "C": "#8cc2f0"}
for sid, title, cup, old in [("FOOD-COFFEE-TOGO", "Coffee to go", PAPER, ["PROP-079", "PROP-199", "PROP-333"]),
                             ("FOOD-COFFEE-TOGO-BLUE", "Coffee to go, blue cup", _cupblue, ["PROP-080"])]:
    sprite(sid, title, G_, {**LIDW, **cup, **KRAFT, **STEAM}, top(TOGO, TOGO_STEAM[0]),
           frames=[None, top(TOGO, TOGO_STEAM[1])], ticks=[5, 5], old=old)


# ---- coffee mug ---------------------------------------------------------------------------------------------------------
MUG = [
    "................",
    "................",
    "................",
    "................",
    "..MMMMMMMMMM....",
    ".MNTTTTTTTTmM...",
    ".MNtuuttttTmM...",
    ".MNNNnnnnnmmMM..",
    ".MNNnnnnnnmmMnM.",
    ".MZZzzzzzzyyM.mM",
    ".MZZzzzzzzyyM.mM",
    ".MNNnnnnnnmmMmM.",
    ".MNNnnnnnnmmMM..",
    ".MNnnnnnnnmmM...",
    "..MmmmmmmmmM....",
    "...MMMMMMMM.....",
]
MUG_STEAM = [wisps(4, [4, 8], 0), wisps(4, [4, 8], 1)]
BAND = {"cream": {"Z": "#8cc2f0", "z": "#4f86cf", "y": "#3456a0"},
        "red":   {"Z": "#fffaf2", "z": "#ebe5e6", "y": "#b6aec0"}}
for sid, title, glaze, old in [("FOOD-COFFEE-MUG", "Coffee mug", "cream", ["PROP-050", "PROP-499", "HOL-LAB-20", "PROP-031"]),
                               ("FOOD-COFFEE-MUG-RED", "Coffee, red mug", "red", ["HOL-LAB-21"])]:
    sprite(sid, title, G_, {**CERAMIC[glaze], **BAND[glaze], **COFFEE, **STEAM}, top(MUG, MUG_STEAM[0]),
           frames=[None, top(MUG, MUG_STEAM[1])], ticks=[5, 5], old=old)


# ---- cocoa with marshmallows ---------------------------------------------------------------------------------------------
MALLOW = {"x": "#a68a98", "w": "#e6d6de", "W": "#fffaf8"}
COCOA = [
    "................",
    "................",
    ".......WWw......",
    "...WWw.wwx......",
    "..MwwxMxxxMM....",
    ".MNxxTTtWWwmM...",
    ".MNtuuutwwxmM...",
    ".MNNNnnnnnmmMM..",
    ".MNNnnnnnnmmMnM.",
    ".MNNnnnnnnmmM.mM",
    ".MNNnnnnnnmmM.mM",
    ".MNNnnnnnnmmMmM.",
    ".MNNnnnnnnmmMM..",
    ".MNnnnnnnnmmM...",
    "..MmmmmmmmmM....",
    "...MMMMMMMM.....",
]
COCOA_STEAM = [wisps(2, [3, 10], 0), wisps(2, [3, 10], 1)]
for sid, title, glaze, old in [("FOOD-COCOA", "Cocoa with marshmallows", "blue", ["PROP-087", "HOL-TG-24", "HOL-XMAS-27"]),
                               ("FOOD-COCOA-GREEN", "Cocoa, green mug", "green", ["HOL-XMAS-28"])]:
    sprite(sid, title, G_, {**CERAMIC[glaze], **COCOA_, **MALLOW, **STEAM}, top(COCOA, COCOA_STEAM[0]),
           frames=[None, top(COCOA, COCOA_STEAM[1])], ticks=[5, 5], old=old)


# ---- teapot -------------------------------------------------------------------------------------------------------------
TEAPOT = [
    "................",
    "................",
    "................",
    "......MMM.......",
    ".....MNNmM......",
    "....MNNnnmM.....",
    "MM.MMMMMMMMM....",
    "MNMMNNNnnnmM....",
    ".MNNNnnnnnmmMMM.",
    ".MNNNnnnnnmmM.nM",
    "..MNNnnnnnmmM.mM",
    "..MZZzzzzzyyM.mM",
    "..MNnnnnnnmmMMM.",
    "..MnnnnnnmmmM...",
    "...MmmmmmmmM....",
    "....MMMMMMM.....",
]
TEAPOT_STEAM = [wisps(3, [0], 0), wisps(3, [0], 1)]
POT_BAND = {"Z": "#fffaf2", "z": "#ebe5e6", "y": "#b6aec0"}
for sid, title, glaze, old in [("FOOD-TEAPOT", "Teapot", "mint", ["PROP-095", "HOL-PRES-48", "HOL-TG-25"]),
                               ("FOOD-TEAPOT-RED", "Teapot, red", "red", ["HOL-XMAS-30"])]:
    sprite(sid, title, G_, {**CERAMIC[glaze], **POT_BAND, **STEAM}, over(TEAPOT, TEAPOT_STEAM[0], 3),
           frames=[None, over(TEAPOT, TEAPOT_STEAM[1], 3)], ticks=[6, 6], old=old)


# ---- hot cider (clay mug, cinnamon stick) --------------------------------------------------------------------------------
CIDER_LIQ = {"T": "#6e2e0e", "t": "#b85a16", "u": "#eb9a3a"}
CINNAMON = {"K": "#4a2412", "k": "#8a4a22", "j": "#c27a3e"}
CIDER = over(MUG, [
    "................",
    "................",
    ".........jk.....",
    ".........kK.....",
    "........jk......",
    "........kK......",
], 0)
CIDER_STEAM = [wisps(4, [3], 0), wisps(4, [3], 1)]
sprite("FOOD-CIDER", "Hot cider", G_, {**CERAMIC["clay"], **BAND["red"], **CIDER_LIQ, **CINNAMON, **STEAM},
       over(CIDER, CIDER_STEAM[0]), frames=[None, over(CIDER, CIDER_STEAM[1])], ticks=[5, 5],
       old=["HOL-PRES-47", "HOL-TG-22", "HOL-TG-23"])


# ---- thermos ------------------------------------------------------------------------------------------------------------
THERMOS = [
    "................",
    "................",
    ".....AAAAAA.....",
    "....AIIiiiaA....",
    "....AIiiiiaA....",
    "....AAAAAAAA....",
    ".....AiiiaA.....",
    "....MNNnnnmM....",
    "....MNNnnnmMMM..",
    "....MNNnnnmM.M..",
    "....AIIiiiaA.M..",
    "....MNNnnnmM.M..",
    "....MNNnnnmMMM..",
    "....MNnnnnmM....",
    "....AIIiiiaA....",
    ".....AAAAAA.....",
]
THERMOS_STEAM = [wisps(2, [7], 0), wisps(2, [7], 1)]
for sid, title, glaze, old in [("FOOD-THERMOS", "Thermos", "green", ["PROP-177", "HOL-LAB-18"]),
                               ("FOOD-THERMOS-RED", "Thermos, red", "red", ["HOL-LAB-19"])]:
    sprite(sid, title, G_, {**CERAMIC[glaze], **METAL, **STEAM}, top(THERMOS, THERMOS_STEAM[0]),
           frames=[None, top(THERMOS, THERMOS_STEAM[1])], ticks=[5, 5], old=old)


# ---- wine glasses (tulip bowl narrower at the rim, stem, foot) ------------------------------------------------------------
WINE = [
    "....GGGGGGGG....",
    "...GWvvvvvvgG...",
    "..GWWvvvvvvvgG..",
    "..GWWvvvvvvvgG..",
    "..GWEEEEEEEEgG..",
    "..GWeeeeeeerrG..",
    "..GeeeeeeerrRG..",
    "...GeeeerrRRG...",
    "....GrrrrRRG....",
    "......GGGG......",
    ".......vG.......",
    ".......vG.......",
    ".......vG.......",
    "......GvgG......",
    "...GWWvvvvggG...",
    "....GGGGGGGG....",
]
WINE_RED = {"R": "#3e0c26", "r": "#7a1838", "e": "#b02a4a", "E": "#e0607a"}
WINE_WHITE = {"R": "#8a6418", "r": "#c49a30", "e": "#e8cc62", "E": "#fff0a8"}
sprite("FOOD-WINE-RED", "Glass of red", G_, {**GLASS, **WINE_RED}, WINE, old=["PROP-070"])
sprite("FOOD-WINE-WHITE", "Glass of white", G_, {**GLASS, **WINE_WHITE}, WINE, old=["PROP-071"])


# ---- martini cocktail with a cherry ---------------------------------------------------------------------------------------
COCKTAIL = [
    "...........h....",
    "..........h.....",
    ".........wC.....",
    "GGGGGGGGGCKGGGGG",
    ".GWQQQQQQQQQQgG.",
    "..GWqqqqqqpppG..",
    "...GWqqqqppPG...",
    "....GWqqqpPG....",
    ".....GWqpPG.....",
    "......GPPG......",
    ".......vG.......",
    ".......vG.......",
    ".......vG.......",
    "......GvgG......",
    "...GWWvvvvggG...",
    "....GGGGGGGG....",
]
CHERRY_PICK = {"K": CHERRY["K"], "C": CHERRY["C"], "w": CHERRY["w"], "h": CHERRY["g"]}  # stem on its own char (g = glass)
BLUE_DRINK = {"P": "#1c3a78", "p": "#2f6cc0", "q": "#5aa8e8", "Q": "#a6e0ff"}
sprite("FOOD-COCKTAIL", "Cocktail", G_, {**GLASS, **FROST_PINK, **CHERRY_PICK}, COCKTAIL, old=["PROP-072"])
sprite("FOOD-COCKTAIL-BLUE", "Cocktail, blue", G_, {**GLASS, **BLUE_DRINK, **CHERRY_PICK}, COCKTAIL, old=["PROP-073"])


# ---- champagne flute, rising bubbles -------------------------------------------------------------------------------------
FLUTE = [
    ".....GGGGGG.....",
    ".....GWvvgG.....",
    ".....GWvvgG.....",
    ".....GWEEeG.....",
    ".....GWeeeG.....",
    ".....GWeeeG.....",
    ".....GeeerG.....",
    "......GerG......",
    "......GrrG......",
    ".......GG.......",
    ".......vG.......",
    ".......vG.......",
    ".......vG.......",
    "......GvgG......",
    "....GWvvvggG....",
    ".....GGGGGG.....",
]
BUBBLE_A = {(8, 5): "B", (7, 7): "B"}
BUBBLE_B = {(7, 4): "B", (8, 6): "B"}
FIZZ_GOLD = {"r": "#c49a30", "e": "#ecd068", "E": "#fff6c4", "B": "#fffdf0"}
FIZZ_PINK = {"r": "#c4566e", "e": "#f39aac", "E": "#ffe0e6", "B": "#fff6f8"}
for sid, title, fz, old in [("FOOD-FLUTE", "Champagne flute", FIZZ_GOLD, ["PROP-437", "HOL-NYD-04"]),
                            ("FOOD-FLUTE-PINK", "Flute, pink", FIZZ_PINK, ["HOL-NYD-05"])]:
    sprite(sid, title, G_, {**GLASS, **fz}, FLUTE, frames=[BUBBLE_A, BUBBLE_B], ticks=[4, 4], old=old)


# ---- beer: glass mug, frothy head ----------------------------------------------------------------------------------------
FOAM = {"F": "#a8988c", "f": "#e8decf", "Y": "#fffcf2"}
AMBER = {"R": "#6e300c", "r": "#b8600e", "e": "#e89a24", "E": "#ffd060"}
BEER = [
    "................",
    "...FFF..FFF.....",
    "..FYYfFFYYffF...",
    ".FYYYffffffffF..",
    ".FYfffffffffFF..",
    ".GFfFffffFfFGGG.",
    ".GWEEeeeerrgG.vG",
    ".GWEeeeeerrgG.vG",
    ".GWEeeeeerrgG.gG",
    ".GWEeeeeerRgG.gG",
    ".GWeeeeerrRgG.gG",
    ".GvEeeeerrRgGGG.",
    ".GveeeerrrRgG...",
    ".GvrrrrrrRRgG...",
    ".GWvvvvvvvvgG...",
    "..GGGGGGGGGG....",
]
sprite("FOOD-BEER", "Beer mug", G_, {**GLASS, **FOAM, **AMBER}, BEER, old=["PROP-092"])


# ---- lemonade: tumbler, lemon wheel, bendy straw ---------------------------------------------------------------------------
LEMONADE_ = {"R": "#b8841a", "r": "#e6c040", "e": "#f8e47c", "E": "#fff8c4"}
LEMON = {"K": "#a8720e", "k": "#f2c418", "j": "#fff2a0"}
STRAW = {"Z": "#f0606a", "z": "#a82a44"}
LEMONADE = [
    "..kkk....ZZZz...",
    ".kjjjk...Zz.....",
    "kjjjjjk..Zz.....",
    "KKKKKKKGGZzGGG..",
    "...GWEEEEZzEEG..",
    "...GWeeeeZzeeG..",
    "...GWvveeZzerG..",
    "...GWvveeZzerG..",
    "...GWeeeeZzerG..",
    "...GWeeeeerrrG..",
    "....GWeeeerrG...",
    "....GeeeerrRG...",
    "....GeeerrRRG...",
    "....GrrrrRRRG...",
    "....GWvvvvggG...",
    ".....GGGGGGG....",
]
sprite("FOOD-LEMONADE", "Lemonade", G_, {**GLASS, **LEMONADE_, **LEMON, **STRAW}, LEMONADE,
       old=["PROP-093", "HOL-MEM-32", "HOL-IND-38"])


# ---- strawberry soda: fountain glass, strawberry on the rim, straw ---------------------------------------------------------
BERRY = {"K": CHERRY["K"], "C": CHERRY["C"], "c": CHERRY["c"], "w": CHERRY["w"], "h": CHERRY["g"], "H": "#8fd14f"}
SODA_PINK = {"P": FROST_PINK["P"], "p": FROST_PINK["p"], "q": FROST_PINK["q"], "Q": FROST_PINK["Q"]}
STRAWSODA = [
    "...ZZZz.........",
    ".....Zz...hHh...",
    ".....Zz..cCCCK..",
    "..GGGZzGGcwCwK..",
    "..GWQZzQQQCCKG..",
    "..GWqZzqqqqKpG..",
    "..GWqZzqqqqppG..",
    "...GWqqqqqppG...",
    "....GqqqqppG....",
    ".....GqqppG.....",
    ".....GqpPPG.....",
    ".....GpPPPG.....",
    "......GvgG......",
    ".......vG.......",
    "....GWWvvggG....",
    ".....GGGGGG.....",
]
sprite("FOOD-STRAWBERRY-SODA", "Strawberry soda", G_, {**GLASS, **SODA_PINK, **BERRY, **STRAW}, STRAWSODA,
       frames=[None, {(7, 6): "Q", (9, 8): "Q"}, {(8, 5): "Q", (8, 9): "Q"}], ticks=[6, 4, 4],
       old=["HOL-JUN-25", "HOL-JUN-26"])


# ---- eggnog: rocks glass, nutmeg dust, holly sprig -----------------------------------------------------------------------
NOG = {"R": "#a07c52", "r": "#dcc08c", "e": "#f4e6bc", "E": "#fffbea", "n": "#8a5a2e"}
HOLLY = {"h": "#2c6a2c", "H": "#5aa83a", "C": CHERRY["C"], "c": CHERRY["c"]}
EGGNOG = [
    "................",
    "................",
    "........hHH.....",
    "......HHhhHH....",
    ".......hhcC.....",
    "..GGGGGGcCCGGG..",
    "..GWEnnEEnnEgG..",
    "..GWEEEEEEEegG..",
    "..GWeeeeeeerrG..",
    "..GWeeeeeeerrG..",
    "..GWeeeeeerrRG..",
    "..GeeeeeerrrRG..",
    "..GrrrrrrrRRRG..",
    "..GvvvvvvvvvgG..",
    "..GWvvvvvvvggG..",
    "...GGGGGGGGGG...",
]
sprite("FOOD-EGGNOG", "Eggnog", G_, {**GLASS, **NOG, **HOLLY}, EGGNOG, old=["HOL-XMAS-29"])


# ---- soda can: metal lid + tab, a shaded wave stripe that wraps the cylinder (no flat white box) -----------------------
CAN_BODY = {"red":  {"O": "#5e1222", "m": "#9c1f30", "n": "#d6323e", "N": "#f2645a"},
            "blue": {"O": "#16285a", "m": "#2a4e9c", "n": "#3f7ed0", "N": "#7cb8f0"}}
WAVE = {"Z": "#fffaf2", "z": "#e2d8d6", "y": "#a898a8"}       # the wave is lit left, turns away on the right
SODACAN = [
    "....AAAAAAAA....",
    "...AIiAAiiiaA...",
    "...AiiiiiiaaA...",
    "...AAAAAAAAAA...",
    "...ONNnnnnmmO...",
    "...ONNnnnnmmO...",
    "...ONNnnnnmmO...",
    "...ONNzznnmmO...",
    "...ONZzzznmyO...",
    "...OZZnnzzyyO...",
    "...OZNnnnzymO...",
    "...ONNnnnnmmO...",
    "...ONNnnnnmmO...",
    "...ONnnnnmmmO...",
    "...AiiiiiiaaA...",
    "....AAAAAAAA....",
]
for sid, title, body, old in [("FOOD-SODA-CAN", "Soda can", "red", ["PROP-085", "HOL-IND-39", "HOL-LAB-47"]),
                              ("FOOD-SODA-CAN-BLUE", "Soda can, blue", "blue", ["PROP-086", "HOL-IND-40"])]:
    sprite(sid, title, G_, {**METAL, **CAN_BODY[body], **WAVE}, SODACAN, old=old)


# ---- soda bottle: crown cap, straight neck that widens in steps to the shoulder, contour waist ---------------------------
CROWN = {"K": CHERRY["K"], "C": CHERRY["C"], "c": CHERRY["c"]}
SODABOTTLE = [
    ".....KccCCK.....",
    ".....KKKKKK.....",
    "......GWgG......",
    "......GWtG......",
    "......GWtG......",
    ".....GWWttG.....",
    "....GWWtttTG....",
    "...GWWtttttTG...",
    "...GWWttttTTG...",
    "...GWWtttTTTG...",
    "....GWtttTTG....",
    "....GWtttTTG....",
    "...GWWtttTTTG...",
    "...GWWtttTTTG...",
    "...GvvttTTTgG...",
    "....GGGGGGGG....",
]
sprite("FOOD-SODA-BOTTLE", "Soda bottle", G_, {**GLASS, **COFFEE, **CROWN}, SODABOTTLE, old=["PROP-094"])


# ---- champagne: green bottle, gold foil, blank cream label; cork pops (hold, cork rises, cork flies + foam) --------------
FOIL = {"F": "#7a4a12", "f": "#c08a22", "y": "#f0c440", "Y": "#fff0a0"}
BOTTLE_GREEN = {"B": "#10281e", "m": "#1e4a32", "n": "#2f6e45", "N": "#5aa06a"}
LABEL = {"L": "#fff4dc", "l": "#e8d6b4", "k": "#a88a68"}
CHAMPAGNE = [
    "................",
    "................",
    "......FFFF......",
    "......FYyF......",
    "......FYyF......",
    "......FyfF......",
    ".....FYyffF.....",
    "....BNNnnmmB....",
    "...BNNnnnnmmB...",
    "...BNNnnnnmmB...",
    "...BLLlllllkB...",
    "...BLLlyyllkB...",
    "...BLLlfflkkB...",
    "...BNNnnnnmmB...",
    "...BNnnnnmmmB...",
    "....BBBBBBBB....",
]
CORK = {"D": DOUGH["D"], "u": DOUGH["b"], "U": DOUGH["B"], "d": DOUGH["d"]}   # own chars: B is the bottle outline
POP_1 = top(CHAMPAGNE, ["................", "......DUuD......", "......DudD......"])
POP_2 = top(CHAMPAGNE, ["......DUuD......", ".....SS..SS.....", "......SSSS......"])
sprite("FOOD-CHAMPAGNE", "Champagne", G_, {**FOIL, **BOTTLE_GREEN, **LABEL, **CORK, **STEAM}, CHAMPAGNE,
       frames=[None, POP_1, POP_2], ticks=[14, 2, 6], old=["PROP-436", "HOL-NYD-03"])


# ---- water bottle: sport bottle, flip spout cap, ribbed grip ---------------------------------------------------------------
WATERBOTTLE = [
    ".......OO.......",
    "......OCoO......",
    "....OOOOOOOO....",
    "....OCCccooO....",
    "....OOOOOOOO....",
    "...MNNnnnnmmM...",
    "...MNNnnnnmmM...",
    "...MNNnnnnmmM...",
    "....MNmmmmmM....",
    "....MNnnnnmM....",
    "....MNmmmmmM....",
    "...MNNnnnnmmM...",
    "...MNNnnnnmmM...",
    "...MNNnnnnmmM...",
    "...MNnnnnmmmM...",
    "....MMMMMMMM....",
]
PINK = {"M": FROST_PINK["P"], "m": FROST_PINK["p"], "n": FROST_PINK["q"], "N": FROST_PINK["Q"]}
for sid, title, body, old in [("FOOD-WATER-BOTTLE", "Water bottle", CERAMIC["blue"], ["PROP-032", "PROP-247"]),
                              ("FOOD-WATER-BOTTLE-PINK", "Water bottle, pink", PINK, ["PROP-033"])]:
    sprite(sid, title, G_, {**PAPER, **body}, WATERBOTTLE, old=old)


# ---- pitchers: glass, pour lip on the left, handle right, floating fruit slices ---------------------------------------------
PITCHER = [
    "................",
    "GGGGGGGGGGGG....",
    ".GWWvvvvvvgG....",
    "..GWEEEEEEgGGG..",
    "..GWeekkeerG.vG.",
    "..GWekjjkerG.vG.",
    "..GWeeKKeerG.gG.",
    "..GWeeeeerrG.gG.",
    "..GWkkeeerrG.gG.",
    "..GkjjkeerRGGG..",
    "..GeKKeerrRG....",
    "..GeeeerrrRG....",
    "..GrrrrrRRRG....",
    "..GvvvvvvvgG....",
    "..GWvvvvvvgG....",
    "...GGGGGGGG.....",
]
LIME = {"K": "#2c6a2c", "k": "#6cbc3c", "j": "#d6f29a"}
PUNCH_RED = {"R": "#5e1030", "r": "#a8203e", "e": "#d83a4e", "E": "#f47a80"}
sprite("FOOD-LEMONADE-PITCHER", "Lemonade pitcher", G_, {**GLASS, **LEMONADE_, **LEMON}, PITCHER,
       old=["HOL-MEM-31", "HOL-IND-37"])
sprite("FOOD-PUNCH", "Red punch pitcher", G_, {**GLASS, **PUNCH_RED, **LIME}, PITCHER, old=["HOL-JUN-27"])
