"""HOOD rewind: put vs shares (evergreen, hindsight). Rebuilt 2026-11-03 for the new wave (tools/newwave.py) from the approved video
(Roz-cleared 10/30 cut): same script, same words, same numbers, same timing. Only the art changes (Kit's rigs + V3.01 rooms).
Numbers as on the approved card (Theo's rewind block): $100 strike, $270 premium, $109.22 (Oct 12), $91.59 (Oct 29 close), -16.1%,
assigned at $100 Oct 30, worked example $270 + ($91.59 - $100) x 100 = -$571 vs -$1,763 for 100 shares bought Oct 12."""
W_, L_, RED = "#F2F2EE", "#C8F03C", "#EB2626"
SPEC = {"label": "THE REWIND", "end": 21.5, "bpm": 138, "root": 45.0, "seed": 1030, "mel": 2, "chart": "crash",
  "hook": "<< PUT VS SHARES. REWIND.", "music": "only_on_paper",
  "bgs": {0: "OFF-THEO-01", 1: "ROOM-01", 2: "ROOM-15", 3: "ROOM-16"}, "bg": "ROOM-01", "bg_dim": 0.36,
  "cold_open": {"big": "−$571", "line": "OUR HOOD PUT, ON PAPER.", "shout": "NOT −$1,763?!", "tone": "loss"},
  "intro_cfg": {"tagline": "And this is what's going on ↓"},
  "endcard": {"line1": "LIKE + FOLLOW", "line2": "FOR MORE UPDATES", "show_positions": False},
  "end_char": "penny",
  "scenes": [
    [0.0, 5.0, "HINDSIGHT, NOT A STRATEGY", [["Oct 12: we sold", W_], ["a $100 HOOD put.", L_]], ["HOOD was $109.22.", "We collected $270."],
     [[3.3, 4.9, "theo", "Rent. Not free.", "nod"]], ["penny", "theo"], 1],
    [5.0, 10.8, "THE DROP", [["HOOD fell", W_], ["16.1%.", RED]], ["Oct 29 close: $91.59.", "Assigned at $100 on Oct 30."],
     [[8.8, 10.3, "penny", "Ouch.", "jump"]], ["penny", "ada"], 0],
    [10.8, 16.2, "HINDSIGHT, NOT A STRATEGY", [["Sell the put vs.", W_], ["buy the shares.", L_]], ["Buy 100 shares Oct 12: −$1,763", "Sell the put: −$571"],
     [[12.8, 13.7, "theo", "Premium = cushion.", "nod"], [14.3, 15.7, "penny", "Not a force field.", "jump"]], ["penny", "theo"], 1],
    [16.2, 21.5, "THE MATH, ON PAPER", [["The cushion:", W_], ["$270.", L_]], ["$270 + ($91.59 − $100) × 100", "= −$571 at the Oct 29 close."],
     [[16.8, 18.9, "ada", "Hindsight, not a strategy!", "jump"]], ["theo", "ada"], 1]],
  "memes": [{"t": 1.0, "dur": 2.2, "kind": "pov", "text": "POV: hindsight shows up"},
            {"t": 6.2, "dur": 2.6, "y": 70, "kind": "twopanel", "a": "HOOD:", "a2": "FALLING", "b": "THEO:", "b2": "UNBOTHERED"},
            {"t": 11.0, "dur": 1.6, "kind": "shades", "who": "theo"},
            {"t": 19.6, "dur": 1.6, "kind": "freeze", "text": "a cushion. not a force field."}]}
