"""WoW Forever v4 (the boss 2026-11-04 picked v3 ending E): v3-E plus
  - THE PRESS: after the button appears, a dramatic macro on the desk: the AUTOMATE button and his finger coming down, whole-number
    zoom steps (x20 -> x24 -> x30), speed lines, a flash and a shake on contact ("boop.");
  - the warlock's robe (V2_06BossGear) had see-through gaps: enclosed transparent pixels are filled from the nearest robe pixel;
  - a closing LIKE + FOLLOW card (Kit's neon sign DEC-59) "for more of this";
  - music: one track per act (intro / raid / outro) when the boss sends them (SONGS below); until then v3's cut.
    python3 make_v4.py <out.mp4> | --panels <sheet.png>"""
import os, sys, math, runpy, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
_argv = sys.argv; sys.argv = sys.argv[:1]
V3 = runpy.run_path(os.path.join(HERE, "make_v3.py"), run_name="v3"); sys.argv = _argv
import numpy as np
from scipy import ndimage
from PIL import Image, ImageDraw
import kitpieces as K
from make_reel import W, H, FPS, mono, fit
LIME, INK = V3["LIME"], V3["INK"]
stamp, black, cards, comp = V3["stamp"], V3["black"], V3["cards"], V3["comp"]

# ---- robe fix: fill holes inside the warlock sprite ----
_piece = K.piece; _FIX = {}
def fill_holes(im):
    a = np.array(im.convert("RGBA")); op = a[..., 3] > 0
    holes = ndimage.binary_fill_holes(op) & ~op
    if not holes.any(): return im
    _, (iy, ix) = ndimage.distance_transform_edt(~op, return_indices=True)
    a[holes] = a[iy[holes], ix[holes]]; a[holes, 3] = 255
    return Image.fromarray(a)
def piece(board, t, name=None):
    im = _piece(board, t, name)
    if "BossGear" in str(board):
        key = (id(im),)
        if key not in _FIX: _FIX.clear() if len(_FIX) > 200 else None; _FIX[key] = fill_holes(im)
        return _FIX[key]
    return im
K.piece = piece

