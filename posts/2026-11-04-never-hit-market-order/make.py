"""NEVER HIT MARKET ORDER: the band's first single (the boss 2026-11-04: "a music video with everyone on the phone dancing to that
song ... extra super catchy ... put the lyrics so people know what it's saying ... painfully obvious that it's about the stock market
... we're all in a band"). Song: Robots Got Manners (tools/music/robots_got_manners.mp3, lyric set "No Market Orders").

  - cut on the beat (161.5 BPM, beat grid from librosa), everyone bounces on the beat; Kit's rigs (V2.03/V2.06: celebrate, point,
    holdsign, nod, shakehead, Kit's dance/play) and his V3.01 rooms; the phones verse is everyone at their desk on the phone
    (desk34_phone rigs, the office-parody desk shots with band nameplates);
  - karaoke lyrics, the current word lit; lines timed to the 8-beat phrases (no timed lyric file exists: phrase-level timing from the
    beat grid and the song's energy, see LINES);
  - stock-market UI, no figures anywhere: ticker tape of order words, up/down candles on UP DOWN, a MARKET ORDER button slapped away,
    a bid/ask ladder with "MY PRICE", a limit order getting FILLED. No numbers -> no fact sheet, no NFA stamp.
  - Missing art (instruments, a band stage, standing phone loops) is asked of Kit on the Ops board; v1 uses what exists.
    python3 make.py <out.mp4> | --panels <sheet.png>"""
import os, sys, math, runpy, subprocess, random
HERE = os.path.dirname(os.path.abspath(__file__)); TOOLS = os.path.join(HERE, "..", "..", "tools"); sys.path.insert(0, TOOLS)
os.environ.setdefault("PARODY_CUT", "/home/claude/out/officeparody/music/breakroom_cut.json")
os.environ.setdefault("RE_ASSETS_DIR", "/tmp/claude-0/-home-claude/97ad6b31-1277-5795-987d-0d7c1b8393c4/scratchpad/assets3/project")
V6 = runpy.run_path(os.path.join(HERE, "..", "2026-11-04-office-intro-parody", "make_v6.py"), run_name="v6")
from PIL import Image, ImageDraw
import rigs, newwave
from make_reel import W, H, FPS, mono, fit
LIME, INK, RED, GREEN, BLUE = "#C8F03C", "#F2F2EE", "#FF5C5C", "#3BD16F", "#7BAAF7"
SONG = os.path.join(TOOLS, "music", "robots_got_manners.mp3")
BEAT, B0 = 60 / 161.5, 0.09                      # librosa beat grid (2026-11-04): 161.5 BPM, first beat 0.09 s
def tb(b): return B0 + b * BEAT                   # beat index -> seconds
def beat_of(t): return (t - B0) / BEAT
END = 62.0

# ---------- lyrics (set "No Market Orders"; each line = 8 beats) ----------
L1, L2, L3, L4 = "Limit order, limit order", "Never smash the market button, that's the border", "Name my price or I don't play", "Robots got manners, okay? OKAY!"
LINES = [(16, "Up down, up down"), (24, "Up down, up down"),
         (32, L1), (40, L2), (48, L3), (56, L4),
         (64, L1), (72, L2), (80, L3), (88, L4),
         (128, L1), (136, L2), (144, L3), (152, L4)]

