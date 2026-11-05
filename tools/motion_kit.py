"""Motion kit: every brand asset exported as plain image files, ready to attach to an animation tool (Claude Motion first).
Nothing here is new art: it re-exports Kit's sprites, rooms and props exactly as our videos use them.
    python3 motion_kit.py <out_dir>
Never includes the boss's characters or office (privacy), any number, or any fund data."""
import os, sys, json, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from PIL import Image
import rigs, newwave, assets

CAST = ["theo", "penny", "ada", "kit", "roz"]          # never boss / realboss / realboss_hood
SCALE = 8                                              # nearest-neighbour; pixel art stays crisp
PALETTE = {"ink": "#0B0B0B", "paper": "#F7F1D8", "lime": "#C8F03C", "red": "#FF5C5C", "green": "#3CCB7F",
           "blue": "#7BAAF7", "gold": "#F5C542", "night": "#0E1018"}

def up(im, k): return im.resize((im.width * k, im.height * k), Image.NEAREST)

def cast(out):
    idx = {}
    for ch in CAST:
        names = rigs.anims(ch) + rigs.desk_anims(ch); idx[ch] = {}
        for an in names:
            frames, ticks = rigs.load(ch, an)[:2]
            d = os.path.join(out, "cast", ch, an); os.makedirs(d, exist_ok=True)
            w = max(f.width for f in frames); h = max(f.height for f in frames)
            strip = Image.new("RGBA", (w * len(frames), h))
            for i, f in enumerate(frames):
                strip.paste(f, (i * w + (w - f.width) // 2, h - f.height), f)
                up(f, SCALE).save(os.path.join(d, f"{ch}_{an}_{i:02d}.png"))
            up(strip, SCALE).save(os.path.join(out, "cast", ch, f"{ch}_{an}_strip.png"))
            big = [up(f, SCALE) for f in frames]
            big[0].save(os.path.join(out, "cast", ch, f"{ch}_{an}_preview.gif"), save_all=True, append_images=big[1:],
                        duration=list(ticks), loop=0, disposal=2, transparency=0)
            idx[ch][an] = {"frames": len(frames), "frame_ms": list(ticks), "frame_px_native": [w, h], "scale": SCALE}
    json.dump(idx, open(os.path.join(out, "cast", "timing.json"), "w"), indent=1)
    return idx

def _room(d, name):
    st = newwave._stage(name); big = newwave.room_big(name, 0.0); K = newwave.K
    px, py, pw, ph = st.frames.get("portrait", (0, 0, 72, 128))
    big.save(os.path.join(d, f"{name}_wide.png"))                                   # whole stage, for pans
    big.crop((px * K, py * K, px * K + 1080, py * K + 1920)).save(os.path.join(d, f"{name}_1080x1920.png"))   # full brightness, no text shade

def rooms(out):
    d = os.path.join(out, "rooms"); os.makedirs(d, exist_ok=True); done = []
    names = [f"ROOM-{i:02d}" for i in range(1, 21)] + [f"OFF-{w}-01" for w in ("PENNY", "THEO", "ADA", "KIT", "ROZ")]   # never OFF-BOSS / OFF-REALBOSS
    for name in names:
        try: _room(d, name); done.append(name)
        except Exception: pass
    return done

def props(out):
    d = os.path.join(out, "props"); os.makedirs(d, exist_ok=True); done = []
    for aid, r in assets.REG.items():
        try:
            im = assets.get(aid, 0.0); k = 8 if r["kind"] == "prop" else 3
            up(im, k).save(os.path.join(d, f"{aid}.png")); done.append(aid)
        except Exception: pass
    return done

def brand(out):
    d = os.path.join(out, "brand"); os.makedirs(d, exist_ok=True)
    for f in os.listdir(os.path.join(HERE, "fonts")): shutil.copy(os.path.join(HERE, "fonts", f), d)
    sw = Image.new("RGB", (160 * len(PALETTE), 160))
    for i, c in enumerate(PALETTE.values()): sw.paste(Image.new("RGB", (160, 160), c), (i * 160, 0))
    sw.save(os.path.join(d, "palette.png")); json.dump(PALETTE, open(os.path.join(d, "palette.json"), "w"), indent=1)

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/out/motion_kit"
    shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
    c = cast(out); r = rooms(out); p = props(out); brand(out)
    print(json.dumps({"cast": {k: len(v) for k, v in c.items()}, "rooms": r, "props": len(p)}))
