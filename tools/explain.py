"""Worked-example panels for lesson videos (the boss 2026-10-28: "a visual example people can pause and go 'ah, that makes sense'").
Each panel reveals one step at a time inside its scene, so any paused frame reads on its own.
spec["visuals"] = {scene_index: {"kind": ..., ...}}. Every number in a panel must be copied from a Theo fact sheet;
math that is not a real trade carries "hypo": True and shows a HYPOTHETICAL stamp."""
from PIL import ImageDraw
from make_reel import W, archivo, mono, fit, fade, blend

M = 72; LIME = "#C8F03C"; INK = "#F2F2EE"; MUT = "#9A9A94"; LINE = "#262626"; RED = "#FF6B5B"; AMB = "#FFC24B"; PANEL = "#0E0E0E"


def _stamp(d, x, y):
    d.rectangle([x, y, x + 280, y + 44], fill="#FF8A5B")
    d.text((x + 140, y + 32), "HYPOTHETICAL", font=mono(26, True), fill="#000000", anchor="ms")


def _step(d, y, n, tot, text, a=1.0):
    """'STEP 2/4' chip + the step's one-line instruction."""
    chip = f"STEP {n}/{tot}"; f = mono(28, True); w = f.getlength(chip) + 32
    d.rectangle([M, y, M + w, y + 48], fill=blend(LIME, a)); d.text((M + 16, y + 35), chip, font=f, fill="#000000", anchor="ls")
    d.text((M + w + 20, y + 36), text, font=mono(30, True), fill=blend(INK, a), anchor="ls")
    return y + 72


def book(d, v, u, y):
    """Order book walk. v: {side, levels:[[price, size]], order, fills:[[price, qty]], avg, top, diff, note, hypo}.
    0-1.2 s: only the top level is visible (what the app shows). Then the hidden levels appear, then the order eats them."""
    lv = v["levels"]; rh = 74; x0, x1 = M, W - M
    reveal = u > v.get("reveal_at", 1.2)
    d.text((x0, y + 30), v.get("title", "THE ORDER BOOK"), font=mono(26, True), fill=MUT, anchor="ls"); y += 50
    d.text((x0 + 20, y + 28), "PRICE", font=mono(24, True), fill=MUT, anchor="ls"); d.text((x0 + 330, y + 28), "SHARES WAITING", font=mono(24, True), fill=MUT, anchor="ls")
    d.text((x1 - 20, y + 28), "WE GET", font=mono(24, True), fill=MUT, anchor="rs"); y += 44
    fills = v.get("fills", []); step_t = v.get("fill_at", 2.4); per = 0.75
    for i, (px, sz) in enumerate(lv):
        vis = i == 0 or reveal
        took = u > step_t + i * per and i < len(fills)
        fill_bg = "#2A1210" if took else PANEL
        d.rectangle([x0, y, x1, y + rh - 8], fill=fill_bg, outline=LIME if i == 0 else LINE, width=4 if i == 0 else 2)
        if vis:
            d.text((x0 + 20, y + 48), px, font=archivo(46, 110, 900), fill=INK, anchor="ls")
            d.text((x0 + 330, y + 48), sz, font=mono(36, True), fill=INK, anchor="ls")
            if took: d.text((x1 - 20, y + 48), fills[i][1] + " @ " + fills[i][0], font=mono(32, True), fill=RED, anchor="rs")
        else:
            d.text((x0 + 20, y + 48), "? ? ?", font=archivo(46, 110, 900), fill="#3A3A3A", anchor="ls")
            d.text((x0 + 330, y + 48), "hidden from you", font=mono(30, True), fill="#3A3A3A", anchor="ls")
        y += rh
    if not reveal:
        d.text((x0, y + 40), "Your app shows you THIS line. Only this.", font=mono(32, True), fill=AMB, anchor="ls")
    elif u > step_t + len(fills) * per + 0.3:
        d.text((x0, y + 44), f"Average fill {v['avg']}  vs  top {v['top']}", font=mono(34, True), fill=INK, anchor="ls")
        d.text((x0, y + 96), v["diff"], font=archivo(54, 110, 900), fill=RED, anchor="ls")
    if v.get("hypo"): _stamp(d, x1 - 280, y + 110)
    if v.get("note"): d.text((x0, y + 190), v["note"], font=mono(22), fill=MUT, anchor="ls")
    return y + 210


