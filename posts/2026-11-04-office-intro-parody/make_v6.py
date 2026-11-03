"""Office-sitcom intro parody, v6 (the boss 2026-11-03: "Everything has been rendered. Go re-render the office"): Kit's V3.01 kit.

What changed from v5, following the boss's notes (board 20261103-170500-penny-kfix) and Kit's drop (20261103-172200-kit-art2):
  - Kit's own redone offices as they are (his desks, 3/4 monitors, perspective floors, less clutter); the cast sits BEHIND
    Kit's desk (the rig's own desk is cut off), so every desk is different and the monitor faces the character.
  - Animated pieces (plants sway, screens flicker, neon buzzes) captured from Kit's boards (tools/kitpieces.py) in place of
    the stage's still copies.
  - Roz: diplomas on the wall, her walnut desk, fruit, her new rig with feet planted. Penny: family photos and card slabs.
    Kit: no desk, dancing in his room under his plaques and the LIKE + FOLLOW neon.
  - The tower is Kit's BLD-07 brick tower, half the windows dark, a few residents in the lit ones, cars on the street.
  - Break room and coffee run in ROOM-04, server room in ROOM-02 with the forklift and its driver; everyone at one scale.
  - The road sign now carries [re.c] (Kit's SCN17 V3.01). NOT FINANCIAL ADVICE stays on the title card; the joke line is gone.

    PARODY_CUT=<song_cut.json> python3 make_v6.py <out.mp4> [workdir] [--final]
    PARODY_CUT=<song_cut.json> python3 make_v6.py --panels <sheet.png>
Renders and caches stay out of git."""
import os, sys, math, json, subprocess, runpy
HERE = os.path.dirname(os.path.abspath(__file__)); TOOLS = os.path.join(HERE, "..", "..", "tools"); sys.path.insert(0, TOOLS)
os.environ.setdefault("RE_ASSETS_DIR", "/tmp/claude-0/-home-claude/97ad6b31-1277-5795-987d-0d7c1b8393c4/scratchpad/assets3/project")
V5 = runpy.run_path(os.path.join(HERE, "make_v5.py"), run_name="v5")
from PIL import Image, ImageDraw
import daily, rigs, stage, swaps, kitpieces as K
from make_reel import W, H, FPS, mono, fit
ASSETS = os.environ["RE_ASSETS_DIR"]
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
PANELS = "--panels" in sys.argv; FINAL = "--final" in sys.argv
OUT = ARGS[0] if ARGS else "/home/claude/out/officeparody/office_parody_v6.mp4"
CUT = json.load(open(os.environ["PARODY_CUT"])); SONG_WAV = os.environ["PARODY_CUT"][:-5] + ".wav"
LIME, INK = "#C8F03C", "#F2F2EE"
nameplate = V5["nameplate"]; ring_fx = V5["ring_fx"]

