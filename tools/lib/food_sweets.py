"""FOOD · Sweets. 16 px icons drawn to match lib/food.py (Kirby Super Star / Stardew / SotN item method): one main colour plus
one accent, hue-shifted 3-4 tone ramps shared with food.py, highlight cluster top-left, outline in each material's own darkest
tone. Light: top-left. The wrapped candies are deliberately small (about 10x6 inside the 16 box)."""
from lib import sprite
from lib.food import *

# --- extra shared ramps (hue-shifted: darks lean violet/blue, lights lean warm) -----------------------------------------
CHOC_GLAZE = {"P": "#3a1d16", "p": "#5e3020", "q": "#8a4a2c", "Q": "#b8754a"}   # same keys as FROST_PINK: a glaze swap
SPRINKLES = {"w": "#ffe9da", "Z": "#ffd23f", "v": "#5aa8e8", "M": "#a6e0cb"}
RED = {"K": "#6e1830", "C": "#b8263a", "c": "#e8484a", "f": "#ff8a72"}           # CHERRY + one warm light
WHITE = {"V": "#8d86b8", "v": "#c4c0e2", "W": "#f0eef8", "w": "#ffe9da"}          # cool-shadowed white
BLUE = {"U": "#1d2a66", "u": "#2c52a8", "i": "#4a86d8", "I": "#86c0f4"}
GOLD = {"X": "#7a4a12", "x": "#c98a14", "z": "#ffd23f", "Z": "#fff2a8"}
CHOC_BAR = {"k": "#3a1d16", "h": "#5e3020", "j": "#8a4a2c", "J": "#b8754a"}

# --- donuts: one grid, two glazes -----------------------------------------------------------------------------------------
DONUT = [
    "................",
    "................",
    ".....pppPPP.....",
    "...ppQQqZZqPP...",
    "..pQQqqqqqqqpP..",
    ".pQqqqqqqqwwqpP.",
    "pqqZqqpPPpqqqqpP",
    "pqqZqpDddDpqvvpP",
    "pqqqqP....PqqqpP",
    "DpMMqqQQQQqqqqpD",
    "DPPqqPPPqqPPPPdD",
    ".DBPPBbbppbbbdD.",
    "..DbBbbbPPbddD..",
    "...DDdbbbddDD...",
    ".....DDDDDD.....",
    "................",
]
sprite("FOOD-DONUT-PINK", "Donut, pink", "Sweets", {**DOUGH, **FROST_PINK, **SPRINKLES}, DONUT, old=["PROP-061"])
sprite("FOOD-DONUT-CHOC", "Donut, chocolate", "Sweets", {**DOUGH, **CHOC_GLAZE, **SPRINKLES}, DONUT, old=["PROP-062"])

# --- ice cream: round scoop on a waffle cone, 2-frame drip ---------------------------------------------------------------
sprite("FOOD-ICECREAM", "Ice cream cone", "Sweets", {**FROST_PINK, **DOUGH}, [
    "......ppPP......",
    "....ppQQqqpP....",
    "...pqQQQqqqpP...",
    "..pqQQqqqqqqpP..",
    "..pQqqqqqqqqpP..",
    "..pqqqqqqqqppP..",
    "..pqqqqqqqpppP..",
    "..PpqqqqqpppPP..",
    "...PpqpPppPpP...",
    "...DBqpBbbbdD...",
    "....DPPbdbbD....",
    "....DbdbbdbD....",
    ".....DbdbdD.....",
    "......DdbD......",
    "......DbdD......",
    ".......DD.......",
], frames=[None, {(5, 10): "q", (6, 10): "p", (5, 11): "P", (6, 11): "P"}], ticks=[16, 12],
   old=["PROP-084", "HOL-MEM-46", "HOL-IND-36", "HOL-LAB-45"])

