"""Our songs, kept private (the boss 2026-11-02, Ops T-088, board 20261102-223754-ada-sng1).

The raw tracks and lyrics are NOT in this repo. Each song is a private asset on Database · Posts (songs/<key>.audio:
asset_id + sha256 of an audio-only mp4 holding the original mp3 stream). A render fetches the track, checks it, and extracts
the mp3 into tools/music/ (gitignored; a local cache that never leaves the machine). Timing and titles come from the same
songs rows, cached in tools/music/songs.json (also gitignored).

Step 1 · rows (ArtifactData list, collection "songs", on https://claude.ai/artifact/7SvAvbd7CFfvgnWoQoKy4j, with out_dir):
    python3 tools/songs.py meta <out_dir>/songs                  -> tools/music/songs.json
Step 2 · what is missing:
    python3 tools/songs.py need <key> [<key> ...]                -> prints "<key> <asset_id>" for each track not cached
Step 3 · for each line: Artifact read, url as above, path = <asset_id>, then
    python3 tools/songs.py install <key> <downloaded .mp4>       -> checks sha256, extracts tools/music/<key>.mp3
Renderers call songs.path(key) and songs.meta(key); both raise with these steps if the cache is missing.
"""
import os, sys, json, hashlib, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); DIR = os.path.join(HERE, "music"); META = os.path.join(DIR, "songs.json")
STEPS = "fetch it first: python3 tools/songs.py meta|need|install (see tools/songs.py)"

def _sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()

def _rows():
    if not os.path.exists(META): raise FileNotFoundError(f"no song metadata ({META}); {STEPS}")
    return json.load(open(META))

def meta(key):
    r = _rows()
    if key not in r: raise KeyError(f"song {key!r} not in songs.json; {STEPS}")
    return r[key]

def path(key):
    p = os.path.join(DIR, key + ".mp3"); meta(key)
    if not os.path.exists(p): raise FileNotFoundError(f"track {key} not cached; {STEPS}")
    return p   # install() is the integrity check (sha256 of the private copy); the cache is only ever written by it

def write_meta(rows_dir):
    out = {}
    for f in sorted(os.listdir(rows_dir)):
        if not f.endswith(".json"): continue
        d = json.load(open(os.path.join(rows_dir, f))); d = d.get("data", d)
        if not isinstance(d, dict) or not d.get("audio"): continue
        out[f[:-5]] = {"title": d.get("title"), "start_s": d.get("start_s"), "dur_s": d.get("dur_s"), "status": d.get("status"),
                       "audio": {k: d["audio"].get(k) for k in ("asset_id", "sha256", "source_mp3_sha256")}}
    os.makedirs(DIR, exist_ok=True); json.dump(out, open(META, "w"), indent=1); print(len(out), "songs ->", META)

def need(keys):
    for k in keys:
        m = meta(k)
        if not os.path.exists(os.path.join(DIR, k + ".mp3")): print(k, m["audio"]["asset_id"])

def install(key, mp4):
    m = meta(key); got = _sha(mp4)
    if got != m["audio"]["sha256"]: raise SystemExit(f"{key}: downloaded file sha256 {got[:12]} != {m['audio']['sha256'][:12]}; not installed")
    out = os.path.join(DIR, key + ".mp3")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp4, "-map", "0:a", "-c:a", "copy", out], check=True)
    # Checked 2026-11-02 on hold_to_expiry_long: the extracted stream decodes to the original's samples exactly, minus 529
    # samples (12 ms) of encoder delay at the start (the LAME gapless header does not survive the mp4 wrap). Inaudible in a video.
    print(key, "->", out)

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "meta": write_meta(sys.argv[2])
    elif cmd == "need": need(sys.argv[2:])
    elif cmd == "install": install(sys.argv[2], sys.argv[3])
