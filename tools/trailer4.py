"""MEET THE FUND v10 (the boss 2026-11-03: "re-render the meet the fund using only the new assets"): the v9 ARCADE cut, rebuilt on
Kit's newest kit. Same beats and timing as trailer3.py's cut A, with:
  - the skyline title and ALL PLAYERS READY in front of the 25-room tower (make_v5.py: furnished apartments, 25 residents in
    Kit's colourways, lights on their own timing) instead of the old generic skyline;
  - each SELECT YOUR TRADER stage is that character's own OFF office (Kit's stage, dressed like the office parody) instead of a
    looping SCN plate, with a Kit fantasy-library item as their pick-up (EXTRAS · Fantasy);
  - PICK YOUR COLOUR: on each select, the big rig cycles through Kit's palette swaps (tools/swaps.py) and lands back on the default.
Everything else (no figures, the boss only as the shadow, the real boss never named, NFA on every frame) is trailer3's.
Usage: python3 tools/trailer4.py <out.mp4> [workdir]   ·   python3 tools/trailer4.py <out.png> <workdir> still <t>"""
import os, sys, runpy
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
os.environ.setdefault("PARODY_CUT", "/home/claude/out/officeparody/music/breakroom_cut.json")
import trailer3 as T3, rigs, stage, swaps
from PIL import Image
P = runpy.run_path(os.path.join(HERE, "..", "posts", "2026-11-04-office-intro-parody", "make_v5.py"), run_name="parody")
W, H = T3.W, T3.H

OFFICE = {"SCN-01": ("OFF-THEO-01", "theo"), "SCN-08": ("OFF-PENNY-01", "penny"), "SCN-02": ("OFF-ADA-01", "ada"),
          "SCN-06": ("OFF-KIT-01", "kit"), "SCN-05": ("OFF-ROZ-01", "roz"), "SCN-15": ("OFF-BOSS-01", "boss")}
PICKUP = {"PROP-454": "Scroll", "PROP-407": "Star", "PROP-101": "Crystal, teal", "PROP-357": "Magic wand", "PROP-004": "Tome"}
_BG = {}
def scene_bg(sid, t, dim=0.55):
    """The character's own office (Kit's stage + the parody's dressing), wide framing, no desk set (they stand in front of it)."""
    if sid not in OFFICE: return T3.__dict__["_scene_bg_v9"](sid, t, dim)
    name, _ = OFFICE[sid]
    if name not in _BG:
        st = stage.load(os.path.join(P["ASSETS"], name + ".dc.html"))
        skip, extra, wall = P["dressed"](st, name, ("CHR",), {})
        im = st.render(skip=skip, extra=extra, wall=wall); x, y, w, h = st.frames.get("wide", (0, 16, 192, 108))
        _BG[name] = im.crop((x, y, x + w, y + h)).convert("RGB")
    im = _BG[name]
    if dim < 1: im = Image.blend(Image.new("RGB", im.size), im, max(0.35, dim))
    return im.resize((im.width * 5, im.height * 5), Image.NEAREST)

def prop(img, pid, t, cx, cy, k=6, bob=True):
    if pid not in PICKUP: return T3.__dict__["_prop_v9"](img, pid, t, cx, cy, k, bob)
    fr = P["board_frames"]("XFANTASY.dc.html", PICKUP[pid] + " at actual size", 1.0); im = fr[int(t * 10) % len(fr)]; im = im.crop(im.getbbox())
    im = im.resize((im.width * k, im.height * k), Image.NEAREST); dy = int(6 * T3.math.sin(t * 3)) if bob else 0
    img.paste(im, (int(cx - im.width // 2), int(cy - im.height // 2 + dy)), im)

_TW = {}
def skyline(img, t, ground, scroll=0.0, k=2, dim=1.0):
    """The 25-room tower in place of the old skyline: its street line lands on `ground`."""
    fr = P["tower_frame"](t)            # 1080x1920, street at native 860 x2 = 1720
    off = ground - 1720
    fr = Image.blend(Image.new("RGB", fr.size), fr, 0.42)            # pushed back so the title reads over it
    img.paste(fr, (0, off)) if off <= 0 else img.paste(fr.crop((0, 0, W, H - off)), (0, off))
def far_skyline(*a, **k): pass

def rig(img, ch, an, t, t0, cx, by, k=8, flip=False, loop=True, alpha=1.0, shade=True):
    """PICK YOUR COLOUR: during a character's select (0.6-2.2 s in), the big rig cycles Kit's palette swaps, then settles."""
    TA = T3.TA
    if k >= 9 and TA["select"] <= t < TA["boss"] and ch in [c[0] for c in T3.CAST]:
        i = [c[0] for c in T3.CAST].index(ch); us = t - TA["select"] - i * TA["per"]
        if 0.6 <= us < 2.2:
            names = swaps.names(ch); sw = names[int((us - 0.6) / 0.32) % len(names)]
            sp = rigs.frame(ch, an, t, k=1, flip=flip, loop=loop, t0=t0); sp = swaps.recolor(sp, ch, sw)
            sp = sp.resize((sp.width * k, sp.height * k), Image.NEAREST)
            if shade: T3.shadow(T3.ImageDraw.Draw(img), cx, by, rigs.body(ch, an, k)[0])
            T3.paste(img, sp, cx, by, alpha)
            d = T3.ImageDraw.Draw(img); d.text((T3.SAFE_L + 24, 1072), "PICK YOUR COLOUR: " + sw.upper(), font=T3.mono(28, True), fill=T3.LIME, anchor="ls")
            return
    return T3.__dict__["_rig_v9"](img, ch, an, t, t0, cx, by, k, flip, loop, alpha, shade)

for name, fn in (("scene_bg", scene_bg), ("prop", prop), ("rig", rig)):
    T3.__dict__["_" + name + "_v9"] = getattr(T3, name); setattr(T3, name, fn)
T3.skyline = skyline; T3.far_skyline = far_skyline

if __name__ == "__main__":
    out = sys.argv[1]; wd = sys.argv[2] if len(sys.argv) > 2 else "/tmp"
    if len(sys.argv) > 4 and sys.argv[3] == "still": T3.a_frame(float(sys.argv[4])).save(out); sys.exit()
    print(T3.build("arcade", out, wd))