# --- popsicles: one grid, two flavours -----------------------------------------------------------------------------------
POPSICLE = [
    ".....CCCKKK.....",
    "....CfffccCK....",
    "...CffcccccCK...",
    "...CfccccccCK...",
    "...CfccccccCK...",
    "...vwWWWWWWvV...",
    "...vwWWWWWWvV...",
    "...vwWWWWWWvV...",
    "...uIiiiiiiuU...",
    "...uIiiiiiiuU...",
    "...uIiiiiiiuU...",
    "....UUUUUUUU....",
    "......DBbD......",
    "......DBbD......",
    "......DBbD......",
    ".......DD.......",
]
LIME = {"K": "#2c5a24", "C": "#4f9a33", "c": "#8fd14f", "f": "#d4f58a",
        "V": "#4f8a3a", "v": "#b8e08a", "W": "#e4f7b8", "w": "#fbffe6",
        "U": "#24502a", "u": "#3f8a3a", "i": "#6cbf48", "I": "#b4e878"}
sprite("FOOD-POPSICLE", "Popsicle, red white blue", "Sweets", {**RED, **WHITE, **BLUE, **DOUGH}, POPSICLE,
       old=["HOL-MEM-45", "HOL-IND-35"])
sprite("FOOD-POPSICLE-LIME", "Popsicle, lime", "Sweets", {**LIME, **DOUGH}, POPSICLE, old=["HOL-LAB-46"])

# --- wrapped candy: SMALL on purpose, 10x6 in the middle of the box ------------------------------------------------------
CANDY = [
    "................",
    "................",
    "................",
    "................",
    "................",
    "...p...PP...p...",
    "...wp.PQqP.pQ...",
    "...wQPqqqpPQq...",
    "...QQPqqppPqq...",
    "...Qp.PppP.pq...",
    "...p...PP...p...",
    "................",
    "................",
    "................",
    "................",
    "................",
]
CANDY_BLUE = {"P": "#1d2a66", "p": "#2c52a8", "q": "#4a86d8", "Q": "#86c0f4", "w": "#e4f2ff"}
sprite("FOOD-CANDY", "Wrapped candy, pink", "Sweets", {**FROST_PINK, "w": "#fff0f4"}, CANDY, old=["PROP-074", "PROP-294"])
sprite("FOOD-CANDY-BLUE", "Wrapped candy, blue", "Sweets", CANDY_BLUE, CANDY, old=["PROP-075"])

# --- chocolate bar: red paper, gold foil peeled back, no purple ----------------------------------------------------------
sprite("FOOD-CHOCBAR", "Chocolate bar", "Sweets", {**CHOC_BAR, **GOLD, **RED}, [
    "................",
    "....hhhhhhhk....",
    "...hJJJhJJJhk...",
    "...hJjjhJjjhk...",
    "...hJjjhJjjhk...",
    "...hhhhhhhhhk...",
    "...zzJJzzJJxX...",
    "..xZZzzzzzxxxX..",
    "..XxxxxxxxxxXX..",
    "...CffcccccCK...",
    "...CfcccccCCK...",
    "...xZzzzzzxxX...",
    "...CfcccccCCK...",
    "...CfcccccCCK...",
    "....KKKKKKKK....",
    "................",
], old=["PROP-076"])

# --- lollipop: round swirl on a stick --------------------------------------------------------------------------------------
sprite("FOOD-LOLLIPOP", "Lollipop", "Sweets", {**FROST_PINK, **WHITE}, [
    "................",
    ".....ppppPP.....",
    "....pqwwwwqP....",
    "...pqwqqqqwqP...",
    "...pwqqwwqqwP...",
    "..pqwqwqqwqwpP..",
    "..pqwqwqwwpQpP..",
    "..pqwqwpppQppP..",
    "...PwqpQQQppP...",
    "...PqqppppppP...",
    "....PppppppP....",
    ".....PPPPPP.....",
    ".......WV.......",
    ".......WV.......",
    ".......WV.......",
    ".......VV.......",
], old=["PROP-099", "PROP-293"])

