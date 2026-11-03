"""WEAR · Clothing & accessories. Glasses (the star of the set), hats, bows & bits.
Method (rec-marketing-pixel-art): hand-drawn grids at final size, light top-left, hue-shifted ramps shared across the set,
sel-out in each material's own darkest tone (never black), chunky glints on glass and metal.
Scale: glasses are 20-24 px wide so they sit across Theo's eyes (his eye line spans x 9..31 of his 41 px sprite);
hats are 20-28 px wide to perch on his 33 px head; bows & bits are 16 px hand-held icons.
Glasses animate a diagonal glint that sweeps each lens (pixel overrides computed per lens; the lens itself is never moved)."""
from lib import sprite

# ---------------------------------------------------------------- shared ramps
INK = {"K": "#1d1a33", "k": "#332d50", "j": "#5f5784", "J": "#9a92c0"}            # black plastic / silk
SMOKE = {"L": "#1f2747", "l": "#36466e", "m": "#557aa4"}                           # dark lens
GLINT = {"w": "#f6fbff", "v": "#a9cdea"}                                           # glass glint (hi, soft)
GOLD = {"o": "#76401a", "G": "#d4952e", "y": "#ffe08a", "Y": "#fff6cc"}            # gold wire / metal
SILV = {"s": "#474c72", "S": "#9aa4c2", "z": "#eef2fa"}                            # silver wire
RED = {"P": "#5e1430", "R": "#b0283c", "r": "#e8484a", "q": "#ff8a72"}             # red cloth / plastic
BLUE = {"N": "#17205a", "n": "#2c4aa6", "c": "#4a82e0", "C": "#92c4f8", "H": "#dcefff"}
SNOW = {"V": "#7d7aa6", "W": "#fbf8ff", "x": "#cac6e4"}                            # white fur / cotton
FELT = {"D": "#3e2214", "d": "#6e3e1e", "b": "#a8642e", "B": "#d89a52", "E": "#f2c47e"}  # brown felt / leather
GREEN = {"F": "#163a2c", "f": "#2a6a3a", "g": "#48a043", "h": "#8ad45a"}
PINK = {"Q": "#6e1a4e", "p": "#c43a7a", "u": "#f070a8", "U": "#ffbcd8"}


def _flood(grid, seed, chars):
    w, h = len(grid[0]), len(grid); out = set(); st = [seed]
    while st:
        x, y = st.pop()
        if (x, y) in out or not (0 <= x < w and 0 <= y < h) or grid[y][x] not in chars: continue
        out.add((x, y)); st += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    return out


def sweep(grid, seeds, chars, steps, hi="w", lo="v"):
    """Glint frames: a 2 px '/' band (hi) with a 1 px soft trailing edge (lo) moves down-right across each region.
    Regions are flood-filled from seeds over `chars` (so the band stays inside the lens). Returns override dicts."""
    regs = []
    for s in seeds:
        r = _flood(grid, s, chars); regs.append((r, min(x for x, _ in r), min(y for _, y in r)))
    out = []
    for k in steps:
        d = {}
        for r, x0, y0 in regs:
            for (x, y) in r:
                u = (x - x0) + (y - y0)
                if k <= u < k + 2: d[(x, y)] = hi
                elif u == k - 1: d[(x, y)] = lo
        out.append(d)
    return out


def glasses(sid, title, legend, grid, seeds, chars, steps, old=(), hold=26):
    fr = sweep(grid, seeds, chars, steps)
    sprite(sid, title, "Glasses", legend, grid, frames=[None, *fr], ticks=[hold] + [1] * len(fr), old=old)


# ================================================================== GLASSES
AV_L = ["yyyyyyyyG", "GLLLLLLLG", "GwwLLLLLG", "GwLLLLLLG", "GlllllllG", "GllllllG.", "olllllG..", ".olllo...", "..ooo...."]
AV_R = ["yyyyyyyyG", "GLLLLLLLG", "GwwLLLLLG", "GwLLLLLLG", "GlllllllG", ".GllllllG", "..Glllllo", "...olllo.", "....ooo.."]
glasses("WEAR-AVIATORS", "Aviators", {**GOLD, **SMOKE, **GLINT}, [
    ("o" if i == 1 else ".") + AV_L[i] + {0: "yy", 2: "oo"}.get(i, "..") + AV_R[i] + ("o" if i == 1 else ".")
    for i in range(9)
], [(4, 1), (15, 1)], "Llwv", [0, 2, 4, 6, 8, 10])

