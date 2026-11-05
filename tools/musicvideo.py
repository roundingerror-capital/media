"""The Band (music videos): shared pieces for every episode (the boss 2026-11-05: "music videos for every one of our songs").
Generalized from posts/2026-11-04-never-hit-market-order/make.py.

    import musicvideo as MV
    g = MV.Grid(bpm, first_beat)                       # beat grid from librosa
    LINES = [(t0, t1, "lyric line"), ...]              # seconds; karaoke lights words across [t0, t1]
    SHOTS = [(t0, fn), ...]                            # fn(t, u) -> PIL image W x H (u = seconds into the shot)
    MV.build(out, song_key, SHOTS, LINES, g, end=..., tape="WORDS  MORE WORDS")
    MV.cover(out_jpg, title, color, scene_fn)          # the music-video cover (same template every episode)

No figures on screen anywhere (no Theo sheet needed). Lyrics come from the songs row; never committed.
"""
import os, math, random, subprocess
from PIL import Image, ImageDraw
import rigs, newwave
from make_reel import W, H, FPS, mono, fit

LIME, INK, RED, GREEN, BLUE, GOLD = "#C8F03C", "#F2F2EE", "#FF5C5C", "#3BD16F", "#7BAAF7", "#FFD166"
TOOLS = os.path.dirname(os.path.abspath(__file__))
def song_path(key): return os.path.join(TOOLS, "music", key + ".mp3")

class Grid:
    def __init__(self, bpm, b0): self.beat = 60.0 / bpm; self.b0 = b0
    def tb(self, b): return self.b0 + b * self.beat
    def of(self, t): return (t - self.b0) / self.beat
    def pulse(self, t): b = self.of(t); return max(0.0, math.sin(math.pi * (b % 1))) if b >= 0 else 0.0

