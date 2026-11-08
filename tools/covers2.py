"""Cover styles (the boss 2026-10-26: "all of our videos look the same from outside, text on top, random animal bottom right").
Six layouts that look different on a grid. Everything that matters stays inside the grid-safe zone (y 285-1635 at 1080x1920).
make(out, style, big, line="", kicker="", who=("theo",), tone="lime"|"red"|"paper", sub="")
Rule for the builder: no two of the last 6 covers share a style, and no two share a background colour in a row."""
import os, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
D = os.path.dirname(os.path.abspath(__file__)); F = D + "/fonts/"; SP = D + "/sprites/"
W, H = 1080, 1920; TOP, BOT = 285, 1635
SAFE_R = 880; CX = (72 + SAFE_R) // 2  # in-feed safe box (daily.py): below y 850 text stays left of the app buttons
LIME = (200, 240, 60); WHITE = (242, 242, 238); BLACK = (0, 0, 0); RED = (235, 38, 38); PAPER = (242, 240, 232); GREY = (154, 154, 148)
def arch(sz, wt=900, wd=125):
    f = ImageFont.truetype(F + "Archivo[wdth,wght].ttf", sz); f.set_variation_by_axes([wt, wd]); return f
def mono(sz): return ImageFont.truetype(F + "IBMPlexMono-SemiBold.ttf", sz)
def fitf(d, t, maxw, mx, wt=900, wd=125):
    s = mx
    while s > 20 and d.textlength(t, font=arch(s, wt, wd)) > maxw: s -= 4
    return arch(s, wt, wd)
def sprite(name, h):
    import newwave; im = newwave.sprite(name)      # Kit's rig, idle frame, trimmed (the old October sprites are never used, 2026-11-07)
    s = max(1, round(h / im.height)); return im.resize((im.width * s, im.height * s), Image.NEAREST)
def bigtext(d, xy, txt, maxw, mx, fill, anchor="ms", wt=900, wd=125, **kw):
    """The cover's BIG text. A number (any digit) is drawn scanner-readable, like the video teaser (the boss 2026-11-07:
    the publisher's OCR read "-8.7%" as "8.1%"/"1%" and "$230" as "$330" on wide heavy type): normal width, weight 700,
    an 18 px gap between characters, extra room after a leading sign, no outline. Words keep the old look."""
    if not any(c.isdigit() for c in txt):
        f = fitf(d, txt, maxw, mx, wt, wd); d.text(xy, txt, font=f, fill=fill, anchor=anchor, **kw); return
    GAP, SG = 18, 44
    mx = min(mx, fitf(d, txt, maxw, mx, wt, wd).size)          # never taller than the old look: layouts stay the same
    gaps = [GAP + (SG if i == 0 and c in "-\u2212+$\u00b1" else 0) for i, c in enumerate(txt[:-1])] + [0]
    s = mx
    while s > 20:
        f = arch(s, 700, 100); w = sum(d.textlength(c, font=f) for c in txt) + sum(gaps)
        if w <= maxw: break
        s -= 4
    x = xy[0] - (w / 2 if anchor[0] == "m" else w if anchor[0] == "r" else 0)
    for c, g in zip(txt, gaps): d.text((x, xy[1]), c, font=f, fill=fill, anchor="l" + anchor[1]); x += d.textlength(c, font=f) + g
def brand(d, col=WHITE):
    d.text((72, TOP + 50), "≈ Rounding Error", font=arch(44, 800, 100), fill=col)
def footer(d, col=GREY):
    d.text((72, BOT - 70), "AI TRADING BOT · REAL MONEY", font=mono(30), fill=col)
def shadowed(img, sp, xy, blur=18, off=(0, 18), alpha=140):
    a = sp.split()[3].point(lambda v: alpha if v else 0); sh = Image.new("RGBA", sp.size, (0, 0, 0, 0)); sh.putalpha(a)
    sh = sh.filter(ImageFilter.GaussianBlur(blur)); img.paste(sh, (xy[0] + off[0], xy[1] + off[1]), sh); img.paste(sp, xy, sp)