glasses("WEAR-SHADES", "Sunglasses", {**INK, **SMOKE, **GLINT}, [
    "jJjjjjjjjjjjjjjjjjjjjk",
    "kkkkkkkkkkkkkkkkkkkkkK",
    ".kwwLLLLLk..kwwLLLLLK.",
    ".kwLLLLLLk..kwLLLLLLK.",
    ".kLLLLLLLk..kLLLLLLLK.",
    ".kLLLLLLlk..kLLLLLLlK.",
    "..kLLLlllK..KLLLlllK..",
    "...KKKKKK....KKKKKK...",
], [(5, 2), (16, 2)], "Llwv", [0, 2, 4, 6, 8, 10],
    old=["PROP-245", "HOL-MEM-40", "HOL-IND-21", "HOL-LAB-44"])

ROUND_L = ["..zzSSS..",
           ".z.....S.",
           "z..vv...S",
           "z.vv....S",
           "S.......s",
           "S.......s",
           "S.......s",
           ".S.....s.",
           "..sssss.."]
glasses("WEAR-ROUND", "Round wire frames", {**SILV, **GLINT}, [
    ("." + ROUND_L[i] + ("SS" if i == 2 else "..") + ROUND_L[i] + "." if i != 2 else
     "S" + ROUND_L[i] + "SS" + ROUND_L[i] + "s") for i in range(9)
], [(5, 4), (16, 4)], ".vw", [0, 2, 4, 6, 8, 10], old=["HOL-NYD-18"])

glasses("WEAR-NERD", "Thick frames", {**INK, **GLINT, "T": "#f4efe2", "t": "#bdb4b0"}, [
    ".jJjjjjjj....jjjjjjjj.",
    "jkkkkkkkktTTtkkkkkkkkK",
    "j.vv.....tTTt.vv.....K",
    "jvv......tttt vv......K".replace(" ", ""),
    "k........k..k........K",
    "k........k..k........K",
    "k........k..k........K",
    ".KKKKKKKK....KKKKKKKK.",
], [(4, 5), (16, 5)], ".vw", [0, 2, 4, 6, 8, 10])

glasses("WEAR-CATEYE", "Cat-eye glasses", {**PINK, **GLINT, "L": "#2b1a3c", "l": "#4c3064", "z": "#fff3c0"}, [
    "z......................z",
    "Uu....................uU",
    "pUuuuuuu........uuuuuuUp",
    ".pwwLLLLLu....uwwLLLLLp.",
    "..pwLLLLLLuppuwLLLLLLp..",
    "..pLLLLLLLp..pLLLLLLLp..",
    "...QlllllQ....QlllllQ...",
    "....QQQQQ......QQQQQ....",
], [(5, 3), (17, 3)], "Llwv", [0, 2, 4, 6, 8, 10])

glasses("WEAR-3D", "3D glasses", {"A": "#fbf8f0", "a": "#ddd5cc", "Z": "#9a90a8",
                                  "R": "#b8203a", "r": "#ee4a54", "B": "#1a6aa8", "b": "#3cb2e6", **GLINT}, [
    "aAAAAAAAAAAAAAAAAAAAAa",
    "AAwwrrrrRAAAAwwbbbbBAa",
    "AAwrrrrRRAAAAwbbbbBBAa",
    "AArrrrRRRAAAAbbbbBBBAa",
    "AArrrRRRRAaaAbbbBBBBAZ",
    "aARRRRRRRa..aBBBBBBBaZ",
    "aaaaaaaaaa..aaaaaaaaaZ",
    ".ZZZZZZZZ....ZZZZZZZZ.",
], [(4, 1), (15, 1)], "rRbBwv", [0, 2, 4, 6, 8, 10])

HEART = [".uu...uu.",
         "uwru.urrQ",
         "uwrrurrrQ",
         "prrrrrrRQ",
         ".prrrrRQ.",
         "..prrRQ..",
         "...pRQ...",
         "....Q...."]
