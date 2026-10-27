"""Lay today's end card (tools/endcard.py) over the last 3.5 s of an evergreen video (the boss 2026-10-27).
The evergreen keeps its own audio and its CTA-only end card underneath; only the picture of the last 3.5 s changes.
Usage: python3 tools/stitch.py body.mp4 endcard.mp4 out.mp4
Run tools/safety_scan.py on out.mp4 before it goes anywhere."""
import subprocess, sys, json

def duration(f):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", f], capture_output=True, text=True, check=True)
    return float(json.loads(r.stdout)["format"]["duration"])

def stitch(body, card, out):
    T = duration(body); C = duration(card); start = max(0.0, T - C)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", body, "-itsoffset", f"{start:.3f}", "-i", card,
        "-filter_complex", f"[0:v][1:v]overlay=0:0:enable='gte(t,{start:.3f})':eof_action=pass[v]",
        "-map", "[v]", "-map", "0:a?", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "20",
        "-c:a", "copy", "-movflags", "+faststart", out], check=True)
    return out

if __name__ == "__main__":
    print(stitch(sys.argv[1], sys.argv[2], sys.argv[3]))
