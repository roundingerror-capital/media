"""V2.03 character rigs (Kit's core-10 animations on the Mascot Designs canvas) as frames for the video tools.
Each canvas board holds one animation: <g id="<key><n>"> per frame (1 px rects on the 64x64 avatar grid) and a CSS
@keyframes block per frame whose percentages give the hold. tools/rigs.py parses the boards into
tools/anim/<char>/<anim>.json = {"w","h","frames":[[[x,y,w,h,"#hex"],...],...],"ticks":[...], "ms": total}
(committed: text only, a few hundred KB; renders stay out of git) and serves them to the renderers:

    import rigs; im = rigs.frame("penny", "celebrate", t)          # RGBA at native 64 px grid
    rigs.frame("theo", "walk", t, k=7, flip=True)                  # scaled NEAREST by a whole number, mirrored
Frames carry PAD px of empty margin left/right/top so nothing is cropped; paste them bottom-centre anchored.
rigs.body(ch, an, k) gives the body box (w, h) for shadows and speech-bubble heights.
    rigs.anims("roz") -> ["idle","walk","talk","nod","shakehead","point","celebrate","facepalm","shrug","holdsign"]
Characters: theo, penny, ada, kit, roz, boss (the shadow chimp), realboss, realboss_hood.
Build: python3 tools/rigs.py build <dir with project/V2_03*.dc.html>"""
import os, re, json, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__)); ANIM = os.path.join(HERE, "anim")
CHARS = {"Theo": "theo", "Penny": "penny", "Ada": "ada", "Kit": "kit", "Roz": "roz", "Boss": "boss", "RealBossHood": "realboss_hood", "RealBoss": "realboss"}
ANIMS = ["idle", "walk", "talk", "nod", "shakehead", "point", "celebrate", "facepalm", "shrug", "holdsign", "standing"]
_CACHE = {}
PAD = 24   # native px of headroom on the left, right and top: jumps, raised signs and flung arms go past Kit's 64 px grid
           # (penny celebrate reaches x -9, holdsign y -19). Feet (bottom) and the body's centre stay where they were.


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
        m = re.match(r'V2_0[36]([A-Za-z]+?)(Idle|Walk|Talk|Nod|Shakehead|Point|Celebrate|Facepalm|Shrug|Holdsign|Standing)\.dc\.html$', f)
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
        ims = []; CW, CH = d["w"] + 2 * PAD, d["h"] + PAD
        for fr in d["frames"]:
            im = Image.new("RGBA", (CW, CH), (0, 0, 0, 0)); px = im.load()
            for x, y, w, h, c in fr:
                col = (int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16), 255)
                for yy in range(max(0, y + PAD), min(CH, y + h + PAD)):
                    for xx in range(max(0, x + PAD), min(CW, x + w + PAD)): px[xx, yy] = col
            ims.append(im)
        _CACHE[k] = (ims, d["ticks"], (d["w"], d["h"]))
    return _CACHE[k]


def anims(ch): return [a for a in ANIMS if os.path.exists(os.path.join(ANIM, ch, a + ".json"))]
def desk_anims(ch): return sorted(f[:-5] for f in os.listdir(os.path.join(ANIM, ch)) if f.startswith("desk"))


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
    ims, ticks, _ = load(ch, an); im = ims[frame_index(ticks, int((t - t0) * 1000), loop)]
    if flip: im = im.transpose(Image.FLIP_LEFT_RIGHT)
    if k != 1: im = im.resize((im.width * k, im.height * k), Image.NEAREST)
    return im


def body(ch, an, k=1):
    """(w, h) of the character's own 64 px grid box at scale k: use it for shadows and bubble heights, not the padded frame."""
    w, h = load(ch, an)[2]; return w * k, h * k


def duration(ch, an): return sum(load(ch, an)[1]) / 1000.0


