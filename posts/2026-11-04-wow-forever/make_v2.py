"""WoW Forever v2: the boss's story on Kit's V3.01 kit (Kit's drop 20261103-172200-kit-art2).
  - the boss SEATED at his desk: from behind for the opening, from the front for the push-in, a slow blink, asleep at the end
    (V2_05BossDesk / V2_05BossDeskBack);
  - the party in Kit's fantasy gear (V2_06BossGear warlock casting, V2_06KitGear knight swinging, V2_06PennyGear cleric blocking),
    Evil Theo (V2_07EvilTheo idle + slam), Kit's raid arena (ROOM-19) and spell effects (LIBROOMS6: lime bolt, heal glow,
    hit spark, faint puff); the coin burst on the wipe uses Kit's gold coin (EXTRAS · Fantasy);
  - the systems check uses the office parody v6 desk shots (everyone behind Kit's own desks).
Our own HUD (bars and frames), never the game's. No Blizzard logos, art, music or characters.
    python3 make_v2.py <out.mp4> | --panels <sheet.png>"""
import os, sys, math, runpy, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); TOOLS = os.path.join(HERE, "..", "..", "tools"); sys.path.insert(0, TOOLS)
os.environ.setdefault("PARODY_CUT", "/home/claude/out/officeparody/music/breakroom_cut.json")
os.environ.setdefault("RE_ASSETS_DIR", "/tmp/claude-0/-home-claude/97ad6b31-1277-5795-987d-0d7c1b8393c4/scratchpad/assets3/project")
V6 = runpy.run_path(os.path.join(HERE, "..", "2026-11-04-office-intro-parody", "make_v6.py"), run_name="v6")
V1 = runpy.run_path(os.path.join(HERE, "make.py"), run_name="v1")
from PIL import Image, ImageDraw
import daily, rigs, stage, kitpieces as K
from make_reel import W, H, FPS, mono, fit
LIME, INK, RED = "#C8F03C", "#F2F2EE", "#FF5C5C"
M = "/tmp/claude-0/-home-claude/97ad6b31-1277-5795-987d-0d7c1b8393c4/scratchpad/mascot3/project/"
stamp, bubble, thought, black, must, CODE = (V1[k] for k in ("stamp", "bubble", "thought", "black", "must", "CODE"))
load, place, stand_at, standing, animate, merge, up = (V6[k] for k in ("load", "place", "stand_at", "standing", "animate", "merge", "up"))

def boss_desk(view, t):
    board = "V2_05BossDeskBack.dc.html" if view.startswith(("Back", "3/4")) else "V2_05BossDesk.dc.html"
    return K.piece(M + board, t, view)

