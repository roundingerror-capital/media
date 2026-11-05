"""The Band, episode 3: ONLY ON PAPER (song: Only on Paper, lyric set "Down Bad (On Paper)"; slow build with a drop, 123 BPM).
A red week that's only on paper: the chart drawn on a sheet of paper, Mark says ouch, Expiry says later, nothing sold, nothing
rolled, Theo's rulebook, and the band waiting for the sun to rise. Verse 2 replays the verse around town (subway, bodega, break
room, boardroom); the bridge is an order on hold; the sun comes up at the end. No figures anywhere.
Lyrics come from tools/music/mv_lines.json (the songs row; never committed).
    python3 make.py <out.mp4> | --panels <sheet.png> | --cover <out.jpg>"""
import os, sys, math, json
HERE = os.path.dirname(os.path.abspath(__file__)); TOOLS = os.path.join(HERE, "..", "..", "tools"); sys.path.insert(0, TOOLS)
os.environ.setdefault("RE_ASSETS_DIR", "/tmp/claude-0/-home-claude/97ad6b31-1277-5795-987d-0d7c1b8393c4/scratchpad/assets3/project")
from PIL import Image, ImageDraw
import musicvideo as MV
from musicvideo import W, H, LIME, INK, RED, GREEN, GOLD, stamp, rig, room, lights, band, mono, fit
g = MV.Grid(123.05, 0.116); END = 125.0; COLOR = "#FF8FB1"
LINES = json.load(open(os.environ.get("MV_LINES", os.path.join(TOOLS, "music", "mv_lines.json"))))["only_on_paper"]
TAPE = ["ON PAPER", "UNREALIZED", "MARK: OUCH", "EXPIRY: LATER", "SOLD: NO", "ROLLED: NO", "RULEBOOK", "WAITING"]

def paper_chart(img, t, u, cx=540, cy=720, s=1.0):
    """A sheet of paper with a red line drawn going down, in pencil. No axis, no figures."""
    d = ImageDraw.Draw(img); w, h = int(640 * s), int(460 * s); x0, y0 = cx - w // 2, cy - h // 2
    d.rectangle([x0 + 14, y0 + 14, x0 + w + 14, y0 + h + 14], fill="#000000"); d.rectangle([x0, y0, x0 + w, y0 + h], fill="#F4EEDB", outline="#000000", width=8)
    for yy in range(y0 + 60, y0 + h - 20, int(44 * s)): d.line([x0 + 20, yy, x0 + w - 20, yy], fill="#C9D6E8", width=3)
    d.line([x0 + int(70 * s), y0 + 10, x0 + int(70 * s), y0 + h - 10], fill="#E8A0A0", width=3)
    k = min(1.0, u / 1.6); pts = []
    for i in range(int(12 * k) + 1):
        xx = x0 + int(90 * s) + i * (w - int(130 * s)) / 12; yy = y0 + int(90 * s) + i * (h - int(170 * s)) / 12 + (18 * s if i % 2 else -10 * s)
        pts.append((xx, yy))
    if len(pts) > 1: d.line(pts, fill="#E23B3B", width=int(12 * s), joint="curve")
    d.text((x0 + w - int(30 * s), y0 + h - int(36 * s)), "ON PAPER", font=mono(int(40 * s), True), fill="#444", anchor="rm")
    return img
