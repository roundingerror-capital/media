# "It's about the facts" (the boss 2026-11-02): Penny tries to render a hyper-realistic 5K Theo; the team stages an intervention.
# Concept video, evergreen, no fund figures (nothing to source from a sheet). Pokes fun at "AI that tries to look like real people":
# our mascots stay 64 px and the numbers stay real. The "5K render" is a joke render: our own pixel Theo blown up with bicubic
# blur, bloom and a lens flare. Drop an AI-generated image (never a real person) at render_theo.png next to this file to use it instead.
import os, math, random, sys
HERE = os.path.dirname(os.path.abspath(__file__)); TOOLS = os.path.join(HERE, "..", "..", "tools"); sys.path.insert(0, TOOLS)
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import daily, rigs
from make_reel import W, H, archivo, mono, fade, fit
M, SAFE_R, BASE = daily.M, daily.SAFE_R, daily.BASE
INK = "#F2F2EE"; LIME = "#C8F03C"; RED = "#FF6B5B"; OR = "#FF8A5B"
RENDER_IMG = os.path.join(HERE, "render_theo.png")

def _theo_render():
    """The 'hyper-realistic' Theo: the real 64 px sprite upscaled with BICUBIC (smooth = 'realistic'), warm grade, bloom, grain."""
    if os.path.exists(RENDER_IMG): return Image.open(RENDER_IMG).convert("RGBA")
    s = daily.SP["theo"].copy(); k = 11
    big = s.resize((s.width * k, s.height * k), Image.BICUBIC)
    rgb = Image.new("RGB", big.size, (16, 14, 12)); rgb.paste(big, (0, 0), big)
    rgb = ImageEnhance.Color(rgb).enhance(1.35); rgb = ImageEnhance.Contrast(rgb).enhance(1.15)
    glow = rgb.filter(ImageFilter.GaussianBlur(18)); rgb = Image.blend(rgb, glow, 0.35)
    out = Image.new("RGBA", big.size); out.paste(rgb, (0, 0), big.filter(ImageFilter.GaussianBlur(1.2)).split()[3])
    return out

