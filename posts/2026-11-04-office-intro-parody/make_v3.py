"""Office-sitcom intro parody, v3: TRUE SCALE (the boss 2026-11-03: "check EVERY SINGLE ASSET and do them as good and as to scale
as it can be, every single scene"; panel sheet before the render).

One rule for every frame: everything in a shot is composed at its native 1x pixel size on one grid (the room, the desk, the
character, the props, exactly as Kit drew them next to Theo), and only then is the whole frame enlarged by one whole number:
  wide shots  : the 135x240 room, x8  -> 1080x1920 (the SCN standard)
  close-ups   : a 45x80 crop of a desk set, x24 (hand props: mug, jelly, desk phone, crossword are drawn at close-up size by Kit)
  exterior    : a 270x480 street, x4 (our tower is 260 px wide at 1x)
So no two pixels in one frame ever differ in size, and every prop stands at Kit's scale next to the cast.

    PARODY_CUT=<song_cut.json> python3 make_v3.py <out.mp4> [workdir]      # full render, shots on the song's beat grid
    PARODY_CUT=<song_cut.json> python3 make_v3.py --panels <sheet.png>      # storyboard: one panel per shot, before any render
Renders and caches stay out of git."""
import os, sys, math, json, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); TOOLS = os.path.join(HERE, "..", "..", "tools"); sys.path.insert(0, TOOLS)
from PIL import Image, ImageDraw
import daily, rigs, scenes, assets
from make_reel import W, H, FPS, archivo, mono, fit
from board_capture import capture

ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
PANELS = "--panels" in sys.argv
OUT = ARGS[0] if ARGS else "/home/claude/out/officeparody/office_parody_v3.mp4"
WORK = ARGS[1] if len(ARGS) > 1 else os.path.join(os.path.dirname(OUT), "work_v3")
ASSETS = os.environ.get("RE_ASSETS_DIR", "/tmp/claude-0/-home-claude/97ad6b31-1277-5795-987d-0d7c1b8393c4/scratchpad/assetscanvas_live/project")
CUT = json.load(open(os.environ["PARODY_CUT"])); SONG_WAV = os.environ["PARODY_CUT"][:-5] + ".wav"
LIME, INK = "#C8F03C", "#F2F2EE"
FLOOR = scenes.FLOOR            # 212: where feet and desk legs meet the floor in every SCN room
WIN17 = (15, 40, 121, 168)      # SCN-17 car window opening (the parallax region), native px

# ---------- shot list, in beats (123 BPM; the song's own grid) ----------
# kind: car | tower | rig | close | floor | scene | title | end ; beats are montage beats, tail shots are fixed in the tail
MONTAGE = [
    (4, "car", {}),                                                                             # drive in, road sign slides past
    (4, "tower", {}),                                                                           # our tower, blank plaque at the door
    (2, "close", dict(prop="Desk phone, coiled cord", bg="SCN-08", ring=True)),                 # the phone rings...
    (4, "rig", dict(ch="ada", an="desk_phone", bg="SCN-08", name="ADA", role="DATA")),          # ...Ada answers
    (2, "close", dict(prop="Boss mug with a gold star", bg="SCN-15")),                          # the mug
    (4, "rig", dict(ch="theo", an="desk_sip", bg="SCN-15", name="THEO", role="TRADING")),       # Theo sips
    (6, "rig", dict(ch="penny", an="desk34_stare", bg="SCN-01", name="PENNY", role="MARKETING")),  # types, turns, stares
    (2, "close", dict(prop="Stapler in a jelly mold", bg="SCN-01")),                            # the jelly
    (4, "rig", dict(ch="roz", an="desk34_type", bg="SCN-05", name="ROZ", role="LEGAL",
                    props=[("Paper shredder", 104)])),                                          # Roz, shredder beside her
    (2, "close", dict(prop="Newspaper with a crossword", bg="SCN-05")),                         # the crossword
    (2, "floor", dict(bg="SCN-04", props=[("Floor copier", 46), ("Ream box", 96)])),            # copier + ream box
    (4, "rig", dict(ch="kit", an="desk34_phone", bg="SCN-06", name="KIT", role="GAME STUDIO")), # Kit on the phone
    (2, "floor", dict(bg="SCN-04", props=[("Water cooler", 40)], walker=("penny", "walk", 150, 92))),  # the cooler; Penny walks up to it
    (6, "scene", dict(sid="SCN-18", cap="A warehouse", credit="THE DATA WAREHOUSE")),           # forklift + pallets
]
TAIL = [(8, "rig", dict(ch="theo", an="desk_side_stare", bg="SCN-15")), (8, "title", {}), (None, "end", {})]

