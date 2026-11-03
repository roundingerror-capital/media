"""FOOD · Meals & snacks. Same method and shared ramps as lib/food.py (Kirby Super Star / Stardew / SotN item icons):
16 px, fills ~80% of the box, one main colour + one accent, hue-shifted ramps, chunky highlight top-left, outline in each
material's own darkest tone. Light: top-left. Plated dishes share one plate ellipse (PLATE) with purple-shifted shadows."""
from lib import sprite
from lib.food import *

# ---- extra ramps for this set (reuse lib.food's BUN / DOUGH / CHEESE / LETTUCE / TOMATO / PATTY where they fit) ----
MOZZ = {"j": "#8a4e14", **CHEESE, "z": "#fff3a0"}                     # cheese: deep, shadow, base, light
PEP = {"K": "#5e1426", "R": TOMATO["R"], "r": TOMATO["r"]}            # pepperoni
PLATE = {"v": "#45466e", "x": "#9a9cc4", "X": "#dfe2f2", "W": "#fbfcff"}  # one plate for the whole set
CARD = {"Q": "#5a3422", "q": "#9a6a40", "c": "#c99a62", "C": "#e8c48a", "H": "#fbe6b8"}   # cardboard
SEED = {"k": "#2b2238", "i": "#fff6e0"}                               # poppy, sesame
CREAM = {"V": "#7c6a74", "c": "#c4b4b2", "w": "#ece2d8", "W": "#fffaf2"}  # cream cheese
PRETZ = {"A": "#3a160c", "a": "#6e2e14", "p": "#a8541f", "P": "#d4843a", "h": "#f5b965"}
SALT = {"S": "#f4f6ff"}
SHELL = {"F": "#8a4f12", "f": "#c9861f", "Z": "#f2b84a", "z": "#ffe08a"}  # taco shell (corn)
RICE = {"I": "#565a7e", "i": "#a3a6c8", "w": "#e8e9f4", "W": "#fbfbff"}
SALMON = {"M": "#8a2e2a", "m": "#e0603e", "l": "#ff9a6a", "L": "#ffd6b8"}
NORI = {"V": "#16261f", "v": "#2b4733", "x": "#4f7552"}
BOWL = {"H": "#4e1a2a", "h": "#8e2a32", "a": "#c8443a", "A": "#ec7a52"}
BROTH = {"U": "#9a5418", "u": "#d88a34"}
NOODLE = {"N": "#ffeaa0", "n": "#e8c060"}
EGG = {"W": "#fbfaf4", "w": "#d9d2cc", "Y": "#ffb02e", "y": "#d8761a"}
STICK = {"T": "#6a3a1c", "t": "#b07a44", "s": "#e8be86"}
STEAM = {"~": "#e4e8f6"}
HAM = {"m": "#9a3a52", "M": "#e88a9a", "L": "#ffc2c8"}
SAUS = {"X": "#5a1a1a", "x": "#9a3328", "q": "#cf5a3a", "Q": "#f08a5a"}
HUSK = {"G": "#2c5a24", "e": "#4f9a33", "E": "#8fd14f", "l": "#d4e88a"}
ROAST = {"A": "#4a1c10", "a": "#86391a", "p": "#bf6428", "P": "#e8963e", "h": "#ffd08a"}
BONE = {"b": "#b8aec4", "B": "#fbf6ee"}
POP = {"J": "#a86a1a", "j": "#e0b040", "w": "#fff2a8", "W": "#fffbe6"}
STRIPE = {"K": "#6e1428", "R": "#c42a3a", "r": "#e8504a", "s": "#c9bccc", "S": "#f6f0f2"}
BAG_RED = {"1": "#5e1420", "2": "#a8242e", "3": "#e04a3a", "4": "#ff8a5a", "5": "#ffd0a8"}
BAG_BLUE = {"1": "#1a2458", "2": "#2c4aa0", "3": "#3e7ad8", "4": "#7ab8f4", "5": "#d0ecff"}
WINDOW = {"o": "#8a96b0", "O": "#e4ecf4"}
CHIP = {"F": "#8a4a10", "f": "#e0a020", "Z": "#ffd23f", "z": "#fff09a"}
SAUCE = {"K": "#5e1426", "R": "#a82424", "r": "#e8473c", "w": "#ffb0a0"}
LABEL = {"c": "#b8a898", "L": "#f4ecdc"}
CAP = {"G": "#2c5a24", "e": "#4f9a33", "E": "#8fd14f"}

