"""Office-sitcom intro parody, v5 (the boss 2026-11-03, notes on v4: every apartment furnished with 5-10 kit pieces and 25
different residents in Kit's colourways, all animated; a readable name plate; monitors facing the character; cabinets and
shelves at the back of every office; a lawyer's book wall and a pet up front for Roz; a gamer's room for Kit; navy behind
the boss mug; the break room for the copier and the coffee run, with depth; a server room with Kit in the lower right; the
phone really rings; a burned-in shot / time / frame strip for notes).

Same rules as v4: Kit's art only (stages, kit components, library sprites, rigs, palette swaps), composed in depth, every
layer enlarged by whole numbers. Stand-ins until Kit draws them are listed in PENDING and shown on the review strip.

    PARODY_CUT=<song_cut.json> python3 make_v5.py <out.mp4> [workdir]          # review render (strip on top)
    PARODY_CUT=<song_cut.json> python3 make_v5.py <out.mp4> [workdir] --final  # clean render (no strip)
    PARODY_CUT=<song_cut.json> python3 make_v5.py --panels <sheet.png>          # storyboard
Renders and caches stay out of git."""
import os, sys, math, json, random, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); TOOLS = os.path.join(HERE, "..", "..", "tools"); sys.path.insert(0, TOOLS)
from PIL import Image, ImageDraw
import daily, rigs, stage, scenes, swaps, lib
from make_reel import W, H, FPS, archivo, mono, fit
from board_capture import capture

ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
PANELS = "--panels" in sys.argv; FINAL = "--final" in sys.argv
OUT = ARGS[0] if ARGS else "/home/claude/out/officeparody/office_parody_v5.mp4"
WORK = ARGS[1] if len(ARGS) > 1 else os.path.join(os.path.dirname(OUT), "work_v5")
ASSETS = os.environ.get("RE_ASSETS_DIR", "/tmp/claude-0/-home-claude/97ad6b31-1277-5795-987d-0d7c1b8393c4/scratchpad/assetscanvas_live/project")
CUT = json.load(open(os.environ["PARODY_CUT"])); SONG_WAV = os.environ["PARODY_CUT"][:-5] + ".wav"
LIME, INK = "#C8F03C", "#F2F2EE"
WIN17 = (15, 40, 121, 168)
PORTRAIT = 15
INSERT = (45, 80, 24)

# ---------- shot list, in beats (the song's own grid) ----------
# kind: car | tower | insert | desk | breakroom | serverroom | title | end
MONTAGE = [
    (4, "car", dict(label="CAR RIDE")),
    (4, "tower", dict(label="THE TOWER")),
    (2, "insert", dict(label="PHONE RINGS", prop="Desk phone, coiled cord", st="OFF-ADA-01", ring=True)),
    (4, "desk", dict(label="ADA", ch="ada", an="desk_phone", st="OFF-ADA-01", name="ADA", role="DATA", mon="l",
                     back=("theo", "walk", 70, 150, 95))),
    (2, "insert", dict(label="BOSS MUG", prop="Boss mug with a gold star", st="OFF-BOSS-01", ghost="boss")),
    (4, "desk", dict(label="THEO", ch="theo", an="desk_sip", st="OFF-THEO-01", name="THEO", role="TRADING", mon="r",
                     back=("ada", "idle", 82, 82, 95))),
    (6, "desk", dict(label="PENNY", ch="penny", an="desk34_stare", st="OFF-PENNY-01", name="PENNY", role="MARKETING", mon="r",
                     back=("kit", "walk", 150, 70, 94))),
    (2, "insert", dict(label="JELLY", prop="Stapler in a jelly mold", st="OFF-PENNY-01", jiggle=True)),
    (4, "desk", dict(label="ROZ", ch="roz", an="desk34_type", st="OFF-ROZ-01", name="ROZ", role="LEGAL", mon="r",
                     back=("penny", "walk", 80, 140, 95))),
    (2, "insert", dict(label="SHREDDER", prop="Paper shredder", st="OFF-ROZ-01", floor=True)),
    (2, "breakroom", dict(label="COPIER", copier=True)),
    (4, "desk", dict(label="KIT", ch="kit", an="desk34_phone", st="OFF-KIT-01", name="KIT", role="GAME STUDIO", mon="r",
                     back=("roz", "walk", 140, 84, 95))),
    (2, "breakroom", dict(label="COFFEE RUN")),
    (6, "serverroom", dict(label="SERVER ROOM", credit="THE SERVER ROOM")),
]
TAIL = [(8, "desk", dict(label="THEO STARE", ch="theo", an="desk_side_stare", st="OFF-THEO-01", mon="r", back=("ada", "walk", 140, 80, 95))),
        (8, "title", dict(label="TITLE")), (None, "end", dict(label="END CARD"))]
# Stand-ins until Kit draws the piece (board 20261103-173900-penny-wk2m and today's follow-up): shown on the review strip
PENDING = {"desk": "monitor back = MON-02 with its screen in casing colour (Kit: MON-06)",
           "ROZ": "law-book wall; diplomas pending Kit", "PENNY": "family photos / graded cards pending Kit",
           "THE TOWER": "cars pending Kit", "BOSS MUG": "'u tried' pending Kit", "JELLY": "real jiggle pending Kit"}

