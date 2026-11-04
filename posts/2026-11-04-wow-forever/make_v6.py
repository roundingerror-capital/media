"""WoW Forever v6 (the boss 2026-11-04, "need this perfect"): v5 plus
  - THE PRESS: the hand comes in on an arm (suit sleeve + shirt cuff from the top-right edge), so it reads as a hand, not a mic;
    AUTOMATE is the keyboard's big bottom-row key (where the spacebar sits), nothing stacked on keys; the press lands with a
    vignette build-up, a pixel starburst, two shockwave rings, flying sparks, a zoom punch and a shake (no thin white lines);
  - his office: the ticker panel right of the door is gone; three framed graded cards (Kit's original slabs) hang there instead;
  - the raid floor: Kit's flagstone tile once, then its own bottom row continued (no second small-brick band under the cast bar);
  - sound: chiptune SFX synthesized the NES/SNES way (tools/sfx.py), under the boss's three tracks, music ducks on the hero hits.
    python3 make_v6.py <out.mp4> | --panels <sheet.png>"""
import os, sys, math, runpy, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
_argv = sys.argv; sys.argv = sys.argv[:1]
V5 = runpy.run_path(os.path.join(HERE, "make_v5.py"), run_name="v5"); sys.argv = _argv
V3, V2, V6o = V5["V3"], V5["V2"], V5["V6"]
import numpy as np
from PIL import Image, ImageDraw
import kitpieces as K, stage, sfx
from make_reel import W, H, FPS, mono, fit
LIME, INK = V5["LIME"], V5["INK"]
stamp, comp, load, place = V5["stamp"], V5["comp"], V5["load"], V5["place"]
G3 = V5["G3"]

