"""Reading-time pacing for daily.py specs (the boss 2026-11-23: "adjust the times for the average watcher, a tad faster").
Average silent reading is ~4 words/s; we pace at 4.4 words/s, +0.45 s per number, +0.9 s settle per scene.
pace(S, vis) re-times S["scenes"] (and their bubbles) from what is on screen; vis = {scene_index: (words, numbers)} for chart text."""
import re
WPS, NUM_S, SETTLE, MIN_S = 4.4, 0.45, 0.9, 3.5

def _count(texts):
    w = n = 0
    for t in texts:
        for tok in str(t).split():
            if re.search(r"\d", tok): n += 1
            else: w += 1
    return w, n

def pace(S, vis=None):
    vis = vis or {}; out, t, rows = [], 0.0, []
    for i, sc in enumerate(S["scenes"]):
        _, _, lab, heads, body, says, cast, ch = sc
        w, n = _count([lab] + [h for h, _ in heads] + list(body)); vw, vn = vis.get(i, (0, 0)); w += vw; n += vn
        bw = [len(s[3].split()) for s in says]
        read = SETTLE + w / WPS + n * NUM_S
        bub = sum(max(1.4, x / WPS + 0.6) for x in bw) + 0.6
        dur = round(max(MIN_S, read, bub), 1)
        b0, nsays = t + 0.5, []
        for (_, _, who, line, pose), x in zip(says, bw):
            bl = max(1.4, x / WPS + 0.6); slot = (dur - 0.7) / max(1, len(says))
            nsays.append((round(b0, 1), round(b0 + max(bl, slot - 0.2), 1), who, line, pose)); b0 += slot
        out.append((round(t, 1), round(t + dur, 1), lab, heads, body, nsays, cast, ch))
        rows.append((i, lab, w, n, round(read, 1), round(bub, 1), dur)); t += dur
    S["scenes"] = out; S["end"] = round(t, 1)
    return rows