glasses("WEAR-HEARTS", "Heart shades", {**PINK, **GLINT, "r": "#e8344e", "R": "#a81c3e"}, [
    ("p" if i == 1 else ".") + HEART[i] + ("pp" if i == 2 else "..") + HEART[i] + ("Q" if i == 1 else ".")
    for i in range(8)
], [(3, 2), (14, 2)], "rRwv", [0, 2, 4, 6, 8])

STAR = [".....y.....",
        "....yGo....",
        "....GLo....",
        "yyyyLLLoooo",
        "GwwLLLLLLLo",
        ".GwLLLLLLo.",
        "..GLLLLLo..",
        "..GLLLLLo..",
        ".GLo...oLo.",
        ".oo.....oo."]
glasses("WEAR-STARS", "Star shades", {**GOLD, **GLINT, "L": "#3a2458", "l": "#5a3a80"}, [
    STAR[i] + ("GG" if i == 4 else "..") + STAR[i] for i in range(10)
], [(5, 4), (18, 4)], "Lwv", [0, 2, 4, 6, 8], old=["HOL-NYD-17"])

glasses("WEAR-PIXEL", "Pixel shades", {**INK, **GLINT}, [
    "jjjjjjjjjjjjjjjjjjjjjk",
    "kkkkkkkkkkkkkkkkkkkkkk",
    "KKwwKKKKKKKKKKwwKKKKKK",
    "KKwwKKKKKKKKKKwwKKKKKK",
    "KKKKwwKKKK..KKKKwwKKKK",
    "KKKKwwKKKK..KKKKwwKKKK",
    "..KKKKKK......KKKKKK..",
    "..KKKKKK......KKKKKK..",
], [(0, 2)], "Kw", [0, 3, 6, 9, 12, 15, 18, 21, 24], hold=30)

glasses("WEAR-MONOCLE", "Monocle", {**GOLD, **GLINT}, [
    "..yyGGG.....",
    ".y.....G....",
    "y..vv...G...",
    "y.vv....G...",
    "G.......o...",
    "G.......o...",
    "G.......oG..",
    ".G.....o..y.",
    "..ooooo...G.",
    "...........y",
    "...........G",
    "..........y.",
    "..........G.",
    "..........o.",
], [(4, 4)], ".vw", [0, 2, 4, 6, 8])

glasses("WEAR-GOGGLES", "Ski goggles", {"F": "#262645", "f": "#45456e", "g": "#7676a2",
                                        "S": "#8a2a3a", "s": "#d84a4a",
                                        "a": "#ffd27a", "A": "#ff9440", "M": "#e0508a", "N": "#6a3aa8", **GLINT}, [
    "...gggggggggggggggggf...",
    "..gfawwaaaaaaaaaaaaAfF..",
    "SSgfwwAAAAAAAAAAAAAMfFSS",
    "ssgfAAAAAAAMMMAAAAMMfFss",
    "SSffMMMMMMMMMMMMMMMNFFSS",
    "..ffNNNNMMMMMNNNNNNNFF..",
    "..fFNNNNNFFFFFFNNNNNFF..",
    "...FFFFFF......FFFFFF...",
], [(5, 1)], "aAMNwv", [0, 2, 4, 6, 8, 10, 12, 14, 16, 18])

RD = ["Uuuuuuut", "u.vv...T", "uvv....T", "t......T", ".t....T.", "..TTTT.."]
glasses("WEAR-READERS", "Reading glasses", {"T": "#4a2412", "t": "#8a4a1e", "u": "#c8803a", "U": "#eab070", **GLINT}, [
    ("t" if i == 0 else ".") + RD[i] + ("tt" if i == 0 else "..") + RD[i] + ("T" if i == 0 else ".") for i in range(6)
], [(4, 3), (14, 3)], ".vw", [0, 2, 4, 6])


def R(w, *segs):
    """One grid row of width w from (x, pixels) segments; '.' elsewhere (pixels are still placed by hand)."""
    row = ["."] * w
    for x, s in segs:
        for i, ch in enumerate(s):
            if ch != " ": row[x + i] = ch
    return "".join(row)


