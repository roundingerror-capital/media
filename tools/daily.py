"""Daily post builder v2 (Penny, locked 2026-10-19 standard).
Cover held 1.0 s (frames 0-29, so TikTok's grid cover is the post's own cover), then the AI TRADING BOT flash-card intro (2.5 s, black, lime chart),
then scenes with big animated characters and an original beat (tools/beat.py).
Usage (from a spec module): build(spec, out_mp4, cover_jpg, variant="a"|"b")
A spec may define "b" overrides: {"hook": [...heads...]} replaces scene 1's headline.
No numbers here: every figure lives in the spec and must be on a Theo fact sheet."""
import re, os, sys, math, random, subprocess, colorsys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
from make_reel import W, H, FPS, archivo, mono, fit, fade, blend
import beat as BEAT
import explain as EXPLAIN
HERE = os.path.dirname(os.path.abspath(__file__))
M = 72; LIME = "#C8F03C"; INK = "#F2F2EE"; MUT = "#9A9A94"; LINE = "#262626"; DIM = (40, 48, 20)
HANDLE = "@roundingerror.capital"  # same handle on Instagram, TikTok and YouTube (Posts settings/channels)
NETS = ("INSTAGRAM", "TIKTOK", "YOUTUBE")
# SAFE LAYOUT (the boss 2026-10-31, measured from his Instagram / TikTok / YouTube phone screenshots): every word on screen sits
# inside this box, so no app header, caption, username or button column ever covers it. Characters and the office may run outside.
SAFE_T, SAFE_B = 270, 1470        # app header above, name + caption below
SAFE_L, SAFE_R = 60, 880          # right of 880 is the button column (from y 850 down); above 850 text may run to W - M
SAFE_Y = 850
CX = (M + SAFE_R) // 2            # centre line for text below SAFE_Y
EXPLAIN.XR = SAFE_R
EXPLAIN.SUBS = False
LOGOS = True  # END CARD STANDARD (the boss 2026-11-01, "until a major rebrand"): solid WHITE Instagram, TikTok and YouTube glyphs (logos.MONO) on black, lime handle. Never the full-colour app icons.
def follow_block(img, y):
    """End card only: FOLLOW @roundingerror.capital + the real Instagram / TikTok / YouTube logos (tools/logos.py),
    centred left of the button column. y = baseline of the handle line. Returns the bottom y."""
    import logos
    d = ImageDraw.Draw(img); hf = mono(40, True); lf = mono(26, True)
    lab = "FOLLOW "; lw = d.textlength(lab, font=lf); hw = d.textlength(HANDLE, font=hf); x = CX - (lw + hw) // 2
    d.text((x, y), lab, font=lf, fill=MUT, anchor="ls"); d.text((x + lw, y), HANDLE, font=hf, fill=LIME, anchor="ls")
    if not LOGOS: return y + 10  # handle only (Roz T-062 2026-10-31: TikTok / YouTube brand pages not yet recorded)
    s = 96; gap = 72; tx = CX - (3 * s + 2 * gap) // 2; ty = y + 60
    for n in NETS: img.paste(logos.logo(n, s), (tx, ty), logos.logo(n, s)); tx += s + gap
    return ty + s
def follow_bar(d, y, big=False):
    """The boss 2026-10-29: every video shows the full handle and where to follow us, so a clip that travels can be traced back.
    Network names as plain text tags (no platform logos). y = baseline of the handle line."""
    hf = mono(44 if big else 34, True); lf = mono(26 if big else 22, True); tf = mono(22 if big else 19, True)
    lab = "FOLLOW "; lw = d.textlength(lab, font=lf); hw = d.textlength(HANDLE, font=hf)
    x = (W - lw - hw) // 2 if big else M
    d.text((x, y), lab, font=lf, fill=MUT, anchor="ls"); d.text((x + lw, y), HANDLE, font=hf, fill=LIME, anchor="ls")
    pad, gap, ty = 12, 12, y + (22 if big else 18)
    ws = [d.textlength(n, font=tf) + 2 * pad for n in NETS]; tx = (W - sum(ws) - gap * 2) // 2 if big else M
    for n, w in zip(NETS, ws):
        d.rounded_rectangle([tx, ty, tx + w, ty + (40 if big else 34)], radius=8, outline=INK, width=2)
        d.text((tx + w / 2, ty + (29 if big else 25)), n, font=tf, fill=INK, anchor="ms"); tx += w + gap
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
SP = {n: Image.open(os.path.join(HERE, "sprites", f"{n}_sprite_1x.png")).convert("RGBA") for n in ("theo", "penny", "ada", "kit", "roz")}  # the five active staff (Ops employees E-0001..E-0005)
SP["ada"] = river_teal(SP["ada"])
# eye boxes on the 1x sprites (x0, y0, x1, y1 inclusive), lid colour sample, closed-line row
EYES = {"penny": ([(12, 20, 14, 23), (26, 20, 28, 23)], (8, 22), 22),
        "theo": ([(13, 13, 17, 17), (24, 13, 28, 17)], (12, 11), 16),
        "ada": ([(8, 10, 12, 15), (24, 10, 28, 15)], (9, 8), 13),
        "kit": ([(15, 8, 19, 13), (34, 8, 38, 13)], (24, 9), 11),
        "roz": ([(12, 10, 17, 16), (28, 10, 33, 16)], (10, 12), 13)}
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
    im = intro_frame(int(fr * INTRO_SRC / INTRO_F), pts, (S.get("intro_cfg") or {}).get("tagline")); d = ImageDraw.Draw(im); txt = hook_text(S)
    f = fit(txt, W - 2 * M, 96, wdth=110, wght=900); bb = d.textbbox((0, 0), txt, font=f)
    f = fit(txt, SAFE_R - M, 96, wdth=110, wght=900); bb = d.textbbox((0, 0), txt, font=f)
    y = SAFE_B - 20 - (bb[3] - bb[1]); d.rectangle([0, y - 40, W, SAFE_B], fill="#000000")
    d.text((M - bb[0], y - bb[1]), txt, font=f, fill=LIME)
    return im