# ================================================================== pizza
sprite("FOOD-PIZZA-SLICE", "Pizza slice", "Meals", {**DOUGH, **MOZZ, **PEP, **PLATE}, [
    "................",
    "....DDDDDDDD....",
    "..DDBYYBBBBbDD..",
    ".DbBYBBBBbbbbdD.",
    ".DdbbbbbddddddD.",
    ".jzzzZZZZZrRZyj.",
    ".jzzrRZZZrRRKyj.",
    "..jrRRKZZZKKyjdD",
    "..jZKKyZZZZyjdD.",
    "...jZZrRZZyjZD..",
    "..vjZrRRKZjdZjv.",
    ".vXXjZKKyjdDjXv.",
    "vXWXjZZyjdDxXXXv",
    "vXWxxjjdDxxxxXxv",
    ".vXXXxxXXXXXXxv.",
    "..vvvvvvvvvvvv..",
], old=["PROP-051", "PROP-334"])

sprite("FOOD-PIZZA", "Whole pizza", "Meals", {**DOUGH, **MOZZ, **PEP}, [
    "....................",
    ".......DDDDDD.......",
    "....DDDYYYYBBDDD....",
    "..DDYyyrRyyyrRyBDD..",
    ".DYyyzrRRKyrRRKyybD.",
    ".DyzyyzKKZyZKKZyyyD.",
    "DYyzrRyyyZyZyyyrRybD",
    "DYyrRRKZZyyyZZrRRKbD",
    "DBjZKKyyyZyZyyyKKjbD",
    "DBBjjyrrRZyZrrRjjbbD",
    ".DBBBjRKKjjjRKKbbbD.",
    ".DdBBbbbbbbbbbbbbdD.",
    "..DDdbbbbbbbbbbdDD..",
    "....DDDddddddDDD....",
    ".......DDDDDD.......",
    "....................",
], old=["PROP-052"])

sprite("FOOD-PIZZA-BOXES", "Pizza boxes", "Meals", CARD, [
    "................",
    "..QQQQQQQQQQQQQQ",
    "..QHHHCCCCCCCCcQ",
    "..QCCCCCCCCCCccQ",
    "..QHcccccqqccccQ",
    "QQQqqqqqqqqqqqqQ",
    "QHQqqqqqqqqqqqqQ",
    "QCQQQQQQQQQQQQQQ",
    "QHccccqqcccccQ..",
    "QqqqqqqqqqqqqQQQ",
    "QqqqqqqqqqqqqQHQ",
    "QQQQQQQQQQQQQQCQ",
    "..QHcccccccqqccQ",
    "..QqqqqqqqqqqqqQ",
    "..QqqqqqqqqqqqqQ",
    "..QQQQQQQQQQQQQQ",
])

# ================================================================== bagels / pretzel
sprite("FOOD-BAGEL", "Bagel stack", "Meals", BUN, [
    "....OOOOOOO.....",
    "..OOsNNNNNnnO...",
    ".OnsNNOOONNnoO..",
    ".OnNNOoooONnoO..",
    ".OnNnnOOOnnnoO..",
    ".OonNNNNnnnnoOO.",
    "..OoonnnnnoooOnO",
    "...OOOOOOOOOOnoO",
    "...OnNNNnnnnnooO",
    ".OOOonnnnnnnnooO",
    "OnsNOoonnnnnoooO",
    "OnNNnOOOOOOOOOO.",
    "OnNNNNnnnnnoO...",
    "OonnnnnnnnnoO...",
    ".OoooonnnoooO...",
    "..OOOOOOOOOO....",
], old=["PROP-053", "PROP-336"])