_R = {}
def render_panel(img, d, u, y):
    """Slide 1: the finished render in a cinema frame with RTX badges, a lens flare sweep and film grain."""
    x0, x1 = M, W - M; top = y + 20; h = 720; bot = top + h
    d.rounded_rectangle([x0, top, x1, bot], radius=22, fill=(8, 8, 10)); d.rounded_rectangle([x0, top, x1, bot], radius=22, outline=(60, 60, 64), width=3)
    if "im" not in _R: _R["im"] = _theo_render()
    im = _R["im"]
    if os.path.exists(RENDER_IMG):   # the AI image fills the frame (cover-crop), slow push-in like a movie still
        z = 1.0 + 0.06 * min(1, u / 5.0); W0, H0 = x1 - x0, h
        bg = im.resize((int(im.width * max(W0 / im.width, H0 / im.height)), int(im.height * max(W0 / im.width, H0 / im.height))), Image.BICUBIC)
        bg = bg.crop((bg.width // 2 - W0 // 2, bg.height // 2 - H0 // 2, bg.width // 2 + W0 // 2, bg.height // 2 + H0 // 2)).filter(ImageFilter.GaussianBlur(24))
        bg = Image.blend(bg, Image.new("RGBA", bg.size, (0, 0, 0, 255)), 0.45)
        fg = im.resize((int(im.width * H0 / im.height * z), int(H0 * z)), Image.BICUBIC)
        fg = fg.crop((fg.width // 2 - min(fg.width, W0) // 2, fg.height // 2 - H0 // 2, fg.width // 2 + min(fg.width, W0) // 2, fg.height // 2 + H0 // 2))
        bg.paste(fg, (W0 // 2 - fg.width // 2, 0), fg); im = bg
        mask = Image.new("L", im.size, 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=22, fill=255); im.putalpha(mask)
        px, py = x0, top
    else:
        sc = min((x1 - x0 - 80) / im.width, (h - 120) / im.height); im = im.resize((int(im.width * sc), int(im.height * sc)), Image.BICUBIC)
        px, py = (x0 + x1) // 2 - im.width // 2, top + 60
    a = min(1, u / 0.5)
    tmp = Image.new("RGBA", img.size); tmp.paste(im, (px, py), im)
    if a < 1: tmp.putalpha(tmp.split()[3].point(lambda v: int(v * a)))
    img.alpha_composite(tmp) if img.mode == "RGBA" else img.paste(tmp, (0, 0), tmp)
    d = ImageDraw.Draw(img)
    # lens flare sweep
    fx = x0 + (x1 - x0) * ((u * 0.45) % 1.2);
    for r, al in ((160, 18), (90, 34), (30, 90)):
        fl = Image.new("RGBA", (r * 2, r * 2)); ImageDraw.Draw(fl).ellipse([0, 0, r * 2 - 1, r * 2 - 1], fill=(255, 240, 200, al))
        img.paste(fl, (int(fx) - r, top + 140 - r), fl)
    d = ImageDraw.Draw(img)
    # film grain
    rnd = random.Random(int(u * 30))
    for _ in range(900):
        gx, gy = rnd.randint(x0 + 4, x1 - 4), rnd.randint(top + 4, bot - 4); d.point((gx, gy), fill=(255, 255, 255) if rnd.random() < 0.5 else (0, 0, 0))
    for i, b in enumerate(["5K", "RTX ON", "RAY TRACED", "HDR"]):
        bx = x0 + 24 + i * 200; d.rounded_rectangle([bx, top + 70, bx + 180, top + 116], radius=8, fill=LIME if i == 0 else (40, 40, 44))
        d.text((bx + 90, top + 102), b, font=mono(26, True), fill="#000000" if i == 0 else INK, anchor="ms")
    d.text((x1 - 24, top + 48), "THEO_FINAL_v12.blend", font=mono(24), fill=(140, 140, 150), anchor="rs")
    return bot + 20

def progress_panel(img, d, u, y):
    """Slide 0: a render progress window. 0 → DONE over 4 s, with a spinning 'rendering' wheel and fake pass names (no digits)."""
    x0, x1 = M, W - M; top = y + 30; bot = top + 520
    d.rounded_rectangle([x0, top, x1, bot], radius=18, fill=(22, 22, 26)); d.rectangle([x0, top, x1, top + 54], fill=(44, 44, 50))
    for i, c in enumerate(((255, 95, 86), (255, 189, 46), (39, 201, 63))): d.ellipse([x0 + 18 + i * 28, top + 17, x0 + 38 + i * 28, top + 37], fill=c)
    d.text(((x0 + x1) // 2, top + 38), "RENDER · THEO · ULTRA", font=mono(26, True), fill=INK, anchor="ms")
    k = min(1, u / 4.0); k = 1 - (1 - k) ** 2
    passes = ["loading fur shader…", "tracing rays…", "subsurface scattering…", "denoising…", "adding lens flare…", "DONE."]
    d.text((x0 + 36, top + 120), passes[min(5, int(k * 5.999))], font=mono(32), fill=LIME if k >= 1 else INK, anchor="ls")
    d.rounded_rectangle([x0 + 36, top + 160, x1 - 36, top + 220], radius=12, fill=(40, 40, 46))
    d.rounded_rectangle([x0 + 36, top + 160, x0 + 36 + int((x1 - x0 - 72) * k), top + 220], radius=12, fill=LIME)
    d.text((x0 + 36, top + 290), "ETA: " + ("now" if k >= 1 else "forever"), font=mono(30), fill=INK, anchor="ls")
    d.text((x0 + 36, top + 350), "QUALITY: unnecessary", font=mono(30), fill=INK, anchor="ls")
    d.text((x0 + 36, top + 410), "FACTS ADDED: none", font=mono(30), fill=RED, anchor="ls")
    # spinner
    cx, cy = x1 - 110, top + 330; ang = u * 300
    for i in range(8):
        a = math.radians(ang + i * 45); col = int(255 * (i + 1) / 8)
        d.ellipse([cx + 44 * math.cos(a) - 8, cy + 44 * math.sin(a) - 8, cx + 44 * math.cos(a) + 8, cy + 44 * math.sin(a) + 8], fill=(col, col, col))
    return bot + 20

WALK = [("ada", 0.0), ("kit", 0.5), ("roz", 1.0)]   # who walks in, and when (seconds after the slide starts)
SAY = [(2.4, 3.9, "ada", "Group hug? No. Group FACTS."), (5.6, 6.4, "roz", "Noted. Carefully.")]
def intervention(img, d, u, y):
    """Slide 2: Ada, Kit and Roz walk in from the right (V2.03 walk rigs, whole-number scale, mirrored) and stop in a line."""
    k = 5; stops = [980, 790, 600]
    for i, (ch, t0) in enumerate(WALK):
        if u < t0: continue
        tw = u - t0; x = max(stops[i], int(W + 100 - 420 * tw)); moving = x > stops[i]
        fr = rigs.frame(ch, "walk" if moving else "idle", u, k=k, flip=True)
        d.ellipse([x - 50, BASE - 8, x + 50, BASE + 16], fill="#1a1a1a"); img.paste(fr, (x - fr.width // 2, BASE - fr.height), fr)
        for a, b, who, ln in SAY:
            if who == ch and a <= u < b: daily.bubble(d, x, BASE - fr.height - 150, ln)
    return y

SLAMS = [(0.0, "IT'S ABOUT", "THE FACTS."), (1.6, "ALWAYS", "FACTS."), (2.5, "NEVER", "HYPE."), (3.4, "VERIFY.", ""), (4.0, "DOUBLE-CHECK.", ""), (4.6, "TRIPLE-CHECK.", ""), (5.4, "NUMBERS,", "NOT FLUFF.")]
def explosion(img, d, u, y):
    """Slide 4: the slam text. Each line punches in big (scale from 1.6 → 1.0 in 0.15 s), a white flash on impact, a shake for 0.25 s."""
    cur = max(i for i, s in enumerate(SLAMS) if u >= s[0]); t0, a, b = SLAMS[cur]; v = u - t0
    if v < 0.08: d.rectangle([0, 0, W, H], fill=(255, 255, 255))
    sc = 1.6 - 0.6 * min(1, v / 0.15); sh = random.Random(int(u * 60)).randint(-16, 16) if v < 0.25 else 0
    cy = 1000
    for j, txt in enumerate([a, b]):
        if not txt: continue
        f = fit(txt, int((W - 2 * M) / sc), 170, wdth=125, wght=900)
        d.text((W // 2 + sh, cy + j * 190 + sh // 2), txt, font=f, fill=LIME if (cur == 0 and j == 1) or cur in (1, 6) else INK, anchor="ms", stroke_width=10, stroke_fill="#000000")
    return y

SPEC = dict(label="CONCEPT", end=29.5, bpm=132, root=49.0, seed=1105, mel=3, chart="zigzag", music="hold_to_expiry_long", music_start=6.0,
 hook="<< IT'S ABOUT THE FACTS.", foot="RUN BY AN AI · REAL MONEY · NOT ADVICE", end_char="penny",
 bg=os.path.normpath(os.path.join(TOOLS, "..", "..", "work", "interest", "plate_standup_clean.png")), bg_dim=0.26, bg_blur=2.0,
 intro_cfg={"tagline": "And this is a public service announcement ↓"},
 scenes=[
  (0.0, 5.0, "PENNY'S SIDE PROJECT", [("Rendering Theo", INK), ("in 5K.", LIME)], ["Hyper-realistic. Ray traced. Forever."],
   [(0.5, 2.4, "penny", "Photoreal or nothing!", "jump"), (2.8, 4.8, "penny", "Almost there…", "point")], ["penny"], -1),
  (5.0, 10.5, "RENDER COMPLETE · 5K ULTRA", [("Behold.", INK), ("Theo.", LIME)], [],
   [(5.6, 7.6, "penny", "Look at the FUR.", "jump"), (7.9, 10.3, "theo", "…that's me?", "brow")], ["penny", "theo"], -1),
  (10.5, 17.0, "THE INTERVENTION", [("Penny.", INK), ("We've been through this.", LIME)], [],
   [(10.8, 12.6, "theo", "Penny. Sit down.", "brow"), (14.6, 16.0, "penny", "It's EIGHT K next time!", "jump")], ["penny", "theo"], -1),
  (17.0, 19.2, "ALL TOGETHER NOW", [("It's not about", INK), ("the graphics.", RED)], [],
   [(17.3, 19.0, "theo", "It's about…", "nod")], ["penny", "theo", "ada"], -1),
  (19.2, 25.6, "ALL TOGETHER NOW", [("Say it with us:", INK)], [], [], ["penny", "theo", "ada"], -1),
  (25.6, 29.5, "THE RULE", [("Cute mascots.", INK), ("Real numbers.", LIME)], ["Every figure from a fact sheet.", "Never a hype word. Never a face."],
   [(26.0, 28.0, "penny", "Fine. Sixty-four pixels it is.", "point"), (28.2, 29.4, "theo", "Plenty.", "nod")], ["penny", "theo", "ada"], 0),
 ],
 charts={0: {"draw": progress_panel}, 1: {"draw": render_panel}, 2: {"draw": intervention}, 4: {"draw": explosion}},
 cast_x={2: [0.16, 0.36], 1: [0.25, 0.75]}, cast_h={1: 230, 2: 330, 4: 330},
 memes=[{"t": 0.3, "dur": 2.0, "kind": "pov", "text": "POV: Penny found the render button"},
        {"t": 7.9, "dur": 1.4, "kind": "zoom", "text": "…THAT'S ME?", "y": 330},
        {"t": 19.2, "dur": 0.9, "kind": "zoom"},
        {"t": 24.6, "dur": 1.0, "kind": "zoom"},
        {"t": 28.2, "dur": 1.3, "kind": "shades", "who": "theo"}])
