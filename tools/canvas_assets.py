"""Artboards for the [re.c] Assets Designs canvas: one sheet per asset family, every asset shown as a looping pixel animation.
Phase 1: python3 tools/canvas_assets.py sheets <out_dir>              -> <out_dir>/sheets/<SET>.png (4x sprite sheets) + <SET>.json (layout)
Phase 2: upload each sheet as an asset of the canvas (Artifact publish, asset: true) and write <out_dir>/blobs.json {"<SET>": "/_blob/<id>"}
Phase 3: python3 tools/canvas_assets.py boards <out_dir> <canvas.json> -> <out_dir>/project/<board>.dc.html + the updated canvas.json
The sheet is one PNG per set (4x NEAREST), each asset one row, frames left to right; CSS keyframes with step-end timing play the
uneven holds (ticks of 100 ms). Nothing is drawn on the canvas with a data: URI; the sheet is an uploaded asset (the Design type's rule)."""
import os, sys, json, html
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import holiday_assets as HA
from pixkit import scaled

K = 4            # canvas preview scale
CELL = 32 * K    # one frame cell on the sheet (the biggest asset is 32 px)

def build_sheet(items, out_png, out_json, kind="HOL"):
    """items: list of (aid, title, frames, ticks). One row per asset, frames left to right, each in a CELL x CELL box (bottom-centred)."""
    nmax = max(len(fr) for _, _, fr, _ in items)
    sheet = Image.new("RGBA", (CELL * nmax, CELL * len(items)), (0, 0, 0, 0)); meta = []
    for r, (aid, title, frames, ticks) in enumerate(items):
        for c, im in enumerate(frames):
            s = scaled(im, K); x = c * CELL + (CELL - s.width) // 2; y = r * CELL + (CELL - s.height); sheet.paste(s, (x, y), s)
        meta.append({"id": aid, "title": title, "row": r, "frames": len(frames), "ticks": ticks, "w": frames[0].width, "h": frames[0].height})
    sheet.save(out_png, optimize=True); json.dump({"cell": CELL, "cols": nmax, "items": meta}, open(out_json, "w"))
    return meta

def css_for(meta, cls, blob):
    """One class + keyframes per asset: background-position jumps at the end of each hold (step-end)."""
    out = [f".{cls}{{width:{CELL}px;height:{CELL}px;background-image:url({blob});background-repeat:no-repeat;image-rendering:pixelated;animation-timing-function:step-end;animation-iteration-count:infinite}}"]
    for m in meta:
        total = sum(m["ticks"]); acc = 0; kf = []
        for i, t in enumerate(m["ticks"]):
            kf.append(f"{acc / total * 100:.2f}%{{background-position:-{i * CELL}px -{m['row'] * CELL}px}}"); acc += t
        kf.append(f"100%{{background-position:-{(len(m['ticks']) - 1) * CELL}px -{m['row'] * CELL}px}}")
        name = cls + m["id"].replace("-", "")
        out.append(f"@keyframes {name}{{{''.join(kf)}}} .{name}{{background-position:0 -{m['row'] * CELL}px;animation-name:{name};animation-duration:{total * 100}ms}}")
    return "\n".join(out)

