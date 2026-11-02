"""EARNINGS PREVIEW · master template (Penny, the boss 2026-11-01: "this is how we're gonna do earnings from now on").
One Theo fact sheet in (numbers.what == "earnings_preview", public_ok), one video + one caption + one Posts card out.
Everything we learned is baked in: cover held, 1 s teaser, AI TRADING BOT intro, safe layout, NFA on every frame, big characters,
one of our own songs, HYPOTHETICAL stamp on every bit of math, no pick / no forecast / no "play", the fund's holding line from
the sheet's wording, end card without positions (an event post, not an evergreen), exactly 5 hashtags, "Not financial advice.".

Sheet fields read (every number on screen comes from here, nothing is typed by hand):
  numbers.report              {date, timing}                      "Wed 11/4 · before the open"
  numbers.straddle_<exp>      {pct_of_spot}                       "Options price about a 13% move"   (first key starting straddle_)
  numbers.last_8_next_day_moves [{report, move_pct}]              the 8 bars
  numbers.summary             {up, down, average_size_of_move_pct, median_size_pct}
  numbers.put_test            {strike_pct_below, held, broke, worst_drop_pct, note}   "a put X% below the close the day before"
                              (HYPOTHETICAL panel, shown ONLY when Theo's sheet carries this field (T-083). Roz 2026-11-02: counts
                              we compute ourselves are not sheet numbers, so no sheet field = no panel and no caption sentence.
                              --derive computes it from the sheet's own moves for TEMPLATE TESTS only, stamped TEMPLATE TEST.)
  History labels follow numbers.report.timing: "REPORT-DAY MOVE" for a before-open report (close the day before vs close on the
  report day), "NEXT-DAY MOVE" for an after-close report (Roz 2026-11-02, SHOP). The method slide quotes the sheet ("History, not a
  forecast.") and Rules §8 word for word ("Hold to expiry." / "Puts are never rolled."); no "OUR RULE" claims of our own.
  Theo's JOB E layout is accepted too: last_8_moves[{report, close_before, close_after, pct}], avg_abs_move_pct, up_days, down_days,
  expected_move{pct, strike, expiry, spot, quote_time}, numbers.ticker.
  wording                     the one holding line, copied as written ("The fund holds no UBER." / "The fund holds UBER puts.")
  company.one_liner           optional, what the company does, with its source on the sheet
Usage: python3 tools/earnings.py <sheet.json> <out_dir> [--derive]
"""
import json, os, sys, re, datetime, random
import earn_charts as EC   # chart styles for the history slide (the boss 2026-11-02 picked the rollercoaster)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
W_, L_, OR = "#F2F2EE", "#C8F03C", "#FF8A5B"
HERE = os.path.dirname(os.path.abspath(__file__))
PLATES = os.path.join(os.path.dirname(HERE), "..", "work", "interest")
ST = os.path.normpath(os.path.join(HERE, "..", "..", "work", "interest", "plate_standup_clean.png"))
PN = os.path.normpath(os.path.join(HERE, "..", "..", "work", "interest", "plate_penny.png"))

