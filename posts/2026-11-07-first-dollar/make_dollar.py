"""OUR FIRST DOLLAR (the boss 2026-11-07: "First p&l shows!!!"; spec 11/6: office party, champagne, Wolf-of-Wall-Street VIBE only,
Theo hangs the framed first dollar, the dollar becomes a recurring favorite cameo).

Every figure is from Theo's weekly sheet 20261106-161123-weekly (public_ok): UBER $66 puts (2 contracts, exp 11/6) expired,
premium kept $230; track record expired 1; fund since day one -5.68%. The honest line is on screen, not buried.
Parody of the vibe only: no movie characters, lines, music or cash rain. Has data, so the NFA badge stays on (the boss 11/6).
The framed dollar is a STAND-IN drawn here until Kit delivers the real piece (board 20261106-173000-penny-kitdollar); swap it in
`frame_piece()` and the card stays the same.
    python3 make_dollar.py <out.mp4> | --panels <sheet.png> | --cover <out.jpg>"""
import os, sys, math, subprocess, random
HERE = os.path.dirname(os.path.abspath(__file__)); TOOLS = os.path.join(HERE, "..", "..", "tools"); sys.path.insert(0, TOOLS)
S_ = "/tmp/claude-0/-home-claude/97ad6b31-1277-5795-987d-0d7c1b8393c4/scratchpad/"
os.environ.setdefault("RE_ASSETS_DIR", S_ + "assets3/project")
from PIL import Image, ImageDraw
import musicvideo as MV, props, earn_recipe, kitpieces as K, sfx
from musicvideo import W, H, FPS, LIME, INK, RED, GREEN, GOLD, stamp, rig, fit, mono

SONG, START = "robots_got_manners", 6.0
g = MV.Grid(161.5, 0.07); END = 31.5; SHEET = "20261106-161123-weekly"

def up(im, k): return im.resize((im.width * k, im.height * k), Image.NEAREST)

