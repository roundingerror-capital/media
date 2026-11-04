"""WoW Forever v5 (the boss 2026-11-04, ship today): v4-E plus his last notes.
  - THE PRESS: a real key on a keyboard (keycap with a top face and bevel, sinks on press) and a rounder hand (round tip, rounded fist);
  - the push-in code: syntax colours (reserved words lime, the rest white) and 2-3 lines twice as big;
  - end cards: the key words bigger and lime ("we AUTOMATED the RESEARCH");
  - the wife's thought bubble text centred in its bubble;
  - his office wall: no lamp on the door, the art centred in the visible wall, the trophy row gone;
  - the raid: one even flagstone floor (no oversized first row), light auras on the party, Evil Theo ENRAGED with a red aura;
  - music: the boss's three Gemini tracks, one per act (intro / raid / outro), cut on their own energy.
    python3 make_v5.py <out.mp4> | --panels <sheet.png>"""
import os, sys, math, runpy, subprocess, re
HERE = os.path.dirname(os.path.abspath(__file__))
_argv = sys.argv; sys.argv = sys.argv[:1]
V4 = runpy.run_path(os.path.join(HERE, "make_v4.py"), run_name="v4"); sys.argv = _argv
V3 = V4["V3"]; V2 = V3["V2"]; V1 = V3["V1"]; V6 = V3["V6"]
import numpy as np
from scipy import ndimage
from PIL import Image, ImageDraw
import kitpieces as K, stage
from make_reel import W, H, FPS, mono, fit
LIME, INK, RED, GOLD = "#C8F03C", "#F2F2EE", "#FF5C5C", "#F5C84B"
black, stamp, comp, load, place = V3["black"], V3["stamp"], V3["comp"], V3["load"], V3["place"]
G3 = V3["shots"].__globals__                      # v3's live module globals (its shot lambdas look names up here)