sprite("FOOD-BAGEL-CC", "Everything bagel, cream cheese", "Meals", {**BUN, **SEED, **CREAM}, [
    "................",
    ".....OOOOOOOO...",
    "...OOnsNNkNNnOO.",
    "..OnsiNNNNNiNkoO",
    "..OsNNkOOOONNnoO",
    ".OnNNNOooooONnoO",
    ".OnkNnnOOOOnnioO",
    ".OonNNNiNNnknooO",
    ".VOooooooooooOOV",
    "VWWWwWWWWWwwwwcV",
    "VcWWwwWWwwwwwccV",
    ".VVcVVVVVVVcVVV.",
    "OnVcVnnnnnVcVnoO",
    "OnnVNNnnnnnVnooO",
    ".OoonnnnnnnoooO.",
    "...OOOOOOOOOO...",
], old=["PROP-054"])

sprite("FOOD-PRETZEL", "Street pretzel", "Snacks", {**PRETZ, **SALT}, [
    "................",
    "..AAAAA..AAAAA..",
    ".AhPPSpAApSPPpA.",
    "AhP...pPPp...ppA",
    "APA...APPA...apA",
    "PPA..ApSaPA..apA",
    "PPA.ApaAApaA.apA",
    "hPA.ApA..AppAapA",
    "hPpApA....ApApaA",
    ".hPPpA....ApppA.",
    ".APSPA....ApSpA.",
    "..APPpppppppppA.",
    "...APPPPSPpppA..",
    "....AaaaaaaaA...",
    ".....AAAAAAA....",
    "................",
], old=["PROP-055", "PROP-335"])

# ================================================================== world
sprite("FOOD-TACO", "Taco", "Meals", {**SHELL, **LETTUCE, **TOMATO, "T": PATTY["T"], "t": PATTY["t"], "u": PATTY["u"], "y": CHEESE["y"], "C": CHEESE["Z"]}, [
    "................",
    "....GEEG.GEEG...",
    "..GEEeEGGEeEEG..",
    ".GEeRrGEEeRrEeG.",
    ".GeRRrCCeGRRCCG.",
    "GeuTCyCtuCCuTyeG",
    "FzzzzzCZZZZZZffF",
    "FzZZZZZyZZZZZffF",
    "FzZZfZZZZZfZZffF",
    ".FZZffZZZZffZfF.",
    ".FZZZZZZZZZZffF.",
    "..FZZZZZfZZZfF..",
    "...FfZZZZZffF...",
    "....FFffffFF....",
    "......FFFF......",
    "................",
], old=["PROP-056"])

sprite("FOOD-NIGIRI", "Nigiri", "Meals", {**RICE, **SALMON}, [
    "................",
    "................",
    "................",
    ".....MMMMMM.....",
    "...MMlLLlllmMM..",
    "..MlLllLLlllmmM.",
    ".MlLlllLLllLmmmM",
    "MlLllLLlllLLmmmM",
    "MlllLLllLLlmmmMM",
    "MmmMMMMMMMMMMMwI",
    "MMwWWwwiiwwwwwiI",
    "IwWWwwwwwwiiwwiI",
    ".IwwiiwwwwwwwiI.",
    "..IiwwwwiiwwiI..",
    "...IIIIIIIIII...",
    "................",
], old=["PROP-057"])

sprite("FOOD-MAKI", "Maki rolls", "Meals", {**RICE, **NORI, **SALMON, "e": LETTUCE["e"], "E": LETTUCE["E"]}, [
    "................",
    "........VVVVVV..",
    "......VWWWWWwiV.",
    ".....VWWmlEwwwiV",
    ".....VWwMmewwwiV",
    ".....VxiwwwwwiiV",
    "..VVVVVVvVvvvvvV",
    ".VWWWWWwiVvvvvV.",
    "VWWWlLEwwiVvVV..",
    "VWWmlmeEwwiV....",
    "VxWwMmeewwiV....",
    "VxiwwwwwwiiV....",
    "VxvvvvvvvvvV....",
    "VxvvvvvvvvvV....",
    ".VvvvvvvvvV.....",
    "..VVVVVVVV......",
], old=["PROP-058"])

