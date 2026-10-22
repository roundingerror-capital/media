"""Daily post builder v2 (Penny, locked 2026-10-19 standard).
Cover held 1.0 s (frames 0-29, so TikTok's grid cover is the post's own cover), then the AI TRADING BOT flash-card intro (2.5 s, black, lime chart),
then scenes with big animated characters and an original beat (tools/beat.py).
Usage (from a spec module): build(spec, out_mp4, cover_jpg, variant="a"|"b")
A spec may define "b" overrides: {"hook": [...heads...]} replaces scene 1's headline.
No numbers here: every figure lives in the spec and must be on a Theo fact sheet."""
import os, sys, math, random, subprocess, colorsys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
from make_reel import W, H, FPS, archivo, mono, fit, fade, blend
import beat as BEAT
HERE = os.path.dirname(os.path.abspath(__file__))
M = 72; LIME = "#C8F03C"; INK = "#F2F2EE"; MUT = "#9A9A94"; LINE = "#262626"; DIM = (40, 48, 20)
INTRO_F = 75  # 2.5 s intro after the cover
COVER_F = 30  # cover held 1.0 s (the boss 2026-10-21: TikTok covers all looked the same)

def river_teal(im):
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if not a: continue
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            if s > 0.18:
                r, g, b = (int(c * 255) for c in colorsys.hsv_to_rgb(0.49, min(1, s * .85), v)); px[x, y] = (r, g, b, a)
    return im
SP = {n: Image.open(os.path.join(HERE, "sprites", f"{n}_sprite_1x.png")).convert("RGBA") for n in ("theo", "penny", "ada")}
SP["ada"] = river_teal(SP["ada"])
# eye boxes on the 1x sprites (x0, y0, x1, y1 inclusive), lid colour sample, closed-line row
EYES = {"penny": ([(12, 20, 14, 23), (26, 20, 28, 23)], (8, 22), 22),
        "theo": ([(13, 13, 17, 17), (24, 13, 28, 17)], (12, 11), 16),
        "ada": ([(8, 10, 12, 15), (24, 10, 28, 15)], (9, 8), 13)}
LASH = (26, 26, 26, 255)

def sprite_state(name, blink, t):
    s = SP[name].copy(); px = s.load()
    if blink:
        boxes, (sx, sy), row = EYES[name]; lid = px[sx, sy]
        for x0, y0, x1, y1 in boxes:
            for y in range(y0, y1 + 1):
                for x in range(x0, x1 + 1):
                    if px[x, y][3]: px[x, y] = lid
            for x in range(x0, x1 + 1): px[x, row] = LASH
    if name == "penny":  # bolt-feather wiggle: shift crest rows
        dx = int(round(math.sin(t * 9)))
        if dx:
            crest = s.crop((0, 0, s.width, 10)); s.paste((0, 0, 0, 0), (0, 0, s.width, 10))
            s.alpha_composite(crest, (dx, 0))
    return s

def chart_pts(shape, seed):
    rnd = random.Random(seed); pts = []
    for i in range(41):
        t = i / 40
        if shape == "crash": v = 0.25 + 0.15 * t + rnd.uniform(-.03, .03) if t < .55 else 0.33 + (t - .55) * 1.4 + rnd.uniform(-.03, .03)
        elif shape == "spike": v = 0.75 - 0.25 * t + rnd.uniform(-.03, .03) if t < .6 else 0.6 - (t - .6) * 1.25 + rnd.uniform(-.03, .03)
        else: v = 0.85 - 0.6 * t + 0.06 * math.sin(t * 14) + rnd.uniform(-.03, .03)  # climb
        pts.append((40 + i * 25, 260 + v * 1300))
    return pts

