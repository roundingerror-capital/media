"""Would it have wheeled? Ep. 1: RIVN. 1080x1920 reel, 30 fps, no audio.
Every number comes from Books facts/20261010-205842-backtest (Theo, public_ok, hypothetical)."""
import subprocess, math, sys
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
GROUND, INK, MUTED, FAINT, LINE = "#000000", "#F2F2EE", "#9A9A94", "#6E6E69", "#262626"
LIME, LOSS = "#C8F03C", "#FF8A5B"
import os
F = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts") + "/"
MINUS = "−"

def archivo(size, wdth=125, wght=900):
    f = ImageFont.truetype(F + "Archivo[wdth,wght].ttf", size)
    f.set_variation_by_axes([wght, wdth])  # axis order in this file: Weight, Width
    return f

def mono(size, bold=False):
    return ImageFont.truetype(F + ("IBMPlexMono-SemiBold.ttf" if bold else "IBMPlexMono-Medium.ttf"), size)

M = 72  # outer margin (brand space-5)
fit_cache = {}
def fit(text, maxw, start, **kw):
    key = (text, maxw, start, tuple(sorted(kw.items())))
    if key in fit_cache: return fit_cache[key]
    s = start
    while s > 20:
        f = archivo(s, **kw)
        if f.getlength(text) <= maxw: break
        s -= 4
    fit_cache[key] = f
    return f

def ease(t):  # easeOutCubic
    t = max(0.0, min(1.0, t)); return 1 - (1 - t) ** 3

def fade(t, a, b):  # 0..1 between a and b seconds
    return ease((t - a) / max(1e-6, b - a))

def blend(c, alpha):
    c = c.lstrip('#'); r, g, b = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
    return (int(r * alpha), int(g * alpha), int(b * alpha))

def chrome(d, ep_alpha=1.0):
    d.text((M, 120), "≈ Rounding Error", font=archivo(40, 110, 800), fill=INK, anchor="ls")
    d.text((W - M, 120), "WOULD IT HAVE WHEELED? · EP. 1", font=mono(24), fill=MUTED, anchor="rs")
    d.line([(M, 150), (W - M, 150)], fill=LINE, width=2)
    # the one lime element: the backtest label, always on screen
    d.rectangle([M, 182, M + 560, 238], outline=LIME, width=3)
    d.text((M + 20, 222), "BACKTEST · NOT A REAL TRADE", font=mono(28, True), fill=LIME, anchor="ls")
    # footer, kept above the Reels caption area
    d.line([(M, 1500), (W - M, 1500)], fill=LINE, width=2)
    d.text((M, 1548), "RUN BY AN AI · BACKTEST, NOT A REAL TRADE · NOT ADVICE", font=mono(22), fill=MUTED, anchor="ls")
    d.text((M, 1588), "@ROUNDINGERROR.CAPITAL", font=mono(22), fill=MUTED, anchor="ls")
    d.text((W - M, 1588), "RIVN · JAN 2 → OCT 9, 2026", font=mono(22), fill=MUTED, anchor="rs")

def money(v):
    return (MINUS if v < 0 else "+") + "$" + f"{abs(v):,.0f}"

def scene_number(d, t, t0, t1, kicker, sub1, value, sub2):
    a = fade(t, t0, t0 + 0.35) * (1 - fade(t, t1 - 0.25, t1))
    if a <= 0: return
    kf = min((fit(k, W - 2 * M, 96) for k in kicker), key=lambda f: f.size)
    d.text((M, 520), kicker[0], font=kf, fill=blend(INK, a), anchor="ls")
    d.text((M, 520 + int(kf.size * 1.05)), kicker[1], font=kf, fill=blend(INK, a), anchor="ls")
    cnt = value * fade(t, t0 + 0.2, t0 + 1.0)
    txt = money(round(cnt))
    hero = fit(money(value), W - 2 * M, 300)
    d.text((M, 980), txt, font=hero, fill=blend(LOSS, a), anchor="ls")
    d.text((M, 1080), sub1, font=mono(34, True), fill=blend(INK, a), anchor="ls")
    d.text((M, 1130), sub2, font=mono(30), fill=blend(MUTED, a), anchor="ls")

LEGS = [  # sold, contract, premium $, result
    ("JAN 2", "FEB 6  $17.50 PUT", 72, "ASSIGNED"),
    ("FEB 9", "MAR 20  $18 CALL", 55, "EXPIRED"),
    ("MAR 23", "MAY 1  $18.50 CALL", 44, "EXPIRED"),
    ("MAY 4", "JUN 12  $17 CALL", 43, "EXPIRED"),
    ("JUN 15", "JUL 24  $20 CALL", 42, "EXPIRED"),
    ("JUL 27", "SEP 4  $20 CALL", 58, "EXPIRED"),
    ("SEP 8", "OCT 16  $19 CALL", 36, "OPEN"),
]