# ---------------------------------------------------------------- CASTING (the boss 2026-11-01)
# "cycle through active staff randomly on every slide; no two videos repeat the same staff combo or catchphrases;
#  placement a bit different." Active staff = Ops employees with status "active" (E-0001..E-0005; the boss E-0000 is
# an Easter egg, never cast). Lines are in each one's voice (Ops employees.personality), no numbers, no picks, no hype
# about outcomes. A ledger (tools/casting_ledger.json) remembers every combo and line used, per month, so a batch never repeats.
STAFF = ["theo", "penny", "ada", "kit", "roz"]
POSE = {"theo": ["nod", "brow"], "penny": ["jump", "point", "wave"], "ada": ["thumbs", "spin"], "kit": ["spin", "wave", "nod"], "roz": ["brow", "nod"]}
LINES = {   # bubble lines (<= 22 chars, no digits: the scan reads every number)
    "theo": ["Numbers, not vibes.", "History. Not a forecast.", "The math doesn't care.", "Calm down.", "Past moves only.", "Noted. Moving on.",
             "Read the chart.", "No adjectives, please.", "That is the whole story.", "Dry facts. Enjoy.", "Interesting. Moving on.", "As one does."],
    "penny": ["Big one?!", "Earnings szn!", "Save this one.", "Plot twist?!", "Wait for it...", "Comment below!", "Episode drop!", "Receipts, not vibes!",
              "Link in bio, besties.", "Okay but WHY?!", "Tell a friend!", "This one's spicy!"],
    "ada": ["All green!", "Data's fresh!", "Checked twice!", "Pipelines flowing!", "Ooh, a big bar!", "Every row verified!", "So clean!", "Fresh from the dam!",
            "Data says: humble.", "Look at those bars!", "Tiny bars, big feels!", "Numbers are happy!"],
    "kit": ["Boss fight incoming.", "New run. Same rules.", "Save point reached.", "Respawn with the rule.", "Read the patch notes.", "Hard mode unlocked.",
            "That's a boss, not a bug.", "Level up the rules.", "Checkpoint saved.", "No cheat codes here."],
    "roz": ["Not advice. Promise.", "Read the fine print.", "Shell first.", "Hypothetical. Noted.", "Careful counts.", "Slow on purpose.",
            "Past isn't promise.", "Footnote: no picks.", "I'll allow it.", "Careful is cool."],
}
XS_POOL = {1: [[.5], [.32], [.68]], 2: [[.3, .7], [.22, .62], [.38, .78], [.26, .74]], 3: [[.2, .5, .8], [.18, .45, .74], [.26, .54, .82]]}
LEDGER = os.path.join(HERE, "casting_ledger.json")

def _ledger(month):
    try: L = json.load(open(LEDGER))
    except Exception: L = {}
    return L, L.setdefault(month, {"combos": [], "lines": [], "hooks": [], "by_ticker": {}})

def cast_video(ticker, month, n_scenes, sizes, save=True):
    """Pick a cast per scene for one video. sizes = how many characters each scene shows. Returns
    {casts: [[names]], lines: [[name, line, pose]] per scene (one or two), xs: [[x...]], flips} and records it in the ledger.
    The same ticker in the same month gets the same casting back (re-renders stay stable)."""
    L, M = _ledger(month)
    if ticker in M["by_ticker"]:
        out = M["by_ticker"][ticker]
        if len(out["casts"]) == n_scenes: return out
        if len(out["casts"]) > n_scenes:
            # a slide left the video since this casting was made (the optional put-test slot at index 2): drop that slot so the
            # opening pair (the cover) and the closing trio stay as rendered and reviewed
            keep = list(range(len(out["casts"])))
            while len(keep) > n_scenes: keep.pop(2)
            out = {"casts": [out["casts"][i] for i in keep], "lines": [out["lines"][i] for i in keep], "xs": [out["xs"][i] for i in keep]}
            if save: M["by_ticker"][ticker] = out; json.dump(L, open(LEDGER, "w"), indent=1)
            return out
    r = random.Random(f"{ticker}-{month}")
    for attempt in range(400):
        casts = []; prev = None
        for k, sz in enumerate(sizes):
            while True:
                c = r.sample(STAFF, sz)
                if c != prev and (prev is None or set(c) != set(prev)): break
            casts.append(c); prev = c
        combo = "|".join(",".join(c) for c in casts); hook = ",".join(sorted(casts[0]))
        if combo in M["combos"]: continue
        if hook in M["hooks"] and attempt < 300: continue          # the opening pair differs from every other video when possible
        used = set(M["lines"]); picked = []; ok = True
        for k, c in enumerate(casts):
            speakers = c[:2] if k == 0 else [r.choice(c)]
            row = []
            for who in speakers:
                pool = [l for l in LINES[who] if l not in used]
                if not pool: pool = LINES[who][:]                   # pool spent this month: allow repeats (never inside one batch of 15)
                ln = r.choice(pool); used.add(ln); row.append([who, ln, r.choice(POSE[who])])
            picked.append(row)
        if not ok: continue
        xs = [r.choice(XS_POOL[len(c)]) for c in casts]
        out = {"casts": casts, "lines": picked, "xs": xs}
        if save:
            M["combos"].append(combo); M["hooks"].append(hook); M["lines"] += [ln for row in picked for _, ln, _ in row]; M["by_ticker"][ticker] = out
            json.dump(L, open(LEDGER, "w"), indent=1)
        return out
    raise RuntimeError("casting: no unique combo left this month")