# ================================================================== HATS
W24 = lambda *s: R(24, *s)
CAP = [
    W24((8, "Cn")),
    W24((6, "NCCccN")),
    W24((4, "NcCHHCcccN")),
    W24((3, "NcCHHCccccnN")),
    W24((2, "NcCHCCcccccnnN")),
    W24((2, "ncCCCccccccnnN")),
    W24((1, "NcCCcccccccccnnN")),
    W24((1, "ncCccccccccccnnN")),
    W24((1, "nccccccccccccnnN")),
    W24((1, "Nnccccccccccnn"), (15, "CHHCCCcN")),
    W24((2, "NNNNNNNNNNNNN"), (15, "ncccccnnN")),
    W24((14, "NNNNNNNNNN")),
]
sprite("WEAR-CAP", "Baseball cap", "Hats", BLUE, CAP, old=["PROP-246", "HOL-MEM-43", "HOL-IND-20"])

W20 = lambda *s: R(20, *s)
BEANIE_BODY = [
    W20((6, "PRRRRRRP")),
    W20((4, "PRrqqrrrRRRP")),
    W20((3, "PrqqrrrrrrrRRP")),
    W20((2, "PrqrrrrrrrrrrRRP")),
    W20((1, "PRrqrrrrrrrrrrrRRP")),
    W20((1, "PRrrrrrrrrrrrrrRRP")),
    W20((0, "PqrRqrRqrRqrRqrRqRRP")),
    W20((0, "PqrRqrRqrRqrRqrRqRRP")),
    W20((0, "PqrRqrRqrRqrRqrRRRRP")),
    W20((1, "PPPPPPPPPPPPPPPPPP")),
]
POM_A = [W20((8, "xWWx")), W20((7, "xWWWWV")), W20((7, "WWWWxV")), W20((8, "VxxV"))]
POM_B = [W20((9, "xWWx")), W20((8, "xWWWWV")), W20((8, "WWWWxV")), W20((8, "VxxV"))]
POM_C = [W20((7, "xWWx")), W20((6, "xWWWWV")), W20((6, "WWWWxV")), W20((8, "VxxV"))]
sprite("WEAR-BEANIE", "Beanie", "Hats", {**RED, **SNOW}, POM_A + BEANIE_BODY,
       frames=[None, POM_B + BEANIE_BODY, POM_A + BEANIE_BODY, POM_C + BEANIE_BODY], ticks=[16, 3, 3, 3],
       old=["HOL-XMAS-46"])

TOP = [
    W20((3, "kjjjjjjjjjjjjk")),
    W20((3, "kkkkkkkkkkkkkK")),
    W20((3, "kjJJkkkkkkkkKK")),
    W20((3, "kjJJkkkkkkkkKK")),
    W20((3, "kjJkkkkkkkkkKK")),
    W20((3, "kjJkkkkkkkkkKK")),
    W20((3, "kjJkkkkkkkkkKK")),
    W20((3, "kjjkkkkkkkkkKK")),
    W20((3, "kjjkkkkkkkkkKK")),
    W20((3, "PqrrrRRRRRRRPP")),
    W20((3, "PRRRRRRRRRRRPP")),
    W20((0, "jk"), (3, "kjjkkkkkkkkkKK"), (18, "kK")),
    W20((0, "jjjjjjjjjjjjkkkkkkkK")),
    W20((1, "KKKKKKKKKKKKKKKKKK")),
]
sprite("WEAR-TOPHAT", "Top hat", "Hats", {**INK, **RED}, TOP,
       frames=[None, *sweep(TOP, [(8, 4)], "kjJ", [0, 3, 6, 9, 12, 15, 18], hi="J", lo="j")],
       ticks=[30, 1, 1, 1, 1, 1, 1, 1], old=["PROP-447", "HOL-NYD-14", "HOL-PRES-03", "HOL-PRES-01"])

