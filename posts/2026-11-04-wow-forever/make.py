"""WoW Forever (launch day, 2026-11-04): the boss automates the whole firm just in time, then hides to play and yells for snacks.

Story (the boss 2026-11-03): the boss pacing 24/7, pushing commits, talking to Claude nonstop, so everything runs itself in time
for World of Warcraft: Forever; last beat, he's hidden away playing and yells at the real boss for snacks.
Kit's art only (OFF stages, kit components, library sprites, rigs, palette swaps), composed like the office parody (make_v5.py).
No Blizzard logos, art, music or characters: the game is named in words only, plus the launch hashtag.

    python3 make.py --panels <sheet.png>      # storyboard (first draft)
Renders stay out of git."""
import os, sys, runpy
HERE = os.path.dirname(os.path.abspath(__file__)); TOOLS = os.path.join(HERE, "..", "..", "tools"); sys.path.insert(0, TOOLS)
os.environ.setdefault("PARODY_CUT", "/home/claude/out/officeparody/music/breakroom_cut.json")
P = runpy.run_path(os.path.join(HERE, "..", "2026-11-04-office-intro-parody", "make_v5.py"), run_name="parody")   # shared helpers
from PIL import Image, ImageDraw
import rigs, stage
from make_reel import W, H, FPS, mono, fit
ASSETS, comp, prop, place, dressed, desk_rig, monitor_back, nameplate, up, dsk_x = (P[k] for k in
    ("ASSETS", "comp", "prop", "place", "dressed", "desk_rig", "monitor_back", "nameplate", "up", "dsk_x"))
LIME, INK, RED = "#C8F03C", "#F2F2EE", "#FF5C5C"
P["DRESS"]["OFF-BOSS-01"] = dict(P["DRESS"]["OFF-BOSS-01"], wall="WALL-18")   # mustard: the shadow-chimp boss reads against it (navy hid him)
COMMITS = ["feat: automate the posts", "feat: automate the fact sheets", "fix: automate the fixes", "chore: automate the chores",
           "feat: automate the automation", "docs: nobody reads this", "feat: auto-approve (just kidding)", "push --tired"]

