import sys, os
sys.path.insert(0, '/home/claude/media/tools'); HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import daily, covers2, spec
out = sys.argv[1]; os.makedirs(os.path.join(out, "wd"), exist_ok=True); cj = os.path.join(out, "cover.jpg")
covers2.make(cj, "panel", "$201", line="ALL 200 SHARES RENTED", who=("theo",), tone="lime")
daily.build(spec.SPEC, os.path.join(out, "a.mp4"), cj, "a", os.path.join(out, "wd")); print("ok", out)
