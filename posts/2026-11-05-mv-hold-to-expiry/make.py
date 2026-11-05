"""The Band, episode 4: HOLD TO EXPIRY (song: Hold to Expiry, long version; lyric set "Assigned (It's the Plan)"; fake opera into a
trap drop, 123 BPM, 2:55). An opera in one expiry: Penny opens behind red curtains, the band assembles, the lights go off, hearts
drum, up or down, and the calendar tears down to EXPIRY. Verse 2 replays around the office; the long instrumental is the solos;
the big chorus comes back on the roof. No figures anywhere. Lyrics from tools/music/mv_lines.json (never committed).
    python3 make.py <out.mp4> | --panels <sheet.png> | --cover <out.jpg>"""
import os, sys, math, json
HERE = os.path.dirname(os.path.abspath(__file__)); TOOLS = os.path.join(HERE, "..", "..", "tools"); sys.path.insert(0, TOOLS)
os.environ.setdefault("RE_ASSETS_DIR", "/tmp/claude-0/-home-claude/97ad6b31-1277-5795-987d-0d7c1b8393c4/scratchpad/assets3/project")
from PIL import Image, ImageDraw
import musicvideo as MV
from musicvideo import W, H, LIME, INK, RED, GREEN, GOLD, stamp, rig, room, lights, band, mono, fit
g = MV.Grid(123.05, 7.779); END = 174.8; COLOR = "#FF5C5C"; BAR = 4 * g.beat
LINES = json.load(open(os.environ.get("MV_LINES", os.path.join(TOOLS, "music", "mv_lines.json"))))["hold_to_expiry_long"]
TAPE = ["HOLD", "TO EXPIRY", "LIGHTS OFF", "UP?", "DOWN?", "WE HOLD", "NO ROLLS", "HERE WE GO"]

def curtains(img, t, open_k=0.0):
    d = ImageDraw.Draw(img); w = int(W * 0.5 * (1 - open_k))
    for side in (0, 1):
        x0 = 0 if side == 0 else W - w
        d.rectangle([x0, 0, x0 + w, H], fill="#7A1020")
        for k in range(0, w, 60): d.rectangle([x0 + k, 0, x0 + k + 18, H], fill="#5A0A16")
    d.rectangle([0, 0, W, 140], fill="#5A0A16"); d.rectangle([0, 130, W, 150], fill=GOLD)
    return img
def spot(img, cx=540, a=110):
    ov = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(ov); d.polygon([(cx - 60, 150), (cx + 60, 150), (cx + 380, 1560), (cx - 380, 1560)], fill=(255, 245, 210, a))
    d.ellipse([cx - 380, 1500, cx + 380, 1620], fill=(255, 245, 210, a)); return Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
def dark(img, k=0.75):
    return Image.blend(img, Image.new("RGB", img.size, (0, 0, 0)), k)
def flashlight(img, t, cx, cy):
    ov = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(ov); sw = math.sin(t * 2.2) * 160
    d.polygon([(cx, cy), (cx + sw - 260, 380), (cx + sw + 260, 380)], fill=(255, 250, 200, 70)); return Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