DESK = {"V2_0[56]([A-Za-z]+?)Desk34\\.dc\\.html$": "desk34", "V2_0[56]([A-Za-z]+?)Desk\\.dc\\.html$": "desk"}
def build_desk(src_dir):
    """Kit's V2.05 desk boards (2026-11-03): several animations per board, each an <svg aria-label="<Name> at the desk: <action>, looping">
    of <use href="#<frame>" class="<anim>_<i>">; holds from each use's @keyframes. -> tools/anim/<char>/<desk|desk34>_<action>.json
    Actions: idle, type, phone, sip, stare (Theo's front board also side_idle, side_type, side_stare)."""
    n = 0
    for f in sorted(os.listdir(src_dir)):
        kind = None
        for pat, k in DESK.items():
            m = re.match(pat, f)
            if m: kind = k; break
        if not kind or m.group(1) not in CHARS: continue
        ch = CHARS[m.group(1)]; html = open(os.path.join(src_dir, f), encoding="utf-8").read()
        defs = re.search(r'<svg[^>]*>\s*<defs>(.*?)</defs>', html, re.S).group(1)
        frames = {k + i: [(int(x), int(y), int(w), int(h), c) for x, y, w, h, c in
                  re.findall(r'<rect x="(-?\d+)" y="(-?\d+)" width="(\d+)" height="(\d+)" fill="(#[0-9A-Fa-f]{6})"', body)]
                  for k, i, body in re.findall(r'<g id="([A-Za-z]+?)(\d+)">(.*?)</g>', defs, re.S)}
        if not any(frames.values()): print("skip (not the desk-board format):", f); continue
        W = max(x + w for fr in frames.values() for x, y, w, h, c in fr); H = max(y + h for fr in frames.values() for x, y, w, h, c in fr)
        for label, body in re.findall(r'<svg[^>]*aria-label="[^"]*at the desk: ([^",]+), looping"[^>]*>(.*?)</svg>', html, re.S):
            act = label.strip().replace("turn to camera", "stare").replace(" ", "_")
            uses = re.findall(r'<use href="#([A-Za-z]+\d+)" class="([A-Za-z0-9_]+)"', body)
            seq, holds = [], []
            for ref, cls in uses:
                dur = float(re.search(r'\.' + cls + r'\{animation:' + cls + r' ([\d.]+)s', html).group(1))
                kf = re.search(r'@keyframes ' + cls + r'\{(.*?)\}\s*\.', html, re.S).group(1)
                pcts = [float(p) for p in re.findall(r'([\d.]+)%\{opacity:1\}', kf)]
                seq.append(frames[ref]); holds.append(max(1, round((max(pcts) - min(pcts)) / 100 * dur * 1000)))
            os.makedirs(os.path.join(ANIM, ch), exist_ok=True)
            json.dump({"w": W, "h": H, "frames": seq, "ticks": holds, "ms": sum(holds), "source": f"Mascot Designs · {f}"},
                      open(os.path.join(ANIM, ch, f"{kind}_{act}.json"), "w"), separators=(",", ":"))
            n += 1; print(f"{ch:6s} {kind}_{act:12s} {len(seq):2d} frames {W}x{H} {sum(holds)} ms")
    print(n, "desk animations")


if __name__ == "__main__":
    if sys.argv[1] == "build": build(sys.argv[2])
    elif sys.argv[1] == "desk": build_desk(sys.argv[2])


def build_captured(src_dir, items, fps=10):
    """Boards whose groups can't be parsed alone (V2.06: the board also draws Theo for scale): capture the '<Name> <Anim>, looping'
    svg in Chromium at fps over one loop and store each frame as 1 px row-runs. items: [(file, label, ch, anim, seconds)]."""
    from board_capture import capture
    for f, label, ch, an, dur in items:
        n = max(1, int(round(dur * fps))); ims = capture(os.path.join(src_dir, f), label, [i / fps + 0.02 for i in range(n)], scale=1)
        frames = []
        for im in ims:
            px = im.load(); rects = []
            for y in range(im.height):
                x = 0
                while x < im.width:
                    r, g, b, a = px[x, y]
                    if a < 128: x += 1; continue
                    x0 = x; col = (r, g, b)
                    while x < im.width and px[x, y][3] >= 128 and px[x, y][:3] == col: x += 1
                    rects.append((x0, y, x - x0, 1, "#%02X%02X%02X" % col))
            frames.append(rects)
        Wd = max(x + w for fr in frames for x, y, w, h, c in fr); Hd = max(y + h for fr in frames for x, y, w, h, c in fr)
        os.makedirs(os.path.join(ANIM, ch), exist_ok=True)
        json.dump({"w": Wd, "h": Hd, "frames": frames, "ticks": [int(1000 / fps)] * n, "ms": int(n * 1000 / fps), "source": f"Mascot Designs · {f} (captured)"},
                  open(os.path.join(ANIM, ch, an + ".json"), "w"), separators=(",", ":"))
        print(f"{ch:6s} {an:10s} {n} frames {Wd}x{Hd}")
