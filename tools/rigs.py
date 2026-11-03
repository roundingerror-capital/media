"""V2.03 character rigs (Kit's core-10 animations on the Mascot Designs canvas) as frames for the video tools.
Each canvas board holds one animation: <g id="<key><n>"> per frame (1 px rects on the 64x64 avatar grid) and a CSS
@keyframes block per frame whose percentages give the hold. tools/rigs.py parses the boards into
tools/anim/<char>/<anim>.json = {"w","h","frames":[[[x,y,w,h,"#hex"],...],...],"ticks":[...], "ms": total}
(committed: text only, a few hundred KB; renders stay out of git) and serves them to the renderers:

    import rigs; im = rigs.frame("penny", "celebrate", t)          # RGBA at native 64 px grid
    rigs.frame("theo", "walk", t, k=7, flip=True)                  # scaled NEAREST by a whole number, mirrored
    rigs.anims("roz") -> ["idle","walk","talk","nod","shakehead","point","celebrate","facepalm","shrug","holdsign"]
Characters: theo, penny, ada, kit, roz, boss (the shadow chimp), realboss, realboss_hood.
Build: python3 tools/rigs.py build <dir with project/V2_03*.dc.html>"""
import os, re, json, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__)); ANIM = os.path.join(HERE, "anim")
CHARS = {"Theo": "theo", "Penny": "penny", "Ada": "ada", "Kit": "kit", "Roz": "roz", "Boss": "boss", "RealBossHood": "realboss_hood", "RealBoss": "realboss"}
ANIMS = ["idle", "walk", "talk", "nod", "shakehead", "point", "celebrate", "facepalm", "shrug", "holdsign"]
_CACHE = {}

def _gate(kind, aid):
    """The star gate (tools/approved.py, the boss 2026-11-02): no star on the canvas, no frame in a video."""
    import approved; approved.check(kind, aid)


def parse_board(html):
    """-> (frames, holds_ms). frames = list of rect lists; holds from the keyframe percentages of a total duration."""
    m = re.search(r'<svg[^>]*>\s*<defs>(.*?)</defs>', html, re.S)
    defs = m.group(1) if m else html
    groups = re.findall(r'<g id="([A-Za-z]+?)(\d+)">(.*?)</g>', defs, re.S)
    frames = []
    for key, n, body in sorted(groups, key=lambda g: int(g[1])):
        rects = [(int(x), int(y), int(w), int(h), c) for x, y, w, h, c in
                 re.findall(r'<rect x="(-?\d+)" y="(-?\d+)" width="(\d+)" height="(\d+)" fill="(#[0-9A-Fa-f]{6})"', body)]
        frames.append(rects)
    key = groups[0][0] if groups else ""
    dur = re.search(r'\.' + re.escape(key) + r'0\{animation:' + re.escape(key) + r'0 ([\d.]+)s', html)
    total = float(dur.group(1)) if dur else 0.1 * len(frames)
    holds = []
    for i in range(len(frames)):
        kf = re.search(r'@keyframes ' + re.escape(key) + str(i) + r'\{(.*?)\}\s*\.', html, re.S)
        pcts = [float(p) for p in re.findall(r'([\d.]+)%\{opacity:1\}', kf.group(1))] if kf else []
        holds.append(round((max(pcts) - min(pcts)) / 100 * total * 1000) if len(pcts) >= 2 else round(total * 1000 / len(frames)))
    return frames, holds, total


def build(src_dir):
    n = 0
    for f in sorted(os.listdir(src_dir)):
        m = re.match(r'V2_03([A-Za-z]+?)(Idle|Walk|Talk|Nod|Shakehead|Point|Celebrate|Facepalm|Shrug|Holdsign)\.dc\.html$', f)
        if not m or m.group(1) not in CHARS: continue
        ch, an = CHARS[m.group(1)], m.group(2).lower()
        frames, holds, total = parse_board(open(os.path.join(src_dir, f), encoding="utf-8").read())
        if not frames: print("no frames:", f); continue
        W = max(x + w for fr in frames for x, y, w, h, c in fr); H = max(y + h for fr in frames for x, y, w, h, c in fr)
        os.makedirs(os.path.join(ANIM, ch), exist_ok=True)
        json.dump({"w": W, "h": H, "frames": frames, "ticks": holds, "ms": round(total * 1000), "source": f"Mascot Designs · {f}"},
                  open(os.path.join(ANIM, ch, an + ".json"), "w"), separators=(",", ":"))
        n += 1; print(f"{ch:14s} {an:10s} {len(frames)} frames  {W}x{H}  {holds}")
    print(n, "animations")


def load(ch, an):
    k = (ch, an)
    if k not in _CACHE:
        d = json.load(open(os.path.join(ANIM, ch, an + ".json")))
        ims = []
        for fr in d["frames"]:
            im = Image.new("RGBA", (d["w"], d["h"]), (0, 0, 0, 0)); px = im.load()
            for x, y, w, h, c in fr:
                col = (int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16), 255)
                for yy in range(max(0, y), min(d["h"], y + h)):
                    for xx in range(max(0, x), min(d["w"], x + w)): px[xx, yy] = col
            ims.append(im)
        _CACHE[k] = (ims, d["ticks"])
    return _CACHE[k]


def anims(ch): return [a for a in ANIMS if os.path.exists(os.path.join(ANIM, ch, a + ".json"))]


def frame_index(ticks, t_ms, loop=True):
    total = sum(ticks)
    if not loop and t_ms >= total: return len(ticks) - 1
    t = t_ms % total; acc = 0
    for i, h in enumerate(ticks):
        acc += h
        if t < acc: return i
    return len(ticks) - 1


def frame(ch, an, t, k=1, flip=False, loop=True, t0=0.0):
    """RGBA frame of character `ch` animation `an` at time t (seconds since the animation started at t0)."""
    _gate("anim", f"{ch}/{an}")
    ims, ticks = load(ch, an); im = ims[frame_index(ticks, int((t - t0) * 1000), loop)]
    if flip: im = im.transpose(Image.FLIP_LEFT_RIGHT)
    if k != 1: im = im.resize((im.width * k, im.height * k), Image.NEAREST)
    return im


def duration(ch, an): return sum(load(ch, an)[1]) / 1000.0


if __name__ == "__main__":
    if sys.argv[1] == "build": build(sys.argv[2])
