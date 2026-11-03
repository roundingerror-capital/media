"""Approval stars on the design canvases (the boss 2026-11-02: "a little star I can click on per asset; only assets with the star
can be used in videos, because I have worked on them until I love them").

Every artboard (*.dc.html) of a Design canvas gets a star button; the generated 50-up grids (holiday sets, random props) get one
per sprite. Clicking it writes {approved: true, at, by} to the canvas's own database at stars/<ASSET-ID> (write rule: admin, so
only the boss and editors); clicking again deletes it. tools/approved.py reads the three canvases' `stars` collections (synced to
tools/approved.json) and the loaders (rigs, scenes, props, assets) refuse anything without a star.

Usage:  python3 tools/stars.py inject <canvas_dir> <out_dir>   # canvas_dir holds project/*.dc.html + project/canvas.json
        -> out_dir/project/<board>.dc.html for every board that changed, out_dir/project/canvas.json (star-list boards added),
           out_dir/ids.json (board -> [asset ids]).

Tiny raw components (no frame, < 400 px wide: the office furniture DEC/CHR/FLR/..., imported into rooms with <dc-import>) are NOT
touched, because a star inside them would appear in every room that imports them; they get a STARS-<FAMILY> list board instead,
with each piece drawn live via <dc-import> next to its star."""
import os, re, sys, json, html

CSS = """.recstar{position:absolute;top:12px;right:12px;z-index:999;width:36px;height:36px;border-radius:50%;border:2px solid #C8F03C;background:#000;color:#C8F03C;font:20px/32px sans-serif;text-align:center;cursor:pointer;padding:0;margin:0;box-shadow:0 0 0 2px #000}
.recstar.on{background:#C8F03C;color:#000}
.recstar.cell{top:2px;right:2px;width:24px;height:24px;font:15px/20px sans-serif}
.recstar:hover{transform:scale(1.12)}"""

LOGIC = """
// Approval stars (tools/stars.py). stars/<id> = {approved:true, at, by}; one write per click; the canvas db rule is admin-only.
const REC_STAR_IDS = %s;
class Component extends RecBase {
  constructor(props) { super(props); this.state = Object.assign({}, this.state || {}, { recStars: {}, recDb: null }); }
  componentDidMount() {
    if (super.componentDidMount) { try { super.componentDidMount(); } catch (e) {} }
    try {
      const p = (window.claude && typeof window.claude.use === 'function') ? window.claude.use('db') : null;
      if (p && typeof p.then === 'function') p.then((db) => {
        if (!db) return;
        this.setState({ recDb: db });
        try {
          this._recUn = db.collection('stars').onSnapshot((snap) => {
            const m = {}; snap.docs.forEach((d) => { const v = d.data(); if (v && v.approved) m[d.id] = true; });
            this.setState({ recStars: m });
          }, () => {});
        } catch (e) {}
      }).catch(() => {});
    } catch (e) {}
  }
  componentWillUnmount() { if (this._recUn) { try { this._recUn(); } catch (e) {} } if (super.componentWillUnmount) { try { super.componentWillUnmount(); } catch (e) {} } }
  renderVals() {
    const base = (super.renderVals ? super.renderVals() : {}) || {}; const o = Object.assign({}, base);
    const stars = this.state.recStars || {}; const db = this.state.recDb;
    REC_STAR_IDS.forEach(([id, key, cell]) => {
      const on = !!stars[id];
      o['sv_' + key] = on ? '\\u2605' : '\\u2606';
      o['sc_' + key] = (on ? 'recstar on' : 'recstar') + (cell ? ' cell' : '');
      o['st_' + key] = (e) => {
        if (e && e.preventDefault) e.preventDefault(); if (e && e.stopPropagation) e.stopPropagation();
        if (!db) return;
        const ref = db.doc('stars/' + id);
        (on ? ref.delete() : ref.set({ approved: true, at: new Date().toISOString(), by: 'owner' })).catch(() => {});
      };
    });
    return o;
  }
}
"""

def key_of(aid): return re.sub(r"[^A-Za-z0-9]", "_", aid)

def board_asset_id(fn):
    """Canonical asset id for a one-asset board, from its file name."""
    stem = fn[:-len(".dc.html")]
    m = re.match(r"^(SCN|BUB|PIG|BLD)(\d\d)(?:F(\d)[A-Za-z]*)?(?:V\d+(?:_\d+)?)?$", stem)
    if m:
        base = f"{m.group(1)}-{m.group(2)}"
        return base + (f"-F{m.group(3)}" if m.group(3) else "")
    return stem   # DEC-01, OFF-THEO-01, V2_03TheoCelebrate, av-theo, ...

