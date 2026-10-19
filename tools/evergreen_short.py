"""Evergreen no-number Shorts (Penny). 1080x1920, 30 fps, original synth track.
Usage: python3 tools/evergreen_short.py <key> [stills] [outdir]
No figures on screen by design (theo_check.no_numbers)."""
import os, sys, math, subprocess, wave, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
from make_reel import W, H, FPS, archivo, mono, fit, fade, blend
M = 72; LIME = "#C8F03C"; INK = "#F2F2EE"; MUT = "#9A9A94"; LINE = "#262626"
HERE = os.path.dirname(os.path.abspath(__file__))
SP = {n: Image.open(os.path.join(HERE, "sprites", f"{n}_sprite_1x.png")).convert("RGBA") for n in ("theo", "penny", "ada")}
SC = 7
def river_teal(im):
    # repo sprite predates Ada's final colour (River teal, V11): rotate saturated hues to teal
    import colorsys
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if not a: continue
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            if s > 0.18:
                h = 0.49; s = min(1, s * 0.85)
                r, g, b = (int(c * 255) for c in colorsys.hsv_to_rgb(h, s, v))
                px[x, y] = (r, g, b, a)
    return im
SP["ada"] = river_teal(SP["ada"])
SPB = {n: s.resize((s.width * SC, s.height * SC), Image.NEAREST) for n, s in SP.items()}
XC = {"penny": 0.22, "theo": 0.50, "ada": 0.78}
BASE = 1660

# scene: (t0, t1, kicker, [(headline, color)], [body lines], [(ts, te, who, line)], cast, hl_body_idx)
SPECS = {
 "the-wall": dict(label="BEHIND THE SCENES", end=22.0, bpm=104, mel=[523.3, 659.3, 784.0, 659.3, 587.3, 523.3, 587.3, 0],
  foot="RUN BY AN AI · REAL MONEY · NOT ADVICE", scenes=[
   (0.0, 5.2, "A QUESTION FROM MARKETING", [("Can the", INK), ("marketing AI", INK), ("make a trade?", LIME)], [],
    [(0.6, 2.6, "penny", "Asking for me."), (2.8, 5.0, "penny", "Just one. Tiny.")], ["penny"], -1),
   (5.4, 10.8, "SHORT ANSWER", [("No.", LIME)], ["Theo trades. Penny posts.", "A wall in between."],
    [(5.8, 8.0, "theo", "No."), (8.2, 10.6, "theo", "Still no.")], ["penny", "theo"], -1),
   (11.0, 17.0, "THE WALL", [("The rules", INK), ("nobody bends.", LIME)],
    ["Penny never touches the money.", "Theo never reads the likes.", "Every number in a post comes", "from Theo's notes. Or it stays out."],
    [(11.6, 13.8, "penny", "Can I spice it up?"), (14.0, 16.8, "theo", "Spice is not a strategy.")], ["penny", "theo"], 2),
   (17.2, 22.0, "WHY", [("Boring", INK), ("by design.", LIME)], ["Likes never move a trade.", "Follow anyway."],
    [(17.6, 19.6, "ada", "All green!"), (19.8, 21.8, "penny", "Link in bio, besties.")], ["penny", "theo", "ada"], -1),
  ]),
 "no-dip-buying": dict(label="LESSONS · NO MATH", end=22.0, bpm=96, mel=[440.0, 523.3, 659.3, 523.3, 493.9, 440.0, 392.0, 0],
  foot="RUN BY AN AI · REAL MONEY · NOT ADVICE", scenes=[
   (0.0, 5.2, "THE DIP IS HERE", [("Why won't", INK), ("an AI", INK), ("buy the dip?", LIME)], [],
    [(0.6, 2.6, "penny", "Everyone's buying!"), (2.8, 5.0, "theo", "We don't buy.")], ["penny", "theo"], -1),
   (5.4, 11.0, "WHAT WE DO INSTEAD", [("We get paid", INK), ("to wait.", LIME)],
    ["Sell a cash-secured put.", "Collect the premium up front.", "Hold to expiry. No rolls."],
    [(6.0, 8.2, "theo", "Premium collected."), (8.4, 10.8, "theo", "Moving on.")], ["theo"], 1),
   (11.2, 17.0, "IF IT KEEPS DROPPING", [("We get assigned.", INK), ("On purpose.", LIME)],
    ["We own the shares at a price", "we picked before the drop.", "Then we sell covered calls", "at or above what we paid."],
    [(11.8, 14.0, "penny", "So... a plan?"), (14.2, 16.8, "theo", "Assignment is the plan.")], ["penny", "theo"], -1),
   (17.2, 22.0, "THE WHEEL, IN ONE LINE", [("We don't chase.", INK), ("We get chased.", LIME)], ["Save this for the next dip."],
    [(17.6, 19.6, "penny", "Hot."), (19.8, 21.8, "theo", "Accurate.")], ["penny", "theo"], -1),
  ]),
 "after-the-bell": dict(label="MASCOT MOMENT", end=22.0, bpm=112, mel=[659.3, 784.0, 880.0, 784.0, 659.3, 587.3, 659.3, 0],
  foot="RUN BY AN AI · REAL MONEY · NOT ADVICE", scenes=[
   (0.0, 5.2, "THE MARKET JUST CLOSED", [("What do AIs do", INK), ("after the", INK), ("closing bell?", LIME)], [],
    [(0.6, 2.8, "penny", "Party?"), (3.0, 5.0, "theo", "Paperwork.")], ["penny", "theo", "ada"], -1),
   (5.4, 9.8, "THEO", [("Writes it", INK), ("all down.", LIME)], ["Every fill, every mark, with", "its source and its time."],
    [(5.8, 9.6, "theo", "Facts. No feelings.")], ["theo"], -1),
   (10.0, 14.2, "ADA", [("Checks the", INK), ("pipes.", LIME)], ["Every table, every test.", "Every bug gets a fix."],
    [(10.4, 12.2, "ada", "All green!"), (12.4, 14.0, "ada", "Best part of my day!")], ["ada"], -1),
   (14.4, 18.4, "PENNY", [("Makes it", INK), ("pretty.", LIME)], ["Then waits. Nothing goes out", "without the boss's yes."],
    [(14.8, 18.2, "penny", "Consent is hot, besties.")], ["penny"], -1),
   (18.6, 22.0, "THEN", [("Same rules", INK), ("tomorrow.", LIME)], ["Follow for the receipts."],
    [(19.0, 21.8, "theo", "Carry on.")], ["penny", "theo", "ada"], -1),
  ]),
}

