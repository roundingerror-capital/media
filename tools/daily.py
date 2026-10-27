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
INTRO_F = 36  # 1.2 s intro after the cover (the boss 2026-10-22: "Go" on a faster start; was 2.5 s)
INTRO_SRC = 60  # the intro animation is designed on 60 frames and played back compressed into INTRO_F
COVER_F = 18  # cover held 0.6 s (2026-10-21 TikTok grid fix; trimmed from 1.0 s on 2026-10-22 for a faster start)

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
    if name in SHADES_ON: s = _shades(s, name, SHADES_ON[name])
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

def hook_text(S):
    """The post's own hook, on screen from the first intro frame: spec["hook"], else scene 1's headline words."""
    if S.get("hook"): return S["hook"]
    return " ".join(h for h, _ in S["scenes"][0][3])

def intro_hook_frame(S, fr, pts):
    im = intro_frame(int(fr * INTRO_SRC / INTRO_F), pts); d = ImageDraw.Draw(im); txt = hook_text(S)
    f = fit(txt, W - 2 * M, 96, wdth=110, wght=900); bb = d.textbbox((0, 0), txt, font=f)
    y = 1560 - (bb[3] - bb[1]); d.rectangle([0, y - 40, W, 1600], fill="#000000")
    d.text((M - bb[0], y - bb[1]), txt, font=f, fill=LIME)
    return im

def intro_frame(fr, pts):
    im = Image.new("RGB", (W, H), (0, 0, 0)); d = ImageDraw.Draw(im); rnd = random.Random(fr)
    n = max(2, min(len(pts), int(len(pts) * fr / 18) + 2)) if fr < 18 else len(pts)
    col = LIME if fr < 18 else DIM
    for k in range(1, n): d.line([pts[k - 1], pts[k]], fill=col, width=14 if fr < 18 else 10)
    if fr < 18:
        x, y = pts[n - 1]; d.ellipse([x - 18, y - 18, x + 18, y + 18], fill=LIME)
    if fr >= 18:
        k = fr - 18; sc = 1.0 + max(0, 0.35 * (1 - k / 6)); sh = (rnd.randint(-10, 10), rnd.randint(-10, 10)) if k < 7 else (0, 0)
        d.text((M, 285), "I'M AN", font=fit("I'M AN", W - 2 * M, 96, wdth=100, wght=900), fill=INK)
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

CTA_S = 3.5  # small CTA at the start of the story (the boss 2026-10-25: "cta at the beginning small and end big")
def _heart(d, x, y, r, col):
    d.ellipse([x - r, y - r, x, y], fill=col); d.ellipse([x, y - r, x + r, y], fill=col)
    d.polygon([(x - r, y - r * 0.45), (x + r, y - r * 0.45), (x, y + r * 0.9)], fill=col)