# --- candy cane -------------------------------------------------------------------------------------------------------------
sprite("FOOD-CANDYCANE", "Candy cane", "Sweets", {**RED, **WHITE}, [
    "......WccWV.....",
    "....WWffwwfcV...",
    "...WwfcVVKcwwK..",
    "...WfcV...WwcK..",
    "...cfWV...WfcV..",
    "...cwWK...cfWV..",
    "...WwcK...KwWK..",
    "...WfcV....VK...",
    "...cfWV.........",
    "...cwWK.........",
    "...WwcK.........",
    "...WfcV.........",
    "...cfWV.........",
    "...cwWK.........",
    "...WwcK.........",
    "....VK..........",
], old=["PROP-100", "HOL-XMAS-21"])

# --- pies: one tin + crust geometry shared by the whole pies; slices share the wedge --------------------------------------
TIN = {"S": "#3a3f5c", "s": "#6d7896", "m": "#a8b4cc", "n": "#e4ecf4"}
APPLE_FILL = {"a": "#6a2c18", "A": "#b0602a", "y": "#f0c050"}
TIN_ROWS = [
    ".snnmmmmmmmsssS.",
    ".snmsmmsmmsssSS.",
    "..smsmmsmmssSS..",
    "....SSSSSSSS....",
    "................",
]
APPLE_FILL = {"a": "#5a2016", "A": "#9a4422", "y": "#f0b048"}
sprite("FOOD-APPLEPIE", "Apple pie, lattice", "Sweets", {**DOUGH, **TIN, **APPLE_FILL}, [
    "................",
    "................",
    ".....dddDDD.....",
    "...dBYBBBBbbD...",
    "..dBBbaaABbabD..",
    ".dbBBBBBBBbBBbD.",
    ".dBaBbaaaBbaabD.",
    "dBAABbaAyBbaAAdD",
    ".dBBBbBBBBBBBbD.",
    ".dbaBbaaAbdaadD.",
    ".DBbdBbdBbdbbdD.",
] + TIN_ROWS[:4] + ["................"], old=["PROP-088", "HOL-PRES-11", "HOL-MEM-47", "HOL-IND-50", "HOL-TG-05"])

PECAN = {"a": "#7a3414", "A": "#c0681e", "U": "#9a4c2a", "u": "#5e2414", "e": "#341008"}
sprite("FOOD-PECANPIE", "Pecan pie", "Sweets", {**DOUGH, **TIN, **PECAN}, [
    "................",
    "................",
    ".....dddDDD.....",
    "...dBYBBBBbbD...",
    "..dBUuuAAUuubD..",
    ".dBAuueaAuueabD.",
    ".dBAAaUuuAaAAbD.",
    "dBUuuAuueaUuuAdD",
    ".dbuueaAaAuuedD.",
    ".dbAaaAAAAAaadD.",
    ".DBbdBbdBbdbbdD.",
] + TIN_ROWS[:4] + ["................"], old=["HOL-TG-06"])

# --- pumpkin pie slice with a cream dollop ---------------------------------------------------------------------------------
PUMPKIN = {"O": "#7a2e14", "o": "#c0561e", "n": "#ec8a2e", "N": "#ffb85a"}
sprite("FOOD-PIE-SLICE", "Pumpkin pie slice", "Sweets", {**DOUGH, **PUMPKIN, **WHITE}, [
    "................",
    "................",
    "............dD..",
    ".......wW..nBbD.",
    "......wWvVnnBbD.",
    ".....wWWWvVnBbD.",
    ".....vvvvVNnBbD.",
    "....NNnnnnnoBbD.",
    "..NNnnnnnnooBbD.",
    "oNnnnnnnnnooBbD.",
    "OooooooooooOBbD.",
    "OooooooooooObdD.",
    ".DBbbbbbbbbbdD..",
    "..DDDDDDDDDDD...",
    "................",
    "................",
], old=["HOL-TG-04", "HOL-TG-03", "HOL-PRES-12"])

