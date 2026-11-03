"""Cut a long generated song down to a short edit on bar lines (the boss 2026-11-03: generators won't make 32 s, so we cut).

The edit keeps the song's own beginning (pickup + intro + head_bars bars) and its own ending (from tail_bar to the end of
the sound), joined by a short crossfade exactly on a downbeat, so it plays as one song with a real start and a real ending.

    python3 tools/song_cut.py <song.mp3> <out.wav> --head 12 --tail 25 [--hold 0.8]
    -> out.wav + out.json {"bpm", "beat", "bar", "pickup", "head_end", "tail_start", "join", "total"}  (seconds, edit time)

Grid: tempo and beat phase from librosa's beat tracker, refined by a straight-line fit over every detected beat; the downbeat
is the beat phase with the strongest onsets every 4 beats. Renders and generated audio stay out of git."""
import sys, json, argparse, subprocess
import numpy as np, librosa

def grid(path):
    y, sr = librosa.load(path, sr=22050, mono=True)
    _, beats = librosa.beat.beat_track(y=y, sr=sr, units="time")
    k = np.arange(len(beats)); beat, phase = np.polyfit(k, beats, 1)          # beats ~= phase + k * beat
    on = librosa.onset.onset_strength(y=y, sr=sr); ot = librosa.times_like(on, sr=sr)
    strength = [np.mean([on[np.argmin(abs(ot - b))] for b in beats[p::4]]) for p in range(4)]
    down = phase + int(np.argmax(strength)) * beat                            # first downbeat
    tr = librosa.effects.trim(y, top_db=45)[1]
    return dict(beat=float(beat), bar=float(4 * beat), bpm=float(60 / beat), pickup=float(down), end=float(tr[1] / sr), dur=len(y) / sr)

def cut(src, out, head, tail, hold=0.8, xf=0.06):
    g = grid(src)
    head_end = g["pickup"] + head * g["bar"]; tail_start = g["pickup"] + tail * g["bar"]
    stop = min(g["dur"], g["end"] + hold)
    fl = f"[0:a]atrim=0:{head_end + xf / 2:.4f},asetpts=PTS-STARTPTS[a];[0:a]atrim={tail_start - xf / 2:.4f}:{stop:.4f},asetpts=PTS-STARTPTS," \
         f"afade=t=out:st={stop - tail_start - 0.5:.3f}:d=0.5[b];[a][b]acrossfade=d={xf}:c1=tri:c2=tri[o]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-filter_complex", fl, "-map", "[o]", "-ar", "44100", out], check=True)
    total = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out]))
    meta = dict(bpm=g["bpm"], beat=g["beat"], bar=g["bar"], pickup=g["pickup"], head_end=head_end, tail_start=tail_start,
                join=head_end, total=total, source=src.split("/")[-1], head_bars=head, tail_bar=tail)
    json.dump(meta, open(out[:-4] + ".json", "w"), indent=1); return meta

if __name__ == "__main__":
    a = argparse.ArgumentParser(); a.add_argument("src"); a.add_argument("out"); a.add_argument("--head", type=int, default=12)
    a.add_argument("--tail", type=int, required=True); a.add_argument("--hold", type=float, default=0.8)
    v = a.parse_args(); print(json.dumps(cut(v.src, v.out, v.head, v.tail, v.hold), indent=1))