def make(out, style, big, line="", kicker="", who=("theo",), tone="lime", sub=""):
    bg = {"lime": LIME, "red": RED, "paper": PAPER, "black": BLACK}
    img = Image.new("RGB", (W, H), BLACK); d = ImageDraw.Draw(img); acc = RED if tone == "red" else LIME
    if style == "hero":  # giant character, word stamped across it
        img.paste(bg["lime" if tone != "red" else "red"], [0, 0, W, H]); d = ImageDraw.Draw(img)
        for i in range(0, H, 60): d.line([(0, i), (W, i - 400)], fill=tuple(max(0, c - 18) for c in (LIME if tone != "red" else RED)), width=22)
        sp = sprite(who[0], 760); shadowed(img, sp, (W // 2 - sp.width // 2, BOT - 120 - sp.height))
        bigtext(d, (W // 2, TOP + 400), big, W - 120, 300, BLACK, "ms", stroke_width=10, stroke_fill=WHITE)
        if line: d.text((W // 2, TOP + 180), line, font=fitf(d, line, W - 160, 80, 900, 110), fill=BLACK, anchor="ms")
    elif style == "versus":  # two characters, diagonal split, VS
        d.polygon([(0, 0), (W, 0), (W, 760), (0, 1220)], fill=(18, 18, 18)); d.polygon([(0, 1220), (W, 760), (W, H), (0, H)], fill=acc)
        a, b = (who + ("penny",))[:2]
        sa = sprite(a, 440); sb = sprite(b, 520).transpose(Image.FLIP_LEFT_RIGHT)
        shadowed(img, sa, (60, 1230 - sa.height)); shadowed(img, sb, (W - 60 - sb.width, BOT - 40 - sb.height))
        d.text((W // 2 + 60, 1130), "VS", font=arch(220), fill=WHITE, anchor="mm", stroke_width=12, stroke_fill=BLACK)
        bigtext(d, (W - 72, TOP + 330), big, W - 140, 170, acc, "rs")
        if line: d.text((W - 72, TOP + 410), line, font=fitf(d, line, W - 160, 64, 800, 110), fill=WHITE, anchor="rs")
        brand(d)
    elif style == "number":  # full-bleed giant number, tiny character peeking
        img.paste(acc if tone != "paper" else PAPER, [0, 0, W, H]); d = ImageDraw.Draw(img); fg = BLACK
        # safe layout (2026-10-31): the giant number ends above y 850, so the apps' button column never cuts it
        bigtext(d, (W // 2, 845), big, W - 80, 340, fg, "ms")
        if line: d.text((W // 2, 590), line, font=fitf(d, line, W - 160, 100), fill=fg, anchor="ms")
        if sub: d.text((CX, 1000), sub, font=fitf(d, sub, SAFE_R - 72, 60, 800, 100), fill=fg, anchor="ms")
        sp = sprite(who[0], 330); img.paste(sp, (W - sp.width - 40, BOT - sp.height + 20), sp)
        d.text((72, TOP + 60), "≈ Rounding Error", font=arch(44, 800, 100), fill=fg)
    elif style == "meme":  # classic top/bottom caption on white, reaction face in the middle
        img.paste(WHITE, [0, 0, W, H]); d = ImageDraw.Draw(img)
        d.rectangle([60, TOP + 230, W - 60, BOT - 230], fill=BLACK)
        sp = sprite(who[0], 600); img.paste(sp, (W // 2 - sp.width // 2, BOT - 250 - sp.height), sp)
        top = (line or kicker).upper(); f = fitf(d, top, W - 120, 110, 900, 110); d.text((W // 2, TOP + 180), top, font=f, fill=BLACK, anchor="ms")
        bigtext(d, (W // 2, BOT - 70), big, W - 120, 170, BLACK, "ms", 900, 110)
        d.text((W // 2, TOP + 40), "≈ Rounding Error", font=arch(36, 800, 100), fill=BLACK, anchor="ma")
    elif style == "panel":  # manga page: paper, ink panels, focus lines
        img.paste(PAPER, [0, 0, W, H]); d = ImageDraw.Draw(img); rnd = random.Random(len(big))
        cx, cy = W // 2, 1080
        for i in range(120):
            a = rnd.uniform(0, 2 * math.pi); r0 = 300 + rnd.uniform(0, 140); w = rnd.uniform(3, 12)
            p1 = (cx + math.cos(a) * r0, cy + math.sin(a) * r0); p2 = (cx + math.cos(a) * 1600, cy + math.sin(a) * 1600)
            n = (-math.sin(a) * w, math.cos(a) * w); d.polygon([p1, (p2[0] + n[0], p2[1] + n[1]), (p2[0] - n[0], p2[1] - n[1])], fill=(20, 20, 20))
        sp = sprite(who[0], 560).convert("LA").convert("RGBA")
        img.paste(sp, (cx - sp.width // 2, cy + 260 - sp.height), sprite(who[0], 560))
        d.rectangle([40, TOP + 30, W - 40, TOP + 300], fill=BLACK); bigtext(d, (W // 2, TOP + 250), big, W - 140, 220, LIME, "ms")
        if line: d.rectangle([W - 560, BOT - 190, W - 40, BOT - 90], fill=WHITE, outline=BLACK, width=6); d.text((W - 300, BOT - 125), line, font=fitf(d, line, 480, 56, 900, 100), fill=BLACK, anchor="ms")
    elif style == "chart":  # big arrow chart, number on it
        img.paste(BLACK, [0, 0, W, H]); d = ImageDraw.Draw(img); col = acc
        pts = []; rnd = random.Random(len(big) * 7); y = 600 if tone == "red" else 1400
        for i in range(13):
            x = 40 + i * 85; y += (rnd.uniform(40, 90) if tone == "red" else -rnd.uniform(40, 90)); pts.append((x, y))
        for i in range(10): d.line([(0, TOP + 120 * i), (W, TOP + 120 * i)], fill=(26, 26, 26), width=2)
        d.line(pts, fill=col, width=26, joint="curve"); ex, ey = pts[-1]
        d.polygon([(ex + 50, ey + (40 if tone == "red" else -40)), (ex - 40, ey - 30), (ex - 10, ey + 50)] if tone == "red" else [(ex + 50, ey - 40), (ex - 30, ey - 40), (ex + 20, ey + 40)], fill=col)
        bigtext(d, (72, 840), big, W - 140, 260, WHITE, "ls", stroke_width=8, stroke_fill=BLACK)  # safe layout: ends above y 850
        if line: d.text((72, TOP + 290), line, font=fitf(d, line, W - 160, 96, 900, 110), fill=col, anchor="ls")
        sp = sprite(who[0], 300); img.paste(sp, (W - sp.width - 60, BOT - sp.height), sp); brand(d)
        d.text((72, 1360), "AI TRADING BOT · REAL MONEY", font=mono(30), fill=GREY)
    ky = {"hero": TOP + 30, "versus": TOP + 135, "number": TOP + 135, "chart": TOP + 135}.get(style)
    if kicker and ky is not None:
        kf = mono(32); tw = d.textlength(kicker, font=kf); kx = 72 if style != "panel" else 40
        dark = style in ("hero", "number", "panel")
        d.rectangle([kx, ky, kx + tw + 28, ky + 50], fill=BLACK if dark else acc)
        d.text((kx + 14, ky + 37), kicker, font=kf, fill=WHITE if dark else BLACK, anchor="ls")
    if True:  # every cover says it once (the boss, 2026-10-26; once only, 2026-10-29)
        f = mono(28); t = "NOT FINANCIAL ADVICE"; w = d.textlength(t, font=f); ny = 1400  # inside the safe box (2026-10-31; was under the captions)
        d.rectangle([CX - w / 2 - 14, ny, CX + w / 2 + 14, ny + 44], fill=BLACK); d.text((CX, ny + 34), t, font=f, fill=WHITE, anchor="ms")
    img.save(out, quality=92); return out
STYLES = ["hero", "versus", "number", "meme", "panel", "chart"]
