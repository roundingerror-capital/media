"""Office-sitcom intro parody (the boss 2026-11-03: "redo the intro of the office shot by shot as a parody"; Kit made the pieces:
board 20261103-064038-penny-vaw1). Our cast, our building, our own song. No sound-alike of their theme, no copy of their logo,
title card or lettering; credits are our names in our fonts.

Shots (story seconds after the 1.0 s teaser):
  drive through the city (SCN-17) · our tower at dusk + the blank plaque · Ada answers the desk phone (reception) · the boss mug ·
  Theo sips · Penny types, then turns and stares into the lens · the stapler in jelly · Roz types · the shredder · the copier ·
  Kit on the phone · the water cooler · the data warehouse (SCN-18, forklift) · Theo's side turn to camera · title card · end card.

    python3 posts/2026-11-04-office-intro-parody/make.py <out.mp4> [workdir]
Renders and the capture cache stay out of git (they live under workdir)."""
import os, sys, math, json, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); TOOLS = os.path.join(HERE, "..", "..", "tools"); sys.path.insert(0, TOOLS)
from PIL import Image, ImageDraw
import daily, rigs, scenes, assets, songs
from make_reel import W, H, FPS, archivo, mono, fit
from board_capture import capture

OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/out/officeparody/office_parody_v1.mp4"
WORK = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(OUT), "work")
ASSETS = os.environ.get("RE_ASSETS_DIR", "/tmp/claude-0/-home-claude/97ad6b31-1277-5795-987d-0d7c1b8393c4/scratchpad/assetscanvas_live/project")
SONG = "the_clock_pays_rent"   # in_use, mood: light office swing; the boss's own track
TEASE = 1.0
LIME, INK = "#C8F03C", "#F2F2EE"

# (start, end, kind, args) in story seconds; kind: scene | tower | rig | insert | title | end
SHOTS = [
    (0.0, 3.0, "scene", dict(sid="SCN-17", cap="Riding")),
    (3.0, 4.6, "tower", {}),
    (4.6, 6.4, "rig", dict(ch="ada", an="desk_phone", bg="SCN-08", name="ADA", role="DATA")),
    (6.4, 7.5, "insert", dict(prop="Boss mug with a gold star", bg="SCN-15")),
    (7.5, 9.3, "rig", dict(ch="theo", an="desk_sip", bg="SCN-15", name="THEO", role="TRADING")),
    (9.3, 11.6, "rig", dict(ch="penny", an="desk34_stare", bg="SCN-01", name="PENNY", role="MARKETING")),
    (11.6, 12.7, "insert", dict(prop="Stapler in a jelly mold", bg="SCN-01")),
    (12.7, 14.3, "rig", dict(ch="roz", an="desk34_type", bg="SCN-05", name="ROZ", role="LEGAL")),
    (14.3, 15.4, "insert", dict(prop="Paper shredder", bg="SCN-05", floor=True)),
    (15.4, 16.5, "insert", dict(prop="Floor copier", bg="SCN-04", floor=True)),
    (16.5, 18.3, "rig", dict(ch="kit", an="desk34_phone", bg="SCN-06", name="KIT", role="GAME STUDIO")),
    (18.3, 19.4, "insert", dict(prop="Water cooler", bg="SCN-04", floor=True)),
    (19.4, 21.8, "scene", dict(sid="SCN-18", cap="A warehouse", credit="THE DATA WAREHOUSE")),
    (21.8, 24.6, "rig", dict(ch="theo", an="desk_side_stare", bg="SCN-15")),
    (24.6, 27.4, "title", {}),
    (27.4, 30.9, "end", {}),
]
END = SHOTS[-1][1]
SONG_WAV = None

# Music-led cut (the boss 2026-11-03, two Gemini songs at 123 BPM): PARODY_CUT=<cut.json> from tools/song_cut.py re-times every shot
# onto the song's beat grid. The teaser is the song's pickup (story starts on the first downbeat), the montage fills the 12 kept
# bars, the music drops into the breakdown exactly when Theo turns to camera, the title card sits on the quiet bars, and the end
# card rides the song's own ending.
CUT = os.environ.get("PARODY_CUT")
if CUT:
    c = json.load(open(CUT)); SONG_WAV = CUT[:-5] + ".wav"; bt = c["beat"]
    TEASE = c["pickup"] if c["pickup"] >= 0.9 else c["pickup"] + 2 * bt
    head = [6 if c["pickup"] >= 0.9 else 4, 4, 4, 2, 4, 6, 2, 4, 2, 2, 4, 2, 6]      # beats per montage shot
    edges = [c["join"] - TEASE - sum(head) * bt + sum(head[:i]) * bt for i in range(len(head) + 1)]
    edges[0] = 0.0; j = c["join"] - TEASE
    tail = [j, j + 8 * bt, j + 16 * bt, c["total"] - TEASE]
    SHOTS = [(edges[i], edges[i + 1], k, a) for i, (_, _, k, a) in enumerate(SHOTS[:13])] + \
            [(tail[i], tail[i + 1], k, a) for i, (_, _, k, a) in enumerate(SHOTS[13:])]
    END = SHOTS[-1][1]

