"""FOOD · Fruit & veg. 16 px icons, same method as lib/food.py (Kirby Super Star / Stardew): fills ~80% of the box, one main
colour + one accent (green stem/leaf), 3-4 tone hue-shifted ramp + chunky highlight top-left, outline in the item's own darkest
tone (sel-out: the lit top-left edge uses the shadow tone, the far edge the darkest). Light: top-left."""
from lib import sprite
from lib.food import *

# ---- shared ramps -------------------------------------------------------------------------------------------------------
LEAF = {"G": "#2c5a24", "g": "#4f9a33", "l": "#8fd14f"}                   # same greens as the burger lettuce
STEM = {"s": "#5a3418", "S": "#8a5a2a"}
APPLE_RED = {"A": "#5c1428", "a": "#a8243a", "r": "#d8383a", "R": "#f06a48", "h": "#ffd8c0"}
APPLE_GRN = {"A": "#24481c", "a": "#4e8a24", "r": "#80bc2c", "R": "#b4dc4a", "h": "#f2fcc0",
             "G": "#2c5a24", "g": "#3f7f2a", "l": "#6aba3c"}
BANANA = {"Y": "#7a4c14", "y": "#d09a22", "b": "#f4cc3a", "B": "#fff08a", "T": "#4a2a14", "t": "#7a4a20"}
AVO = {"K": "#1c3418", "k": "#3e6a26", "f": "#9cc848", "F": "#dfe88a", "E": "#f8f8c8"}
PIT = {"D": "#4e2614", "d": "#7e4220", "b": "#b06a34", "B": "#d89a5a"}
MELON_FLESH = {"M": "#7a1834", "m": "#c4304a", "n": "#ee4f58", "N": "#ff8676", "z": "#2a1622"}
MELON_RIND = {"X": "#1a3c22", "V": "#2f7430", "v": "#5ea83a", "L": "#9ad45a", "w": "#eef6c8", "W": "#c8e49a"}
CHERRY2 = {"K": "#5a1028", "C": "#a81e36", "c": "#dc3a3e", "e": "#ff7058", "w": "#ffe2d4"}
BERRY = {"K": "#5e1230", "C": "#a81e3e", "c": "#e23a4a", "e": "#ff765e", "y": "#ffe08a", "w": "#ffe2d4"}
LEMON = {"Y": "#7a5814", "y": "#d8a424", "b": "#f8d838", "B": "#fff27e", "h": "#fffbd8"}
ORANGE = {"O": "#6a2814", "o": "#b8501c", "n": "#e87a20", "N": "#ffa84a", "h": "#ffd890"}
PUMP_STEM = {"T": "#3e4a18", "t": "#6e7e2a", "i": "#a4ae46"}
CREAM = {"O": "#625a72", "o": "#aaa2b6", "n": "#e2dcd6", "N": "#f6f2ea", "h": "#fffcf4"}
WICKER = {"D": "#4e2614", "d": "#8a4c22", "b": "#c47c38", "B": "#eab062"}
CRAN = {"J": "#44081e", "j": "#86123a", "c": "#bc2648", "C": "#e65466", "w": "#ffc0bc"}
PLATE = {"P": "#5c6280", "p": "#a8b0c6", "q": "#dfe4ee", "Q": "#f8faff"}
GRAVY = {"k": "#3a1c10", "h": "#6e3a1c", "H": "#a2602e"}
GRAPE = {"U": "#2e1640", "u": "#5e2f7a", "v": "#9a5ab8", "V": "#d0a0e6"}
CLOTH = {"x": "#8a1a2a", "X": "#d8323a", "o": "#fff0e4"}

# ---- apples (one grid, two legends) ------------------------------------------------------------------------------------
APPLE = [
    ".......s...ggG..",
    ".......s.gllgG..",
    "........sGgG....",
    "...aaaa..aaaA...",
    "..aRRRRaaRrrrA..",
    ".aRhhRRRRRrrrrA.",
    ".aRhhRRRRrrrraA.",
    ".aRhRRRRrrrrraA.",
    ".aRRRRRrrrrrraA.",
    ".aRRRrrrrrrraaA.",
    ".arRrrrrrrrraaA.",
    ".arrrrrrrrraaaA.",
    "..ArrrrrrraaaA..",
    "..AarrrrraaaaA..",
    "...AAaaaaaaAA...",
    ".....AAAAAA.....",
]
sprite("FOOD-APPLE", "Apple", "Fruit & veg", {**APPLE_RED, **LEAF, **STEM}, APPLE, old=["PROP-064"])
sprite("FOOD-APPLE-GREEN", "Green apple", "Fruit & veg", {**APPLE_GRN, **STEM}, APPLE, old=["PROP-065"])

