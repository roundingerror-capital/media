"""Daily positions end card (the boss 2026-10-27): one 3.5 s clip per day, built from the newest Theo close sheet,
checked once (Theo numbers, Roz every frame), then laid over the last 3.5 s of any evergreen at publish time
(tools/stitch.py), so a video scheduled days ago still ends with that day's positions.

Usage: python3 tools/endcard.py card.json out.mp4
card.json = {"positions": [["HOOD", "$100 put", "exp 10/30", "in the money"], ...], "positions_asof": "10/27 CLOSE",
             "sheet": "<Theo facts doc id>"}
Silent video, 1080x1920, 30 fps, same encoder settings as tools/daily.py."""
import json, subprocess, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import daily

def build(card, out):
    S = {"positions": card["positions"][:5], "positions_asof": card.get("positions_asof", ""), "chars": {}, "end": 0, "bpm": card.get("bpm", 140)}
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{daily.W}x{daily.H}",
        "-r", str(daily.FPS), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "20", "-movflags", "+faststart", out],
        stdin=subprocess.PIPE)
    for i in range(int(daily.OUTRO_S * daily.FPS)):
        p.stdin.write(daily.nfa(daily.outro_frame(S, i / daily.FPS)).tobytes())
    p.stdin.close(); p.wait(); return out

if __name__ == "__main__":
    print(build(json.load(open(sys.argv[1])), sys.argv[2]))
