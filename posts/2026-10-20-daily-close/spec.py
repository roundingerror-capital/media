# Every number from Theo fact sheet 20261020-160727-close
INK = "#F2F2EE"; LIME = "#C8F03C"
SPEC = dict(label="DAILY CLOSE · TUE 10/20", end=20.5, bpm=138, root=55.0, seed=2010, mel=2, chart="spike",
 foot="REAL TRADES · REAL MONEY · NOT ADVICE", scenes=[
  (0.0, 4.8, "HOOD AT TODAY'S CLOSE", [("HOOD", INK), ("+1.8%", LIME)], ["$96.52 to $98.29."],
   [(0.5, 2.4, "penny", "Green day!", "jump"), (2.6, 4.7, "theo", "Still in the money.", "brow")], ["penny", "theo"], -1),
  (5.0, 10.4, "OUR TWO HOOD PUTS", [("Still in", INK), ("the money.", LIME)],
   ["$100 put and $99 put.", "10 days left. Expiry 10/30.", "In the money is not assigned.", "That's decided at expiry."],
   [(5.4, 7.6, "penny", "So close!", "point"), (7.8, 10.2, "theo", "Holding to expiry.", "nod")], ["penny", "theo"], 2),
  (10.6, 15.2, "OUR UBER PUTS", [("Still out of", INK), ("the money.", LIME)], ["$66 and $67.50 puts.", "UBER slipped 1.5%."],
   [(11.0, 12.9, "ada", "All green!", "spin"), (13.1, 15.0, "theo", "Mostly.", "brow")], ["theo", "ada"], -1),
  (15.4, 20.5, "THE RECEIPT", [("No trades", INK), ("today.", LIME)],
   ["Open puts: -$827.50 on paper.", "HOOD reports 10/27, after the close.", "No rolls. Same plan."],
   [(15.8, 18.0, "penny", "Receipts, besties.", "wave"), (18.2, 20.3, "theo", "Carry on.", "nod")], ["penny", "theo", "ada"], 0),
 ], b=dict(hook=[("Still in the", INK), ("money.", LIME), ("10 days left.", INK)]))
