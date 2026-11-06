"""LET THE RULEBOOK DO THE STRESSING (the boss 2026-11-05: "the market in total turmoil, but my trading runs on rules so I'm chilling,
playing games... use the real trades, real money, make it good").

Every figure is from Theo's close sheet 20261105-160716-close (public_ok): S&P 500 ETF -4.4% on Thu 11/5, no trades Thursday,
HIMS $26 puts in the money, both UBER puts and the HOOD calls out of the money. Dated "Thu 11/5" on screen because it posts later.
Wording kept inside Roz's earlier calls on the WoW video: no "automate", the boss approves every trade, the rules do the work.
The boss appears only as the shadow chimp (never the real-boss sprites). Song: The Clock Pays Rent (in_use), no karaoke.
    python3 make.py <out.mp4> | --panels <sheet.png> | --cover <out.jpg>"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); TOOLS = os.path.join(HERE, "..", "..", "tools"); sys.path.insert(0, TOOLS)
os.environ.setdefault("RE_ASSETS_DIR", "/tmp/claude-0/-home-claude/97ad6b31-1277-5795-987d-0d7c1b8393c4/scratchpad/assets3/project")
from PIL import Image, ImageDraw
import musicvideo as MV, props, earn_recipe
from musicvideo import W, H, LIME, INK, RED, GREEN, GOLD, stamp, rig, room, fit, mono

g = MV.Grid(80.75, 1.579); END = 34.0; SHEET = "20261105-160716-close"
CALM = "#9FB8FF"

def prop(img, label, t, cx, feet, k=8):
    fr, tk = props.frames(earn_recipe.prop_id(label)); u = int(t * 10) % sum(tk); acc = 0; im = fr[-1]
    for f_, n in zip(fr, tk):
        acc += n
        if u < acc: im = f_; break
    im = im.resize((im.width * k, im.height * k), Image.NEAREST); img.paste(im, (int(cx - im.width // 2), int(feet - im.height)), im)

def nfa(img):
    d = ImageDraw.Draw(img); f = mono(24, True); d.rectangle([60, 300, 60 + d.textlength("NOT FINANCIAL ADVICE", font=f) + 24, 340], fill="#000000")
    d.text((72, 320), "NOT FINANCIAL ADVICE", font=f, fill=INK, anchor="lm"); return img

def alarm(img, t, strength=1.0):
    a = int((70 + 60 * (0.5 + 0.5 * math.sin(t * 9))) * strength)
    ov = Image.new("RGBA", (W, H), (255, 40, 40, a)); img = Image.alpha_composite(img.convert("RGBA"), ov)
    d = ImageDraw.Draw(img)
    for i in range(6):                                                       # red pixel ticker slashes across the top band
        y = 160 + i * 18; x = int((t * 900 + i * 210) % (W + 300)) - 300; d.rectangle([x, y, x + 220, y + 8], fill=(255, 92, 92, 200))
    return img.convert("RGB")

def glow(img, cx, cy, r=330, col=(120, 170, 255)):
    """TV light behind the shadow chimp so his silhouette reads on dark rooms."""
    ov = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(ov)
    for i in range(10, 0, -1):
        rr = int(r * i / 10); d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=col + (int(14 + 6 * (10 - i)),))
    return Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")

def calm(img, t):
    ov = Image.new("RGBA", (W, H), (60, 90, 180, 40)); return Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")

def panel(img, rows, foot, u):
    d = ImageDraw.Draw(img); x0, y0, x1 = 80, 470, W - 80; y1 = y0 + 120 + 110 * len(rows)
    d.rectangle([x0, y0, x1, y1], fill="#0B0B0B", outline="#3A3A3A", width=6)
    d.text((x0 + 36, y0 + 60), f"THE BOOK · THU 11/5 CLOSE", font=mono(30, True), fill=LIME, anchor="lm")
    for i, (txt, col) in enumerate(rows):
        a = max(0.0, min(1.0, (u - 0.35 * i) / 0.3))
        if a <= 0: continue
        y = y0 + 150 + 110 * i; f = fit(txt, x1 - x0 - 72, 64, wdth=110, wght=800)
        d.text((x0 + 36, y), txt, font=f, fill=col, anchor="lm")
    d.text((W // 2, y1 + 60), foot, font=mono(30, True), fill=INK, anchor="mm")

# ---------------------------------------------------------------- shots
def s_chaos(t, u):
    img = room("ROOM-01", t, 0.4)
    prop(img, "Chart, down (no figures)", t, 820, 1180, 9)
    rig(img, "ada", "facepalm", t, 300, 1460, 8, False, g, hop=False); rig(img, "penny", "shakehead", t, 640, 1460, 8, True, g, hop=False)
    img = alarm(img, t)
    stamp(img, "THURSDAY.", INK, 520, 90)
    if u > 0.7:
        stamp(img, "S&P 500 ETF", INK, 660, 92); stamp(img, "-4.4%", RED, 820, 210)
        stamp(img, "Thu 11/5 close vs Wed close", INK, 960, 44)
    return nfa(img)

def s_panic(t, u):
    img = room("ROOM-02", t, 0.45)
    x = int(-150 + (u / 3.0) * (W + 300)); rig(img, "penny", "walk", t * 2, x, 1460, 8, False, g, hop=False)
    rig(img, "kit", "facepalm", t, 820, 1460, 7, True, g, hop=False)
    prop(img, "Old TV, static", t, 240, 1290, 9)
    img = alarm(img, t, 1.2)
    stamp(img, "RED SCREENS.", INK, 560, 110)
    if u > 1.0: stamp(img, "TURMOIL.", RED, 720, 170)
    return nfa(img)

def s_meanwhile(t, u):
    img = calm(room("ROOM-07", t, 0.3), t)
    prop(img, "Old TV, static", t, 800, 1250, 10)
    img = glow(img, 430, 1300); rig(img, "boss", "idle", t, 430, 1500, 9, False, g, hop=False)
    prop(img, "Game controller", t, 430 + int(6 * math.sin(t * 14)), 1310, 6)
    prop(img, "Desk coffee", t, 200, 1500, 6)
    stamp(img, "MEANWHILE,", CALM, 520, 100); stamp(img, "THE BOSS:", INK, 660, 130)
    if u > 1.6: stamp(img, "PLAYING GAMES.", LIME, 820, 96)
    return nfa(img)

def s_why(t, u):
    img = calm(room("ROOM-07", t, 0.35), t)
    img = glow(img, 540, 1260, 380); rig(img, "boss", "nod", t, 540, 1500, 11, False, g, hop=False)
    prop(img, "Game controller", t, 540 + int(6 * math.sin(t * 14)), 1250, 7)
    stamp(img, "WHY SO CALM?", INK, 560, 130)
    return nfa(img)

def s_rule(t, u):
    img = room("ROOM-15", t, 0.45)
    rig(img, "theo", "holdsign", t, 540, 1480, 10, False, g, hop=False)
    prop(img, "Ledger", t, 220, 1480, 8)
    stamp(img, "WHAT DOES THE", INK, 470, 92); stamp(img, "RULEBOOK SAY?", INK, 590, 92)
    if u > 1.4: stamp(img, "HOLD TO EXPIRY.", LIME, 760, 120)
    if u > 2.4: stamp(img, "Puts are never rolled.", INK, 880, 56)
    return nfa(img)

def s_book(t, u):
    img = room("ROOM-16", t, 0.62)
    rig(img, "theo", "point", t, 820, 1560, 7, True, g, hop=False)
    panel(img, [("Trades Thursday: 0", INK), ("HIMS $26 puts: in the money", RED), ("UBER puts: out of the money", GREEN),
                ("HOOD calls: out of the money", GREEN)], "The rules already decided all of these.", u)
    return nfa(img)

def s_tap(t, u):
    img = calm(room("ROOM-07", t, 0.35), t)
    img = glow(img, 540, 1290, 360); rig(img, "boss", "shrug", t, 540, 1500, 10, False, g, hop=False)
    prop(img, "Phone", t, 820, 1500, 7)
    stamp(img, "NOTHING TO", INK, 520, 120); stamp(img, "APPROVE TODAY.", LIME, 650, 120)
    stamp(img, "(he taps Approve on every trade)", INK, 780, 46)
    return nfa(img)

def s_raid(t, u):
    img = glow(MV.lights(room("ROOM-19", t, 0.4), t, g), 300, 1330, 260, (255, 210, 120))
    rig(img, "boss", "celebrate", t, 300, 1500, 8, False, g); rig(img, "kit", "dance", t, 560, 1500, 8, False, g); rig(img, "penny", "celebrate", t, 800, 1500, 8, True, g)
    stamp(img, "BACK TO", INK, 560, 110); stamp(img, "THE RAID.", LIME, 700, 150)
    return nfa(img)

def s_end(t, u):
    img = Image.new("RGB", (W, H), "#05060A")
    stamp(img, "LET THE RULEBOOK", INK, 640, 100); stamp(img, "DO THE STRESSING.", LIME, 780, 108)
    stamp(img, "Rounding Error Capital", INK, 960, 54); stamp(img, "An AI-run fund, learning in public.", INK, 1040, 40)
    stamp(img, "LIKE + FOLLOW FOR THE NOTES", LIME, 1180, 56)
    img = glow(img, 750, 1560, 230); rig(img, "theo", "nod", t, 330, 1700, 6, False, g); rig(img, "boss", "idle", t, 750, 1700, 6, True, g)
    return nfa(img)

SHOTS = [(0.0, s_chaos), (4.6, s_panic), (7.6, s_meanwhile), (11.6, s_why), (14.4, s_rule), (19.0, s_book), (24.2, s_tap), (27.4, s_raid), (30.4, s_end)]
KW = dict(karaoke_on=False, end_fn=s_end)

if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if "--panels" in sys.argv: MV.panels(a[0], SHOTS, [], g, END, **KW)
    elif "--cover" in sys.argv: MV.frame_at(9.6, SHOTS, [], g, **KW).save(a[0], quality=92)
    else: MV.build(a[0] if a else "/home/claude/out/rulebook_stress_v1.mp4", "the_clock_pays_rent", SHOTS, [], g, END, **KW)
