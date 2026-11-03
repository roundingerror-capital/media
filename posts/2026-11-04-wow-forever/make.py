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
    skip, extra, wall = dressed(st, "OFF-BOSS-01", ("CHR",) + tuple(skip_more), extra)
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

import swaps, scenes
CODE = ["def automate(everything):", "    for job in firm.jobs:", "        job.run(forever=True)", "SELECT * FROM posts WHERE done = 0;",
        "git push origin main --force-with-love", "render(video, fps=30)", "while not ready: automate()", "theo.fact_sheet(today)",
        "penny.build(3, every_day=True)", "roz.audit(every_frame=True)", "ada.ship(ticket)", "kit.draw(more_rooms)"]

def office(t, u, cast=(), dark=False, boss_an="idle", boss_x=124, skip_more=()):
    """The boss at his desk at night (mustard wall). cast: [(ch, anim, x, feet, flip)] standing in the room."""
    st = stage.load(os.path.join(ASSETS, "OFF-BOSS-01.dc.html")); extra = {}
    door = comp("DEC-25"); place(extra, "L6", door, 80, 88 - door.height)          # the door she walks in through
    sp = rigs.frame("boss", boss_an, t); place(extra, "L13", sp, boss_x - sp.width // 2, 104 - sp.height)
    for ch, an, x, feet, flip in cast:
        f = rigs.frame(ch, an, t, flip=flip); place(extra, "L16", f, int(x) - f.width // 2, feet - f.height)
    skip, extra, wall = dressed(st, "OFF-BOSS-01", ("CHR",) + tuple(skip_more), extra)
    im = st.render(skip=skip, extra=extra, wall=wall)
    if dark: im = Image.alpha_composite(im, Image.new("RGBA", im.size, (6, 8, 26, 120)))
    return st, im

def portrait(st, im): x0, y0, w, h = st.frames["portrait"]; return stage.camera(im, x0, y0, w, h, 15).convert("RGB")

def thought(img, lines, cx, y):
    d = ImageDraw.Draw(img); f = fit(max(lines, key=len), 700, 50, wdth=105, wght=800); lh = 64
    w = max(int(f.getlength(l)) for l in lines) + 80; h = lh * len(lines) + 50
    d.rounded_rectangle([cx - w // 2, y, cx + w // 2, y + h], radius=60, fill=INK, outline="#000000", width=6)
    for r, (dx, dy) in ((26, (60, h + 30)), (16, (100, h + 80))): d.ellipse([cx + dx - r, y + dy - r, cx + dx + r, y + dy + r], fill=INK, outline="#000000", width=5)
    for i, l in enumerate(lines): d.text((cx, y + 40 + i * lh + lh // 2), l, font=f, fill="#0B0B0B", anchor="mm")
    return img

def hangover(t, u, k=30):
    """The push-in on his face (The Hangover style): a tighter window on the same stage, screen light on his face, code flying at him."""
    st, im = office(t, u, dark=False, boss_an="idle", skip_more=("MON01", "TEC07"))   # the screen is behind the camera now
    w, h = 1080 // k, 1920 // k; cx, cy = 124, 50
    img = stage.camera(im, cx - w // 2, cy - h // 2, w, h, k).convert("RGBA")
    glow = (90, 200, 255, 70) if int(u * 6) % 2 else (200, 240, 60, 70)                    # monitor light flickering on his face
    img = Image.alpha_composite(img, Image.new("RGBA", img.size, glow)).convert("RGB")
    d = ImageDraw.Draw(img); f = mono(38, True)
    for i in range(6):
        z = (u * 0.9 + i / 6) % 1; line = CODE[(i + int(u * 3)) % len(CODE)]
        x = int(W / 2 + (i % 2 * 2 - 1) * (120 + z * 380)); y = int(300 + i * 230 + (z - 0.5) * 160)
        ff = mono(int(24 + z * 34), True); d.text((x, y), line, font=ff, fill=LIME if i % 3 else INK, anchor="mm", stroke_width=3, stroke_fill="#000000")
    return img

def must(img, u):
    n = 1 + int(u * 2.4); f = fit("MUST AUTOMATE.", W - 160, 110, wdth=125, wght=900); d = ImageDraw.Draw(img)
    for i in range(min(3, n)): d.text((W // 2, 1300 + i * 140), "MUST AUTOMATE.", font=f, fill=INK, anchor="mm", stroke_width=10, stroke_fill="#000000")
    return img

def button(t, u):
    st, im = office(t, u, dark=True, boss_an="point"); img = portrait(st, im); d = ImageDraw.Draw(img)
    press = u > 0.6; y = 1240 + (16 if press else 0)
    d.rectangle([180, y + (0 if press else 24), 900, y + 220 + 24], fill="#000000")
    d.rectangle([180, y, 900, y + 220], fill=LIME if not press else "#9DBF2A", outline="#000000", width=8)
    d.text((540, y + 110), "AUTOMATE", font=fit("AUTOMATE", 620, 130, wdth=125, wght=900), fill="#0B0B0B", anchor="mm")
    if press: d.text((780, y - 40), "boop.", font=mono(64, True), fill=INK, anchor="mm", stroke_width=6, stroke_fill="#000000")
    return img

def raid(t, u, wipe=False):
    """The dream: the boss and his party vs a giant raid boss (Evil Theo, Kit's Ash colourway), generic MMO HUD (ours, not the game's)."""
    c = P["scn"]("SCN-14", t); img = P["up"](c, 8).convert("RGBA")
    big = swaps.recolor(rigs.frame("theo", "shakehead" if wipe else "talk", t), "theo", "Ash"); big = big.crop(big.getbbox())
    big = big.resize((big.width * 18, big.height * 18), Image.NEAREST); img.alpha_composite(big, (W - big.width + 260, 1700 - big.height)) if False else img.paste(big, (W - big.width + 260, 1700 - big.height), big)
    party = [("boss", 120), ("kit", 330), ("penny", 520)]
    for i, (ch, x) in enumerate(party):
        an = "facepalm" if wipe else ("celebrate" if int(u * 3 + i) % 2 else "point")
        sp = rigs.frame(ch, an, t + i * 0.2); sp = sp.crop(sp.getbbox()); sp = sp.resize((sp.width * 8, sp.height * 8), Image.NEAREST)
        if wipe: sp = sp.rotate(90, expand=True)
        img.paste(sp, (x - sp.width // 2, 1760 - sp.height), sp)
    d = ImageDraw.Draw(img)
    hp = 0.62 - u * 0.1 if not wipe else 0.55                                                # raid-boss health bar
    d.rectangle([60, 110, W - 60, 170], fill="#000000", outline=INK, width=4); d.rectangle([66, 116, 66 + int((W - 132) * hp), 164], fill=RED)
    d.text((80, 100), "EVIL THEO · RAID BOSS", font=mono(30, True), fill=INK, anchor="ls")
    for i, (nm, v) in enumerate((("THE BOSS", 0.8), ("KIT", 0.6), ("PENNY", 0.9))):    # party frames
        y = 230 + i * 86; v = 0 if wipe else v
        d.rectangle([40, y, 380, y + 60], fill="#000000", outline=INK, width=3); d.rectangle([44, y + 30, 44 + int(332 * v), y + 56], fill=LIME)
        d.text((52, y + 24), nm, font=mono(22, True), fill=INK, anchor="ls")
    d.rectangle([240, 1800, 840, 1890], fill="#000000", outline=INK, width=3)                # action bar
    for i in range(6): d.rectangle([254 + i * 98, 1812, 334 + i * 98, 1878], outline=LIME if i == 0 else "#6E6E69", width=4)
    if wipe:
        img = Image.alpha_composite(img.convert("RGBA"), Image.new("RGBA", img.size, (60, 60, 60, 120))).convert("RGB")
        stamp(img, "PARTY WIPED.", RED, 960, 130)
    else:
        d.rectangle([240, 1720, 840, 1770], fill="#000000", outline=INK, width=3); d.rectangle([244, 1724, 244 + int(592 * min(1, u / 1.6)), 1766], fill="#7BAAF7")
        d.text((540, 1745), "CASTING: AUTOMATE", font=mono(26, True), fill=INK, anchor="mm")
    return img.convert("RGB")

def wake(t, u):
    st, im = office(t, u, cast=[("realboss", "talk", 96, 124, False)], boss_an="idle"); img = portrait(st, im)
    return P["bubble"](img, "HONEY. WAKE UP. BEDTIME.", W // 2, 330) if "bubble" in P else bubble(img, "HONEY. WAKE UP. BEDTIME.", W // 2, 330)

# (seconds, label, draw(t, u) -> 1080x1920 RGB)
SHOTS = [
    (1.0, "TEASER", lambda t, u: stamp(stamp(black(), "WOW FOREVER", INK, 760, 110), "LAUNCHES TOMORROW.", LIME, 900, 90)),
    (2.5, "THE WIFE WALKS IN", lambda t, u: portrait(*office(t, u, dark=True, cast=[("realboss", "walk", 70 + u * 12, 124, False)]))),
    (2.5, "SHE'S WORRIED", lambda t, u: thought(portrait(*office(t, u, dark=True, cast=[("realboss", "idle", 96, 124, False)])),
                                               ["He's been working", "nonstop. I'm worried."], 380, 760)),
    (2.5, "HANGOVER ZOOM", lambda t, u: hangover(t, u)),
    (2.0, "MUST AUTOMATE", lambda t, u: must(hangover(t, u + 2.5, 40), u)),
    (1.5, "THE BUTTON", lambda t, u: button(t, u)),
    (1.2, "ALL SYSTEMS CHECK", lambda t, u: stamp(portrait(*office(t, u, boss_an="talk")), "ALL SYSTEMS CHECK.", INK, 420, 100)),
    (0.8, "THEO", lambda t, u: stamp(desk_shot(t, u, "OFF-THEO-01", "theo", "desk_type"), "AUTOMATED.", LIME, 1500, 100)),
    (0.8, "PENNY", lambda t, u: stamp(desk_shot(t, u, "OFF-PENNY-01", "penny", "desk34_type"), "AUTOMATED.", LIME, 1500, 100)),
    (0.8, "ROZ", lambda t, u: stamp(desk_shot(t, u, "OFF-ROZ-01", "roz", "desk34_type"), "AUTOMATED.", LIME, 1500, 100)),
    (0.8, "ADA", lambda t, u: stamp(desk_shot(t, u, "OFF-ADA-01", "ada", "desk_type"), "AUTOMATED.", LIME, 1500, 100)),
    (0.8, "KIT", lambda t, u: stamp(desk_shot(t, u, "OFF-KIT-01", "kit", "desk34_type"), "AUTOMATED.", LIME, 1500, 100)),
    (1.5, "EVERYTHING IS READY", lambda t, u: stamp(portrait(*office(t, u, boss_an="celebrate")), "EVERYTHING IS READY.", LIME, 420, 96)),
    (0.6, "BLINK", lambda t, u: black()),
    (3.5, "THE RAID", lambda t, u: raid(t, u)),
    (1.5, "PARTY WIPED", lambda t, u: raid(t, u, wipe=True)),
    (1.0, "HONEY...", lambda t, u: stamp(black(), "honey...", INK, 960, 90)),
    (2.5, "WAKE UP", lambda t, u: wake(t, u)),
    (3.0, "ALMOST READY", lambda t, u: stamp(stamp(stamp(black(), "WE'RE ALMOST READY", INK, 700, 90), "FOR WOW FOREVER.", LIME, 830, 90),
                                             "(the real reason this fund exists)", "#9A9A94", 980, 46)),
    (1.5, "STAY TUNED", lambda t, u: stamp(stamp(black(), "STAY TUNED.", INK, 880, 120), "#WoWForever", LIME, 1020, 80)),
]

def panels(out):
    items = []; t = 0
    for dur, lab, fn in SHOTS: items.append((t, dur, lab, fn)); t += dur
    pw, ph = 270, 480; cols = 7; rows = (len(items) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (pw + 16) + 16, rows * (ph + 70) + 90), (12, 12, 16)); d = ImageDraw.Draw(sheet)
    d.text((16, 52), f"WOW FOREVER · STORYBOARD DRAFT 2 (your notes) · {t:.1f}s · Kit's assets only", font=mono(26, True), fill=LIME, anchor="ls")
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