STRIPE_TOP = [
    W20((3, "WWqqWWqqWWqqWW")),
    W20((3, "xxRRxxRRxxRRxP")),
    W20((3, "WWrrWWrrWxRRxP")),
    W20((3, "WWrrWWrrWxRRxP")),
    W20((3, "WWrrWWrrWxRRxP")),
    W20((3, "WWrrWWrrWxRRxP")),
    W20((3, "WWrrWWrrWxRRxP")),
    W20((3, "WWrrWWrrWxRRxP")),
    W20((3, "xWrrWWrrxxRRVP")),
    W20((3, "NcnnnnWnnnnnNN")),
    W20((3, "NnnWnnnnnnWnNN")),
    W20((0, "Cn"), (3, "xWrrWWrrxxRRVP"), (18, "nN")),
    W20((0, "CCCcccccccccccccnnnN")),
    W20((1, "NNNNNNNNNNNNNNNNNN")),
]
sprite("WEAR-TOPHAT-STRIPES", "Striped top hat", "Hats", {**RED, **SNOW, **BLUE}, STRIPE_TOP,
       frames=[None, {(9, 9): "H", (6, 10): "H", (13, 10): "H"}], ticks=[14, 4], old=["HOL-IND-19"])

W28 = lambda *s: R(28, *s)
sprite("WEAR-COWBOY", "Cowboy hat", "Hats", {**FELT, "T": "#2a1410", **SILV}, [
    W28((9, "dBB"), (16, "Bbd")),
    W28((8, "dBEBBdBBBbbD")),
    W28((8, "dBEBbbdbbbbD")),
    W28((7, "dBEBbbbdbbbbD")),
    W28((0, "dB"), (7, "dBEbbbbbbbbbD"), (26, "Bd")),
    W28((0, "dBB"), (7, "TTTTTzSTTTTTT"), (25, "BBd")),
    W28((0, "dBEB"), (7, "dbbbbbbbbbbbD"), (24, "BBbd")),
    W28((1, "dBEEBBBBBBBBBBBBBBBBBBBBbd")),
    W28((2, "DdBBBBBBBBBBBBBBBBBBBBbD")),
    W28((4, "DDddddddddddddddddddDD")),
    W28((7, "DDDDDDDDDDDDDD")),
])

W14 = lambda *s: R(14, *s)
PARTY_CONE = [
    W14((6, "CN")),
    W14((6, "CnN")),
    W14((5, "CcnN")),
    W14((5, "yGGoo")),
    W14((4, "CcccnN")),
    W14((4, "CCccnnN")),
    W14((3, "CCcccnnN")),
    W14((3, "yyGGGGoo")),
    W14((2, "CCcccccnnN")),
    W14((2, "CCccccccnnN")),
    W14((1, "yyGGGGGGGooo")),
    W14((1, "CCcccccccnnnN")),
    W14((0, "CCCccccccccnnN")),
    W14((1, "NNNNNNNNNNNN")),
]
PP_A = [W14((6, "yG")), W14((5, "yYGo")), W14((5, "GGoo"))]
PP_B = [W14((7, "yG")), W14((6, "yYGo")), W14((5, "GGoo"))]
PP_C = [W14((5, "yG")), W14((4, "yYGo")), W14((5, "GGoo"))]
sprite("WEAR-PARTYHAT", "Party hat", "Hats", {**BLUE, **GOLD}, PP_A + PARTY_CONE,
       frames=[None, PP_B + PARTY_CONE, PP_A + PARTY_CONE, PP_C + PARTY_CONE], ticks=[14, 2, 2, 2],
       old=["PROP-433", "HOL-NYD-11", "HOL-NYD-12", "HOL-NYD-13"])

CROWN = [
    W20((0, "WW"), (9, "WW"), (18, "WW")),
    W20((0, "xV"), (9, "xV"), (18, "xV")),
    W20((0, "yG"), (9, "yG"), (18, "Go")),
    W20((0, "yGo"), (8, "yGGo"), (17, "yGo")),
    W20((0, "yGGo"), (7, "yGGGGo"), (16, "yGGo")),
    W20((0, "yGGGo"), (6, "yGGGGGGo"), (15, "yGGGo")),
    W20((0, "yGGGGGyGGGGGGGGyGGGo")),
    W20((0, "yYyyyyyyyyyyyyyyyyGo")),
    W20((0, "yGCcGGGGGqrGGGGGCcGo")),
    W20((0, "yGcnGGGGGRPGGGGGcnGo")),
    W20((0, "yGGGGGGGGGGGGGGGGGoo")),
    W20((1, "oooooooooooooooooo")),
]
sprite("WEAR-CROWN", "Crown", "Hats", {**GOLD, **SNOW, **RED, **BLUE}, CROWN,
       frames=[None, *sweep(CROWN, [(4, 6), (6, 10)], "Gy", [0, 3, 6, 9, 12, 15, 18, 21], hi="Y", lo="y")],
       ticks=[26, 1, 1, 1, 1, 1, 1, 1, 1], old=["PROP-384"])