def intro_frame(fr, pts, tagline=None):
    im = Image.new("RGB", (W, H), (0, 0, 0)); d = ImageDraw.Draw(im); rnd = random.Random(fr)
    n = max(2, min(len(pts), int(len(pts) * fr / 18) + 2)) if fr < 18 else len(pts)
    col = LIME if fr < 18 else DIM
    for k in range(1, n): d.line([pts[k - 1], pts[k]], fill=col, width=14 if fr < 18 else 10)
    if fr < 18:
        x, y = pts[n - 1]; d.ellipse([x - 18, y - 18, x + 18, y + 18], fill=LIME)
    if fr >= 18:
        k = fr - 18; sc = 1.0 + max(0, 0.35 * (1 - k / 6)); sh = (rnd.randint(-10, 10), rnd.randint(-10, 10)) if k < 7 else (0, 0)
        d.text((M, 330), "I'M AN", font=fit("I'M AN", W - 2 * M, 96, wdth=100, wght=900), fill=INK)
        y = 450
        for t, c, cap in (("AI", LIME, 260), ("TRADING", LIME, 170), ("BOT", INK, 210)):
            f = archivo(int(cap * 1.4 * sc), 125, 900); bb = d.textbbox((0, 0), t, font=f)
            if bb[2] - bb[0] > (SAFE_R - M) * sc:
                f = archivo(int(f.size * (SAFE_R - M) * sc / (bb[2] - bb[0])), 125, 900); bb = d.textbbox((0, 0), t, font=f)
            if bb[3] - bb[1] > cap * sc:
                f = archivo(int(f.size * cap * sc / (bb[3] - bb[1])), 125, 900); bb = d.textbbox((0, 0), t, font=f)
            w, h = bb[2] - bb[0], bb[3] - bb[1]
            d.text((CX - w // 2 - bb[0] + sh[0], y - bb[1] + sh[1]), t, font=f, fill=c); y += int(h / sc) + 34
        if fr >= 42:
            a = fade(fr / FPS, 42 / FPS, 48 / FPS); txt = tagline or "And this is what's going on ↓"
            d.text((M, y + 30), txt, font=fit(txt, SAFE_R - M, 72, wdth=100, wght=900), fill=blend(INK, a))
    return im

def bubble(d, xc, y, txt):
    f = mono(34, True); tw = int(f.getlength(txt)); bw, bh = tw + 48, 76
    bx = int(min(max(M, xc - bw / 2), SAFE_R - bw))
    d.rectangle([bx, y, bx + bw, y + bh], fill=INK); d.rectangle([bx + 4, y + 4, bx + bw - 5, y + bh - 5], outline="#1A1A1A", width=4)
    d.polygon([(xc - 14, y + bh), (xc + 14, y + bh), (xc, y + bh + 20)], fill=INK)
    d.text((bx + 24, y + 52), txt, font=f, fill="#000000", anchor="ls")

XS = {1: [0.5], 2: [0.3, 0.7], 3: [0.2, 0.5, 0.8]}
BLINK = {"penny": (2.7, 0.3), "theo": (3.6, 1.1), "ada": (2.2, 0.7), "kit": (3.1, 1.6), "roz": (4.2, 0.9)}
BASE = 1690

def char_layer(img, d, S, t, cast, lines, text_bottom):
    bpm = S["bpm"]; ph = t * bpm / 60
    hpx = S.get("_hpx") or (430 if len(cast) < 3 else 380)
    xs = S.get("_xs") or XS[len(cast)]   # per-scene placement override (earnings casting varies it per video)
    for i, n in enumerate(cast):
        xc = int(W * xs[i]); per, off = BLINK[n]
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
            xc = int(W * xs[cast.index(w)])
            y = max(text_bottom + 24, BASE - hpx - 150)
            bubble(d, xc, y, ln)

CTA_S = 3.5  # small CTA at the start of the story (the boss 2026-10-25: "cta at the beginning small and end big")
def _heart(d, x, y, r, col):
    d.ellipse([x - r, y - r, x, y], fill=col); d.ellipse([x, y - r, x + r, y], fill=col)
    d.polygon([(x - r, y - r * 0.45), (x + r, y - r * 0.45), (x, y + r * 0.9)], fill=col)
def button(img, x0, y0, x1, y1, fill=None, radius=None):
    """Shaded button (the boss 2026-10-31: the COMMENT BELOW button looked flat and as wide as its text).
    Soft drop shadow, vertical gradient (lighter top, deeper bottom), 4 px black outline, glossy top highlight. Returns img."""
    import numpy as np
    from PIL import ImageFilter
    fill = fill or LIME_T; r = radius if radius is not None else (y1 - y0) // 2
    w, h = int(x1 - x0), int(y1 - y0)
    if w <= 0 or h <= 0: return img
    base = img.convert("RGBA")
    sh = Image.new("RGBA", base.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([x0 + 6, y0 + 14, x1 + 6, y1 + 14], radius=r, fill=(0, 0, 0, 170))
    base = Image.alpha_composite(base, sh.filter(ImageFilter.GaussianBlur(14)))
    top = np.array([min(255, c * 1.18 + 20) for c in fill]); bot = np.array([c * 0.72 for c in fill])
    g = np.linspace(0, 1, h)[:, None, None]; grad = (top * (1 - g) + bot * g).astype("uint8").repeat(w, 1)
    mask = Image.new("L", (w, h), 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], radius=r, fill=255)
    base.paste(Image.fromarray(grad, "RGB"), (int(x0), int(y0)), mask)
    hl = Image.new("RGBA", base.size, (0, 0, 0, 0)); hd = ImageDraw.Draw(hl)
    hd.rounded_rectangle([x0 + r * 0.45, y0 + 6, x1 - r * 0.45, y0 + h * 0.42], radius=max(4, int(r * 0.6)), fill=(255, 255, 255, 70))
    base = Image.alpha_composite(base, hl)
    ImageDraw.Draw(base).rounded_rectangle([x0, y0, x1, y1], radius=r, outline=(0, 0, 0, 255), width=4)
    return base.convert("RGB")

def cta_pill(img, u, text="LIKE + FOLLOW", scale=1.0, hold=False, y=None, dur=CTA_S, xr=None):
    """Call to action pill: slides in, pulses twice, slides out after `dur` s (stays if hold). u = seconds since it appeared.
    Shaded button with padding well past the text (about one text-height on each side)."""
    if u < 0 or (not hold and u > dur): return img
    d = ImageDraw.Draw(img); f = archivo(int(40 * scale), 110, 900)
    tw = d.textlength(text, font=f); r = int(14 * scale); h = int(72 * scale); pad = int(h * 0.62)
    w = int(tw + pad * 2 + r * 2 + int(14 * scale))
    k_in = min(1, u / 0.25); k_out = 0 if hold else max(0, (u - (dur - 0.3)) / 0.3)
    off = int((1 - (1 - (1 - k_in) ** 3)) * (w + M)) + int(k_out ** 2 * (w + M))
    pulse = 1 + 0.06 * max(0, math.sin(math.pi * min(1, max(0, (u - 0.6) / 0.3)))) + 0.06 * max(0, math.sin(math.pi * min(1, max(0, (u - 1.6) / 0.3))))
    w2, h2 = int(w * pulse), int(h * pulse)
    x1 = (xr or (W - M)) + off; x0 = x1 - w2; y0 = (y if y is not None else 176) - (h2 - h) // 2; y1 = y0 + h2
    img = button(img, x0, y0, x1, y1); d = ImageDraw.Draw(img)
    hx = x0 + (w2 - (tw + r * 2 + int(14 * scale))) // 2
    _heart(d, hx + r, (y0 + y1) // 2 - r // 4, r, "#000000")
    d.text((hx + r * 2 + int(14 * scale), (y0 + y1) // 2), text, font=f, fill="#000000", anchor="lm")
    return img

def cta_button(img, text, cx, y, size=64, arrow=True):
    """Big centred CTA (e.g. COMMENT BELOW + a down arrow): shaded button, padding one text-height each side. y = top."""
    d = ImageDraw.Draw(img)
    while size > 24:  # shrink until text + one text-height of padding each side fits the safe box (M .. SAFE_R)
        f = archivo(size, 125, 900); tw = d.textlength(text, font=f)
        if tw + size * 2 <= SAFE_R - M: break
        size -= 2
    h = int(size * 2.0); pad = int(size * 1.0); w = tw + pad * 2; cx = min(max(cx, M + w / 2), SAFE_R - w / 2)
    x0, x1 = cx - w / 2, cx + w / 2
    img = button(img, x0, y, x1, y + h, radius=int(h * 0.3)); d = ImageDraw.Draw(img)
    d.text((cx, y + h / 2), text, font=f, fill="#000000", anchor="mm")
    if arrow:
        a = y + h + 30; s = size / 64
        pts = [(cx - 70 * s, a), (cx + 70 * s, a), (cx + 70 * s, a + 80 * s), (cx + 140 * s, a + 80 * s), (cx, a + 210 * s), (cx - 140 * s, a + 80 * s), (cx - 70 * s, a + 80 * s)]
        img = button_poly(img, pts)
    return img

def button_poly(img, pts, fill=None):
    """Same shading for a polygon (the CTA arrow): shadow, flat fill with a lighter top half, black outline."""
    from PIL import ImageFilter
    fill = fill or LIME_T; base = img.convert("RGBA")
    sh = Image.new("RGBA", base.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).polygon([(x + 6, y + 14) for x, y in pts], fill=(0, 0, 0, 170))
    base = Image.alpha_composite(base, sh.filter(ImageFilter.GaussianBlur(12))); d = ImageDraw.Draw(base)
    d.polygon(pts, fill=tuple(int(c * 0.8) for c in fill) + (255,))
    ys = [p[1] for p in pts]; mid = min(ys) + (max(ys) - min(ys)) * 0.45
    top = Image.new("RGBA", base.size, (0, 0, 0, 0)); ImageDraw.Draw(top).polygon(pts, fill=tuple(min(255, int(c * 1.12 + 15)) for c in fill) + (255,))
    clip = Image.new("L", base.size, 0); ImageDraw.Draw(clip).rectangle([0, 0, base.width, mid], fill=255)
    base.paste(top, (0, 0), Image.composite(top.split()[3], Image.new("L", base.size, 0), clip))
    ImageDraw.Draw(base).polygon(pts, outline=(0, 0, 0, 255), width=4)
    return base.convert("RGB")

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
    big = co["big"]; pm = big.startswith("\u00b1"); num = big[1:] if pm else big   # a leading \u00b1 is drawn smaller, with a gap: OCR read "\u00b113.3%" as "413.3%" (2026-11-01)
    f = fit(num, int((W - 2 * M - (160 if pm else 0)) * min(1.0, sc / 1.6 + 0.4)), 400, wdth=125, wght=900)
    sw = 10; sf = "#000000" if win else "#FFFFFF"
    if pm:
        pf = archivo(int(f.size * .62), 125, 900); pw = d.textlength("\u00b1", font=pf); nw = d.textlength(num, font=f); x0 = W // 2 - (pw + 34 + nw) / 2
        d.text((x0, 720 - int(f.size * .14)), "\u00b1", font=pf, fill=col, anchor="ls", stroke_width=sw, stroke_fill=sf)
        d.text((x0 + pw + 34, 720), num, font=f, fill=col, anchor="ls", stroke_width=sw, stroke_fill=sf)
    else: d.text((W // 2, 720), big, font=f, fill=col, anchor="ms", stroke_width=sw, stroke_fill=sf)
    if co.get("line"): d.text((W // 2, 400), co["line"], font=fit(co["line"], W - 2 * M, 96, wdth=125, wght=900), fill=INK, anchor="ms")
    if u > 0.45:
        sh = co.get("shout", "WAIT, WHAT?!"); f2 = fit(sh, W - 2 * M, int(110 * (1 + max(0, .25 - (u - .45)))), wdth=125, wght=900)
        d.text((W // 2, 840), sh, font=f2, fill=INK, anchor="ms", stroke_width=6, stroke_fill="#000000")
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
        k = m["kind"]; my = m.get("y", 0)   # per-meme vertical offset (earnings chart slides move the band under the chart, 2026-11-02)
        if k == "pov":
            f = fit(m["text"], SAFE_R - M - 20, 64, wdth=100, wght=900); a = min(1, u / 0.12)
            d.rectangle([0, 900 + my, W, 1020 + my], fill=(255, 255, 255))
            d.text((CX, 982 + my), m["text"], font=f, fill="#000000", anchor="ms")
        elif k == "zoom":
            z = 1 + 0.07 * min(1, u / 0.12); cx, cy = (M + SAFE_R) // 2, H // 2  # small punch-in: a big zoom pushed the headline under the app header (2026-10-31)
            box = (int(cx - W / z / 2), int(cy - H / z / 2), int(cx + W / z / 2), int(cy + H / z / 2))
            im2 = img.crop(box).resize((W, H)); sh = random.Random(int(t * 30)).randint(-14, 14) if u < 0.4 else 0
            im2 = im2.transform(im2.size, Image.AFFINE, (1, 0, sh, 0, 1, sh // 2))
            g = Image.new("RGB", (W, H), (0, 0, 0)); im2 = Image.composite(g, im2, _vignette().point(lambda v: int(v * 0.8)))
            img.paste(im2); d = ImageDraw.Draw(img)
            if m.get("text"):
                f = fit(m["text"], SAFE_R - M - 20, 110, wdth=125, wght=900)
                d.text((CX, 1000 + my), m["text"], font=f, fill=(255, 255, 255), anchor="ms", stroke_width=8, stroke_fill="#000000")
        elif k == "twopanel":
            d.rectangle([0, 860 + my, W, 1120 + my], fill=(0, 0, 0))
            for i, (lab, val) in enumerate(((m["a"], m["a2"]), (m["b"], m["b2"]))):
                if u < i * 0.6: continue
                y = 950 + my + i * 120
                d.text((M, y), lab, font=archivo(52, 100, 900), fill=INK, anchor="ls")
                d.text((SAFE_R, y), val, font=archivo(64, 100, 900), fill=m.get("a2c", "#EB2626") if i == 0 else m.get("b2c", LIME), anchor="rs")
            if m.get("hypo"):   # lesson figures in a two-panel carry the same orange tag as the worked-example panels (Roz 2026-11-02)
                d.rectangle([SAFE_R - 280, 1066 + my, SAFE_R, 1110 + my], fill="#FF8A5B"); d.text((SAFE_R - 140, 1098 + my), "HYPOTHETICAL", font=mono(26, True), fill="#000000", anchor="ms")
        elif k == "freeze":
            g = img.convert("L").convert("RGB"); img.paste(Image.blend(g, Image.new("RGB", (W, H), (40, 30, 20)), 0.25)); d = ImageDraw.Draw(img)
            f = fit(m["text"], SAFE_R - M - 20, 84, wdth=110, wght=900)
            d.rectangle([0, 900 + my, W, 1040 + my], fill=(0, 0, 0)); d.text((CX, 995 + my), m["text"], font=f, fill=(255, 255, 255), anchor="ms")
    return img
def meme_sfx(S, offset):
    """(time, kind) list for the beat: boom on shades/zoom, scratch on freeze, pop on pov/twopanel. offset = seconds before the story starts."""
    out = []
    for m in S.get("memes", []):
        kk = {"shades": "boom", "zoom": "boom", "freeze": "scratch", "pov": "pop", "twopanel": "pop"}[m["kind"]]
        out.append((offset + m["t"], kk))
    return out
def pctlab(v):
    """+42% / \u22125.3%: integers stay whole, decimals keep one place (as written on the sheet)."""
    t = f"{int(v):+d}%" if float(v).is_integer() else f"{float(v):+.1f}%"
    return t.replace("-", "\u2212")

def chart_panel(d, vals, labels, y0, y1, note="", k=1.0, avg=None, title=""):
    """Bars of a series (e.g. next-day moves after each report). Every value must be on a Theo fact sheet.
    Redesign 2026-11-02 (the boss: "the black chart looks terrible"), per the dataviz rules: a dark card with a quiet border and a
    title, a recessive zero line, slim bars with rounded ends at the data side (anchored to the baseline), lime up / coral down,
    value labels in ink just past each bar end, dates under the plot, an optional dashed +/- average band, bars grow in (k 0..1)."""
    img = d._image; n = len(vals); lo = min(0, min(vals)); hi = max(0, max(vals)); rng = (hi - lo) or 1
    if avg: lo, hi = min(lo, -avg), max(hi, avg); rng = hi - lo
    px0, px1 = M - 20, SAFE_R + 20; top = y0 - (64 if title else 30); bot = y1 + (150 if note else 110)
    card = Image.new("RGBA", img.size, (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
    cd.rounded_rectangle([px0, top, px1, bot], radius=22, fill=(14, 16, 18, 238), outline=(46, 50, 56, 255), width=2)
    base = img.convert("RGBA"); base.alpha_composite(card); img.paste(base.convert("RGB")); d = ImageDraw.Draw(img)
    if title: d.text((M, top + 40), title + ("  ·  - - - average size" if avg else ""), font=mono(20, True), fill=MUT, anchor="ls")
    plot0, plot1 = y0 + 48, y1 - 20   # headroom: the tallest bar's label stays under the title
    Y = lambda v: plot0 + (hi - v) / rng * (plot1 - plot0)
    zero = Y(0); bw = (SAFE_R - M) / n
    if avg:   # dashed average band, recessive
        for yy in (Y(avg), Y(-avg)):
            for x in range(M, SAFE_R, 18): d.line([(x, yy), (x + 9, yy)], fill=(70, 74, 80), width=2)
    d.line([(M, zero), (SAFE_R, zero)], fill=(120, 124, 128), width=2)
    for i, (v, lab) in enumerate(zip(vals, labels)):
        ki = max(0.0, min(1.0, k * (n + 2) / n - i * .12 * k)) if k < 1 else 1.0
        ki = 1 - (1 - ki) ** 3
        cx = M + (i + .5) * bw; w2 = bw * .26; yv = zero + (Y(v) - zero) * ki
        col = LIME_T if v >= 0 else (255, 107, 91)
        if abs(yv - zero) >= 2:
            yt, yb = min(zero, yv), max(zero, yv); r = min(8, int((yb - yt) / 2))
            d.rounded_rectangle([cx - w2, yt, cx + w2, yb], radius=r, fill=col)
            if v >= 0: d.rectangle([cx - w2, yb - r, cx + w2, yb], fill=col)   # square at the baseline, round at the data end
            else: d.rectangle([cx - w2, yt, cx + w2, yt + r], fill=col)
        if ki >= .98:
            lab_v = pctlab(v).lstrip("+")   # up bars drop the "+" (OCR read "+2.9%" as "42.9%", 2026-11-01)
            ty = yv - 14 if v >= 0 else yv + 40
            d.text((cx, ty), lab_v, font=mono(30 if n <= 6 else 24, True), fill=INK, anchor="ms")
        d.text((cx, plot1 + 88), lab, font=mono(22), fill=MUT, anchor="ms")   # dates sit below the lowest value label
    if note: d.text((M, bot - 26), note, font=mono(20), fill=MUT, anchor="ls")
    return d

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

_BG = {}
def office_bg(S, path=None, t=0.0):
    """Office backdrop (HQ render, 2026-10-28 the boss: "use the office as a setup to tell our stories"): a 9:16 crop of the office,
    dimmed so white and lime text stays readable, cached per spec. spec["bg"] = png path, spec["bg_dim"] = 0..1 (default 0.42 brightness).
    spec["bg"] = "SCN-03" (2026-11-02): a looping pixel scene from tools/scenes.py, drawn fresh per loop frame, dimmed the same way, no blur."""
    from PIL import ImageEnhance, ImageFilter
    path = path or S["bg"]
    if isinstance(path, str) and path.startswith("SCN-"):
        import scenes
        fr, tk = scenes.frames_1x(path) if path not in scenes._CACHE else scenes._CACHE[path]; scenes._CACHE[path] = (fr, tk)
        total = sum(tk); u = (t * 10) % total; acc = 0; idx = len(fr) - 1
        for i, kk in enumerate(tk):
            acc += kk
            if u < acc: idx = i; break
        k = (path, idx, S.get("bg_dim", 0.42))
        if k not in _BG: _BG[k] = ImageEnhance.Brightness(fr[idx].resize((W, H), Image.NEAREST).convert("RGB")).enhance(k[2])
        return _BG[k].copy()
    k = (path, S.get("bg_dim", 0.42))
    if k not in _BG:
        im = Image.open(path).convert("RGB"); r = max(W / im.width, H / im.height)
        im = im.resize((int(im.width * r + 0.5), int(im.height * r + 0.5)), Image.NEAREST)
        x0 = (im.width - W) // 2; y0 = (im.height - H) // 2; im = im.crop((x0, y0, x0 + W, y0 + H))
        im = ImageEnhance.Brightness(im.filter(ImageFilter.GaussianBlur(S.get("bg_blur", 1.5)))).enhance(k[1])
        _BG[k] = im
    return _BG[k].copy()

def scene_frame(S, t, heads_override=None):
    SHADES_ON.clear()
    for m in S.get("memes", []):
        if m["kind"] == "shades" and m["t"] <= t <= m["t"] + m.get("dur", 1.6): SHADES_ON[m.get("who", "theo")] = min(1, (t - m["t"]) / 0.3)
    sc = S["scenes"]; k = max(i for i, s in enumerate(sc) if t >= s[0] or i == 0)
    bgp = (S.get("bgs") or {}).get(k) or S.get("bg")
    img = office_bg(S, bgp, t) if bgp else Image.new("RGB", (W, H), "#000000"); d = ImageDraw.Draw(img)
    sc = S["scenes"]; k = max(i for i, s in enumerate(sc) if t >= s[0] or i == 0)
    t0, t1, kick, heads, body, lines, cast, hl = sc[k]
    if k == 0 and heads_override: heads = heads_override
    a = 1.0 if k == 0 else fade(t, t0, t0 + 0.3)
    cen = S.get("align") == "center"                       # recipe placement (earnings, 2026-11-05): same text band, centred or left
    def TX(y_, w_): return ((M + w_) // 2, "ms") if cen else (M, "ls")
    xk, ak = M, "ls"; d.text((xk, 352), kick, font=mono(30, True), fill=blend(LIME, a), anchor=ak)
    f = min((fit(h, W - 2 * M - 8, 160 if len(heads) == 1 else 132, wdth=110, wght=900) for h, _ in heads), key=lambda q: q.size)
    y = 362 + int(f.size * 1.05)
    for i, (h, c) in enumerate(heads):
        ha = a * fade(t, t0 + i * 0.12, t0 + 0.3 + i * 0.12) if k else (1.0 if t > 0.25 else fade(t, i * 0.06, 0.2 + i * 0.06))
        xh, ah = TX(y, W - M); d.text((xh, y), h, font=f, fill=blend(c, ha), anchor=ah); y += int(f.size * 1.05)
    y += 30
    for i, ln in enumerate(body):
        ba = a * fade(t, t0 + 0.5 + i * 0.3, t0 + 0.8 + i * 0.3); wr = W - M if y < SAFE_Y else SAFE_R
        xb, ab = TX(y, wr); d.text((xb, y), ln, font=fit_mono(ln, wr - M, 38), fill=blend(LIME if i == hl else INK, ba), anchor=ab); y += 62
    tw = (S.get("threeway") or {}).get(k)
    if tw:
        threeway_panel(d, tw["cards"], y + 10, tw.get("quote", "")); y += 660
    ch = (S.get("charts") or {}).get(k)
    if ch:
        if ch.get("draw"): y = ch["draw"](img, d, t - t0, y); d = ImageDraw.Draw(img)   # a spec-supplied chart style (tools/earnings.py chart styles)
        else: d = chart_panel(d, ch["vals"], ch["labels"], y + 110, y + 480, ch.get("note", ""), k=fade(t, t0 + .3, t0 + 1.5), avg=ch.get("avg"), title=ch.get("title", "")); y += 660
    vz = (S.get("visuals") or {}).get(k)
    S["_hpx"] = None
    if vz:  # worked example (explain.py): characters shrink to the bottom band so the steps have room
        y = EXPLAIN.draw(d, vz, t - t0, y); S["_hpx"] = 250
    S["_xs"] = (S.get("cast_x") or {}).get(k)
    if (S.get("cast_h") or {}).get(k) and not vz: S["_hpx"] = S["cast_h"][k]
    char_layer(img, d, S, t, cast, lines, y - 20)
    S["_hpx"] = None; S["_xs"] = None
    # safe layout (2026-10-31): no header, no follow bar, no top-right pill on story frames; the apps already show our name + Follow there
    img = meme_layer(img, S, t)
    # outro-off videos have no end card: a bigger CTA holds through the last 2.5 s. Loops never get it (T-069: an end pill says "this is the end";
    # a loop's CTA lives in the caption and the small start pill).
    if S.get("outro") is False and not S.get("loop") and S.get("end") and t > S["end"] - 2.5:
        img = cta_pill(img, t - (S["end"] - 2.5), "LIKE + FOLLOW FOR MORE", 1.0, hold=True, y=1360, xr=SAFE_R)
    return img

LOOP_F = 12  # 0.4 s crossfade to the cover in the loop variant
OUTRO_S = 3.5  # end card (the boss 2026-10-21): "like and follow for more updates" + our open positions
END_CAST = {"theo": "nod", "penny": "point", "ada": "thumbs"}  # every character this file can animate; add Roz/Kit once they have video sprites (T-067)
def end_char(S):
    """Who hosts the end card: spec["end_char"] if set, else one pick from END_CAST that stays the same for a day (seeded by positions_asof)."""
    import random
    c = S.get("end_char")
    return c if c in END_CAST else random.Random(S.get("positions_asof") or S.get("seed") or "").choice(sorted(END_CAST))

def outro_frame(S, t):
    """End card. Positions come ONLY from the spec's "positions" list, copied from a Theo fact sheet's
    open_legs: [(ticker, "$100 put", "exp 10/30", "out of the money"), ...]. Never account value, cash,
    account numbers or a broker screenshot (Rules: no fund size or personal data in public).
    1-5 positions: big rows. 6-10: compact rows (ITM / OTM). More than 10: the first 9 plus "+N MORE", so a leg never silently vanishes (T-067)."""
    img = Image.new("RGB", (W, H), "#000000"); d = ImageDraw.Draw(img)
    ec = S.get("endcard") or {}  # Posts settings/endcard (the boss 2026-10-29: edit the end card in one place)
    pos = list((S.get("positions") or []) if ec.get("show_positions", True) else []); y = 352
    if len(pos) > 10: pos = pos[:9] + [("+%d MORE" % (len(pos) - 9), "", "", "")]
    big = len(pos) <= 5; rh = 110 if big else 72
    if pos:
        d.text((M, y), "OUR OPEN POSITIONS" + (" \u00b7 " + S["positions_asof"] if S.get("positions_asof") else ""), font=mono(30, True), fill=LIME, anchor="ls"); y += 30
        for i, row in enumerate(pos):
            a = 1.0 if t >= 0.1 + i * (0.12 if big else 0.06) else 0.0  # pop-in, no half-faded figures (OCR)
            col = LIME if "out of" in row[3] or "worthless" in row[3] else "#FF8A5B"
            d.rectangle([M, y, SAFE_R, y + rh - 18], outline=blend(LINE, a), width=3)
            if big:
                d.text((M + 24, y + 62), row[0], font=archivo(48, 110, 900), fill=blend(INK, a), anchor="ls")
                d.text((M + 230, y + 42), row[1] + "  " + row[2], font=mono(30, True), fill=blend(INK, a), anchor="ls")
                d.text((M + 230, y + 78), row[3].upper(), font=mono(24, True), fill=blend(col, a), anchor="ls")
            else:
                d.text((M + 20, y + 40), row[0], font=archivo(36, 110, 900), fill=blend(INK, a), anchor="ls")
                if row[1]:
                    d.text((M + 170, y + 38), row[1] + "  " + row[2], font=mono(24, True), fill=blend(INK, a), anchor="ls")
                    d.text((SAFE_R - 20, y + 38), "OTM" if col == LIME else "ITM", font=mono(24, True), fill=blend(col, a), anchor="rs")
            y += rh
        y += 40 if big else 16
    else:
        y = 560
    k = max(0.0, t - 0.3); sc = 1.0 + max(0, 0.3 * (1 - k / 0.25)) if t > 0.3 else 0
    if t > 0.3:
        for txt, c in ((ec.get("line1") or "LIKE + FOLLOW", LIME), (ec.get("line2") or "FOR MORE UPDATES", INK)):
            f = fit(txt, int((SAFE_R - M) * min(sc, 1.15)), (160 if not pos else 120 if big else 80), wdth=125, wght=900)
            bb = d.textbbox((0, 0), txt, font=f)
            d.text((CX - (bb[2] - bb[0]) // 2 - bb[0], y - bb[1]), txt, font=f, fill=c); y += bb[3] - bb[1] + (26 if big else 14)
        follow_block(img, y + (60 if big else 44)); d = ImageDraw.Draw(img)
    who = end_char(S)
    S["_hpx"] = None if len(pos) < 4 else (300 if big else 240)
    char_layer(img, d, S, 30 + t, [who], [(30.0, 40.0, who, "", END_CAST[who])] if t > 0.3 else [], 10**6)
    S["_hpx"] = None
    return img

MUSIC = os.path.join(HERE, "music")
def mix_music(S, sfx_wav, total, workdir):
    """spec["music"] = a song key (one of our own Gemini songs, Database · Posts songs/<key>). The song enters right after the teaser
    (1.0 s; at 0.6 s without a teaser) from its start_s, under the teaser hit and the meme sounds, then fades out at the end.
    The track is private (T-088): tools/songs.py fetches it from the Posts copy into the gitignored tools/music/ cache."""
    import songs
    man = songs.meta(S["music"]); track = songs.path(S["music"])
    loop = bool(S.get("loop"))  # loops: song from frame 1 and no fade-out (build_loop cross-fades the tail into the head)
    enter = 0.0 if loop else (COLD_F if S.get("cold_open") else COVER_F) / FPS
    start = S.get("music_start", man["start_s"]); out = sfx_wav[:-4] + "_mix.wav"
    fades = "afade=t=in:d=0.08" + ("" if loop else f",afade=t=out:st={max(0, total - enter - 1.2):.2f}:d=1.2")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", sfx_wav, "-ss", str(start), "-i", track,
        "-filter_complex", f"[1:a]atrim=0:{total - enter:.2f},{fades},volume=0.85,adelay={int(enter*1000)}|{int(enter*1000)}[m];"
        f"[0:a][m]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]", "-map", "[a]", "-ar", "44100", out], check=True)
    return out

def nfa(img):
    """'NOT FINANCIAL ADVICE' on every frame of every video (the boss, 2026-10-26), once, small, at the top-left of the safe box
    (2026-10-31: it used to sit under the apps' captions). Scenes start their kicker below it at y 352."""
    d = ImageDraw.Draw(img); f = mono(24, True); t = "NOT FINANCIAL ADVICE"
    w = d.textlength(t, font=f); d.rectangle([M - 10, SAFE_T + 4, M + w + 10, SAFE_T + 44], fill="#000000")
    d.text((M, SAFE_T + 34), t, font=f, fill="#F2F2EE", anchor="ls"); return img
def fit_mono(txt, width, size, bold=True):
    f = mono(size, bold)
    while size > 22 and f.getlength(txt) > width: size -= 2; f = mono(size, bold)
    return f

def build(S, out, cover_jpg, variant="a", workdir="/tmp"):
    # Per-post switches (Posts card intro/outro, the boss 2026-10-29): spec["intro"] False skips the AI TRADING BOT card,
    # spec["outro"] False skips the end card (a big LIKE + FOLLOW pill holds over the last 2.5 s instead). Default: both on.
    if S.get("loop"):  # T-069: a real loop has no beginning and no end (no cover, teaser, intro card or end pill)
        return build_loop(S, out, cover_jpg, variant, workdir)
    IF = INTRO_F if S.get("intro", True) is not False else 0
    tail = LOOP_F / FPS if S.get("loop") else (OUTRO_S if S.get("outro", True) is not False else 0.0)
    content = S["end"]; total = ((COLD_F if S.get("cold_open") else COVER_F) + IF) / FPS + content + tail
    wav = os.path.join(workdir, os.path.basename(out) + ".wav")
    BEAT.make(wav, total + 0.3, S["bpm"], S["root"], S["seed"], S["mel"], groove=not S.get("music"), cold=(COLD_F - COVER_F) / FPS if S.get("cold_open") else 0.0, sfx=meme_sfx(S, ((COLD_F if S.get("cold_open") else COVER_F) + IF) / FPS))
    if S.get("music"): wav = mix_music(S, wav, total + 0.3, workdir)
    pts = chart_pts(S["chart"], S["seed"]); cover = Image.open(cover_jpg).convert("RGB").resize((W, H))
    hov = S.get("b", {}).get("hook") if variant == "b" else None
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "20",
        "-c:a", "aac", "-b:a", "160k", "-af", "adelay=33|33,loudnorm=I=-14:TP=-1.5", "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    cb = cover.tobytes()
    if S.get("cold_open"):
        for fr in range(COLD_F): p.stdin.write((nfa(cold_open_frame(S, fr, cover, pts).copy()) if fr >= 3 else cover).tobytes())  # the cover carries its own NFA badge
    else:
        for _ in range(COVER_F): p.stdin.write(cb)
    for fr in range(IF): p.stdin.write(nfa(intro_hook_frame(S, fr, pts)).tobytes())
    for i in range(int(content * FPS)): p.stdin.write(nfa(scene_frame(S, i / FPS, hov)).tobytes())
    if S.get("loop"):
        # LOOP variant (A/B "loop", 2026-10-22): no end card; the last 0.4 s crossfades back into the cover,
        # so the replay starts on the exact frame the viewer just saw.
        last = scene_frame(S, content - 1 / FPS, hov)
        for i in range(LOOP_F): p.stdin.write(nfa(Image.blend(last, cover, (i + 1) / LOOP_F)).tobytes())
    elif S.get("outro", True) is not False:
        for i in range(int(OUTRO_S * FPS)): p.stdin.write(nfa(outro_frame(S, i / FPS)).tobytes())
    p.stdin.close(); p.wait(); os.remove(wav); return out

def _loop_wav(path, total, xf):
    """Make the audio loop: the file is cut to `total` s and its last `xf` s are cross-faded with its first `xf` s,
    so the end of the song runs straight into the start on replay."""
    import wave, numpy as np
    with wave.open(path) as w: ch, sw, sr = w.getnchannels(), w.getsampwidth(), w.getframerate(); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, ch).astype(np.float32)
    n = int(total * sr); k = int(xf * sr); a = a[:n + k] if len(a) >= n + k else np.pad(a, ((0, n + k - len(a)), (0, 0)))
    body = a[:n].copy(); r = np.linspace(0, 1, k)[:, None]
    body[n - k:n] = a[n - k:n] * (1 - r) + a[:k] * r  # tail fades into the head
    with wave.open(path, "wb") as w: w.setnchannels(ch); w.setsampwidth(sw); w.setframerate(sr); w.writeframes(np.clip(body, -32768, 32767).astype(np.int16).tobytes())
    return path

def build_loop(S, out, cover_jpg, variant="a", workdir="/tmp"):
    """LOOP variant (T-069, the boss 2026-10-28: "it has to end the same way it started"). Starts straight on the first story
    frame (no cover flash, teaser or intro card), runs a whole number of bars, then the last 0.4 s cross-fades picture AND
    music back into frame 1, so the replay is seamless. No end pill: the CTA lives in the caption and the small start pill.
    Write the script so the last line runs into the first (e.g. ends "...so when the bell rings," and restarts on "DING!").
    The custom cover still goes to every network as the thumbnail (publish.cover_url), so the video needn't start on it."""
    bar = 4 * 60.0 / S["bpm"]; content = max(bar, round(S["end"] / bar) * bar); xf = LOOP_F / FPS
    wav = os.path.join(workdir, os.path.basename(out) + ".wav")
    BEAT.make(wav, content + xf + 0.3, S["bpm"], S["root"], S["seed"], S["mel"], groove=not S.get("music"), cold=0.0, sfx=meme_sfx(S, 0.0))
    if S.get("music"): wav = mix_music(S, wav, content + xf + 0.3, workdir)
    _loop_wav(wav, content, xf)
    hov = S.get("b", {}).get("hook") if variant == "b" else None
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "20",
        "-c:a", "aac", "-b:a", "160k", "-af", "loudnorm=I=-14:TP=-1.5", "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    n = int(round(content * FPS)); first = nfa(scene_frame(S, 0.0, hov))
    for i in range(n):
        fr = nfa(scene_frame(S, min(i / FPS, S["end"] - 1 / FPS), hov))
        if i >= n - LOOP_F: fr = Image.blend(fr, first, (i - (n - LOOP_F) + 1) / (LOOP_F + 1))
        p.stdin.write(fr.tobytes())
    p.stdin.close(); p.wait(); os.remove(wav); return out

# NEW WAVE (the boss 2026-11-03): Kit's rigs, V3.01 rooms and rig covers for every video this file builds. NEW_WAVE=0 = old look.
if os.environ.get("NEW_WAVE", "1") != "0":
    import newwave; newwave.install(sys.modules[__name__])
    _scene_frame_old = scene_frame
    def scene_frame(S, t, heads_override=None):
        if not S.get("bg") and not S.get("bgs"): S["bg"] = S.get("room", newwave.DEFAULT_ROOM); S.setdefault("bg_dim", 0.34)
        return _scene_frame_old(S, t, heads_override)

if __name__ == "__main__":
    import importlib.util
    spec = importlib.util.spec_from_file_location("spec", sys.argv[1]); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    print(build(m.SPEC, sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else "a"))
