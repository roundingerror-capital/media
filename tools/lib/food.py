"""FOOD · Food & drink. 16 px icons (Kirby Super Star / Stardew method): fills ~80% of the box, one main colour + one accent,
3-4 tone hue-shifted ramp + one highlight cluster top-left, outline in the item's own darkest tone. Light: top-left."""
from lib import sprite

# shared ramps (reused across the whole set so everything belongs together)
FROST_PINK = {"P": "#7d2f5f", "p": "#c04f87", "q": "#ee82b0", "Q": "#ffc8dc"}
CHERRY = {"K": "#6e1830", "C": "#b8263a", "c": "#e8484a", "w": "#ffe9da", "g": "#5b7f2c"}
LINER_MINT = {"L": "#2b4f5e", "l": "#3e8384", "m": "#67b9ad", "M": "#a6e0cb"}
DOUGH = {"D": "#6b3a1f", "d": "#a8642e", "b": "#d89a52", "B": "#f2c47e", "Y": "#fff0c8"}
CHOC = {"k": "#3a1d16", "h": "#5e3020"}

sprite("FOOD-CUPCAKE", "Cupcake", "Sweets", {**FROST_PINK, **CHERRY, **LINER_MINT}, [
    "........gg......",
    ".......cwC......",
    "......ccccK.....",
    "......QCCKP.....",
    ".....QqqqppP....",
    "...QqppppppPP...",
    "...QqqqqqqqppP..",
    "...qqqqqqqpppP..",
    ".QQqpppppppppPP.",
    ".QqqqqqqqqqqppP.",
    ".PqPqqPqqPqqpPP.",
    "..LMMlMMlMMllL..",
    "..LMMlMMlMMllL..",
    "...LMlMMlMllL...",
    "...LMlMMlMllL...",
    "....LLLLLLLL....",
], frames=[None, {(8, 1): "w", (7, 1): "c"}], ticks=[24, 3], old=["PROP-083"])

sprite("FOOD-COOKIE", "Chocolate chip cookie", "Sweets", {**DOUGH, **CHOC}, [
    "................",
    ".....DDDDDD.....",
    "...DdBBYBkhdD...",
    "..DbBkhBBBBbbD..",
    "..dBBBBBkkBbhdD.",
    ".DbBkkBBkhbbbbdD",
    ".DbBkhBbbbbkhbdD",
    ".DbBBbbbkkbbbbdD",
    ".DkhbbbbkhbbbkdD",
    ".DbbbkkbbbbbbhdD",
    ".Ddbbkhbbbkkbbd.",
    "..DdbbbbbbkhbdD.",
    "..DkhbbkkbbbddD.",
    "...DDddkhdddDD..",
    ".....DDDDDDD....",
    "................",
], old=["PROP-091"])

BUN = {"O": "#5a2c14", "o": "#9a5223", "n": "#d0843b", "N": "#f0b464", "s": "#fff4dc"}
LETTUCE = {"G": "#2c5a24", "e": "#4f9a33", "E": "#8fd14f"}
CHEESE = {"y": "#c98a14", "Z": "#ffd23f"}
PATTY = {"T": "#2e1612", "t": "#5a2a1c", "u": "#86452c"}
TOMATO = {"R": "#a82424", "r": "#e8473c"}

sprite("FOOD-BURGER", "Burger", "Meals", {**BUN, **LETTUCE, **CHEESE, **PATTY, **TOMATO}, [
    ".....OOOOOO.....",
    "...OnNsNNNnoO...",
    "..OnNNsNNNNnoO..",
    ".OnsNNNNNNnnnoO.",
    ".OoonnnnnnnooOO.",
    "GEeEeGEEeEeGEe..",
    ".GeGGeeGGeeGeGGG",
    "..ZrrRrrZrrRrrR.",
    ".ZZRRRRZZZRRRRZy",
    "ZZyZZZZZZZZZZyy.",
    "y.ZTuuuuuTuuuyZ.",
    "..TtuuttuttuuTT.",
    "..TTttTTttTTTTT.",
    ".OnnNNNnnnnnooO.",
    ".OoonnnnnnoooOO.",
    "..OOOOOOOOOOOO..",
], old=["PROP-081"])