HARD = [
    W24((8, "OyYYYyyO")),
    W24((6, "OyYWWYyyyyyO")),
    W24((5, "OyYWWYYyyyyyyO")),
    W24((4, "OyYWYYyyYOyyyyOa")),
    W24((4, "OyYYyyyyYOyyyyOa")),
    W24((3, "OyYYyyyyyYOyyyyyOa")),
    W24((3, "OyYyyyyyyYOyyyyyOa")),
    W24((3, "OyyyyyyyyYOyyyyOOa")),
    W24((0, "OyyYYYYYYYYYYyyyyyyyyOOa")),
    W24((0, "aOOOOOOOOOOOOOOOOOOOOOaa")),
    W24((1, "aaaaaaaaaaaaaaaaaaaaaa")),
]
sprite("WEAR-HARDHAT", "Hard hat", "Hats", {"a": "#7a4410", "O": "#c88414", "y": "#f4c430", "Y": "#ffe66a", "W": "#fff8cc"},
       HARD, frames=[None, *sweep(HARD, [(9, 1)], "yYW", [0, 3, 6, 9, 12, 15, 18], hi="W", lo="Y")],
       ticks=[30, 1, 1, 1, 1, 1, 1, 1], old=["PROP-172", "HOL-LAB-01", "HOL-LAB-02", "HOL-LAB-03"])

W22 = lambda *s: R(22, *s)
SANTA = [
    W22((7, "PRRRP")),
    W22((5, "PRrrrrRRP")),
    W22((4, "PRrqqrrrRRRP")),
    W22((3, "PRrqqrrrrRRRRPP")),
    W22((3, "Rrqrrrrrrr"), (14, "PRRRP")),
    W22((2, "PRrqrrrrrrR"), (16, "PRRP")),
    W22((2, "Rrrrrrrrrrr"), (17, "PRP")),
    W22((2, "RrrrrrrrrrRP"), (17, "bBBb")),
    W22((1, "PRrrrrrrrrrRP"), (16, "bBBBBe")),
    W22((1, "RrrrrrrrrrrRRP"), (16, "BBBbbe")),
    W22((1, "RrrrrrrrrrrrRP"), (16, "ebbbe")),
    W22((0, "xWWWWWWWWWxxxxxV")),
    W22((0, "WWWxWWWWxWWxxxxxV")),
    W22((0, "xWWWWWxxxxxxxxxV")),
    W22((1, "VVVVVVVVVVVVVV")),
]
POM_SNOW = {"B": SNOW["W"], "b": SNOW["x"], "e": SNOW["V"]}
SANTA_SWING = {(17, 6): ".", (18, 6): "P", (19, 6): "R", (20, 6): "P", (17, 7): ".", (18, 7): "b", (19, 7): "B", (20, 7): "B",
               (21, 7): "b", (16, 8): ".", (17, 8): "b", (18, 8): "B", (19, 8): "B", (20, 8): "B", (21, 8): "B",
               (16, 9): ".", (17, 9): "B", (18, 9): "B", (19, 9): "B", (20, 9): "b", (21, 9): "b",
               (16, 10): ".", (17, 10): "e", (18, 10): "b", (19, 10): "b", (20, 10): "b", (21, 10): "e"}
sprite("WEAR-SANTA", "Santa hat", "Hats", {**RED, **SNOW, **POM_SNOW}, SANTA, frames=[None, SANTA_SWING, None],
       ticks=[14, 4, 6], old=["HOL-XMAS-44"])
# elf hat: the same drawing in a green ramp, red cuff, gold bell (palette swap, rec-marketing-pixel-art section 11)
sprite("WEAR-ELF", "Elf hat", "Hats", {"P": GREEN["F"], "R": GREEN["f"], "r": GREEN["g"], "q": GREEN["h"],
                                       "W": RED["q"], "x": RED["r"], "V": RED["P"],
                                       "B": GOLD["Y"], "b": GOLD["G"], "e": GOLD["o"]}, SANTA,
       frames=[None, SANTA_SWING, None, {(15, 7): "B", (14, 9): "B"}], ticks=[12, 3, 3, 2], old=["HOL-XMAS-45"])