def boss_office(t, u, extra=None, an="walk", x=None, dark=False):
    st = stage.load(os.path.join(ASSETS, "OFF-BOSS-01.dc.html")); extra = extra or {}
    span = 56; ph = (u * 22) % (2 * span); xx = x if x is not None else 84 + (ph if ph < span else 2 * span - ph)
    sp = rigs.frame("boss", an, t, flip=not (ph < span) if x is None else False)
    place(extra, "L13", sp, int(xx - sp.width // 2), 102 - sp.height)
    skip, extra, wall = dressed(st, "OFF-BOSS-01", ("CHR",), extra)
    im = st.render(skip=skip, extra=extra, wall=wall)
    if dark: im = Image.alpha_composite(im, Image.new("RGBA", im.size, (6, 8, 26, 150)))
    x0, y0, w, h = st.frames["portrait"]
    return stage.camera(im, x0, y0, w, h, 15).convert("RGB")

def commits(img, u, n=5):
    d = ImageDraw.Draw(img); f = mono(34, True); y = 1180
    k = int(u * 6)
    for i in range(max(0, k - n), k):
        d.rectangle([40, y - 40, W - 40, y + 12], fill=(0, 0, 0))
        d.text((60, y), "$ git commit -m \"" + COMMITS[i % len(COMMITS)] + "\"", font=f, fill=LIME, anchor="ls"); y += 62
    return img

def bubble(img, txt, cx, y, size=58):
    d = ImageDraw.Draw(img); f = fit(txt, W - 200, size, wdth=110, wght=900); tw = int(f.getlength(txt))
    d.rectangle([cx - tw // 2 - 30, y - 24, cx + tw // 2 + 30, y + size + 20], fill=INK, outline="#000000", width=6)
    d.polygon([(cx - 20, y + size + 20), (cx + 10, y + size + 20), (cx - 30, y + size + 60)], fill=INK)
    d.text((cx, y + size // 2), txt, font=f, fill="#0B0B0B", anchor="mm"); return img

def stamp(img, txt, col=LIME, y=820, size=120):
    d = ImageDraw.Draw(img); f = fit(txt, W - 160, size, wdth=125, wght=900)
    d.text((W // 2, y), txt, font=f, fill=col, anchor="mm", stroke_width=10, stroke_fill="#000000"); return img

def desk_shot(t, u, st_name, ch, an):
    st = stage.load(os.path.join(ASSETS, st_name + ".dc.html")); extra = {}
    sp, x, y = desk_rig(st, ch, an, t, 0); place(extra, "L13", sp, x, y)
    m = monitor_back(); dx = dsk_x(st); place(extra, "L15", m, dx + 56 - m.width + 2, 99 - m.height)
    skip, extra, wall = dressed(st, st_name, P["DESK_SET"], extra)
    im = st.render(skip=skip, extra=extra, wall=wall); x0, y0, w, h = st.frames["portrait"]
    return stage.camera(im, x0, y0, w, h, 15).convert("RGB")

def cave(t, u):
    """The hideout: Kit's game room with the lights off, the boss at the arcade cabinet, headphones on."""
    st = stage.load(os.path.join(ASSETS, "OFF-KIT-01.dc.html")); extra = {}
    sp = rigs.frame("boss", "celebrate" if int(u * 2) % 2 else "idle", t); place(extra, "L13", sp, 108 - sp.width // 2, 104 - sp.height)
    skip, extra, wall = dressed(st, "OFF-KIT-01", P["DESK_SET"], extra)
    im = st.render(skip=skip, extra=extra, wall=wall)
    im = Image.alpha_composite(im, Image.new("RGBA", im.size, (6, 8, 26, 110)))
    x0, y0, w, h = st.frames["portrait"]; return stage.camera(im, x0, y0, w, h, 15).convert("RGB")

def realboss(t, u):
    st = stage.load(os.path.join(ASSETS, "OFF-BOSS-01.dc.html")); extra = {}
    sp = rigs.frame("realboss", "shakehead", t); place(extra, "L13", sp, 112 - sp.width // 2, 104 - sp.height)
    skip, extra, wall = dressed(st, "OFF-BOSS-01", ("CHR",), extra)
    im = st.render(skip=skip, extra=extra, wall=wall); x0, y0, w, h = st.frames["portrait"]
    return stage.camera(im, x0, y0, w, h, 15).convert("RGB")

def black(): return Image.new("RGB", (W, H))

# (seconds, label, draw(t, u) -> 1080x1920 RGB)
SHOTS = [
    (1.0, "TEASER", lambda t, u: stamp(stamp(black(), "WOW FOREVER", INK, 760, 110), "LAUNCHES TOMORROW.", LIME, 900, 90)),
    (2.5, "THE DEADLINE", lambda t, u: nameplate(boss_office(t, u), "THE BOSS", "HAS ONE DAY", u)),
    (3.0, "COMMITS", lambda t, u: commits(boss_office(t, u, an="talk", x=110), u)),
    (2.0, "TALKING TO CLAUDE", lambda t, u: bubble(boss_office(t, u, an="talk", x=96), "CLAUDE. AUTOMATE IT.", W // 2, 360)),
    (2.0, "3:12 AM", lambda t, u: stamp(boss_office(t, u, dark=True), "3:12 AM", INK, 420, 140)),
    (1.0, "AUTO · THEO", lambda t, u: stamp(desk_shot(t, u, "OFF-THEO-01", "theo", "desk_type"), "AUTOMATED.", LIME, 1500, 100)),
    (1.0, "AUTO · PENNY", lambda t, u: stamp(desk_shot(t, u, "OFF-PENNY-01", "penny", "desk34_type"), "AUTOMATED.", LIME, 1500, 100)),
    (1.0, "AUTO · ROZ", lambda t, u: stamp(desk_shot(t, u, "OFF-ROZ-01", "roz", "desk34_type"), "AUTOMATED.", LIME, 1500, 100)),
    (1.0, "AUTO · ADA", lambda t, u: stamp(desk_shot(t, u, "OFF-ADA-01", "ada", "desk_type"), "AUTOMATED.", LIME, 1500, 100)),
    (2.0, "LAUNCH DAY", lambda t, u: nameplate(boss_office(t, u, an="celebrate", x=110), "LAUNCH DAY", "EVERYTHING RUNS ITSELF", u)),
    (2.5, "THE HIDEOUT", lambda t, u: nameplate(cave(t, u), "THE BOSS", "IN A MEETING", u)),
    (2.0, "SNACKS PLEASE!", lambda t, u: stamp(cave(t, u), "SNACKS PLEASE!!", RED, 820, 140)),
    (2.5, "THE REAL BOSS", lambda t, u: realboss(t, u)),
    (2.0, "SEE YOU SUNDAY", lambda t, u: stamp(stamp(black(), "SEE YOU SUNDAY.", INK, 860, 110), "#WoWForever", LIME, 1000, 80)),
]

def panels(out):
    items = []; t = 0
    for dur, lab, fn in SHOTS: items.append((t, dur, lab, fn)); t += dur
    pw, ph = 270, 480; cols = 7; rows = (len(items) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (pw + 16) + 16, rows * (ph + 70) + 90), (12, 12, 16)); d = ImageDraw.Draw(sheet)
    d.text((16, 52), f"WOW FOREVER · STORYBOARD DRAFT 1 · {t:.1f}s · Kit's assets only", font=mono(26, True), fill=LIME, anchor="ls")
    for n, (s0, dur, lab, fn) in enumerate(items):
        u = dur * 0.6; img = fn(s0 + u, u)
        x = 16 + (n % cols) * (pw + 16); y = 80 + (n // cols) * (ph + 70)
        sheet.paste(img.resize((pw, ph), Image.LANCZOS), (x, y))
        d.text((x, y + ph + 26), f"{n + 1} · {lab}"[:26], font=mono(18, True), fill=INK, anchor="ls")
        d.text((x, y + ph + 50), f"{s0:.1f}-{s0 + dur:.1f}s", font=mono(16), fill="#9A9A94", anchor="ls")
    sheet.save(out); print(out, len(items), "panels", f"{t:.1f}s")

if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    panels(a[0] if a else "/home/claude/out/wow/storyboard_v1.png")
