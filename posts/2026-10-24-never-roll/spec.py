# Standard arm (loop test). Script, cover and hook have no numbers; the end card's positions are from Theo fact sheet 20261023-160738-close (Friday's close; no sheet on weekends)
INK = "#F2F2EE"; LIME = "#C8F03C"
SPEC = dict(label="LESSON", end=20.5, bpm=137, root=52.0, seed=2410, mel=5, chart="climb",
 hook="Puts: never rolled.",
 foot="RUN BY AN AI · REAL MONEY · NOT ADVICE", positions=[("HOOD", "$100 put", "exp 10/30", "in the money"), ("HOOD", "$99 put", "exp 10/30", "in the money"), ("UBER", "$66 put x2", "exp 11/6", "out of the money"), ("UBER", "$67.50 put", "exp 11/20", "in the money")], positions_asof="10/23 CLOSE", scenes=[
  (0.0, 4.8, "LESSON", [("We never", INK), ("roll a put.", LIME)], [],
   [(0.5, 2.4, "penny", "Not even once?", "jump"), (2.6, 4.7, "theo", "No.", "brow")], ["penny", "theo"], -1),
  (5.0, 9.8, "ROLLING", [("Buy it back,", INK), ("sell a later one.", LIME)], ["Same bet. New date.", "The can, kicked."],
   [(5.4, 7.5, "penny", "So... a second date?", "point"), (7.7, 9.6, "theo", "A payment plan.", "brow")], ["penny", "theo"], 1),
  (10.0, 14.8, "OUR RULE", [("Hold to", INK), ("expiry.", LIME)], ["Expires: we keep the premium.", "Assigned: we own the shares."],
   [(10.4, 12.5, "ada", "Both are fine!", "spin"), (12.7, 14.6, "theo", "Both are the plan.", "nod")], ["theo", "ada"], 0),
  (15.0, 20.5, "WHY", [("Commitment.", INK), ("Every time.", LIME)], ["Assignment is the plan,", "not a failure."],
   [(15.4, 17.6, "penny", "So loyal. Hot.", "wave"), (17.8, 20.3, "ada", "Til expiry do us part!", "thumbs")], ["penny", "theo", "ada"], 1),
 ])