sprite("WEAR-BOWLER", "Bowler hat", "Hats", {**INK, **FELT}, [
    W20((6, "kjjjjjk")),
    W20((4, "kjJJjjkkkkK")),
    W20((3, "kjJJjkkkkkkkK")),
    W20((3, "kjJjkkkkkkkkK")),
    W20((3, "kjjkkkkkkkkKK")),
    W20((3, "dBbbbbbbbbbdD")),
    W20((0, "jk"), (3, "kjkkkkkkkkkKK"), (17, "kK")),
    W20((0, "jkkkkkkkkkkkkkkkkkkK")),
    W20((1, "KKKKKKKKKKKKKKKKKK")),
], old=["HOL-MLK-49", "HOL-PRES-40"])

sprite("WEAR-TRICORNE", "Tricorne", "Hats", {**INK, **GOLD, **RED}, [
    W24((8, "kjjjjjjk")),
    W24((6, "kjJJjjjjjkK")),
    W24((5, "kjJjjjjjjjjkK")),
    W24((0, "y"), (4, "kjjjjjjjjjjjjjkK"), (23, "o")),
    W24((0, "Gy"), (3, "kjjjjjjjjjjjjjjjkK"), (22, "oG")),
    W24((1, "GyykkkkkkkkkkkkkkkkkooG")),
    W24((2, "GyyykkkkkkkkkkkkoooG")),
    W24((3, "GGyyyykkkkkkooooGG"), (6, " rR ")),
    W24((5, "GGGyyyykooooGGG")),
    W24((8, "GGGyyoGGG")),
    W24((11, "Go")),
], old=["HOL-PRES-02"])

sprite("WEAR-FLATCAP", "Flat cap", "Hats", FELT, [
    W22((5, "dBBBBBBbbD")),
    W22((3, "dBEEEBBBBbbbbD")),
    W22((2, "dBEEBBBBBbbbbbbD")),
    W22((1, "dBBBBBbbbbbbbbbbbD")),
    W22((1, "dBbbbbbbbbbbbbbbBBD")),
    W22((1, "DddddddddddddbbbEEEBd")),
    W22((2, "DDDDDDDDDDDDdddbbbbD")),
    W22((13, "DDDDDDD")),
], old=["HOL-MLK-50"])

# ================================================================== BOWS & BITS
W16 = lambda *s: R(16, *s)
sprite("WEAR-BOWTIE", "Bow tie", "Bows & bits", RED, [
    W16((1, "PR"), (13, "RP")),
    W16((0, "Rqqr"), (12, "rRRP")),
    W16((0, "Rqrrrr"), (10, "rrRRRP")),
    W16((0, "Rqrrrr"), (6, "PqrP"), (10, "rrrRRP")),
    W16((0, "RrrRrr"), (6, "PrRP"), (10, "rrRrRP")),
    W16((0, "RrRrrr"), (6, "PRRP"), (10, "rRRRRP")),
    W16((0, "RRRR"), (12, "RRPP")),
    W16((1, "PP"), (13, "PP")),
], old=["PROP-446", "HOL-NYD-15", "HOL-NYD-16", "HOL-PRES-39", "HOL-IND-23"])

HAIRBOW = [
    W16((1, "pp"), (13, "pp")),
    W16((0, "pUUpp"), (11, "ppuuQ")),
    W16((0, "pUuuupp"), (9, "ppuuuuQ")),
    W16((0, "pUuuuu"), (6, "QUuQ"), (10, "uuuuuQ")),
    W16((0, "puuuuu"), (6, "QuuQ"), (10, "uuuupQ")),
    W16((0, "puuupp"), (6, "QppQ"), (10, "ppupQ")),
    W16((0, "QQpp"), (5, "pupQQp"), (12, "ppQQ")),
    W16((2, "QQ"), (4, "puQ"), (9, "Qup"), (12, "QQ")),
]
HB_A = [W16((3, "puQ"), (10, "Qup")), W16((3, "pQ"), (11, "Qp")), W16((2, "Q Q"), (11, "Q Q"))]
HB_B = [W16((3, "puQ"), (10, "Qup")), W16((2, "puQ"), (11, "Qup")), W16((1, "Q Q"), (12, "Q Q"))]
sprite("WEAR-HAIRBOW", "Hair bow", "Bows & bits", PINK, HAIRBOW + HB_A,
       frames=[None, HAIRBOW + HB_B], ticks=[14, 6])

