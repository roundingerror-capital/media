"""Opening looks for the 1 s teaser (the boss 2026-11-13: "all videos starting to look the same... time to mix it up").
Same facts, a different costume each day. daily.cold_open_frame picks the look; "glow" (the original red/lime pulse) lives there.
Rules every look keeps:
- The big number is drawn by daily's tested number drawer (Inter Display Black, true minus, spaced): never rotated, never
  pixelated, never textured, and it holds still once it lands, so the publisher's OCR reads it the same on every frame.
- Words only around it (no extra figures): every number on screen must be on a Theo sheet.
- Text stays inside the safe box (daily.SAFE_*); NOT FINANCIAL ADVICE sits on top at the top-left.
- Original art only: no logos, no real newspaper or network names, no copyrighted characters."""
import math, random
from PIL import Image, ImageDraw, ImageFont
from make_reel import W, H, archivo, mono, fit

# Scene looks play one of Kit's looping pixel rooms (tools/scenes.py) at full colour behind a sign that fits the room, with a
# rotating cast (all five mascots, not only Penny: the boss 2026-11-13 "use more than Penny ... office backgrounds, relevant places").
# id: (scene, sign style, cast, tone it is kept for or None)
SCENE_LOOKS = {
    "floor":     ("SCN-01", "station",   ["theo", "penny"], None),
    "boardroom": ("SCN-15", "screen",    ["theo", "ada", "penny", "roz", "kit"], None),
    "subway":    ("SCN-09", "station",   ["kit", "penny"], None),
    "rooftop":   ("SCN-03", "neon",      ["ada", "theo"], None),
    "vault":     ("SCN-16", "plaque",    ["roz", "theo"], None),
    "bodega":    ("SCN-11", "neon",      ["kit", "ada"], None),
    "lobby":     ("SCN-08", "plaque",    ["roz", "penny"], None),
    "arcade":    ("SCN-06", "neon",      ["kit", "theo"], None),
    "rain":      ("SCN-10", "neon",      ["penny"], "loss"),
}
FLAT_CAST = {"receipt": ["ada"], "breaking": ["theo"], "headline": ["roz"], "chalk": ["ada", "kit"]}
# The order is the rotation: a place, then a flat graphic look, so neighbours never match.
LOOKS = ["glow", "receipt", "breaking", "chalk"]
# 2026-11-13 (the boss: "did you use OLD ASSETS?"): the room looks drew the October SCN loops, not Kit's current rooms, and the
# front-page look was rejected. All pulled from the rotation until the rooms are rebuilt on Kit's V3.01 stages (newwave.room_frame).
# Parked (still callable with spec["cold_open"]["look"], but out of the rotation): "rooftop" and "arcade" each gave a wrong
# number in the scanner test (2026-11-13: "-16.5%" read as "18.5%"; a stray "3%"). Every look in LOOKS scored 0 wrong numbers
# on 16 figures x 7 frames x both scanner passes.
def pick(day_ordinal, win):
    """The look for a date; a look kept for the other tone is skipped to the next one."""
    for k in range(len(LOOKS)):
        lk = LOOKS[(day_ordinal + k) % len(LOOKS)]; tone = SCENE_LOOKS.get(lk, (0, 0, 0, None))[3]
        if tone is None or (tone == "win") == win: return lk
    return "glow"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
def serif(sz): return ImageFont.truetype(SERIF, sz)
def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3

