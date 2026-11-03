"""Contact sheet of a spec rendered through daily.py (new wave check): cold open, scene frames, outro, cover.
Usage: python3 tools/nw_stills.py <spec.py> <out.png> [t,t,...]   (spec module defines SPEC)"""
import sys, os, runpy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import daily
from PIL import Image, ImageDraw
from make_reel import mono
spec_path, out = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.dirname(os.path.abspath(spec_path)))
S = runpy.run_path(spec_path)["SPEC"]
ts = [float(x) for x in sys.argv[3].split(",")] if len(sys.argv) > 3 else [0.8] + [sc[0] + (sc[1] - sc[0]) * 0.6 for sc in S["scenes"]]
ims = []
if S.get("cold_open"):
    pts = daily.chart_pts(S.get("chart", "climb"), S["seed"]); ims.append(("cold", daily.cold_open_frame(S, 20, Image.new("RGB", (daily.W, daily.H)), pts)))
for t in ts: ims.append((f"{t:.1f}s", daily.nfa(daily.scene_frame(S, t))))
try: ims.append(("end", daily.outro_frame(S, 1.5)))
except Exception as e: print("outro:", e)
w = 270; h = 480; sheet = Image.new("RGB", (w * len(ims), h + 30), "#111"); d = ImageDraw.Draw(sheet)
for i, (lab, im) in enumerate(ims):
    sheet.paste(im.convert("RGB").resize((w, h)), (i * w, 30)); d.text((i * w + 6, 6), lab, font=mono(18, True), fill="#C8F03C")
sheet.save(out); print(out)
