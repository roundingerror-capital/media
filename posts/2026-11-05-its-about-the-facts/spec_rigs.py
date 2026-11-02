# "It's about the facts", V2.03 edition (the boss 2026-11-02: "replace one for one: every character a real video-game animation,
# every room an actual asset"). Same script, same timing, same text as spec.py. Swaps only:
#   characters -> tools/rigs.py (Mascot Designs V2.03 animations: idle/talk/celebrate/point/nod/shrug/shakehead/walk)
#   rooms      -> tools/scenes.py looping scenes (SCN-02 server room for the render, SCN-01 trading floor for the intervention)
#   props      -> tools/props.py (laptop, monitor, desk lamp, coffee) on Penny's desk
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); TOOLS = os.path.join(HERE, "..", "..", "tools"); sys.path.insert(0, TOOLS); sys.path.insert(0, HERE)
from PIL import Image, ImageDraw
import daily, rigs, scenes, props as PROPS
from make_reel import W, H, fade
import spec as BASE_SPEC
SPEC = dict(BASE_SPEC.SPEC)
BASE = daily.BASE

ROOMS = {0: "SCN-02", 1: "SCN-02", 2: "SCN-01", 3: "SCN-01", 4: "SCN-01", 5: "SCN-01"}
DIM = 0.5
ANIM = {"jump": "celebrate", "point": "point", "brow": "shrug", "nod": "nod", "wave": "talk", "spin": "celebrate", "thumbs": "nod"}
FLIP = {"theo": False, "penny": False, "ada": True, "kit": True, "roz": True}   # the V2.03 boards face right; mirror the right-hand side of the line-up
DESK_PROPS = {0: [("PROP-001", 0.62, 60), ("PROP-014", 0.74, 40), ("PROP-499", 0.84, 20)]}   # (prop, x as a fraction of W, lift above the floor line)

def room_bg(S, path, t):
    """Looping scene for the current slide (daily.scene_frame calls office_bg(S, bgp, t); bgp is the room id here)."""
    sid = path if isinstance(path, str) and path.startswith("SCN-") else "SCN-01"
    im = scenes.frame(sid, t); return Image.eval(im, lambda v: int(v * DIM))

def rig_layer(img, d, S, t, cast, lines, text_bottom):
    """Same contract as daily.char_layer: cast left to right at XS positions, the speaker's pose becomes a V2.03 animation,
    everyone else idles. Whole-number scale (NEAREST), no rotation, no stretching: the rig's own frames do the acting."""
    hpx = S.get("_hpx") or (430 if len(cast) < 3 else 380); k = max(3, round(hpx / 64))
    xs = S.get("_xs") or daily.XS[len(cast)]
    sc = S["scenes"]; kk = max(i for i, s in enumerate(sc) if t >= s[0] or i == 0)
    for pid, fx, lift in DESK_PROPS.get(kk, []):
        pr = PROPS.at(pid, t); pr = pr.resize((pr.width * 5, pr.height * 5), Image.NEAREST)
        img.paste(pr, (int(W * fx) - pr.width // 2, BASE - lift - pr.height), pr)
    for i, n in enumerate(cast):
        xc = int(W * xs[i])
        talk = [(ts, te, pose) for ts, te, w, _, pose in lines if w == n and ts <= t < te]
        if talk: ts, te, pose = talk[0]; an, t0 = ANIM.get(pose, "talk"), ts
        else: an, t0 = "idle", 0.0
        if an not in rigs.anims(n): an = "talk" if talk else "idle"
        sp = rigs.frame(n, an, t, k=k, flip=FLIP.get(n, False), loop=True, t0=t0)
        d.ellipse([xc - sp.width * 0.33, BASE - 8, xc + sp.width * 0.33, BASE + 16], fill="#1a1a1a")
        img.paste(sp, (xc - sp.width // 2, BASE - sp.height), sp)
    for ts, te, w, ln, _ in lines:
        if ts <= t < te and w in cast:
            xc = int(W * xs[cast.index(w)]); y = max(text_bottom + 24, BASE - hpx - 150); daily.bubble(d, xc, y, ln)

daily.office_bg = room_bg
daily.char_layer = rig_layer
SPEC["bg"] = None; SPEC["bgs"] = ROOMS