def speech(img, x, y, who, what, col):
    d = ImageDraw.Draw(img); f = fit(what, 380, 96, wdth=125, wght=900); w = int(max(f.getlength(what), 260)) + 70
    d.rectangle([x - w // 2, y - 90, x + w // 2, y + 70], fill="#000000", outline=col, width=8); d.polygon([(x - 30, y + 66), (x + 10, y + 66), (x - 40, y + 120)], fill=col)
    d.text((x, y - 50), who, font=mono(40, True), fill=INK, anchor="mm"); d.text((x, y + 18), what, font=f, fill=col, anchor="mm")
def mark_expiry(img, t, u):
    speech(img, 300, 560, "MARK", "OUCH.", "#FF5C5C")
    if u > 1.6: speech(img, 780, 860, "EXPIRY", "LATER.", LIME)
    return img
def checklist(img, t, u, x0=200, y0=520):
    d = ImageDraw.Draw(img); rows = [("SELL?", "NO"), ("ROLL?", "NO"), ("CRY?", "(MUCH)")]; f = fit("ROLL?", 360, 110, wdth=125, wght=900)
    d.rectangle([x0 - 40, y0 - 60, W - x0 + 40, y0 + 3 * 170 - 40], fill="#05060A", outline=INK, width=6)
    for i, (q, a) in enumerate(rows):
        if u < i * 1.25: break
        y = y0 + i * 170 + 40; d.text((x0, y), q, font=f, fill=INK, anchor="lm")
        if a == "NO":
            d.rectangle([W - x0 - 140, y - 60, W - x0 - 20, y + 60], outline=RED, width=10); d.line([W - x0 - 125, y - 45, W - x0 - 35, y + 45], fill=RED, width=14); d.line([W - x0 - 35, y - 45, W - x0 - 125, y + 45], fill=RED, width=14)
        else: d.text((W - x0 - 20, y), a, font=fit(a, 260, 70, wdth=110, wght=900), fill=GOLD, anchor="rm")
    return img
def rulebook(img, t, cx=540, cy=620):
    d = ImageDraw.Draw(img); w, h = 420, 520
    d.rectangle([cx - w // 2 + 16, cy - h // 2 + 16, cx + w // 2 + 16, cy + h // 2 + 16], fill="#000000")
    d.rectangle([cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2], fill="#1F3B2B", outline="#000000", width=8); d.rectangle([cx - w // 2 + 20, cy - h // 2, cx - w // 2 + 44, cy + h // 2], fill="#14281D")
    d.text((cx + 10, cy - 90), "THE", font=mono(52, True), fill=GOLD, anchor="mm"); d.text((cx + 10, cy + 0), "RULE", font=fit("RULE", 300, 120, wdth=125, wght=900), fill=GOLD, anchor="mm")
    d.text((cx + 10, cy + 110), "BOOK", font=fit("BOOK", 300, 120, wdth=125, wght=900), fill=GOLD, anchor="mm")
    return img
def sunrise(img, k, low=980):
    ov = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(ov); sy = int(low + 200 - k * 520)
    for y in range(max(0, sy - 500), H, 8): d.rectangle([0, y, W, y + 8], fill=(255, 150, 70, int(min(90, 90 * k) * max(0, 1 - abs(y - sy) / 700))))
    c = Image.new("RGBA", (W // 10, H // 10)); dc = ImageDraw.Draw(c); dc.ellipse([W // 20 - 14, sy // 10 - 14, W // 20 + 14, sy // 10 + 14], fill=(255, 196, 90, int(255 * min(1, k * 1.5))))
    ov.alpha_composite(c.resize((W, H), Image.NEAREST)); return Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
def phone(img, t, u, cx=640, cy=760):
    d = ImageDraw.Draw(img); w, h = 420, 760
    d.rounded_rectangle([cx - w // 2 + 14, cy - h // 2 + 14, cx + w // 2 + 14, cy + h // 2 + 14], 40, fill="#000000")
    d.rounded_rectangle([cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2], 40, fill="#16181D", outline=INK, width=8)
    d.rectangle([cx - w // 2 + 30, cy - h // 2 + 70, cx + w // 2 - 30, cy + h // 2 - 90], fill="#05060A")
    d.text((cx, cy - 230), "ORDER", font=mono(48, True), fill=INK, anchor="mm"); d.text((cx, cy - 160), "ON HOLD", font=fit("ON HOLD", 320, 80, wdth=125, wght=900), fill=GOLD, anchor="mm")
    dots = "." * (1 + int(t * 3) % 3); d.text((cx, cy - 60), "going through" + dots, font=mono(34, True), fill=INK, anchor="mm")
    k = min(1.0, u / 11.0); d.rectangle([cx - 150, cy + 20, cx + 150, cy + 70], outline=INK, width=5); d.rectangle([cx - 144, cy + 26, cx - 144 + int(288 * k), cy + 64], fill=LIME)
    d.text((cx, cy + 150), "(hold music)", font=mono(34, True), fill="#8A8A84", anchor="mm")
    return img

# ---------- shots ----------
def s_title(t, u): return MV.title_card(t, g, ["ONLY", "ON PAPER"], COLOR, "ROOM-10")
def s_intro(t, u):
    img = MV.lights(room("ROOM-03", t, 0.45), t, g); rig(img, "penny", "talk", t, 540, 1440, 10, False, g, hop=False); return img
def verse_scene(name, who, flip=False):
    def l1(t, u): img = paper_chart(room(name, t, 0.4), t, u); rig(img, who, "facepalm", t, 820, 1460, 6, True, g, hop=False); return img
    def l2(t, u): img = room(name, t, 0.45); rig(img, "penny", "point", t, 220, 1460, 6, False, g); rig(img, "roz", "shrug", t, 880, 1460, 6, True, g); return mark_expiry(img, t, u)
    def l3(t, u): img = checklist(room(name, t, 0.35), t, u); rig(img, "ada" if not flip else "kit", "shakehead", t, 540, 1470, 6, False, g); return img
    def l4(t, u): img = rulebook(room(name, t, 0.45), t); rig(img, "theo", "nod", t, 540, 1460, 6, False, g); return img
    return l1, l2, l3, l4
V1 = verse_scene("ROOM-01", "theo"); V2 = [f for f in verse_scene("ROOM-09", "penny", True)]
V2 = [verse_scene("ROOM-09", "penny", True)[0], verse_scene("ROOM-11", "penny", True)[1], verse_scene("ROOM-04", "penny", True)[2], verse_scene("ROOM-15", "penny", True)[3]]
def chorus(name, t0, dur):
    def f(t, u):
        return band(t, g, name, None, 0.62, bg=lambda im: sunrise(im, min(1, u / dur)))
    return f
def s_solo(t, u): return MV.solo(t, g, "kit", "play" if int(g.of(t) / 4) % 2 else "dance", "OFF-KIT-01", "KIT'S SOLO", "(still only on paper)")
def s_wait(t, u):
    img = room("ROOM-08", t, 0.5)
    for ch, cx, fl in (("theo", 200, False), ("ada", 420, False), ("roz", 650, True), ("penny", 880, True)): rig(img, ch, "idle", t + cx * 0.01, cx, 1450, 5, fl, g, hop=False)
    return stamp(img, "THE WAITING ROOM", INK, 560, 110)
def s_bridge(t, u):
    img = room("ROOM-01", t, 0.35); rig(img, "penny", "talk", t, 250, 1460, 7, False, g, hop=False); return phone(img, t, u)
def s_after(t, u):
    img = band(t, g, "ROOM-03", {"theo": "nod", "penny": "celebrate", "ada": "nod", "roz": "nod", "kit": "dance"}, 0.7, bg=lambda im: sunrise(im, 1.0))
    return MV.confetti(img, t, 114.0) if t > 114 else img
def s_outro(t, u):
    img = sunrise(room("ROOM-03", t, 0.7), 1.0); rig(img, "theo", "nod", t, 360, 1440, 8, False, g); rig(img, "penny", "celebrate", t, 740, 1440, 8, True, g)
    return stamp(img, "ON PAPER.", COLOR, 640, 170)
def s_end(t, u): return MV.end_card(t, g, ["ONLY", "ON PAPER"], COLOR, "Rounding Error · The Band", "Down bad? Check the rulebook. Follow the band.")

SHOTS = [(0.0, s_title), (7.8, s_intro), (15.6, V1[0]), (19.5, V1[1]), (23.4, V1[2]), (27.3, V1[3]), (31.1, chorus("ROOM-03", 31.1, 17.4)),
         (48.5, s_solo), (56.3, s_wait), (63.9, V2[0]), (67.8, V2[1]), (71.7, V2[2]), (75.6, V2[3]), (79.5, chorus("ROOM-12", 79.5, 17.4)),
         (96.9, s_bridge), (108.5, s_after), (120.3, s_outro), (123.2, s_end)]
KW = dict(tape_words=TAPE, tape_kw=dict(bad=("MARK: OUCH",), good=("EXPIRY: LATER",)), end_fn=s_end)

if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if "--panels" in sys.argv: MV.panels(a[0], SHOTS, LINES, g, END, **KW)
    elif "--cover" in sys.argv: MV.cover(a[0], ["ONLY", "ON PAPER"], COLOR, band(40.0, g, "ROOM-03", None, 0.6, bg=lambda im: sunrise(im, 1.0)))
    else: MV.build(a[0] if a else "/home/claude/out/mv/only_on_paper_v1.mp4", "only_on_paper", SHOTS, LINES, g, END, **KW)