# ---------- office: graded cards where the ticker panel was ----------
def office(t, view="Back · Type", cast=(), dark=False):
    st = load("OFF-BOSS-01"); extra = {}
    door = comp("DEC-25"); place(extra, "L6", door, 80, 88 - door.height)
    art = K.piece("DEC-56", 0); place(extra, "L6", art, 128 - art.width // 2, 10)
    for x in (115, 141): f = K.piece("DEC-47", 0); place(extra, "L6", f, x - f.width // 2, 14)
    for i, (x, n) in enumerate(((114, "DEC-54"), (128, "DEC-55"), (142, "DEC-54"))):              # three slabs in a row, right of the door
        sl = K.piece(n, 0); place(extra, "L6", sl, x - sl.width // 2, 36)
    gal = comp("DEC-31"); place(extra, "L6", gal, 170 - gal.width // 2, 8)
    bd = V2["boss_desk"](view, t); place(extra, "L14", bd, 126 - bd.width // 2, 113 - bd.height)
    for ch, an, x, feet, flip in cast:
        sp_ = V6o["standing"](ch, an, t, 0, flip); place(extra, "L16", sp_, int(x) - sp_.width // 2, feet - sp_.height)
    im = st.render(skip=("CHR", "DSK", "MON01", "MON04", "TEC07", "DEC05"), extra=extra, wall=comp("WALL-05"))
    if dark: im = Image.alpha_composite(im, Image.new("RGBA", im.size, (6, 8, 26, 90)))
    return st, im
G3["office"] = office; V2["office"].__globals__["office"] = office; V5["office"].__globals__["office"] = office


# ---------- player cards: room between the frame and the text (the boss: the name sat a pixel from the border) ----------
def player_card(img, who, u):
    nm, job, cls, race, role = V3["ROSTER"][who]; d = ImageDraw.Draw(img)
    k = min(1, u / 0.18); y0 = int(1250 + (1 - k) * 680); L = 112
    d.rectangle([70, y0 + 14, W - 56, y0 + 534], fill="#000000")
    d.rectangle([56, y0, W - 70, y0 + 520], fill="#0E0E14", outline=LIME, width=6)
    d.text((L, y0 + 140), nm, font=fit(nm, 580, 104, wdth=125, wght=900), fill=INK, anchor="ls")
    d.text((L, y0 + 196), job, font=mono(34, True), fill="#9A9A94", anchor="ls")
    d.line([L, y0 + 230, W - 126, y0 + 230], fill="#2A2A33", width=4)
    d.text((L, y0 + 292), "CLASS", font=mono(26, True), fill="#9A9A94", anchor="ls")
    d.text((L, y0 + 360), cls, font=fit(cls, 410, 66, wdth=120, wght=900), fill=LIME, anchor="ls")
    d.text((570, y0 + 292), "RACE", font=mono(26, True), fill="#9A9A94", anchor="ls")
    d.text((570, y0 + 360), race, font=fit(race, 380, 66, wdth=120, wght=900), fill=V3["GOLD"], anchor="ls")
    d.text((L, y0 + 462), role, font=mono(34, True), fill=INK, anchor="ls")
    return img
G3["player_card"] = player_card

# ---------- raid floor ----------
def arena(t):
    st = load("ROOM-19"); flat = tuple(f"fbROOMFLRFLAG{y}" for y in (88, 96, 104, 112, 120))
    im = st.render(skip=flat); c = Image.new("RGBA", (135, 240), (10, 10, 16, 255))
    wall = K.piece("LIBROOMS6", 0, "Wall, dungeon stone"); flr = K.piece("LIBROOMS6", 0, "Floor, flagstones")
    for y in range(0, 70, wall.height):
        for x in range(0, 135, wall.width): c.alpha_composite(wall.crop((0, 0, min(wall.width, 135 - x), min(wall.height, 70 - y))), (x, y))
    band = flr.crop((0, flr.height - 12, flr.width, flr.height))                                  # the tile's own last (largest) row
    y = 158
    for x in range(0, 135, flr.width): c.alpha_composite(flr.crop((0, 0, min(flr.width, 135 - x), min(flr.height, 240 - y))), (x, y))
    y += flr.height
    while y < 240:
        for x in range(0, 135, band.width): c.alpha_composite(band.crop((0, 0, min(band.width, 135 - x), min(12, 240 - y))), (x, y))
        y += 12
    c.alpha_composite(im.crop((92, 0, 227, 128)), (0, 70))
    return c
V2["arena"] = arena

# ---------- THE PRESS ----------
CW, CH = 64, 112
SUIT, CUFF, HAND, RIM = (40, 42, 66), (214, 214, 224), (22, 22, 44), (58, 58, 92)
def press_canvas(u):
    c = Image.new("RGB", (CW, CH), (92, 52, 30)); d = ImageDraw.Draw(c)
    for y in range(0, CH, 12):
        d.rectangle([0, y, CW - 1, y + 10], fill=[(92, 52, 30), (110, 64, 36)][(y // 12) % 2]); d.line([0, y + 11, CW - 1, y + 11], fill=(78, 44, 26))
    kb = (0, 54, CW - 1, 106); d.rectangle(kb, fill=(28, 30, 38)); d.line([0, 54, CW - 1, 54], fill=(60, 62, 76))
    def key(x0, y0, w, h, top=(80, 82, 96), skirt=(56, 58, 70)):
        d.rectangle([x0, y0, x0 + w - 1, y0 + h - 1], fill=skirt); d.rectangle([x0 + 1, y0, x0 + w - 2, y0 + h - 3], fill=top)
    for r, ky in enumerate((57, 65, 73)):                                                          # three ordinary rows
        for kx in range(1 + (r % 2) * 3, CW - 6, 8): key(kx, ky, 7, 7)
    press = u >= 0.82; dip = 2 if press else 0
    for kx in (1, 9): key(kx, 81, 7, 16)                                                           # bottom row: two keys,
    key(CW - 8, 81, 7, 16)                                                                         # ... one key on the right,
    kx0, kw, ky0, kh = 17, 38, 81, 16                                                              # ... and AUTOMATE where the spacebar sits
    d.rectangle([kx0, ky0, kx0 + kw - 1, ky0 + kh - 1], fill=(30, 40, 10))                         # its well
    d.rectangle([kx0, ky0 + dip, kx0 + kw - 1, ky0 + kh - 1], fill=(120, 148, 30) if press else (150, 186, 40))
    d.rectangle([kx0 + 1, ky0 + dip, kx0 + kw - 2, ky0 + kh - 4 + (1 if press else 0)], fill=(176, 214, 48) if press else (200, 240, 60))
    if not press: d.line([kx0 + 2, ky0 + 1, kx0 + kw - 3, ky0 + 1], fill=(232, 255, 150))
    keytop = ky0 + dip; cx = kx0 + kw // 2
    e = max(0.0, min(1.0, (u - 0.05) / 0.77)); e = e * e                                           # the hand eases in, then commits
    tipx = int(cx + (1 - e) * 26); tipy = int(keytop + 1 - (1 - e) * 46)
    # arm: from the top-right edge into the wrist: a suit sleeve with a white shirt cuff, fist and finger at its end
    wx, wy = tipx + 4, tipy - 19                                                                   # wrist (top-right of the fist)
    ax, ay = 0.53, -0.85                                                                           # arm direction, toward the top-right corner
    px, py = -ay, ax                                                                               # perpendicular
    def band(d0, d1, half, col):
        p0 = (wx + ax * d0, wy + ay * d0); p1 = (wx + ax * d1, wy + ay * d1)
        d.polygon([(p0[0] + px * half, p0[1] + py * half), (p1[0] + px * half, p1[1] + py * half),
                   (p1[0] - px * half, p1[1] - py * half), (p0[0] - px * half, p0[1] - py * half)], fill=col)
    band(6, 120, 8, SUIT); band(6, 120, 8, SUIT)
    d.line([(wx + ax * 6 - px * 8, wy + ay * 6 - py * 8), (wx + ax * 120 - px * 8, wy + ay * 120 - py * 8)], fill=(64, 66, 98))  # lit edge of the sleeve
    band(2, 7, 7, CUFF)                                                                            # shirt cuff at the wrist
    d.rounded_rectangle([tipx - 8, tipy - 23, tipx + 8, tipy - 10], radius=6, fill=HAND, outline=RIM)  # fist, knuckles round
    for kx in (tipx - 4, tipx + 1): d.line([kx, tipy - 12, kx + 3, tipy - 12], fill=(36, 36, 64))
    d.rounded_rectangle([tipx - 3, tipy - 14, tipx + 3, tipy], radius=3, fill=HAND, outline=RIM)    # index finger, round tip
    d.rounded_rectangle([tipx - 1, tipy - 5, tipx + 1, tipy - 2], radius=1, fill=(46, 46, 80))       # nail
    return c, keytop, (kx0, kw, kh)

def burst(img, cx, cy, s, t):
    """Pixel starburst + shockwave rings + sparks, drawn chunky (8 px grid) so it matches the pixel art."""
    lo = Image.new("RGBA", (W // 8, H // 8), (0, 0, 0, 0)); d = ImageDraw.Draw(lo); x0, y0 = cx / 8, cy / 8
    pts = []
    for i in range(16):
        a = i / 16 * 2 * math.pi + 0.2; r = (26 if i % 2 == 0 else 12) * s
        pts.append((x0 + math.cos(a) * r, y0 + math.sin(a) * r))
    d.polygon(pts, fill=(200, 240, 60, 255)); d.polygon([(x0 + (p[0] - x0) * 0.55, y0 + (p[1] - y0) * 0.55) for p in pts], fill=(255, 255, 255, 255))
    for k, rr in enumerate((30 * s + 4, 42 * s + 2)):
        d.ellipse([x0 - rr, y0 - rr * 0.8, x0 + rr, y0 + rr * 0.8], outline=(255, 255, 255, int(200 / (k + 1))), width=2)
    for i in range(14):
        a = i / 14 * 2 * math.pi + 0.4; r = 20 + s * 46 + (i % 3) * 4
        px, py = x0 + math.cos(a) * r, y0 + math.sin(a) * r * 0.9; d.rectangle([px, py, px + 1, py + 1], fill=(255, 220, 90, 255) if i % 2 else (255, 255, 255, 255))
    img.alpha_composite(lo.resize((W, H), Image.NEAREST))

def the_press(t, u):
    u = u / 1.6; c, keytop, (kx0, kw, kh) = press_canvas(u)
    k, (cw, ch) = (17, (CW, CH)) if u < 0.5 else (20, (54, 96)) if u < 0.82 else (24, (45, 80))       # whole-number push-in, punch on contact
    x0 = (CW - cw) // 2 + (2 if cw < CW else 0); y0 = max(0, min(CH - ch, keytop + 26 - ch))
    img = c.crop((x0, y0, x0 + cw, y0 + ch)).resize((cw * k, ch * k), Image.NEAREST)
    pad = Image.new("RGB", (W, H), (0, 0, 0)); pad.paste(img, ((W - img.width) // 2, (H - img.height) // 2)); img = pad.convert("RGBA")
    ox, oy = (W - cw * k) // 2, (H - ch * k) // 2
    kcx, kcy = ox + (kx0 + kw // 2 - x0) * k, oy + (keytop - y0 + 6) * k
    label = lambda im: ImageDraw.Draw(im).text((kcx, kcy), "AUTOMATE", font=fit("AUTOMATE", int((kw - 4) * k * 0.9), int(7 * k), wdth=125, wght=900), fill="#0B0B0B", anchor="mm")
    label(img)
    if u < 0.82:                                                                                   # tension: the edges close in
        v = Image.new("L", (W // 8, H // 8), 0); dv = ImageDraw.Draw(v); m = int(10 + u * 26)
        dv.rectangle([0, 0, W // 8, H // 8], fill=int(200 * u)); dv.ellipse([m // 2, m, W // 8 - m // 2, H // 8 - m], fill=0)
        from PIL import ImageFilter
        img = Image.composite(Image.new("RGBA", img.size, (0, 0, 0, 255)), img, v.filter(ImageFilter.GaussianBlur(6)).resize((W, H), Image.BILINEAR))
    else:
        p = (u - 0.82) / 0.18
        if p < 0.12: img = Image.alpha_composite(img, Image.new("RGBA", img.size, (255, 255, 255, 170)))
        if p < 0.75: burst(img, kcx, kcy - 6 * k, 0.6 + p * 1.1, t)
        label(img)
        s = int(26 * max(0, 1 - p)); img = img.transform(img.size, Image.AFFINE, (1, 0, (s if int(u * 60) % 2 else -s), 0, 1, (s // 2 if int(u * 45) % 2 else 0)))
        stamp(img, "CLICK.", LIME, 300, 170)
    return img.convert("RGB")

def shots():
    return [(d, l, the_press if l == "THE PRESS" else f) for d, l, f in V5["shots"]()]

# ---------- sound ----------
def sound(S, total, out):
    V5["music"](S, total, out[:-4] + "_music.wav")
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", out[:-4] + "_music.wav", "-ac", "2", "-ar", str(sfx.SR), "-f", "f32le", "-"], capture_output=True).stdout
    m = np.frombuffer(raw, np.float32).reshape(-1, 2); bus = sfx.Bus(total)
    T, t = {}, 0
    for d, l, _ in S: T[l] = (t, d); t += d
    rng = np.random.default_rng(3)
    def typing(a, b, rate=9, gain=0.16):
        x = a
        while x < b: bus.add(sfx.click(rng.uniform(-0.15, 0.15)), x, gain * rng.uniform(0.7, 1.0)); x += rng.uniform(0.6, 1.4) / rate
    a, d = T["TEASER"]; bus.add(sfx.thump(), a + 0.05, 0.35)
    a, d = T["FROM BEHIND · SHE WALKS IN"]; typing(a, a + d)
    for i in range(4): bus.add(sfx.step(i % 2), a + 0.3 + i * 0.45, 0.22)
    a, d = T["SHE'S WORRIED"]; typing(a, a + d, 6, 0.11); bus.add(sfx.pop(), a + 0.02, 0.25)
    a, d = T["PUSH-IN"]; typing(a, a + d, 12, 0.17); bus.add(sfx.whoosh(d, True), a, 0.25)
    a, d = T["MUST AUTOMATE"]; typing(a, a + d, 14, 0.18)
    for i in range(3): bus.add(sfx.thump(), a + 0.05 + i * 2.0 / 2.4, 0.3)
    a, d = T["THE PRESS"]; hit = a + 0.82 * 1.6
    bus.add(sfx.whoosh(hit - a, True), a, 0.18); bus.add(sfx.key_slam(), hit, 0.55, duck=6); bus.add(sfx.impact(), hit, 0.55); bus.add(sfx.arp_up(72), hit + 0.12, 0.22)
    a, d = T["ALL SYSTEMS CHECK"]; bus.add(sfx.arp_up(64, (0, 7, 12), 0.06), a + 0.05, 0.2)
    for n, who in enumerate(("THEO", "PENNY", "ROZ", "ADA", "KIT")):
        a, d = T[who]; bus.add(sfx.click(), a + 0.05, 0.1); bus.add(sfx.ding(83 + n), a + 0.58, 0.32)      # card slides in, AUTOMATED lands
    a, d = T["EVERYTHING IS READY"]; bus.add(sfx.arp_up(72), a + 0.05, 0.28)
    a, d = T["SLOW BLINK"]; bus.add(sfx.arp_down(79, (0, -5, -12), 0.18), a + 0.2, 0.12)
    a, d = T["THE RAID"]
    for k in range(5):
        for i, kind in enumerate(("boss", "kit", "penny")):
            at = a + i * 0.3 + k * 0.9 + 0.3 * 0.9
            if at < a + d: bus.add({"boss": sfx.zap, "kit": sfx.bonk, "penny": sfx.heal}[kind](), at, {"boss": 0.22, "kit": 0.3, "penny": 0.16}[kind])
    bus.add(sfx.roar(), a + 2.35, 0.32, duck=3)
    a, d = T["PARTY WIPED"]; bus.add(sfx.roar(), a, 0.35); bus.add(sfx.impact(), a + 0.05, 0.4, duck=5); bus.add(sfx.wipe(), a + 0.6, 0.3)
    for i in range(10): bus.add(sfx.coin(i % 5), a + 0.15 + i * 0.07, 0.14)
    a, d = T["ASLEEP ON THE DESK"]; bus.add(sfx.pop(), a + 0.02, 0.2)
    for lab, ats in (("S1", (0.0, 0.25)), ("S2", (0.0,)), ("S3", (0.0, 0.2)), ("WHY", (0.0, 0.2, 0.5))):
        a, d = T[lab]
        for x in ats: bus.add(sfx.thump(), a + x, 0.32)
    a, d = T["LIKE + FOLLOW"]; bus.add(sfx.sparkle(), a + 0.05, 0.3)
    y = bus.mix_into(m)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(sfx.SR), "-ac", "2", "-i", "-", "-af", "loudnorm=I=-14:TP=-1.5", "-ar", "44100", out],
                   input=y.astype(np.float32).tobytes(), check=True)

def build(out):
    S = shots(); total = sum(d for d, _, _ in S); wav = out[:-4] + "_mix.wav"; sound(S, total, wav)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "20",
        "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for i in range(int(round(total * FPS))): p.stdin.write(V3["frame_at"](S, i / FPS).tobytes())
    p.stdin.close(); p.wait(); print(out, f"{total:.1f}s")

def panels(out, ts):
    S = shots(); ims = []
    for lab, u in ts:
        t = 0
        for dur, l, fn in S:
            if l == lab: ims.append(V3["frame_at"](S, t + u)); break
            t += dur
    s = Image.new("RGB", (len(ims) * 270, 480))
    for i, im in enumerate(ims): s.paste(im.resize((270, 480)), (i * 270, 0))
    s.save(out); print(out)

if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if "--panels" in sys.argv:
        panels(a[0], [("THE PRESS", 0.2), ("THE PRESS", 0.9), ("THE PRESS", 1.25), ("THE PRESS", 1.33), ("THE PRESS", 1.5), ("SHE'S WORRIED", 1.5), ("THE RAID", 1.0)])
    else: build(a[0] if a else "/home/claude/out/wow/wow_v6.mp4")