def board_html(set_code, set_name, meta, blob, w=1240, cols=10, note=""):
    rows = (len(meta) + cols - 1) // cols; cell_w = (w - 64 - (cols - 1) * 8) // cols; cell_h = CELL + 44
    h = 32 + 70 + 18 + rows * (cell_h + 8) + 60
    cls = "s" + set_code.lower()
    cells = []
    for m in meta:
        name = cls + m["id"].replace("-", "")
        cells.append(f'<div style="display: flex; flex-direction: column; align-items: center; gap: 4px; background: #0E1018; padding: 6px 4px; min-width: 0">'
                     f'<div class="{cls} {name}" role="img" aria-label="{html.escape(m["title"])}"></div>'
                     f'<div style="font-family: \'IBM Plex Mono\', monospace; font-size: 10px; letter-spacing: .5px; color: #C8F03C">{m["id"].split("-")[-1]} &#183; {m["w"]}&#215;{m["h"]} &#183; {m["frames"]}f</div>'
                     f'<div style="font-size: 11px; font-weight: 700; color: #C9C9C2; text-align: center; line-height: 1.15; max-width: {cell_w - 8}px">{html.escape(m["title"])}</div></div>')
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>HOL-{set_code} {html.escape(set_name)} assets</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&amp;family=IBM+Plex+Mono:wght@400;500;600;700&amp;display=swap">
<style>body{{margin:0;background:#000000}}
{css_for(meta, cls, blob)}
</style>
</helmet>
<div style="width: {w}px; height: {h}px; box-sizing: border-box; padding: 32px; outline: 10px solid #C8F03C; outline-offset: -10px; background: #000000; color: #F2F2EE; font-family: 'Archivo', 'Helvetica Neue', sans-serif; display: flex; flex-direction: column; gap: 14px">
<div style="display: flex; justify-content: space-between; font-family: 'IBM Plex Mono', monospace; font-size: 12px; letter-spacing: 1px; color: #9A9A94"><span>&#8776; ROUNDING ERROR &#183; HOLIDAY ASSETS</span><span>HOL-{set_code}-01..{len(meta):02d} &#183; V2.03 &#183; {K}&#215; preview, 1 tick = 100 ms</span></div>
<div style="display: flex; align-items: baseline; gap: 14px"><h1 style="margin: 0; font-size: 34px; font-weight: 900; font-stretch: 125%; letter-spacing: -1px">{html.escape(set_name)}</h1><span style="font-size: 16px; font-weight: 700; color: #C9C9C2">{html.escape(note)}</span></div>
<div style="display: grid; grid-template-columns: repeat({cols}, minmax(0, 1fr)); gap: 8px">
{"".join(cells)}
</div>
<div style="display: flex; justify-content: space-between; font-family: 'IBM Plex Mono', monospace; font-size: 10px; letter-spacing: 1px; color: #9A9A94"><span>holiday_assets.frames("HOL-{set_code}-NN") &#183; every frame its own drawing &#183; signs blank, no digits, no brands</span><span>@roundingerror.capital</span></div>
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{w},"height":{h}}}}}'>
class Component extends DCLogic {{
renderVals() {{ return {{}}; }}
}}
</script>
</body>
</html>
''', h

NOTES = {"NYD": "The ball, the clock, the pop, the confetti. No year digits anywhere.", "MLK": "A day of service: the podium, the dove, the vigil candle, the open book, the blank placard.",
         "PRES": "Stovepipe, tricorne, quill and parchment, cherry pie, the obelisk and the dome.", "GF": "The spring long weekend: tulips, eggs, chicks, rain boots and the first sprout.",
         "MEM": "Poppies, the folded flag, the bugle, then the grill, the cooler and the lawn chair.", "JUN": "Red, black, green and gold: drums, bells, lanterns, red velvet and strawberry soda.",
         "IND": "Fireworks, flags, Liberty's crown and torch, the grill and the pool float.", "LAB": "Hard hats, tools, the lunch pail, then the hammock and the last beach day.",
         "TG": "The bird, the pies, the cornucopia, maple leaves and the pilgrim hat.", "XMAS": "The tree, baubles, stockings, cocoa, snowman and the fireplace."}

if __name__ == "__main__":
    cmd, out = sys.argv[1], sys.argv[2]; os.makedirs(os.path.join(out, "sheets"), exist_ok=True)
    if cmd == "sheets":
        for code in HA.SETS:
            items = []
            for aid in HA.ids(code):
                fr, tk = HA.frames(aid); items.append((aid, HA.title(aid), fr, tk))
            build_sheet(items, os.path.join(out, "sheets", f"{code}.png"), os.path.join(out, "sheets", f"{code}.json")); print(code, "ok")
    elif cmd == "boards":
        blobs = json.load(open(os.path.join(out, "blobs.json"))); cj = json.load(open(sys.argv[3])); os.makedirs(os.path.join(out, "project"), exist_ok=True)
        x, y = 0, 0; written = []
        for i, code in enumerate(HA.SETS):
            meta = json.load(open(os.path.join(out, "sheets", f"{code}.json")))["items"]
            src, h = board_html(code, HA.SETS[code], meta, blobs[code], note=NOTES.get(code, ""))
            fn = f"HOL{code}V2_03.dc.html"; open(os.path.join(out, "project", fn), "w").write(src)
            cj["boards"][fn] = {"title": f"HOL-{code} · {HA.SETS[code]} · 50 animated assets · V2.03", "page": "holidays", "x": (i % 2) * 1320, "y": (i // 2) * (h + 120), "w": 1240, "h": h}
            if fn not in cj["order"]: cj["order"].append(fn)
            written.append(fn)
        cj["notes"]["hol_title"] = {"kind": "title1", "page": "holidays", "x": 0, "y": -300, "maxW": 2560, "text": "Holiday assets V2.03 (2026-11-02) · 10 market-closed days × 50 animated props · HOL-<SET>-NN · one drawing per frame"}
        json.dump(cj, open(sys.argv[3], "w"), indent=1); print(json.dumps(written))