sprite("FOOD-RAMEN", "Ramen", "Meals", {**BOWL, **BROTH, **NOODLE, **EGG, **STICK, **STEAM, "e": LETTUCE["e"], "E": LETTUCE["E"]}, [
    "..........sT..sT",
    "..........sT..sT",
    ".........sT..sT.",
    ".........sT..sT.",
    "....HHHHsTHHsT..",
    "..HHAAAAsTaasTH.",
    ".HAuNNnNsTuWWwuH",
    "HAuNnnNNuuWYYwuH",
    "HauNNnnNNuWYywEH",
    "HhAuuuuueEuwwuhH",
    "HhAAAaaaaaaaahhH",
    ".HAaaaaaaaaaahH.",
    ".HhAaaaaaaaahhH.",
    "..HhaaaaaaahhH..",
    "...HHhhhhhhHH...",
    ".....HHHHHH.....",
], frames=[{(4, 3): "~", (3, 2): "~", (3, 1): "~", (4, 0): "~", (7, 2): "~", (6, 1): "~", (6, 0): "~"},
           {(3, 3): "~", (4, 2): "~", (4, 1): "~", (3, 0): "~", (6, 2): "~", (7, 1): "~", (7, 0): "~"}],
   ticks=[5, 5], old=["PROP-059", "PROP-060"])

sprite("FOOD-SANDWICH", "Sandwich", "Meals", {**DOUGH, **LETTUCE, **TOMATO, **CHEESE, **HAM, "k": "#6e1830"}, [
    "....DDDDDDDDDD..",
    "...DbYYYBBBBBbD.",
    "..DbYBBBBBBBBbD.",
    ".DbbbbbbbbbbbbD.",
    ".DddddddddddddD.",
    "GEEeEEEeEEEeEEeG",
    ".GeGGeeGGeGGeeGG",
    "..RrrrrRkRrrrrrR",
    "ZZZRRRRkZkRRRRRk",
    "ZZZZZZZZZZZZZyk.",
    "yZZZZZZZZZZZyy..",
    "yyLLMMMMMMLMMMm.",
    ".ymmmMMmmmmMmmmm",
    ".DbYYBBBBBBBBbD.",
    ".DdbbbbbbbbbbdD.",
    "..DDDDDDDDDDDD..",
], old=["PROP-063"])

sprite("FOOD-HOTDOG", "Hot dog", "Meals", {**BUN, **SAUS, "H": "#ffc8a0", "y": CHEESE["y"], "Z": CHEESE["Z"]}, [
    "................",
    "................",
    "....OOOOOOOO....",
    "..OOnNNNNNNnOO..",
    ".OnNNNNNNNnnnoO.",
    ".XXXXXXXXXXXXXX.",
    "XQQZZQQZZqqZZqxX",
    "XqZqqZZqqZZqqZxX",
    "XxOsNNNNNNNnnOxX",
    ".OnNNNNNNnnnnoO.",
    "OnNNNNNNNnnnnooO",
    "OnnNNNnnnnnnoooO",
    ".OoonnnnnnnoooO.",
    "..OOOOOOOOOOOO..",
    "................",
    "................",
], frames=[None, {(1, 6): "H", (2, 6): "H"}], ticks=[24, 3],
   old=["PROP-082", "HOL-MEM-26", "HOL-MEM-27", "HOL-JUN-31", "HOL-IND-31", "HOL-LAB-33"])

sprite("FOOD-CORN", "Corn on the cob", "Meals", {**MOZZ, **HUSK}, [
    ".....jjjjjj.....",
    "....jzzzZZZj....",
    "...jzzZZZZZyj...",
    "...jzzyyZyZyj...",
    "...jZZzZyjyyj...",
    "...jyyZZZZjjj.G.",
    ".G.jzzyyZyZyjGG.",
    ".GGjZZzZyjyyGEG.",
    ".GEGyyZZZZjGeEG.",
    "..GEeGyyZyGeeEG.",
    "..GlEeGZyjGeeG..",
    "...GlEeGyGeeG...",
    "....GlEeGeeG....",
    ".....GlEeeGG....",
    "......GEeeG.....",
    ".......GGG......",
], old=["PROP-090", "HOL-MEM-29", "HOL-JUN-32", "HOL-IND-33", "HOL-LAB-35", "HOL-TG-10", "HOL-TG-11"])