def grid_ids(src):
    """[(asset id, cell class name)] for the generated 50-up grids (canvas_assets.board_html)."""
    out = []
    for cls, name in re.findall(r'<div class="(s[a-z]+) (s[a-z]+[A-Z][A-Z0-9]*)" role="img"', src):
        raw = name[len(cls):]
        if raw.startswith("PROP"): aid = f"PROP-{raw[4:]}"
        elif raw.startswith("HOL"):
            mm = re.match(r"HOL([A-Z]+?)(\d+)$", raw); aid = f"HOL-{mm.group(1)}-{mm.group(2)}"
        else: aid = raw
        out.append((aid, name))
    return out

ROOT = re.compile(r'</helmet>(?:\s*<svg width="0" height="0"[^>]*>.*?</svg>)?\s*<div style="(width: (\d+)px[^"]*)">', re.S)   # the hidden svg defs some boards carry come first
def root_width(src):
    m = ROOT.search(src); return int(m.group(2)) if m else None

def is_raw(src):
    """A bare component (no frame): imported into other boards, so it must not carry the star."""
    w = root_width(src)
    return w is not None and w < 400 and "outline: 10px solid" not in src

def inject(src, aid):
    """One star at the top-right of the board (or one per cell on a grid). Returns (new_src, ids) or (None, []) if untouched."""
    if "recstar" in src: return None, []
    ids = []
    cells = grid_ids(src)
    if cells:
        for cid, name in cells:
            k = key_of(cid); ids.append([cid, k, True])
            # make the cell relative and add the star right after its opening tag
            pat = re.compile(r'(<div style="display: flex; flex-direction: column; align-items: center; gap: 4px; background: #0E1018; padding: 6px 4px; min-width: 0)(">)(\s*<div class="s[a-z]+ ' + re.escape(name) + r'" role="img")')
            src, n = pat.subn(r'\1; position: relative\2<button type="button" class="{{sc_' + k + r'}}" onClick="{{st_' + k + r'}}" title="' + html.escape(cid) + r' · approved for videos">{{sv_' + k + r'}}</button>\3', src, count=1)
            if n != 1: raise RuntimeError(f"grid cell not found for {cid}")
    else:
        k = key_of(aid); ids.append([aid, k, False])
        m = ROOT.search(src)
        if not m: return None, []
        star = f'<button type="button" class="{{{{sc_{k}}}}}" onClick="{{{{st_{k}}}}}" title="{html.escape(aid)} · approved for videos">{{{{sv_{k}}}}}</button>'
        # position: relative on the root div, the star right after its opening tag
        s1, e1 = m.start(1), m.end(1)
        src = src[:s1] + "position: relative; " + src[s1:m.end()] + star + src[m.end():]
    # css into the helmet style block
    src = src.replace("</style>\n</helmet>", "\n" + CSS + "\n</style>\n</helmet>", 1) if "</style>\n</helmet>" in src else src.replace("</style>", "\n" + CSS + "\n</style>", 1)
    # logic: rename the existing component, extend it
    src, n = re.subn(r"class Component extends DCLogic", "class RecBase extends DCLogic", src, count=1)
    if n != 1: raise RuntimeError("no DCLogic component")
    src = src.replace("</script>\n</body>", LOGIC % json.dumps(ids) + "</script>\n</body>", 1)
    return src, ids

def title_of(src):
    m = re.search(r"<title>(.*?)</title>", src, re.S); return html.unescape(m.group(1)) if m else ""

def star_list_board(family, items, w=1240):
    """A framed board listing raw components of one family: live <dc-import> thumbnail, id, title, star."""
    cols = 4; rows = (len(items) + cols - 1) // cols; cell_h = 150; h = 32 + 70 + 18 + rows * (cell_h + 8) + 60
    ids = []; cells = []
    for aid, title, cw, ch in items:
        k = key_of(aid); ids.append([aid, k, True])
        sc = min(1.0, 96 / max(cw, 1), 96 / max(ch, 1))
        cells.append(f'<div style="position: relative; display: flex; flex-direction: column; align-items: center; gap: 6px; background: #0E1018; padding: 8px 6px; min-width: 0; height: {cell_h}px; box-sizing: border-box">'
                     f'<button type="button" class="{{{{sc_{k}}}}}" onClick="{{{{st_{k}}}}}" title="{html.escape(aid)} · approved for videos">{{{{sv_{k}}}}}</button>'
                     f'<div style="height: 100px; display: flex; align-items: center; justify-content: center; line-height: 0"><div style="transform: scale({sc:.3f}); transform-origin: center; image-rendering: pixelated"><dc-import name="{html.escape(aid)}" hint-size="{cw}px,{ch}px"></dc-import></div></div>'
                     f'<div style="font-family: \'IBM Plex Mono\', monospace; font-size: 11px; letter-spacing: .5px; color: #C8F03C">{html.escape(aid)}</div>'
                     f'<div style="font-size: 11px; font-weight: 700; color: #C9C9C2; text-align: center; line-height: 1.15">{html.escape(title)}</div></div>')
    src = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>STARS {html.escape(family)} approvals</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&amp;family=IBM+Plex+Mono:wght@400;500;600;700&amp;display=swap">