# ---------- text ----------
def stamp(img, txt, col=LIME, y=820, size=120, x=None):
    d = ImageDraw.Draw(img); f = fit(txt, W - 160, size, wdth=125, wght=900)
    d.text((W // 2 if x is None else x, y), txt, font=f, fill=col, anchor="mm", stroke_width=max(6, size // 12), stroke_fill="#000000"); return img

def karaoke(img, t, LINES, y_mid=1560):
    cur = [x for x in LINES if x[0] <= t < x[1] + 0.35]
    if not cur: return img
    t0, t1, line = cur[-1]; words = line.split(" "); n = len(words); span = max(0.5, (t1 - t0) * 0.92)
    lit = sum(1 for i in range(n) if t >= t0 + i * span / n)
    f = fit("Never smash the market", W - 150, 92, wdth=110, wght=900)
    rows, row = [], []
    for w_ in words:
        if f.getlength(" ".join(row + [w_])) > W - 140 and row: rows.append(row); row = []
        row.append(w_)
    rows.append(row)
    d = ImageDraw.Draw(img); lh = int(f.size * 1.15); y0 = y_mid - (len(rows) - 1) * lh // 2
    pad = 22; bw = max(f.getlength(" ".join(r)) for r in rows)
    d.rectangle([W // 2 - bw / 2 - pad, y0 - lh // 2 - pad + 6, W // 2 + bw / 2 + pad, y0 + (len(rows) - 1) * lh + lh // 2 + pad - 6], fill="#000000")
    k = 0
    for ri, r in enumerate(rows):
        x = W // 2 - f.getlength(" ".join(r)) / 2; y = y0 + ri * lh
        for w_ in r:
            col = LIME if k < lit else "#6E6E68"
            if k == lit - 1 and t - (t0 + (lit - 1) * span / n) < 0.35: col = INK
            d.text((x, y), w_, font=f, fill=col, anchor="lm"); x += f.getlength(w_ + " "); k += 1
    return img

def tape(img, t, words, y=236, speed=150, good=(), bad=()):
    """A ticker tape of words (no figures). Tokens in `good` are green, in `bad` red."""
    d = ImageDraw.Draw(img); f = mono(34, True); line = "  ".join(words) + "  "
    d.rectangle([0, y - 30, W, y + 30], fill="#05060A"); d.line([(0, y - 30), (W, y - 30)], fill=LIME, width=3); d.line([(0, y + 30), (W, y + 30)], fill=LIME, width=3)
    L = int(f.getlength(line)); x = -int(t * speed) % L - L
    while x < W:
        cx = x
        for tok in words:
            col = GREEN if tok in good else RED if tok in bad else INK
            d.text((cx, y), tok, font=f, fill=col, anchor="lm"); cx += f.getlength(tok + "  ")
        x += L
    return img

# ---------- the cast ----------
def rig(img, ch, an, t, cx, feet, k=6, flip=False, g=None, hop=True):
    sp = rigs.frame(ch, an, t, k=k, flip=flip, loop=True)
    h = int(k * 3 * g.pulse(t)) if (g and hop) else 0
    bw = rigs.body(ch, "idle", k)[0]
    d = ImageDraw.Draw(img); d.ellipse([cx - bw * 0.33, feet - 8, cx + bw * 0.33, feet + 14], fill="#121212")
    img.paste(sp, (int(cx - sp.width // 2), int(feet - sp.height - h)), sp)
    return img

def room(name, t, dim=0.62): return newwave.room_frame(name, t, dim)

def lights(img, t, g, n=4, cols=((200, 240, 60), (123, 170, 247), (255, 92, 92), (255, 255, 255)), a=46):
    c = Image.new("RGBA", (W // 8, H // 8)); d = ImageDraw.Draw(c); b = g.of(t)
    for i in range(n):
        x = (i + 0.5) * c.width / n; sw = math.sin(math.pi * (b / 2 + i * 0.5)) * 30; col = cols[(i + int(b / 4)) % len(cols)]
        d.polygon([(x - 2, 0), (x + 2, 0), (x + sw + 22, c.height * 0.78), (x + sw - 22, c.height * 0.78)], fill=col + (a,))
    base = img.convert("RGBA"); base.alpha_composite(c.resize(img.size, Image.NEAREST)); return base.convert("RGB")

def confetti(img, t, t0, n=70):
    d = ImageDraw.Draw(img); rnd = random.Random(7); u = t - t0
    for i in range(n):
        x = rnd.randrange(0, W); v = rnd.uniform(260, 520); y = int((rnd.uniform(-1400, 0) + u * v) % (H + 200)) - 100
        col = rnd.choice([LIME, RED, BLUE, INK, GOLD]); s = 12
        d.rectangle([x // s * s, y // s * s, x // s * s + s, y // s * s + s * (1 + int(u * 8 + i) % 2)], fill=col)
    return img

BAND = (("ada", 230, 1180, 5, False), ("roz", 540, 1170, 5, False), ("kit", 850, 1180, 5, True), ("theo", 330, 1440, 7, False), ("penny", 760, 1440, 7, True))
def band(t, g, name="ROOM-03", anims=None, dim=0.66, lit=True):
    img = room(name, t, dim)
    if lit: img = lights(img, t, g)
    a = anims or {}
    for ch, cx, feet, k, fl in BAND: rig(img, ch, a.get(ch, "celebrate"), t + cx * 0.001, cx, feet, k, fl, g)
    return img

def solo(t, g, ch, an, room_name, label, sub=None, dim=0.55):
    img = lights(room(room_name, t, dim), t, g); rig(img, ch, an, t, 540, 1440, 10, False, g)
    stamp(img, label, LIME, 560, 130)
    if sub: stamp(img, sub, INK, 700, 54)
    return img

def title_card(t, g, title_lines, color, room_name="ROOM-03", anims=None):
    img = band(t, g, room_name, anims or {"theo": "idle", "penny": "idle", "ada": "idle", "roz": "idle", "kit": "idle"})
    stamp(img, "ROUNDING ERROR · THE BAND", INK, 520, 70)
    for i, ln in enumerate(title_lines): stamp(img, ln, color, 660 + i * 150, 140)
    return img

def end_card(t, g, title_lines, color, line2="Rounding Error · The Band", line3="Follow the band."):
    img = Image.new("RGB", (W, H), "#05060A")
    for i, ln in enumerate(title_lines): stamp(img, ln, color, 700 + i * 170, 150)
    y = 700 + len(title_lines) * 170
    stamp(img, line2, INK, y + 30, 58); stamp(img, line3, LIME, y + 140, 50)
    rig(img, "penny", "celebrate", t, 300, 1700, 5, False, g); rig(img, "theo", "nod", t, 540, 1700, 5, False, g); rig(img, "kit", "dance", t, 780, 1700, 5, True, g)
    return img

# ---------- the music-video cover (one template for the series) ----------
def cover(out, title_lines, color, scene):
    """scene: a full-frame PIL image (the band shot). Adds a dark gradient, the title, an OFFICIAL MUSIC VIDEO badge, a play triangle, [re.c] · THE BAND."""
    img = scene.convert("RGB").copy(); ov = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(ov)
    for y in range(H):
        a = int(235 * max(0, (y - 1380) / (H - 1380)) ** 0.8) if y > 1380 else int(150 * max(0, (380 - y) / 380))
        d.line([(0, y), (W, y)], fill=(0, 0, 0, a))
    img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB"); d = ImageDraw.Draw(img)
    # badge with a play triangle
    f = mono(44, True); bw = int(f.getlength("OFFICIAL MUSIC VIDEO")) + 150
    d.rectangle([W // 2 - bw // 2, 150, W // 2 + bw // 2, 240], fill=color)
    tx = W // 2 - bw // 2 + 30; d.polygon([(tx, 168), (tx, 222), (tx + 48, 195)], fill="#0B0B0B")
    d.text((tx + 72, 195), "OFFICIAL MUSIC VIDEO", font=f, fill="#0B0B0B", anchor="lm")
    # title under the band, label at the bottom
    for i, ln in enumerate(title_lines): stamp(img, ln, color if i == len(title_lines) - 1 else INK, 1560 + i * 160 - (len(title_lines) - 2) * 80, 150)
    d.text((W // 2, 1860), "[re.c] · THE BAND", font=mono(44, True), fill=INK, anchor="mm")
    img.save(out, quality=92); print(out); return img

# ---------- build ----------
def frame_at(t, SHOTS, LINES, g, tape_words=None, karaoke_on=True, tape_kw=None, end_fn=None):
    i = max(j for j, (s0, _) in enumerate(SHOTS) if t >= s0 or j == 0)
    s0, fn = SHOTS[i]; img = fn(t, t - s0)
    if img.size != (W, H): img = img.resize((W, H), Image.NEAREST)
    if fn is not end_fn:
        if tape_words: img = tape(img, t, tape_words, **(tape_kw or {}))
        if karaoke_on: img = karaoke(img, t, LINES)
    return img.convert("RGB")

def panels(out, SHOTS, LINES, g, end, **kw):
    ts = [min(end - 0.1, s0 + 1.5) for s0, _ in SHOTS]; pw, ph = 216, 384; cols = 10; rows = (len(ts) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * pw, rows * (ph + 30)), "#111"); d = ImageDraw.Draw(sheet)
    for n, t in enumerate(ts):
        sheet.paste(frame_at(t, SHOTS, LINES, g, **kw).resize((pw, ph)), ((n % cols) * pw, (n // cols) * (ph + 30) + 30)); d.text(((n % cols) * pw + 4, (n // cols) * (ph + 30) + 6), f"{t:.1f}s", fill=LIME)
    sheet.save(out); print(out)

def build(out, song_key, SHOTS, LINES, g, end, **kw):
    os.makedirs(os.path.dirname(out), exist_ok=True); wav = out[:-4] + "_mix.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", song_path(song_key), "-af", f"apad,atrim=0:{end:.3f},afade=t=out:st={end - 1.5:.3f}:d=1.5", "-ar", "44100", wav], check=True)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "23",
        "-c:a", "aac", "-b:a", "160k", "-af", "loudnorm=I=-14:TP=-1.5", "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for i in range(int(round(end * FPS))): p.stdin.write(frame_at(i / FPS, SHOTS, LINES, g, **kw).tobytes())
    p.stdin.close(); p.wait(); print(out, f"{end:.1f}s")
