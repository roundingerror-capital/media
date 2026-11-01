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
                              (HYPOTHETICAL: did the next-day close stay above the strike? Theo's field when present; otherwise
                              arithmetic on the sheet's own last_8 moves and expected move. --derive stamps TEMPLATE TEST for test renders.)
  Theo's JOB E layout is accepted too: last_8_moves[{report, close_before, close_after, pct}], avg_abs_move_pct, up_days, down_days,
  expected_move{pct, strike, expiry, spot, quote_time}, numbers.ticker.
  wording                     the one holding line, copied as written ("The fund holds no UBER." / "The fund holds UBER puts.")
  company.one_liner           optional, what the company does, with its source on the sheet
Usage: python3 tools/earnings.py <sheet.json> <out_dir> [--derive]
"""
import json, os, sys, re, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
W_, L_, OR = "#F2F2EE", "#C8F03C", "#FF8A5B"
HERE = os.path.dirname(os.path.abspath(__file__))
PLATES = os.path.join(os.path.dirname(HERE), "..", "work", "interest")
ST = os.path.normpath(os.path.join(HERE, "..", "..", "work", "interest", "plate_standup_clean.png"))
PN = os.path.normpath(os.path.join(HERE, "..", "..", "work", "interest", "plate_penny.png"))
TAGS = ["#earnings", "#optionstrading", "#stockmarket", "#thewheel", "#aitrading"]  # exactly 5 (Posts rule)

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

def put_test(n, derive):
    pt = n.get("put_test")
    if pt: return pt, False
    if straddle(n, False) is None: return None, False   # no expected move, no strike to test
    # Not on the sheet: arithmetic on the sheet's own numbers (like the paid-twice interest math), stamped HYPOTHETICAL.
    # A put struck the implied move below the close before the report: did the next-day close stay above it?
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
    sc = [
        [0.0, 4.5, f"EARNINGS PREVIEW · {T}", [[f"{T} reports", W_], [f"{day}, {tm}.", L_]],
         ([f"Options priced a move of about {pct(x)}" + (f" ({ao})." if ao else ".")] if x else [f"Average move, last {N} reports: {pct(s['average_size_of_move_pct'])}."]) + ([one] if one else []),
         [[0.4, 2.2, "penny", "Big one?!", "jump"], [2.4, 4.3, "theo", "Let's look back.", "nod"]], ["penny", "theo"], 0],
        [4.5, 13.0, f"LAST {N} REPORTS · NEXT-DAY MOVE", [[f"Up {s['up']}. Down {s['down']}.", W_], [f"Average size {pct(s['average_size_of_move_pct'])}.", L_]],
         [(f"Median {pct(s['median_size_pct'])}. " if s.get("median_size_pct") is not None else "") + "Close before vs close after the report."],
         [[10.6, 12.8, "theo", "Numbers, not vibes.", "brow"]], ["theo", "ada"], 0]]
    charts = {1: {"vals": [m["move_pct"] for m in moves], "labels": labels, "note": "Past moves. Not a prediction."}}
    visuals = {}; t = 13.0
    if pt:
        sc.append([t, t + 9.5, "WOULD A PUT HAVE BEEN SAFE? · HYPOTHETICAL", [[f"A put {pct(pt['strike_pct_below'])} below", W_], ["the close before…", L_]], [],
                  [[t + 6.6, t + 9.3, "theo", "Past moves. No promise.", "brow"]], ["theo", "ada"], 0])
        visuals[2] = {"kind": "calc", "two_line": True, "hypo": True, "every": 1.5, "size": 1.0,
                      "stamp": "TEMPLATE TEST" if test else "HYPOTHETICAL",
                      "rows": [["Reports where the stock stayed above it", f"{pt['held']} of {N}", L_],
                               ["Reports where it broke through", f"{pt['broke']} of {N}", OR],
                               ["Worst next-day drop", f"−{pct(abs(pt['worst_drop_pct']))}", OR]],
                      "total": ["Hypothetical. No trade was made.", "", W_]}
        t += 9.5
    sc.append([t, t + 6.5, "OUR RULE", [["We don't guess", W_], ["the direction.", L_]],
               ["Earnings move big, both ways. We don't bet on it."] + ([hold] if hold else []),
               [[t + 3.2, t + 6.3, "ada", "Data says: humble.", "thumbs"]], ["theo", "ada"], 1 if hold else -1]); t += 6.5
    sc.append([t, t + 4.5, "YOUR TURN", [["Holding through", W_], ["earnings?", L_]], ["Tell us below."],
               [[t + 0.3, t + 4.3, "penny", "Comment!", "point"]], ["penny", "ada", "theo"], 0]); end = t + 4.5
    return {"label": "EARNINGS", "end": end, "bpm": 126, "root": 49.0, "seed": sum(map(ord, T)) + 1101, "mel": 1, "chart": "zigzag",
            "hook": f"<< {T} EARNINGS. WHAT THE DATA SAYS.", "music": "hold_to_expiry", "music_start": 7.0,
            "bg": ST, "bgs": {0: PN, len(sc) - 1: PN}, "bg_dim": 0.26, "bg_blur": 2.0,
            "cold_open": {"big": f"±{pct(x)}" if x else T, "line": f"{T} EARNINGS {day.upper()}.", "shout": "HOW BIG A MOVE?!", "tone": "win"},
            "intro_cfg": {"tagline": "And this is what the data says ↓"},
            "endcard": {"line1": "LIKE + FOLLOW", "line2": "FOR MORE UPDATES", "show_positions": False},
            "scenes": sc, "charts": charts, "visuals": visuals,
            "memes": [{"t": 0.2, "dur": 2.0, "kind": "pov", "text": f"POV: {T} reports {day}"},
                      {"t": 5.0, "dur": 1.6, "kind": "shades", "who": "theo"}],
            "_test": test}

def caption(sheet):
    sheet = normalize(sheet); n = sheet["numbers"]; T = sheet["ticker"]; day, tm = when(n["report"]); s = n["summary"]; N = len(n["last_8_next_day_moves"])
    xs = straddle(n, False); ao = asof(n); hold = holding(sheet)
    em = f"The options market priced a move of about {pct(xs['pct_of_spot'])}{' ' + ao if ao else ''}. " if xs else ""
    pt, _ = put_test(n, False); mid = ""
    if pt: mid = f" Hypothetical: a put {pct(pt['strike_pct_below'])} below the prior close stayed above water in {pt['held']} of those {N}. Not a trade, not a plan."
    return (f"I'm an AI trading bot. {T} reports {day} {tm}. {em}"
            f"Last {N} reports: up {s['up']}, down {s['down']}, average move {pct(s['average_size_of_move_pct'])}.{mid} {hold} Holding through earnings? 👇 "
            f"Not financial advice. " + " ".join(TAGS)).replace("  ", " ")

def card(sheet, sheet_id, mp4_blob=None, cover_blob=None):
    sheet = normalize(sheet); n = sheet["numbers"]; T = sheet["ticker"]; d = n["report"]["date"]
    return {"id": f"{d}-earnings-{T.lower()}", "title": f"Earnings preview · {T}", "series": "Earnings", "stage": "brainstorm",
            "kind": "event", "post_by": (datetime.date.fromisoformat(d) - datetime.timedelta(days=2)).isoformat(),
            "caption": caption(sheet), "hashtags": TAGS, "networks": ["instagram", "tiktok", "youtube"],
            "media": {"music": "Original song: Hold to Expiry · Rounding Error original", "ai_label": True},
            "theo_check": {"sheet": sheet_id, "status": "sourced", "note": "every number on screen is a field of this sheet (tools/earnings.py)"},
            "files": [b for b in (mp4_blob, cover_blob) if b], "penny_reply": "Earnings master template (tools/earnings.py). Brainstorm draft: no Roz until the boss says ready for review."}

def cover(sheet, out_jpg):
    from PIL import Image, ImageDraw
    import daily; from make_reel import W, H, archivo, mono, fit
    sheet = normalize(sheet); n = sheet["numbers"]; T = sheet["ticker"]; day, tm = when(n["report"]); xs = straddle(n, False); N = len(n["last_8_next_day_moves"])
    big = f"\u00b1{pct(xs['pct_of_spot'])}?" if xs else f"{pct(n['summary']['average_size_of_move_pct'])}"
    img = Image.new("RGB", (W, H), "#000000"); d = ImageDraw.Draw(img)
    d.text((daily.M, 420), f"EARNINGS PREVIEW · {day.upper()}", font=mono(34, True), fill=daily.LIME, anchor="ls")
    d.text((daily.M, 640), T, font=archivo(260, 125, 900), fill=daily.INK, anchor="ls")
    if big.startswith("\u00b1"):   # the sign smaller and apart from the digits, so the scan's OCR reads the figure (not "4" + figure)
        pf = archivo(120, 125, 900); d.text((daily.M, 830), "\u00b1", font=pf, fill=daily.LIME, anchor="ls")
        d.text((daily.M + d.textlength("\u00b1", font=pf) + 30, 860), big[1:], font=archivo(200, 125, 900), fill=daily.LIME, anchor="ls")
    else: d.text((daily.M, 860), big, font=archivo(200, 125, 900), fill=daily.LIME, anchor="ls")
    d.text((daily.M, 960), "what the last 8 reports say", font=fit("what the last 8 reports say", daily.SAFE_R - daily.M, 64, wdth=110, wght=800), fill=daily.INK, anchor="ls")
    s = daily.sprite_state("penny", False, 0); h = 520; s = s.resize((int(s.width * h / s.height), h), Image.NEAREST); img.paste(s, (W // 2 - s.width // 2, 1700 - h), s)
    s = daily.sprite_state("theo", False, 0); h = 440; s = s.resize((int(s.width * h / s.height), h), Image.NEAREST); img.paste(s, (W // 2 + 180, 1700 - h), s)
    img = daily.nfa(img); img.save(out_jpg, quality=92); return out_jpg

def render(sheet, out_dir, derive=False):
    import daily, subprocess
    sheet = normalize(sheet); os.makedirs(out_dir, exist_ok=True); T = sheet["ticker"].lower()
    S = build_spec(sheet, derive); cj = cover(sheet, os.path.join(out_dir, f"earnings_{T}_cover.jpg"))
    raw = os.path.join(out_dir, f"earnings_{T}_raw.mp4"); out = os.path.join(out_dir, f"earnings_{T}.mp4")
    daily.build(S, raw, cj, workdir=out_dir)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-c:v", "libx264", "-preset", "slow", "-crf", "23", "-tune", "animation", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", out], check=True); os.remove(raw)
    open(os.path.join(out_dir, f"earnings_{T}_caption.txt"), "w").write(caption(sheet))
    return out, cj, S

if __name__ == "__main__":
    sheet = json.load(open(sys.argv[1])); sheet = sheet.get("data", sheet)
    out, cj, S = render(sheet, sys.argv[2], derive="--derive" in sys.argv)
    print(out, cj, f"{S['end']:.1f}s" , "TEMPLATE TEST" if S["_test"] else "")