def _cast(img, sprite, names, u, y=1700, h=340):
    """The cast runs in from both sides and hops out of step. One or two stand big; a full room lines up smaller."""
    n = len(names); h = h if n <= 2 else 230; xs = [W // 2] if n == 1 else [int(W * (i + 0.5) / n) for i in range(n)]
    if n == 2: xs = [W // 2 - 190, W // 2 + 190]
    for i, (nm, x) in enumerate(zip(names, xs)):
        s = sprite(nm, False, u); s = s.resize((int(s.width * h / s.height), h), Image.NEAREST)
        if x > W // 2 and n > 1: s = s.transpose(Image.FLIP_LEFT_RIGHT) if nm != "kit" else s
        side = -1 if x < W // 2 else 1; run = int(side * 700 * (1 - ease((u - 0.05 - 0.04 * i) / 0.28))) if n > 1 else 0
        hop = int(60 * abs(math.sin((u + 0.11 * i) * math.pi * 4)))
        img.paste(s, (x - s.width // 2 + run, y - h - hop), s)
def _penny(img, sprite, u, y=1700, h=340, look=None): _cast(img, sprite, FLAT_CAST.get(look, ["penny"]), u, y, h)

def _wfit(d, txt, maxw, start, fontf):
    s = start
    while s > 20 and d.textlength(txt, font=fontf(s)) > maxw: s -= 4
    return fontf(s)

# ---------------------------------------------------------------- receipt: a till slip prints down from the top
def receipt(S, u, pts, num, sprite, win):
    co = S["cold_open"]; img = Image.new("RGB", (W, H), (20, 20, 22)); d = ImageDraw.Draw(img)
    ink = (28, 28, 30); col = (20, 130, 60) if win else (200, 30, 30)
    x0, x1 = 150, 930; c = (x0 + x1) // 2; o = int(-820 * (1 - ease((u - 0.05) / 0.3)))   # the slip prints down out of the slot
    bot = 1120 + o
    zig = [(x, bot + (16 if (x // 26) % 2 else 0)) for x in range(x0, x1 + 1, 26)]
    d.polygon([(x0, 330), (x1, 330)] + zig[::-1], fill=(244, 241, 232))
    def t(y, txt, f, fill=ink, anchor="ms", x=c):
        if y + o > 350: d.text((x, y + o), txt, font=f, fill=fill, anchor=anchor)
    t(430, "ROUNDING ERROR", mono(46, True)); t(480, "* TRADE SLIP *", mono(30, True))
    t(540, "-" * 30, mono(32), (150, 150, 150))
    if co.get("line"): t(630, co["line"], _wfit(d, co["line"], x1 - x0 - 80, 60, lambda s: mono(s, True)))
    t(720, "TOTAL", mono(36, True), anchor="ls", x=x0 + 40)
    if o > -4: num(d, c, 880, col, x1 - x0 - 90)                                        # lands once the slip has stopped
    t(950, "-" * 30, mono(32), (150, 150, 150)); t(1040, "THANK YOU. NOT ADVICE.", mono(30, True))
    d.rectangle([110, 300, 970, 334], fill=(60, 60, 64))                                 # printer slot, over the paper
    if u > 0.45:
        sh = co.get("shout", "WAIT, WHAT?!"); f = _wfit(d, sh, 700, 96, lambda s: archivo(s, 125, 900))
        tw = d.textlength(sh, font=f); d.rectangle([W // 2 - tw / 2 - 24, 1190, W // 2 + tw / 2 + 24, 1310], outline=col, width=8)
        d.text((W // 2, 1285), sh, font=f, fill=col, anchor="ms")
    _penny(img, sprite, u, y=1760, look="receipt")
    return img

# ---------------------------------------------------------------- breaking: TV news lower third
def breaking(S, u, pts, num, sprite, win):
    co = S["cold_open"]; img = Image.new("RGB", (W, H), (10, 18, 40)); d = ImageDraw.Draw(img)
    for i in range(14):                                                                # studio light beams
        a = (i / 14) * math.pi + u * 0.6; d.line([(W // 2, -200), (W // 2 + int(1600 * math.cos(a)), int(1600 * math.sin(a)))], fill=(18, 30, 64), width=40)
    col = (90, 230, 130) if win else (255, 60, 60)
    slide = int(-900 * (1 - ease((u - 0.08) / 0.18)))
    d.rectangle([60 + slide, 380, 420 + slide, 470], fill=(210, 20, 30)); d.text((240 + slide, 448), "BREAKING", font=archivo(58, 110, 900), fill="white", anchor="ms")
    if co.get("line"):
        f = _wfit(d, co["line"], W - 2 * 80, 64, lambda s: archivo(s, 110, 900))
        d.rectangle([60 - slide, 470, W - 60 - slide, 570], fill=(245, 245, 245)); d.text((W // 2 - slide, 546), co["line"], font=f, fill=(15, 15, 25), anchor="ms")
    num(d, W // 2, 860, col, W - 2 * 90)
    if u > 0.45:
        sh = co.get("shout", "WAIT, WHAT?!"); f = _wfit(d, sh, 760, 100, lambda s: archivo(s, 125, 900))
        d.text((W // 2 - 50, 1010), sh, font=f, fill="white", anchor="ms", stroke_width=6, stroke_fill="black")
    crawl = "ROUNDING ERROR  ///  NOT ADVICE  ///  " * 4; f = mono(34, True)     # words only on the crawl
    d.rectangle([0, 1290, 880, 1350], fill=(255, 205, 40)); d.text((60 - int(u * 900) % 700, 1334), crawl, font=f, fill=(15, 15, 25), anchor="ls")
    d.rectangle([880, 1290, W, 1350], fill=(10, 18, 40))
    _penny(img, sprite, u, y=1780, look="breaking")
    return img

# ---------------------------------------------------------------- headline: front page (invented masthead)
def headline(S, u, pts, num, sprite, win):
    co = S["cold_open"]; paper = (238, 232, 218); ink = (24, 22, 20)
    img = Image.new("RGB", (W, H), paper); d = ImageDraw.Draw(img); rng = random.Random(7)
    for _ in range(2500):                                                              # newsprint grain, kept off the number band
        x, y = rng.randrange(W), rng.randrange(H)
        if not 620 < y < 900: d.point((x, y), fill=(222, 214, 196))
    d.text((W // 2, 420), "THE DAILY ROUNDING", font=_wfit(d, "THE DAILY ROUNDING", W - 2 * 80, 92, serif), fill=ink, anchor="ms")
    d.line([(70, 450), (W - 70, 450)], fill=ink, width=6); d.line([(70, 462), (W - 70, 462)], fill=ink, width=2)
    if co.get("line"):
        f = _wfit(d, co["line"].upper(), W - 2 * 80, 84, serif); d.text((W // 2, 570), co["line"].upper(), font=f, fill=ink, anchor="ms")
    col = (18, 110, 50) if win else (175, 20, 20)
    if u > 0.12: num(d, W // 2, 860, col, W - 2 * 100)                                 # lands like a stamp
    d.line([(70, 910), (W - 70, 910)], fill=ink, width=2)
    if u > 0.45:
        sh = co.get("shout", "WAIT, WHAT?!"); f = _wfit(d, sh, 760, 76, serif); d.text((W // 2 - 50, 1000), sh, font=f, fill=ink, anchor="ms")
    for i in range(6):                                                                 # fake column text (bars, no letters)
        for k in range(2):
            x = 90 + k * 400; y = 1070 + i * 34; d.rectangle([x, y, x + 360 - rng.randrange(80), y + 12], fill=(200, 192, 176))
    _penny(img, sprite, u, y=1760, look="headline")
    return img

# ---------------------------------------------------------------- chalk: classroom board
def chalk(S, u, pts, num, sprite, win):
    co = S["cold_open"]; img = Image.new("RGB", (W, H), (34, 56, 46)); d = ImageDraw.Draw(img); rng = random.Random(3)
    d.rectangle([0, 0, W, H], outline=(120, 80, 40), width=34)
    for _ in range(1800):
        x, y = rng.randrange(W), rng.randrange(H)
        if not 640 < y < 900: d.point((x, y), fill=(52, 76, 64))                        # chalk dust, off the number band
    chalkc = (236, 236, 226); col = (190, 245, 140) if win else (255, 150, 140)
    if co.get("line"):
        f = _wfit(d, co["line"], W - 2 * 90, 80, lambda s: archivo(s, 100, 700)); d.text((W // 2, 520), co["line"], font=f, fill=chalkc, anchor="ms")
    num(d, W // 2, 820, col, W - 2 * 110)
    k = ease((u - 0.2) / 0.3)                                                          # the underline scribbles itself in
    if k > 0:
        xs = [150 + i * 20 for i in range(int(39 * k) + 1)]
        d.line([(x, 880 + 6 * math.sin(x / 37)) for x in xs], fill=chalkc, width=10)
    if u > 0.45:
        sh = co.get("shout", "WAIT, WHAT?!"); f = _wfit(d, sh, 760, 90, lambda s: archivo(s, 100, 800))
        d.text((W // 2 - 50, 1020), sh, font=f, fill=(250, 225, 120), anchor="ms")
    _penny(img, sprite, u, y=1760, look="chalk")
    return img

# ---------------------------------------------------------------- scene looks: a real room, a sign that belongs there
PANEL = (8, 8, 12)   # every sign face is near-black, so the number reads the same in any room
def _sign(img, d, style, box, u, col):
    x0, y0, x1, y1 = box
    if style == "board":                                   # LED board: chasing bulbs round the frame
        d.rectangle([x0 - 26, y0 - 26, x1 + 26, y1 + 26], fill=(30, 30, 36)); d.rectangle(box, fill=PANEL)
        k = int(u * 12)
        for i, x in enumerate(range(x0 - 13, x1 + 14, 44)):
            for y in (y0 - 13, y1 + 13): d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=col if (i + k) % 3 == 0 else (70, 60, 20))
    elif style == "screen":                                # wall screen: bezel and a stand
        d.rectangle([W // 2 - 40, y1, W // 2 + 40, y1 + 70], fill=(40, 42, 50)); d.rectangle([W // 2 - 150, y1 + 60, W // 2 + 150, y1 + 82], fill=(40, 42, 50))
        d.rounded_rectangle([x0 - 22, y0 - 22, x1 + 22, y1 + 22], 18, fill=(52, 56, 66)); d.rectangle(box, fill=PANEL)
        d.ellipse([x1 - 6, y1 + 4, x1 + 8, y1 + 18], fill=col)
    elif style == "station":                               # enamel platform sign on two hangers
        for x in (x0 + 90, x1 - 90): d.rectangle([x - 8, 0, x + 8, y0], fill=(30, 60, 40))
        d.rounded_rectangle([x0 - 16, y0 - 16, x1 + 16, y1 + 16], 26, fill=(240, 240, 235)); d.rounded_rectangle(box, 14, fill=PANEL)
    elif style == "billboard":                             # rooftop billboard: legs and two spot lamps
        for x in (x0 + 110, x1 - 110): d.rectangle([x - 12, y1, x + 12, 1700], fill=(36, 34, 40))
        d.rectangle([x0 - 20, y0 - 20, x1 + 20, y1 + 20], fill=(92, 66, 44)); d.rectangle(box, fill=PANEL)
        for x in (x0 + 60, W // 2, x1 - 60): d.polygon([(x - 16, y0 - 20), (x + 16, y0 - 20), (x + 8, y0 - 56), (x - 8, y0 - 56)], fill=(250, 235, 160))
    elif style == "plaque":                                # brass plate, four rivets
        d.rounded_rectangle([x0 - 24, y0 - 24, x1 + 24, y1 + 24], 16, fill=(176, 136, 56)); d.rounded_rectangle([x0 - 12, y0 - 12, x1 + 12, y1 + 12], 10, fill=(232, 196, 104)); d.rectangle(box, fill=PANEL)
        for x in (x0 - 18, x1 + 18):
            for y in (y0 - 18, y1 + 18): d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=(110, 80, 30))
    else:                                                  # neon: a tube that flickers on
        on = u > 0.2 or int(u * 20) % 2 == 0; c = col if on else (60, 40, 60)
        d.rectangle(box, fill=PANEL)
        for w, a in ((30, 0.25), (18, 0.5), (8, 1.0)): d.rounded_rectangle([x0 - 18, y0 - 18, x1 + 18, y1 + 18], 30, outline=tuple(int(v * a) for v in c), width=w)
def scene_look(look, S, u, pts, num, sprite, win):
    import scenes
    from PIL import ImageEnhance
    sid, style, cast, _ = SCENE_LOOKS[look]; co = S["cold_open"]
    # Scanner-tested 2026-11-13: the room at half brightness plus a full-width dark band behind the sign gave 0 wrong
    # numbers; a brighter room or a sign with the room showing beside it made the OCR read "-8.7%" as "3.7%".
    img = ImageEnhance.Brightness(scenes.frame(sid, u)).enhance(0.5); d = ImageDraw.Draw(img)
    col = (200, 240, 60) if win else (245, 60, 60)
    drop = int(-900 * (1 - ease((u - 0.06) / 0.12)))                     # the sign drops in fast and is still by 0.2 s (the scanner looks at 0.25 s)
    box = (84, 500 + drop, W - 84, 850 + drop)
    d.rectangle([0, box[1] - 60, W, box[3] + 60], fill=PANEL)
    for y in (box[1] - 60, box[3] + 54): d.rectangle([0, y, W, y + 6], fill=col)
    _sign(img, d, style, box, u, col)
    if u >= 0.3: num(d, W // 2, 790, col, W - 2 * 130)                    # the sign lands empty, then the number slams on and never moves
    if co.get("line"):
        f = _wfit(d, co["line"], W - 2 * 90, 84, lambda s: archivo(s, 125, 900)); tw = d.textlength(co["line"], font=f)
        d.rounded_rectangle([W // 2 - tw / 2 - 26, 356, W // 2 + tw / 2 + 26, 458], 12, fill=(8, 8, 12)); d.text((W // 2, 436), co["line"], font=f, fill=(242, 242, 238), anchor="ms")
    if look == "arcade":
        t = _pixel_text("LEVEL UP!" if win else "GAME OVER", 6, col)
        if u > 0.5 or int(u * 8) % 2 == 0: img.paste(t, (470 - t.width // 2, 1120), t)
    if u > 0.45:
        sh = co.get("shout", "WAIT, WHAT?!"); f = _wfit(d, sh, 780, int(108 * (1 + max(0, .25 - (u - .45)))), lambda s: archivo(s, 125, 900))
        d.text((470, 1010), sh, font=f, fill=(242, 242, 238), anchor="ms", stroke_width=8, stroke_fill=(0, 0, 0))
    _cast(img, sprite, cast, u)
    if u < 0.2:                                                          # white flash on the cut
        img = Image.blend(img, Image.new("RGB", (W, H), (255, 255, 255)), 0.7 * (1 - u / 0.2))
    return img
def _pixel_text(txt, scale, color):
    f = ImageFont.truetype(SANS_B, 20); w = int(f.getlength(txt)) + 4
    t = Image.new("RGBA", (w, 26), (0, 0, 0, 0)); ImageDraw.Draw(t).text((2, 22), txt, font=f, fill=color, anchor="ls")
    return t.resize((w * scale, 26 * scale), Image.NEAREST)

FUNCS = {"receipt": receipt, "breaking": breaking, "headline": headline, "chalk": chalk}
for _lk in SCENE_LOOKS: FUNCS[_lk] = (lambda lk: lambda S, u, pts, num, sprite, win: scene_look(lk, S, u, pts, num, sprite, win))(_lk)
