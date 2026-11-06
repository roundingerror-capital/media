"""NEW WAVE (the boss 2026-11-03: "update all the assets, all the characters, all the sprites, make sure everything is looking on the
new wave"). One switch for every builder that runs through tools/daily.py (dailies, lessons, loops, earnings previews):

  characters  old static 1x stickers squashed and rotated in code  ->  Kit's rigs (tools/rigs.py, V2.03/V2.06 boards), whole-number
              scale, the rig's own frames do the acting: the speaker plays the animation for its pose, everyone else idles on a
              beat hop. Shades meme drops on the rig's real eyes.
  rooms       old HQ plates (blurred render) and the SCN loops      ->  Kit's V3.01 stages (tools/stage.py): SCN-NN -> ROOM-NN,
              the standup plate -> ROOM-01 trading floor, Penny's plate -> her OFF-PENNY-01 studio, characters on the stage left
              out (ours stand in front), animated pieces (plants, monitors, pets) playing, a slow camera drift across the room.
  covers      tools/covers2.py sprite() -> the rig's idle frame.

daily.py calls install(module) at import; NEW_WAVE=0 in the environment turns it off (old look, for diffing).
Assets: RE_ASSETS_DIR (local copy of Assets Designs, Kit V3.01)."""
import os, math
from PIL import Image, ImageDraw, ImageEnhance
import rigs, stage

ASSETS = os.environ.get("RE_ASSETS_DIR", "/tmp/claude-0/-home-claude/97ad6b31-1277-5795-987d-0d7c1b8393c4/scratchpad/assets3/project")
os.environ.setdefault("RE_ASSETS_DIR", ASSETS)
K = 15                       # stage px -> video px (72 x 128 portrait window = 1080 x 1920)
ROOMS = {f"SCN-{i:02d}": f"ROOM-{i:02d}" for i in range(1, 20)}
ROOMS.update({"SCN-05": "OFF-ROZ-01", "SCN-13": "ROOM-03"})            # no V3.01 legal library / deep space: Roz's chambers, the rooftop
PLATES = {"plate_standup": "ROOM-01", "plate_standup_clean": "ROOM-01", "plate_penny": "OFF-PENNY-01", "plate_boss": "OFF-BOSS-01"}
DEFAULT_ROOM = "ROOM-01"
POSE = {"jump": "celebrate", "point": "point", "brow": "shakehead", "nod": "nod", "wave": "talk", "spin": "celebrate", "thumbs": "nod",
        "talk": "talk", "shrug": "shrug", "facepalm": "facepalm", "celebrate": "celebrate"}
FLIP = {"theo": False, "penny": False, "ada": True, "kit": True, "roz": True}
# eye boxes on each rig's idle frame 0 (x0, y0, x1, y1), measured from the dark interior clusters (2026-11-03)
EYES = {"theo": [(38, 39, 42, 44), (51, 39, 55, 44)], "penny": [(40, 33, 45, 36), (49, 32, 54, 36)],
        "ada": [(35, 36, 39, 41), (52, 36, 56, 41)], "kit": [(40, 36, 44, 41), (59, 36, 63, 41)],
        "roz": [(51, 52, 56, 58), (66, 52, 71, 58)]}
DESK_SKIP = ("OFFCOOLER",)            # the water cooler reads wrong in a trading room (the boss on the parody)

def room_of(path):
    if not path: return None
    if isinstance(path, str) and (path.startswith("ROOM-") or path.startswith("OFF-")): return path
    if isinstance(path, str) and path.startswith("SCN-"): return ROOMS.get(path, DEFAULT_ROOM)
    base = os.path.splitext(os.path.basename(str(path)))[0]
    return PLATES.get(base, DEFAULT_ROOM)

_ST, _BIG = {}, {}
def _stage(name):
    if name not in _ST: _ST[name] = stage.load(os.path.join(ASSETS, name + ".dc.html"))
    return _ST[name]