def karaoke(img, t):
    b = beat_of(t); cur = [x for x in LINES if x[0] <= b < x[0] + 8]
    if not cur: return img
    b0, line = cur[0]; words = line.split(" "); n = len(words); u = b - b0
    lit = sum(1 for i in range(n) if u >= i * 7.0 / n)
    f = fit("Never smash the market", W - 150, 96, wdth=110, wght=900)
    # wrap into up to two rows
    rows, row = [], []
    for w_ in words:
        if f.getlength(" ".join(row + [w_])) > W - 140 and row: rows.append(row); row = []
        row.append(w_)
    rows.append(row)
    d = ImageDraw.Draw(img); lh = int(f.size * 1.15); y0 = 1560 - (len(rows) - 1) * lh // 2
    pad = 22; bw = max(f.getlength(" ".join(r)) for r in rows)
    d.rectangle([W // 2 - bw / 2 - pad, y0 - lh // 2 - pad + 6, W // 2 + bw / 2 + pad, y0 + (len(rows) - 1) * lh + lh // 2 + pad - 6], fill="#000000")
    k = 0
    for ri, r in enumerate(rows):
        x = W // 2 - f.getlength(" ".join(r)) / 2; y = y0 + ri * lh
        for w_ in r:
            col = LIME if k < lit else "#6E6E68"
            if k == lit - 1 and (u - (lit - 1) * 7.0 / n) < 0.5: col = INK          # the word just sung flashes white
            d.text((x, y), w_, font=f, fill=col, anchor="lm"); x += f.getlength(w_ + " "); k += 1
    return img

# ---------- stock-market UI (no figures) ----------
TAPE = "  LIMIT: YES  MARKET: NO  BID  ASK  SPREAD  FILLED: YES  LIMIT: YES  MARKET: NO  NAME YOUR PRICE  BID  ASK  "
def tape(img, t):
    d = ImageDraw.Draw(img); f = mono(34, True); y = 236
    d.rectangle([0, y - 30, W, y + 30], fill="#05060A"); d.line([(0, y - 30), (W, y - 30)], fill=LIME, width=3); d.line([(0, y + 30), (W, y + 30)], fill=LIME, width=3)
    x = -int(t * 160) % int(f.getlength(TAPE)); x -= int(f.getlength(TAPE))
    while x < W:
        cx = x
        for tok in TAPE.split("  "):
            if not tok: cx += f.getlength("  "); continue
            col = RED if "NO" in tok.split() or tok == "ASK" else (GREEN if "YES" in tok or tok == "BID" or "PRICE" in tok else INK)
            d.text((cx, y), tok, font=f, fill=col, anchor="lm"); cx += f.getlength(tok + "  ")
        x += int(f.getlength(TAPE))
    return img

def candles(img, t, b0):
    """UP DOWN: candles at 1/12 res, one new candle per beat, green on UP, red on DOWN."""
    c = Image.new("RGBA", (90, 60)); d = ImageDraw.Draw(c); nb = int(beat_of(t) - b0) + 1; lvl = 30
    for i in range(min(nb, 16)):
        up_ = (i // 2) % 2 == 0 if False else i % 2 == 0; h = 7 + (i * 3) % 5; x = 4 + i * 5
        o = lvl; cl = lvl - h if up_ else lvl + h; lvl = cl
        top, bot = min(o, cl), max(o, cl); col = (59, 209, 111, 255) if up_ else (255, 92, 92, 255)
        d.line([(x + 1, top - 3), (x + 1, bot + 3)], fill=col); d.rectangle([x, top, x + 2, bot], fill=col)
    big = c.resize((c.width * 12, c.height * 12), Image.NEAREST); img.paste(big, (0, 420), big); return img

def market_button(img, t, b_slap):
    b = beat_of(t); d = ImageDraw.Draw(img); f = fit("MARKET ORDER", 600, 110, wdth=125, wght=900)
    if b < b_slap:
        y = 700 + (10 if int(b) % 2 else 0)
        d.rectangle([200, y + 26, 880, y + 246], fill="#000000"); d.rectangle([200, y, 880, y + 220], fill=RED, outline="#000000", width=8)
        d.text((540, y + 110), "MARKET ORDER", font=f, fill="#0B0B0B", anchor="mm")
        if b > b_slap - 2: d.text((760, y - 50), "don't...", font=mono(54, True), fill=INK, anchor="mm", stroke_width=6, stroke_fill="#000000")
    else:
        u = (b - b_slap) * BEAT; lay = Image.new("RGBA", (700, 260)); dd = ImageDraw.Draw(lay)
        dd.rectangle([10, 10, 690, 230], fill=RED, outline="#000000", width=8); dd.text((350, 120), "MARKET ORDER", font=f, fill="#0B0B0B", anchor="mm")
        lay = lay.rotate(-u * 500, expand=True); x = int(190 + u * 1600); y = int(700 - u * 900 + u * u * 1500)
        img.paste(lay, (x, y), lay)
        stamp(img, "SLAPPED.", LIME, 760, 120)
    return img

def ladder(img, t, b0, fill_at=None):
    """Bid/ask ladder, no prices: red ask rows on top, green bid rows below, depth bars breathing on the beat, MY PRICE marker."""
    d = ImageDraw.Draw(img); b = beat_of(t); x0, x1, y0, rh = 140, 940, 420, 64; f = mono(34, True)
    d.rectangle([x0 - 20, y0 - 70, x1 + 20, y0 + 10 * rh + 20], fill="#05060A", outline=INK, width=4)
    d.text((x0, y0 - 36), "ASK", font=f, fill=RED, anchor="lm"); d.text((x1, y0 - 36), "ORDER BOOK", font=f, fill=INK, anchor="rm")
    for i in range(10):
        y = y0 + i * rh; ask = i < 5; base = (5 - i if ask else i - 4) * 0.13 + 0.2
        w = base + 0.12 * abs(math.sin(math.pi * (b + i * 0.37)))
        col = RED if ask else GREEN
        d.rectangle([x0, y + 8, x0 + int((x1 - x0) * min(1, w)), y + rh - 8], fill=col)
        d.text((x1 - 10, y + rh // 2), "ASK" if ask else "BID", font=mono(26, True), fill="#0B0B0B" if w > 0.95 else "#8A8A84", anchor="rm")
    my = y0 + 6 * rh + rh // 2 if fill_at is None or b < fill_at else y0 + 5 * rh + rh // 2
    d.rectangle([x0 - 34, my - 26, x0 + 300, my + 26], fill=LIME, outline="#000000", width=4)
    d.text((x0 - 20, my), "< MY PRICE", font=mono(36, True), fill="#0B0B0B", anchor="lm")
    if fill_at is not None and b >= fill_at: stamp(img, "FILLED!", LIME, y0 + 10 * rh + 110, 130)
    return img

def stamp(img, txt, col=LIME, y=820, size=120):
    d = ImageDraw.Draw(img); f = fit(txt, W - 160, size, wdth=125, wght=900)
    d.text((W // 2, y), txt, font=f, fill=col, anchor="mm", stroke_width=10, stroke_fill="#000000"); return img

# ---------- cast ----------
def rig(img, ch, an, t, cx, feet, k=6, flip=False, hop=True):
    sp = rigs.frame(ch, an, t, k=k, flip=flip, loop=True)
    b = beat_of(t); h = int(k * 3 * max(0, math.sin(math.pi * (b % 1)))) if hop else 0
    bw = rigs.body(ch, "idle", k)[0]
    d = ImageDraw.Draw(img); d.ellipse([cx - bw * 0.33, feet - 8, cx + bw * 0.33, feet + 14], fill="#121212")
    img.paste(sp, (int(cx - sp.width // 2), int(feet - sp.height - h)), sp)

def lights(img, t, n=4, cols=((200, 240, 60), (123, 170, 247), (255, 92, 92), (255, 255, 255))):
    """Stage spotlights at 1/8 res (pixel cones), swinging on the beat."""
    c = Image.new("RGBA", (W // 8, H // 8)); d = ImageDraw.Draw(c); b = beat_of(t)
    for i in range(n):
        x = (i + 0.5) * c.width / n; sw = math.sin(math.pi * (b / 2 + i * 0.5)) * 30; col = cols[(i + int(b / 4)) % len(cols)]
        d.polygon([(x - 2, 0), (x + 2, 0), (x + sw + 22, c.height * 0.78), (x + sw - 22, c.height * 0.78)], fill=col + (46,))
    img.paste(Image.new("RGB", img.size), (0, 0), Image.new("L", img.size, 0))
    up_ = c.resize(img.size, Image.NEAREST); base = img.convert("RGBA"); base.alpha_composite(up_); return base.convert("RGB")

def confetti(img, t, t0):
    d = ImageDraw.Draw(img); rnd = random.Random(7); u = t - t0
    for i in range(70):
        x = rnd.randrange(0, W); v = rnd.uniform(260, 520); y = int((rnd.uniform(-1400, 0) + u * v) % (H + 200)) - 100
        col = rnd.choice([LIME, RED, BLUE, INK, "#FFD166"]); s = 12
        d.rectangle([x // s * s, y // s * s, x // s * s + s, y // s * s + s * (1 + int(u * 8 + i) % 2)], fill=col)
    return img

def room(name, t, dim=0.62): return newwave.room_frame(name, t, dim)

def band(t, name="ROOM-03", anims=None, dim=0.66):
    """The whole band on the rooftop: back row Ada, Roz, Kit; front row Penny (vocals) and Theo."""
    img = lights(room(name, t, dim), t); a = anims or {}
    for ch, cx, feet, k, fl in (("ada", 230, 1180, 5, False), ("roz", 540, 1170, 5, False), ("kit", 850, 1180, 5, True),
                                ("theo", 330, 1440, 7, False), ("penny", 760, 1440, 7, True)):
        rig(img, ch, a.get(ch, "celebrate"), t + cx * 0.001, cx, feet, k, fl)
    return img

def desk(ch, st, an, mon, role):
    def f(t, u): return V6["desk_shot"](dict(st=st, ch=ch, an=an, mon=mon, name=ch.upper(), role=role), t, u, 3.0, 0)
    return f

# ---------- shots: (start beat, fn(t, u)) ----------
def s_title(t, u):
    img = band(t, anims={"theo": "idle", "penny": "idle", "ada": "idle", "roz": "idle", "kit": "dance"})
    stamp(img, "ROUNDING ERROR", INK, 640, 130); return stamp(img, "THE BAND", LIME, 790, 110)
def s_single(t, u):
    img = Image.new("RGB", (W, H)); img.paste(room("OFF-KIT-01", t, 0.7)); rig(img, "kit", "dance", t, 540, 1440, 9)
    stamp(img, "FIRST SINGLE:", INK, 600, 90); stamp(img, "NEVER HIT", RED, 760, 150); return stamp(img, "MARKET ORDER", RED, 920, 150)
def s_updown(t, u):
    img = candles(room("ROOM-01", t, 0.45), t, 16); up_ = int(beat_of(t)) % 2 == 0
    rig(img, "theo", "celebrate" if up_ else "idle", t, 300, 1440, 7); rig(img, "penny", "idle" if up_ else "celebrate", t, 780, 1440, 7, True)
    return stamp(img, "UP!" if up_ else "DOWN!", GREEN if up_ else RED, 1280, 150)
def s_limit(t, u):
    img = room("ROOM-01", t, 0.55); rig(img, "ada", "nod", t, 190, 1400, 6); rig(img, "roz", "nod", t, 890, 1400, 6, True)
    rig(img, "theo", "holdsign", t, 540, 1440, 8, hop=False)
    d = ImageDraw.Draw(img); d.rectangle([250, 600, 830, 800], fill=INK, outline="#000000", width=10)
    f = fit("LIMIT ORDER", 520, 110, wdth=125, wght=900); d.text((540, 700), "LIMIT ORDER", font=f, fill="#0B0B0B", anchor="mm")
    return img
def s_button(t, u):
    img = room("ROOM-16", t, 0.55); rig(img, "penny", "point", t, 300, 1440, 8); rig(img, "theo", "shakehead", t, 820, 1440, 7, True)
    return market_button(img, t, 44)
def s_ladder(t, u):
    img = room("ROOM-15", t, 0.5); ladder(img, t, 48); rig(img, "roz", "shakehead", t, 840, 1440, 6, True); return img
def s_okay(t, u):
    img = band(t); b = beat_of(t)
    return stamp(img, "OKAY!", LIME, 820, 220) if b >= 61 else img
def s_phone(ch, st, an, mon, role):
    f = desk(ch, st, an, mon, role)
    def g(t, u): return f(t, u)
    return g
def s_solo(t, u):
    img = Image.new("RGB", (W, H)); img.paste(room("OFF-KIT-01", t, 0.55)); img = lights(img, t)
    rig(img, "kit", "play" if int(beat_of(t) / 4) % 2 else "dance", t, 540, 1440, 10)
    stamp(img, "KIT'S SOLO", LIME, 560, 140); return stamp(img, "(still no market orders)", INK, 700, 54)
def s_book_solo(t, u):
    img = room("ROOM-01", t, 0.45); ladder(img, t, 104, fill_at=118); rig(img, "theo", "celebrate" if beat_of(t) >= 118 else "idle", t, 820, 1440, 6, True)
    return stamp(img, "THEO'S SOLO: THE ORDER BOOK", INK, 300, 64)
def s_final(t, u):
    img = band(t); return confetti(img, t, tb(128))
def s_vocal(t, u):
    img = lights(room("OFF-PENNY-01", t, 0.6), t); rig(img, "penny", "talk", t, 540, 1440, 10); return confetti(img, t, tb(128))
def s_okay2(t, u):
    img = confetti(band(t), t, tb(128)); return stamp(img, "OKAY!", LIME, 820, 220) if beat_of(t) >= 157 else img
def s_end(t, u):
    img = Image.new("RGB", (W, H), "#05060A"); stamp(img, "NEVER HIT", RED, 700, 160); stamp(img, "MARKET ORDER", RED, 880, 160)
    stamp(img, "Rounding Error · our first single", INK, 1080, 58); stamp(img, "Limit orders only. Follow the band.", LIME, 1200, 48)
    rig(img, "penny", "celebrate", t, 300, 1640, 5); rig(img, "theo", "nod", t, 540, 1640, 5); rig(img, "kit", "dance", t, 780, 1640, 5, True)
    return img

SHOTS = [(0, s_title), (8, s_single), (16, s_updown), (32, s_limit), (40, s_button), (48, s_ladder), (56, s_okay),
         (64, s_phone("theo", "OFF-THEO-01", "desk_phone", "MON-01", "BASS · ON THE PHONE")),
         (72, s_phone("penny", "OFF-PENNY-01", "desk34_phone", "MON-05", "LEAD VOCALS")),
         (80, s_phone("ada", "OFF-ADA-01", "desk_phone", "MON-01", "DRUMS")),
         (88, s_phone("roz", "OFF-ROZ-01", "desk34_phone", "MON-02", "KEYS")),
         (96, s_solo), (104, s_book_solo), (120, s_final), (128, s_final), (136, s_vocal), (144, s_final), (152, s_okay2), (160, s_end)]

def frame_at(t):
    b = beat_of(t); i = max(j for j, (sb, _) in enumerate(SHOTS) if b >= sb or j == 0)
    sb, fn = SHOTS[i]; img = fn(t, t - tb(sb))
    if img.size != (W, H): img = img.resize((W, H), Image.NEAREST)
    if fn is not s_end: img = tape(img, t); img = karaoke(img, t)
    return img.convert("RGB")

def panels(out):
    ts = [tb(sb) + 3 * BEAT for sb, _ in SHOTS]; pw, ph = 216, 384; cols = 10; rows = (len(ts) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * pw, rows * (ph + 30)), "#111"); d = ImageDraw.Draw(sheet)
    for n, t in enumerate(ts):
        sheet.paste(frame_at(min(t, END - 0.1)).resize((pw, ph)), ((n % cols) * pw, (n // cols) * (ph + 30) + 30)); d.text(((n % cols) * pw + 4, (n // cols) * (ph + 30) + 6), f"{t:.1f}s", fill=LIME)
    sheet.save(out); print(out)

def build(out):
    wav = out[:-4] + "_mix.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", SONG, "-af", f"apad,atrim=0:{END:.3f},afade=t=out:st={END - 1.5:.3f}:d=1.5", "-ar", "44100", wav], check=True)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "21",
        "-c:a", "aac", "-b:a", "160k", "-af", "loudnorm=I=-14:TP=-1.5", "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for i in range(int(round(END * FPS))): p.stdin.write(frame_at(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print(out, f"{END:.1f}s")

if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    panels(a[0]) if "--panels" in sys.argv else build(a[0] if a else "/home/claude/out/nhmo/never_hit_market_order_v1.mp4")
