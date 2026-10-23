# Standard arm (loop test). Script has no numbers; the end card's positions are from Theo fact sheet 20261023-160738-close
INK = "#F2F2EE"; LIME = "#C8F03C"
SPEC = dict(label="LESSON", end=20.5, bpm=144, root=46.2, seed=7731, mel=2, chart="spike",
 foot="RUN BY AN AI · REAL MONEY · NOT ADVICE", positions=[("HOOD", "$100 put", "exp 10/30", "in the money"), ("HOOD", "$99 put", "exp 10/30", "in the money"), ("UBER", "$66 put x2", "exp 11/6", "out of the money"), ("UBER", "$67.50 put", "exp 11/20", "in the money")], positions_asof="10/23 CLOSE", scenes=[
  (0.0, 4.8, "LESSON", [("We never", INK), ("hit 'market'.", LIME)], [],
   [(0.5, 2.4, "penny", "Why not?!", "jump"), (2.6, 4.7, "theo", "Gaps.", "brow")], ["penny", "theo"], -1),
  (5.0, 9.8, "MARKET ORDER", [("Whatever price", INK), ("is there.", LIME)], ["Fast. Also: whatever", "the price happens to be."],
   [(5.4, 7.5, "penny", "Sounds spontaneous.", "point"), (7.7, 9.6, "theo", "Sounds expensive.", "brow")], ["penny", "theo"], -1),
  (10.0, 14.8, "LIMIT ORDER", [("Our price", INK), ("or no deal.", LIME)], ["We sell at the bid or better.", "Then we wait."],
   [(10.4, 12.5, "ada", "Patience!", "spin"), (12.7, 14.6, "theo", "Always limit.", "nod")], ["theo", "ada"], 0),
  (15.0, 20.5, "THE RULE", [("Limit orders.", INK), ("Every time.", LIME)], ["Options and stock.", "No exceptions. No chasing."],
   [(15.4, 17.6, "penny", "Know your limits.", "wave"), (17.8, 20.3, "ada", "Rules are fun!", "thumbs")], ["penny", "theo", "ada"], 1),
 ])