# --- birthday cake: pink-frosted layer cake, one plain candle, 2-frame flame ----------------------------------------------
sprite("FOOD-CAKE", "Birthday cake", "Sweets",
       {**FROST_PINK, **DOUGH, **RED, **LINER_MINT, **GOLD, "r": "#f06a2a", "y": "#ffd23f", "i": "#5aa8e8"}, [
    ".......z........",
    ".......Zz.......",
    ".......rr.......",
    ".......Mm.......",
    ".......Mm.......",
    "....pppMmPPP....",
    "..pqQQQMmqyypP..",
    ".pqQQqqqpqqqqpP.",
    ".pqqiiqqqqqqppP.",
    ".dqpddqpddqpddD.",
    ".dPPBbqpbbPPbdD.",
    ".KccccPPccccCCK.",
    ".dBBbbbbbbbbddD.",
    "..DdbbbbbbbddD..",
    "....DDDDDDDD....",
    "................",
], frames=[None, {(7, 0): ".", (8, 0): "z", (7, 1): "z", (8, 1): "Z"}], ticks=[4, 4],
   old=["PROP-438", "HOL-PRES-44", "HOL-TG-35"])

# --- red velvet slice: red sponge, cream-cheese layers --------------------------------------------------------------------
VELVET = {"K": "#4e1024", "C": "#8a1a2e", "c": "#b82a36", "f": "#d84a48"}
sprite("FOOD-REDVELVET", "Red velvet slice", "Sweets", {**VELVET, **WHITE}, [
    "................",
    "..........wwWvV.",
    ".......wwWWWWvV.",
    "....wwWWWWWWWvV.",
    ".wwWWWWWWWWWWvV.",
    "VWWWWWWWWWWvWvV.",
    "KffcccccccCCWvV.",
    "KfcccccccCCCWvV.",
    "KcccccccccCCWvV.",
    "VWWWWWWWWWWvWvV.",
    "KffcccccccCCWvV.",
    "KfcccccccCCCWvV.",
    "KcccccccccCCWvV.",
    "KKKKKKKKKKKKVVV.",
    "................",
    "................",
], old=["HOL-JUN-22", "HOL-JUN-23"])

# --- gingerbread person -----------------------------------------------------------------------------------------------------
GINGER = {"D": "#4a2414", "d": "#8a4a22", "b": "#b8692e", "B": "#dc9050"}
sprite("FOOD-GINGERBREAD", "Gingerbread person", "Sweets",
       {**GINGER, **WHITE, "c": "#e8484a", "C": "#b8263a", "g": "#5b7f2c", "h": "#3c5a1c", "k": "#2a1410"}, [
    "......dddD......",
    ".....dBBbbD.....",
    "....dBkBbkbD....",
    "....dBBbbbbD....",
    "....dbwbbwbD....",
    ".....dbwwbD.....",
    "..dBBBbbbbbbbD..",
    ".dwBbbbcCbbbdwD.",
    ".DwdDBbbbbdDdwD.",
    "....dBbghbbD....",
    "....dBbbbbbD....",
    "...dBbbddbbbD...",
    "...dBbD..dbbD...",
    "..dBbbD..dbbbD..",
    "..dwwbD..dwwbD..",
    "..DDDD....DDDD..",
], old=["HOL-XMAS-22"])

# --- iced cut-out cookies ---------------------------------------------------------------------------------------------------
sprite("FOOD-STARCOOKIE", "Star cookie", "Sweets", {**DOUGH, **GOLD}, [
    ".......bD.......",
    ".......Bd.......",
    "......bZxD......",
    "......bZzD......",
    ".....bZzzxD.....",
    "bbbbbZZzzzxbbbbD",
    ".dZZzzzzzzzzxxD.",
    "..dZzzzzzzzxxD..",
    "...dzzzzzzxxD...",
    "....dzzzzxxD....",
    "....dzzxxxxD....",
    "...dzzxDDxxbD...",
    "...dzxD..DxbD...",
    "..dzxD....DxbD..",
    "..dDD......DDD..",
    "................",
], old=["HOL-XMAS-23", "HOL-TG-37"])