def heart(img, t, cx=540, cy=700):
    c = Image.new("RGBA", (W // 10, H // 10)); d = ImageDraw.Draw(c); k = 1 + 0.35 * g.pulse(t); s = int(10 * k); x, y = cx // 10, cy // 10
    d.ellipse([x - s, y - s, x, y], fill=(255, 70, 90, 255)); d.ellipse([x, y - s, x + s, y], fill=(255, 70, 90, 255)); d.polygon([(x - s, y - s // 2), (x + s, y - s // 2), (x, y + s)], fill=(255, 70, 90, 255))
    d.point((x - s // 2, y - s + 2), fill=(255, 200, 210, 255))
    base = img.convert("RGBA"); base.alpha_composite(c.resize((W, H), Image.NEAREST)); return base.convert("RGB")
def updown(img, t):
    d = ImageDraw.Draw(img); up_ = int(g.of(t)) % 2 == 0; col = GREEN if up_ else RED; cx, cy = 540, 680
    pts = [(cx, cy - 260), (cx + 200, cy - 40), (cx + 80, cy - 40), (cx + 80, cy + 220), (cx - 80, cy + 220), (cx - 80, cy - 40), (cx - 200, cy - 40)]
    if not up_: pts = [(x, 2 * cy - y) for x, y in pts]
    d.polygon([(x + 16, y + 16) for x, y in pts], fill="#000000"); d.polygon(pts, fill=col, outline="#000000")
    return stamp(img, "UP?" if up_ else "DOWN?", col, 1100, 120)
def calendar(img, t, u, n_tear=4, cx=540, cy=720):
    d = ImageDraw.Draw(img); w, h = 520, 560; torn = min(n_tear, int(u / 0.6))
    d.rectangle([cx - w // 2 + 16, cy - h // 2 + 16, cx + w // 2 + 16, cy + h // 2 + 16], fill="#000000")
    d.rectangle([cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2], fill="#F4F2EA", outline="#000000", width=8); d.rectangle([cx - w // 2, cy - h // 2, cx + w // 2, cy - h // 2 + 110], fill=COLOR)
    for k in range(6): d.ellipse([cx - w // 2 + 50 + k * 80, cy - h // 2 - 20, cx - w // 2 + 74 + k * 80, cy - h // 2 + 20], fill="#333")
    last = torn >= n_tear; word = "EXPIRY" if last else ["NOT YET", "NOPE", "HOLD", "STILL HOLD"][torn % 4]
    d.text((cx, cy - h // 2 + 55), "CALENDAR", font=mono(44, True), fill="#0B0B0B", anchor="mm")
    d.text((cx, cy + 60), word, font=fit(word, w - 80, 150, wdth=125, wght=900), fill=COLOR if last else "#0B0B0B", anchor="mm")
    if not last:
        k = (u % 0.6) / 0.6; px_ = Image.new("RGBA", (w, h - 110), (244, 242, 234, int(255 * (1 - k)))); px_ = px_.rotate(-k * 25, expand=True)
        img.paste(px_, (int(cx - w // 2 + k * 300), int(cy - h // 2 + 110 + k * 500)), px_)
    return img

# ---------- shots ----------
def s_opera(t, u):
    img = spot(dark(room("ROOM-15", t, 0.3), 0.6)); rig(img, "penny", "talk", t, 540, 1560, 11, False, None, hop=False); img = curtains(img, t, 0.35)
    stamp(img, "AN OPERA", GOLD, 330, 110); return stamp(img, "IN ONE EXPIRY", INK, 470, 80)
def s_title(t, u): return MV.title_card(t, g, ["HOLD TO", "EXPIRY"], COLOR, "ROOM-16")
def s_assemble(t, u):
    img = MV.lights(room("ROOM-03", t, 0.6), t, g); n = 1 + int(u / BAR)
    for ch, cx, feet, k, fl in MV.BAND[: max(1, min(5, n))]: rig(img, ch, "celebrate", t + cx * 0.001, cx, feet, k, fl, g)
    return img
def v_lights(name):
    def f(t, u):
        img = flashlight(dark(room(name, t, 0.5), 0.72), t, 540, 1320); rig(img, "theo", "idle", t, 540, 1460, 8, False, g); return stamp(img, "LIGHTS OFF.", INK, 560, 120)
    return f
def v_heart(name):
    def f(t, u): img = heart(room(name, t, 0.45), t); rig(img, "ada", "celebrate", t, 300, 1460, 7, False, g); rig(img, "kit", "dance", t, 800, 1460, 7, True, g); return img
    return f
def v_updown(name):
    def f(t, u): img = updown(room(name, t, 0.4), t); rig(img, "theo", "shrug", t, 830, 1470, 6, True, g); return img
    return f
def v_calendar(name):
    def f(t, u): img = calendar(room(name, t, 0.4), t, u); rig(img, "roz", "nod", t, 220, 1470, 6, False, g); return img
    return f
def s_roof(t, u): return band(t, g, "ROOM-03", None, 0.66)
def s_chorus(t0):
    def f(t, u): return MV.confetti(band(t, g, "ROOM-03", None, 0.7), t, t0)
    return f
def s_drop(t, u):
    img = band(t, g, "ROOM-19", {"theo": "celebrate", "penny": "celebrate", "ada": "celebrate", "roz": "nod", "kit": "dance"}, 0.6)
    if g.pulse(t) > 0.85: img = Image.blend(img, Image.new("RGB", img.size, (255, 255, 255)), 0.25)
    sh = int(10 * g.pulse(t)); img = img.transform(img.size, Image.AFFINE, (1, 0, sh if int(g.of(t)) % 2 else -sh, 0, 1, 0))
    return stamp(img, "THE DROP.", COLOR, 560, 150) if u < 2.0 else img
def s_decks(t, u): return MV.solo(t, g, "kit", "dance" if int(g.of(t) / 4) % 2 else "play", "ROOM-06", "KIT ON THE DECKS")
def s_drums(t, u): return heart(MV.solo(t, g, "ada", "celebrate", "ROOM-02", "ADA ON DRUMS", "(she counts every beat)"), t, 540, 820)
def s_still(t, u):
    img = MV.lights(room("ROOM-16", t, 0.4), t, g); img = calendar(img, t, u % 2.4, 99, 340, 880); rig(img, "theo", "holdsign", t, 820, 1460, 7, True, g, hop=False)
    return stamp(img, "THEO: STILL HOLDING", LIME, 470, 100)
def s_fine(t, u): return MV.solo(t, g, "roz", "nod", "ROOM-15", "ROZ ON KEYS", "(she read the fine print)")
def s_encore(t, u): return MV.solo(t, g, "penny", "talk", "OFF-PENNY-01", "PENNY: ENCORE?", None)
def s_blackout(t, u):
    img = dark(band(t, g, "ROOM-03", None, 0.6, lit=False), 0.8)
    for cx in (230, 540, 850, 330, 760): img = flashlight(img, t + cx, cx, 1300)
    return stamp(img, "LIGHTS OFF...", INK, 560, 120)
def s_build(t, u):
    img = band(t, g, "ROOM-03", None, 0.66); return stamp(img, "HERE WE GO", LIME, 560, 140) if int(g.of(t)) % 2 == 0 else img
def s_expiry(t, u):
    img = band(t, g, "ROOM-19", None, 0.55); img = calendar(img, t, 99, 0, 540, 640); return img
def s_reprise(t, u):
    img = spot(dark(room("ROOM-15", t, 0.3), 0.6)); rig(img, "penny", "talk", t, 540, 1560, 11, False, None, hop=False); return curtains(img, t, 0.35)
def s_final(t, u): return MV.confetti(band(t, g, "ROOM-03", None, 0.72), t, 160.4)
def s_end(t, u): return MV.end_card(t, g, ["HOLD TO", "EXPIRY"], COLOR, "Rounding Error · The Band", "Puts are never rolled. Follow the band.")

SHOTS = [(0.0, s_opera), (7.8, s_title), (15.5, s_assemble),
         (22.6, v_lights("ROOM-01")), (25.55, v_heart("ROOM-01")), (28.5, v_updown("ROOM-01")), (31.45, v_calendar("ROOM-01")), (34.4, s_roof),
         (38.5, s_chorus(38.5)), (46.6, s_drop), (54.4, s_decks),
         (61.4, v_lights("ROOM-02")), (64.35, v_heart("ROOM-06")), (67.3, v_updown("ROOM-15")), (70.25, v_calendar("ROOM-16")),
         (73.2, s_drums), (81.0, s_still), (88.8, s_fine), (96.6, s_encore), (104.4, s_blackout), (112.2, s_build),
         (119.0, s_chorus(119.0)), (137.8, s_drop), (145.6, s_expiry), (152.3, s_reprise), (156.2, s_build), (160.4, s_final), (169.8, s_end)]
KW = dict(tape_words=TAPE, tape_kw=dict(good=("UP?", "WE HOLD"), bad=("DOWN?",)), end_fn=s_end)

if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if "--panels" in sys.argv: MV.panels(a[0], SHOTS, LINES, g, END, **KW)
    elif "--cover" in sys.argv: MV.cover(a[0], ["HOLD TO", "EXPIRY"], COLOR, curtains(band(40.0, g, "ROOM-03", None, 0.65), 40.0, 0.72))
    else: MV.build(a[0] if a else "/home/claude/out/mv/hold_to_expiry_v1.mp4", "hold_to_expiry_long", SHOTS, LINES, g, END, **KW)
