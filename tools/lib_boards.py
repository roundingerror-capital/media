"""Library boards for the [re.c] Assets Designs canvas (the boss 2026-11-02): one board per genre, sprites grouped, and every cell
shows the sprite three ways so small never surprises us:
  ZOOM ×6 (animated)  ·  WITH THEO (true scale, ×2)  ·  ACTUAL (true scale, ×1: roughly phone size)

  python3 tools/lib_boards.py sheet <GENRE> <out_dir>          -> <out_dir>/<GENRE>_zoom.png, _pair.png, _meta.json
  python3 tools/lib_boards.py board <GENRE> <out_dir> <zoom_blob> <pair_blob>  -> <out_dir>/project/LIB<GENRE>.dc.html (+ prints h)
"""
import os, sys, json, html
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib
HERE = os.path.dirname(os.path.abspath(__file__))
THEO = Image.open(os.path.join(HERE, "sprites", "theo_sprite_1x.png")).convert("RGBA")
Z = 6           # zoom factor
CELL = 16 * Z   # zoom box (96) — 20/24 px sprites shrink to fit? no: box grows to the largest sprite
PAIR_K = 2

def order(genre):
    ids = lib.ids(genre); groups = []
    for sid in ids:
        g = lib.info(sid)["group"]
        if g not in groups: groups.append(g)
    return [(g, [s for s in ids if lib.info(s)["group"] == g]) for g in groups]