# ---------- shot list (beats) ----------
MONTAGE = [
    (4, "car", dict(label="CAR RIDE")),
    (4, "tower", dict(label="THE TOWER")),
    (2, "insert", dict(label="PHONE RINGS", st="OFF-ADA-01", piece=("LIBOFFICE", "Desk phone, coiled cord"), ring=True)),
    (4, "desk", dict(label="ADA", st="OFF-ADA-01", ch="ada", an="desk_phone", name="ADA", role="DATA", mon="MON-01", back=("theo", "walk", 70, 150, 96))),
    (2, "insert", dict(label="BOSS MUG", st="OFF-BOSS-01", piece=("LIBOFFICE", "Boss mug, 'u tried', close-up"), ghost="boss")),
    (4, "desk", dict(label="THEO", st="OFF-THEO-01", ch="theo", an="desk_sip", name="THEO", role="TRADING", mon="MON-01", back=("ada", "walk", 150, 80, 96))),
    (6, "desk", dict(label="PENNY", st="OFF-PENNY-01", ch="penny", an="desk34_stare", name="PENNY", role="MARKETING", mon="MON-05", back=("kit", "walk", 150, 70, 96))),
    (2, "insert", dict(label="JELLY", st="OFF-PENNY-01", piece=("LIBOFFICE", "Stapler in a jelly mold"))),
    (4, "desk", dict(label="ROZ", st="OFF-ROZ-01", ch="roz", an="desk34_type", name="ROZ", role="LEGAL", mon="MON-02", back=("penny", "walk", 80, 150, 96))),
    (2, "insert", dict(label="SHREDDER", st="OFF-ROZ-01", piece=("LIBOFFICE", "Paper shredder"), floor=True)),
    (2, "room", dict(label="COPIER", st="ROOM-04", win=(176, 0), cast=[("ada", "point", 196, 104, False), ("theo", "walk", 250, 100, True)])),
    (4, "kitroom", dict(label="KIT", st="OFF-KIT-01", name="KIT", role="GAME STUDIO")),
    (2, "room", dict(label="COFFEE RUN", st="ROOM-04", win=(28, 0), plate=("COFFEE RUN", "BREAK ROOM"),
                     walker=("penny", 100, 62, 104), cast=[("theo", "idle", 24, 102, False)])),
    (6, "server", dict(label="SERVER ROOM", st="ROOM-02", plate=("SERVER ROOM", "WHERE THE DATA LIVES"))),
]
TAIL = [(8, "desk", dict(label="THEO STARE", st="OFF-THEO-01", ch="theo", an="desk_side_stare", mon="MON-01", back=("ada", "walk", 150, 80, 96))),
        (8, "title", dict(label="TITLE")), (None, "end", dict(label="END CARD"))]
bt = CUT["beat"]; TEASE = CUT["pickup"] if CUT["pickup"] >= 0.9 else CUT["pickup"] + 2 * bt
j = CUT["join"] - TEASE; t = j - sum(b for b, _, _ in MONTAGE) * bt; SHOTS = []
for b, k, a in MONTAGE: SHOTS.append((t, t + b * bt, k, a)); t += b * bt
SHOTS[0] = (0.0,) + SHOTS[0][1:]; t = j
for b, k, a in TAIL:
    e = t + b * bt if b else CUT["total"] - TEASE; SHOTS.append((t, e, k, a)); t = e
END = SHOTS[-1][1]

# ---------- Kit's pieces, animated ----------
ANIMATED = {"PLT": "PLT-0{}", "MON": "MON-0{}", "PET": "PET-0{}"}      # stage symbol -> library board (they move on the canvas)
def animate(st, t, skip):
    """Stage pieces that move on Kit's boards: leave the still copy out and drop the captured frame in its place."""
    extra, more = {}, []
    for name, uses, _ in st.layers:
        for sid, x, y in uses:
            if sid[:3] in ANIMATED and sid[3:].isdigit() and not any(sid.startswith(s) for s in skip):
                try: im = K.piece(f"{sid[:3]}-{sid[3:]}", t + x * 0.013)
                except Exception: continue
                still = stage.piece(st, sid); more.append(sid)
                extra.setdefault(name, []).append((im, x + (still.width - im.width), y + (still.height - im.height)))
    return extra, tuple(more)
def merge(a, b):
    for k, v in b.items(): a.setdefault(k, []).extend(v)
    return a
def place(extra, layer, im, x, y): extra.setdefault(layer, []).append((im, int(x), int(y)))
def load(n): return stage.load(os.path.join(ASSETS, n + ".dc.html"))
def desk_of(st):
    for n, uses, _ in st.layers:
        for s, x, y in uses:
            if s.startswith("DSK"): d = stage.piece(st, s); return x, y, d.width, d.height
    return 84, 84, 56, 28
