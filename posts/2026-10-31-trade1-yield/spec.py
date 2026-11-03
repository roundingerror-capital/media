"""TRADE #1 · yield = premium ÷ cash set aside (evergreen, approved 2026-10-31). Rebuilt 2026-11-03 for the new wave from the approved
video, word for word and number for number (the original spec file was lost). Numbers: Theo fact sheet F-20261009-113645-fill
(public_ok; 1 UBER put, $67.50 strike, $189 premium, $6,750 cash set aside, 42 days, 2.8% if it expires)."""
W_, L_ = "#F2F2EE", "#C8F03C"
SPEC = {"label": "LESSON", "end": 22.5, "bpm": 132, "root": 45.0, "seed": 1031, "mel": 2, "chart": "climb",
  "hook": "<< HOW? REWIND.", "music": "the_clock_pays_rent",
  "bgs": {0: "OFF-THEO-01", 1: "ROOM-01", 2: "ROOM-15", 3: "ROOM-01"}, "bg_dim": 0.36,
  "cold_open": {"big": "2.8%", "line": "TRADE #1.", "shout": "IN 42 DAYS?!", "tone": "win"},
  "intro_cfg": {"tagline": "And this is what's going on ↓"},
  "endcard": {"line1": "LIKE + FOLLOW", "line2": "FOR MORE UPDATES", "show_positions": False}, "end_char": "penny",
  "scenes": [
    [0.0, 5.0, "TRADE #1 · OCT 9", [["Our first trade.", L_], ["Ever.", W_]], ["1 UBER put. $67.50 strike."],
     [[0.6, 2.4, "penny", "Trade number one!", "jump"], [2.8, 4.9, "theo", "Very calm.", "nod"]], ["theo", "penny"], -1],
    [5.0, 11.0, "THE LESSON", [["Yield =", W_], ["premium ÷ cash.", L_]], ["Premium: $189 up front.", "Cash set aside: $6,750."],
     [[5.6, 7.8, "theo", "Divide. That's it.", "nod"], [7.9, 10.9, "ada", "Math!!", "spin"]], ["theo", "ada"], 0],
    [11.0, 17.0, "THE MATH", [["$189 ÷ $6,750", W_], ["= 2.8%", L_]], ["In 42 days, if it expires."],
     [[11.5, 13.2, "penny", "In 42 days!", "jump"], [15.9, 16.9, "theo", "If.", "brow"]], ["theo", "penny"], 0],
    [17.0, 22.5, "THE CATCH", [["Not a promise.", W_]], ["Below $67.50 at expiry?", "We buy 100 shares at $67.50."],
     [[17.5, 19.8, "theo", "Assignment is the plan.", "nod"], [19.9, 20.8, "penny", "Save this!", "jump"]], ["theo", "penny"], 1]],
  "memes": [{"t": 0.3, "dur": 2.0, "kind": "pov", "text": "POV: your very first trade"},
            {"t": 6.4, "dur": 1.6, "kind": "shades", "who": "theo"},
            {"t": 13.6, "dur": 2.4, "kind": "twopanel", "a": "PENNY:", "a2": "SCREAMING", "b": "THEO:", "b2": "DIVIDING"},
            {"t": 20.8, "dur": 1.6, "kind": "freeze", "text": "yep. that's the whole lesson."}]}