sprite("FOOD-BANANA", "Banana", "Fruit & veg", BANANA, [
    "............TT..",
    "............tT..",
    "...........yBbY.",
    "...........yBbyY",
    "..........yBBbyY",
    "..........yBbbyY",
    ".........yBBbbyY",
    ".........yBbbyY.",
    "........yBBbbyY.",
    ".......yBBbbyYY.",
    ".....yyBBbbbyY..",
    "...yyBBBbbbyY...",
    ".TBBbbbbbbyY....",
    "TTyybbbbyyYY....",
    "..YYYYYYYY......",
    "................",
], old=["PROP-066"])

sprite("FOOD-AVOCADO", "Avocado, halved", "Fruit & veg", {**AVO, **PIT}, [
    "......KKKK......",
    ".....KkffkK.....",
    "....KkfEEfkK....",
    "....KkEFFfkK....",
    "...KkfEFFFfkK...",
    "...KkfFFFFfkK...",
    "..KkfFFFFFFfkK..",
    "..KkfFFFFFFfkK..",
    ".KkfFFDDDDFFfkK.",
    ".KkfFDBBbdDFfkK.",
    ".KkfFDBbbdDFfkK.",
    ".KkfFDbbddDFfkK.",
    ".KkffDdddDDffkK.",
    "..KkffDDDDffkK..",
    "...KkffffffkK...",
    ".....KKKKKK.....",
], old=["PROP-067"])

sprite("FOOD-WATERMELON-SLICE", "Watermelon slice", "Fruit & veg", {**MELON_FLESH, **MELON_RIND}, [
    ".......MM.......",
    "......MNmM......",
    "......MNnM......",
    ".....MNnnmM.....",
    ".....MNznmM.....",
    "....MNNznnmM....",
    "....MNnnnnmM....",
    "...MNNznnznmM...",
    "...MNznnnnzmM...",
    "..MNNnnnnnnnmM..",
    "..MNznnznnnzmM..",
    ".MNznnnznnnnzmM.",
    "LwwwwwwwwwwwWWWX",
    "VLLvvvvvvvvvvVVX",
    ".XvvvvvvvvvvVVX.",
    "...XXXXXXXXXX...",
], old=["HOL-MEM-30", "HOL-JUN-28", "HOL-IND-34", "PROP-089"])

MELON_WHOLE = {"X": "#16321c", "S": "#2a5e2c", "q": "#448e34", "v": "#6cb440", "L": "#a4dc62", "w": "#e4f8b4"}
sprite("FOOD-WATERMELON", "Watermelon, whole", "Fruit & veg", MELON_WHOLE, [
    "................",
    "................",
    ".....SSSSXX.....",
    "...SLLLLLvvvX...",
    "..SLLSSLLSSvSX..",
    ".SLSSSSSSSSSSvX.",
    "SSSwwLLvvvvvvXXX",
    "SLLwLvvvvvvvvqqX",
    "SSSSSSSSSSSXXXXX",
    "SvSSvvSSvvXXqqXX",
    "SSSvvvvvvqqqqXXX",
    ".SSSSSSXXXXXXXX.",
    "..XqSSqqXXqqXX..",
    "...XqqqqqqqqX...",
    ".....XXXXXX.....",
    "................",
], old=["HOL-JUN-29"])

sprite("FOOD-CHERRIES", "Cherries", "Fruit & veg", {**CHERRY2, **LEAF, "s": "#5b7f2c"}, [
    "..........GGG...",
    ".........sllgG..",
    ".........sGGG...",
    "........s.s.....",
    ".......s..s.....",
    "......s....s....",
    ".....s...CCKK...",
    "....s...CwwccK..",
    "..CCKK.CewwcccK.",
    ".CwwccKCewcccCK.",
    "CewwcccKccccCCK.",
    "CewcccCKcccCCCK.",
    "CccccCCKKcCCCK..",
    "CcccCCCK.KKKK...",
    ".KcCCCK.........",
    "..KKKK..........",
], old=["PROP-096", "HOL-PRES-13"])