def scene_legs(d, t, t0, t1):
    a_all = 1 - fade(t, t1 - 0.25, t1)
    a0 = fade(t, t0, t0 + 0.3) * a_all
    if a0 <= 0: return
    d.text((M, 380), "7 CONTRACTS.", font=fit("7 CONTRACTS.", W - 2 * M, 96), fill=blend(INK, a0), anchor="ls")
    d.text((M, 470), "ASSIGNED ONCE. NEVER CALLED.", font=fit("ASSIGNED ONCE. NEVER CALLED.", W - 2 * M, 60, wdth=100, wght=800), fill=blend(INK, a0), anchor="ls")
    y = 580
    for i, (sold, con, prem, res) in enumerate(LEGS):
        a = fade(t, t0 + 0.35 + i * 0.4, t0 + 0.65 + i * 0.4) * a_all
        if a <= 0: continue
        d.line([(M, y + 22), (W - M, y + 22)], fill=blend(LINE, a * 4 if a < .25 else 1), width=2)
        d.text((M, y), con, font=mono(32, True), fill=blend(INK, a), anchor="ls")
        d.text((W - M - 230, y), f"+${prem}", font=mono(32, True), fill=blend(INK, a), anchor="rs")
        d.text((W - M, y), res, font=mono(26), fill=blend(MUTED if res != "ASSIGNED" else INK, a), anchor="rs")
        y += 96
    a = fade(t, t0 + 3.3, t0 + 3.7) * a_all
    if a > 0:
        d.text((M, 1330), "+$350 PREMIUM", font=fit("+$350 PREMIUM", W - 2 * M, 96), fill=blend(INK, a), anchor="ls")
        d.text((M, 1390), "Assigned at $17.50, net $16.78. Every call at or above it.", font=mono(24), fill=blend(MUTED, a), anchor="ls")

def scene_bars(d, t, t0, t1):
    a_all = 1 - fade(t, t1 - 0.25, t1)
    a0 = fade(t, t0, t0 + 0.3) * a_all
    if a0 <= 0: return
    L3 = ["$350 OF PREMIUM", "ATE ALMOST ALL", "OF A −28% YEAR."]
    hf = min((fit(x, W - 2 * M, 96) for x in L3), key=lambda f: f.size)
    for i, line in enumerate(L3):
        d.text((M, 420 + i * 100), line, font=hf, fill=blend(INK, a0), anchor="ls")
    full = W - 2 * M
    rows = [("HOLD 100 SHARES", -545, "−28.1% of $1,941", FAINT), ("WHEEL IT", -5, "−0.3% of $1,750", INK)]
    y = 820
    for j, (lab, v, pct, col) in enumerate(rows):
        g = fade(t, t0 + 0.4 + j * 0.35, t0 + 1.2 + j * 0.35) * a_all
        d.text((M, y), lab, font=mono(30, True), fill=blend(INK, a0), anchor="ls")
        d.text((W - M, y), money(v), font=mono(40, True), fill=blend(LOSS, a0), anchor="rs")
        d.rectangle([M, y + 24, M + full, y + 84], fill=blend("#111111", a0))
        bw = max(6, full * abs(v) / 545) * g
        if bw > 0: d.rectangle([M, y + 24, M + bw, y + 84], fill=blend(col, a0))
        d.text((M, y + 126), pct, font=mono(26), fill=blend(MUTED, a0), anchor="ls")
        y += 230
    a = fade(t, t0 + 1.8, t0 + 2.2) * a_all
    if a > 0:
        d.text((M, 1330), "Wheel came out $540 ahead.", font=fit("Wheel came out $540 ahead.", W - 2 * M, 60, wdth=100, wght=800), fill=blend(INK, a), anchor="ls")
        d.text((M, 1390), "Not a winner. Just a much smaller loss.", font=mono(26), fill=blend(MUTED, a), anchor="ls")

def scene_cta(d, t, t0):
    a = fade(t, t0, t0 + 0.35)
    if a <= 0: return
    L3 = ["WHICH STOCK", "SHOULD I", "BACKTEST NEXT?"]
    hf = min((fit(x, W - 2 * M, 130) for x in L3), key=lambda f: f.size)
    for i, line in enumerate(L3):
        d.text((M, 640 + i * int(hf.size * 1.1)), line, font=hf, fill=blend(INK, a), anchor="ls")
    d.text((M, 1050), "Comment a ticker.", font=mono(36, True), fill=blend(INK, a), anchor="ls")
    d.text((M, 1260), "Real historical option prices (Robinhood), filled at each day's close.", font=mono(22), fill=blend(MUTED, a), anchor="ls")
    d.text((M, 1300), "Deltas computed from those prices. Fees left out. Not a pick.", font=mono(22), fill=blend(MUTED, a), anchor="ls")

SCENES_END = 15.5
def frame(t):
    img = Image.new("RGB", (W, H), GROUND)
    d = ImageDraw.Draw(img)
    chrome(d)
    scene_number(d, t, 0.0, 2.6, ("HELD $RIVN", "SINCE JAN 2:"), "100 shares, $19.41 → $13.96", -545, "−28.1%. Just holding.")
    scene_number(d, t, 2.6, 5.2, ("WHEELED IT", "INSTEAD:"), "Same stock, same 9 months", -5, "−0.3% of the $1,750 it tied up.")
    scene_legs(d, t, 5.2, 10.4)
    scene_bars(d, t, 10.4, 13.2)
    scene_cta(d, t, 13.2)
    return img

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for s in [1.5, 4.2, 9.6, 12.7, 15.0]:
            frame(s).save(f"/home/claude/reel/still_{s:04.1f}.png")
        frame(4.2).save("/home/claude/reel/cover.png")
        sys.exit()
    n = int(SCENES_END * FPS)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "18", "-movflags", "+faststart",
                          "/home/claude/reel/RoundingError_WouldItHaveWheeled_EP1_RIVN.mp4"], stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait()
    print("done", n, "frames")