def cta_pill(img, u, text="LIKE + FOLLOW", scale=1.0, hold=False, y=None, dur=CTA_S):
    """Small call to action: a lime pill top-right, in the free band between the header rule (y 150) and the kicker (y ~262).
    Slides in, pulses twice, slides out after `dur` s (stays if hold). u = seconds since it appeared."""
    if u < 0 or (not hold and u > dur): return img
    d = ImageDraw.Draw(img); f = archivo(int(40 * scale), 110, 900)
    tw = d.textlength(text, font=f); r = int(14 * scale); pad = int(22 * scale); h = int(64 * scale)
    w = int(tw + pad * 3 + r * 2)
    k_in = min(1, u / 0.25); k_out = 0 if hold else max(0, (u - (dur - 0.3)) / 0.3)
    off = int((1 - (1 - (1 - k_in) ** 3)) * (w + M)) + int(k_out ** 2 * (w + M))
    pulse = 1 + 0.06 * max(0, math.sin(math.pi * min(1, max(0, (u - 0.6) / 0.3)))) + 0.06 * max(0, math.sin(math.pi * min(1, max(0, (u - 1.6) / 0.3))))
    w2, h2 = int(w * pulse), int(h * pulse)
    x1 = W - M + off; x0 = x1 - w2; y0 = (y if y is not None else 176) - (h2 - h) // 2; y1 = y0 + h2
    d.rounded_rectangle([x0, y0, x1, y1], radius=h2 // 2, fill=LIME)
    _heart(d, x0 + pad + r, (y0 + y1) // 2 - r // 4, r, "#000000")
    d.text((x0 + pad * 2 + r * 2, (y0 + y1) // 2), text, font=f, fill="#000000", anchor="lm")
    return img

# TEASER / COLD OPEN (the boss 2026-10-25/26: "all of our videos start with a 1s teaser, short intro, and then the whole story").
# spec["cold_open"] = {"big": "$700", "line": "4 HIMS PUTS.", "shout": "FREE MONEY?!", "tone": "win"|"loss"}; spec["hook"] reads like a rewind.
# Timeline: 0-1.0 s teaser (frames 0-2 = the cover, then it explodes), 1.0-2.2 s the AI TRADING BOT intro, story from 2.2 s.
COLD_F = 30
RED = (235, 38, 38); LIME_T = (200, 240, 60)
_VIG = None
def _vignette():
    global _VIG
    if _VIG is None:
        import numpy as np
        yy, xx = np.mgrid[0:H, 0:W]; r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
        _VIG = Image.fromarray((np.clip((r - 0.35) / 0.9, 0, 1) * 255).astype("uint8"), "L")
    return _VIG
def cold_open_frame(S, fr, cover, pts):
    if fr < 3: return cover
    co = S["cold_open"]; u = fr / FPS; win = co.get("tone") == "win"
    col = LIME_T if win else RED; glow = (40, 70, 0) if win else (120, 8, 8)
    pulse = 0.5 + 0.5 * math.sin(u * 2 * math.pi * 4)
    img = Image.composite(Image.new("RGB", (W, H), glow), Image.new("RGB", (W, H), (0, 0, 0)), _vignette().point(lambda v: int(v * (0.45 + 0.55 * pulse))))
    d = ImageDraw.Draw(img)
    n = max(2, int(len(pts) * min(1, (u - 0.1) / 0.45)))  # the line draws itself
    line = [(x, 1300 + (y - 260) * 0.35) for x, y in pts[:n]]
    if len(line) > 1: d.line(line, fill=col, width=14)
    sc = 1 + 0.6 * max(0, 1 - (u - 0.1) / 0.15)
    big = co["big"]; f = fit(big, int((W - 2 * M) * min(1.0, sc / 1.6 + 0.4)), 420, wdth=125, wght=900)
    d.text((W // 2, 1000), big, font=f, fill=col, anchor="ms", stroke_width=10, stroke_fill="#000000" if win else "#FFFFFF")
    if co.get("line"): d.text((W // 2, 560), co["line"], font=fit(co["line"], W - 2 * M, 96, wdth=125, wght=900), fill=INK, anchor="ms")
    if u > 0.45:
        sh = co.get("shout", "WAIT, WHAT?!"); f2 = fit(sh, W - 2 * M, int(110 * (1 + max(0, .25 - (u - .45)))), wdth=125, wght=900)
        d.text((W // 2, 1180), sh, font=f2, fill=INK, anchor="ms", stroke_width=6, stroke_fill="#000000")
    s = sprite_state("penny", False, u); h = 380; s = s.resize((int(s.width * h / s.height), h), Image.NEAREST)
    hop = int(90 * abs(math.sin(u * math.pi * 4))); img.paste(s, (W // 2 - s.width // 2, 1700 - h - hop), s)
    if u < 0.35:  # impact shake
        k = random.Random(fr).randint(-22, 22); img = img.transform(img.size, Image.AFFINE, (1, 0, k, 0, 1, -k // 2))
    return img

# MEMES (the boss 2026-10-26: "MEME IT UP BRO, we need to go VIRAL"). Original takes on generic meme formats only:
# no copyrighted images, characters, clips or sound samples (every sound is synthesized in tools/beat.py / here).
# spec["memes"] = [{"t": 0.2, "dur": 2.8, "kind": "pov", "text": "POV: ..."},
#                  {"t": 3.0, "dur": 1.6, "kind": "shades", "who": "theo"},          # pixel deal-with-it shades drop + boom
#                  {"t": 9.0, "dur": 1.2, "kind": "zoom", "text": "..."},             # dramatic zoom + shake + boom
#                  {"t": 13.0, "dur": 2.4, "kind": "twopanel", "a": "OPTIONS:", "a2": "PANICKING", "b": "THE STOCK:", "b2": "CHILLING"},
#                  {"t": 19.5, "dur": 1.6, "kind": "freeze", "text": "yep. that's the whole plan."}]  # freeze frame + record scratch
# Meme text sits in the free middle band (y ~860-1120, between the body text and the characters): never over a number, a headline or a face; every number in it is on a Theo sheet.
SHADES_ON = {}
def _shades(s, name, k):
    """Draw pixel shades over the sprite's eyes; k 0..1 = drop progress (0 = above the head)."""
    boxes, _, _ = EYES[name]; d = ImageDraw.Draw(s)
    x0 = min(b[0] for b in boxes) - 2; x1 = max(b[2] for b in boxes) + 2; y0 = min(b[1] for b in boxes); y1 = max(b[3] for b in boxes)
    dy = int((1 - k) * -(y0 + 6))
    d.rectangle([x0, y0 + dy, x1, y0 + dy + 1], fill=(10, 10, 10, 255))
    for bx0, by0, bx1, by1 in boxes:
        d.rectangle([bx0 - 1, y0 + dy, bx1 + 1, y1 + dy], fill=(10, 10, 10, 255))
        d.point((bx0, y0 + dy + 1), fill=(255, 255, 255, 255))
    return s
def meme_layer(img, S, t):
    d = ImageDraw.Draw(img)
    for m in S.get("memes", []):
        u = t - m["t"]
        if u < 0 or u > m.get("dur", 1.5): continue
        k = m["kind"]
        if k == "pov":
            f = fit(m["text"], W - 2 * M, 64, wdth=100, wght=900); a = min(1, u / 0.12)
            d.rectangle([0, 900, W, 1020], fill=(255, 255, 255))
            d.text((W // 2, 982), m["text"], font=f, fill="#000000", anchor="ms")
        elif k == "zoom":
            z = 1 + 0.25 * min(1, u / 0.12); cx, cy = W // 2, H // 2
            box = (int(cx - W / z / 2), int(cy - H / z / 2), int(cx + W / z / 2), int(cy + H / z / 2))
            im2 = img.crop(box).resize((W, H)); sh = random.Random(int(t * 30)).randint(-14, 14) if u < 0.4 else 0
            im2 = im2.transform(im2.size, Image.AFFINE, (1, 0, sh, 0, 1, sh // 2))
            g = Image.new("RGB", (W, H), (0, 0, 0)); im2 = Image.composite(g, im2, _vignette().point(lambda v: int(v * 0.8)))
            img.paste(im2); d = ImageDraw.Draw(img)
            if m.get("text"):
                f = fit(m["text"], W - 2 * M, 110, wdth=125, wght=900)
                d.text((W // 2, 1000), m["text"], font=f, fill=(255, 255, 255), anchor="ms", stroke_width=8, stroke_fill="#000000")
        elif k == "twopanel":
            d.rectangle([0, 860, W, 1120], fill=(0, 0, 0))
            for i, (lab, val) in enumerate(((m["a"], m["a2"]), (m["b"], m["b2"]))):
                if u < i * 0.6: continue
                y = 950 + i * 120
                d.text((M, y), lab, font=archivo(52, 100, 900), fill=INK, anchor="ls")
                d.text((W - M, y), val, font=archivo(64, 100, 900), fill=m.get("a2c", "#EB2626") if i == 0 else m.get("b2c", LIME), anchor="rs")
        elif k == "freeze":
            g = img.convert("L").convert("RGB"); img.paste(Image.blend(g, Image.new("RGB", (W, H), (40, 30, 20)), 0.25)); d = ImageDraw.Draw(img)
            f = fit(m["text"], W - 2 * M, 84, wdth=110, wght=900)
            d.rectangle([0, 900, W, 1040], fill=(0, 0, 0)); d.text((W // 2, 995), m["text"], font=f, fill=(255, 255, 255), anchor="ms")
    return img
def meme_sfx(S, offset):
    """(time, kind) list for the beat: boom on shades/zoom, scratch on freeze, pop on pov/twopanel. offset = seconds before the story starts."""
    out = []
    for m in S.get("memes", []):
        kk = {"shades": "boom", "zoom": "boom", "freeze": "scratch", "pov": "pop", "twopanel": "pop"}[m["kind"]]
        out.append((offset + m["t"], kk))
    return out
def chart_panel(d, vals, labels, y0, y1, note=""):
    """Bars of a series (e.g. a put's P&L as % of the premium, per day). Every value must be on a Theo fact sheet."""
    n = len(vals); lo = min(0, min(vals)); hi = max(0, max(vals)); rng = (hi - lo) or 1
    zero = y0 + (hi / rng) * (y1 - y0); bw = (W - 2 * M) / n
    d.line([(M, zero), (W - M, zero)], fill=MUT, width=3)
    for i, (v, lab) in enumerate(zip(vals, labels)):
        x0 = M + i * bw + bw * .18; x1 = M + (i + 1) * bw - bw * .18; yv = zero - v / rng * (y1 - y0)
        d.rectangle([x0, min(zero, yv), x1, max(zero, yv)], fill=RED if v < 0 else LIME)
        d.text(((x0 + x1) / 2, max(zero, yv) + 34), f"{v:+d}%".replace("-", "\u2212"), font=mono(24, True), fill=INK, anchor="ms")
        d.text(((x0 + x1) / 2, y0 - 14), lab, font=mono(22), fill=MUT, anchor="ms")
    if note: d.text((M, y1 + 90), note, font=mono(22), fill=MUT, anchor="ls")

def threeway_panel(d, cards, y0, quote=""):
    """THE THREE-WAY (decision 20261022-threeway-series-1): SAFER · OURS · RISKIER side by side.
    cards = [{"tag": "SAFER", "strike": "$22", "prem": "$0.40", "yld": "1.82%", "delta": "0.139", "hypo": True}, ...] from the fill sheet's variants."""
    cw = (W - 2 * M - 2 * 24) // 3; ch = 470
    for i, c in enumerate(cards):
        x0 = M + i * (cw + 24); ours = not c.get("hypo")
        d.rectangle([x0, y0, x0 + cw, y0 + ch], fill="#0f0f0f", outline=LIME if ours else "#5a5a5a", width=8 if ours else 3)
        d.text((x0 + cw // 2, y0 + 56), c["tag"], font=archivo(44, 125, 900), fill=LIME if ours else INK, anchor="ms")
        d.text((x0 + cw // 2, y0 + 160), c["strike"], font=archivo(80, 110, 900), fill=INK, anchor="ms")
        d.text((x0 + cw // 2, y0 + 200), "strike", font=mono(22), fill=MUT, anchor="ms")
        d.text((x0 + cw // 2, y0 + 268), c["prem"], font=archivo(54, 110, 900), fill=INK, anchor="ms")
        d.text((x0 + cw // 2, y0 + 300), "premium/share", font=mono(22), fill=MUT, anchor="ms")
        d.text((x0 + cw // 2, y0 + 362), c["yld"], font=archivo(54, 110, 900), fill=LIME if ours else INK, anchor="ms")
        d.text((x0 + cw // 2, y0 + 394), "if it expires", font=mono(22), fill=MUT, anchor="ms")
        d.text((x0 + cw // 2, y0 + 436), "delta " + c["delta"], font=mono(22, True), fill=MUT, anchor="ms")
        if c.get("hypo"):
            d.rectangle([x0 + 10, y0 + ch - 4, x0 + cw - 10, y0 + ch + 40], fill="#FF8A5B")
            d.text((x0 + cw // 2, y0 + ch + 28), "HYPOTHETICAL", font=mono(24, True), fill="#000000", anchor="ms")
    d.text((W // 2, y0 + ch + 90), "Variants: hypothetical, never traded, not a recommendation.", font=mono(24, True), fill=INK, anchor="ms")
    if quote: d.text((W // 2, y0 + ch + 126), quote, font=mono(22), fill=MUT, anchor="ms")

def scene_frame(S, t, heads_override=None):
    SHADES_ON.clear()
    for m in S.get("memes", []):
        if m["kind"] == "shades" and m["t"] <= t <= m["t"] + m.get("dur", 1.6): SHADES_ON[m.get("who", "theo")] = min(1, (t - m["t"]) / 0.3)
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
    tw = (S.get("threeway") or {}).get(k)
    if tw:
        threeway_panel(d, tw["cards"], y + 10, tw.get("quote", "")); y += 660
    ch = (S.get("charts") or {}).get(k)
    if ch:
        chart_panel(d, ch["vals"], ch["labels"], y + 40, y + 300, ch.get("note", "")); y += 400
    char_layer(img, d, S, t, cast, lines, y - 20)
    d.line([(M, 1735), (W - M, 1735)], fill=LINE, width=2)
    d.text((M, 1780), S["foot"].replace("NOT ADVICE", "NOT FINANCIAL ADVICE"), font=mono(22), fill=MUT, anchor="ls")
    d.text((M, 1816), "@ROUNDINGERROR.CAPITAL", font=mono(22), fill=MUT, anchor="ls")
    img = meme_layer(img, S, t)
    cta_pill(img, t)  # small CTA as the story starts (every video)
    if S.get("loop") and S.get("end") and t > S["end"] - 2.5:  # loops have no end card: a bigger CTA holds through the last 2.5 s
        cta_pill(img, t - (S["end"] - 2.5), "LIKE + FOLLOW FOR MORE", 1.15, hold=True)
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
            a = 1.0 if t >= 0.1 + i * 0.12 else 0.0  # pop-in, no half-faded figures (2026-10-25: faint numbers were OCR-misread by the safety scan)
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
    d.text((M, 1780), "REAL TRADES \u00b7 REAL MONEY \u00b7 NOT FINANCIAL ADVICE", font=mono(22), fill=MUT, anchor="ls")
    d.text((M, 1816), "@ROUNDINGERROR.CAPITAL", font=mono(22), fill=MUT, anchor="ls")
    return img

MUSIC = os.path.join(HERE, "music")
def mix_music(S, sfx_wav, total, workdir):
    """spec["music"] = a key of tools/music/manifest.json (one of our own Gemini songs). The song enters right after the teaser
    (1.0 s; at 0.6 s without a teaser) from its start_s, under the teaser hit and the meme sounds, then fades out at the end."""
    import json
    man = json.load(open(os.path.join(MUSIC, "manifest.json")))[S["music"]]
    enter = (COLD_F if S.get("cold_open") else COVER_F) / FPS
    start = S.get("music_start", man["start_s"]); out = sfx_wav[:-4] + "_mix.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", sfx_wav, "-ss", str(start), "-i", os.path.join(MUSIC, S["music"] + ".mp3"),
        "-filter_complex", f"[1:a]atrim=0:{total - enter:.2f},afade=t=in:d=0.08,afade=t=out:st={max(0, total - enter - 1.2):.2f}:d=1.2,volume=0.85,adelay={int(enter*1000)}|{int(enter*1000)}[m];"
        f"[0:a][m]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]", "-map", "[a]", "-ar", "44100", out], check=True)
    return out

def nfa(img):
    """'NOT FINANCIAL ADVICE' on every frame of every video (the boss, 2026-10-26), bottom centre, below the safe footer."""
    d = ImageDraw.Draw(img); f = mono(26, True); t = "NOT FINANCIAL ADVICE"
    w = d.textlength(t, font=f); d.rectangle([W // 2 - w / 2 - 14, 1846, W // 2 + w / 2 + 14, 1886], fill="#000000")
    d.text((W // 2, 1876), t, font=f, fill="#F2F2EE", anchor="ms"); return img

def build(S, out, cover_jpg, variant="a", workdir="/tmp"):
    content = S["end"]; total = ((COLD_F if S.get("cold_open") else COVER_F) + INTRO_F) / FPS + content + (LOOP_F / FPS if S.get("loop") else OUTRO_S)
    wav = os.path.join(workdir, os.path.basename(out) + ".wav")
    BEAT.make(wav, total + 0.3, S["bpm"], S["root"], S["seed"], S["mel"], groove=not S.get("music"), cold=(COLD_F - COVER_F) / FPS if S.get("cold_open") else 0.0, sfx=meme_sfx(S, ((COLD_F if S.get("cold_open") else COVER_F) + INTRO_F) / FPS))
    if S.get("music"): wav = mix_music(S, wav, total + 0.3, workdir)
    pts = chart_pts(S["chart"], S["seed"]); cover = Image.open(cover_jpg).convert("RGB").resize((W, H))
    hov = S.get("b", {}).get("hook") if variant == "b" else None
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "20",
        "-c:a", "aac", "-b:a", "160k", "-af", "adelay=33|33,loudnorm=I=-14:TP=-1.5", "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    cb = cover.tobytes()
    if S.get("cold_open"):
        for fr in range(COLD_F): p.stdin.write(nfa(cold_open_frame(S, fr, cover, pts).copy()).tobytes())
    else:
        for _ in range(COVER_F): p.stdin.write(cb)
    for fr in range(INTRO_F): p.stdin.write(nfa(intro_hook_frame(S, fr, pts)).tobytes())
    for i in range(int(content * FPS)): p.stdin.write(nfa(scene_frame(S, i / FPS, hov)).tobytes())
    if S.get("loop"):
        # LOOP variant (A/B "loop", 2026-10-22): no end card; the last 0.4 s crossfades back into the cover,
        # so the replay starts on the exact frame the viewer just saw.
        last = scene_frame(S, content - 1 / FPS, hov)
        for i in range(LOOP_F): p.stdin.write(nfa(Image.blend(last, cover, (i + 1) / LOOP_F)).tobytes())
    else:
        for i in range(int(OUTRO_S * FPS)): p.stdin.write(nfa(outro_frame(S, i / FPS)).tobytes())
    p.stdin.close(); p.wait(); os.remove(wav); return out

if __name__ == "__main__":
    import importlib.util
    spec = importlib.util.spec_from_file_location("spec", sys.argv[1]); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    print(build(m.SPEC, sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else "a"))