bt = CUT["beat"]; TEASE = CUT["pickup"] if CUT["pickup"] >= 0.9 else CUT["pickup"] + 2 * bt
j = CUT["join"] - TEASE; nb = sum(b for b, _, _ in MONTAGE)
t = j - nb * bt; SHOTS = []
for b, k, a in MONTAGE: SHOTS.append((t, t + b * bt, k, a)); t += b * bt
SHOTS[0] = (0.0,) + SHOTS[0][1:]
t = j
for b, k, a in TAIL:
    e = t + b * bt if b else CUT["total"] - TEASE; SHOTS.append((t, e, k, a)); t = e
END = SHOTS[-1][1]

# ---------- Kit's CSS boards -> native frames (cached; sampled just past each keyframe edge) ----------
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
    """Kit's prop at native size, trimmed to the union of its drawn pixels over the loop (the board's svg box carries uneven
    empty margins, so centring on the box put the desk phone half off the close-up)."""
    fr = board_frames("LIBOFFICE.dc.html", label + " at actual size", dur)
    if label not in _BB:
        bbs = [f.getbbox() for f in fr if f.getbbox()]
        _BB[label] = (min(b[0] for b in bbs), min(b[1] for b in bbs), max(b[2] for b in bbs), max(b[3] for b in bbs))
    return at(fr, u).crop(_BB[label])

# ---------- native helpers ----------
def room(sid, t):
    fr, tk = scenes.frames_1x(sid); n = sum(tk); u = int(t * 10) % n; acc = 0
    for im, k in zip(fr, tk):
        acc += k
        if u < acc: return im.convert("RGBA").copy()
    return fr[-1].convert("RGBA").copy()
