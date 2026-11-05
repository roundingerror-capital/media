"""The Band, episode 2: THE CLOCK PAYS RENT (song: The Clock Pays Rent, lyric set "Theta Lullaby"; lo-fi lullaby, 80.7 BPM).
The night shift: the office asleep, a clock that pays rent every night (time decay), the band humming a lullaby on the roof.
Lyrics are read from the songs row at render time (never committed); lines timed to the vocal phrases on the bar grid.
    python3 make.py <out.mp4> | --panels <sheet.png> | --cover <out.jpg>"""
import os, sys, math, json
HERE = os.path.dirname(os.path.abspath(__file__)); TOOLS = os.path.join(HERE, "..", "..", "tools"); sys.path.insert(0, TOOLS)
os.environ.setdefault("RE_ASSETS_DIR", "/tmp/claude-0/-home-claude/97ad6b31-1277-5795-987d-0d7c1b8393c4/scratchpad/assets3/project")
from PIL import Image, ImageDraw
import musicvideo as MV, assets
from musicvideo import W, H, LIME, INK, RED, GREEN, GOLD, stamp, rig, room, lights, band
g = MV.Grid(80.75, 1.579); END = 62.4; COLOR = "#9FB8FF"
LINES = json.load(open(os.environ.get("MV_LINES", os.path.join(TOOLS, "music", "mv_lines.json"))))["the_clock_pays_rent"]
TAPE = ["THETA", "TIME DECAY", "TICK", "TOCK", "RENT: PAID", "PATIENCE", "HUSH", "GOODNIGHT"]

