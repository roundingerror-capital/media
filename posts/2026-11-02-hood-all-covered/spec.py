"""HOOD: all 200 shares covered (event card, 11/2). Rebuilt 2026-11-03 for the new wave (tools/newwave.py) from the approved video:
same script, words, numbers and timing; only the art changes (Kit's rigs + V3.01 rooms).
Numbers as on the approved card (Theo fill + close sheets 11/2): covered call $100 strike, Dec 4, $2.01/sh = $201, 10:43 AM ET,
HOOD $87.21 at the fill, $100 basis, 2 calls $360 collected; end-card positions = 11/2 close."""
W_, L_ = "#F2F2EE", "#C8F03C"
SPEC = {"label": "THE WHEEL", "end": 22.6, "bpm": 132, "root": 45.0, "seed": 1102, "mel": 2, "chart": "climb",
  "hook": "<< 200 SHARES, ALL RENTED. REWIND.", "music": "the_clock_pays_rent",
  "bgs": {0: "OFF-THEO-01", 1: "ROOM-15", 2: "ROOM-10", 3: "ROOM-16"}, "bg": "ROOM-01", "bg_dim": 0.36,
  "cold_open": {"big": "$201", "line": "1 MORE HOOD CALL.", "shout": "RENT DAY?!", "tone": "win"},
  "intro_cfg": {"tagline": "And this is what's going on ↓"},
  "endcard": {"line1": "LIKE + FOLLOW", "line2": "FOR MORE UPDATES", "show_positions": True},
  "end_char": "theo",
  "positions": [("UBER", "$66 put x2", "exp 11/6", "out of the money"), ("HIMS", "$26 put x4", "exp 11/13", "in the money"),
                ("UBER", "$67.50 put", "exp 11/20", "in the money"), ("HOOD", "$100 call x2", "exp 12/4", "out of the money")],
  "positions_asof": "11/2 CLOSE",
  "scenes": [
    [0.0, 5.8, "HOOD · TODAY 10:43 AM ET", [["All 200 HOOD", W_], ["shares: rented.", L_]], ["Sold 1 more covered call.", "$100 strike · expires Dec 4.", "$2.01 a share = $201."],
     [[0.3, 1.9, "penny", "Landlord era!", "jump"], [5.3, 5.8, "theo", "Filed.", "nod"]], ["penny", "theo"], 2],
    [5.8, 11.8, "THE DEAL", [["Above $100", W_], ["on Dec 4?", L_]], ["We sell 100 shares at $100", "and keep the $201.", "HOOD at the fill: $87.21."],
     [[6.3, 8.4, "ada", "Rent collected!", "jump"], [8.8, 10.9, "theo", "Either way, paid.", "jump"]], ["theo", "ada"], 1],
    [11.8, 17.8, "BELOW $100 ON DEC 4?", [["We keep the", W_], ["shares + $201.", L_]], ["HOOD is under our $100 basis.", "That loss is on paper.", "Then we sell another call."],
     [[11.8, 12.9, "penny", "So... still paid?", "brow"], [16.3, 17.0, "theo", "Still paid.", "nod"]], ["penny", "theo"], 1],
    [17.8, 22.6, "THE RECEIPT", [["2 calls.", W_], ["$360 collected.", L_]], ["Both: $100 strike, Dec 4.", "Hold to expiry."],
     [[17.8, 19.4, "roz", "Not advice. Promise.", "jump"], [21.3, 22.6, "penny", "Receipts, besties.", "jump"]], ["penny", "roz"], -1]],
  "memes": [{"t": 2.8, "dur": 2.4, "kind": "pov", "text": "POV: your shares pay rent"},
            {"t": 13.8, "dur": 2.4, "kind": "twopanel", "a": "SHARES:", "a2": "UNDERWATER", "b": "CALL:", "b2": "PAYING RENT"},
            {"t": 19.8, "dur": 1.4, "kind": "shades", "who": "roz"}]}