ANIMATED = ("PLT", "MON", "PET")
def _animated(st, t):
    """Pieces that move on Kit's boards: swap the still for the captured frame (tools/kitpieces.py), else keep the still."""
    extra, moving = {}, []
    try: import kitpieces as KP
    except Exception: return extra, ()
    for name, uses, _ in st.layers:
        for sid, x, y in uses:
            if sid[:3] in ANIMATED and sid[3:].isdigit():
                try: im = KP.piece(f"{sid[:3]}-{sid[3:]}", t + x * 0.013)
                except Exception: continue
                still = stage.piece(st, sid); moving.append(sid)
                extra.setdefault(name, []).append((im, x + (still.width - im.width), y + (still.height - im.height)))
    return extra, tuple(moving)

def room_big(name, t):
    """The stage at x15 for time t (quantized to Kit's 10 fps), desk chairs kept, cooler out."""
    q = int(t * 10)
    key = (name, q % 40)
    if key not in _BIG:
        st = _stage(name); extra, moving = _animated(st, q / 10)
        im = st.render(skip=DESK_SKIP + moving, extra=extra).convert("RGB")
        if len(_BIG) > 48: _BIG.clear()          # each entry is a 4800x1920 RGB (~28 MB)
        _BIG[key] = im.resize((im.width * K, im.height * K), Image.NEAREST)
    return _BIG[key]