TAGS = ["#earnings", "#optionstrading", "#stockmarket", "#thewheel", "#aitrading"]  # the generic set (legacy)
def tags(T):
    """Exactly 5 Instagram hashtags (Posts rule), two of them the ticker's own, because the earnings series exists for reach
    (the boss 2026-11-02: the PLTR post went out without #PLTR). YouTube adds #Shorts; TikTok takes the same five."""
    return [f"#{T}", f"#{T}earnings", "#earnings", "#optionstrading", "#aitrading"]

def pct(v):
    v = float(v); return f"{int(v)}%" if v.is_integer() else f"{v:.1f}%"

def when(rep):
    d = datetime.date.fromisoformat(rep["date"]); day = d.strftime("%a") + f" {d.month}/{d.day}"
    tm = rep.get("timing", ""); tm = {"after close": "after the close", "before open": "before the open"}.get(tm, tm)
    return day, tm

def straddle(n, need=True):
    em = n.get("expected_move")  # Theo JOB E layout (2026-10-31): expected_move {pct, strike, expiry, spot, quote_time}
    if em and em.get("pct") is not None: return {"pct_of_spot": em["pct"], **em}
    for k, v in n.items():
        if k.startswith("straddle_") and isinstance(v, dict) and "pct_of_spot" in v: return v
    if need: raise KeyError("no expected move on the sheet (expected_move.pct or straddle_<exp>.pct_of_spot)")
    return None

def asof(n):
    """'as of Fri 10/30 close' from the sheet's quote time (Theo's expected_move.quote_time or straddle at)."""
    x = straddle(n, False) or {}; q = x.get("quote_time") or x.get("at") or ""
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", q)
    if not m: return ""
    dd = datetime.date(int(m[1]), int(m[2]), int(m[3])); return f"as of {dd.strftime('%a')} {dd.month}/{dd.day}" + (" close" if "close" in q.lower() or "3:59" in q else "")

def holding(sheet):
    for src in (sheet.get("wording_holding"), sheet.get("what_happened", ""), sheet.get("wording", "")):
        for ln in re.split(r"(?<=\.)\s+", src or ""):
            if ln.strip().startswith("The fund holds"): return ln.strip()
    return ""