bt = CUT["beat"]; TEASE = CUT["pickup"] if CUT["pickup"] >= 0.9 else CUT["pickup"] + 2 * bt
j = CUT["join"] - TEASE; nb = sum(b for b, _, _ in MONTAGE)
t = j - nb * bt; SHOTS = []
for b, k, a in MONTAGE: SHOTS.append((t, t + b * bt, k, a)); t += b * bt
SHOTS[0] = (0.0,) + SHOTS[0][1:]
t = j
for b, k, a in TAIL:
    e = t + b * bt if b else CUT["total"] - TEASE; SHOTS.append((t, e, k, a)); t = e
END = SHOTS[-1][1]

# ---------- Kit's CSS boards -> native frames (cached) ----------
CACHE = os.path.join(WORK, "cache"); os.makedirs(CACHE, exist_ok=True)
def board_frames(board, label, dur, fps=10):
    key = os.path.join(CACHE, f"{board}_{label}".replace(" ", "_").replace(",", ""))
    n = int(math.ceil(dur * fps)) + 1
    if all(os.path.exists(key + f"_{i}.png") for i in (0, n - 1)):
        return [Image.open(key + f"_{i}.png").convert("RGBA") for i in range(n)]
    ims = capture(os.path.join(ASSETS, board), label, [i / fps + 0.02 for i in range(n)], scale=1)
    for i, im in enumerate(ims): im.save(key + f"_{i}.png")
    return ims
def at(frames, u, fps=10): return frames[min(len(frames) - 1, int(u * fps))]
_BB = {}
def prop(label, u, dur=6.0):
    """Kit's prop at native size, trimmed to the union of its drawn pixels over the loop."""
    fr = board_frames("LIBOFFICE.dc.html", label + " at actual size", dur)
    if label not in _BB:
        bbs = [f.getbbox() for f in fr if f.getbbox()]
        _BB[label] = (min(b[0] for b in bbs), min(b[1] for b in bbs), max(b[2] for b in bbs), max(b[3] for b in bbs))
    return at(fr, u).crop(_BB[label])
def comp(name): return stage.component(os.path.join(ASSETS, name + ".dc.html"))

def libsprite(i, u=0.0):
    return lib.get(i, u).convert("RGBA")

# ---------- set dressing per stage ----------
# wall: WALL tile in place of Kit's; rug; skip: stage pieces left out; add: [(layer, piece, x, bottom)]; piece "lib:<ID>" = library sprite
BACK = "L6"     # back-wall layer: drawn after Kit's wall art, before the chair and everything on the floor
DRESS = {
    "OFF-ADA-01":   dict(wall="WALL-11", rug=("RUG-02", 88, 108), skip=("DEC06",),
                         add=[(BACK, "DEC-16", 78, 92), (BACK, "DEC-16", 98, 92), (BACK, "DEC-04", 120, 92), (BACK, "DEC-32", 78, 58),
                              (BACK, "DEC-03", 104, 26), (BACK, "lib:DESK-FOLDER-RED", 80, 62), (BACK, "PLT-03", 100, 62)]),
    "OFF-BOSS-01":  dict(wall="WALL-05", rug=("RUG-01", 88, 108)),
    "OFF-THEO-01":  dict(wall="WALL-12", add=[(BACK, "DEC-04", 76, 92), (BACK, "DEC-42", 112, 92), (BACK, "lib:PLAY-TROPHY-GOLD", 118, 37),
                         (BACK, "DEC-03", 98, 22), (BACK, "PLT-01", 146, 92)]),
    "OFF-PENNY-01": dict(rug=("RUG-01", 88, 110), skip=("DEC31",),
                         add=[(BACK, "DEC-42", 76, 92), (BACK, "DEC-02", 116, 40), (BACK, "DEC-32", 100, 70), (BACK, "DEC-30", 112, 30),
                              (BACK, "lib:TOYS-TEDDY-BOW", 113, 13), (BACK, "lib:TOYS-SNOW-GLOBE", 130, 13), (BACK, "PLT-06", 140, 36)]),
    "OFF-ROZ-01":   dict(wall="WALL-04", rug=("RUG-03", 88, 108), skip=("DEC11",),
                         add=[(BACK, "DEC-04", 76, 92), (BACK, "DEC-04", 112, 92), (BACK, "DEC-38", 104, 30),
                              ("L16", "PET-06", 100, 126)]),
    "OFF-KIT-01":   dict(wall="WALL-17", rug=("RUG-07", 88, 108),
                         add=[(BACK, "TEC-03", 76, 92), (BACK, "TEC-03", 120, 92), (BACK, "DEC-02", 104, 40), (BACK, "DEC-30", 96, 62),
                              (BACK, "lib:TECH-CONTROLLER", 98, 45), (BACK, "lib:TOYS-ROBOT", 112, 45), (BACK, "DEC-33", 100, 94),
                              (BACK, "lib:TOYS-TEDDY", 102, 84), (BACK, "lib:TECH-HEADPHONES", 128, 37)]),
}
def piece_img(name):
    return libsprite(name[4:]) if name.startswith("lib:") else comp(name)