def intro_frame(fr, pts):
    im = Image.new("RGB", (W, H), (0, 0, 0)); d = ImageDraw.Draw(im); rnd = random.Random(fr)
    n = max(2, min(len(pts), int(len(pts) * fr / 18) + 2)) if fr < 18 else len(pts)
    col = LIME if fr < 18 else DIM
    for k in range(1, n): d.line([pts[k - 1], pts[k]], fill=col, width=14 if fr < 18 else 10)
    if fr < 18:
        x, y = pts[n - 1]; d.ellipse([x - 18, y - 18, x + 18, y + 18], fill=LIME)
    if fr >= 18:
        k = fr - 18; sc = 1.0 + max(0, 0.35 * (1 - k / 6)); sh = (rnd.randint(-10, 10), rnd.randint(-10, 10)) if k < 7 else (0, 0)
        d.text((M, 300), "I'M A FULLY AUTONOMOUS", font=fit("I'M A FULLY AUTONOMOUS", W - 2 * M, 120, wdth=100, wght=900), fill=INK)
        y = 400
        for t, c, cap in (("AI", LIME, 400), ("TRADING", LIME, 260), ("BOT", INK, 330)):
            f = archivo(int(cap * 1.4 * sc), 125, 900); bb = d.textbbox((0, 0), t, font=f)
            if bb[2] - bb[0] > (W - 2 * M) * sc:
                f = archivo(int(f.size * (W - 2 * M) * sc / (bb[2] - bb[0])), 125, 900); bb = d.textbbox((0, 0), t, font=f)
            if bb[3] - bb[1] > cap * sc:
                f = archivo(int(f.size * cap * sc / (bb[3] - bb[1])), 125, 900); bb = d.textbbox((0, 0), t, font=f)
            w, h = bb[2] - bb[0], bb[3] - bb[1]
            d.text(((W - w) // 2 - bb[0] + sh[0], y - bb[1] + sh[1]), t, font=f, fill=c); y += int(h / sc) + 34
        if fr >= 42:
            a = fade(fr / FPS, 42 / FPS, 48 / FPS); txt = "And this is what's going on ↓"
            d.text((M, y + 30), txt, font=fit(txt, W - 2 * M, 90, wdth=100, wght=900), fill=blend(INK, a))
    return im

def bubble(d, xc, y, txt):
    f = mono(34, True); tw = int(f.getlength(txt)); bw, bh = tw + 48, 76
    bx = int(min(max(M, xc - bw / 2), W - M - bw))
    d.rectangle([bx, y, bx + bw, y + bh], fill=INK); d.rectangle([bx + 4, y + 4, bx + bw - 5, y + bh - 5], outline="#1A1A1A", width=4)
    d.polygon([(xc - 14, y + bh), (xc + 14, y + bh), (xc, y + bh + 20)], fill=INK)
    d.text((bx + 24, y + 52), txt, font=f, fill="#000000", anchor="ls")

XS = {1: [0.5], 2: [0.3, 0.7], 3: [0.2, 0.5, 0.8]}
BLINK = {"penny": (2.7, 0.3), "theo": (3.6, 1.1), "ada": (2.2, 0.7)}
BASE = 1690

def char_layer(img, d, S, t, cast, lines, text_bottom):
    bpm = S["bpm"]; ph = t * bpm / 60
    hpx = 430 if len(cast) < 3 else 380
    for i, n in enumerate(cast):
        xc = int(W * XS[len(cast)][i]); per, off = BLINK[n]
        blink = ((t + off) % per) < 0.12
        talk = [(ts, te, pose) for ts, te, w, _, pose in lines if w == n and ts <= t < te]
        sx = 1 - 0.03 * math.sin(2 * math.pi * ph / 2); sy = 1 + 0.035 * math.sin(2 * math.pi * ph / 2)
        hop = 12 * abs(math.sin(math.pi * ph)); ang = 3 * math.sin(2 * math.pi * t / 3.1 + off * 3); dx = 0; zoom = 1.0
        if talk:
            ts, te, pose = talk[0]; u = t - ts
            zoom = 1 + 0.15 * fade(t, ts, ts + 0.25) * (1 - fade(t, te - 0.2, te))
            if pose == "jump": hop += 70 * abs(math.sin(math.pi * u * 2.5))
            elif pose == "wave": ang = 10 * math.sin(2 * math.pi * u * 3)
            elif pose == "point": ang = 12 if xc > W / 2 else -12; dx = -18 if xc > W / 2 else 18
            elif pose == "nod": hop = -10 * abs(math.sin(2 * math.pi * u * 1.5)) if u < 1.2 else hop * .3
            elif pose == "brow": ang = 6; hop *= 0.3
            elif pose == "spin":
                if u < 0.8: sx *= math.cos(2 * math.pi * u / 0.8)
                hop += 30 * abs(math.sin(math.pi * u * 2))
            elif pose == "thumbs": hop += 50 * abs(math.sin(math.pi * u * 3)); ang = 8
        s = sprite_state(n, blink, t)
        h = int(hpx * sy * zoom); w = max(2, int(abs(s.width * hpx / s.height * sx * zoom)))
        big = s.resize((w, h), Image.NEAREST)
        if sx < 0: big = big.transpose(Image.FLIP_LEFT_RIGHT)
        if abs(ang) > 0.5: big = big.rotate(ang, resample=Image.NEAREST, expand=True)
        d.ellipse([xc - w * 0.33, BASE - 8, xc + w * 0.33, BASE + 16], fill="#1a1a1a")
        top = BASE - big.height - int(hop)
        img.paste(big, (xc - big.width // 2 + dx, top), big)
    for ts, te, w, ln, _ in lines:
        if ts <= t < te and w in cast:
            xc = int(W * XS[len(cast)][cast.index(w)])
            y = max(text_bottom + 24, BASE - hpx - 150)
            bubble(d, xc, y, ln)

def scene_frame(S, t, heads_override=None):
    img = Image.new("RGB", (W, H), "#000000"); d = ImageDraw.Draw(img)
    d.text((M, 120), "≈ Rounding Error", font=archivo(40, 110, 800), fill=INK, anchor="ls")
    d.text((W - M, 120), S["label"], font=mono(24), fill=MUT, anchor="rs")
    d.line([(M, 150), (W - M, 150)], fill=LINE, width=2)
    sc = S["scenes"]; k = max(i for i, s in enumerate(sc) if t >= s[0] or i == 0)
    t0, t1, kick, heads, body, lines, cast, hl = sc[k]
    if k == 0 and heads_override: heads = heads_override
    a = 1.0 if k == 0 else fade(t, t0, t0 + 0.3)
    d.text((M, 290), kick, font=mono(30, True), fill=blend(LIME, a), anchor="ls")
    f = min((fit(h, W - 2 * M - 8, 160 if len(heads) == 1 else 132, wdth=110, wght=900) for h, _ in heads), key=lambda q: q.size)
    y = 300 + int(f.size * 1.05)
    for i, (h, c) in enumerate(heads):
        ha = a * fade(t, t0 + i * 0.12, t0 + 0.3 + i * 0.12) if k else (1.0 if t > 0.25 else fade(t, i * 0.06, 0.2 + i * 0.06))
        d.text((M, y), h, font=f, fill=blend(c, ha), anchor="ls"); y += int(f.size * 1.05)
    y += 30
    for i, ln in enumerate(body):
        ba = a * fade(t, t0 + 0.5 + i * 0.3, t0 + 0.8 + i * 0.3)
        d.text((M, y), ln, font=mono(38, True), fill=blend(LIME if i == hl else INK, ba), anchor="ls"); y += 62
    char_layer(img, d, S, t, cast, lines, y - 20)
    d.line([(M, 1735), (W - M, 1735)], fill=LINE, width=2)
    d.text((M, 1780), S["foot"], font=mono(22), fill=MUT, anchor="ls")
    d.text((M, 1816), "@ROUNDINGERROR.CAPITAL", font=mono(22), fill=MUT, anchor="ls")
    return img

LOOP_F = 12  # 0.4 s crossfade to the cover in the loop variant
OUTRO_S = 3.5  # end card (the boss 2026-10-21): "like and follow for more updates" + our open positions
def outro_frame(S, t):
    """End card. Positions come ONLY from the spec's "positions" list, copied from a Theo fact sheet's
    open_legs: [(ticker, "$100 put", "exp 10/30", "out of the money"), ...]. Never account value, cash,
    account numbers or a broker screenshot (Rules: no fund size or personal data in public)."""
    img = Image.new("RGB", (W, H), "#000000"); d = ImageDraw.Draw(img)
    d.text((M, 120), "\u2248 Rounding Error", font=archivo(40, 110, 800), fill=INK, anchor="ls")
    d.line([(M, 150), (W - M, 150)], fill=LINE, width=2)
    pos = S.get("positions") or []; y = 260
    if pos:
        d.text((M, y), "OUR OPEN POSITIONS" + (" \u00b7 " + S["positions_asof"] if S.get("positions_asof") else ""), font=mono(30, True), fill=LIME, anchor="ls"); y += 30
        for i, row in enumerate(pos[:5]):
            a = fade(t, 0.1 + i * 0.12, 0.35 + i * 0.12)
            d.rectangle([M, y, W - M, y + 92], outline=blend(LINE, a), width=3)
            d.text((M + 24, y + 62), row[0], font=archivo(48, 110, 900), fill=blend(INK, a), anchor="ls")
            d.text((M + 230, y + 42), row[1] + "  " + row[2], font=mono(30, True), fill=blend(INK, a), anchor="ls")
            col = LIME if "out of" in row[3] or "worthless" in row[3] else "#FF8A5B"
            d.text((M + 230, y + 78), row[3].upper(), font=mono(24, True), fill=blend(col, a), anchor="ls")
            y += 110
        y += 40
    else:
        y = 520
    k = max(0.0, t - 0.3); sc = 1.0 + max(0, 0.3 * (1 - k / 0.25)) if t > 0.3 else 0
    if t > 0.3:
        for txt, c in (("LIKE + FOLLOW", LIME), ("FOR MORE UPDATES", INK)):
            f = fit(txt, int((W - 2 * M) * min(sc, 1.3)), 170, wdth=125, wght=900)
            bb = d.textbbox((0, 0), txt, font=f)
            d.text(((W - (bb[2] - bb[0])) // 2 - bb[0], y - bb[1]), txt, font=f, fill=c); y += bb[3] - bb[1] + 26
    char_layer(img, d, S, 30 + t, ["penny"], [(30.0, 40.0, "penny", "", "point")] if t > 0.3 else [], 10**6)
    d.line([(M, 1735), (W - M, 1735)], fill=LINE, width=2)
    d.text((M, 1780), "REAL TRADES \u00b7 REAL MONEY \u00b7 NOT ADVICE", font=mono(22), fill=MUT, anchor="ls")
    d.text((M, 1816), "@ROUNDINGERROR.CAPITAL", font=mono(22), fill=MUT, anchor="ls")
    return img

def build(S, out, cover_jpg, variant="a", workdir="/tmp"):
    content = S["end"]; total = (COVER_F + INTRO_F) / FPS + content + (LOOP_F / FPS if S.get("loop") else OUTRO_S)
    wav = os.path.join(workdir, os.path.basename(out) + ".wav")
    BEAT.make(wav, total + 0.3, S["bpm"], S["root"], S["seed"], S["mel"])
    pts = chart_pts(S["chart"], S["seed"]); cover = Image.open(cover_jpg).convert("RGB").resize((W, H))
    hov = S.get("b", {}).get("hook") if variant == "b" else None
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "20",
        "-c:a", "aac", "-b:a", "160k", "-af", "adelay=33|33,loudnorm=I=-14:TP=-1.5", "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    cb = cover.tobytes()
    for _ in range(COVER_F): p.stdin.write(cb)
    for fr in range(INTRO_F): p.stdin.write(intro_frame(fr, pts).tobytes())
    for i in range(int(content * FPS)): p.stdin.write(scene_frame(S, i / FPS, hov).tobytes())
    if S.get("loop"):
        # LOOP variant (A/B "loop", 2026-10-22): no end card; the last 0.4 s crossfades back into the cover,
        # so the replay starts on the exact frame the viewer just saw.
        last = scene_frame(S, content - 1 / FPS, hov)
        for i in range(LOOP_F): p.stdin.write(Image.blend(last, cover, (i + 1) / LOOP_F).tobytes())
    else:
        for i in range(int(OUTRO_S * FPS)): p.stdin.write(outro_frame(S, i / FPS).tobytes())
    p.stdin.close(); p.wait(); os.remove(wav); return out

if __name__ == "__main__":
    import importlib.util
    spec = importlib.util.spec_from_file_location("spec", sys.argv[1]); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    print(build(m.SPEC, sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else "a"))
