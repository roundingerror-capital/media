"""WoW Forever v3 (the boss 2026-11-04, game launches today): v2 with his fixes, five endings to pick from.
  - his office: navy pin-dot wallpaper instead of the mustard, Kit's art print, framed gallery and sconces on the wall;
  - ALL SYSTEMS CHECK: each desk gets a player card (the office-parody nameplate idea): name, day job, and their raid class + race;
  - the raid moves: the party takes turns lunging in and out to hit Evil Theo, he lunges back, sparks and heals on contact;
  - no "not financial advice" stamp (no stocks in this one), teaser says LAUNCHES TODAY;
  - the ending is the fund's origin story (automating the boss's options research so he could play more), not a gaming-channel launch.
    Endings A-E: ORIGIN (black cards), THEO NEVER SLEEPS, HONEY ASKS, ATTEMPT #2, THREE STAMPS.
    python3 make_v3.py <ending A-E> <out.mp4> | --panels <ending> <sheet.png>"""
import os, sys, math, runpy, subprocess, json
HERE = os.path.dirname(os.path.abspath(__file__))
_argv = sys.argv; sys.argv = sys.argv[:1]                  # v6 reads argv at import (workdir); keep ours away from it
V2 = runpy.run_path(os.path.join(HERE, "make_v2.py"), run_name="v2"); sys.argv = _argv
V6, V1 = V2["V6"], V2["V1"]
from PIL import Image, ImageDraw
import daily, stage, kitpieces as K
from make_reel import W, H, FPS, mono, fit
LIME, INK, RED, GOLD = "#C8F03C", "#F2F2EE", "#FF5C5C", "#F5C84B"
stamp, bubble, thought, black, must = V1["stamp"], V1["bubble"], V1["thought"], V1["black"], V1["must"]
load, place, standing, animate, merge, up = (V6[k] for k in ("load", "place", "standing", "animate", "merge", "up"))
A = V6["ASSETS"]; M = V2["M"]
comp = lambda n: stage.component(os.path.join(A, n + ".dc.html"))

