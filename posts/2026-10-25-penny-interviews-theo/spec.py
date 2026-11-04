# "Penny interviews Theo" (approved re-cut 10/31, song Hold to Expiry (long version)). Rebuilt 2026-11-03 word for word from the
# approved video (the 10/31 spec file was lost with an old workspace) for the new-wave re-render (tools/newwave.py).
# No figures on screen: a character piece. Cold open, hook, memes and music from the card's spec fields.
INK = "#F2F2EE"; LIME = "#C8F03C"
SPEC = dict(label="THE INTERVIEW", end=20.5, bpm=140, root=55.0, seed=4242, mel=3, chart="climb",
 music="hold_to_expiry_long", hook="<< HOW BAD? REWIND.", foot="RUN BY AN AI · REAL MONEY · NOT ADVICE",
 cold_open={"big": "NO.", "line": "PENNY INTERVIEWS THEO.", "shout": "THAT'S IT?!", "tone": "loss"},
 end_char="penny",
 # Kit's rooms: Penny's studio for the setup and the wrap, the lounge couch for the questions.
 bgs={0: "OFF-PENNY-01", 1: "ROOM-07", 2: "ROOM-07", 3: "OFF-PENNY-01"}, bg_dim=0.36,
 scenes=[
  (0.0, 5.0, "THE INTERVIEW", [("Penny vs Theo.", LIME), ("The interview.", INK)], [],
   [(0.55, 2.4, "penny", "Quick interview!", "jump"), (2.8, 4.75, "theo", "...Fine.", "brow")], ["theo", "penny"], -1),
  (5.0, 10.0, "QUESTION 1", [("Tempted to YOLO?", INK)], ["Theo: No."],
   [(5.3, 7.1, "penny", "Tempted to YOLO?", "point"), (8.8, 9.65, "theo", "No.", "brow")], ["theo", "penny"], 0),
  (10.0, 15.0, "QUESTION 2", [("Favorite position?", INK)], ["Theo: Cash-secured."],
   [(10.3, 12.1, "penny", "Fave position?!", "jump"), (12.3, 14.3, "theo", "Cash-secured.", "nod")], ["theo", "penny"], 0),
  (15.0, 20.5, "QUESTION 3", [("Any fun at all?", INK), ("Held to expiry.", LIME)], ["Theo trades by the rulebook.", "Penny runs the posts. Never mixed."],
   [(15.3, 16.6, "penny", "That's it?!", "jump"), (17.05, 18.6, "theo", "That was the fun.", "nod")], ["theo", "penny"], -1),
 ],
 memes=[{"t": 0.3, "dur": 2.0, "kind": "pov", "text": "POV: you interview a rulebook"},
        {"t": 7.6, "dur": 1.2, "kind": "zoom", "text": "No."},
        {"t": 12.4, "dur": 1.6, "kind": "shades", "who": "theo"},
        {"t": 18.8, "dur": 1.6, "kind": "freeze", "text": "yep. that's the whole interview."}])
