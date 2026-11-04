"""WoW Forever v7: v6c with Roz's 11/4 08:29 hold resolved.
  - no family of the owner (Rules section 3 rule 3, holds even if the boss asks): Penny is the one who walks in, worries and wakes
    him ("BOSS. WAKE UP. IT'S 3 AM."); the "honey..." card is now "3:07 AM";
  - no origin claims / owner's trading history: the ending is "THE BOT DOES THE HOMEWORK. NOW WE RAID. YOU GET THE NOTES.";
  - AI wording (D-20261027-ai-wording-1): no "automated everything"; "MUST AUTOMATE" is "MUST... HIT... THE BUTTON."; the cover
    says "I'M AN AI TRADING BOT. NOW WE RAID.";
  - captions carry "Not financial advice. Not affiliated with Blizzard." (on the card, not in the video).
    python3 make_v7.py <out.mp4> | --panels <sheet.png> | --cover <out.jpg>"""
import os, sys, runpy
HERE = os.path.dirname(os.path.abspath(__file__))
_argv = sys.argv; sys.argv = sys.argv[:1]
V6 = runpy.run_path(os.path.join(HERE, "make_v6.py"), run_name="v6"); sys.argv = _argv
V5, V3, V2 = V6["V5"], V6["V3"], V6["V2"]; V6o = V6["V6o"]
from PIL import Image, ImageDraw
from make_reel import W, H, FPS, mono, fit
LIME, INK = V6["LIME"], V6["INK"]
stamp, black, portrait = V3["stamp"], V3["black"], V3["portrait"]
office = lambda *a, **k: V3["shots"].__globals__["office"](*a, **k)
thought, bubble = V5["thought"], V3["bubble"]
rich, rcards = V5["rich"], V5["rcards"]

CODE = V3["V1"]["CODE"]                                # same list object every version draws from: no "automate everything / forever" lines
CODE[0] = "def build_notes(today):"; CODE[2] = "        job.run(check=True)"; CODE[6] = "while not done: roz.check()"
_standing = V6o["standing"]
def standing(ch, an, t, t0, flip=False):
    if ch == "realboss": ch, an = "penny", {"walk": "walk", "idle": "idle", "talk": "talk"}.get(an, "idle")
    return _standing(ch, an, t, t0, flip)
V6o["standing"] = standing

def must(t, u):
    img = V2["pushin"](t, u + 2.5, 40); d = ImageDraw.Draw(img)
    for i, w in enumerate(("MUST...", "HIT...", "THE BUTTON.")[: 1 + int(u * 2.4)]):
        d.text((W // 2, 1300 + i * 140), w, font=fit("THE BUTTON.", W - 160, 110, wdth=125, wght=900), fill=LIME if i == 2 else INK, anchor="mm", stroke_width=10, stroke_fill="#000000")
    return img

END = [
    (1.6, "S1", rcards([([("THE", False), ("BOT", False), ("DOES", False)], 860, 0), ([("THE", False), ("HOMEWORK.", True)], 1020, 0.25)])),
    (1.4, "S2", rcards([([("NOW", False), ("WE", False), ("RAID.", True)], 960, 0)])),
    (1.8, "S3", rcards([([("YOU", False), ("GET", False)], 860, 0), ([("THE", False), ("NOTES.", True)], 1020, 0.2)])),
    (2.6, "WHY", rcards([([("an", False), ("AI-run", True), ("fund,", False)], 820, 0), ([("learning", False), ("in", False), ("public.", True)], 940, 0.2)],
                        [("FOLLOW FOR THE NOTES.", LIME, 1500, 96, 0.5)])),
]
REPL = {
    "SHE'S WORRIED": lambda t, u: thought(portrait(*office(t, "3/4-back · Type", dark=True, cast=[("realboss", "idle", 88, 108, False)])), ["He's been coding", "nonstop. I'm worried."], 380, 520),
    "MUST AUTOMATE": must,
    "HONEY...": lambda t, u: stamp(black(), "3:07 AM.", INK, 960, 110),
    "ASLEEP ON THE DESK": lambda t, u: bubble(portrait(*office(t, "Front · Asleep", cast=[("realboss", "talk", 88, 108, False)])), "BOSS. WAKE UP. IT'S 3 AM.", W // 2, 330),
}
def shots():
    out = []
    for d, l, f in V6["shots"]():
        if l in ("S1", "S2", "S3", "WHY"):
            if l == "S1": out += END
            continue
        out.append((d, l, REPL.get(l, f)))
    return out
V6["shots"].__globals__["shots"] = shots              # v6's sound() and build() take S from their argument; build looks shots() up here

def cover(out):
    S = shots(); t = 0
    for d, l, f in S:
        if l == "THE RAID": break
        t += d
    im = V3["frame_at"](S, t + 1.6)
    stamp(im, "I'M AN AI", INK, 1250, 120); stamp(im, "TRADING BOT.", LIME, 1390, 130); stamp(im, "NOW WE RAID.", INK, 1530, 110)
    im.save(out, quality=92); print(out)

if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if "--panels" in sys.argv:
        S = shots(); want = [("FROM BEHIND · SHE WALKS IN", 1.5), ("SHE'S WORRIED", 1.5), ("MUST AUTOMATE", 1.8), ("HONEY...", 0.5), ("ASLEEP ON THE DESK", 1.2), ("S1", 1.0), ("S3", 1.2), ("WHY", 1.5)]
        ims = []
        for lab, u in want:
            t = 0
            for d, l, f in S:
                if l == lab: ims.append(V3["frame_at"](S, t + u)); break
                t += d
        s = Image.new("RGB", (len(ims) * 270, 480))
        for i, im in enumerate(ims): s.paste(im.resize((270, 480)), (i * 270, 0))
        s.save(a[0]); print(a[0])
    elif "--cover" in sys.argv: cover(a[0])
    else: V6["build"](a[0] if a else "/home/claude/out/wow/wow_v7.mp4")
