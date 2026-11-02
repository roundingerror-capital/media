# "It's about the facts", V2.03 edition (the boss 2026-11-02: "replace one for one: every character a real video-game animation,
# every room an actual asset"). Same script, same timing, same text as spec.py. Swaps only:
#   characters -> tools/rigs.py (Mascot Designs V2.03 animations: idle/talk/celebrate/point/nod/shrug/shakehead/walk)
#   rooms      -> tools/scenes.py looping scenes (SCN-02 server room for the render, SCN-01 trading floor for the intervention)
#   props      -> tools/props.py (laptop, monitor, desk lamp, coffee) on Penny's desk
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); TOOLS = os.path.join(HERE, "..", "..", "tools"); sys.path.insert(0, TOOLS); sys.path.insert(0, HERE)
from PIL import Image, ImageDraw
import daily, rigs, scenes, props as PROPS
from make_reel import W, H, fade, archivo
import spec as BASE_SPEC
SPEC = dict(BASE_SPEC.SPEC)
BASE = daily.BASE

# Rooms (the boss 2026-11-02: "there are cool ones, you picked gray"): the render happens in Kit's neon game studio, the intervention in
# the boardroom with the city behind the glass, the slam sequence in deep space (To the moon), the close on the rooftop at night.
ROOMS = {0: "SCN-06", 1: "SCN-06", 2: "SCN-15", 3: "SCN-15", 4: "SCN-13", 5: "SCN-03"}
DIM = 0.72
ANIM = {"jump": "celebrate", "point": "point", "brow": "shakehead", "nod": "nod", "wave": "talk", "spin": "celebrate", "thumbs": "nod"}
# One or two animations per scene per character (the boss: "they have ten each, pick one or two per scene"); used when not speaking.
# v5 (the boss: "Theo and Penny look like stickers"): the subtle ones (idle breathe, point, shrug) read as frozen at phone size, so every
# scene uses the big-motion animations (celebrate = jump, shakehead = sway, walk = step, facepalm, nod), plus a whole-pixel beat hop.
ACT = {0: {"penny": "celebrate"},
       1: {"penny": "celebrate", "theo": "facepalm"},
       2: {"penny": "celebrate", "theo": "shakehead"},
       3: {"penny": "shakehead", "theo": "nod", "ada": "celebrate"},
       4: {"penny": "celebrate", "theo": "celebrate", "ada": "celebrate"},
       5: {"penny": "facepalm", "theo": "nod", "ada": "celebrate"}}
HOP = True   # beat hop: a 0-2 native-pixel lift on the music's beat (translation only; frames untouched)
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
        else: an, t0 = ACT.get(kk, {}).get(n, "idle"), sc[kk][0]
        if an not in rigs.anims(n): an = "talk" if talk else "idle"
        sp = rigs.frame(n, an, t, k=k, flip=FLIP.get(n, False), loop=True, t0=t0)
        ph = t * S["bpm"] / 60; hop = k * int(round(2 * abs(math.sin(math.pi * ph)))) if HOP else 0
        d.ellipse([xc - sp.width * 0.33, BASE - 8, xc + sp.width * 0.33, BASE + 16], fill="#1a1a1a")
        img.paste(sp, (xc - sp.width // 2, BASE - sp.height - hop), sp)
    for ts, te, w, ln, _ in lines:
        if ts <= t < te and w in cast:
            xc = int(W * xs[cast.index(w)]); y = max(text_bottom + 24, BASE - hpx - 150); daily.bubble(d, xc, y, ln)

def banner(img, d, u, y):
    """The INTERVENTION banner: red cloth unrolls from the ceiling as the team walks in, then sways. Drawn over the base hook."""
    y = BASE_SPEC.intervention(img, d, u, y)
    if u < 0.3: return y
    k = min(1, (u - 0.3) / 0.6); k = 1 - (1 - k) ** 3; top = 950; hgt = int(150 * k); sway = int(6 * math.sin(u * 2.2))
    x0, x1 = 120 + sway, W - 120 + sway
    d.rectangle([x0 - 10, top - 14, x1 + 10, top], fill=(110, 80, 50))                         # the rod
    d.rectangle([x0, top, x1, top + hgt], fill=(190, 40, 48)); d.rectangle([x0, top, x1, top + 10], fill=(230, 80, 80))
    if k >= 1:
        for i in range(x0, x1, 48): d.polygon([(i, top + hgt), (i + 24, top + hgt + 22), (i + 48, top + hgt)], fill=(190, 40, 48))   # scalloped hem
        d.text(((x0 + x1) // 2, top + 112), "INTERVENTION", font=archivo(104, 125, 900), fill="#F2F2EE", anchor="ms", stroke_width=4, stroke_fill=(120, 20, 28))
    return y

SPEC["charts"] = dict(SPEC["charts"]); SPEC["charts"][2] = {"draw": banner}
# daily.py runs as __main__ and imports the spec, so the spec's `daily` is a second module object: patch BOTH, or the old
# static sprites keep drawing (v3/v4 shipped that way: the walkers were rigs, Theo and Penny were the stickers. The boss 2026-11-02.)
for mod in {daily, sys.modules.get("__main__")}:
    if mod is not None and hasattr(mod, "char_layer"):
        mod.office_bg = room_bg; mod.char_layer = rig_layer
SPEC["bg"] = None; SPEC["bgs"] = ROOMS
