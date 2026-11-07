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
g = MV.Grid(161.5, 0.07); END = 25.0; SHEET = "20261106-161123-weekly"

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
    d = ImageDraw.Draw(img); f = mono(24, True); w = d.textlength("NOT FINANCIAL ADVICE", font=f)
    d.rectangle([60, 336, 60 + w + 24, 376], fill="#000000", outline="#3A3A3A", width=2); d.text((72, 356), "NOT FINANCIAL ADVICE", font=f, fill=INK, anchor="lm"); return img

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
    d = ImageDraw.Draw(img); x0, y0, x1 = 80, 470, W - 80; y1 = y0 + 120 + 110 * len(rows)
    d.rectangle([x0, y0, x1, y1], fill="#0B0B0B", outline="#3A3A3A", width=6)
    d.text((x0 + 36, y0 + 60), title, font=mono(30, True), fill=LIME, anchor="lm")
    for i, (txt, col) in enumerate(rows):
        if u < 0.35 * i: continue
        d.text((x0 + 36, y0 + 150 + 110 * i), txt, font=fit(txt, x1 - x0 - 72, 64, wdth=110, wght=800), fill=col, anchor="lm")
    if foot: d.text((W // 2, y1 + 60), foot, font=mono(30, True), fill=INK, anchor="mm")

# ---------------------------------------------------------------- shots
def s_ping(t, u):
    img = band(MV.room("ROOM-01", t, 0.45))
    rig(img, "penny", "point", t, 360, 1500, 9, False, g, hop=False); rig(img, "ada", "shrug", t, 760, 1500, 9, True, g, hop=False)
    mixed(img, [("THE ", INK), ("P&L", LIME), (" LOADS…", INK)], 170, 110)
    if u > 1.4: stamp(img, "ONE GREEN LINE?!", LIME, 270, 84)
    return nfa(img)

def s_book(t, u):
    img = band(MV.room("ROOM-16", t, 0.6))
    rig(img, "theo", "point", t, 820, 1640, 7, True, g, hop=False)
    panel(img, "THEO'S BOOK · FRI 11/6", [("UBER $66 puts: expired", INK), ("Premium kept: $230", LIME), ("Our first one to expire.", INK)],
          "Kept in full. Rules: hold to expiry.", u)
    mixed(img, [("FIRST ONE ", INK), ("KEPT IN FULL.", LIME)], 190, 96)
    return nfa(img)

def s_party(t, u):
    img = band(MV.lights(MV.room("ROOM-01", t, 0.5), t, g))
    rig(img, "kit", "dance", t, 170, 1560, 8, False, g); rig(img, "ada", "celebrate", t, 400, 1560, 8, False, g)
    rig(img, "boss", "celebrate", t, 650, 1560, 9, False, g); rig(img, "roz", "celebrate", t, 900, 1560, 8, True, g)
    rig(img, "penny", "celebrate", t, 290, 1820, 8, False, g); rig(img, "theo", "celebrate", t, 790, 1820, 8, True, g)
    confetti(img, t, 0)
    mixed(img, [("WE ARE ", INK), ("NOT", LIME), (" LEAVING", INK)], 150, 100)
    if u > 1.0: mixed(img, [("THIS ", INK), ("OFFICE!", LIME)], 270, 110)
    return nfa(img)

def s_toast(t, u):
    img = band(MV.lights(MV.room("ROOM-01", t, 0.5), t, g))
    rig(img, "boss", "celebrate", t, 540, 1620, 11, False, g)
    rig(img, "kit", "celebrate", t, 190, 1640, 8, False, g); rig(img, "penny", "celebrate", t, 890, 1640, 8, True, g)
    confetti(img, t, -3, 0.6)
    stamp(img, "TO THE", INK, 150, 90); mixed(img, [("FIRST ", LIME), ("DOLLAR!", INK)], 270, 120)
    return nfa(img)

WALL = (250, 720)      # left of Theo's framed chart on OFF-THEO-01's back wall
def s_hang(t, u):
    img = band(MV.room("OFF-THEO-01", t, 0.62))
    if u < 2.0:
        x = int(1000 - (u / 2.0) * 700); rig(img, "theo", "walk", t * 1.4, x, 1620, 9, True, g, hop=False)
        img = framed(img, x, 1480, 5)                      # held in front of him, below the face
    else:
        if u < 2.8:                                        # at the wall, still holding it; taps (sound) then it's up
            rig(img, "theo", "idle", t, 300, 1620, 9, True, g, hop=False); img = framed(img, 300, 1480, 5)
        else:
            img = framed(img, *WALL, 7, glow=min(1, (u - 2.8) * 2)); rig(img, "theo", "celebrate", t, 300, 1620, 9, True, g)
    stamp(img, "THEO DOES", INK, 150, 90); mixed(img, [("THE ", INK), ("HONORS.", LIME)], 270, 110)
    return nfa(img)

def s_honest(t, u):
    img = band(MV.room("OFF-THEO-01", t, 0.4)); img = framed(img, *WALL, 7, glow=0.5)
    rig(img, "theo", "nod", t, 640, 1620, 9, True, g, hop=False)
    mixed(img, [("THE FUND ", INK), ("OVERALL:", LIME)], 150, 96)
    if u > 0.6: stamp(img, "-5.68% since day one.", RED, 262, 76)
    if u > 1.6:
        d = ImageDraw.Draw(img); d.rectangle([90, 1700, W - 90, 1830], fill="#0B0B0B", outline="#3A3A3A", width=4)
        d.text((W // 2, 1765), "It's a start. Week of 11/6, Theo's sheet.", font=mono(34, True), fill=INK, anchor="mm")
    return nfa(img)

def s_end(t, u):
    img = Image.new("RGB", (W, H), "#05060A")
    mixed(img, [("ONE DOWN.", LIME)], 480, 120); mixed(img, [("FRAMED ", INK), ("FOREVER.", LIME)], 620, 92)
    if u > 1.2:
        n = K.piece("DEC-59", t); k = max(1, min(820 // n.width, 420 // n.height)); sg = up(n, k)
        if int(u * 6) % 7: img.paste(sg, (W // 2 - sg.width // 2, 1000), sg)
        stamp(img, "An AI-run fund, learning in public.", INK, 1000 + sg.height + 70, 40)
    else: img = framed(img, W // 2, 1100, 9, glow=0.6)
    return nfa(img)

SHOTS = [(0.0, s_ping), (3.2, s_book), (7.4, s_party), (12.2, s_toast), (14.6, s_hang), (19.0, s_honest), (21.6, s_end)]

def mix(out_mp3):
    import librosa, soundfile as sf
    y, sr = librosa.load(MV.song_path(SONG), sr=sfx.SR, mono=False, offset=START, duration=END + 0.5); y = y.T if y.ndim == 2 else y
    bus = sfx.Bus(END + 1)
    bus.add(sfx.ding(), 1.6, 0.2); bus.add(sfx.coin(), 4.2, 0.2); bus.add(sfx.coin(1), 4.6, 0.2)
    bus.add(sfx.impact(), 7.4, 0.35); bus.add(sfx.thump(), 7.45, 0.3); bus.add(sfx.arp_up(), 8.6, 0.15)
    for k in range(3): bus.add(sfx.bonk(), 14.6 + 2.1 + k * 0.22, 0.12)
    bus.add(sfx.sparkle(), 17.4, 0.3); bus.add(sfx.sparkle(), 22.8, 0.25)
    m = bus.mix_into(y[: int(END * sfx.SR)]); wav = out_mp3.replace(".mp3", ".wav"); sf.write(wav, m, sfx.SR)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", wav, "-b:a", "256k", out_mp3], check=True)

if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]; KW = dict(karaoke_on=False, end_fn=s_end)
    if "--panels" in sys.argv: MV.panels(a[0], SHOTS, [], g, END, **KW)
    elif "--cover" in sys.argv: MV.frame_at(18.2, SHOTS, [], g, **KW).save(a[0], quality=92)
    else:
        mix(MV.song_path("_dollar_mix")); MV.build(a[0] if a else "/home/claude/out/first_dollar_v1.mp4", "_dollar_mix", SHOTS, [], g, END, **KW)