sprite("FOOD-STRAWBERRY", "Strawberry", "Fruit & veg", {**BERRY, **LEAF}, [
    "........G.......",
    ".......gG.......",
    "..GlllgggggggG..",
    "..GGecggGccGGG..",
    "..CewweGccccCK..",
    ".CewweycccycCCK.",
    ".CeweccccccCCCK.",
    ".CeeycccyccCyCK.",
    "..CeccccccCCCK..",
    "..CeccyccCyCCK..",
    "...CcccccCCCK...",
    "...CcyccCyCCK...",
    "....KcccCCCK....",
    ".....KcyCCK.....",
    "......KCCK......",
    ".......KK.......",
])

sprite("FOOD-LEMON", "Lemon", "Fruit & veg", {**LEMON, **LEAF, **STEM}, [
    "................",
    "..........ggG...",
    ".........sgllG..",
    ".....yyyyYY.....",
    "...yBBBBbbbYY...",
    "..yBhhBBbbbbyY..",
    ".yBhhBBbbbbbbyY.",
    ".yBhBbbbbbbbbyY.",
    "yBBBbbbbbbbbbyyY",
    "YbBbbbbbbbbyyyyY",
    ".YbbbbbbbbbyyyY.",
    ".YbbbbbbbbyyyyY.",
    "..YybbbbbyyyyY..",
    "...YYyyyyyyYY...",
    ".....YYYYYY.....",
    "................",
])

sprite("FOOD-CARROT", "Carrot", "Fruit & veg", {**ORANGE, **LEAF}, [
    ".........lg..lgG",
    ".........ggGlggG",
    "..........GglgG.",
    ".........ooGgGG.",
    "........oNhhnO..",
    ".......oNhNnnO..",
    ".......oNNnnoO..",
    "......oNNnooO...",
    ".....oNNnnnoO...",
    ".....oNnooO.....",
    "....oNnnoO......",
    "...oNnooO.......",
    "...oNnO.........",
    "..onoO..........",
    "..oO............",
    ".oO.............",
], old=["PROP-097", "HOL-GF-36"])

PUMPKIN = [
    "................",
    ".........tT.....",
    "........tiT.....",
    ".......tiT......",
    "...oooo tTOOOO...".replace(" ", ""),
    ".onNNoNNnonnooO.",
    "onohNoNNnonnooOO",
    "onohhoNNnonnooOO",
    "onohNoNnnonnooOO",
    "onoNNoNnnonnooOO",
    "onoNnoNnnonoooOO",
    "oooNnonnoonooOOO",
    "OoonnonnoooooOOO",
    ".OonoonoooooOOO.",
    "..OOooooooooOO..",
    "....OOOOOOOO....",
]
sprite("FOOD-PUMPKIN", "Pumpkin", "Fruit & veg", {**ORANGE, **PUMP_STEM}, PUMPKIN, old=["HOL-TG-07"])
sprite("FOOD-PUMPKIN-WHITE", "White pumpkin", "Fruit & veg", {**CREAM, **PUMP_STEM}, PUMPKIN, old=["HOL-TG-09"])
sprite("FOOD-PUMPKIN-SMALL", "Pumpkin, small", "Fruit & veg", {**ORANGE, **PUMP_STEM}, [
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "........tT......",
    ".......tiT......",
    "....oootTOOO....",
    "...ohoNNnonnO...",
    "..ohhoNNnonnoO..",
    "..ohNoNnnonnoO..",
    "..oNNoNnnonooO..",
    "..OnnonnoooooO..",
    "...OnonoooooO...",
    "....OOOOOOOO....",
], old=["HOL-TG-08"])

