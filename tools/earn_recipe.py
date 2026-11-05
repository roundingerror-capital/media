"""EARNINGS RECIPE (the boss 2026-11-05: "not all earnings videos the same, a tad of randomization, 1 in a billion, no chance of going rogue").

One roll per video picks from FIXED, pre-approved menus: room, time of day, history-chart style, each character's palette swap,
the opener shout and the joke set. Dice pick; they never write. Every word and number still comes from Theo's sheet or from a line
on Roz's cleared list (ROZ_CLEARED below). Same ticker + report date = same recipe (re-renders are frame-identical). The recipe is
saved on the Posts card (`recipe`) and in tools/casting_ledger.json, and a recipe already used is re-rolled, so no two repeat.

Adding an option = append it to its menu here; a new LINE goes in PENDING_ROZ until Roz clears it once, then moves to ROZ_CLEARED.
"""
import json, os, random, hashlib
import numpy as np
from PIL import Image

# rooms Kit drew that our renderer crops cleanly (ROOM-05/13/17/20 left out: 05/13/17 don't exist, 20 is the band stage)
ROOMS = ["ROOM-01", "ROOM-02", "ROOM-03", "ROOM-04", "ROOM-06", "ROOM-07", "ROOM-08", "ROOM-09", "ROOM-10", "ROOM-11",
         "ROOM-12", "ROOM-14", "ROOM-15", "ROOM-16", "ROOM-18", "ROOM-19"]
BOOKENDS = ["OFF-PENNY-01", "OFF-THEO-01", "OFF-ADA-01", "OFF-KIT-01", "OFF-ROZ-01"]   # first and last slide; never the boss's office
TOD = {"day": None, "dusk": (255, 140, 70, 46), "night": (40, 60, 140, 70)}            # RGBA wash over the room, text band untouched
CHARTS = ["coaster", "monitor"]   # earn_charts.py styles that clear the meme lane; "cards"/"scoreboard" overlap the twist banner (fix, then add back)
SWAP_P = 0.35                                                                            # chance each character wears one of Kit's swaps

# Lines the dice may use. Only lines already on approved videos (Roz-cleared in context) are here today.
ROZ_CLEARED = {
    "shout": ["HOW BIG A MOVE?!"],
    "pov1": ["POV: {T} reports {day}"],
    "pov2": ["POV: you held through earnings"],
    "zoom": ["HOLD ON"],
}
# Drafted 2026-11-05 by Penny, NOT usable until Roz clears each line once (board ask 20261105-171500-penny-recipe1).
# Rules for every line: no numbers, no picks, no outcome hype, no "safe", no promises.
PENDING_ROZ = {
    "shout": ["BIG MOVE OR NAP?!", "WHAT DOES HISTORY SAY?", "HERE WE GO AGAIN?!", "REPORT CARD DAY!", "BRACE OR YAWN?!",
              "PLOT TWIST INCOMING?", "ROLL THE TAPE!", "RECEIPTS FIRST.", "HOLD ONTO SOMETHING?!"],
    "pov1": ["POV: {T} reports {day}, you check the history first", "POV: it's {T}'s turn", "POV: {day} has {T} on it"],
    "pov2": ["POV: you looked at the last 8 reports", "POV: the data, not the hype", "POV: you read before you react"],
    "zoom": ["WAIT FOR IT", "BUCKLE UP", "NOT SO FAST", "AND THEN…"],
}

def menu(slot): return ROZ_CLEARED[slot]

def roll(ticker, report_date, used, attempt_cap=50):
    """Deterministic for (ticker, report_date); re-rolls past any recipe key in `used` (a set of keys)."""
    import swaps
    for a in range(attempt_cap):
        r = random.Random(f"{ticker}|{report_date}|{a}")
        rec = {"room": r.choice(ROOMS), "bookend": r.choice(BOOKENDS), "tod": r.choice(list(TOD)), "chart": r.choice(CHARTS),
               "swaps": {c: (r.choice(swaps.names(c)) if r.random() < SWAP_P else None) for c in ["theo", "penny", "ada", "kit", "roz"]},
               "shout": r.choice(menu("shout")), "pov1": r.choice(menu("pov1")), "pov2": r.choice(menu("pov2")), "zoom": r.choice(menu("zoom"))}
        k = key(rec)
        if k not in used: rec["key"] = k; rec["attempt"] = a; return rec
    raise RuntimeError("recipe: no unused combination after 50 rolls")

def key(rec):
    return hashlib.sha1(json.dumps({k: rec[k] for k in ("room", "bookend", "tod", "chart", "swaps", "shout", "pov1", "pov2", "zoom")},
                                   sort_keys=True).encode()).hexdigest()[:12]

def combos():
    import swaps
    n = len(ROOMS) * len(BOOKENDS) * len(TOD) * len(CHARTS)
    for c in ["theo", "penny", "ada", "kit", "roz"]: n *= len(swaps.names(c)) + 1
    for s in ROZ_CLEARED: n *= len(ROZ_CLEARED[s])
    return n

# ---------------------------------------------------------------- render helpers (fast palette swap, time-of-day wash)
_LUT = {}
def recolor(img, ch, swap):
    """Kit's palette swap on any rig frame, vectorised (tools/swaps.py maps, exact colours only, alpha kept)."""
    if not swap: return img
    import swaps
    if (ch, swap) not in _LUT:
        m = swaps.maps(ch)[swap]
        _LUT[(ch, swap)] = (np.array([(a[0] << 16) | (a[1] << 8) | a[2] for a in m], np.int64), np.array(list(m.values()), np.uint8))
    src, dst = _LUT[(ch, swap)]
    a = np.array(img.convert("RGBA")); p = (a[..., 0].astype(np.int64) << 16) | (a[..., 1].astype(np.int64) << 8) | a[..., 2]
    order = np.argsort(src); srt = src[order]
    idx = np.clip(np.searchsorted(srt, p), 0, len(srt) - 1); hit = (srt[idx] == p) & (a[..., 3] > 0)
    a[..., :3][hit] = dst[order][idx[hit]]
    return Image.fromarray(a, "RGBA")

def wash(img, tod):
    c = TOD.get(tod)
    if not c: return img
    ov = Image.new("RGBA", img.size, c); return Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