def px_layer(): return Image.new("RGBA", (W // 10, H // 10))
def up(c): return c.resize((W, H), Image.NEAREST)
def paste(img, c): base = img.convert("RGBA"); base.alpha_composite(up(c)); return base.convert("RGB")
def moon(img, t, x=86, y=44):
    c = px_layer(); d = ImageDraw.Draw(c); d.ellipse([x - 7, y - 7, x + 7, y + 7], fill=(244, 238, 210, 255)); d.ellipse([x - 3, y - 9, x + 9, y + 5], fill=(0, 0, 0, 0))
    for i, (sx, sy) in enumerate([(12, 36), (30, 40), (52, 34), (70, 52), (20, 58), (96, 62)]):
        if int(t * 2 + i) % 3: d.point((sx, sy), fill=(255, 255, 255, 255))
    return paste(img, c)
def clock(img, t, cx=54, cy=70, r=22, speed=1.0):
    c = px_layer(); d = ImageDraw.Draw(c)
    d.ellipse([cx - r - 2, cy - r - 2, cx + r + 2, cy + r + 2], fill=(20, 20, 30, 255)); d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(242, 242, 238, 255))
    for k in range(12):
        a = k / 12 * 2 * math.pi; d.point((cx + math.sin(a) * (r - 3), cy - math.cos(a) * (r - 3)), fill=(20, 20, 30, 255))
    am = t * speed * 2 * math.pi / 4; ah = am / 12
    d.line([cx, cy, cx + math.sin(am) * (r - 5), cy - math.cos(am) * (r - 5)], fill=(20, 20, 30, 255), width=1)
    d.line([cx, cy, cx + math.sin(ah) * (r - 10), cy - math.cos(ah) * (r - 10)], fill=(200, 40, 40, 255), width=2)
    d.rectangle([cx - 1, cy - 1, cx + 1, cy + 1], fill=(20, 20, 30, 255))
    return paste(img, c)
def envelope(img, x, y, s=1.0):
    d = ImageDraw.Draw(img); w, h = int(220 * s), int(140 * s)
    d.rectangle([x - w // 2, y - h // 2, x + w // 2, y + h // 2], fill="#F7F1D8", outline="#000000", width=8)
    d.line([x - w // 2, y - h // 2, x, y + 6, x + w // 2, y - h // 2], fill="#B9AF8F", width=8)
    d.text((x, y + h // 4), "RENT", font=MV.fit("RENT", int(w * 0.6), int(56 * s), wdth=125, wght=900), fill="#0B0B0B", anchor="mm")
def piggy(img, t, cx, feet, k=8):
    p = assets.get("PIG-01", t).resize((64 * k, 64 * k), Image.NEAREST); img.paste(p, (cx - p.width // 2, feet - p.height), p)

def s_title(t, u):
    img = moon(MV.title_card(t, g, ["THE CLOCK", "PAYS RENT"], COLOR), t); return img
def s_whisper(t, u):
    img = moon(room("OFF-PENNY-01", t, 0.35), t); rig(img, "penny", "talk", t, 540, 1440, 9, False, g, hop=False); return img
def s_hush(t, u):
    img = room("ROOM-10", t, 0.5); rig(img, "theo", "facepalm", t, 360, 1440, 8, False, g, hop=False); rig(img, "penny", "talk", t, 760, 1440, 7, True, g, hop=False)
    c = px_layer(); d = ImageDraw.Draw(c)                                       # a small sad red candle, crying
    d.line([54, 44, 54, 66], fill=(255, 92, 92, 255)); d.rectangle([51, 48, 57, 62], fill=(255, 92, 92, 255))
    for k in range(3):
        ty = 54 + ((t * 9 + k * 4) % 12); d.point((49, ty), fill=(123, 170, 247, 255)); d.point((59, ty + 2), fill=(123, 170, 247, 255))
    return paste(img, c)
def s_decay(t, u):
    img = room("ROOM-01", t, 0.35); img = clock(img, t, 54, 72, 26, 3.0)
    rig(img, "ada", "nod", t, 220, 1440, 6, False, g); rig(img, "kit", "idle", t, 860, 1440, 6, True, g); return stamp(img, "TICK. TOCK.", INK, 1240, 110)
def s_rent(t, u):
    img = room("ROOM-03", t, 0.5); img = moon(clock(img, t, 26, 52, 14, 3.0), t)
    piggy(img, t, 800, 1300, 7); rig(img, "theo", "celebrate" if u > 2.4 else "idle", t, 300, 1440, 7, False, g)
    k = min(1.0, u / 2.2); x = 260 + (800 - 260) * k; y = 520 - math.sin(k * math.pi) * 260 + k * 380
    if u < 2.4: envelope(img, int(x), int(y), 0.8 + 0.2 * (1 - k))
    else: stamp(img, "PAID.", LIME, 760, 170)
    return img
def s_advice(t, u):
    img = room("ROOM-15", t, 0.45); rig(img, "roz", "holdsign", t, 540, 1440, 9, False, g, hop=False)
    return stamp(img, "NOT ADVICE.", LIME, 600, 140) if u > 1.0 else img
def s_sway(t, u):
    return moon(band(t, g, "ROOM-03", {"theo": "idle", "penny": "talk", "ada": "nod", "roz": "nod", "kit": "idle"}, 0.55), t)
def s_keys(t, u):
    return moon(MV.solo(t, g, "kit", "play", "OFF-KIT-01", "KIT ON KEYS", "(lullaby mode)", 0.45), t)
def s_nights(t, u):
    img = room("ROOM-03", t, 0.45); ph = (u / 2.0) % 1
    c = px_layer(); d = ImageDraw.Draw(c); mx = int(-10 + ph * 128); my = int(40 - math.sin(ph * math.pi) * 24)
    d.ellipse([mx - 6, my - 6, mx + 6, my + 6], fill=(244, 238, 210, 255)); img = paste(img, c)
    img = clock(img, t, 54, 60, 18, 12.0); piggy(img, t, 540, 1420, 8)
    yy = 820 + (ph * 520); envelope(img, 540, int(yy), 0.7)
    return stamp(img, "EVERY NIGHT.", COLOR, 360, 120)
def s_dawn(t, u):
    img = band(t, g, "ROOM-03", {"theo": "nod", "penny": "celebrate", "ada": "celebrate", "roz": "nod", "kit": "dance"}, 0.66)
    ov = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(ov); k = min(1, u / 3.0)
    for y in range(900, H, 6): d.rectangle([0, y, W, y + 6], fill=(255, 170, 80, int(70 * k * (y - 900) / (H - 900))))
    img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB"); return stamp(img, "GOODNIGHT, TRADER.", COLOR, 620, 110)
def s_end(t, u): return MV.end_card(t, g, ["THE CLOCK", "PAYS RENT"], COLOR, "Rounding Error · The Band", "Time decay never sleeps. Follow the band.")

SHOTS = [(0.0, s_title), (6.0, s_whisper), (12.0, s_hush), (18.6, s_decay), (24.9, s_rent), (30.4, s_advice), (34.6, s_sway),
         (40.6, s_keys), (46.6, s_nights), (52.6, s_dawn), (57.4, s_end)]
KW = dict(tape_words=TAPE, tape_kw=dict(good=("RENT: PAID",)), end_fn=s_end)

if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if "--panels" in sys.argv: MV.panels(a[0], SHOTS, LINES, g, END, **KW)
    elif "--cover" in sys.argv: MV.cover(a[0], ["THE CLOCK", "PAYS RENT"], COLOR, moon(band(30.0, g, "ROOM-03", {"theo": "idle", "penny": "talk", "ada": "nod", "roz": "nod", "kit": "play"}, 0.6), 30.0))
    else: MV.build(a[0] if a else "/home/claude/out/mv/clock_pays_rent_v1.mp4", "the_clock_pays_rent", SHOTS, LINES, g, END, **KW)