def bubble(d, xc, y, txt):
    f = mono(32, True); tw = int(f.getlength(txt)); bw, bh = tw + 44, 72
    bx = int(min(max(M, xc - bw / 2), W - M - bw))
    d.rectangle([bx, y, bx + bw, y + bh], fill=INK); d.rectangle([bx + 4, y + 4, bx + bw - 5, y + bh - 5], outline="#1A1A1A", width=4)
    d.polygon([(xc - 14, y + bh), (xc + 14, y + bh), (xc, y + bh + 18)], fill=INK)
    d.text((bx + 22, y + 49), txt, font=f, fill="#000000", anchor="ls")

def frame(S, t):
    img = Image.new("RGB", (W, H), "#000000"); d = ImageDraw.Draw(img)
    d.text((M, 120), "≈ Rounding Error", font=archivo(40, 110, 800), fill=INK, anchor="ls")
    d.text((W - M, 120), S["label"], font=mono(24), fill=MUT, anchor="rs")
    d.line([(M, 150), (W - M, 150)], fill=LINE, width=2)
    for k, (t0, t1, kick, heads, body, lines, cast, hl) in enumerate(S["scenes"]):
        a_in = 1.0 if k == 0 else fade(t, t0, t0 + 0.3)
        a_out = 1.0 if k == len(S["scenes"]) - 1 else 1 - fade(t, t1 - 0.2, t1 + 0.1)
        a = a_in * a_out
        if a <= 0 or t < t0: continue
        d.text((M, 290), kick, font=mono(30, True), fill=blend(LIME if k == 0 else MUT, a), anchor="ls")
        longest = max((h for h, _ in heads), key=len)
        f = fit(longest, W - 2 * M, 150 if len(heads) == 1 else 128, wdth=110, wght=900)
        y = 300 + int(f.size * 1.05)
        for i, (h, c) in enumerate(heads):
            ha = a if k == 0 else a * fade(t, t0 + i * 0.15, t0 + 0.35 + i * 0.15)
            d.text((M, y), h, font=f, fill=blend(c, ha), anchor="ls"); y += int(f.size * 1.05)
        y += 40
        for i, ln in enumerate(body):
            ba = a * fade(t, t0 + 0.6 + i * 0.35, t0 + 0.9 + i * 0.35)
            d.text((M, y), ln, font=mono(38, True), fill=blend(LIME if i == hl or (hl >= 0 and i == hl + 1 and k == 2 and S is SPECS["the-wall"]) else INK, ba), anchor="ls"); y += 62
        for n in cast:
            s = SPB[n]; xc = int(W * XC[n])
            talking = any(ts <= t < te and w == n for ts, te, w, _ in lines)
            hop = int(abs(math.sin((t * 2.4) * math.pi)) * 22) if talking else (SC if int(t * 2) % 2 else 0)
            sa = a
            if sa < 1:
                tmp = s.copy(); al = tmp.getchannel("A").point(lambda p: int(p * sa)); tmp.putalpha(al)
            else: tmp = s
            d.ellipse([xc - s.width * 0.35, BASE - 8, xc + s.width * 0.35, BASE + 14], fill=blend("#1a1a1a", a))
            img.paste(tmp, (xc - s.width // 2, BASE - s.height - hop), tmp)
        for ts, te, w, ln in lines:
            if ts <= t < te and a > 0.5:
                bubble(d, int(W * XC[w]), BASE - SPB[w].height - 120, ln)
    d.line([(M, 1720), (W - M, 1720)], fill=LINE, width=2)
    d.text((M, 1768), S["foot"], font=mono(22), fill=MUT, anchor="ls")
    d.text((M, 1806), "@ROUNDINGERROR.CAPITAL", font=mono(22), fill=MUT, anchor="ls")
    return img

def track(S, path, seed=1):
    rng = np.random.default_rng(seed); SR = 44100; END = S["end"]; BEAT = 60 / S["bpm"]
    N = int(SR * (END + 0.5)); out = np.zeros(N); tt = lambda n: np.arange(n) / SR
    def add(sig, at):
        i = int(at * SR); j = min(N, i + len(sig))
        if i < N: out[i:j] += sig[:j - i]
    def kick():
        n = int(.3 * SR); t = tt(n); f = 50 + 100 * np.exp(-t * 30); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9) * 0.9
    def clap():
        n = int(.2 * SR); t = tt(n); return rng.standard_normal(n) * np.exp(-t * 22) * 0.3
    def hat():
        n = int(.04 * SR); t = tt(n); x = np.diff(np.concatenate([[0], rng.standard_normal(n)])); return x * np.exp(-t * 90) * 0.1
    def pluck(f, l):
        n = int(l * SR); t = tt(n); return (np.sin(2 * np.pi * f * t) + 0.4 * np.sin(4 * np.pi * f * t)) * np.exp(-t * 6) * 0.16
    def bass(f, l):
        n = int(l * SR); t = tt(n); return (np.sign(np.sin(2 * np.pi * f * t)) * 0.3 + np.sin(2 * np.pi * f * t) * 0.5) * np.minimum(1, t * 200) * np.exp(-t * 3) * 0.3
    bl = [S["mel"][0] / 8, S["mel"][0] / 8, S["mel"][2] / 8, S["mel"][1] / 8]
    for k in range(int(END / BEAT)):
        t0 = k * BEAT; add(kick(), t0)
        if k % 2 == 1: add(clap(), t0)
        add(hat(), t0 + BEAT / 2); add(bass(bl[(k // 2) % 4], BEAT * 0.9), t0)
        f = S["mel"][k % 8]
        if k >= 4 and f: add(pluck(f, BEAT * 0.8), t0 + BEAT / 2)
    fo = int(1.2 * SR); out[-fo:] *= np.linspace(1, 0, fo); out = out / np.max(np.abs(out)) * 0.6
    data = (np.stack([out, out], 1) * 32767).astype(np.int16)
    w = wave.open(path, "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(data.tobytes()); w.close()

if __name__ == "__main__":
    key = sys.argv[1]; S = SPECS[key]
    outdir = sys.argv[3] if len(sys.argv) > 3 else "."
    if len(sys.argv) > 2 and sys.argv[2] == "stills":
        ts = [0.0, 3.0, 7.5, 13.5, 16.0, 20.0]; sh = Image.new("RGB", (len(ts) * 270, 480))
        for i, s in enumerate(ts): sh.paste(frame(S, s).resize((270, 480)), (i * 270, 0))
        sh.save(os.path.join(outdir, f"{key}_contact.png")); frame(S, 0.0).save(os.path.join(outdir, f"{key}_frame1.png")); sys.exit()
    wav = os.path.join(outdir, f"{key}_track.wav"); track(S, wav, seed=len(key))
    out = os.path.join(outdir, key.replace("-", "_") + "_short.mp4")
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", wav,
        "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "20", "-c:a", "aac", "-b:a", "160k",
        "-af", "loudnorm=I=-14:TP=-1.5", "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for i in range(int(S["end"] * FPS)): p.stdin.write(frame(S, i / FPS).tobytes())
    p.stdin.close(); p.wait(); os.remove(wav); print(out)
