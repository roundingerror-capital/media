"""Office-sitcom intro parody, v4: STAGED ROOMS IN DEPTH (the boss 2026-11-03, on the v3 panels: "you're using the background as
a background despite it being assets... people can be in the back doing stuff with other people in the middle and some upfront";
"ZOOM in the background instead of stretching it vertically"; "all scenes need 1++ characters").

Every office shot is one of Kit's OFF stages (Assets Designs, Offices page: a 192x128 world of kit pieces in depth layers, at the
scale Kit set next to the cast) rendered by tools/stage.py, with the cast inserted INTO the layers:
  - back    : a colleague walking or standing by the back wall (feet y 92-100), drawn before the furniture that stands in front
  - middle  : the desk rig (character + its own desk) in the place of Kit's desk set, at Kit's desk position
  - front   : the pet, the shredder, the big foreground Kit in the warehouse
Cameras are Kit's own portrait window (72x128, x15 -> 1080x1920): no vertical stretch, the room is zoomed, not pulled.
Inserts (mug, phone, jelly, crossword) are a 45x80 window (x24) of the same stage, the prop standing on Kit's desk top.
The break room is composed from kit components (stage.Set) until Kit's BREAK ROOM stage lands (board request 20261103-121114).

    PARODY_CUT=<song_cut.json> python3 make_v4.py <out.mp4> [workdir]      # full render, shots on the song's beat grid
    PARODY_CUT=<song_cut.json> python3 make_v4.py --panels <sheet.png>      # storyboard: one panel per shot, before any render
Renders and caches stay out of git."""
import os, sys, math, json, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); TOOLS = os.path.join(HERE, "..", "..", "tools"); sys.path.insert(0, TOOLS)
from PIL import Image, ImageDraw
import daily, rigs, assets, stage
from make_reel import W, H, FPS, archivo, mono, fit
from board_capture import capture

ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
PANELS = "--panels" in sys.argv
OUT = ARGS[0] if ARGS else "/home/claude/out/officeparody/office_parody_v4.mp4"
WORK = ARGS[1] if len(ARGS) > 1 else os.path.join(os.path.dirname(OUT), "work_v4")
ASSETS = os.environ.get("RE_ASSETS_DIR", "/tmp/claude-0/-home-claude/97ad6b31-1277-5795-987d-0d7c1b8393c4/scratchpad/assetscanvas_live/project")
CUT = json.load(open(os.environ["PARODY_CUT"])); SONG_WAV = os.environ["PARODY_CUT"][:-5] + ".wav"
LIME, INK = "#C8F03C", "#F2F2EE"
WIN17 = (15, 40, 121, 168)      # SCN-17 car window opening (the parallax region), native px
PORTRAIT = 15                   # Kit's 72x128 window x15 = 1080x1920
INSERT = (45, 80, 24)           # insert window x24

# ---------- shot list, in beats (the song's own grid) ----------
# kind: car | tower | insert | desk | room | warehouse | title | end
# back=(ch, anim, x0, x1, feet_y): a colleague at the back wall, walking from x0 to x1 over the shot (x0==x1: standing)
MONTAGE = [
    (4, "car", {}),                                                                              # drive in, road sign slides past
    (4, "tower", {}),                                                                            # our tower (Kit: lights, residents)
    (2, "insert", dict(prop="Desk phone, coiled cord", st="OFF-ADA-01", ring=True)),             # the phone rings on Ada's desk...
    (4, "desk", dict(ch="ada", an="desk_phone", st="OFF-ADA-01", name="ADA", role="DATA",
                     back=("theo", "walk", 60, 150, 95))),                                       # ...Ada answers; Theo crosses the back
    (2, "insert", dict(prop="Boss mug with a gold star", st="OFF-BOSS-01", ghost="boss")),       # the mug (Kit: "u tried"); the boss, 10%
    (4, "desk", dict(ch="theo", an="desk_sip", st="OFF-THEO-01", name="THEO", role="TRADING",
                     back=("ada", "idle", 130, 130, 96))),                                       # Theo sips; Ada at the shelves
    (6, "desk", dict(ch="penny", an="desk34_stare", st="OFF-PENNY-01", name="PENNY", role="MARKETING",
                     back=("kit", "walk", 160, 40, 94))),                                        # Penny types, turns, stares; Kit walks by
    (2, "insert", dict(prop="Stapler in a jelly mold", st="OFF-PENNY-01", jiggle=True)),         # the jelly (Kit: real jiggle frames)
    (4, "desk", dict(ch="roz", an="desk34_type", st="OFF-ROZ-01", name="ROZ", role="LEGAL",
                     front=[("Paper shredder", 134, 126)], back=("penny", "idle", 82, 82, 97))),  # Roz; shredder up front; Penny behind
    (2, "insert", dict(prop="Newspaper with a crossword", st="OFF-ROZ-01")),                     # the crossword
    (2, "room", dict(set="break", front=[("Floor copier", 80, 124), ("Ream box", 120, 127)],
                     cast=[("ada", "idle", 104, 110, True), ("theo", "idle", 76, 98, False)])),   # copier + ream box; Ada feeds it; Theo at the counter
    (4, "desk", dict(ch="kit", an="desk34_phone", st="OFF-KIT-01", name="KIT", role="GAME STUDIO",
                     back=("roz", "walk", 40, 150, 95))),                                        # Kit on the phone; Roz crosses
    (2, "room", dict(set="break", front=[("Water cooler", 120, 122)], walker=("penny", 64, 100, 118),
                     cast=[("theo", "idle", 78, 98, False)])),                                    # the cooler; Penny walks up to it
    (6, "warehouse", dict(credit="THE DATA WAREHOUSE")),                                         # forklift + pallets; Kit up front
]
TAIL = [(8, "desk", dict(ch="theo", an="desk_side_stare", st="OFF-THEO-01", back=("ada", "walk", 150, 60, 95))),
        (8, "title", {}), (None, "end", {})]

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
def credit(img, name, role, u):
    if not name or u < 0.25: return img
    k = min(1, (u - 0.25) / 0.2); d = ImageDraw.Draw(img); x = 76; y = 400
    d.rectangle([x, y, x + int(120 * k), y + 6], fill=LIME)
    d.text((x, y + 92), name, font=fit(name, W - 2 * x, 84, wdth=125, wght=900), fill=INK, anchor="ls", stroke_width=4, stroke_fill="#000000")
    if role: d.text((x, y + 138), role, font=mono(32, True), fill=LIME, anchor="ls", stroke_width=3, stroke_fill="#000000")
    return img