sprite("FOOD-HEARTCOOKIE", "Heart cookie", "Sweets", {**DOUGH, **FROST_PINK}, [
    "................",
    "..dddD....dddD..",
    ".dQQqpD..dQqqpD.",
    "dQQqqqpddQqqqppD",
    "dQqqqqqqqqqqqppD",
    "dqqqqqqqqqqqqppD",
    "dqqqqqqqqqqqppbD",
    ".dqqqqqqqqqqpbD.",
    "..dqqqqqqqqpbD..",
    "...dqqqqqqpbD...",
    "....dqqqqpbD....",
    ".....dqqpbD.....",
    "......dpbD......",
    ".......DD.......",
    "................",
    "................",
], old=["HOL-XMAS-24"])

# --- yule log: chocolate roll, cream spiral end, holly sprig ----------------------------------------------------------------
sprite("FOOD-YULELOG", "Yule log", "Sweets",
       {**CHOC_BAR, **WHITE, "G": "#2c5a24", "e": "#4f9a33", "E": "#8fd14f", "c": "#e8484a", "K": "#6e1830"}, [
    "................",
    "................",
    "................",
    "..........eE....",
    "........GeEecK..",
    ".........GGccK..",
    ".hhhhhhhhhhhhhh.",
    "hjWWWjhJJJjjJJjk",
    "hWjjjWhjhhhjjjjk",
    "hWjWjWhjjjjhhhjk",
    "hWjWWjhhhjjjjjjk",
    "hWjjjjhjjjhhhjjk",
    "hjWWvvkhhhhhhhhk",
    ".kkkkkkkkkkkkkk.",
    "................",
    "................",
], old=["HOL-XMAS-25"])

# --- cupcake palette swaps: same grid as FOOD-CUPCAKE (food.py), new legends ------------------------------------------------
from lib import SPRITES
_CUP = SPRITES["FOOD-CUPCAKE"]["grid"]
_CHERRY = {k: CHERRY[k] for k in "KCcwg"}
def _cup(frost, liner, top=_CHERRY):
    return {**dict(zip("PpqQ", frost)), **dict(zip("LlmM", liner)), **top}
sprite("FOOD-CUPCAKE-RWB", "Cupcake, red white blue", "Sweets",
       _cup(("#8d86b8", "#c4c0e2", "#f0eef8", "#ffffff"), ("#1d2a66", "#2c52a8", "#4a86d8", "#86c0f4")), _CUP,
       old=["HOL-PRES-45"])
sprite("FOOD-CUPCAKE-SPRING", "Cupcake, spring", "Sweets",
       _cup(("#3f7a3a", "#6cbf48", "#a4e070", "#dcf7b0"), ("#7a4a12", "#c98a14", "#ffd23f", "#fff2a8")), _CUP,
       old=["HOL-GF-49"])
sprite("FOOD-CUPCAKE-PEPPERMINT", "Peppermint cupcake", "Sweets",
       _cup(("#8d86b8", "#c4c0e2", "#f0eef8", "#ffffff"), ("#6e1830", "#b8263a", "#e8484a", "#ff8a72")), _CUP,
       old=["HOL-XMAS-26"])
sprite("FOOD-CUPCAKE-PUMPKIN", "Pumpkin cupcake", "Sweets",
       _cup(("#a8542a", "#e08a4a", "#f6b878", "#ffe0b8"), ("#3a1d16", "#5e3020", "#8a4a2c", "#b8754a"),
            {"K": "#7a2e14", "C": "#c0561e", "c": "#ff9a3a", "w": "#ffd08a", "g": "#5b7f2c"}), _CUP,
       old=["HOL-TG-36"])
sprite("FOOD-CUPCAKE-REDVELVET", "Red velvet cupcake", "Sweets",
       _cup(("#8d86b8", "#c4c0e2", "#f0eef8", "#ffffff"), ("#4e1024", "#8a1a2e", "#b82a36", "#d84a48")), _CUP,
       old=["HOL-JUN-24"])

# "Cupcake" (PROP-439) is the plain pink cupcake: it belongs on FOOD-CUPCAKE, not on a new sprite.
if "PROP-439" not in SPRITES["FOOD-CUPCAKE"]["old"]:
    SPRITES["FOOD-CUPCAKE"]["old"].append("PROP-439")