def room_frame(name, t, dim=0.42, t0=0.0):
    """1080x1920 crop of the room: starts on Kit's portrait window and drifts slowly (whole video px, pixels stay square)."""
    st = _stage(name); big = room_big(name, t)
    px, py, pw, ph = st.frames.get("portrait", (0, 0, 72, 128))
    x0 = px * K; span = big.width - 1080
    if span > 0:
        amp = min(span, 260); u = (t - t0) * 22                                # ~22 px/s, ping-pong inside the stage
        off = int(amp - abs((u % (2 * amp)) - amp)) if amp else 0
        x = max(0, min(span, x0 - amp // 2 + off))
    else: x = 0
    im = big.crop((x, py * K, x + 1080, py * K + 1920))
    im = ImageEnhance.Brightness(im).enhance(dim)
    return Image.composite(Image.new("RGB", im.size), im, _shade())   # text band darker, floor (where the cast stands) as is

_SH = []
def _shade():
    """Readability mask: y 270-1150 (headline, body, panels) darkened ~45 %, easing back to none by y 1350."""
    if not _SH:
        m = Image.new("L", (1080, 1920), 0); d = ImageDraw.Draw(m)
        for y in range(1920):
            a = 115 if 200 <= y <= 1150 else (int(115 * (1 - (y - 1150) / 200)) if 1150 < y < 1350 else (int(115 * y / 200) if y < 200 else 0))
            d.line([(0, y), (1079, y)], fill=a)
        _SH.append(m)
    return _SH[0]

def sprite(name, anim="idle", t=0.0):
    """A rig frame trimmed to its drawing (the new 'sticker')."""
    s = rigs.frame(name, anim, t); bb = s.getbbox(); return s.crop(bb) if bb else s

def shades(sp, name, k, origin=(0, 0)):
    """Deal-with-it shades on the rig's idle frame 0 (untrimmed coordinates minus origin); k 0..1 = drop progress."""
    boxes = [(a - origin[0], b - origin[1], c - origin[0], e - origin[1]) for a, b, c, e in EYES[name]]
    d = ImageDraw.Draw(sp); x0 = min(b[0] for b in boxes) - 2; x1 = max(b[2] for b in boxes) + 2
    y0 = min(b[1] for b in boxes); y1 = max(b[3] for b in boxes); dy = int((1 - k) * -(y0 + 6))
    d.rectangle([x0, y0 + dy, x1, y0 + dy + 1], fill=(10, 10, 10, 255))
    for bx0, by0, bx1, by1 in boxes:
        d.rectangle([bx0 - 1, y0 + dy, bx1 + 1, y1 + dy], fill=(10, 10, 10, 255)); d.point((bx0, y0 + dy + 1), fill=(255, 255, 255, 255))
    return sp

def install(D):
    """Patch a loaded daily module in place."""
    W, H, BASE = D.W, D.H, D.BASE
    old_bg = D.office_bg

    def office_bg(S, path=None, t=0.0):
        name = room_of(path or S.get("bg"))
        if not name: return old_bg(S, path, t)
        im = room_frame(name, t, max(0.34, S.get("bg_dim", 0.42)))
        if S.get("tod"):
            import earn_recipe; im = earn_recipe.wash(im, S["tod"])                     # recipe time of day (earnings, 2026-11-05)
        return im

    def sprite_state(name, blink, t):
        an = "celebrate" if name == "penny" else "idle"
        s = sprite(name, an, t)
        if name in D.SHADES_ON:
            f = rigs.frame(name, "idle", 0); bb = f.getbbox(); s = shades(f.crop(bb), name, D.SHADES_ON[name], bb[:2])
        return s

    def char_layer(img, d, S, t, cast, lines, text_bottom):
        hpx = S.get("_hpx") or (430 if len(cast) < 3 else 380); k = max(3, round(hpx / 60))
        xs = S.get("_xs") or D.XS[len(cast)]
        pk = [i for i, sc_ in enumerate(S["scenes"]) if t >= sc_[0]]; slide = pk[-1] if pk else 0
        if (S.get("props") or {}).get(slide):                                    # recipe props (earnings, 2026-11-05): floor lane, never on a face
            import earn_recipe; earn_recipe.draw_props(img, S["props"][slide], t, [int(W * x) for x in xs], BASE, W, k)
        for i, n in enumerate(cast):
            xc = int(W * xs[i]); flip = FLIP.get(n, False) and xs[i] > 0.5
            talk = [(ts, te, pose) for ts, te, w, _, pose in lines if w == n and ts <= t < te]
            if n in D.SHADES_ON:                                                # shades meme: rig's idle frame 0 + shades
                f = rigs.frame(n, "idle", 0); sp = shades(f.copy(), n, D.SHADES_ON[n]); hop = 0
                if flip: sp = sp.transpose(Image.FLIP_LEFT_RIGHT)
                sp = sp.resize((sp.width * k, sp.height * k), Image.NEAREST)
            else:
                if talk: ts, te, pose = talk[0]; an, t0 = POSE.get(pose, "talk"), ts
                else: an, t0 = "idle", 0.0
                if an not in rigs.anims(n): an = "talk" if talk else "idle"
                sp = rigs.frame(n, an, t, k=k, flip=flip, loop=True, t0=t0)
                ph = t * S["bpm"] / 60; hop = k * int(round(2 * abs(math.sin(math.pi * ph)))) if not talk else 0
            if (S.get("swaps") or {}).get(n):
                import earn_recipe; sp = earn_recipe.recolor(sp, n, S["swaps"][n])      # Kit's palette swap from the recipe
            bw, _ = rigs.body(n, "idle", k)
            d.ellipse([xc - bw * 0.33, BASE - 8, xc + bw * 0.33, BASE + 16], fill="#1a1a1a")
            img.paste(sp, (xc - sp.width // 2, BASE - sp.height - hop), sp)
        for ts, te, w, ln, _ in lines:
            if ts <= t < te and w in cast:
                xc = int(W * xs[cast.index(w)]); y = max(text_bottom + 24, BASE - hpx - 150); D.bubble(d, xc, y, ln)

    D.office_bg = office_bg; D.sprite_state = sprite_state; D.char_layer = char_layer
    D.END_CAST.update({"roz": "nod", "kit": "jump"})
    D.NEW_WAVE = True
    return D
