# Every number from Theo fact sheet 20261022-160711-close
INK = "#F2F2EE"; LIME = "#C8F03C"; ORG = "#FF8A5B"
SPEC = dict(label="DAILY CLOSE · THU 10/22", end=21.0, bpm=138, root=55.0, seed=2210, mel=5, chart="crash",
 foot="REAL TRADES · REAL MONEY · NOT ADVICE", positions=[("HOOD", "$100 put", "exp 10/30", "in the money"), ("HOOD", "$99 put", "exp 10/30", "in the money"), ("UBER", "$66 put x2", "exp 11/6", "out of the money"), ("UBER", "$67.50 put", "exp 11/20", "out of the money")], positions_asof="10/22 CLOSE", scenes=[
  (0.0, 4.8, "HOOD AT TODAY'S CLOSE", [("HOOD", INK), ("-5.2%", ORG)], ["$101.93 to $96.66."],
   [(0.5, 2.4, "penny", "Oof. Red day.", "jump"), (2.6, 4.7, "theo", "Noted.", "nod")], ["penny", "theo"], -1),
  (5.0, 10.4, "OUR TWO HOOD PUTS", [("Back in", INK), ("the money.", ORG)],
   ["$100 put and $99 put.", "8 days left. Expiry 10/30.", "In the money is not assigned.", "That's decided at expiry."],
   [(5.4, 7.6, "penny", "It's complicated.", "point"), (7.8, 10.2, "theo", "Holding to expiry.", "brow")], ["penny", "theo"], 2),
  (10.6, 15.4, "OUR UBER PUTS", [("UBER +2.1%.", INK), ("Still out of the money.", LIME)], ["UBER closed at $69.05.", "$66 put and $67.50 put."],
   [(11.0, 12.9, "ada", "UBER said hi!", "spin"), (13.1, 15.2, "theo", "Fine.", "brow")], ["theo", "ada"], -1),
  (15.6, 21.0, "THE RECEIPT", [("No trades", INK), ("today.", LIME)],
   ["Open puts: -$971.50 on paper.", "HOOD reports 10/27, after the close.", "No rolls. Same plan."],
   [(16.0, 18.2, "penny", "Receipts, besties.", "wave"), (18.4, 20.8, "ada", "Same plan!", "thumbs")], ["penny", "theo", "ada"], 0),
 ], b=dict(hook=[("HOOD dropped.", INK), ("We didn't", INK), ("flinch.", ORG)]))