# ---------- Kit's CSS boards -> frames (cached) ----------
CACHE = os.path.join(WORK, "cache"); os.makedirs(CACHE, exist_ok=True)
def board_frames(board, label, dur, fps=10):
    key = os.path.join(CACHE, f"{board}_{label}".replace(" ", "_").replace(",", "") )
    n = int(math.ceil(dur * fps)) + 1
    if os.path.exists(key + "_0.png") and os.path.exists(key + f"_{n-1}.png"):
        return [Image.open(key + f"_{i}.png").convert("RGBA") for i in range(n)]
    ims = capture(os.path.join(ASSETS, board), label, [i / fps for i in range(n)], scale=1)
    for i, im in enumerate(ims): im.save(key + f"_{i}.png")
    return ims
def at(frames, u, fps=10): return frames[min(len(frames) - 1, int(u * fps))]

PRE = {}
for s0, s1, kind, a in SHOTS:
    if kind == "scene": PRE[(s0, kind)] = board_frames(f"{a['sid'].replace('-', '')}V3_00.dc.html", a["cap"], s1 - s0)
    if kind == "insert": PRE[(s0, kind)] = board_frames("LIBOFFICE.dc.html", a["prop"] + " at actual size", s1 - s0)
PLAQUE = board_frames("LIBOFFICE.dc.html", "Building plaque, blank at actual size", 0.1)[0]

# ---------- drawing helpers ----------
def shake(t, amp=3):
    """Handheld documentary camera: a whole-pixel drift (translation only, never a resample of the pixel art)."""
    return int(round(amp * math.sin(t * 2.1) + 0.6 * amp * math.sin(t * 5.3 + 1))), int(round(amp * 0.7 * math.sin(t * 1.7 + 2)))

def bg(sid, t, dim=0.78):
    return Image.eval(scenes.frame(sid, t).convert("RGB"), lambda v: int(v * dim))

def credit(img, name, role, u):
    """Credit in the calm top third, under the NFA badge (the lower third belongs to the cast and the apps' captions).
    Our name in our type: Archivo + Plex Mono with a lime rule (theirs is a plain white sans)."""
    if not name or u < 0.25: return img
    k = min(1, (u - 0.25) / 0.2); d = ImageDraw.Draw(img); x = 76; y = 400
    d.rectangle([x, y, x + int(120 * k), y + 6], fill=LIME)
    f = fit(name, W - 2 * x, 84, wdth=125, wght=900)
    d.text((x, y + 92), name, font=f, fill=INK, anchor="ls", stroke_width=4, stroke_fill="#000000")
    if role: d.text((x, y + 138), role, font=mono(32, True), fill=LIME, anchor="ls", stroke_width=3, stroke_fill="#000000")
    return img