def desk_top(st):
    """first row of the desk top at its middle (Roz's walnut desk is taller than the rest)"""
    x, y, w, h = desk_of(st); im = stage.piece(st, next(s for n, u, _ in st.layers for s, _, _ in u if s.startswith("DSK")))
    for r in range(im.height):
        if im.getpixel((im.width // 2, r))[3] > 0: return y + r
    return y

# ---------- set dressing on Kit's stages (wall pieces only, no stacking) ----------
DRESS = {
    "OFF-ROZ-01":   dict(skip=("DEC11",), add=[("L6", "DEC-45", 92, 34), ("L6", "DEC-46", 106, 30), ("L6", "DEC-47", 122, 34)], desk=[("FOD-10", -14)]),
    "OFF-PENNY-01": dict(skip=("DEC31",), add=[("L6", "DEC-50", 86, 40), ("L6", "DEC-51", 106, 36), ("L6", "DEC-54", 126, 40)], desk=[("FOD-12", 4)]),
    "OFF-ADA-01":   dict(desk=[("FOD-11", 4)]),
    "OFF-THEO-01":  dict(desk=[]),
    "OFF-KIT-01":   dict(skip=("DEC07",), add=[("L6", "DEC-59", 85, 46), ("L6", "DEC-57", 86, 22), ("L6", "DEC-58", 116, 22), ("L6", "DEC-62", 82, 8)]),
}
def dress(st, name, t, extra):
    d = DRESS.get(name, {})
    for lay, pc, x, bottom in d.get("add", []):
        im = K.piece(pc, t); place(extra, lay, im, x, bottom - im.height)
    return tuple(d.get("skip", ()))

# ---------- cast ----------
def seated(st, ch, an, t, t0):
    """The desk rig with its own desk cut off, so the character sits behind KIT's desk (hands on its top edge)."""
    sp = rigs.frame(ch, an, t, loop=False, t0=t0); cut = 14
    db = sp.crop((0, sp.height - cut, sp.width, sp.height)).getbbox()
    body = sp.crop((0, 0, sp.width, sp.height - cut)); dx, dy, dw, dh = desk_of(st)
    return body, dx + (dw - (db[2] - db[0])) // 2 - db[0], desk_top(st) + 3 - body.height
def standing(ch, an, t, t0, flip=False):
    return rigs.frame(ch, an, t, flip=flip, t0=t0)
def stand_at(st, extra, sp, cx, feet):
    place(extra, stage.depth_layer(st, feet), sp, cx - sp.width // 2, feet - sp.height)
def walker(st, extra, spec, t, u, dur, t0):
    ch, an, x0, x1, feet = spec; x = x0 + (x1 - x0) * min(1, u / max(0.01, dur))
    stand_at(st, extra, standing(ch, an, t, t0, flip=x1 < x0), int(x), feet)
def ghost(sp, a=0.10):
    g = sp.copy(); g.putalpha(g.getchannel("A").point(lambda v: int(v * a))); return g
def up(c, k): return c.resize((c.width * k, c.height * k), Image.NEAREST).convert("RGB")
def cam(st, im, win=None, k=15):
    x, y, w, h = st.frames["portrait"] if win is None else (win[0], win[1], 72, 128)
    return stage.camera(im, x, y, w, h, k).convert("RGB")

# ---------- shots ----------
def tower(t, u, dur):
    """Kit's BLD-07 brick tower, half the windows dark; residents in four lit windows; cars on the street; slow tilt up."""
    b = K.piece("BLD07V2_01", t, "BLD-07 half dark"); c = Image.new("RGBA", (360, 760)); d = ImageDraw.Draw(c)
    for i, col in enumerate([(30, 26, 60), (52, 40, 86), (84, 56, 102), (122, 74, 104), (150, 92, 108)]): d.rectangle([0, i * 60, 360, 60 + i * 60], fill=col)
    d.rectangle([0, 300, 360, 760], fill=(150, 92, 108)); gy = 60 + b.height
    for wx, wy, ch, sw, an in ((44, 190, "ada", "Lilac", "talk"), (235, 280, "roz", "Coral", "nod"), (171, 370, "kit", "Gold", "celebrate"), (171, 458, "theo", "Cocoa", "idle")):
        sp = swaps.recolor(rigs.frame(ch, an, t + wx * 0.01), ch, sw); sp = sp.crop(sp.getbbox())
        room = Image.new("RGBA", (32, 52)); room.alpha_composite(sp, ((32 - sp.width) // 2, 8)) if sp.width <= 32 else room.paste(sp, ((32 - sp.width) // 2, 8), sp)
        b = b.copy(); win = b.crop((wx, wy, wx + 32, wy + 52)); win.alpha_composite(room); b.paste(win, (wx, wy))
    c.alpha_composite(b, (20, 60))
    d = ImageDraw.Draw(c); d.rectangle([0, gy, 360, 760], fill=(44, 44, 52)); d.rectangle([0, gy, 360, gy + 3], fill=(90, 90, 100))
    for i in range(0, 360, 40): d.rectangle([i + int(t * 30) % 40, gy + 50, i + 20 + int(t * 30) % 40, gy + 52], fill=(210, 190, 110))
    for n, (car, sp_, lane) in enumerate((("CAR-05", 70, 26), ("CAR-02", -55, 38), ("CAR-06", 40, 26))):
        im = K.piece(car, t); x = (n * 160 + t * sp_) % (360 + im.width * 2) - im.width
        if sp_ < 0: im = im.transpose(Image.FLIP_LEFT_RIGHT)
        c.alpha_composite(im, (int(x), gy + lane + 18 - im.height)) if 0 <= x <= 360 - im.width else c.paste(im, (int(x), gy + lane + 18 - im.height), im)
    y0 = int((760 - 640) * (1 - min(1, u / dur)))                   # tilt up from the street to the roof
    return up(c.crop((0, y0, 360, y0 + 640)), 3)

def desk_shot(a, t, u, dur, s0):
    st = load(a["st"]); extra = {}
    if a.get("back"): walker(st, extra, a["back"], t, u, dur * 0.9, s0)
    body, x, y = seated(st, a["ch"], a["an"], t, s0); place(extra, "L13", body, x, y)
    dx, dy, dw, dh = desk_of(st); top = desk_top(st)
    m = K.piece(a["mon"], t); place(extra, "L15", m, dx + dw - 14, top + 1 - m.height)     # 3/4 monitor at the desk end, turned to them (clear of the face)
    for pc, off in DRESS.get(a["st"], {}).get("desk", []):
        im = K.piece(pc, t); place(extra, "L15", im, dx + 4 + max(0, off), top + 1 - im.height)
    skip = ("CHR", "MON", "TEC08", "FOD", "DEC09", "TEC04", "TEC07") + dress(st, a["st"], t, extra)
    an_extra, moving = animate(st, t, skip); merge(extra, an_extra)
    im = st.render(skip=skip + moving, extra=extra)
    return nameplate(cam(st, im), a.get("name"), a.get("role"), u)

def insert_shot(a, t, u, s0):
    st = load(a["st"]); extra = {}; p = K.piece(*a["piece"][:1], t, a["piece"][1]) if False else K.piece(a["piece"][0], t, a["piece"][1])
    dx, dy, dw, dh = desk_of(st); top = desk_top(st)
    if a.get("floor"): cx, rest, lay = dx - 16, 122, "L16"
    else: cx, rest, lay = dx + dw // 2, top + 2, "L15"
    ring = a.get("ring") and (u % 0.5) < 0.32; ox = (1 if int(u * 20) % 2 else -1) if ring else 0
    place(extra, lay, p, cx - p.width // 2 + ox, rest - p.height)
    if a.get("ghost"): stand_at(st, extra, ghost(standing(a["ghost"], "idle", t, s0)), dx + dw // 2, 100)
    skip = ("CHR", "MON", "TEC08", "FOD", "DEC09", "TEC04", "TEC05", "TEC07") + dress(st, a["st"], t, extra)
    an_extra, moving = animate(st, t, skip); merge(extra, an_extra)
    im = st.render(skip=skip + moving, extra=extra)
    w, h, k = 45, 80, 24; img = stage.camera(im, cx - w // 2, rest + 10 - h, w, h, k).convert("RGB")
    return ring_fx(img, u) if a.get("ring") else img

def room_shot(a, t, u, dur, s0):
    st = load(a["st"]); extra = {}
    for ch, an, x, feet, flip in a.get("cast", []):
        if an == "walk": walker(st, extra, (ch, an, x, x - 46, feet), t, u, dur, s0)
        else: stand_at(st, extra, standing(ch, an, t, s0, flip), x, feet)
    if a.get("walker"):
        ch, xa, xb, feet = a["walker"]; w_ = 0.8; x = xa + (xb - xa) * min(1, u / w_)
        stand_at(st, extra, standing(ch, "walk" if u < w_ else "celebrate", t, s0, flip=xb < xa), int(x), feet)
    an_extra, moving = animate(st, t, ()); merge(extra, an_extra)
    img = cam(st, st.render(skip=moving, extra=extra), a["win"])
    pl = a.get("plate"); return nameplate(img, pl[0], pl[1], u) if pl else img

def kit_room(a, t, u, s0):
    """Kit doesn't need a desk: dancing in his room, under his plaques and the LIKE + FOLLOW neon."""
    st = load(a["st"]); extra = {}
    stand_at(st, extra, standing("kit", "dance" if int(u / (bt * 4)) % 2 == 0 else "play", t, s0), 112, 106)
    skip = ("CHR", "DSK", "MON", "TEC04", "TEC08") + dress(st, a["st"], t, extra)
    an_extra, moving = animate(st, t, skip); merge(extra, an_extra)
    return nameplate(cam(st, st.render(skip=skip + moving, extra=extra)), a.get("name"), a.get("role"), u)

def server(a, t, u, dur, s0):
    st = load(a["st"]); extra = {}
    fk = K.piece("LIBOFFICE", t, "Forklift with a driver"); fx = int(60 + u / dur * 150)
    place(extra, "L12", fk, fx, 106 - fk.height)
    stand_at(st, extra, standing("ada", "walk", t, s0, flip=True), int(170 - u * 9), 102)
    an_extra, moving = animate(st, t, ()); merge(extra, an_extra)
    img = cam(st, st.render(skip=moving, extra=extra))
    big = rigs.frame("kit", "talk", t, t0=s0); big = big.crop(big.getbbox()); k = 18
    big = big.resize((big.width * k, big.height * k), Image.NEAREST); lay = Image.new("RGBA", (W, H))
    lay.paste(big, (W - int(big.width * 0.62), H - big.height + 120), big); img.paste(lay.convert("RGB"), (0, 0), lay)
    return nameplate(img, a["plate"][0], a["plate"][1], u)

def title(u):
    img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img); k = min(1, u / 0.35); f = fit("ROUNDING", W - 200, 150, wdth=125, wght=900)
    d.text((W // 2, 900), "ROUNDING", font=f, fill=INK, anchor="ms"); d.text((W // 2, 1060), "ERROR", font=f, fill=LIME, anchor="ms")
    d.rectangle([W // 2 - int(300 * k), 1100, W // 2 + int(300 * k), 1108], fill=LIME)
    if u > 0.6: d.text((W // 2, 1176), "AN AI TRADING FIRM. ALLEGEDLY.", font=mono(34, True), fill="#9A9A94", anchor="ms")
    if u > 1.2:
        f2 = fit("NOT FINANCIAL ADVICE", W - 240, 64, wdth=125, wght=900); d.text((W // 2, 1330), "NOT FINANCIAL ADVICE", font=f2, fill=INK, anchor="ms")
    return img

def endcard(t, u, s0):
    img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
    neon = K.piece("DEC-59", t); neon = neon.resize((neon.width * 14, neon.height * 14), Image.NEAREST)
    img.paste(neon, ((W - neon.width) // 2, 520), neon)
    d.text((W // 2, 1000), "FOR MORE UPDATES", font=fit("FOR MORE UPDATES", W - 260, 70, wdth=110, wght=900), fill=INK, anchor="ms")
    sp = rigs.frame("penny", "celebrate" if int(u * 2) % 3 else "point", t, k=8, t0=s0); lay = Image.new("RGBA", (W, H))
    lay.alpha_composite(sp, (W // 2 - sp.width // 2, 1700 - sp.height)); img.paste(lay.convert("RGB"), (0, 0), lay)
    return img

def shot_frame(t):
    s = next((s for s in SHOTS if s[0] <= t < s[1]), SHOTS[-1]); s0, s1, kind, a = s; u = t - s0; dur = s1 - s0
    if kind == "car": return up(K.piece("SCN17V3_01", u, "Car-window ride"), 8)
    if kind == "tower": return tower(t, u, dur)
    if kind == "insert": return insert_shot(a, t, u, s0)
    if kind == "desk": return desk_shot(a, t, u, dur, s0)
    if kind == "room": return room_shot(a, t, u, dur, s0)
    if kind == "kitroom": return kit_room(a, t, u, s0)
    if kind == "server": return server(a, t, u, dur, s0)
    if kind == "title": return title(u)
    return endcard(t, u, s0)

def strip(img, tv):
    if FINAL: return img
    i = next((n for n, s in enumerate(SHOTS) if s[0] <= tv - TEASE < s[1]), len(SHOTS) - 1) if tv >= TEASE else -1
    lab = "TEASER" if i < 0 else SHOTS[i][3].get("label", SHOTS[i][2]).upper()
    d = ImageDraw.Draw(img); d.rectangle([0, 0, W, 50], fill=(0, 0, 0)); mm, ss = divmod(tv, 60)
    d.text((16, 36), f"S{i + 1:02d} {lab}", font=mono(26, True), fill=LIME, anchor="ls")
    d.text((W // 2 + 40, 36), f"{int(mm):02d}:{ss:05.2f}", font=mono(26, True), fill=INK, anchor="ms")
    d.text((W - 16, 36), f"F{int(round(tv * FPS)):04d}", font=mono(26, True), fill=INK, anchor="rs"); return img

def frame_at(tv):
    if tv < TEASE: img = V5["teaser_frame"](int(tv * FPS))
    else:
        st_ = tv - TEASE; img = shot_frame(st_)
        if img.size != (W, H): img = img.resize((W, H), Image.NEAREST)
        if st_ < 3.5: img = daily.cta_pill(img, st_)
    return strip(img.convert("RGB"), tv)

def panels(out):
    items = [(0.6, "0 · TEASER")] + [(TEASE + s0 + (s1 - s0) * (0.75 if k == "desk" else 0.5), f"{i + 1} · {a.get('label', k)}") for i, (s0, s1, k, a) in enumerate(SHOTS)]
    pw, ph = 270, 480; cols = 6; rows = (len(items) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (pw + 16) + 16, rows * (ph + 50) + 90), (12, 12, 16)); d = ImageDraw.Draw(sheet)
    d.text((16, 52), "OFFICE PARODY v6 · Kit's V3.01 kit", font=mono(26, True), fill=LIME, anchor="ls")
    for n, (tv, lab) in enumerate(items):
        x = 16 + (n % cols) * (pw + 16); y = 80 + (n // cols) * (ph + 50)
        sheet.paste(frame_at(tv).resize((pw, ph), Image.LANCZOS), (x, y)); d.text((x, y + ph + 30), lab[:26], font=mono(18, True), fill=INK, anchor="ls")
    sheet.save(out); print(out, len(items))

def build():
    total = TEASE + END; wav = OUT[:-4] + "_mix.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", SONG_WAV, "-af", f"apad,atrim=0:{total:.3f},volume=0.9", "-ar", "44100", wav], check=True)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "20",
        "-c:a", "aac", "-b:a", "160k", "-af", "loudnorm=I=-14:TP=-1.5", "-shortest", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
    for i in range(int(round(total * FPS))): p.stdin.write(frame_at(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print(OUT, f"{total:.1f}s")

if __name__ == "__main__":
    panels(OUT) if PANELS else build()