def office(t, view="Back · Type", cast=(), dark=False):
    """v2's office, re-dressed: navy pin-dot wall, art on the wall instead of bare mustard."""
    st = load("OFF-BOSS-01"); extra = {}
    door = comp("DEC-25"); place(extra, "L6", door, 80, 88 - door.height)
    art = comp("DEC-56"); place(extra, "L6", art, 150 - art.width // 2, 34 - art.height // 2)            # sunset hills print, right of the desk
    gal = comp("DEC-31"); place(extra, "L6", gal, 126 - gal.width // 2, 20 - gal.height // 2)            # three frames, above his head
    for x in (104, 148):
        sc = comp("DEC-38"); place(extra, "L6", sc, x - sc.width // 2, 50 - sc.height)
    bd = V2["boss_desk"](view, t); place(extra, "L14", bd, 126 - bd.width // 2, 113 - bd.height)
    for ch, an, x, feet, flip in cast: sp_ = standing(ch, an, t, 0, flip); place(extra, "L16", sp_, int(x) - sp_.width // 2, feet - sp_.height)
    an_extra, moving = animate(st, t, ("MON",)); merge(extra, an_extra)
    im = st.render(skip=("CHR", "DSK", "MON01", "TEC07") + moving, extra=extra, wall=comp("WALL-05"))
    if dark: im = Image.alpha_composite(im, Image.new("RGBA", im.size, (6, 8, 26, 90)))
    return st, im
V2["office"].__globals__["office"] = office                 # pushin(), button() in v2 use the new office too
portrait = V2["portrait"]

ROSTER = {  # name, day job, class, race, role line
    "theo": ("THEO", "FINANCE · THE NUMBERS GUY", "MAGE", "GNOME", "DPS. DOES THE MATH."),
    "penny": ("PENNY", "MARKETING · THE HYPE", "PRIEST", "ELF", "HEALER. HEALS THE TIMELINE."),
    "roz": ("ROZ", "LEGAL · READS THE FINE PRINT", "WARRIOR", "DWARF", "TANK. BLOCKS EVERYTHING."),
    "ada": ("ADA", "DATA · THE HAPPY ONE", "HUNTER", "GOBLIN", "PET: THE PIPELINE."),
    "kit": ("KIT", "ART · THE GAME STUDIO", "PALADIN", "HUMAN", "DRAWS AGGRO. AND ROOMS."),
}
def player_card(img, who, u):
    """Slides up from the bottom: the parody nameplate, plus a raid line."""
    nm, job, cls, race, role = ROSTER[who]; d = ImageDraw.Draw(img)
    k = min(1, u / 0.18); y0 = int(1280 + (1 - k) * 640)
    d.rectangle([70, y0 + 14, W - 56, y0 + 470], fill="#000000")
    d.rectangle([56, y0, W - 70, y0 + 456], fill="#0E0E14", outline=LIME, width=6)
    d.text((96, y0 + 96), nm, font=fit(nm, 600, 110, wdth=125, wght=900), fill=INK, anchor="ls")
    d.text((96, y0 + 152), job, font=mono(34, True), fill="#9A9A94", anchor="ls")
    d.line([96, y0 + 186, W - 110, y0 + 186], fill="#2A2A33", width=4)
    d.text((96, y0 + 250), "CLASS", font=mono(26, True), fill="#9A9A94", anchor="ls")
    d.text((96, y0 + 318), cls, font=fit(cls, 420, 66, wdth=120, wght=900), fill=LIME, anchor="ls")
    d.text((560, y0 + 250), "RACE", font=mono(26, True), fill="#9A9A94", anchor="ls")
    d.text((560, y0 + 318), race, font=fit(race, 400, 66, wdth=120, wght=900), fill=GOLD, anchor="ls")
    d.text((96, y0 + 410), role, font=mono(34, True), fill=INK, anchor="ls")
    return img

def auto(a, who):
    def f(t, u):
        img = V6["kit_room"](dict(a, name=None), t, u, 0) if a["st"] == "OFF-KIT-01" else V6["desk_shot"](a, t, u, 1.0, 0)
        img = player_card(img, who, u)
        if u > 0.55: stamp(img, "AUTOMATED.", LIME, 240, 110)
        return img
    return f

# ---- the raid: turns, lunges, contact ----
def bump(ph):            # 0..1 -> 0..1..0 with a quick strike and slow return
    return math.sin(min(1, ph / 0.35) * math.pi / 2) if ph < 0.35 else max(0, 1 - (ph - 0.35) / 0.45)
PARTY = V2["PARTY"]
def raid(t, u, wipe=False, dur=4.5, win=False):
    c = V2["arena"](t); turn = 0.9
    ev = "Slam" if (wipe or (not win and (u * dur) % 3.0 > 2.4)) else "Idle"
    boss = K.piece(M + "V2_07EvilTheo.dc.html", t, ev)
    lunge_b = 0 if (wipe or win) else int(14 * bump(((u * dur) % 3.0 - 2.4) / 0.6)) if (u * dur) % 3.0 > 2.4 else 0
    shake = (int(math.sin(t * 60) * 2), int(math.cos(t * 50) * 1)) if (wipe and u < 0.5) or lunge_b > 10 else (0, 0)
    bx = 135 - boss.width + 34 - lunge_b + shake[0]
    if win and u > 0.3:
        boss = boss.rotate(-90, expand=True); pf = K.piece("LIBROOMS6", t, "Faint puff"); c.alpha_composite(pf, (100 - pf.width // 2, 196 - pf.height))
    c.paste(boss, (bx, 206 - boss.height + shake[1]), boss)
    hits = []
    for i, (ch, board, label, x) in enumerate(PARTY):
        sp = K.piece(board, t + i * 0.2, label)
        ph = ((u * dur) - i * turn / 3) % turn / turn
        dx = 0 if (wipe or win) else int((26 if ch == "kit" else 12) * bump(ph))
        if (u * dur) % 3.0 > 2.4 and not (wipe or win): dx -= int(6 * bump(((u * dur) % 3.0 - 2.4) / 0.6))   # knocked back by his lunge
        if wipe and u > 0.35:
            sp = sp.rotate(90, expand=True); pf = K.piece("LIBROOMS6", t, "Faint puff"); c.alpha_composite(pf, (x - pf.width // 2, 196 - pf.height))
        if win: dx = int(3 * abs(math.sin(t * 9 + i)))                                                   # victory bounce
        c.paste(sp, (x - sp.width // 2 + dx + shake[0], 206 - sp.height - (dx if win else 0) + shake[1]), sp)
        if not (wipe or win) and 0.3 < ph < 0.5: hits.append(ch)
    if not (wipe or win):
        for i in range(2):
            ph = (u * dur * 0.9 + i / 2) % 1; b = K.piece("LIBROOMS6", t, "Lime bolt"); c.alpha_composite(b, (int(30 + ph * 70), int(150 - ph * 30)))
        if "penny" in hits or (u * dur) % 3.0 > 2.6:
            hg = K.piece("LIBROOMS6", t, "Heal glow"); c.alpha_composite(hg, (40, 160))
        if hits: sp_ = K.piece("LIBROOMS6", t, "Hit spark"); c.alpha_composite(sp_, (bx + 4, 120 + (len(hits) * 7) % 20))
    img = up(c, 8).convert("RGBA")
    if wipe: img = V1["coins"](img, max(0, u * dur - 0.15), [(x * 8, 1500) for _, _, _, x in PARTY], t)
    d = ImageDraw.Draw(img)
    hp = 0.0 if win else (max(0.12, 0.7 - u * 0.3) if not wipe else 0.45)
    d.rectangle([60, 110, W - 60, 170], fill="#000000", outline=INK, width=4); d.rectangle([66, 116, 66 + int((W - 132) * hp), 164], fill=RED)
    d.text((80, 100), "EVIL THEO · RAID BOSS", font=mono(30, True), fill=INK, anchor="ls")
    for i, (nm, v) in enumerate((("THE BOSS · WARLOCK", 0.8), ("KIT · PALADIN", 0.6), ("PENNY · PRIEST", 0.9))):
        y = 300 + i * 86; v = 0 if (wipe and u > 0.3) else (v if win else v - u * 0.2 + (0.15 if "penny" in hits else 0))
        d.rectangle([40, y, 420, y + 60], fill="#000000", outline=INK, width=3); d.rectangle([44, y + 30, 44 + int(372 * max(0, min(1, v))), y + 56], fill=LIME)
        d.text((52, y + 24), nm, font=mono(22, True), fill=INK, anchor="ls")
    if hits and not (wipe or win):
        word = {"kit": "BONK!", "boss": "ZAP!", "penny": "+HEAL"}[hits[0]]
        d.text((830, 760), word, font=fit(word, 360, 90, wdth=125, wght=900), fill=LIME if hits[0] == "penny" else GOLD, anchor="mm", stroke_width=8, stroke_fill="#000000")
    if wipe:
        if u > 0.3: img = Image.alpha_composite(img, Image.new("RGBA", img.size, (60, 60, 60, int(min(120, (u - 0.3) * 400)))))
        if u > 0.45: stamp(img, "PARTY WIPED.", RED, 960, 130)
    elif win:
        if u > 0.35: stamp(img, "RAID CLEARED.", LIME, 960, 130)
    else:
        d.rectangle([240, 1730, 840, 1780], fill="#000000", outline=INK, width=3); d.rectangle([244, 1734, 244 + int(592 * min(1, u * 1.2)), 1776], fill="#7BAAF7")
        d.text((540, 1755), "CASTING: AUTOMATE", font=mono(26, True), fill=INK, anchor="mm")
    return img.convert("RGB")

def cards(lines):
    """Black end cards, lines arrive one by one (txt, colour, y, size, at seconds)."""
    def f(t, u):
        img = black()
        for txt, col, y, size, at in lines:
            if u >= at: stamp(img, txt, col, y, size)
        return img
    return f

def over(base, lines, dim=110):
    def f(t, u):
        img = base(t, u).convert("RGBA"); img = Image.alpha_composite(img, Image.new("RGBA", img.size, (0, 0, 0, dim))).convert("RGB")
        for txt, col, y, size, at in lines:
            if u >= at: stamp(img, txt, col, y, size)
        return img
    return f

asleep = lambda t, u: portrait(*office(t, "Front · Asleep"))
theo_desk = lambda t, u: V6["desk_shot"](dict(st="OFF-THEO-01", ch="theo", an="desk_type", mon="MON-01"), t, u, 1.0, 0)
FOLLOW = ("FOLLOW FOR THE RESEARCH.", LIME, 1500, 96)

ENDINGS = {
 "A": ("ORIGIN", [
    (2.0, "THE TRUTH", cards([("THE TRUTH?", INK, 900, 130, 0)])),
    (2.6, "A JOKE", cards([("THIS FUND STARTED", INK, 760, 92, 0), ("AS A JOKE:", INK, 880, 92, 0),
                           ("automate my options research", LIME, 1040, 62, 0.25), ("so I could play more WoW.", LIME, 1130, 62, 0.25)])),
    (2.6, "YEARS", cards([("YEARS OF TRADING.", INK, 760, 92, 0), ("HUNDREDS OF HOURS", INK, 880, 92, 0.15), ("OF RESEARCH.", INK, 990, 92, 0.15),
                          ("all of it, taught to a bot.", LIME, 1150, 62, 0.4)])),
    (3.0, "SHARE", cards([("NOW THE BOT", INK, 700, 110, 0), ("DOES THE RESEARCH.", INK, 830, 100, 0), ("AND WE SHARE IT HERE.", LIME, 990, 92, 0.25),
                          FOLLOW + (0.55,), ("(we'll be in the raid)", "#9A9A94", 1620, 48, 0.7)])),
 ]),
 "B": ("THEO NEVER SLEEPS", [
    (2.2, "WHILE HE SLEEPS", over(asleep, [("WHILE HE SLEEPS...", INK, 420, 96, 0)], 60)),
    (2.6, "THEO WORKS", over(theo_desk, [("THEO RUNS THE RESEARCH.", LIME, 420, 84, 0)], 40)),
    (2.8, "BUILT IN", over(theo_desk, [("YEARS OF OPTIONS TRADING,", INK, 380, 72, 0), ("BUILT INTO A BOT.", INK, 480, 92, 0.1),
                                       ("so the boss can raid.", LIME, 600, 62, 0.45)], 90)),
    (2.8, "YOU GET IT", cards([("THE BOT DOES", INK, 700, 110, 0), ("THE HOMEWORK.", INK, 820, 110, 0), ("YOU GET THE NOTES.", LIME, 940, 96, 0.2), FOLLOW + (0.5,)])),
 ]),
 "C": ("HONEY ASKS", [
    (2.4, "SO THE FUND...", lambda t, u: bubble(portrait(*office(t, "Front · Asleep", cast=[("realboss", "talk", 88, 108, False)])),
                                                "SO THE FUND IS SO YOU CAN PLAY WOW?", W // 2, 330, 50)),
    (2.0, "ALSO RESEARCH", lambda t, u: bubble(portrait(*office(t, "Front · Type", cast=[("realboss", "idle", 88, 108, False)])),
                                               "...IT'S ALSO RESEARCH.", W // 2, 330)),
    (2.8, "HANDED TO A BOT", cards([("YEARS OF OPTIONS RESEARCH,", INK, 780, 80, 0), ("HANDED TO A BOT.", INK, 900, 100, 0.1),
                                    ("It trades. We raid.", LIME, 1060, 70, 0.4), ("You get the notes.", LIME, 1160, 70, 0.55)])),
    (2.4, "FOLLOW", cards([FOLLOW[:4] + (0,), ("(he really did fall asleep)", "#9A9A94", 1620, 46, 0.4)])),
 ]),
 "D": ("ATTEMPT #2", [
    (1.2, "ATTEMPT 2", cards([("ATTEMPT #2.", LIME, 900, 140, 0)])),
    (2.6, "THE RAID AGAIN", lambda t, u: raid(t, u / 4.5)),
    (2.0, "RAID CLEARED", lambda t, u: raid(t, u / 2.0, win=True, dur=2.0)),
    (3.2, "THE DEAL", cards([("THE BOT DOES", INK, 640, 100, 0), ("THE RESEARCH.", INK, 760, 100, 0), ("WE DO THE RAID.", INK, 880, 100, 0.2),
                             ("YOU GET THE RESEARCH.", LIME, 1020, 92, 0.45), ("years of trading, taught to a bot", "#9A9A94", 1640, 46, 0.6)])),
    (2.0, "FOLLOW", cards([FOLLOW[:4] + (0,)])),
 ]),
 "E": ("THREE STAMPS", [
    (1.6, "S1", cards([("WE AUTOMATED", INK, 820, 120, 0), ("THE RESEARCH.", INK, 960, 120, 0)])),
    (1.4, "S2", cards([("NOW WE RAID.", LIME, 900, 150, 0)])),
    (1.8, "S3", cards([("YOU GET", INK, 820, 130, 0), ("THE RESEARCH.", LIME, 960, 130, 0)])),
    (2.6, "WHY", cards([("years of options trading, taught to a bot", "#9A9A94", 820, 46, 0), FOLLOW[:4] + (0.2,)])),
 ]),
}

def shots(ending):
    head = [
        (1.0, "TEASER", lambda t, u: stamp(stamp(black(), "WOW FOREVER", INK, 760, 110), "LAUNCHES TODAY.", LIME, 900, 90)),
        (2.5, "FROM BEHIND · SHE WALKS IN", lambda t, u: portrait(*office(t, "Back · Type", dark=True, cast=[("realboss", "walk", 70 + u * 8, 108, False)]))),
        (2.5, "SHE'S WORRIED", lambda t, u: thought(portrait(*office(t, "3/4-back · Type", dark=True, cast=[("realboss", "idle", 88, 108, False)])),
                                                   ["He's been working", "nonstop. I'm worried."], 380, 520)),
        (2.5, "PUSH-IN", lambda t, u: V2["pushin"](t, u, [15, 20, 24, 30, 40][min(4, int(u / 0.5))])),
        (2.0, "MUST AUTOMATE", lambda t, u: must(V2["pushin"](t, u + 2.5, 40), u)),
        (1.5, "THE BUTTON", lambda t, u: V2["button"](t, u)),
        (1.2, "ALL SYSTEMS CHECK", lambda t, u: stamp(portrait(*office(t, "Front · Type")), "ALL SYSTEMS CHECK.", INK, 420, 100)),
        (1.5, "THEO", auto(dict(st="OFF-THEO-01", ch="theo", an="desk_type", mon="MON-01"), "theo")),
        (1.5, "PENNY", auto(dict(st="OFF-PENNY-01", ch="penny", an="desk34_type", mon="MON-05"), "penny")),
        (1.5, "ROZ", auto(dict(st="OFF-ROZ-01", ch="roz", an="desk34_type", mon="MON-02"), "roz")),
        (1.5, "ADA", auto(dict(st="OFF-ADA-01", ch="ada", an="desk_type", mon="MON-01"), "ada")),
        (1.5, "KIT", auto(dict(st="OFF-KIT-01"), "kit")),
        (1.3, "EVERYTHING IS READY", lambda t, u: stamp(portrait(*office(t, "Front · Type")), "EVERYTHING IS READY.", LIME, 420, 96)),
        (1.2, "SLOW BLINK", lambda t, u: stage.camera(office(t, "Front · Slow blink")[1], 126 - 22, 70 - 40, 45, 80, 24).convert("RGB")),
        (0.5, "BLACK", lambda t, u: black()),
        (4.5, "THE RAID", lambda t, u: raid(t, u / 4.5)),
        (2.0, "PARTY WIPED", lambda t, u: raid(t, u / 2.0, wipe=True, dur=2.0)),
        (0.9, "HONEY...", lambda t, u: stamp(black(), "honey...", INK, 960, 90)),
        (2.2, "ASLEEP ON THE DESK", lambda t, u: bubble(portrait(*office(t, "Front · Asleep", cast=[("realboss", "talk", 88, 108, False)])), "HONEY. WAKE UP. BEDTIME.", W // 2, 330)),
    ]
    return head + ENDINGS[ending][1]

def frame_at(S, tv):
    t = 0
    for dur, lab, fn in S:
        if tv < t + dur or lab == S[-1][1]:
            img = fn(tv, tv - t)                                 # u in seconds, as in v2
            if img.size != (W, H): img = img.resize((W, H), Image.NEAREST)
            if 1.0 <= tv < 4.5: img = daily.cta_pill(img, tv - 1.0)
            return img.convert("RGB")                       # no NFA stamp: no stocks in this video (the boss 11/4)
        t += dur

def song(total, out):
    """Same song, same head; the tail starts earlier on the bar grid so the music runs the whole video."""
    c = json.load(open("/home/claude/out/wow/music/clock_cut.json")); src = "/home/claude/media/tools/music/the_clock_pays_rent.mp3"
    full = 62.380333; need_tail = total - c["head_end"] + 0.3; n = math.floor((full - need_tail - c["pickup"]) / c["bar"]); ts = c["pickup"] + n * c["bar"]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-filter_complex",
        f"[0]atrim=0:{c['head_end']:.3f},asetpts=PTS-STARTPTS[a];[0]atrim={ts:.3f},asetpts=PTS-STARTPTS[b];[a][b]acrossfade=d=0.04[m];"
        f"[m]apad,atrim=0:{total:.3f},afade=t=out:st={total - 1.2:.3f}:d=1.2", "-ar", "44100", out], check=True)

def build(ending, out):
    S = shots(ending); total = sum(d for d, _, _ in S); wav = out[:-4] + "_mix.wav"; song(total, wav)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "20",
        "-c:a", "aac", "-b:a", "160k", "-af", "loudnorm=I=-14:TP=-1.5", "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for i in range(int(round(total * FPS))): p.stdin.write(frame_at(S, i / FPS).tobytes())
    p.stdin.close(); p.wait(); print(out, f"{total:.1f}s")

def panels(ending, out, only=None):
    S = shots(ending); t = 0; items = []
    for dur, lab, fn in S:
        if only is None or lab in only: items.append((t + dur * 0.7, lab))
        t += dur
    pw, ph = 270, 480; cols = 7; rows = (len(items) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (pw + 16) + 16, rows * (ph + 50) + 90), (12, 12, 16)); d = ImageDraw.Draw(sheet)
    d.text((16, 52), f"WOW FOREVER v3 · ending {ending} {ENDINGS[ending][0]} · {t:.1f}s", font=mono(26, True), fill=LIME, anchor="ls")
    for n, (tv, lab) in enumerate(items):
        x = 16 + (n % cols) * (pw + 16); y = 80 + (n // cols) * (ph + 50)
        sheet.paste(frame_at(S, tv).resize((pw, ph), Image.LANCZOS), (x, y)); d.text((x, y + ph + 30), f"{n + 1} · {lab}"[:26], font=mono(18, True), fill=INK, anchor="ls")
    sheet.save(out); print(out)

if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if "--panels" in sys.argv: panels(a[0], a[1], a[2].split(",") if len(a) > 2 else None)
    else: build(a[0], a[1])