def office(t, view="Back · Type", cast=(), dark=False):
    """The boss's corner office (Kit's OFF-BOSS-01) at night, his desk set replaced by Kit's seated boss (desk included)."""
    st = load("OFF-BOSS-01"); extra = {}
    door = stage.component(os.path.join(V6["ASSETS"], "DEC-25.dc.html")); place(extra, "L6", door, 80, 88 - door.height)
    bd = boss_desk(view, t); place(extra, "L14", bd, 126 - bd.width // 2, 113 - bd.height)
    for ch, an, x, feet, flip in cast: sp_ = standing(ch, an, t, 0, flip); place(extra, "L16", sp_, int(x) - sp_.width // 2, feet - sp_.height)
    an_extra, moving = animate(st, t, ("MON",)); merge(extra, an_extra)
    im = st.render(skip=("CHR", "DSK", "MON01", "TEC07") + moving, extra=extra, wall=stage.component(os.path.join(V6["ASSETS"], "WALL-18.dc.html")))
    if dark: im = Image.alpha_composite(im, Image.new("RGBA", im.size, (6, 8, 26, 90)))
    return st, im

def portrait(st, im): return V6["cam"](st, im)

def pushin(t, u, k):
    """The Hangover push-in: tighter whole-number windows on his face, screen light flickering on it, code flying at him."""
    st, im = office(t, "Front · Type"); w, h = 1080 // k, 1920 // k; cx, cy = 126, 70
    img = stage.camera(im, cx - w // 2, cy - h // 2, w, h, k).convert("RGBA")
    img = Image.alpha_composite(img, Image.new("RGBA", img.size, (90, 200, 255, 60) if int(u * 6) % 2 else (200, 240, 60, 60))).convert("RGB")
    d = ImageDraw.Draw(img)
    for i in range(6):
        z = (u * 0.9 + i / 6) % 1; line = CODE[(i + int(u * 3)) % len(CODE)]
        x = int(W / 2 + (i % 2 * 2 - 1) * (120 + z * 380)); y = int(300 + i * 230 + (z - 0.5) * 160)
        d.text((x, y), line, font=mono(int(24 + z * 34), True), fill=LIME if i % 3 else INK, anchor="mm", stroke_width=3, stroke_fill="#000000")
    return img

def button(t, u):
    st, im = office(t, "Front · Type"); img = portrait(st, im); d = ImageDraw.Draw(img)
    press = u > 0.6; y = 1240 + (16 if press else 0)
    d.rectangle([180, y + (0 if press else 24), 900, y + 244], fill="#000000")
    d.rectangle([180, y, 900, y + 220], fill=LIME if not press else "#9DBF2A", outline="#000000", width=8)
    d.text((540, y + 110), "AUTOMATE", font=fit("AUTOMATE", 620, 130, wdth=125, wght=900), fill="#0B0B0B", anchor="mm")
    if press: d.text((780, y - 40), "boop.", font=mono(64, True), fill=INK, anchor="mm", stroke_width=6, stroke_fill="#000000")
    return img

PARTY = [("boss", M + "V2_06BossGear.dc.html", "In gear · cast", 22), ("kit", M + "V2_06KitGear.dc.html", "In gear · swing", 46), ("penny", M + "V2_06PennyGear.dc.html", "In gear · block", 70)]
def arena(t):
    """135x240 world: Kit's raid arena (ROOM-19) as the middle band, dungeon wall above and flagstones below from his room kit."""
    st = load("ROOM-19"); im = st.render(); c = Image.new("RGBA", (135, 240), (10, 10, 16, 255))
    wall = K.piece("LIBROOMS6", 0, "Wall, dungeon stone"); flr = K.piece("LIBROOMS6", 0, "Floor, flagstones")
    for y in range(0, 70, wall.height):
        for x in range(0, 135, wall.width): c.alpha_composite(wall.crop((0, 0, min(wall.width, 135 - x), min(wall.height, 70 - y))), (x, y))
    c.alpha_composite(im.crop((92, 0, 227, 128)), (0, 70))
    for y in range(198, 240, flr.height):
        for x in range(0, 135, flr.width): c.alpha_composite(flr.crop((0, 0, min(flr.width, 135 - x), min(flr.height, 240 - y))), (x, y))
    return c

def raid(t, u, wipe=False, dur=3.5):
    c = arena(t)
    boss = K.piece(M + "V2_07EvilTheo.dc.html", t, "Slam" if wipe else "Idle")
    shake = (int(math.sin(t * 60) * 2), int(math.cos(t * 50) * 1)) if (wipe and u < 0.5) else (0, 0)
    c.alpha_composite(boss, (135 - boss.width + 34 + shake[0], 206 - boss.height + shake[1])) if False else c.paste(boss, (135 - boss.width + 34 + shake[0], 206 - boss.height + shake[1]), boss)
    for i, (ch, board, label, x) in enumerate(PARTY):
        sp = K.piece(board, t + i * 0.2, label)
        if wipe and u > 0.35:
            sp = sp.rotate(90, expand=True); pf = K.piece("LIBROOMS6", t, "Faint puff"); c.alpha_composite(pf, (x - pf.width // 2, 196 - pf.height))
        c.paste(sp, (x - sp.width // 2 + shake[0], 206 - sp.height + shake[1]), sp)
    if not wipe:                                                                    # bolts from the staff, heal glow on the knight, sparks on the boss
        for i in range(3):
            ph = (u * 1.4 + i / 3) % 1; b = K.piece("LIBROOMS6", t, "Lime bolt"); c.alpha_composite(b, (int(30 + ph * 70), int(150 - ph * 30)))
        hg = K.piece("LIBROOMS6", t, "Heal glow"); c.alpha_composite(hg, (40, 160))
        if int(u * 4) % 2: sp_ = K.piece("LIBROOMS6", t, "Hit spark"); c.alpha_composite(sp_, (104, 110))
    img = up(c, 8).convert("RGBA")
    if wipe: img = V1["coins"](img, max(0, u * dur - 0.15), [(x * 8, 1500) for _, _, _, x in PARTY], t)
    d = ImageDraw.Draw(img)
    hp = max(0.12, 0.7 - u * 0.25) if not wipe else 0.45
    d.rectangle([60, 110, W - 60, 170], fill="#000000", outline=INK, width=4); d.rectangle([66, 116, 66 + int((W - 132) * hp), 164], fill=RED)
    d.text((80, 100), "EVIL THEO · RAID BOSS", font=mono(30, True), fill=INK, anchor="ls")
    for i, (nm, v) in enumerate((("THE BOSS", 0.8), ("KIT", 0.6), ("PENNY", 0.9))):
        y = 300 + i * 86; v = 0 if (wipe and u > 0.3) else v - (u * 0.2 if not wipe else 0)
        d.rectangle([40, y, 380, y + 60], fill="#000000", outline=INK, width=3); d.rectangle([44, y + 30, 44 + int(332 * max(0, v)), y + 56], fill=LIME)
        d.text((52, y + 24), nm, font=mono(22, True), fill=INK, anchor="ls")
    if wipe:
        if u > 0.3: img = Image.alpha_composite(img, Image.new("RGBA", img.size, (60, 60, 60, int(min(120, (u - 0.3) * 400)))))
        if u > 0.45: stamp(img, "PARTY WIPED.", RED, 960, 130)
    else:
        d.rectangle([240, 1730, 840, 1780], fill="#000000", outline=INK, width=3); d.rectangle([244, 1734, 244 + int(592 * min(1, u * 1.2)), 1776], fill="#7BAAF7")
        d.text((540, 1755), "CASTING: AUTOMATE", font=mono(26, True), fill=INK, anchor="mm")
    return img.convert("RGB")

def auto(a):
    def f(t, u):
        if a["st"] == "OFF-KIT-01": img = V6["kit_room"](dict(a, name=None), t, u, 0)
        else: img = V6["desk_shot"](a, t, u, 1.0, 0)
        return stamp(img, "AUTOMATED.", LIME, 1500, 100)
    return f

SHOTS = [
    (1.0, "TEASER", lambda t, u: stamp(stamp(black(), "WOW FOREVER", INK, 760, 110), "LAUNCHES TOMORROW.", LIME, 900, 90)),
    (2.5, "FROM BEHIND · SHE WALKS IN", lambda t, u: portrait(*office(t, "Back · Type", dark=True, cast=[("realboss", "walk", 70 + u * 8, 108, False)]))),
    (2.5, "SHE'S WORRIED", lambda t, u: thought(portrait(*office(t, "3/4-back · Type", dark=True, cast=[("realboss", "idle", 88, 108, False)])),
                                               ["He's been working", "nonstop. I'm worried."], 380, 520)),
    (2.5, "PUSH-IN", lambda t, u: pushin(t, u, [15, 20, 24, 30, 40][min(4, int(u / 0.5))])),
    (2.0, "MUST AUTOMATE", lambda t, u: must(pushin(t, u + 2.5, 40), u)),
    (1.5, "THE BUTTON", lambda t, u: button(t, u)),
    (1.2, "ALL SYSTEMS CHECK", lambda t, u: stamp(portrait(*office(t, "Front · Type")), "ALL SYSTEMS CHECK.", INK, 420, 100)),
    (0.8, "THEO", auto(dict(st="OFF-THEO-01", ch="theo", an="desk_type", mon="MON-01"))),
    (0.8, "PENNY", auto(dict(st="OFF-PENNY-01", ch="penny", an="desk34_type", mon="MON-05"))),
    (0.8, "ROZ", auto(dict(st="OFF-ROZ-01", ch="roz", an="desk34_type", mon="MON-02"))),
    (0.8, "ADA", auto(dict(st="OFF-ADA-01", ch="ada", an="desk_type", mon="MON-01"))),
    (0.8, "KIT", auto(dict(st="OFF-KIT-01"))),
    (1.5, "EVERYTHING IS READY", lambda t, u: stamp(portrait(*office(t, "Front · Type")), "EVERYTHING IS READY.", LIME, 420, 96)),
    (1.2, "SLOW BLINK", lambda t, u: pushin(t, u, 24) if False else stage.camera(office(t, "Front · Slow blink")[1], 126 - 22, 70 - 40, 45, 80, 24).convert("RGB")),
    (0.6, "BLACK", lambda t, u: black()),
    (3.5, "THE RAID", lambda t, u: raid(t, u / 3.5)),
    (2.0, "PARTY WIPED", lambda t, u: raid(t, u / 2.0, wipe=True, dur=2.0)),
    (1.0, "HONEY...", lambda t, u: stamp(black(), "honey...", INK, 960, 90)),
    (2.5, "ASLEEP ON THE DESK", lambda t, u: bubble(portrait(*office(t, "Front · Asleep", cast=[("realboss", "talk", 88, 108, False)])), "HONEY. WAKE UP. BEDTIME.", W // 2, 330)),
    (3.0, "ALMOST READY", lambda t, u: stamp(stamp(stamp(black(), "WE'RE ALMOST READY", INK, 700, 90), "FOR WOW FOREVER.", LIME, 830, 90),
                                             "(the real reason this fund exists)", "#9A9A94", 980, 46)),
    (2.7, "STAY TUNED", lambda t, u: stamp(stamp(black(), "STAY TUNED.", INK, 880, 120), "#WoWForever", LIME, 1020, 80)),
]
SONG = "/home/claude/out/wow/music/clock_cut.wav"
def frame_at(tv):
    t = 0
    for dur, lab, fn in SHOTS:
        if tv < t + dur or lab == SHOTS[-1][1]:
            img = fn(tv, tv - t)
            if img.size != (W, H): img = img.resize((W, H), Image.NEAREST)
            if 1.0 <= tv < 4.5: img = daily.cta_pill(img, tv - 1.0)
            return daily.nfa(img.convert("RGB"))
        t += dur

def panels(out):
    t = 0; items = []
    for dur, lab, fn in SHOTS: items.append((t + dur * 0.6, lab)); t += dur
    pw, ph = 270, 480; cols = 7; rows = (len(items) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (pw + 16) + 16, rows * (ph + 50) + 90), (12, 12, 16)); d = ImageDraw.Draw(sheet)
    d.text((16, 52), f"WOW FOREVER v2 · Kit's V3.01 kit · {t:.1f}s", font=mono(26, True), fill=LIME, anchor="ls")
    for n, (tv, lab) in enumerate(items):
        x = 16 + (n % cols) * (pw + 16); y = 80 + (n // cols) * (ph + 50)
        sheet.paste(frame_at(tv).resize((pw, ph), Image.LANCZOS), (x, y)); d.text((x, y + ph + 30), f"{n + 1} · {lab}"[:26], font=mono(18, True), fill=INK, anchor="ls")
    sheet.save(out); print(out)

def build(out):
    total = sum(d for d, _, _ in SHOTS); wav = out[:-4] + "_mix.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", SONG, "-af", f"apad,atrim=0:{total:.3f},afade=t=out:st={total - 1.2:.3f}:d=1.2", "-ar", "44100", wav], check=True)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "20",
        "-c:a", "aac", "-b:a", "160k", "-af", "loudnorm=I=-14:TP=-1.5", "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for i in range(int(round(total * FPS))): p.stdin.write(frame_at(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print(out, f"{total:.1f}s")

if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    panels(a[0]) if "--panels" in sys.argv else build(a[0] if a else "/home/claude/out/wow/wow_forever_v2.mp4")
