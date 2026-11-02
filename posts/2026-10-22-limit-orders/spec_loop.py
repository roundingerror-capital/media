# Loop arm, SENTENCE LOOP (the boss 2026-11-02): frame 1 is the conclusion, the story runs in full, the last line stops
# mid-sentence and the cross-fade back to frame 1 finishes it. Every number: Theo sheet 20261029-105500-lesson-pack (public_ok).
INK = "#F2F2EE"; LIME = "#C8F03C"; RED = "#FF6B5B"
SPEC = dict(label="LESSON", end=23.3, bpm=144, root=46.2, seed=7731, mel=2, chart="spike", loop=True, music="robots_got_manners",
 foot="RUN BY AN AI · REAL MONEY · NOT ADVICE", scenes=[
  (0.0, 3.4, "THE LESSON · LIMIT ORDERS", [("…and THAT is why", INK), ("we never hit 'market'.", LIME)], [],
   [(0.4, 3.2, "theo", "Every. Single. Time.", "nod")], ["theo", "penny"], -1),
  (3.4, 10.6, "REAL HOOD BOOK · 10/29 9:52 AM ET", [("Sell 1,000 shares", INK), ("at market?", RED)], [],
   [(3.8, 5.4, "penny", "Just smash SELL!", "jump"), (5.6, 7.4, "theo", "Let's look first.", "brow")], ["penny", "theo"], -1),
  (10.6, 15.4, "THE FIX", [("Limit order:", INK), ("name your price.", LIME)], ["Bid or better. Then we wait."],
   [(11.0, 12.8, "ada", "Patience!", "spin"), (13.0, 15.2, "theo", "Our price or no deal.", "nod")], ["theo", "ada"], 0),
  (15.4, 19.6, "TAKEAWAY", [("Thin book?", INK), ("Market eats the levels.", RED)], ["The top bid had 1 share."],
   [(15.8, 17.8, "penny", "Save this. Seriously.", "point")], ["theo", "penny"], -1),
  (19.6, 23.3, "AND NEXT TIME…", [("So you smash", INK), ("'market', and…", LIME)], [],
   [(20.0, 21.6, "penny", "…and?", "jump"), (21.8, 23.1, "theo", "Watch.", "brow")], ["penny", "theo"], -1),
 ],
 visuals={0: {"kind": "calc", "instant": True, "hypo": True, "every": 0.0, "two_line": True, "size": 1.15,
              "rows": [["One market order, 1,000 shares", "−$101", RED]]},
          1: {"kind": "book", "title": "HOOD ORDER BOOK · TOP 5 BIDS", "hypo": True, "reveal_at": 1.0, "fill_at": 2.0,
              "levels": [["$90.21", "1"], ["$90.20", "4"], ["$90.19", "5"], ["$90.17", "73"], ["$90.12", "150"]],
              "fills": [["$90.21", "1"], ["$90.20", "4"], ["$90.19", "5"], ["$90.17", "73"], ["$90.12", "150"]],
              "avg": "$90.11", "top": "$90.21", "diff": "−$101 vs the top bid"}},
 memes=[{"t": 0.3, "dur": 1.8, "kind": "pov", "text": "POV: you hit market at 9:52 AM"},
        {"t": 11.6, "dur": 3.0, "kind": "twopanel", "a": "MARKET:", "a2": "ANY PRICE", "b": "LIMIT:", "b2": "OUR PRICE"},
        {"t": 16.0, "dur": 1.6, "kind": "shades", "who": "theo"}])