# ---------- the break room, composed from kit components (until Kit's stage lands) ----------
_SETS = {}
def break_room():
    if "break" in _SETS: return _SETS["break"]
    s = stage.Set()
    s.tile("wall", comp("WALL-09"), 0, 88); s.tile("floor", comp("FLR-03"), 88, 128)
    s.tile("base", comp("SHL-01"), 83, 88)
    s.add("trim", comp("DEC-03"), 100, 24)                     # clock
    s.add("trim", comp("DEC-32"), 62, 62)                      # bulletin board
    s.layer("people_back")                                     # someone at the counter stands behind it
    s.add("backwall", comp("DEC-24"), 112, 88)                 # door
    s.add("backwall", comp("DEC-27"), 60, 100)                 # credenza (the coffee counter)
    s.add("backwall", comp("FOD-02"), 66, 76); s.add("backwall", comp("FOD-05"), 86, 76); s.add("backwall", comp("FOD-08"), 76, 75)
    s.add("backwall", comp("PLT-02"), 100, 104)
    s.layer("mid"); s.layer("front")
    _SETS["break"] = s; return s

# ---------- one shot -> one 1080x1920 frame ----------
def frame_portrait(st, extra, skip=()):
    im = st.render(skip=skip, extra=extra); x, y, w, h = st.frames["portrait"]
    return stage.camera(im, x, y, w, h, PORTRAIT).convert("RGB")

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
    if kind == "tower":
        c = Image.new("RGBA", (270, 480)); d = ImageDraw.Draw(c)
        bands = [(38, 32, 72), (52, 40, 86), (74, 50, 98), (102, 62, 104), (132, 78, 104)]
        for i, col in enumerate(bands): d.rectangle([0, i * 80, 270, i * 80 + 80], fill=col)
        tw = assets.get("BLD-02", t); dy = -int(u * 6)
        c.alpha_composite(tw, (135 - tw.width // 2, 452 - dy - tw.height))
        d = ImageDraw.Draw(c); d.rectangle([0, 452 - dy, 270, 480], fill=(40, 40, 48)); d.rectangle([0, 452 - dy, 270, 453 - dy], fill=(70, 70, 80))
        pl = prop("Building plaque, blank", u); c.alpha_composite(pl, (196 - pl.width // 2, 440 - dy - pl.height))
        return up(c, 4)
    if kind == "insert":
        st = stage.load(os.path.join(ASSETS, a["st"] + ".dc.html")); p = prop(a["prop"], u); extra = {}
        dx = next(x for n, uses, _ in st.layers for s_, x, y in uses if s_.startswith("DSK")); cx = dx + 28; rest = 92
        ox = (1 if int(u * 16) % 2 else -1) if (a.get("ring") and (u % 0.5) < 0.3) else 0       # the phone rattles on its rings
        oy = -1 if (a.get("jiggle") and int(u * bt * 8) % 2) else 0                               # the jelly bounces on the beat (Kit: squash frames)
        place(extra, "L14", p, cx - p.width // 2 + ox, rest - p.height + oy)
        if a.get("ghost"):
            sp = rigs.frame(a["ghost"], "idle", t, k=1, t0=s0); stand_at(extra, st, ghost(sp), dx + 28, 100)
        im = st.render(skip=("CHR", "MON", "TEC08", "TEC04", "TEC05", "TEC07", "FOD", "DEC09"), extra=extra)
        w, h, k = INSERT; return stage.camera(im, cx - w // 2, rest + 8 - h, w, h, k).convert("RGB")
    if kind == "desk":
        st = stage.load(os.path.join(ASSETS, a["st"] + ".dc.html")); extra = {}
        if a.get("back"): back_cast(st, extra, a["back"], t, u, dur * 0.9, s0)
        sp, x, y = desk_rig(st, a["ch"], a["an"], t, s0); place(extra, "L13", sp, x, y)
        for lab, cx, feet in a.get("front", []):
            p = prop(lab, u); place(extra, "L15", p, cx - p.width // 2, feet - p.height)
        img = frame_portrait(st, extra, skip=DESK_SET)
        return credit(img, a.get("name"), a.get("role"), u)
    if kind == "room":
        s_ = break_room(); extra = {}
        for ch, an, cx, feet, flip in a.get("cast", []):
            sp = rigs.frame(ch, an, t, k=1, flip=flip, t0=s0); place(extra, "people_back" if feet < 100 else "mid" if feet < 112 else "front", sp, cx - sp.width // 2, feet - sp.height)
        for lab, cx, feet in a.get("front", []):
            p = prop(lab, u); place(extra, "front", p, cx - p.width // 2, feet - p.height)
        if a.get("walker"):
            ch, xa, xb, feet = a["walker"]; walk = 0.75; x = int(xa + (xb - xa) * min(1, u / walk))
            sp = rigs.frame(ch, "walk" if u < walk else "idle", t, k=1, t0=s0); place(extra, "mid", sp, x - sp.width // 2, feet - sp.height)
        im = s_.render(extra=extra)
        return stage.camera(im, 60, 0, 72, 128, PORTRAIT).convert("RGB")
    if kind == "warehouse":
        c = at(board_frames("SCN18V3_00.dc.html", "A warehouse", dur + 0.2), u).copy()        # 135x240 at x8
        for ch, an, cx, feet, flip in (("ada", "walk", 30 + int(u * 8), 186, False), ("roz", "idle", 100, 184, True)):
            sp = rigs.frame(ch, an, t, k=1, flip=flip, t0=s0); c.alpha_composite(sp, (cx - sp.width // 2, feet - sp.height))
        img = up(c, 8)
        K = 28; big = rigs.frame("kit", "talk", t, k=1, t0=s0); big = big.crop(big.getbbox()); big = big.resize((big.width * K, big.height * K), Image.NEAREST)
        lay = Image.new("RGBA", (W, H)); lay.alpha_composite(big, (W - int(big.width * 0.72), H - big.height - 40))   # 70% tall, on the right
        img.paste(lay.convert("RGB"), (0, 0), lay)
        return credit(img, a.get("credit"), "", u)
    if kind == "title":
        img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img); k = min(1, u / 0.35); f = fit("ROUNDING", W - 200, 150, wdth=125, wght=900)
        d.text((W // 2, 900), "ROUNDING", font=f, fill=INK, anchor="ms"); d.text((W // 2, 1060), "ERROR", font=f, fill=LIME, anchor="ms")
        d.rectangle([W // 2 - int(300 * k), 1100, W // 2 + int(300 * k), 1108], fill=LIME)
        if u > 0.6: d.text((W // 2, 1176), "AN AI TRADING FIRM. ALLEGEDLY.", font=mono(34, True), fill="#9A9A94", anchor="ms")
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
    if tv < TEASE: return daily.nfa(teaser_frame(int(tv * FPS)))
    st = tv - TEASE; img = shot_frame(st)
    if st < 3.5: img = daily.cta_pill(img, st)
    return daily.nfa(img)

def panels(out):
    items = [(0.6, "0 · TEASER", "pickup")]
    for i, (s0, s1, kind, a) in enumerate(SHOTS):
        key = s0 + (s1 - s0) * (0.75 if kind == "desk" else 0.5)
        what = a.get("name") or a.get("prop") or a.get("credit") or {"car": "CAR RIDE + ROAD SIGN", "tower": "TOWER (Kit: lights)",
                "room": " + ".join(p for p, _, _ in a.get("front", [])), "title": "TITLE CARD", "end": "END CARD"}.get(kind, kind.upper())
        if kind == "desk" and not a.get("name"): what = "THEO TURNS TO CAMERA (music drops)"
        items.append((TEASE + key, f"{i + 1} · {what}", f"{TEASE + s0:.1f}-{TEASE + s1:.1f}s · {round((s1 - s0) / bt)} beats · {a.get('st', a.get('set', ''))}"))
    pw, ph = 270, 480; cols = 6; rows = (len(items) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (pw + 16) + 16, rows * (ph + 70) + 90), (12, 12, 16)); d = ImageDraw.Draw(sheet)
    d.text((16, 52), f"OFFICE PARODY v4 · STORYBOARD · {CUT['source']} · {CUT['total']:.1f}s · Kit's stages, cast in depth", font=mono(26, True), fill=LIME, anchor="ls")
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