def sheet(genre, out):
    os.makedirs(out, exist_ok=True)
    ids = [s for _, ss in order(genre) for s in ss]
    mw = max(lib.info(s)["size"][0] for s in ids); mh = max(lib.info(s)["size"][1] for s in ids); mf = max(len(lib.frames(s)[0]) for s in ids)
    zw, zh = mw * Z, mh * Z
    zoom = Image.new("RGBA", (zw * mf, zh * len(ids))); meta = {"zw": zw, "zh": zh, "items": []}
    pw = THEO.width + mw + 4; ph = max(THEO.height, mh); pair = Image.new("RGBA", (pw * PAIR_K, ph * PAIR_K * len(ids)))
    for r, sid in enumerate(ids):
        fr, tk = lib.frames(sid); s = lib.info(sid); w, h = s["size"]
        for c, im in enumerate(fr):
            b = im.resize((w * Z, h * Z), Image.NEAREST); zoom.paste(b, (c * zw + (zw - b.width) // 2, r * zh + (zh - b.height) // 2), b)
        p = Image.new("RGBA", (pw, ph)); p.paste(THEO, (0, ph - THEO.height), THEO); p.paste(fr[0], (THEO.width + 4, ph - h), fr[0])
        p = p.resize((pw * PAIR_K, ph * PAIR_K), Image.NEAREST); pair.paste(p, (0, r * ph * PAIR_K), p)
        meta["items"].append({"id": sid, "title": s["title"], "group": s["group"], "w": w, "h": h, "n": len(fr), "ticks": tk})
    meta.update({"pw": pw * PAIR_K, "ph": ph * PAIR_K})
    zoom.save(os.path.join(out, f"{genre}_zoom.png")); pair.save(os.path.join(out, f"{genre}_pair.png"))
    json.dump(meta, open(os.path.join(out, f"{genre}_meta.json"), "w")); print(genre, len(ids), "sprites", zoom.size, pair.size)

def board(genre, out, zblob, pblob, cols=6, w=1240):
    meta = json.load(open(os.path.join(out, f"{genre}_meta.json"))); name = dict((g, n) for g, n, _ in lib.GENRES)[genre]
    note = dict((g, x) for g, _, x in lib.GENRES)[genre]
    zw, zh, pw, ph = meta["zw"], meta["zh"], meta["pw"], meta["ph"]
    css = [f".lz{{width:{zw}px;height:{zh}px;background-image:url({zblob});background-repeat:no-repeat;image-rendering:pixelated}}",
           f".lp{{width:{pw}px;height:{ph}px;background-image:url({pblob});background-repeat:no-repeat;image-rendering:pixelated}}",
           f".la{{width:{pw // PAIR_K}px;height:{ph // PAIR_K}px;background-image:url({pblob});background-repeat:no-repeat;background-size:{pw // PAIR_K}px auto;image-rendering:pixelated}}"]
    sections = []; idx = 0; rows_total = 0
    by_group = {}
    for it in meta["items"]: by_group.setdefault(it["group"], []).append(it)
    for g, items in by_group.items():
        cells = []
        for it in items:
            k = "z" + it["id"].replace("-", "_"); r = idx; idx += 1
            tot = sum(it["ticks"]); acc = 0; kf = []
            for c, t in enumerate(it["ticks"]):
                kf.append(f"{acc / tot * 100:.2f}%{{background-position:-{c * zw}px -{r * zh}px}}"); acc += t
            kf.append(f"100%{{background-position:-{(len(it['ticks']) - 1) * zw}px -{r * zh}px}}")
            anim = f"animation:{k} {tot * 100}ms step-end infinite;" if it["n"] > 1 else ""
            css.append(f".{k}{{background-position:0 -{r * zh}px;{anim}}}" + (f"@keyframes {k}{{{''.join(kf)}}}" if it["n"] > 1 else ""))
            css.append(f".p{k}{{background-position:0 -{r * ph}px}} .a{k}{{background-position:0 -{r * ph // PAIR_K}px}}")
            cells.append(
                f'<div style="display: flex; flex-direction: column; align-items: center; gap: 6px; background: #0E1018; padding: 10px 6px; min-width: 0">'
                f'<div class="lz {k}" role="img" aria-label="{html.escape(it["title"])}, zoomed"></div>'
                f'<div style="display: flex; align-items: flex-end; gap: 10px"><div class="lp p{k}" role="img" aria-label="{html.escape(it["title"])} next to Theo, true scale"></div>'
                f'<div class="la a{k}" role="img" aria-label="{html.escape(it["title"])} at actual size"></div></div>'
                f'<div style="font-family: \'IBM Plex Mono\', monospace; font-size: 10px; letter-spacing: .5px; color: #C8F03C">{it["id"]} &#183; {it["w"]}&#215;{it["h"]}{" &#183; " + str(it["n"]) + "f" if it["n"] > 1 else ""}</div>'
                f'<div style="font-size: 12px; font-weight: 700; color: #C9C9C2; text-align: center; line-height: 1.15">{html.escape(it["title"])}</div></div>')
        rows = (len(items) + cols - 1) // cols; rows_total += rows
        sections.append(f'<div style="display: flex; flex-direction: column; gap: 8px"><h2 style="margin: 0; font-size: 22px; font-weight: 900; font-stretch: 110%; color: #F2F2EE">{html.escape(g)} <span style="font-family: \'IBM Plex Mono\', monospace; font-size: 12px; color: #9A9A94">{len(items)}</span></h2>'
                        f'<div style="display: grid; grid-template-columns: repeat({cols}, minmax(0, 1fr)); gap: 8px">{"".join(cells)}</div></div>')
    cell_h = zh + ph + 70
    h = 32 + 80 + 40 + len(by_group) * 50 + rows_total * (cell_h + 8) + 60
    src = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{genre} {html.escape(name)}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&amp;family=IBM+Plex+Mono:wght@400;500;600;700&amp;display=swap">
<style>body{{margin:0;background:#000000}}
{chr(10).join(css)}
</style>
</helmet>
<div style="width: {w}px; height: {h}px; box-sizing: border-box; padding: 32px; outline: 10px solid #C8F03C; outline-offset: -10px; background: #000000; color: #F2F2EE; font-family: 'Archivo', 'Helvetica Neue', sans-serif; display: flex; flex-direction: column; gap: 18px">
<div style="display: flex; justify-content: space-between; font-family: 'IBM Plex Mono', monospace; font-size: 12px; letter-spacing: 1px; color: #9A9A94"><span>&#8776; ROUNDING ERROR &#183; THE LIBRARY</span><span>{genre}-&#8230; &#183; {len(meta["items"])} sprites &#183; V3.00 &#183; zoom &#215;{Z} &#183; with Theo &#215;{PAIR_K} &#183; actual &#215;1</span></div>
<div style="display: flex; align-items: baseline; gap: 14px"><h1 style="margin: 0; font-size: 40px; font-weight: 900; font-stretch: 125%; letter-spacing: -1px">{html.escape(name)}</h1><span style="font-size: 16px; font-weight: 700; color: #C9C9C2">{html.escape(note)}</span></div>
{"".join(sections)}
<div style="display: flex; justify-content: space-between; font-family: 'IBM Plex Mono', monospace; font-size: 10px; letter-spacing: 1px; color: #9A9A94"><span>lib.get("{meta["items"][0]["id"]}", t) &#183; hand-drawn grids, every frame its own drawing &#183; no digits, no brands</span><span>@roundingerror.capital</span></div>
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{w},"height":{h}}}}}'>
class Component extends DCLogic {{
renderVals() {{ return {{}}; }}
}}
</script>
</body>
</html>
'''
    os.makedirs(os.path.join(out, "project"), exist_ok=True)
    open(os.path.join(out, "project", f"LIB{genre}.dc.html"), "w").write(src); print(h); return h

if __name__ == "__main__":
    if sys.argv[1] == "sheet": sheet(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "board": board(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