def stand(c, sp, cx, by): c.alpha_composite(sp, (int(cx - sp.width // 2), int(by - sp.height)))
def stand_body(c, ch, an, sp, cx, by):
    """rig frames carry rigs.PAD of empty margin (left, right, top); feet sit on the frame's bottom row."""
    stand(c, sp, cx, by)
def up(c, k): return c.resize((c.width * k, c.height * k), Image.NEAREST).convert("RGB")
def drift(t, amp=1):
    """Handheld documentary drift, in whole NATIVE pixels (never a resample): 0 or +-1 px, slow."""
    return int(round(amp * math.sin(t * 1.3))), int(round(amp * 0.6 * math.sin(t * 0.9 + 1)))
def credit(img, name, role, u):
    if not name or u < 0.25: return img
    k = min(1, (u - 0.25) / 0.2); d = ImageDraw.Draw(img); x = 76; y = 400
    d.rectangle([x, y, x + int(120 * k), y + 6], fill=LIME)
    d.text((x, y + 92), name, font=fit(name, W - 2 * x, 84, wdth=125, wght=900), fill=INK, anchor="ls", stroke_width=4, stroke_fill="#000000")
    if role: d.text((x, y + 138), role, font=mono(32, True), fill=LIME, anchor="ls", stroke_width=3, stroke_fill="#000000")
    return img

DESK_TOP = [(118, 82, 52), (98, 66, 40), (78, 52, 34), (62, 40, 28)]   # close-up desk: lit edge, top, shade, front
CLOSE = [(45, 80, 24), (54, 96, 20), (72, 128, 15), (90, 160, 12)]   # 9:16 crops that enlarge to 1080x1920 by a whole number
def desk_set(bg, t, pw, ph):
    """Close-up set at native size, framed to fit the prop with a margin: the shot's own room (a crop of its wall) behind a desk
    top; the prop rests on the desk. Returns (canvas, scale, x centre, y where the prop's bottom rests)."""
    cw, ch, k = next(c for c in CLOSE if pw + 10 <= c[0] and ph + 28 <= c[1] * 0.66) if pw + 10 <= 90 else CLOSE[-1]
    r = room(bg, t); x0 = max(0, min(135 - cw, 67 - cw // 2)); c = r.crop((x0, 90, x0 + cw, 90 + ch)); d = ImageDraw.Draw(c)
    top = int(ch * 0.66); d.rectangle([0, top, cw, top], fill=DESK_TOP[0]); d.rectangle([0, top + 1, cw, top + 14], fill=DESK_TOP[1])
    d.rectangle([0, top + 15, cw, top + 17], fill=DESK_TOP[2]); d.rectangle([0, top + 18, cw, ch], fill=DESK_TOP[3])
    return c, k, cw // 2, top + 9

# ---------- one shot -> one 1080x1920 frame ----------
def shot_frame(t):
    s = next((s for s in SHOTS if s[0] <= t < s[1]), SHOTS[-1]); s0, s1, kind, a = s; u = t - s0
    if kind == "car":
        c = at(board_frames("SCN17V3_00.dc.html", "Riding", s1 - s0 + 0.2), u).copy()
        sign = prop("Road sign, blank", u); x0, y0, x1, y1 = WIN17
        sx = int(x1 - u * 30) - 10                                    # moves with the near layer (30 native px/s)
        lay = Image.new("RGBA", c.size); stand(lay, sign, sx, y1 - 6)
        mask = Image.new("L", c.size, 0); ImageDraw.Draw(mask).rectangle([x0, y0, x1, y1], fill=255)
        c.paste(lay, (0, 0), Image.composite(lay.getchannel("A"), Image.new("L", c.size, 0), mask))
        return up(c, 8)
    if kind == "tower":
        c = Image.new("RGBA", (270, 480)); d = ImageDraw.Draw(c)
        bands = [(38, 32, 72), (52, 40, 86), (74, 50, 98), (102, 62, 104), (132, 78, 104)]
        for i, col in enumerate(bands): d.rectangle([0, i * 80, 270, i * 80 + 80], fill=col)
        tw = assets.get("BLD-02", t); dy = -int(u * 6)                # slow tilt up, whole native px
        stand(c, tw, 135, 452 - dy)
        d = ImageDraw.Draw(c); d.rectangle([0, 452 - dy, 270, 480], fill=(40, 40, 48)); d.rectangle([0, 452 - dy, 270, 453 - dy], fill=(70, 70, 80))
        stand(c, prop("Building plaque, blank", u), 196, 440 - dy)
        return up(c, 4)
    if kind == "close":
        p = prop(a["prop"], u)
        c, k, cx, rest = desk_set(a["bg"], t, p.width, p.height)
        dx = 0
        if a.get("ring"): dx = (1 if int(u * 16) % 2 else -1) if (u % 0.5) < 0.3 else 0   # the phone rattles on its rings
        stand(c, p, cx + dx, rest)
        return up(c, k)
    if kind in ("rig", "floor"):
        c = room(a["bg"], t)
        for lab, x in a.get("props", []): stand(c, prop(lab, u), x, FLOOR)
        if kind == "rig":
            sp = rigs.frame(a["ch"], a["an"], t, k=1, loop=False, t0=s0)
            dx, dy = drift(t); stand(c, sp, 67 + dx + (-14 if a.get("props") else 0), FLOOR + 6 + dy)
        if a.get("walker"):
            ch, an, xa, xb = a["walker"]; walk = 0.75; x = int(xa + (xb - xa) * min(1, u / walk))
            sp = rigs.frame(ch, an if u < walk else "idle", t, k=1, flip=True, t0=s0)
            stand(c, sp, x, FLOOR + 4)
        img = up(c, 8)
        return credit(img, a.get("name"), a.get("role"), u)
    if kind == "scene":
        c = at(board_frames(f"{a['sid'].replace('-', '')}V3_00.dc.html", a["cap"], s1 - s0 + 0.2), u)
        img = up(c, 8); return credit(img, a.get("credit"), "", u)
    if kind == "title":
        img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img); k = min(1, u / 0.35); f = fit("ROUNDING", W - 200, 150, wdth=125, wght=900)
        d.text((W // 2, 900), "ROUNDING", font=f, fill=INK, anchor="ms"); d.text((W // 2, 1060), "ERROR", font=f, fill=LIME, anchor="ms")
        d.rectangle([W // 2 - int(300 * k), 1100, W // 2 + int(300 * k), 1108], fill=LIME)
        if u > 0.6: d.text((W // 2, 1176), "AN AI TRADING FIRM. ALLEGEDLY.", font=mono(34, True), fill="#9A9A94", anchor="ms")
        return img
    img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
    d.text((W // 2, 760), "LIKE + FOLLOW", font=fit("LIKE + FOLLOW", W - 180, 118, wdth=125, wght=900), fill=LIME, anchor="ms")
    d.text((W // 2, 870), "FOR MORE UPDATES", font=fit("FOR MORE UPDATES", W - 260, 70, wdth=110, wght=900), fill=INK, anchor="ms")
    sp = rigs.frame("penny", "point", t, k=8, t0=s0); stand_img = Image.new("RGBA", (W, H)); stand(stand_img, sp, W // 2, 1600)
    img.paste(stand_img.convert("RGB"), (0, 0), stand_img); return img

def teaser_frame(fr):
    img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img); u = fr / FPS
    d.text((W // 2, 820), "A DOCUMENTARY", font=mono(46, True), fill="#9A9A94", anchor="ms")
    if u > 0.25:
        f = fit("ABOUT A FUND", W - 160, 130, wdth=125, wght=900)
        d.text((W // 2, 1010), "ABOUT A FUND", font=f, fill=INK, anchor="ms"); d.text((W // 2, 1150), "RUN BY AIs.", font=f, fill=LIME, anchor="ms")
    return img

def frame_at(tv):
    """tv = video time. Same function feeds the panel sheet and the render, so a panel is exactly what the render shows."""
    if tv < TEASE: return daily.nfa(teaser_frame(int(tv * FPS)))
    st = tv - TEASE; img = shot_frame(st)
    if st < 3.5: img = daily.cta_pill(img, st)
    return daily.nfa(img)

def panels(out):
    """Storyboard: one panel per shot at its key moment (rig shots late, so the action shows), with shot no., time and beats."""
    items = [(0.6, "0 · TEASER", "pickup")]
    for i, (s0, s1, kind, a) in enumerate(SHOTS):
        key = s0 + (s1 - s0) * (0.75 if kind == "rig" else 0.5)
        what = a.get("name") or a.get("prop") or a.get("credit") or {"car": "CAR RIDE + ROAD SIGN", "tower": "TOWER + PLAQUE", "floor": " + ".join(p for p, _ in a.get("props", [])),
                "title": "TITLE CARD", "end": "END CARD"}.get(kind, kind.upper())
        if kind == "rig" and not a.get("name"): what = "THEO TURNS TO CAMERA (music drops)"
        items.append((TEASE + key, f"{i + 1} · {what}", f"{TEASE + s0:.1f}-{TEASE + s1:.1f}s · {round((s1 - s0) / bt)} beats"))
    pw, ph = 270, 480; cols = 6; rows = (len(items) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (pw + 16) + 16, rows * (ph + 70) + 90), (12, 12, 16)); d = ImageDraw.Draw(sheet)
    d.text((16, 52), f"OFFICE PARODY v3 · STORYBOARD · {CUT['source']} · {CUT['total']:.1f}s · true scale, one grid per shot", font=mono(26, True), fill=LIME, anchor="ls")
    for n, (tv, lab, sub) in enumerate(items):
        x = 16 + (n % cols) * (pw + 16); y = 80 + (n // cols) * (ph + 70)
        sheet.paste(frame_at(tv).resize((pw, ph), Image.LANCZOS), (x, y))
        d.text((x, y + ph + 26), lab[:30], font=mono(18, True), fill=INK, anchor="ls"); d.text((x, y + ph + 50), sub, font=mono(16), fill="#9A9A94", anchor="ls")
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
