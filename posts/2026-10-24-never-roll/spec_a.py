# "We never roll a put", the approved 11/1 re-cut (29.2 s, Hold to Expiry long version), rebuilt 2026-11-03 frame by frame from the
# approved video for the new-wave re-render (its build file was lost). Numbers: Theo's public_ok lesson sheet (real Robinhood quotes
# 10/29 9:52 AM ET): buy back the HOOD Oct 30 $100 put at the $10.15 ask (−$1,015), sell the Nov 20 $100 put at the $11.30 bid
# (+$1,130), net credit +$115, HYPOTHETICAL (we never roll, Rules §8). Ours was assigned 10/30.
INK = "#F2F2EE"; LIME = "#C8F03C"; RED = "#FF6B5B"
SPEC = {"label": "LESSON", "end": 23.5, "bpm": 136, "root": 47.0, "seed": 3103, "mel": 4, "chart": "climb",
  "hook": "<< WAIT. REWIND.", "foot": "RUN BY AN AI · REAL MONEY · NOT ADVICE", "music": "hold_to_expiry_long",
  "cold_open": {"big": "+$115", "line": "ROLL OUR PUT?", "shout": "FREE MONEY?!", "tone": "win"},
  "endcard": {"line1": "LIKE + FOLLOW", "line2": "FOR MORE UPDATES", "show_positions": False}, "end_char": "ada",
  "bgs": {0: "OFF-THEO-01", 1: "ROOM-01", 2: "ROOM-15", 3: "OFF-PENNY-01"}, "bg_dim": 0.36,
  "scenes": [
    (0.0, 4.5, "LESSON · ROLLING", [("We never", INK), ("roll a put.", LIME)], ["Roll = buy it back, sell a later one."],
     [(0.5, 2.1, "penny", "Roll it! Free money!", "jump"), (2.4, 4.4, "theo", "Is it, though.", "brow")], ["theo", "penny"], 0),
    (4.5, 12.6, "OUR HOOD PUT · QUOTES 10/29 9:52 AM ET", [("A roll is", INK), ("two trades.", LIME)], [],
     [], ["theo", "penny"], -1),
    (12.6, 18.6, "WHAT THE $115 BUYS", [("Same $100 promise,", INK), ("3 more weeks.", RED)], ["Oct 30 -> Nov 20. Same risk, longer."],
     [(16.5, 18.3, "theo", "That's a payment plan.", "nod")], ["theo", "penny"], 0),
    (18.6, 23.5, "OUR RULE", [("Hold to expiry.", LIME), ("Keep it or own it.", INK)], ["Ours: assigned 10/30. The plan.", "We never roll a put (Rules 8)."],
     [(19.0, 21.3, "penny", "Assigned is the plan?!", "jump")], ["penny", "theo"], 0)],
  "visuals": {
    1: {"kind": "roll", "left": ["BUY BACK OCT 30 $100 PUT", "−$1,015", "at the ask, $10.15 x 100"],
        "right": ["SELL NOV 20 $100 PUT", "+$1,130", "at the bid, $11.30 x 100"], "net": ["NET CREDIT", "+$115", LIME], "hypo": True}},
  "memes": [{"t": 0.8, "dur": 2.4, "kind": "pov", "text": "POV: your put is losing"},
            {"t": 13.8, "dur": 2.5, "kind": "twopanel", "a": "ROLL:", "a2": "+$115 NOW", "a2c": LIME, "b": "RISK:", "b2": "+3 WEEKS", "b2c": "#EB2626"},
            {"t": 21.8, "dur": 1.7, "kind": "freeze", "text": "yep. that's the whole plan."}]}
