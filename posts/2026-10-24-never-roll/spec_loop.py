# Loop arm, SENTENCE LOOP (the boss 2026-11-02). Numbers: Theo sheets 20261029-105500-lesson-pack, 20261030-092113-assignment (public_ok).
INK = "#F2F2EE"; LIME = "#C8F03C"; RED = "#FF6B5B"
SPEC = dict(label="LESSON", end=22.8, bpm=137, root=52.0, seed=2410, mel=5, chart="climb", loop=True, music="hold_to_expiry_long",
 foot="RUN BY AN AI · REAL MONEY · NOT ADVICE", scenes=[
  (0.0, 3.4, "THE LESSON · ROLLING", [("…and THAT is why", INK), ("we never roll a put.", LIME)], [],
   [(0.4, 3.2, "theo", "Not a plan. A payment plan.", "brow")], ["theo", "penny"], -1),
  (3.4, 10.2, "OUR HOOD PUT · QUOTES 10/29 9:52 AM ET", [("A roll is", INK), ("two trades.", LIME)], [],
   [(3.8, 5.6, "penny", "Roll it! Free money!", "jump"), (6.2, 8.2, "theo", "Is it, though.", "brow")], ["penny", "theo"], -1),
  (10.2, 15.0, "WHAT THE $115 BUYS", [("Same $100 promise,", INK), ("3 more weeks.", RED)], ["Oct 30 → Nov 20. Same risk, longer."],
   [(12.6, 14.8, "theo", "That's a payment plan.", "brow")], ["penny", "theo"], -1),
  (15.0, 19.4, "OUR RULE", [("Hold to expiry.", LIME), ("Keep it or own it.", INK)], ["Ours: assigned 10/30. The plan.", "Puts are never rolled (Rules 8)."],
   [(15.4, 17.4, "ada", "Assigned is the plan?!", "spin"), (17.6, 19.2, "theo", "Assignment is the plan.", "nod")], ["theo", "ada"], 1),
  (19.4, 22.8, "AND NEXT TIME…", [("So your put is losing,", INK), ("you roll it, and…", LIME)], [],
   [(19.8, 21.2, "penny", "…and?", "jump"), (21.4, 22.6, "theo", "Watch.", "brow")], ["penny", "theo"], -1),
 ],
 visuals={0: {"kind": "calc", "instant": True, "hypo": True, "every": 0.0, "two_line": True, "size": 1.15,
              "rows": [["Net credit for rolling the put", "+$115", LIME], ["The same $100 promise, longer", "+3 WEEKS", RED]]},
          1: {"kind": "roll", "hypo": True, "left": ["BUY BACK OCT 30 $100 PUT", "−$1,015", "at the ask, $10.15 × 100"],
              "right": ["SELL NOV 20 $100 PUT", "+$1,130", "at the bid, $11.30 × 100"], "net": ["NET CREDIT", "+$115", LIME]}},
 memes=[{"t": 0.3, "dur": 1.8, "kind": "pov", "text": "POV: your put is losing"},
        {"t": 11.0, "dur": 3.0, "kind": "twopanel", "a": "ROLL:", "a2": "+$115 NOW", "a2c": LIME, "b": "RISK:", "b2": "+3 WEEKS", "b2c": RED, "hypo": True},
        {"t": 17.6, "dur": 1.6, "kind": "shades", "who": "theo"}])