def dressed(st, name, skip=(), extra=None):
    d = DRESS.get(name, {}); extra = dict(extra or {}); skip = tuple(skip) + tuple(d.get("skip", ()))
    if d.get("rug"): skip += ("RUG",); r, x, y = d["rug"]; place(extra, "L7", comp(r), x, y)
    adds = {}
    for lay, pc, x, bottom in d.get("add", []):
        im = piece_img(pc); adds.setdefault(lay, []).append((im, x, bottom - im.height))
    for lay, items in adds.items(): extra[lay] = items + extra.get(lay, [])     # dressing first, cast after it on the same layer
    return skip, extra, (comp(d["wall"]) if d.get("wall") else None)

_MONB = {}
def monitor_back():
    """Stand-in for Kit's monitor-back piece (requested as MON-06): MON-02 with every screen colour set to its own casing grey."""
    if "m" not in _MONB:
        im = comp("MON-02"); px = im.load(); keep = {(0x15, 0x15, 0x1C), (0x2B, 0x2B, 0x33)}
        for y in range(im.height):
            for x in range(im.width):
                r, g, b, a = px[x, y]
                if a and (r, g, b) not in keep and y < 15: px[x, y] = (0x2B, 0x2B, 0x33, a)
        _MONB["m"] = im
    return _MONB["m"]