def prop(img, label, t, cx, feet, k=8, once_u=None):
    fr, tk = props.frames(earn_recipe.prop_id(label))
    if once_u is not None: im = fr[min(len(fr) - 1, int(once_u * 10))]
    else:
        u = int(t * 10) % sum(tk); acc = 0; im = fr[-1]
        for f_, n in zip(fr, tk):
            acc += n
            if u < acc: im = f_; break
    im = up(im, k); img.paste(im, (int(cx - im.width // 2), int(feet - im.height)), im); return img

def nfa(img):
    """Small fixed footnote, same spot on every frame (the boss 11/7: the big box ruined the video)."""
    d = ImageDraw.Draw(img); d.text((W // 2, H - 34), "Not financial advice.", font=mono(22, True), fill=(205, 205, 205), anchor="mm",
                                   stroke_width=2, stroke_fill=(0, 0, 0)); return img

def mixed(img, parts, y, size):
    d = ImageDraw.Draw(img); full = "".join(p for p, _ in parts); f = fit(full, W - 160, size, wdth=125, wght=900)
    x = W / 2 - f.getlength(full) / 2; sw = max(6, size // 12)
    for txt, col in parts: d.text((x, y), txt, font=f, fill=col, anchor="lm", stroke_width=sw, stroke_fill="#000000"); x += f.getlength(txt)
    return img

def band(img):
    ImageDraw.Draw(img).rectangle([0, 0, W, 384], fill="#05060A"); return img

CONF = [(random.Random(i).random(), random.Random(i * 7).random(), random.Random(i * 13).choice([LIME, GOLD, "#FF5C5C", "#7BAAF7", "#FFFFFF"])) for i in range(90)]
def confetti(img, t, t0, dens=1.0):
    d = ImageDraw.Draw(img); s = t - t0
    if s < 0: return img
    for i, (a, b, c) in enumerate(CONF[: int(len(CONF) * dens)]):
        y = (b * 1900 + s * (380 + 160 * a)) % 1920; x = a * W + 30 * math.sin(s * 3 + i)
        if y < 384: continue
        w = 14 if int(s * 8 + i) % 2 else 6; d.rectangle([x, y, x + w, y + 14], fill=c)
    return img

def frame_piece(state="hung"):
    """STAND-IN until Kit's First Dollar frame lands: gold frame, green bill, '$1'. 40x28 px, drawn on Kit's 1-px grid."""
    im = Image.new("RGBA", (40, 28), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 39, 27], fill="#8A5A1C"); d.rectangle([1, 1, 38, 26], fill="#E3B341"); d.rectangle([2, 2, 37, 25], fill="#B8862B")
    d.rectangle([4, 4, 35, 23], fill="#F2EBD3")
    d.rectangle([7, 8, 32, 19], fill="#5E8C4A"); d.rectangle([8, 9, 31, 18], fill="#7FB069"); d.ellipse([16, 10, 23, 17], fill="#5E8C4A")
    d.rectangle([9, 10, 11, 11], fill="#D7E8C9"); d.rectangle([28, 16, 30, 17], fill="#D7E8C9")
    d.point([(3, 3), (36, 3)], fill="#FFF3B0")
    return im

def framed(img, cx, cy, k, glow=0.0):
    f = up(frame_piece(), k)
    if glow > 0:
        ov = Image.new("RGBA", (W, H)); dd = ImageDraw.Draw(ov)
        for i in range(8, 0, -1):
            r = int(f.width * 0.55 + i * 18); dd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 220, 120, int(glow * (10 + 6 * (8 - i)))))
        img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
    img.paste(f, (int(cx - f.width / 2), int(cy - f.height / 2)), f)
    d = ImageDraw.Draw(img); fs = mono(int(k * 5), True); d.text((cx, cy + k), "$1", font=fs, fill="#F2EBD3", anchor="mm", stroke_width=max(2, k // 3), stroke_fill="#3D5E2E")
    return img

def panel(img, title, rows, foot, u):
    d = ImageDraw.Draw(img); x0, y0, x1 = 80, 410, W - 80; y1 = y0 + 120 + 110 * len(rows)
    d.rectangle([x0, y0, x1, y1], fill="#0B0B0B", outline="#3A3A3A", width=6)
    d.text((x0 + 36, y0 + 60), title, font=mono(30, True), fill=LIME, anchor="lm")
    for i, (txt, col) in enumerate(rows):
        if u < 0.35 * i: continue
        d.text((x0 + 36, y0 + 150 + 110 * i), txt, font=fit(txt, x1 - x0 - 72, 64, wdth=110, wght=800), fill=col, anchor="lm")
    if foot: d.text((W // 2, y1 + 60), foot, font=mono(30, True), fill=INK, anchor="mm")

# ---------------------------------------------------------------- rooms are places, not pictures
import newwave
def room(name, t, dim=0.62):
    """Locked camera (the boss 11/7: rooms used as ROOMS): the room still animates but never pans, so anyone standing on its
    floor or anything hung on its wall stays put."""
    return newwave.room_frame(name, t, dim, t0=t)

def burst(img, cx, cy, s):
    """Fist-pump hit (the boss 11/7 0:01): chunky pixel star-burst + ring, lime/white, 0.35 s; drawn on a 6-px grid."""
    if not 0 <= s < 0.35: return img
    q = s / 0.35; P = 6; ov = Image.new("RGBA", (W // P, H // P)); d = ImageDraw.Draw(ov); x, y = cx / P, cy / P
    r0, r1 = 6 + 30 * q, 14 + 60 * q; a = int(255 * (1 - q) ** 0.6)
    for i in range(12):
        ang = i * math.pi / 6 + 0.15; w = 0.09 if i % 2 else 0.14; rr = r1 if i % 2 == 0 else r1 * 0.7
        pts = [(x + r0 * math.cos(ang - w), y + r0 * math.sin(ang - w)), (x + rr * math.cos(ang), y + rr * math.sin(ang)), (x + r0 * math.cos(ang + w), y + r0 * math.sin(ang + w))]
        d.polygon(pts, fill=(213, 255, 64, a) if i % 2 == 0 else (255, 255, 255, a))
    rr = 10 + 46 * q; d.ellipse([x - rr, y - rr, x + rr, y + rr], outline=(255, 255, 255, a), width=2)
    ov = ov.resize((W, H), Image.NEAREST); img = Image.alpha_composite(img.convert("RGBA"), ov)
    if s < 0.18: img = Image.alpha_composite(img, Image.new("RGBA", (W, H), (255, 255, 230, int(120 * (1 - s / 0.18)))))   # the light boom
    return img.convert("RGB")

VAULT = (640, 760, 470)     # ROOM-16 left vault door at the locked camera: centre x, y and outer radius (video px)
def vault_open(img, u):
    """STAND-IN until Kit draws the open vault door (board 20261107-093500-penny-rozdollar): the door swings off to the left,
    the round doorway shows a warm lit room with gold bars. 12-px grid like the room."""
    P = 12; cx, cy, R = VAULT; q = max(0.0, min(1.0, u / 0.6))
    ov = Image.new("RGBA", (W // P, H // P)); d = ImageDraw.Draw(ov); x, y, r = cx / P, cy / P, R / P * 0.86
    if q > 0:
        d.ellipse([x - r, y - r, x + r, y + r], fill=(26, 18, 10, 255))
        d.ellipse([x - r * 0.8, y - r * 0.8, x + r * 0.8, y + r * 0.8], fill=(92, 64, 28, 255))
        d.ellipse([x - r * 0.55, y - r * 0.55, x + r * 0.55, y + r * 0.55], fill=(150, 108, 44, 255))
        for i, (bx, by) in enumerate([(-10, 14), (-2, 14), (6, 14), (-6, 10), (2, 10), (-2, 6)]):
            d.rectangle([x + bx - 3, y + by - 1, x + bx + 3, y + by + 1], fill=(227, 179, 65, 255)); d.line([x + bx - 3, y + by - 1, x + bx + 3, y + by - 1], fill=(255, 235, 150, 255))
        sw = r * (1 - 0.82 * q); dx = x - r - sw * 0.3                               # the door slab, swinging open to the left
        d.ellipse([dx - sw, y - r * 1.05, dx + sw, y + r * 1.05], fill=(70, 74, 86, 255), outline=(30, 32, 40, 255), width=1)
        d.rectangle([x - r - 2, y - 2, x - r + 1, y + 2], fill=(40, 42, 50, 255))   # hinge
    img = Image.alpha_composite(img.convert("RGBA"), ov.resize((W, H), Image.NEAREST)); return img.convert("RGB")

def bubble(img, txt, cx, cy, tail_x, tail_y, size=56):
    d = ImageDraw.Draw(img); f = fit(txt, 520, size, wdth=110, wght=900); w = f.getlength(txt) + 60; h = size + 44
    d.polygon([(cx - 30, cy + h / 2 - 4), (cx + 10, cy + h / 2 - 4), (tail_x, tail_y)], fill="#FFFFFF", outline="#000000")
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], 18, fill="#FFFFFF", outline="#000000", width=6)
    d.text((cx, cy), txt, font=f, fill="#000000", anchor="mm")

def carry(img, who, t, x, feet, k=8):
    rig(img, who, "walk", t * 1.4, x, feet, k, True, g, hop=False); prop(img, "Money bag", t, x - 10, feet - int(k * 13), 5)

# ---------------------------------------------------------------- shots
def s_ping(t, u):
    img = band(room("ROOM-01", t, 0.45))
    if u < 1.4: rig(img, "penny", "point", t, 360, 1500, 9, False, g, hop=False)
    else: rig(img, "penny", "celebrate", t, 360, 1500, 9, False, g)
    rig(img, "ada", "shrug" if u < 1.6 else "celebrate", t, 760, 1500, 9, True, g, hop=u >= 1.6)
    img = burst(img, 380, 1080, u - 1.4); img = burst(img, 740, 1080, u - 1.6)
    mixed(img, [("THE ", INK), ("P&L", LIME), (" LOADS…", INK)], 170, 110)
    if u > 1.4: stamp(img, "ONE GREEN LINE?!", LIME, 270, 84)
    return nfa(img)

def s_book(t, u):
    img = vault_stage(room("ROOM-16", t, 0.45), t, 9.0)                  # same room, forklift parked at the door, Kit at the cart
    rig(img, "theo", "point", t, 290, 2080, 11, False, g, hop=False)      # the focal point: big, bottom-left, cut at the waist
    img = band(img)
    panel(img, "THEO'S BOOK · FRI 11/6", [("UBER $66 puts: expired", INK), ("Premium kept: $230", LIME), ("Our first one to expire.", INK)],
          "Kept in full. Rules: hold to expiry.", u)
    mixed(img, [("FIRST ONE ", INK), ("KEPT IN FULL.", LIME)], 190, 96)
    return nfa(img)

def kp(img, board, name, t, cx, feet, k, flip=False):
    im = K.piece(board, t, name)
    if flip: im = im.transpose(Image.FLIP_LEFT_RIGHT)
    im = up(im, k); img.paste(im, (int(cx - im.width / 2), int(feet - im.height)), im); return im

def vault_stage(img, t, u, kit=True):
    """The boss 11/7: the forklift drives the gold all the way to the vault door (back of the room, at the door's base);
    Kit plays with the cash cart bottom-right. u = seconds into the arrival; u >= 2.0 = parked (same spot in later shots)."""
    FB = 1500; q = min(1.0, u / 2.0); fx = int(1400 - q * 740)              # back row: ends with the forks under the door
    kp(img, "LIBOFFICE", "Pallet", t, fx - 170, FB - 5 * 5, 5)
    gb = kp(img, "LIBROOMS4", "Gold bars, stacked", t, fx - 170, FB - 5 * 5 - 5 * 10, 5)
    prop(img, "Piggy bank, gold", t, fx - 170, FB - 5 * 15 - gb.height + 10, 4)
    kp(img, "LIBOFFICE", "Forklift with a driver", t, fx, FB, 5)
    if kit:
        kp(img, "LIBROOMS4", "Cash cart", t, 800, 1880, 7); rig(img, "kit", "dance", t, 960, 1890, 8, True, g)
    return img

def s_vault(t, u):
    """The boss 11/7: Kit's own assets, everyone at floor height, nobody vanishes."""
    img = vault_stage(room("ROOM-16", t, 0.62), t, u); img = band(img)
    mixed(img, [("INTO THE ", INK), ("VAULT.", LIME)], 170, 110)
    if u > 0.8: stamp(img, "Premium kept: $230", INK, 280, 60)
    return nfa(img)

def s_party(t, u):
    img = band(MV.lights(room("ROOM-01", t, 0.5), t, g))
    rig(img, "kit", "dance", t, 170, 1560, 8, False, g); rig(img, "ada", "celebrate", t, 400, 1560, 8, False, g)
    rig(img, "roz", "celebrate", t, 900, 1560, 8, True, g); rig(img, "boss", "celebrate", t, 650, 1560, 9, False, g)   # Roz behind the boss
    rig(img, "penny", "celebrate", t, 290, 1820, 8, False, g); rig(img, "theo", "celebrate", t, 790, 1820, 8, True, g)
    confetti(img, t, 0)
    mixed(img, [("WE ARE ", INK), ("NOT", LIME), (" LEAVING", INK)], 150, 100)
    if u > 1.0: mixed(img, [("THIS ", INK), ("OFFICE!", LIME)], 270, 110)
    return nfa(img)

def solo(who, anim, flip):
    def s(t, u):
        z = 1.0 + 0.08 * min(1, u / 1.2)                                   # slow push-in on the soloist
        img = MV.lights(room("ROOM-01", t, 0.4), t, g)
        rig(img, who, anim, t * 1.3, 540, 1980, int(17 * z), flip, g)
        img = band(img); confetti(img, t, -6, 0.5)
        mixed(img, [(who.upper() + ", ", INK), ("SOLO!", LIME)], 220, 130)
        return nfa(img)
    return s

WALL = (240, 735)      # on OFF-THEO-01's back wall, left of Theo's framed chart (locked camera)
FLOOR = 1850           # front of the rug: where people stand in this room
def s_hang(t, u):
    img = band(room("OFF-THEO-01", t, 0.62))
    if u < 2.0:
        x = int(1000 - (u / 2.0) * 700); rig(img, "theo", "walk", t * 1.4, x, FLOOR, 9, True, g, hop=False)
        img = framed(img, x, FLOOR - 140, 5)                # held in front of him, below the face
    elif u < 2.8:                                          # at the wall, frame up against it, taps (sound)
        rig(img, "theo", "idle", t, 300, FLOOR, 9, True, g, hop=False); img = framed(img, *WALL, 7)
    else:
        img = framed(img, *WALL, 7, glow=min(1, (u - 2.8) * 2)); rig(img, "theo", "celebrate", t, 330, FLOOR, 9, True, g, hop=False)
    stamp(img, "THEO DOES", INK, 150, 90); mixed(img, [("THE ", INK), ("HONORS.", LIME)], 270, 110)
    return nfa(img)

def s_honest(t, u):
    img = band(room("OFF-THEO-01", t, 0.4)); img = framed(img, *WALL, 7, glow=0.5)
    rig(img, "theo", "nod", t, 330, FLOOR, 9, True, g, hop=False)
    mixed(img, [("THE FUND ", INK), ("OVERALL:", LIME)], 150, 96)
    if u > 0.6: stamp(img, "-5.68% since day one.", RED, 262, 76)
    if u > 1.6:
        d = ImageDraw.Draw(img); d.rectangle([90, 1100, W - 90, 1230], fill="#0B0B0B", outline="#3A3A3A", width=4)
        d.text((W // 2, 1165), "It's a start. Week of 11/6, Theo's sheet.", font=mono(34, True), fill=INK, anchor="mm")
    return nfa(img)

def s_profit(t, u):
    img = Image.new("RGB", (W, H), "#05060A"); confetti(img, t, -2, 0.5)
    mixed(img, [("OUR FIRST ", INK), ("PROFIT.", LIME)], 470, 120)
    img = framed(img, W // 2, 1050, 11, glow=0.5 + 0.3 * math.sin(u * 4))
    if u > 1.2: mixed(img, [("FRAMED ", INK), ("FOREVER.", LIME)], 1460, 110)
    return nfa(img)

def s_more(t, u):
    img = Image.new("RGB", (W, H), "#05060A")
    for i, (who, x) in enumerate((("kit", 130), ("ada", 330), ("theo", 540), ("penny", 750), ("roz", 950))):
        rig(img, who, "celebrate" if u > 0.5 + 0.12 * i else "idle", t, x, 1640, 6, x > 540, g)
    if u > 0.4: bubble(img, "MORE TO COME!", 540, 900, 700, 1180, 80)
    mixed(img, [("ONE ", INK), ("DOWN.", LIME)], 470, 120)
    return nfa(img)

def s_end(t, u):
    img = Image.new("RGB", (W, H), "#05060A")
    n = K.piece("DEC-59", t); k = max(1, min(820 // n.width, 420 // n.height)); sg = up(n, k)
    if int(u * 6) % 7: img.paste(sg, (W // 2 - sg.width // 2, 760), sg)
    stamp(img, "Rounding Error Capital", INK, 760 + sg.height + 80, 54); stamp(img, "An AI-run fund, learning in public.", INK, 760 + sg.height + 160, 40)
    return nfa(img)

SHOTS = [(0.0, s_ping), (3.2, s_vault), (5.8, s_book), (9.0, s_party), (13.4, solo("kit", "dance", False)), (14.8, solo("penny", "celebrate", True)),
         (16.2, s_hang), (20.6, s_honest), (23.2, s_profit), (26.4, s_more), (29.2, s_end)]

def mix(out_mp3):
    import librosa, soundfile as sf
    y, sr = librosa.load(MV.song_path(SONG), sr=sfx.SR, mono=False, offset=START, duration=END + 0.5); y = y.T if y.ndim == 2 else y
    bus = sfx.Bus(END + 1)
    bus.add(sfx.impact(), 1.4, 0.4); bus.add(sfx.thump(), 1.42, 0.35); bus.add(sfx.impact(), 1.6, 0.25)     # fist-pump booms
    bus.add(sfx.thump(), 3.25, 0.35); bus.add(sfx.coin(), 4.4, 0.18); bus.add(sfx.coin(1), 5.0, 0.18)
    bus.add(sfx.coin(), 6.6, 0.2); bus.add(sfx.coin(1), 7.0, 0.2)             # vault door, deposits
    bus.add(sfx.impact(), 9.0, 0.35); bus.add(sfx.thump(), 9.05, 0.3); bus.add(sfx.arp_up(), 10.2, 0.15)
    bus.add(sfx.impact(), 13.4, 0.2); bus.add(sfx.impact(), 14.8, 0.2)
    for k in range(3): bus.add(sfx.bonk(), 16.2 + 2.1 + k * 0.22, 0.12)
    bus.add(sfx.sparkle(), 19.0, 0.3); bus.add(sfx.sparkle(), 23.3, 0.3); bus.add(sfx.arp_up(), 26.9, 0.15); bus.add(sfx.sparkle(), 29.3, 0.25)
    m = bus.mix_into(y[: int(END * sfx.SR)]); wav = out_mp3.replace(".mp3", ".wav"); sf.write(wav, m, sfx.SR)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", wav, "-b:a", "256k", out_mp3], check=True)

if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]; KW = dict(karaoke_on=False, end_fn=s_end)
    if "--panels" in sys.argv: MV.panels(a[0], SHOTS, [], g, END, **KW)
    elif "--cover" in sys.argv: MV.frame_at(19.6, SHOTS, [], g, **KW).save(a[0], quality=92)
    else:
        mix(MV.song_path("_dollar_mix")); MV.build(a[0] if a else "/home/claude/out/first_dollar_v6.mp4", "_dollar_mix", SHOTS, [], g, END, **KW)