sprite("FOOD-ROLL", "Dinner roll", "Meals", BUN, [
    "................",
    "................",
    "................",
    "......OOOOO.....",
    "...OOOnNNNnOO...",
    "..OnNsNNooNnnO..",
    ".OnssNNsooNnnoO.",
    ".OnsNNNNsonnnoO.",
    "OnNNNNNNNNsonooO",
    "OnNNNNNNnnnnoooO",
    "OnnNNNnnnnnoooOO",
    "OonnnnnnnnooooO.",
    "OoooonnnooooOOO.",
    ".OOooooooooOOO..",
    "...OOOOOOOOO....",
    "................",
], old=["PROP-098", "HOL-TG-21"])

sprite("FOOD-TURKEY", "Roast turkey", "Meals", {**ROAST, **BONE, **PLATE, "G": LETTUCE["G"], "e": LETTUCE["e"], "E": LETTUCE["E"]}, [
    "................",
    ".....AAAAAA.....",
    "...AAhhPPPpaA...",
    "..AhhPPPPPppaA..",
    ".AhPPPPPPpppaaA.",
    ".AhPPPPPPpppaaA.",
    "BBAPPPPPPpppaABB",
    "BbAAAPPppppAAAbB",
    ".AhPPAppppAhPPA.",
    "AhPPPpAaaAhPPppA",
    "AhPPppAaaAPPpaaA",
    "vAppaAAAAAAppaAv",
    ".vAAAXxxxxxAAAv.",
    "vXWXGeExxxxxeEGv",
    ".vXXXXXXXXXXXxv.",
    "..vvvvvvvvvvvv..",
], old=["HOL-TG-01", "HOL-TG-02"])

# ================================================================== snacks
sprite("FOOD-POPCORN", "Popcorn", "Snacks", {**POP, **STRIPE}, [
    "....JJJ..JJJ....",
    "..JJWWwJJWwwJJ..",
    ".JWWwwjJWWwjjwJ.",
    ".JWwwjJWWwwjJjwJ",
    "JWWwjjJWwwjjJwjJ",
    "JwwjJJWwwjjJWwjJ",
    "KSSRRSSrrSSRRssK",
    "KSSRRSSrrSSRRssK",
    ".KSSRRSSrRSSRsK.",
    ".KSSRRSSrRSSRsK.",
    ".KSSRRSSrRSSRsK.",
    "..KSRRSSrRSSRK..",
    "..KSRRSSrRSSRK..",
    "..KSRRSSrRSSRK..",
    "..KsRRssRRssRK..",
    "...KKKKKKKKKK...",
], old=["PROP-077"])

_CHIPS = [  # crimped pillow bag; the window shows one corn chip sitting low
    "...1441144114...",
    "...1111111111...",
    "..134533333221..",
    ".13453222222221.",
    ".1345OOOOOOOo21.",
    ".1345OOOOOOOo21.",
    ".1345OOOOOOOo21.",
    ".1345OOOOzOOo21.",
    ".1345OOOzZfOo21.",
    ".1345OOzZZffo21.",
    ".1345OzZZZfff21.",
    ".1345FFFFFFFF21.",
    ".13453222222321.",
    "..134433333221..",
    "...1111111111...",
    "...1441144114...",
]
sprite("FOOD-CHIPS", "Bag of chips", "Snacks", {**BAG_RED, **WINDOW, **CHIP, "K": BAG_RED["1"]}, _CHIPS, old=["PROP-068"])
sprite("FOOD-CHIPS-BLUE", "Chips, blue bag", "Snacks", {**BAG_BLUE, **WINDOW, **CHIP, "K": BAG_BLUE["1"]}, _CHIPS, old=["PROP-069"])

sprite("FOOD-HOTSAUCE", "Hot sauce", "Snacks", {**SAUCE, **LABEL, **CAP}, [
    "......GGGG......",
    ".....GEEeeG.....",
    ".....GeeeGG.....",
    "......KrRK......",
    "......KwRK......",
    ".....KrwrRK.....",
    "....KrwrrrRK....",
    "...KrwwrrrRRK...",
    "...KrwrrrrrRK...",
    "...KLLLLLLccK...",
    "...KLLLLLLccK...",
    "...KLLLLLLccK...",
    "...KwrrrrrRRK...",
    "...KrrrrrRRRK...",
    "...KRRRRRRRRK...",
    "....KKKKKKKK....",
], old=["PROP-078"])