sprite("FOOD-CRANBERRY", "Cranberry sauce", "Fruit & veg", {**CRAN, **PLATE}, [
    "................",
    ".....JJJJJJ.....",
    "....JCCwwCcJ....",
    "...JjCCCCCcjJ...",
    "...JCjjjjjjjJ...",
    "...JCwcccccjJ...",
    "...JCwCCCCcjJ...",
    "...JjjccccjjJ...",
    "...JCwjjjjcjJ...",
    "...JCwCCCCcjJ...",
    "...JjjccccjjJ...",
    ".PPJCCjjjjcjJPP.",
    "PpqJCcccccjjJqpP",
    "PpqQJJJJJJJJpppP",
    ".PpqqqqqqqqqqpP.",
    "...PPPPPPPPPP...",
], old=["HOL-TG-20"])

STEAM = {"Z": "#f2eef8"}
sprite("FOOD-GRAVY", "Gravy boat", "Fruit & veg", {**PLATE, **GRAVY, **STEAM}, [
    "................",
    "................",
    "................",
    "................",
    "PP..............",
    "PHPPPPPPPPPPP...",
    ".PhHHHHHHhhkPPP.",
    "..PQQQQQqqqqpP.P",
    "...PqQQqqqqppP.P",
    "....PqqqqqpppPP.",
    ".....PppppppP...",
    "......PqqpP.....",
    "..PPPPPPPPPPPP..",
    ".PqQQQQQqqqqqpP.",
    "..PpppppppppppP.",
    "...PPPPPPPPPP...",
], frames=[{(6, 3): "Z", (6, 2): "Z", (7, 1): "Z", (10, 3): "Z", (10, 2): "Z", (9, 1): "Z"},
           {(7, 3): "Z", (7, 2): "Z", (6, 1): "Z", (9, 3): "Z", (9, 2): "Z", (10, 1): "Z"}], ticks=[6, 6], old=["HOL-TG-19"])

sprite("FOOD-CORNUCOPIA", "Cornucopia", "Fruit & veg", {**WICKER, "k": "#2a140c", **APPLE_RED, **GRAPE, **ORANGE, **PUMP_STEM}, [
    "..............D.",
    "..............bD",
    "...DDBBDD....DbD",
    "..DBkkBBBDD..DBD",
    ".DBkkkdbBBBDDbD.",
    ".DBkkkdbbBbBBbD.",
    ".DBkkkdbbdbbdbD.",
    ".DBkkkdbbdbbdD..",
    ".DBkkkdbbdbdD...",
    ".aaAAkdddbddD...",
    "aRhrrAddddD.t...",
    "aRrrrAVuVuoNoO..",
    "arrraAuUuUNhnoO.",
    "arraaAVuVuNnnoO.",
    ".AAAA.uUuUnnooO.",
    ".......VuU.OOO..",
], old=["HOL-TG-12"])

sprite("FOOD-HARVEST-BASKET", "Harvest basket", "Fruit & veg", {**WICKER, **APPLE_RED, **GRAPE, **ORANGE, **PUMP_STEM, **LEAF, **STEM}, [
    "........s.......",
    ".....Gl.s.......",
    "...t.GgaaA.U....",
    "..oNoOaRhrAVuU..",
    ".oNhNnaRrrAuUVu.",
    "oNNnnoarraAVuuU.",
    "oNnnnoarraAuUVuU",
    "onnnooAAAAAVuuUU",
    "DBBBBBBBBBBBbbbD",
    ".DbbddbbddbbddD.",
    ".DbbddbbddbbddD.",
    "..DddbbddbbddD..",
    "..DddbbddbbddD..",
    "..DbbddbbddbbD..",
    "...DddbbddbbD...",
    "...DDDDDDDDDD...",
], old=["HOL-TG-34"])

sprite("FOOD-PICNIC-BASKET", "Picnic basket", "Fruit & veg", {**WICKER, **CLOTH}, [
    ".....DDDDDD.....",
    "....DBBBBbbD....",
    "...DBD....DdD...",
    "...DbD....DdD...",
    "...DbD....DdD...",
    ".DDDDDDDDDDDDDD.",
    "DBBBBBBBBBBbbbbD",
    "DbbbbbbbbbbddddD",
    "DXXooXXooXXooXXD",
    "DxXXooXXbbddbbdD",
    "DbxXXbbddbbddbbD",
    "DddbxddbbddbbddD",
    "DddbbddbbddbbddD",
    "DbbddbbddbbddbbD",
    "DbbddbbddbbddddD",
    ".DDDDDDDDDDDDDD.",
], old=["HOL-GF-18"])