<style>body{{margin:0;background:#000000}}
{CSS}
</style>
</helmet>
<div style="width: {w}px; height: {h}px; box-sizing: border-box; padding: 32px; outline: 10px solid #C8F03C; outline-offset: -10px; background: #000000; color: #F2F2EE; font-family: 'Archivo', 'Helvetica Neue', sans-serif; display: flex; flex-direction: column; gap: 14px">
<div style="display: flex; justify-content: space-between; font-family: 'IBM Plex Mono', monospace; font-size: 12px; letter-spacing: 1px; color: #9A9A94"><span>&#8776; ROUNDING ERROR &#183; APPROVALS</span><span>{html.escape(family)} &#183; {len(items)} pieces &#183; &#9733; = cleared for videos</span></div>
<div style="display: flex; align-items: baseline; gap: 14px"><h1 style="margin: 0; font-size: 34px; font-weight: 900; font-stretch: 125%; letter-spacing: -1px">{html.escape(family)} &#183; approvals</h1><span style="font-size: 16px; font-weight: 700; color: #C9C9C2">Tap the star when a piece is good enough for a video. These pieces are imported into rooms, so their stars live here, not on them.</span></div>
<div style="display: grid; grid-template-columns: repeat({cols}, minmax(0, 1fr)); gap: 8px">
{"".join(cells)}
</div>
<div style="display: flex; justify-content: space-between; font-family: 'IBM Plex Mono', monospace; font-size: 10px; letter-spacing: 1px; color: #9A9A94"><span>stars/&lt;ID&gt; in this canvas's database &#183; tools/approved.py reads them</span><span>@roundingerror.capital</span></div>
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{w},"height":{h}}}}}'>
class RecBase extends DCLogic {{
renderVals() {{ return {{}}; }}
}}
{LOGIC % json.dumps(ids)}</script>
</body>
</html>
'''
    return src, h, ids

def run(canvas_dir, out_dir):
    proj = os.path.join(canvas_dir, "project"); cj = json.load(open(os.path.join(proj, "canvas.json")))
    os.makedirs(os.path.join(out_dir, "project"), exist_ok=True)
    all_ids = {}; raw = {}; changed = []
    for fn in sorted(os.listdir(proj)):
        if not fn.endswith(".dc.html"): continue
        src = open(os.path.join(proj, fn), encoding="utf-8").read()
        if fn == "Main.dc.html" and "what lives here" in (cj["boards"].get(fn, {}).get("title", "") + title_of(src)).lower(): continue   # an index page, not an asset
        if is_raw(src):
            fam = fn.split("-")[0] if "-" in fn else "MISC"
            m = re.search(r'<div style="width: (\d+)px; height: (\d+)px', src)
            raw.setdefault(fam, []).append((fn[:-8], title_of(src).split(" ", 1)[-1] if title_of(src) else fn[:-8], int(m.group(1)), int(m.group(2))))
            continue
        new, ids = inject(src, board_asset_id(fn))
        if new is None: continue
        open(os.path.join(out_dir, "project", fn), "w", encoding="utf-8").write(new); all_ids[fn] = [i[0] for i in ids]; changed.append(fn)
        if fn in cj["boards"]: cj["boards"][fn]["is_interactive"] = True   # the Play button: stars are clicked in Play, not in the editing view
    # star-list boards for the raw families, placed to the right of the family's boards on their page
    for fam, items in sorted(raw.items()):
        src, h, ids = star_list_board(fam, items)
        fn = f"STARS-{fam}.dc.html"; open(os.path.join(out_dir, "project", fn), "w", encoding="utf-8").write(src)
        fam_boards = [cj["boards"][f] for f in cj["boards"] if f.startswith(fam + "-")]
        page = fam_boards[0]["page"] if fam_boards else cj["pages"][0]["id"]
        x = max(b["x"] + b["w"] for b in fam_boards) + 120 if fam_boards else 0; y = min(b["y"] for b in fam_boards) if fam_boards else 0
        cj["boards"][fn] = {"title": f"STARS · {fam} · approvals for videos", "page": page, "x": x, "y": y, "w": 1240, "h": h, "is_interactive": True}
        if fn not in cj["order"]: cj["order"].append(fn)
        all_ids[fn] = [i[0] for i in ids]; changed.append(fn)
    json.dump(cj, open(os.path.join(out_dir, "project", "canvas.json"), "w"), indent=1)
    json.dump(all_ids, open(os.path.join(out_dir, "ids.json"), "w"), indent=1)
    print(len(changed), "boards written;", sum(len(v) for v in all_ids.values()), "stars;", "raw families:", {k: len(v) for k, v in raw.items()})

if __name__ == "__main__":
    if sys.argv[1] == "inject": run(sys.argv[2], sys.argv[3])