T_A = ["RrqrP", "WWxxV", "RrqrP", "RrqrP", "WWxxV", "RrqrP", "RrrRP", "V V V"]
T_B = ["rRRP", "rRRP", "WxxV", "rRRP", "rRRP", "WxxV", "V VV"]
SCARF = [
    W16((3, "PRRRRRRRRRP")),
    W16((1, "PRRRrrrrrrRRRP")),
    W16((0, "PRRP"), (12, "RRRP")),
    W16((0, "RrqR"), (12, "rRRP")),
    W16((0, "RrqWxrrrrrrWxRRP")),
    W16((0, "PRqWxrrrrrrWxRPP")),
    W16((1, "PPRrqrPrrRRPPP")),
] + [W16((3, T_A[i]), *([(8, T_B[i])] if i < len(T_B) else [])) for i in range(len(T_A))] + [W16()]
SCARF_SWAY = {(8, 11): ".", (9, 11): "r", (10, 11): "R", (11, 11): "R", (12, 11): "P",
              (8, 12): ".", (9, 12): "W", (10, 12): "x", (11, 12): "x", (12, 12): "V",
              (8, 13): ".", (9, 13): "V", (10, 13): ".", (11, 13): "V", (12, 13): "V",
              (3, 14): ".", (4, 14): "V", (5, 14): ".", (6, 14): "V", (7, 14): "."}
sprite("WEAR-SCARF", "Scarf", "Bows & bits", {**RED, **SNOW}, SCARF[:15], frames=[None, SCARF_SWAY], ticks=[14, 6])

W18 = lambda *s: R(18, *s)
sprite("WEAR-SNEAKER", "Sneaker", "Bows & bits", {**BLUE, **SNOW, "o": "#c8501e", "O": "#f08a3a"}, [
    W18((1, "NnnN")),
    W18((0, "NcCWcN")),
    W18((0, "NcCxWnN")),
    W18((0, "OcCcxWnN")),
    W18((0, "OcCcnxWcN")),
    W18((0, "OcCccnxWccN")),
    W18((0, "ocCcccnxWxccnnN")),
    W18((0, "onccccccccccxWWx")),
    W18((0, "WWWWWWWWWWWWWxWWWx")),
    W18((0, "xxxxxxxxxxxxxxxxxV")),
    W18((1, "VVVVVVVVVVVVVVVV")),
])

RB = {"a": "#7a4410", "O": "#c88414", "y": "#f4c430", "Y": "#ffe66a", "W": "#fff8cc", "k": "#4a2e24", "K": "#2e1a1e"}
sprite("WEAR-RAINBOOTS", "Rain boots", "Bows & bits", RB, [   # front boot overlaps the darker back boot
    W16((8, "aaaaaa")),
    W16((8, "ayyyOa")),
    W16((1, "aWWWYa"), (8, "ayyyOa")),
    W16((1, "aOOOOa"), (8, "ayyyOa")),
    W16((1, "OYWyya"), (8, "ayyyOa")),
    W16((1, "OYWyya"), (8, "ayyyOa")),
    W16((1, "OYWyya"), (8, "ayyyOa")),
    W16((1, "OYWyya"), (8, "ayyyOa")),
    W16((1, "OYyyya"), (8, "ayyyyOa")),
    W16((1, "OYyyya"), (8, "ayyyyyOa")),
    W16((1, "OYyyyyOa"), (9, "yyyyyO")),
    W16((1, "OYyyyyyyay"), (11, "KKKKK")),
    W16((1, "OYyyyyyyyOa")),
    W16((1, "kkkkkkkkkkk")),
], old=["PROP-346", "HOL-GF-32", "HOL-GF-33"])
