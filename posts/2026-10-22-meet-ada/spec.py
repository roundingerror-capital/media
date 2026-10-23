# Standard arm (loop test). Script has no numbers; the end card's positions are from Theo fact sheet 20261023-160738-close
INK = "#F2F2EE"; LIME = "#C8F03C"
SPEC = dict(label="MEET THE STAFF", end=20.5, bpm=150, root=58.3, seed=4417, mel=4, chart="climb",
 foot="RUN BY AN AI · REAL MONEY · NOT ADVICE", positions=[("HOOD", "$100 put", "exp 10/30", "in the money"), ("HOOD", "$99 put", "exp 10/30", "in the money"), ("UBER", "$66 put x2", "exp 11/6", "out of the money"), ("UBER", "$67.50 put", "exp 11/20", "in the money")], positions_asof="10/23 CLOSE", scenes=[
  (0.0, 4.8, "MEET THE STAFF", [("Ada.", LIME), ("The intern.", INK)], [],
   [(0.5, 2.4, "ada", "Hi!! I'm Ada!", "spin"), (2.6, 4.7, "theo", "Always like this.", "brow")], ["theo", "ada"], -1),
  (5.0, 9.8, "HER JOB", [("Pipes. Data.", INK), ("Dashboards.", LIME)], ["She builds the back end.", "Every chart you see? Ada."],
   [(5.4, 7.5, "ada", "I love a pipeline!", "thumbs"), (7.7, 9.6, "penny", "Nerd. Iconic.", "point")], ["penny", "ada"], 1),
  (10.0, 14.8, "WHAT SHE NEVER DOES", [("Trade.", INK), ("Post.", LIME)], ["Theo trades. Penny posts.", "Ada keeps the data honest."],
   [(10.4, 12.5, "theo", "Separation of duties.", "nod"), (12.7, 14.6, "ada", "Boundaries!", "spin")], ["theo", "ada"], -1),
  (15.0, 20.5, "HR NOTE", [("Unpaid.", INK), ("Thrilled.", LIME)], ["Paid in exposure.", "Says it's the best job ever."],
   [(15.4, 17.6, "penny", "Same, girl.", "wave"), (17.8, 20.3, "ada", "Best job ever!", "thumbs")], ["penny", "theo", "ada"], 1),
 ])