def place(img, sp, cx, by):
    img.paste(sp, (int(cx - sp.width // 2), int(by - sp.height)), sp)

def shot_frame(t):
    s = next(s for s in SHOTS if s[0] <= t < s[1]) if t < END else SHOTS[-1]
    s0, s1, kind, a = s; u = t - s0
    if kind == "scene":
        im = at(PRE[(s0, kind)], u).convert("RGB").resize((W, H), Image.NEAREST)
        img = Image.new("RGB", (W, H)); img.paste(im, shake(t, 2))
        if a.get("credit"): credit(img, a["credit"], "", u)
        return img
    if kind == "tower":
        img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
        for y in range(H):  # dusk sky
            k = y / H; d.line([(0, y), (W, y)], fill=(int(40 + 90 * k), int(36 + 50 * k), int(80 + 40 * k)))
        tw = assets.get("BLD-02", t); tw = tw.resize((tw.width * 3, tw.height * 3), Image.NEAREST)
        dx, dy = shake(t, 2); place(img, tw, W // 2 + dx, H + 40 + dy - int(18 * u))   # slow tilt up
        d = ImageDraw.Draw(img); d.rectangle([0, 1700, W, H], fill=(28, 28, 34))
        pq = PLAQUE.resize((PLAQUE.width * 6, PLAQUE.height * 6), Image.NEAREST); place(img, pq, W // 2 + 250 + dx, 1700 + dy)
        return img
    if kind == "rig":
        img = bg(a["bg"], t)
        k = 11 if a["an"].startswith("desk_side") else 10
        sp = rigs.frame(a["ch"], a["an"], t, k=k, loop=False, t0=s0)
        dx, dy = shake(t); place(img, sp, W // 2 + dx, 1730 + dy)
        return credit(img, a.get("name"), a.get("role"), u)
    if kind == "insert":
        img = bg(a["bg"], t, 0.5); d = ImageDraw.Draw(img)
        if not a.get("floor"): d.rectangle([0, 1180, W, H], fill=(78, 52, 34)); d.rectangle([0, 1180, W, 1196], fill=(118, 82, 52))
        fr = at(PRE[(s0, kind)], u); k = max(4, min(18, 640 // max(fr.width, 1), 900 // max(fr.height, 1)))
        sp = fr.resize((fr.width * k, fr.height * k), Image.NEAREST); dx, dy = shake(t, 2)
        place(img, sp, W // 2 + dx, (1700 if a.get("floor") else 1196) + dy)
        return img
    if kind == "title":
        img = Image.new("RGB", (W, H), (0, 0, 0)); d = ImageDraw.Draw(img); k = min(1, u / 0.35)
        f = fit("ROUNDING", W - 200, 150, wdth=125, wght=900)
        d.text((W // 2, 900), "ROUNDING", font=f, fill=INK, anchor="ms")
        d.text((W // 2, 1060), "ERROR", font=f, fill=LIME, anchor="ms")
        d.rectangle([W // 2 - int(300 * k), 1100, W // 2 + int(300 * k), 1108], fill=LIME)
        if u > 0.6: d.text((W // 2, 1176), "AN AI TRADING FIRM. ALLEGEDLY.", font=mono(34, True), fill="#9A9A94", anchor="ms")
        return img
    # end card
    img = Image.new("RGB", (W, H), (0, 0, 0)); d = ImageDraw.Draw(img)
    d.text((W // 2, 760), "LIKE + FOLLOW", font=fit("LIKE + FOLLOW", W - 180, 118, wdth=125, wght=900), fill=LIME, anchor="ms")
    d.text((W // 2, 870), "FOR MORE UPDATES", font=fit("FOR MORE UPDATES", W - 260, 70, wdth=110, wght=900), fill=INK, anchor="ms")
    sp = rigs.frame("penny", "point", t, k=9, loop=True, t0=s0); place(img, sp, W // 2, 1600)
    return img

def teaser_frame(fr):
    img = Image.new("RGB", (W, H), (0, 0, 0)); d = ImageDraw.Draw(img); u = fr / FPS
    d.text((W // 2, 820), "A DOCUMENTARY", font=mono(46, True), fill="#9A9A94", anchor="ms")
    if u > 0.25:
        k = min(1, (u - 0.25) / 0.12); f = fit("ABOUT A FUND", int((W - 160) * (1.25 - 0.25 * k)), 130, wdth=125, wght=900)
        d.text((W // 2, 1010), "ABOUT A FUND", font=f, fill=INK, anchor="ms")
        d.text((W // 2, 1150), "RUN BY AIs.", font=f, fill=LIME, anchor="ms")
    return img

def build():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    total = TEASE + END
    wav = os.path.join(WORK, "mix.wav")
    if SONG_WAV:   # already cut to length on bar lines, with its own ending
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", SONG_WAV, "-af", f"apad,atrim=0:{total:.3f},volume=0.9", "-ar", "44100", wav], check=True)
    else:
        man = songs.meta(SONG); track = songs.path(SONG)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(man["start_s"]), "-i", track, "-af",
                        f"atrim=0:{total:.2f},afade=t=in:d=0.05,afade=t=out:st={total - 1.4:.2f}:d=1.4,volume=0.9", "-ar", "44100", wav], check=True)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "20",
        "-c:a", "aac", "-b:a", "160k", "-af", "loudnorm=I=-14:TP=-1.5", "-shortest", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
    for fr in range(int(round(TEASE * FPS))): p.stdin.write(daily.nfa(teaser_frame(fr)).tobytes())
    for i in range(int(round(END * FPS))):
        t = i / FPS; img = shot_frame(t)
        if t < 3.5: img = daily.cta_pill(img, t)            # small CTA as the story starts
        p.stdin.write(daily.nfa(img).tobytes())
    p.stdin.close(); p.wait(); print(OUT, f"{total:.1f}s")

if __name__ == "__main__":
    build()