# ---------- office wall ----------
def office(t, view="Back · Type", cast=(), dark=False):
    st = load("OFF-BOSS-01"); extra = {}
    door = comp("DEC-25"); place(extra, "L6", door, 80, 88 - door.height)               # door spans x 80-108
    art = K.piece("DEC-56", 0); art = art.resize((art.width * 1, art.height * 1))
    place(extra, "L6", art, 128 - art.width // 2, 10)                                     # art print centred in the wall the camera sees (108-148)
    for x in (115, 141):                                                                  # small frames either side, clear of the door
        f = K.piece("DEC-47", 0); place(extra, "L6", f, x - f.width // 2, 14)
    gal = comp("DEC-31"); place(extra, "L6", gal, 170 - gal.width // 2, 8)                # gallery over the bookshelf (wide shots)
    bd = V2["boss_desk"](view, t); place(extra, "L14", bd, 126 - bd.width // 2, 113 - bd.height)
    for ch, an, x, feet, flip in cast:
        sp_ = V6["standing"](ch, an, t, 0, flip); place(extra, "L16", sp_, int(x) - sp_.width // 2, feet - sp_.height)
    an_extra, moving = V6["animate"](st, t, ("MON",)); V6["merge"](extra, an_extra)
    im = st.render(skip=("CHR", "DSK", "MON01", "TEC07", "DEC05") + moving, extra=extra, wall=comp("WALL-05"))
    if dark: im = Image.alpha_composite(im, Image.new("RGBA", im.size, (6, 8, 26, 90)))
    return st, im
G3["office"] = office; V2["office"].__globals__["office"] = office

# ---------- thought bubble: text centred ----------
def thought(img, lines, cx, y):
    d = ImageDraw.Draw(img); f = fit(max(lines, key=len), 700, 50, wdth=105, wght=800); lh = 64
    w = max(int(f.getlength(l)) for l in lines) + 80; h = lh * len(lines) + 50
    d.rounded_rectangle([cx - w // 2, y, cx + w // 2, y + h], radius=60, fill=INK, outline="#000000", width=6)
    for r, (dx, dy) in ((26, (60, h + 30)), (16, (100, h + 80))): d.ellipse([cx + dx - r, y + dy - r, cx + dx + r, y + dy + r], fill=INK, outline="#000000", width=5)
    top = y + (h - lh * len(lines)) // 2
    for i, l in enumerate(lines): d.text((cx, top + i * lh + lh // 2), l, font=f, fill="#0B0B0B", anchor="mm")
    return img
G3["thought"] = thought

# ---------- push-in code: syntax colours, some lines 2x ----------
KW = r"\b(def|for|in|while|not|return|SELECT|FROM|WHERE|git|push|True|forever|automate)\b"
def code_line(d, x, y, line, size, anchor_center=True):
    f = mono(size, True); parts = re.split(KW, line); total = sum(f.getlength(p) for p in parts if p)
    cx = x - total / 2
    for p in parts:
        if not p: continue
        col = LIME if re.fullmatch(KW, p) else INK
        d.text((cx, y), p, font=f, fill=col, anchor="lm", stroke_width=3 if size < 50 else 5, stroke_fill="#000000"); cx += f.getlength(p)
CODE = V1["CODE"]
def pushin(t, u, k):
    st, im = office(t, "Front · Type"); w, h = 1080 // k, 1920 // k; cx, cy = 126, 70
    img = stage.camera(im, cx - w // 2, cy - h // 2, w, h, k).convert("RGBA")
    img = Image.alpha_composite(img, Image.new("RGBA", img.size, (90, 200, 255, 60) if int(u * 6) % 2 else (200, 240, 60, 60))).convert("RGB")
    d = ImageDraw.Draw(img)
    for i in range(6):
        z = (u * 0.9 + i / 6) % 1; line = CODE[(i + int(u * 3)) % len(CODE)]
        big = i in (1, 4)                                                                   # two of six lines twice the size
        size = int((24 + z * 34) * (2 if big else 1)); y = int(300 + i * 230 + (z - 0.5) * 160)
        if big:
            line = line.strip()
            while mono(size, True).getlength(line) > W - 100 and size > 40: size -= 4          # big lines always fit the frame
            x = W // 2
        else: x = int(W / 2 + (i % 2 * 2 - 1) * (120 + z * 380))
        code_line(d, x, y, line, size)
    return img
V2["pushin"] = pushin

# ---------- THE PRESS: a keyboard key and a rounder hand ----------
def press_canvas(u):
    c = Image.new("RGB", (54, 96), (92, 52, 30)); d = ImageDraw.Draw(c)
    for y in range(0, 96, 12):
        d.rectangle([0, y, 53, y + 10], fill=[(92, 52, 30), (110, 64, 36)][(y // 12) % 2]); d.line([0, y + 11, 53, y + 11], fill=(78, 44, 26))
    d.rounded_rectangle([1, 46, 53, 92], radius=3, fill=(30, 32, 40), outline=(14, 14, 20))      # keyboard body
    for r, ky in enumerate(range(49, 90, 8)):                                                      # rows of ordinary keys
        for kx in range(3 + (r % 2) * 3, 50, 8):
            if 7 <= kx <= 46 and 57 <= ky <= 74: continue                                          # space for the big key
            d.rectangle([kx, ky, kx + 6, ky + 6], fill=(58, 60, 72)); d.rectangle([kx + 1, ky, kx + 5, ky + 4], fill=(78, 80, 94))
    press = u >= 0.82; dip = 2 if press else 0; by = 58 + dip
    d.rectangle([8, 58, 46, 76], fill=(40, 52, 16))                                                # key well
    d.rectangle([9, 58 + dip, 45, 75], fill=(122, 150, 30) if press else (150, 186, 40))           # keycap skirt (bevel)
    d.rectangle([11, 58 + dip, 43, 71 if not press else 72], fill=(170, 210, 46) if press else (200, 240, 60))   # keycap top face
    if not press: d.line([12, 59, 42, 59], fill=(232, 255, 150)); d.line([11, 60, 11, 70], fill=(225, 250, 120))
    e = max(0.0, min(1.0, (u - 0.12) / 0.70)); tip = int(4 + e * e * (by - 6))
    if u < 0.12: return c, by
    col, rim, nail = (20, 20, 42), (52, 52, 86), (44, 44, 76)
    f0 = max(-4, tip - 22)
    d.rounded_rectangle([24, f0, 31, tip], radius=3, fill=col, outline=rim)                       # finger with a round tip
    d.rounded_rectangle([26, tip - 7, 29, tip - 3], radius=1, fill=nail)
    d.line([25, tip - 12, 30, tip - 12], fill=(34, 34, 60))                                       # knuckle crease
    if f0 > -4:
        d.rounded_rectangle([19, f0 - 11, 37, f0 + 3], radius=6, fill=col, outline=rim)           # rounded fist
        for kx in (22, 28): d.line([kx, f0 - 1, kx + 3, f0 - 1], fill=(34, 34, 60))                # curled fingers
    return c, by
def the_press(t, u):
    u = u / 1.6; c, by = press_canvas(u)
    k, (cw, ch) = (20, (54, 96)) if u < 0.45 else (24, (45, 80)) if u < 0.75 else (30, (36, 64))
    x0 = (54 - cw) // 2; y0 = max(0, min(96 - ch, by + 20 - ch))
    img = c.crop((x0, y0, x0 + cw, y0 + ch)).resize((cw * k, ch * k), Image.NEAREST)
    if 0.82 <= u < 0.9: img = Image.blend(img, Image.new("RGB", img.size, (255, 255, 255)), 0.5)
    if u >= 0.82:
        s = int(16 * max(0, 1 - (u - 0.82) / 0.18)); img = img.transform(img.size, Image.AFFINE, (1, 0, (s if int(u * 60) % 2 else -s), 0, 1, 0))
    d = ImageDraw.Draw(img); top = (by - y0) * k; capw = (43 - 11) * k
    d.text(((11 - x0) * k + capw // 2, top + 6 * k), "AUTOMATE", font=fit("AUTOMATE", int(capw * 0.86), int(6 * k), wdth=125, wght=900), fill="#0B0B0B", anchor="mm")
    if u < 0.82:
        for i in range(10):
            a = i / 10 * math.pi * 2; r0 = 700 - (u * 900 + i * 37) % 300; r1 = r0 + 120; cx, cy = W // 2, top + 6 * k
            d.line([cx + math.cos(a) * r0, cy + math.sin(a) * r0, cx + math.cos(a) * r1, cy + math.sin(a) * r1], fill=INK, width=6)
    else: stamp(img, "boop.", INK, 330, 150)
    return img

# ---------- the raid: even floor, auras, enraged boss ----------
def arena(t):
    st = load("ROOM-19"); flat = tuple(f"fbROOMFLRFLAG{y}" for y in (88, 96, 104, 112, 120))
    im = st.render(skip=flat); c = Image.new("RGBA", (135, 240), (10, 10, 16, 255))
    wall = K.piece("LIBROOMS6", 0, "Wall, dungeon stone"); flr = K.piece("LIBROOMS6", 0, "Floor, flagstones")
    for y in range(0, 70, wall.height):
        for x in range(0, 135, wall.width): c.alpha_composite(wall.crop((0, 0, min(wall.width, 135 - x), min(wall.height, 70 - y))), (x, y))
    for y in range(70 + 88, 240, flr.height):                                                     # one flagstone size from the wall line to the bottom
        for x in range(0, 135, flr.width): c.alpha_composite(flr.crop((0, 0, min(flr.width, 135 - x), min(flr.height, 240 - y))), (x, y))
    c.alpha_composite(im.crop((92, 0, 227, 128)), (0, 70))
    return c
V2["arena"] = arena

AURA = {"BossGear": (170, 120, 255), "KitGear": (255, 226, 140), "PennyGear": (190, 255, 210), "EvilTheo": (255, 50, 50)}
def aura(im, col, t, big=False):
    a = np.array(im.convert("RGBA")); op = a[..., 3] > 0; p = 4 if big else 3
    pad = np.zeros((a.shape[0] + p, a.shape[1] + 2 * p, 4), np.uint8); pad[p:, p:p + a.shape[1]] = a; opp = pad[..., 3] > 0
    r1 = ndimage.binary_dilation(opp, iterations=1) & ~opp; r2 = ndimage.binary_dilation(opp, iterations=p) & ~opp & ~r1
    pulse = 0.65 + 0.35 * math.sin(t * (9 if big else 5))
    out = np.zeros_like(pad); out[r2] = (*col, int(70 * pulse)); out[r1] = (*col, int(170 * pulse))
    o = Image.fromarray(out); o.alpha_composite(Image.fromarray(pad)); return o
_piece = K.piece
def piece(board, t, name=None):
    im = _piece(board, t, name); b = str(board)
    for key, col in AURA.items():
        if key in b: return aura(im, col, t, big=(key == "EvilTheo"))
    return im
K.piece = piece
_raid = V3["raid"]
def raid(t, u, wipe=False, dur=4.5, win=False):
    img = _raid(t, u, wipe=wipe, dur=dur, win=win)
    if not (wipe or win):
        d = ImageDraw.Draw(img); on = int(t * 4) % 2
        d.text((W - 80, 100), "ENRAGED", font=mono(30, True), fill=RED if on else "#FFB0B0", anchor="rs")
        img = Image.alpha_composite(img.convert("RGBA"), Image.new("RGBA", img.size, (255, 0, 0, 18 if on else 6))).convert("RGB")
    return img
G3["raid"] = raid

# ---------- end cards: key words bigger and lime ----------
def rich(img, segs, y):
    """One centred line of (text, big?) segments: big words lime and ~1.4x, the rest white."""
    d = ImageDraw.Draw(img); base = 96
    fonts = [fit(s, 2000, int(base * (1.45 if b else 1)), wdth=125, wght=900) for s, b in segs]
    gap = 26; tot = sum(f.getlength(s) for (s, _), f in zip(segs, fonts)) + gap * (len(segs) - 1)
    scale = min(1, (W - 120) / tot)
    if scale < 1:
        fonts = [fit(s, 2000, int(base * scale * (1.45 if b else 1)), wdth=125, wght=900) for s, b in segs]; tot = sum(f.getlength(s) for (s, _), f in zip(segs, fonts)) + gap * (len(segs) - 1)
    x = W / 2 - tot / 2
    for (s, b), f in zip(segs, fonts):
        d.text((x, y), s, font=f, fill=LIME if b else INK, anchor="ls", stroke_width=10, stroke_fill="#000000"); x += f.getlength(s) + gap
    return img
def rcards(rows, extra=()):
    def f(t, u):
        img = black()
        for segs, y, at in rows:
            if u >= at: rich(img, segs, y)
        for txt, col, y, size, at in extra:
            if u >= at: stamp(img, txt, col, y, size)
        return img
    return f
END_E = [
    (1.6, "S1", rcards([([("WE", False), ("AUTOMATED", True)], 860, 0), ([("THE", False), ("RESEARCH.", True)], 1020, 0.25)])),
    (1.4, "S2", rcards([([("NOW", False), ("WE", False), ("RAID.", True)], 960, 0)])),
    (1.8, "S3", rcards([([("YOU", False), ("GET", False)], 860, 0), ([("THE", False), ("RESEARCH.", True)], 1020, 0.2)])),
    (2.6, "WHY", rcards([([("years", True), ("of", False), ("options", False), ("trading,", False)], 820, 0),
                         ([("taught", False), ("to", False), ("a", False), ("bot.", True)], 940, 0.2)],
                        [("FOLLOW FOR THE RESEARCH.", LIME, 1500, 96, 0.5)])),
]

def shots():
    S = V4["shots"](); out = []
    for dur, lab, fn in S:
        if lab in ("S1", "S2", "S3", "WHY"):
            if lab == "S1": out += END_E
            continue
        out.append((dur, lab, the_press if lab == "THE PRESS" else fn))
    return out

A = "/mnt/user-data/attachments/97ad6b31-1277-5795-987d-0d7c1b8393c4/"
TRACKS = {"intro": (A + "c862546a-office_worried_wife_push-in_the_button_systems_check.mp3", 0.0),   # calm, builds at ~20 s, drops at 23
          "raid": (A + "27172401-the_boss_fight_and_the_party_wipe.mp3", 12.0),                       # its loudest stretch
          "outro": (A + "4a661aec-honey_wake_up__the_three_stamps_LIKE__FOLLOW.mp3", 8.9)}              # beat drops at 12 s = when the stamps start
def music(S, total, out):
    t, marks = 0, {}
    for dur, lab, _ in S:
        if lab == "THE RAID": marks["raid"] = t
        if lab == "HONEY...": marks["outro"] = t
        t += dur
    parts = [("intro", 0, marks["raid"]), ("raid", marks["raid"], marks["outro"]), ("outro", marks["outro"], total)]
    inp, fl = [], []
    for n, (key, a, b) in enumerate(parts):
        src, off = TRACKS[key]; inp += ["-i", src]; L = b - a
        fade_in = "" if n == 0 else ",afade=t=in:st=0:d=0.06"
        fl.append(f"[{n}]atrim={off:.3f}:{off + L + 0.12:.3f},asetpts=PTS-STARTPTS,loudnorm=I=-14:TP=-1.5{fade_in},afade=t=out:st={L - 0.06:.3f}:d=0.18,adelay={int(a * 1000)}|{int(a * 1000)}[s{n}]")
    fl.append(f"[s0][s1][s2]amix=inputs=3:normalize=0,atrim=0:{total:.3f},afade=t=out:st={total - 0.8:.3f}:d=0.8")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inp, "-filter_complex", ";".join(fl), "-ar", "44100", "-ac", "2", out], check=True)

def build(out):
    S = shots(); total = sum(d for d, _, _ in S); wav = out[:-4] + "_mix.wav"; music(S, total, wav)
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
        panels(a[0], [("FROM BEHIND · SHE WALKS IN", 1.5), ("SHE'S WORRIED", 1.5), ("PUSH-IN", 1.2), ("THE PRESS", 0.8), ("THE PRESS", 1.25), ("THE PRESS", 1.4),
                      ("THE RAID", 1.0), ("S1", 1.0), ("WHY", 1.5)])
    else: build(a[0] if a else "/home/claude/out/wow/wow_v5.mp4")