def normalize(sheet):
    """Accept both sheet layouts: the RDDT sheet (last_8_next_day_moves/move_pct, summary) and Theo's JOB E preview
    (last_8_moves/pct, avg_abs_move_pct, up_days, down_days). Returns the sheet with the RDDT names filled in."""
    n = sheet["numbers"]
    if "last_8_next_day_moves" not in n and "last_8_moves" in n:
        n["last_8_next_day_moves"] = [{"report": m["report"], "move_pct": m["pct"], "close_before": m.get("close_before"), "close_after": m.get("close_after")} for m in n["last_8_moves"]]
    if "summary" not in n:
        mv = sorted(abs(m["move_pct"]) for m in n["last_8_next_day_moves"]); k = len(mv)
        med = mv[k // 2] if k % 2 else (mv[k // 2 - 1] + mv[k // 2]) / 2
        n["summary"] = {"up": n.get("up_days", sum(1 for m in n["last_8_next_day_moves"] if m["move_pct"] > 0)),
                        "down": n.get("down_days", sum(1 for m in n["last_8_next_day_moves"] if m["move_pct"] < 0)),
                        "average_size_of_move_pct": n.get("avg_abs_move_pct", round(sum(mv) / k, 1)), "median_size_pct": None}   # not on Theo's sheet: not shown
    if "ticker" not in sheet: sheet["ticker"] = n["ticker"]
    return sheet

def bmo(n):
    """True for a before-the-open report: the sheet's moves are then report-day moves, not next-day moves."""
    return "before" in (n["report"].get("timing") or "").lower()

def put_test(n, derive):
    pt = n.get("put_test")
    if pt: return pt, False
    # Not on the sheet: no panel. The counts would be our arithmetic, not a Theo number (Roz, UBER audit 2026-11-02; T-083 asks
    # Theo to add put_test to the sheet). --derive keeps the template testable: computed from the sheet's own moves, TEMPLATE TEST stamp.
    if not derive or straddle(n, False) is None: return None, False
    # A put struck the implied move below the close before the report: did the close after the report stay above it?
    x = straddle(n)["pct_of_spot"]; mv = [m["move_pct"] for m in n["last_8_next_day_moves"]]
    broke = sum(1 for m in mv if m <= -x)
    return {"strike_pct_below": x, "held": len(mv) - broke, "broke": broke, "worst_drop_pct": min(mv),
            "note": "arithmetic on the sheet's last-8 moves and expected move; ask Theo to put put_test on the sheet (D-20261031-earnings-d2-1)"}, derive

def build_spec(sheet, derive=False):
    sheet = normalize(sheet); n = sheet["numbers"]; T = sheet["ticker"]; day, tm = when(n["report"])
    xs = straddle(n, False); x = xs["pct_of_spot"] if xs else None; ao = asof(n)
    moves = n["last_8_next_day_moves"]; s = n["summary"]; N = len(moves)
    labels = [f"{int(m['report'][5:7])}/{m['report'][2:4]}" for m in moves]
    hold = holding(sheet)
    pt, test = put_test(n, derive)
    one = (sheet.get("company") or {}).get("one_liner")
    mv_day = "report-day" if bmo(n) else "next-day"   # the sheet's sources.moves: before-open = close before vs close ON the report day
    sc = [
        [0.0, 4.5, f"EARNINGS PREVIEW · {T}", [[f"{T} reports", W_], [f"{day}, {tm}.", L_]],
         ([f"Options priced a move of about {pct(x)}" + (f" ({ao})." if ao else ".")] if x else [f"Average move, last {N} reports: {pct(s['average_size_of_move_pct'])}."])
         + ([f"Analysts expect EPS of ${n['report']['eps_estimate']:.2f} (Robinhood)."] if n["report"].get("eps_estimate") is not None else []) + ([one] if one else []),
         [[0.4, 2.2, "penny", "Big one?!", "jump"], [2.4, 4.3, "theo", "Let's look back.", "nod"]], ["penny", "theo"], 0],
        [4.5, 13.0, f"LAST {N} REPORTS · {mv_day.upper()} MOVE", [[f"Up {s['up']}. Down {s['down']}.", W_], [f"Average size {pct(s['average_size_of_move_pct'])}.", L_]],
         [(f"Median {pct(s['median_size_pct'])}. " if s.get("median_size_pct") is not None else "") + "Close before vs close after the report."],
         [[10.6, 12.8, "theo", "Numbers, not vibes.", "brow"]], ["theo", "ada"], 0]]
    charts = {1: {"draw": EC.make("coaster", [m["move_pct"] for m in moves], labels, s["average_size_of_move_pct"])}}   # the rollercoaster: Kit rides the moves
    visuals = {}; t = 13.0
    if pt:
        # Theo's put_test field only (see put_test). No "safe": a hindsight count, not a safety claim (Roz 2026-11-02).
        sc.append([t, t + 9.5, "HOW FAR DID IT FALL? · HYPOTHETICAL", [[f"A put {pct(pt['strike_pct_below'])} below", W_], ["the close before…", L_]], [],
                  [[t + 6.6, t + 9.3, "theo", "Past moves. No promise.", "brow"]], ["theo", "ada"], 0])
        visuals[2] = {"kind": "calc", "two_line": True, "hypo": True, "every": 1.5, "size": 1.0,
                      "stamp": "TEMPLATE TEST" if test else "HYPOTHETICAL",
                      "rows": [["Reports where the stock stayed above it", f"{pt['held']} of {N}", L_],
                               ["Reports where it broke through", f"{pt['broke']} of {N}", OR],
                               [f"Worst {mv_day} drop", f"−{pct(abs(pt['worst_drop_pct']))}", OR]],
                      "total": ["Hypothetical, not a recommendation.", "", W_]}
        t += 9.5
    # The method slide: the sheet's own wording ("History, not a forecast.") and Rules §8 word for word ("Hold to expiry." /
    # "Puts are never rolled."). Nothing of ours: Roz 2026-11-02 struck "OUR RULE · We don't guess the direction… We don't bet on it."
    # (no sheet or decision backs it; Rules §6a lets a put span a report).
    sc.append([t, t + 6.5, "HISTORY, NOT A FORECAST", [["Our rule:", W_], ["hold to expiry.", L_]],
               ([hold] if hold else []) + ["Puts are never rolled."],
               [[t + 3.2, t + 6.3, "ada", "Data says: humble.", "thumbs"]], ["theo", "ada"], 0 if hold else -1]); t += 6.5
    sc.append([t, t + 4.5, "YOUR TURN", [["Holding through", W_], ["earnings?", L_]], ["Tell us below."],
               [[t + 0.3, t + 4.3, "penny", "Comment!", "point"]], ["penny", "ada", "theo"], 0]); end = t + 4.5
    # casting: random active staff per slide, unique per video this month (the ledger), varied placement
    month = n["report"]["date"][:7]; sizes = [2, 2] + ([2] if pt else []) + [2, 3]
    cv = cast_video(T, month, len(sc), sizes, save=not test)
    cast_x = {}
    for k, scn in enumerate(sc):
        t0, t1 = scn[0], scn[1]; c = cv["casts"][k]; rows = cv["lines"][k]
        if k == 0: tl = [[t0 + 0.4, t0 + 2.2], [t0 + 2.4, t1 - 0.2]]
        elif k == len(sc) - 1: tl = [[t0 + 0.3, t1 - 0.2]]
        elif k == 1: tl = [[t0 + 3.9, t1 - 0.2]]   # the boss 2026-11-02: no dead air after Kit's cart lands (~t0+3.6); the line lands with a zoom
        else: tl = [[t0 + 1.2, t1 - 0.2]]          # middle slides: react right after the headline, not 3 s before the slide ends
        if k == len(sc) - 1 and not any(w == c[0] for w, _, _ in rows): rows = [[c[0], rows[0][1], rows[0][2]]] if rows[0][0] not in c else rows
        scn[5] = [[a, b, w, ln, pose] for (a, b), (w, ln, pose) in zip(tl, rows)]
        if k == len(sc) - 1 and scn[5]: scn[5][0][3] = "Comment!" if scn[5][0][2] == "penny" else scn[5][0][3]
        scn[6] = c; cast_x[k] = cv["xs"][k]
        if k == 1 and scn[5]: twist = {"t": scn[5][0][0], "dur": 1.3, "kind": "zoom", "text": scn[5][0][3].upper(), "y": 330}   # "PLOT TWIST?!" punch-in with the bubble
    shades_who = next((w for w in cv["casts"][1] if w in ("theo", "penny", "ada", "kit", "roz")), "theo")
    return {"cast_x": cast_x, "cast_h": {1: 220}, "label": "EARNINGS", "end": end, "bpm": 126, "root": 49.0, "seed": sum(map(ord, T)) + 1101, "mel": 1, "chart": "zigzag",
            "hook": f"<< {T} EARNINGS. WHAT THE DATA SAYS.", "music": "hold_to_expiry_long", "music_start": 8.0,
            "bg": ST, "bgs": {0: PN, len(sc) - 1: PN}, "bg_dim": 0.26, "bg_blur": 2.0,
            "cold_open": {"big": f"±{pct(x)}" if x else T, "line": f"{T} EARNINGS {day.upper()}.", "shout": "HOW BIG A MOVE?!", "tone": "win"},
            "intro_cfg": {"tagline": "And this is what the data says ↓"},
            "endcard": {"line1": "LIKE + FOLLOW", "line2": "FOR MORE UPDATES", "show_positions": False},
            "scenes": sc, "charts": charts, "visuals": visuals,
            "memes": [{"t": 0.2, "dur": 2.0, "kind": "pov", "text": f"POV: {T} reports {day}"},
                      {"t": 4.8, "dur": 1.6, "kind": "pov", "text": "POV: you held through earnings", "y": 330},
                      {"t": 6.8, "dur": 1.2, "kind": "zoom", "text": "HOLD ON", "y": 330},   # as the cart flies off the end
                      {"t": 5.0, "dur": 1.6, "kind": "shades", "who": shades_who}, twist],
            "_test": test}

def caption(sheet):
    sheet = normalize(sheet); n = sheet["numbers"]; T = sheet["ticker"]; day, tm = when(n["report"]); s = n["summary"]; N = len(n["last_8_next_day_moves"])
    xs = straddle(n, False); ao = asof(n); hold = holding(sheet)
    em = f"The options market priced a move of about {pct(xs['pct_of_spot'])}{' ' + ao if ao else ''}. " if xs else ""
    pt, _ = put_test(n, False); mid = ""   # only when Theo's sheet carries put_test (T-083); never our own count
    if pt: mid = f" Hypothetical: a put {pct(pt['strike_pct_below'])} below the prior close finished above its strike in {pt['held']} of those {N}. Not a recommendation, not a plan."
    return (f"I'm an AI trading bot. {T} reports {day} {tm}. {em}"
            f"Last {N} reports: up {s['up']}, down {s['down']}, average move {pct(s['average_size_of_move_pct'])}. History, not a forecast.{mid} {hold} Holding through earnings? 👇 "
            f"Not financial advice. " + " ".join(tags(T))).replace("  ", " ")

def card(sheet, sheet_id, mp4_blob=None, cover_blob=None):
    sheet = normalize(sheet); n = sheet["numbers"]; T = sheet["ticker"]; d = n["report"]["date"]
    return {"id": f"{d}-earnings-{T.lower()}", "title": f"Earnings preview · {T}", "series": "Earnings", "stage": "brainstorm",
            "kind": "event", "post_by": (datetime.date.fromisoformat(d) - datetime.timedelta(days=2)).isoformat(),
            "caption": caption(sheet), "hashtags": tags(T), "networks": ["instagram", "tiktok", "youtube"],
            "media": {"music": "Original song: Hold to Expiry (long version) · Rounding Error original", "ai_label": True},
            "theo_check": {"sheet": sheet_id, "status": "sourced", "note": "every number on screen is a field of this sheet (tools/earnings.py)"},
            "files": [b for b in (mp4_blob, cover_blob) if b], "penny_reply": "Earnings master template (tools/earnings.py). Brainstorm draft: no Roz until the boss says ready for review."}

def cover(sheet, out_jpg, derive=False):
    """Cover: layout x background x the video's own opening cast, varied per video (tools/earn_covers.py)."""
    import earn_covers
    sheet = normalize(sheet); n = sheet["numbers"]; T = sheet["ticker"]; month = n["report"]["date"][:7]
    pt, test = put_test(n, derive); sizes = [2, 2] + ([2] if pt else []) + [2, 3]
    cv = cast_video(T, month, len(sizes), sizes, save=not test)
    L, Mo = _ledger(month); layout, bg = earn_covers.pick(T, month, Mo)
    if not test: json.dump(L, open(LEDGER, "w"), indent=1)
    return earn_covers.cover(sheet, out_jpg, cv["casts"][0], layout, bg)

def render(sheet, out_dir, derive=False):
    import daily, subprocess
    sheet = normalize(sheet); os.makedirs(out_dir, exist_ok=True); T = sheet["ticker"].lower()
    S = build_spec(sheet, derive); cj = cover(sheet, os.path.join(out_dir, f"earnings_{T}_cover.jpg"), derive)
    raw = os.path.join(out_dir, f"earnings_{T}_raw.mp4"); out = os.path.join(out_dir, f"earnings_{T}.mp4")
    daily.build(S, raw, cj, workdir=out_dir)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-tune", "animation", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", out], check=True); os.remove(raw)
    open(os.path.join(out_dir, f"earnings_{T}_caption.txt"), "w").write(caption(sheet))
    return out, cj, S

if __name__ == "__main__":
    sheet = json.load(open(sys.argv[1])); sheet = sheet.get("data", sheet)
    out, cj, S = render(sheet, sys.argv[2], derive="--derive" in sys.argv)
    print(out, cj, f"{S['end']:.1f}s" , "TEMPLATE TEST" if S["_test"] else "")