# ---------- cast on a stage ----------
DESK_SET = ("DSK", "MON", "TEC08", "TEC04", "TEC05", "TEC07", "FOD", "DEC09", "CHR")   # Kit's desk set: the rig brings its own
def place(extra, layer, sp, x, y): extra.setdefault(layer, []).append((sp, x, y))
def stand_at(extra, st, sp, cx, feet):
    """A standing rig (feet on the frame's bottom row) with its feet at (cx, feet), at the right depth."""
    place(extra, stage.depth_layer(st, feet), sp, cx - sp.width // 2, feet - sp.height)
def desk_rig(st, ch, an, t, t0):
    """The desk rig in the place of Kit's desk (DSK at (x, 84), 56 wide, bottom y 112): its own desk's left edge on Kit's."""
    sp = rigs.frame(ch, an, t, k=1, loop=False, t0=t0)
    db = sp.crop((0, sp.height - 14, sp.width, sp.height)).getbbox()
    dx = next(x for n, uses, _ in st.layers for s, x, y in uses if s.startswith("DSK"))
    return sp, dx - db[0], 112 - sp.height
def back_cast(st, extra, spec, t, u, dur, t0):
    ch, an, x0, x1, feet = spec
    x = int(x0 + (x1 - x0) * min(1, u / max(0.01, dur)))
    sp = rigs.frame(ch, an, t, k=1, flip=(x1 < x0), t0=t0)
    stand_at(extra, st, sp, x, feet)
def ghost(sp, a=0.10):
    g = sp.copy(); g.putalpha(g.getchannel("A").point(lambda v: int(v * a))); return g

def up(c, k): return c.resize((c.width * k, c.height * k), Image.NEAREST).convert("RGB")

# ---------- name plate: an RPG dialog window, pixel-stepped (the boss: readable, cool, not a pill) ----------
PX = 6
def nameplate(img, name, role, u, y=300):
    if not name or u < 0.2: return img
    k = min(1.0, (u - 0.2) / 0.22); k = 1 - (1 - k) ** 3
    fn = fit(name, 600, 104, wdth=125, wght=900); tw = int(fn.getlength(name))
    bw = max(tw + 120, 420) // PX; bh = (216 if role else 150) // PX
    box = Image.new("RGBA", (bw, bh), (0, 0, 0, 0)); d = ImageDraw.Draw(box)
    d.rectangle([1, 0, bw - 2, bh - 1], fill=(8, 8, 12, 255)); d.rectangle([0, 1, bw - 1, bh - 2], fill=(8, 8, 12, 255))
    d.rectangle([1, 1, bw - 2, bh - 2], fill=(242, 242, 238, 255)); d.rectangle([2, 2, bw - 3, bh - 3], fill=(18, 20, 42, 255))
    d.rectangle([3, 3, bw - 4, bh - 4], outline=(200, 240, 60, 255))
    for cx, cy in ((1, 1), (bw - 2, 1), (1, bh - 2), (bw - 2, bh - 2)): d.point((cx, cy), fill=(8, 8, 12, 255))
    box = box.resize((bw * PX, bh * PX), Image.NEAREST)
    x = 54 - int((1 - k) * (bw * PX + 80)) // PX * PX
    lay = Image.new("RGBA", img.size); lay.alpha_composite(box, (max(-box.width, x), y)) if x >= 0 else lay.paste(box, (x, y), box)
    dd = ImageDraw.Draw(lay); tx = x + 7 * PX
    dd.text((tx, y + 6 * PX + 92), name, font=fn, fill=INK, anchor="ls")
    if role:
        n = int(len(role) * min(1, max(0, (u - 0.35) / 0.3)))            # typewriter
        dd.text((tx, y + bh * PX - 6 * PX + 2), role[:n] + ("_" if n < len(role) and int(u * 8) % 2 else ""), font=mono(40, True), fill=LIME, anchor="ls")
    img.paste(lay.convert("RGB"), (0, 0), lay); return img

# ---------- review strip: shot, time, frame (the boss: "add the frame # on the top or bottom to reference") ----------
def strip(img, tv):
    if FINAL: return img
    i = next((n for n, s in enumerate(SHOTS) if s[0] <= tv - TEASE < s[1]), len(SHOTS) - 1) if tv >= TEASE else -1
    lab = "TEASER" if i < 0 else SHOTS[i][3].get("label", SHOTS[i][2]).upper()
    note = "" if i < 0 else PENDING.get(lab) or (PENDING["desk"] if SHOTS[i][2] == "desk" else "")
    d = ImageDraw.Draw(img); d.rectangle([0, 0, W, 50], fill=(0, 0, 0))
    mm, ss = divmod(tv, 60)
    d.text((16, 36), f"S{i + 1:02d} {lab}", font=mono(26, True), fill=LIME, anchor="ls")
    d.text((W // 2 + 40, 36), f"{int(mm):02d}:{ss:05.2f}", font=mono(26, True), fill=INK, anchor="ms")
    d.text((W - 16, 36), f"F{int(round(tv * FPS)):04d}", font=mono(26, True), fill=INK, anchor="rs")
    if note:
        d.rectangle([0, H - 44, W, H], fill=(0, 0, 0)); d.text((16, H - 14), "STAND-IN: " + note, font=mono(20), fill="#9A9A94", anchor="ls")
    return img

# ---------- the tower: 25 furnished apartments, 25 residents (5 cast x Kit's 5 colourways), lights on their own timing ----------
TW, TH, TK = 540, 960, 2           # native canvas x2 = 1080x1920
RW, RH, WALLH = 92, 80, 56         # room window, wall height inside
COLS, ROWS, GAP = 5, 5, 8
BX = (TW - (COLS * RW + (COLS + 1) * GAP)) // 2; ROOF = 250
WALLS = ["WALL-01", "WALL-02", "WALL-04", "WALL-05", "WALL-06", "WALL-07", "WALL-08", "WALL-09", "WALL-11", "WALL-12", "WALL-13",
         "WALL-14", "WALL-15", "WALL-16", "WALL-17", "WALL-18"]
FLOORS = ["FLR-01", "FLR-02", "FLR-04", "FLR-05", "FLR-06", "FLR-08", "FLR-09", "FLR-10", "FLR-13", "FLR-14", "FLR-07", "FLR-03"]
TALL = ["DEC-04", "DEC-42", "DEC-16", "TEC-03", "PLT-01", "DEC-08", "DEC-35"]
SEAT = ["DEC-14", "DEC-15", "DEC-43", "DEC-44", "DEC-39", "DEC-40", "DEC-33", "DEC-34"]
WALLART = ["DEC-03", "DEC-01", "DEC-02", "DEC-30", "DEC-32", "DEC-38", "DEC-07", "DEC-31"]
SMALL = ["PLT-02", "PLT-03", "PLT-04", "PLT-05", "DEC-29", "PET-01", "PET-02", "PET-03", "PET-04", "PET-06", "PET-07"]
ONTOP = ["lib:TECH-TV", "lib:TECH-BOOMBOX", "lib:DESK-GLOBE", "lib:TOYS-SNOW-GLOBE", "lib:PLAY-TROPHY-GOLD", "lib:TOYS-ROBOT",
         "lib:TECH-SPEAKER", "lib:TOYS-TEDDY", "lib:DESK-PLANT", "lib:TECH-VINYL", "FOD-08", "FOD-02", "FOD-06"]
CURTAINS = ["DEC-19", "DEC-20", "DEC-21", "DEC-22", "DEC-23"]
ANIMS = ["idle", "talk", "nod", "celebrate", "shrug", "point", "facepalm", "shakehead", "holdsign", "walk"]
CAST = ["theo", "penny", "ada", "roz", "kit"]
_TOWER = {}
def _room(i):
    r = random.Random(1000 + i * 7919)
    room = Image.new("RGBA", (RW, RH)); wall = comp(WALLS[i % len(WALLS)]); flr = comp(FLOORS[(i * 5) % len(FLOORS)])
    for y in range(0, WALLH, wall.height):
        for x in range(0, RW, wall.width): room.alpha_composite(wall.crop((0, 0, min(wall.width, RW - x), min(wall.height, WALLH - y))), (x, y))
    for y in range(WALLH, RH, flr.height):
        for x in range(0, RW, flr.width): room.alpha_composite(flr.crop((0, 0, min(flr.width, RW - x), min(flr.height, RH - y))), (x, y))
    base = comp(r.choice(["SHL-01", "SHL-02"]))
    for x in range(0, RW, base.width): room.alpha_composite(base.crop((0, 0, min(base.width, RW - x), base.height)), (x, WALLH - base.height))
    back, front, n = [], [], 0
    def put(lst, im, x, bottom):
        nonlocal n; lst.append((im, int(x), int(bottom - im.height))); n += 1
    side = r.random() < 0.5
    tall = comp(r.choice(TALL)); tx = 4 if side else RW - tall.width - 4; put(back, tall, tx, WALLH + 4)
    if tall.height < 40 and r.random() < 0.7:
        it = piece_img(r.choice(ONTOP)); put(back, it, tx + (tall.width - it.width) // 2, WALLH + 4 - tall.height)
    seat = comp(r.choice(SEAT)); sx = RW - seat.width - 6 if side else 6; put(back, seat, sx, WALLH + 8)
    if r.random() < 0.6:
        cr = comp("DEC-27" if r.random() < 0.5 else "DEC-28")
        if cr.width < RW - tall.width - seat.width:
            cx = (tx + tall.width + 2) if side else (sx + seat.width + 2)
            if cx + cr.width < (sx if side else tx): put(back, cr, cx, WALLH + 2); it = piece_img(r.choice(ONTOP)); put(back, it, cx + 8, WALLH + 2 - cr.height)
    for _ in range(r.choice([1, 2])):
        art = comp(r.choice(WALLART)); ax = r.randint(14, max(15, RW - art.width - 14)); put(back, art, ax, r.randint(22, 38))
    for c in (r.choice(CURTAINS),):
        cu = comp(c); put(front, cu, 0, cu.height); put(front, cu.transpose(Image.FLIP_LEFT_RIGHT), RW - cu.width, cu.height)
    if r.random() < 0.6: lamp = comp(r.choice(["DEC-36", "DEC-37"])); put(back, lamp, r.randint(30, 50), lamp.height)
    sm = comp(r.choice(SMALL)); put(front, sm, r.choice([14, RW - sm.width - 14]), RH - 2)
    if r.random() < 0.5: tb = comp("DEC-41"); put(back, tb, (RW - tb.width) // 2 + r.randint(-10, 10), WALLH + 14)
    return room, back, front, n
def tower_rooms():
    if "rooms" not in _TOWER: _TOWER["rooms"] = [_room(i) for i in range(COLS * ROWS)]
    return _TOWER["rooms"]
def resident(i):
    ch = CAST[i % 5]; sw = ([None] + swaps.names(ch))[(i // 5) % 5]; an = ANIMS[(i * 3) % len(ANIMS)]
    return ch, sw, an
def lights(i, t):
    r = random.Random(77 + i); period = r.uniform(1.6, 4.5); off = r.uniform(0, period); u = (t + off) % period
    if r.random() < 0.55: return 1.0                                       # steady
    if u < 0.5: return 0.0 if u < 0.32 else (1.0 if int(u * 30) % 2 else 0.0)   # off, then flicker back on
    return 1.0
def tower_frame(t):
    c = Image.new("RGBA", (TW, TH)); d = ImageDraw.Draw(c)
    bands = [(30, 26, 60), (38, 32, 72), (52, 40, 86), (74, 50, 98), (102, 62, 104), (132, 78, 104)]
    for i, col in enumerate(bands): d.rectangle([0, i * 50, TW, i * 50 + 50], fill=col)
    d.rectangle([0, 300, TW, TH], fill=bands[-1])
    brick = comp("WALL-03"); top = ROOF; bottom = ROOF + ROWS * (RH + GAP) + GAP + 110
    for y in range(top, bottom, brick.height):
        for x in range(BX, BX + COLS * RW + (COLS + 1) * GAP, brick.width):
            c.alpha_composite(brick.crop((0, 0, min(brick.width, BX + COLS * RW + (COLS + 1) * GAP - x), min(brick.height, bottom - y))), (x, y))
    cor = comp("SHL-02")
    for x in range(BX - 4, BX + COLS * RW + (COLS + 1) * GAP + 4, cor.width): c.alpha_composite(cor, (x, top - cor.height))
    dish = libsprite("TECH-DISH"); c.alpha_composite(dish, (BX + 30, top - cor.height - dish.height))
    sill = comp("SHL-01")
    for i, (room, back, front, n) in enumerate(tower_rooms()):
        col, row = i % COLS, i // COLS; x0 = BX + GAP + col * (RW + GAP); y0 = top + GAP + row * (RH + GAP)
        im = room.copy()
        for sp, x, y in back: im.alpha_composite(sp, (x, y)) if x >= 0 and y >= 0 and x + sp.width <= RW and y + sp.height <= RH else im.paste(sp, (x, y), sp)
        ch, sw, an = resident(i); sp = rigs.frame(ch, an, t + i * 0.37, k=1, flip=(i % 2 == 1))
        if sw: sp = swaps.recolor(sp, ch, sw)
        bb = sp.getbbox(); sp = sp.crop(bb); feet = RH - 6
        if an == "walk":
            span = RW - 30 - sp.width; ph = ((t * 14 + i * 9) % (2 * max(1, span))); xx = 15 + (ph if ph < span else 2 * span - ph)
            sp = rigs.frame(ch, an, t + i * 0.37, k=1, flip=not (ph < span)); sp = swaps.recolor(sp, ch, sw) if sw else sp; sp = sp.crop(sp.getbbox())
        else: xx = (RW - sp.width) // 2 + ((i * 13) % 21 - 10)
        im.paste(sp, (int(xx), feet - sp.height), sp)
        for sp2, x, y in front: im.paste(sp2, (x, y), sp2)
        lv = lights(i, t)
        if lv < 1: im = Image.alpha_composite(im, Image.new("RGBA", im.size, (8, 10, 28, 190)))
        c.alpha_composite(im, (x0, y0))
        for x in range(x0 - 2, x0 + RW + 2, sill.width): c.alpha_composite(sill.crop((0, 0, min(sill.width, x0 + RW + 2 - x), sill.height)), (x, y0 + RH))
    gy = top + GAP + ROWS * (RH + GAP)                                  # ground floor: glass doors, plaque, plants, sconces
    door = comp("DEC-26"); mid = TW // 2
    for dxx in (-door.width, 0): c.alpha_composite(door, (mid + dxx, bottom - door.height))
    pl = prop("Building plaque, blank", t); c.alpha_composite(pl, (mid + door.width + 14, bottom - 52))
    for px_ in (mid - door.width - 26, mid + door.width + 50): p_ = comp("PLT-01"); c.alpha_composite(p_, (px_, bottom - p_.height))
    for sx_ in (mid - door.width - 12, mid + door.width + 2): s_ = comp("DEC-38"); c.alpha_composite(s_, (sx_, bottom - 70))
    d = ImageDraw.Draw(c); d.rectangle([0, bottom, TW, TH], fill=(40, 40, 48)); d.rectangle([0, bottom, TW, bottom + 3], fill=(84, 84, 94))
    for x in range(0, TW, 48): d.rectangle([x + int(t * 40) % 48, bottom + 60, x + 24 + int(t * 40) % 48, bottom + 63], fill=(200, 190, 120))
    return up(c, TK)

# ---------- break room (SCN-04) and server room (SCN-02) with depth: far layer x8 (the room, people at the back),
# near layer x12 (the cast up front), so the room reads deep instead of stretched ----------
def scn(sid, t):
    fr, tk = scenes.frames_1x(sid); n = sum(tk); u = int(t * 10) % n; acc = 0
    for im, k in zip(fr, tk):
        acc += k
        if u < acc: return im.convert("RGBA").copy()
    return fr[-1].convert("RGBA").copy()
def near(img, sp, cx, feet, k=12):
    sp = sp.crop(sp.getbbox()); big = sp.resize((sp.width * k, sp.height * k), Image.NEAREST)
    lay = Image.new("RGBA", img.size); lay.paste(big, (int(cx - big.width / 2), int(feet - big.height)), big)
    img.paste(lay.convert("RGB"), (0, 0), lay); return img
def breakroom_frame(a, t, u, s0):
    c = scn("SCN-04", t)
    if a.get("copier"):
        sp = rigs.frame("theo", "idle", t, t0=s0); c.alpha_composite(sp, (60 - sp.width // 2, scenes.FLOOR + 2 - sp.height))   # Theo at the counter, far
        img = up(c, 8)
        cp = prop("Floor copier", u); img = near(img, cp, 760, 1930)
        rb = prop("Ream box", u); img = near(img, rb, 980, 1940)
        sp = rigs.frame("ada", "point", t, t0=s0); img = near(img, sp, 330, 1920)
        return img
    sp = rigs.frame("ada", "talk", t, t0=s0, flip=True); c.alpha_composite(sp, (112 - sp.width // 2, scenes.FLOOR + 2 - sp.height))  # Ada at the fridge, far
    img = up(c, 8); walk = 1.0; x = 120 + min(1, u / walk) * 260
    sp = rigs.frame("penny", "walk" if u < walk else "celebrate", t, t0=s0, flip=True); img = near(img, sp, x, 1930)
    sp = rigs.frame("theo", "sip" if "sip" in rigs.anims("theo") else "nod", t, t0=s0, flip=True); img = near(img, sp, 880, 1940)
    return img
def serverroom_frame(a, t, u, s0, dur):
    c = scn("SCN-02", t)
    fk = prop("Forklift", u); rack = comp("TEC-02")
    fx = int(-36 + u / dur * 110)                                             # forklift drives a server rack across, for no reason
    unit = Image.new("RGBA", (fk.width + 30, fk.height + rack.height)); unit.alpha_composite(fk, (0, unit.height - fk.height))
    unit.alpha_composite(rack, (fk.width - 8, unit.height - fk.height + fk.height - rack.height - 6 if False else unit.height - rack.height - 8))
    c.paste(unit, (fx, scenes.FLOOR + 4 - unit.height), unit)
    sp = rigs.frame("ada", "walk", t, t0=s0); c.alpha_composite(sp, (int(110 - u * 10) - sp.width // 2, scenes.FLOOR - sp.height))
    sp = rigs.frame("roz", "holdsign", t, t0=s0); c.alpha_composite(sp, (24 - sp.width // 2, scenes.FLOOR - 2 - sp.height))
    img = up(c, 8)
    big = rigs.frame("kit", "talk", t, t0=s0); big = big.crop(big.getbbox()); K = 18
    big = big.resize((big.width * K, big.height * K), Image.NEAREST)
    lay = Image.new("RGBA", (W, H)); lay.paste(big, (W - int(big.width * 0.62), H - big.height + 120), big)    # lower right, into the bottom of Q1
    img.paste(lay.convert("RGB"), (0, 0), lay)
    return img

# ---------- one shot -> one 1080x1920 frame ----------
def frame_portrait(st, extra, skip=(), wall=None):
    im = st.render(skip=skip, extra=extra, wall=wall); x, y, w, h = st.frames["portrait"]
    return stage.camera(im, x, y, w, h, PORTRAIT).convert("RGB")
def dsk_x(st): return next(x_ for n, uses, _ in st.layers for s_, x_, y_ in uses if s_.startswith("DSK"))

def ring_fx(img, u):
    """the phone rings: it rattles (in the insert), and RING / RING pop on the beat"""
    if (u % 0.5) > 0.32: return img
    d = ImageDraw.Draw(img); f = fit("RING!", 420, 150, wdth=125, wght=900); n = int(u / 0.5)
    x, y, ang = ((300, 520), (780, 600), (340, 680), (760, 500))[n % 4] + (0,)
    d.text((x, y), "RING!", font=f, fill=LIME, anchor="mm", stroke_width=10, stroke_fill="#000000")
    return img

def shot_frame(t):
    s = next((s for s in SHOTS if s[0] <= t < s[1]), SHOTS[-1]); s0, s1, kind, a = s; u = t - s0; dur = s1 - s0
    if kind == "car":
        c = at(board_frames("SCN17V3_00.dc.html", "Riding", dur + 0.2), u).copy()
        sign = prop("Road sign, blank", u); x0, y0, x1, y1 = WIN17
        sx = int(x1 - u * 30) - 10
        lay = Image.new("RGBA", c.size); lay.alpha_composite(sign, (sx - sign.width // 2, y1 - 6 - sign.height))
        mask = Image.new("L", c.size, 0); ImageDraw.Draw(mask).rectangle([x0, y0, x1, y1], fill=255)
        c.paste(lay, (0, 0), Image.composite(lay.getchannel("A"), Image.new("L", c.size, 0), mask))
        return up(c, 8)
    if kind == "tower": return tower_frame(t)
    if kind == "insert":
        st = stage.load(os.path.join(ASSETS, a["st"] + ".dc.html")); p = prop(a["prop"], u); extra = {}
        dx = dsk_x(st)
        if a.get("floor"): cx, rest, lay = dx - 14, 124, "L16"
        else: cx, rest, lay = dx + 28, 92, "L14"
        ring = a.get("ring") and (u % 0.5) < 0.32
        ox = (1 if int(u * 20) % 2 else -1) if ring else 0
        oy = -1 if (a.get("jiggle") and int(u / bt * 2) % 2) else 0
        if ring:                                                             # the screen lights up while it rings
            p = p.copy(); px = p.load()
            for yy in range(p.height):
                for xx in range(p.width):
                    r_, g_, b_, a_ = px[xx, yy]
                    if a_ and g_ > r_ + 12 and g_ > b_ and g_ < 140: px[xx, yy] = (200, 240, 60, a_)
        place(extra, lay, p, cx - p.width // 2 + ox, rest - p.height + oy)
        if a.get("ghost"):
            sp = rigs.frame(a["ghost"], "idle", t, k=1, t0=s0); stand_at(extra, st, ghost(sp), dx + 28, 100)
        skip, extra, wall = dressed(st, a["st"], ("CHR", "MON", "TEC08", "TEC04", "TEC05", "TEC07", "FOD", "DEC09"), extra)
        im = st.render(skip=skip, extra=extra, wall=wall)
        w, h, k = INSERT; img = stage.camera(im, cx - w // 2, rest + 8 - h, w, h, k).convert("RGB")
        return ring_fx(img, u) if a.get("ring") else img
    if kind == "desk":
        st = stage.load(os.path.join(ASSETS, a["st"] + ".dc.html")); extra = {}
        if a.get("back"): back_cast(st, extra, a["back"], t, u, dur * 0.9, s0)
        sp, x, y = desk_rig(st, a["ch"], a["an"], t, s0); place(extra, "L13", sp, x, y)
        m = monitor_back(); dx = dsk_x(st)                                   # the monitor faces the character: we see its back
        place(extra, "L15", m, dx + 56 - m.width + 2 if a.get("mon", "r") == "r" else dx - 2, 99 - m.height)
        skip, extra, wall = dressed(st, a["st"], DESK_SET, extra)
        img = frame_portrait(st, extra, skip=skip, wall=wall)
        return nameplate(img, a.get("name"), a.get("role"), u)
    if kind == "breakroom": return nameplate(breakroom_frame(a, t, u, s0), "COFFEE RUN" if not a.get("copier") else None, "BREAK ROOM", u)
    if kind == "serverroom": return nameplate(serverroom_frame(a, t, u, s0, dur), "SERVER ROOM", "WHERE THE DATA LIVES", u)
    if kind == "title":
        img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img); k = min(1, u / 0.35); f = fit("ROUNDING", W - 200, 150, wdth=125, wght=900)
        d.text((W // 2, 900), "ROUNDING", font=f, fill=INK, anchor="ms"); d.text((W // 2, 1060), "ERROR", font=f, fill=LIME, anchor="ms")
        d.rectangle([W // 2 - int(300 * k), 1100, W // 2 + int(300 * k), 1108], fill=LIME)
        if u > 0.6: d.text((W // 2, 1176), "AN AI TRADING FIRM. ALLEGEDLY.", font=mono(34, True), fill="#9A9A94", anchor="ms")
        if u > 1.2:
            f = fit("NOT FINANCIAL ADVICE", W - 240, 64, wdth=125, wght=900); d.text((W // 2, 1330), "NOT FINANCIAL ADVICE", font=f, fill=INK, anchor="ms")
            d.text((W // 2, 1380), "(there were no numbers. you're welcome.)", font=mono(28), fill="#9A9A94", anchor="ms")
        return img
    img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
    d.text((W // 2, 760), "LIKE + FOLLOW", font=fit("LIKE + FOLLOW", W - 180, 118, wdth=125, wght=900), fill=LIME, anchor="ms")
    d.text((W // 2, 870), "FOR MORE UPDATES", font=fit("FOR MORE UPDATES", W - 260, 70, wdth=110, wght=900), fill=INK, anchor="ms")
    sp = rigs.frame("penny", "point", t, k=8, t0=s0); lay = Image.new("RGBA", (W, H)); lay.alpha_composite(sp, (W // 2 - sp.width // 2, 1600 - sp.height))
    img.paste(lay.convert("RGB"), (0, 0), lay); return img

def teaser_frame(fr):
    img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img); u = fr / FPS
    d.text((W // 2, 820), "A DOCUMENTARY", font=mono(46, True), fill="#9A9A94", anchor="ms")
    if u > 0.25:
        f = fit("ABOUT A FUND", W - 160, 130, wdth=125, wght=900)
        d.text((W // 2, 1010), "ABOUT A FUND", font=f, fill=INK, anchor="ms"); d.text((W // 2, 1150), "RUN BY AIs.", font=f, fill=LIME, anchor="ms")
    return img

def frame_at(tv):
    if tv < TEASE: return strip(teaser_frame(int(tv * FPS)), tv)
    st = tv - TEASE; img = shot_frame(st)
    if st < 3.5: img = daily.cta_pill(img, st)
    return strip(img, tv)                              # no corner disclaimer on this one: it lives on the title card (the boss 2026-11-03)

def panels(out):
    items = [(0.6, "0 · TEASER", "pickup")]
    for i, (s0, s1, kind, a) in enumerate(SHOTS):
        key = s0 + (s1 - s0) * (0.75 if kind == "desk" else 0.5)
        what = a.get("label", kind.upper())
        items.append((TEASE + key, f"{i + 1} · {what}", f"{TEASE + s0:.1f}-{TEASE + s1:.1f}s · {round((s1 - s0) / bt)} beats · {a.get('st', a.get('set', ''))}"))
    pw, ph = 270, 480; cols = 6; rows = (len(items) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (pw + 16) + 16, rows * (ph + 70) + 90), (12, 12, 16)); d = ImageDraw.Draw(sheet)
    d.text((16, 52), f"OFFICE PARODY v5 · STORYBOARD · {CUT['source']} · {CUT['total']:.1f}s · review strip on", font=mono(26, True), fill=LIME, anchor="ls")
    for n, (tv, lab, sub) in enumerate(items):
        x = 16 + (n % cols) * (pw + 16); y = 80 + (n // cols) * (ph + 70)
        sheet.paste(frame_at(tv).resize((pw, ph), Image.LANCZOS), (x, y))
        d.text((x, y + ph + 26), lab[:26], font=mono(18, True), fill=INK, anchor="ls"); d.text((x, y + ph + 50), sub[:30], font=mono(16), fill="#9A9A94", anchor="ls")
    sheet.save(out); print(out, len(items), "panels")

def build():
    os.makedirs(os.path.dirname(OUT), exist_ok=True); total = TEASE + END; wav = os.path.join(WORK, "mix.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", SONG_WAV, "-af", f"apad,atrim=0:{total:.3f},volume=0.9", "-ar", "44100", wav], check=True)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "20",
        "-c:a", "aac", "-b:a", "160k", "-af", "loudnorm=I=-14:TP=-1.5", "-shortest", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
    for i in range(int(round(total * FPS))): p.stdin.write(frame_at(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print(OUT, f"{total:.1f}s")

if __name__ == "__main__":
    panels(OUT) if PANELS else build()
