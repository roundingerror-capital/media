"""THE LIBRARY (the boss 2026-11-02): every prop, holiday item and small asset, redrawn by the rec-marketing-pixel-art skill,
de-duplicated and grouped by genre. Replaces the procedural tools/props.py + tools/holiday_assets.py drawings (kept for old specs).

Sprites are hand-authored character grids at their FINAL size (skill section 8): one character per pixel, a legend maps
characters to colours, '.' is transparent. Animation = extra frames written as full grids or as small pixel overrides on the
base grid (steam, a sparkle, a drip); never a transform of the image.

    from lib import get, frames, ids, GENRES
    im = get("FOOD-CUPCAKE", t)            # RGBA at native size, animated
    fr, ticks = frames("FOOD-CUPCAKE")     # every frame + holds (1 tick = 100 ms)

Scale (games convention, not real-world): hand-held items 16 px tall, desk items 24, floor items 32-48, next to a 45 px mascot.
"""
import importlib, os
from PIL import Image

GENRES = [  # id prefix, name, note
    ("FOOD", "Food & drink", "Meals, snacks, sweets, fruit, drinks. 16 px icons, Kirby / Stardew style."),
    ("DESK", "Desk & office", "Laptops, mugs, paper, pens, the duck."),
    ("TECH", "Tech", "Gadgets that blink; nothing branded."),
    ("TOOL", "Tools & work", "Hard hats to blowtorches."),
    ("PLAY", "Sports & games", "Balls, boards, chess, cards, dice."),
    ("TOYS", "Toys", "Bears, blocks, ducks, tops."),
    ("CITY", "City street", "NYC: hydrant, taxi, the rat with the slice."),
    ("FANT", "Fantasy", "Kit's studio: swords, potions, chests."),
    ("MUSI", "Music", "Instruments, speakers, records."),
    ("MONY", "Money desk", "Bull, bear, bell, coins; symbols only, never a figure."),
    ("NATR", "Nature & seasons", "Flowers, leaves, snow, weather, critters."),
    ("WEAR", "Clothing & accessories", "Hats, glasses, shoes, bows."),
    ("PRTY", "Celebration", "Balloons, bunting, fireworks, gifts, candles."),
]

SPRITES = {}   # id -> dict(title, genre, group, size, legend, grid, frames, ticks, old)

def sprite(sid, title, group, legend, grid, frames=None, ticks=None, old=()):
    """Register one sprite. grid: list of equal-length strings. frames: list of frames, each either a full grid (list of
    strings) or a dict {(x, y): char} of overrides on the base grid; None = a still with a 2-frame idle sparkle-free hold."""
    h = len(grid); w = len(grid[0])
    assert all(len(r) == w for r in grid), f"{sid}: ragged grid"
    for r in grid:
        for ch in r:
            assert ch == "." or ch in legend, f"{sid}: '{ch}' not in legend"
    fr = [grid if f is None else f for f in (frames or [None])]
    SPRITES[sid] = dict(id=sid, title=title, genre=sid.split("-")[0], group=group, size=(w, h), legend=legend, grid=grid,
                        frames=fr, ticks=ticks or [10] * len(fr), old=list(old))

def _hex(c): c = c.lstrip("#"); return (int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16), 255)

def _paint(s, g):
    w, h = s["size"]; im = Image.new("RGBA", (w, h)); px = im.load()
    for y, row in enumerate(g):
        for x, ch in enumerate(row):
            if ch != ".": px[x, y] = _hex(s["legend"][ch])
    return im

def _grid(s, fr):
    if isinstance(fr, dict):
        g = [list(r) for r in s["grid"]]
        for (x, y), ch in fr.items(): g[y][x] = ch
        return ["".join(r) for r in g]
    return fr

_LOADED = False
def _load():
    global _LOADED
    if _LOADED: return
    here = os.path.dirname(__file__)
    for f in sorted(os.listdir(here)):
        if f.endswith(".py") and f != "__init__.py": importlib.import_module("lib." + f[:-3])
    _LOADED = True

def ids(genre=None): _load(); return [k for k, v in SPRITES.items() if genre is None or v["genre"] == genre]
def info(sid): _load(); return SPRITES[sid]
def frames(sid):
    _load(); s = SPRITES[sid]; return [_paint(s, _grid(s, f)) for f in s["frames"]], s["ticks"]
def get(sid, t=0.0):
    fr, tk = frames(sid); total = sum(tk); u = (t * 10) % total; acc = 0
    for im, k in zip(fr, tk):
        acc += k
        if u < acc: return im
    return fr[-1]
def old_to_new():
    """PROP-xxx / HOL-xxx-nn -> library id, so older specs keep working."""
    _load(); return {o: k for k, v in SPRITES.items() for o in v["old"]}