# ---- THE PRESS: macro on the button ----
WOOD = [(92, 52, 30), (110, 64, 36), (78, 44, 26)]
def press_canvas(u):
    """54x96 stage px: desk planks, the lime AUTOMATE button (ours), his shadow finger coming down."""
    c = Image.new("RGB", (54, 96), WOOD[0]); d = ImageDraw.Draw(c)
    for y in range(0, 96, 12):
        d.rectangle([0, y, 53, y + 10], fill=WOOD[(y // 12) % 2]); d.line([0, y + 11, 53, y + 11], fill=WOOD[2])
        for x in ((y * 7) % 40 + 6,): d.line([x, y + 3, x + 6, y + 3], fill=WOOD[2])
    press = u >= 0.82; by = 58 + (2 if press else 0)
    d.rectangle([9, 62, 45, 78], fill=(40, 52, 16))                                   # button housing shadow
    d.rectangle([9, by - 4, 45, by + 12], fill=(122, 150, 30) if press else (200, 240, 60), outline=(20, 24, 8))
    d.line([10, by - 3, 44, by - 3], fill=(230, 255, 140)) if not press else None
    e = max(0.0, min(1.0, (u - 0.12) / 0.70)); tip = int(4 + e * e * (by - 8))          # finger enters early, accelerates onto the cap
    col, rim = (20, 20, 42), (52, 52, 86)
    if u < 0.12: return c, by
    f0 = max(-2, tip - 22)                                                           # index finger, 8 px wide, 22 long
    d.rectangle([24, f0, 31, tip - 2], fill=col); d.rectangle([25, tip - 2, 30, tip], fill=col)
    d.line([23, f0, 23, tip - 2], fill=rim); d.line([32, f0, 32, tip - 2], fill=rim); d.line([25, tip, 30, tip], fill=rim)
    d.rectangle([26, tip - 7, 29, tip - 4], fill=(40, 40, 70))                        # nail
    for j in (f0 - 1, f0 - 7):                                                        # knuckle creases
        d.line([25, j + 10, 30, j + 10], fill=(34, 34, 60)) if j + 10 < tip - 8 else None
    if f0 > -2: d.rectangle([16, -2, 39, f0 + 2], fill=col); d.line([15, -2, 15, f0 + 2], fill=rim); d.line([40, -2, 40, f0 + 2], fill=rim)   # the fist
    return c, by
def the_press(t, u):
    u = u / 1.6; c, by = press_canvas(u)
    k, (cw, ch) = (20, (54, 96)) if u < 0.45 else (24, (45, 80)) if u < 0.75 else (30, (36, 64))
    x0 = (54 - cw) // 2; y0 = max(0, min(96 - ch, by + 18 - ch))                 # button low, finger in frame
    img = c.crop((x0, y0, x0 + cw, y0 + ch)).resize((cw * k, ch * k), Image.NEAREST)
    if u >= 0.82 and u < 0.9: img = Image.blend(img, Image.new("RGB", img.size, (255, 255, 255)), 0.55)
    if u >= 0.82:
        s = int(16 * max(0, 1 - (u - 0.82) / 0.18)); img = img.transform(img.size, Image.AFFINE, (1, 0, (s if int(u * 60) % 2 else -s), 0, 1, 0))
    d = ImageDraw.Draw(img)
    bx = (by - 4 - y0) * k                                                            # button cap top in screen px
    d.text((W // 2, bx + 8 * k * (1 if k < 30 else 1)), "AUTOMATE", font=fit("AUTOMATE", int(34 * k * 0.8), int(7 * k), wdth=125, wght=900), fill="#0B0B0B", anchor="mm")
    if u < 0.82:
        for i in range(10):                                                           # speed lines toward the button
            a = i / 10 * math.pi * 2; r0 = 700 - (u * 900 + i * 37) % 300; r1 = r0 + 120
            cx, cy = W // 2, bx
            d.line([cx + math.cos(a) * r0, cy + math.sin(a) * r0, cx + math.cos(a) * r1, cy + math.sin(a) * r1], fill=INK, width=6)
    else:
        stamp(img, "boop.", INK, 330, 150)
    return img

def cta(t, u):
    img = black(); n = K.piece("DEC-59", t); k = max(1, min(900 // n.width, 700 // n.height))
    sg = n.resize((n.width * k, n.height * k), Image.NEAREST); glow = 1 if int(u * 6) % 4 else 0
    img.paste(sg, (W // 2 - sg.width // 2, 760 - sg.height // 2), sg)
    stamp(img, "FOR MORE OF THIS.", LIME if glow else INK, 1260, 110)
    return img

def shots():
    S = V3["shots"]("E"); out = []
    for dur, lab, fn in S:
        out.append((dur, lab, fn))
        if lab == "MUST AUTOMATE": out.append((1.6, "THE PRESS", the_press))
    i = [l for _, l, _ in out].index("THE BUTTON"); out.pop(i)                       # the macro IS the button now
    return out + [(2.2, "LIKE + FOLLOW", cta)]

SONGS = {}   # "intro" / "raid" / "outro": paths to the boss's Gemini tracks; empty = v3's cut
def music(S, total, out):
    if not SONGS: return V3["song"](total, out)
    t, marks = 0, {}
    for dur, lab, _ in S:
        if lab == "THE RAID": marks["raid"] = t
        if lab == "HONEY...": marks["outro"] = t
        t += dur
    parts = [("intro", 0, marks["raid"]), ("raid", marks["raid"], marks["outro"]), ("outro", marks["outro"], total)]
    inp, fl = [], []
    for n, (key, a, b) in enumerate(parts):
        inp += ["-i", SONGS[key]]; fl.append(f"[{n}]atrim=0:{b - a + 0.25:.3f},asetpts=PTS-STARTPTS,afade=t=out:st={b - a - 0.05:.3f}:d=0.3,adelay={int(a * 1000)}|{int(a * 1000)}[s{n}]")
    fl.append(f"[s0][s1][s2]amix=inputs=3:normalize=0,atrim=0:{total:.3f},afade=t=out:st={total - 1.0:.3f}:d=1.0")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inp, "-filter_complex", ";".join(fl), "-ar", "44100", out], check=True)

def build(out):
    S = shots(); total = sum(d for d, _, _ in S); wav = out[:-4] + "_mix.wav"; music(S, total, wav)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "20",
        "-c:a", "aac", "-b:a", "160k", "-af", "loudnorm=I=-14:TP=-1.5", "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
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
        panels(a[0], [("THE PRESS", 0.2), ("THE PRESS", 0.9), ("THE PRESS", 1.25), ("THE PRESS", 1.4), ("THE RAID", 1.0), ("PARTY WIPED", 0.3), ("LIKE + FOLLOW", 1.0)])
    else: build(a[0] if a else "/home/claude/out/wow/wow_v4_E.mp4")
