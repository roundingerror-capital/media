"""MEET ROZ, our Counsel (meet the staff, approved). Rebuilt 2026-11-03 for the new wave from the approved video, word for word
(the original spec file was lost). No fund figures."""
W_, L_ = "#F2F2EE", "#C8F03C"
SPEC = {"label": "MEET THE STAFF", "end": 22.0, "bpm": 128, "root": 47.0, "seed": 1102, "mel": 3, "chart": "climb",
  "hook": "<< WHO WROTE THAT? REWIND.", "music": "robots_got_manners",
  "bgs": {0: "OFF-ROZ-01", 1: "OFF-ROZ-01", 2: "OFF-ROZ-01", 3: "OFF-ROZ-01"}, "bg_dim": 0.36,
  "cold_open": {"big": "NFA.", "line": "MEET OUR COUNSEL.", "shout": "A TURTLE?!", "tone": "win"},
  "intro_cfg": {"tagline": "And this is what's going on ↓"},
  "endcard": {"line1": "LIKE + FOLLOW", "line2": "FOR MORE UPDATES", "show_positions": False}, "end_char": "theo",
  "scenes": [
    [0.0, 5.8, "MEET THE STAFF", [["Meet Roz.", W_], ["Counsel.", L_]], ["An AI. A turtle.", "Not a licensed lawyer."],
     [[0.6, 2.4, "roz", "Shell first.", "nod"], [4.9, 5.7, "penny", "So serious!", "jump"]], ["penny", "roz"], -1],
    [5.8, 11.4, "HER FAVORITE THING", [["The fine", W_], ["print.", L_]], ["Footnotes? Loves them.", "Disclaimers? Collects them.", "Hype words? Hates them."],
     [[6.0, 8.2, "roz", "Read the fine print.", "point"], [8.5, 10.8, "theo", "Finally. A friend.", "jump"]], ["theo", "roz"], 2],
    [11.4, 16.9, "HER ONE RULE", [["Not financial", W_], ["advice.", L_]], ["We show what we did.", "Never what you should do.", "Your money, your call."],
     [[11.6, 12.9, "penny", "Not even a little?", "spin"], [15.8, 16.8, "roz", "Not even a little.", "nod"]], ["penny", "roz"], 1],
    [16.9, 22.0, "THAT'S ROZ", [["Slow on", W_], ["purpose.", L_]], ["Careful is cool."],
     [[17.5, 19.2, "ada", "She's the best!", "spin"], [20.4, 21.9, "roz", "I'll allow it.", "nod"]], ["penny", "roz", "ada"], -1]],
  "memes": [{"t": 3.0, "dur": 1.8, "kind": "pov", "text": "POV: the fine print has a fan"},
            {"t": 13.4, "dur": 1.6, "kind": "shades", "who": "roz"},
            {"t": 19.4, "dur": 1.4, "kind": "freeze", "text": "yep. that's her whole personality."}]}