def gap(d, v, u, y):
    """Overnight gap. v: {close:[label, price], open:[label, price], move, line1, line2, note}."""
    h = 420; x0, x1 = M + 40, W - M - 40; top = y + 20
    p_c, p_o = float(v["close"][1].strip("$")), float(v["open"][1].strip("$")); hi, lo = max(p_c, p_o), min(p_c, p_o); pad = (hi - lo) * 0.6
    def Y(p): return top + (hi + pad - p) / (hi - lo + 2 * pad) * h
    xc, xo = x0 + 160, x1 - 160
    d.line([(x0, Y(p_c)), (xc, Y(p_c))], fill=INK, width=8); d.ellipse([xc - 14, Y(p_c) - 14, xc + 14, Y(p_c) + 14], fill=INK)
    d.text((x0, Y(p_c) - 26), v["close"][0] + "  " + v["close"][1], font=mono(30, True), fill=INK, anchor="ls")
    if u > 1.0:
        k = min(1, (u - 1.0) / 0.6)
        d.rectangle([xc + 30, Y(p_c), xo - 30, Y(p_c) + (Y(p_o) - Y(p_c)) * k], fill="#3A1410")
        for yy in range(int(Y(p_c)), int(Y(p_c) + (Y(p_o) - Y(p_c)) * k), 22): d.line([(xc + 30, yy), (xo - 30, yy)], fill="#5A2018", width=2)
        d.text(((xc + xo) // 2, (Y(p_c) + Y(p_o)) / 2 + 14), "NO TRADES HERE", font=mono(28, True), fill=RED, anchor="ms")
    if u > 1.8:
        d.ellipse([xo - 14, Y(p_o) - 14, xo + 14, Y(p_o) + 14], fill=RED); d.line([(xo, Y(p_o)), (x1, Y(p_o) + 30)], fill=RED, width=8)
        d.text((x1, Y(p_o) + 70), v["open"][0] + "  " + v["open"][1], font=mono(30, True), fill=RED, anchor="rs")
        d.text(((xc + xo) // 2, top + h + 60), v["move"], font=archivo(64, 110, 900), fill=RED, anchor="ms")
    y = top + h + 100
    if u > 2.6: d.text((M, y + 20), v["line1"], font=mono(32, True), fill=INK, anchor="ls")
    if u > 3.4: d.text((M, y + 70), v["line2"], font=mono(32, True), fill=AMB, anchor="ls")
    if v.get("note"): d.text((M, y + 120), v["note"], font=mono(22), fill=MUT, anchor="ls")
    return y + 140


def calc(d, v, u, y):
    """Step-by-step arithmetic. v: {rows:[[label, value, color]], total:[label, value, color], every, hypo, note}."""
    ev = v.get("every", 1.1); x0, x1 = M, W - M
    for i, (lab, val, col) in enumerate(v["rows"]):
        a = fade(u, i * ev, i * ev + 0.25)
        if a <= 0: break
        d.rectangle([x0, y, x1, y + 84], fill=PANEL, outline=LINE, width=2)
        d.text((x0 + 24, y + 54), lab, font=mono(32, True), fill=blend(INK, a), anchor="ls")
        d.text((x1 - 24, y + 56), val, font=archivo(48, 110, 900), fill=blend(col or INK, a), anchor="rs"); y += 96
    n = len(v["rows"])
    if v.get("total") and u > n * ev:
        lab, val, col = v["total"]; d.line([(x0, y + 6), (x1, y + 6)], fill=INK, width=4); y += 20
        d.text((x0 + 24, y + 62), lab, font=mono(36, True), fill=INK, anchor="ls"); d.text((x1 - 24, y + 66), val, font=archivo(66, 110, 900), fill=col or LIME, anchor="rs"); y += 100
    if v.get("hypo"): _stamp(d, x1 - 280, y + 6); y += 60
    if v.get("note"): d.text((x0, y + 30), v["note"], font=mono(22), fill=MUT, anchor="ls"); y += 50
    return y


def outcomes(d, v, u, y):
    """Three outcome cards, one per step. v: {cards:[{tag, price, lines:[[label, value]], total, col}], every, hypo, note}."""
    ev = v.get("every", 1.4); n = len(v["cards"]); gapw = 20; cw = (W - 2 * M - gapw * (n - 1)) // n; ch = 520
    for i, c in enumerate(v["cards"]):
        a = fade(u, i * ev, i * ev + 0.3)
        x0 = M + i * (cw + gapw); col = c.get("col", INK)
        d.rectangle([x0, y, x0 + cw, y + ch], fill=PANEL, outline=blend(col, a) if a > 0 else LINE, width=4)
        if a <= 0:
            d.text((x0 + cw // 2, y + ch // 2), str(i + 1), font=archivo(120, 110, 900), fill="#2A2A2A", anchor="ms"); continue
        d.text((x0 + cw // 2, y + 56), c["tag"], font=mono(26, True), fill=blend(col, a), anchor="ms")
        d.text((x0 + cw // 2, y + 140), c["price"], font=archivo(64, 110, 900), fill=blend(INK, a), anchor="ms")
        yy = y + 210
        for lab, val in c["lines"]:
            d.text((x0 + cw // 2, yy), lab, font=mono(22), fill=blend(MUT, a), anchor="ms")
            d.text((x0 + cw // 2, yy + 44), val, font=archivo(40, 110, 900), fill=blend(INK, a), anchor="ms"); yy += 96
        d.text((x0 + cw // 2, y + ch - 30), c["total"], font=archivo(44, 110, 900), fill=blend(col, a), anchor="ms")
    y += ch + 20
    if v.get("hypo"): _stamp(d, W - M - 280, y); y += 60
    if v.get("note"): d.text((M, y + 30), v["note"], font=mono(22), fill=MUT, anchor="ls"); y += 50
    return y


def roll(d, v, u, y):
    """A roll is two trades. v: {left:[tag, value, sub], right:[tag, value, sub], net:[label, value, color], after, note}."""
    cw = (W - 2 * M - 120) // 2; ch = 330
    for i, (side, at) in enumerate(((v["left"], 0.0), (v["right"], 1.2))):
        a = fade(u, at, at + 0.3); x0 = M + i * (cw + 120)
        col = RED if side[1].startswith(("−", "-")) else LIME
        d.rectangle([x0, y, x0 + cw, y + ch], fill=PANEL, outline=blend(col, a) if a else LINE, width=4)
        if a:
            d.text((x0 + cw // 2, y + 64), side[0], font=mono(28, True), fill=blend(INK, a), anchor="ms")
            d.text((x0 + cw // 2, y + 190), side[1], font=archivo(80, 110, 900), fill=blend(col, a), anchor="ms")
            d.text((x0 + cw // 2, y + 262), side[2], font=mono(24), fill=blend(MUT, a), anchor="ms")
    if u > 1.2: d.text((W // 2, y + ch // 2 + 30), "+", font=archivo(90, 110, 900), fill=INK, anchor="ms")
    y += ch + 40
    if u > 2.4:
        lab, val, col = v["net"]; d.rectangle([M, y, W - M, y + 120], fill="#141414", outline=col, width=4)
        d.text((M + 30, y + 78), lab, font=mono(34, True), fill=INK, anchor="ls"); d.text((W - M - 30, y + 84), val, font=archivo(70, 110, 900), fill=col, anchor="rs")
    y += 150
    if u > 3.4 and v.get("after"): d.text((M, y + 20), v["after"], font=mono(30, True), fill=AMB, anchor="ls"); y += 60
    if v.get("note"): d.text((M, y + 30), v["note"], font=mono(22), fill=MUT, anchor="ls"); y += 50
    return y


def spread(d, v, u, y):
    """Bid/ask width at two times. v: {rows:[{time, bid, ask, width, pct}], scale:[lo, hi], every, note}."""
    lo, hi = v["scale"]; x0, x1 = M + 220, W - M - 20; ev = v.get("every", 1.6)
    def X(p): return x0 + (p - lo) / (hi - lo) * (x1 - x0)
    for i, r in enumerate(v["rows"]):
        a = fade(u, i * ev, i * ev + 0.3)
        if a <= 0: break
        b, k = float(r["bid"].strip("$")), float(r["ask"].strip("$")); col = RED if i == 0 else LIME
        d.text((M, y + 70), r["time"], font=mono(32, True), fill=blend(INK, a), anchor="ls")
        d.line([(x0, y + 60), (x1, y + 60)], fill=LINE, width=2)
        d.rectangle([X(b), y + 36, X(k), y + 84], fill=blend(col, a))
        d.text((X(b), y + 24), "bid " + r["bid"], font=mono(24, True), fill=blend(INK, a), anchor="ls")
        d.text((X(k), y + 118), "ask " + r["ask"], font=mono(24, True), fill=blend(INK, a), anchor="rs")
        d.text((x1, y + 160), f"gap {r['width']}  ({r['pct']} of the price)", font=mono(28, True), fill=blend(col, a), anchor="rs"); y += 200
    if v.get("note"): d.text((M, y + 20), v["note"], font=mono(22), fill=MUT, anchor="ls"); y += 50
    return y


KINDS = {"book": book, "gap": gap, "calc": calc, "outcomes": outcomes, "roll": roll, "spread": spread}


def draw(d, v, u, y):
    """Draw the scene's worked example; u = seconds since the scene started. Optional step chip on top."""
    if v.get("step"): y = _step(d, y, v["step"][0], v["step"][1], v["step"][2], fade(u, 0, 0.25))
    return KINDS[v["kind"]](d, v, u, y)
