"""The star gate (the boss 2026-11-02): only assets he starred on the design canvases may appear in a video.

Stars live in each canvas's own database, collection `stars`, doc id = asset id, {approved: true, at, by} (tools/stars.py puts
the buttons on the boards). This module reads a synced copy, tools/approved.json:
  {"synced_at": "...", "mascots": ["V2_03TheoCelebrate", ...], "assets": ["SCN-01", "PROP-001", "BLD-03-F1", ...], "social": [...]}
Sync = ArtifactData list of `stars` on the three canvases (Penny's chat or the builder task does it before a build):
  python3 tools/approved.py sync <mascots.json> <assets.json> <social.json>   # each: the ArtifactData list result saved as JSON

Loaders call `approved.check(kind, id)`; it raises NotApproved unless the id (or, for a character animation, the character's
Core10 board) is starred. REC_UNSTARRED=1 in the environment turns the gate into a warning for drafts and tests; the publisher
never sets it, so nothing unstarred can reach Roz or the boss by accident.

  kind "anim":  id "theo/celebrate" -> board V2_03TheoCelebrate, or the character's V2_03TheoCore10 star (all ten at once)
  kind "scene": "SCN-01"   kind "prop": "PROP-001"   kind "holiday": "HOL-XMAS-07"   kind "asset": "BLD-03", "BUB-01", "PIG-01"
"""
import os, sys, json, warnings
HERE = os.path.dirname(os.path.abspath(__file__)); FILE = os.path.join(HERE, "approved.json")
CHAR = {"theo": "Theo", "penny": "Penny", "ada": "Ada", "kit": "Kit", "roz": "Roz", "boss": "Boss", "realboss": "RealBoss", "realboss_hood": "RealBossHood"}
_D = None

class NotApproved(RuntimeError): pass

def load():
    global _D
    if _D is None:
        try: _D = json.load(open(FILE))
        except Exception: _D = {"synced_at": None, "mascots": [], "assets": [], "social": []}
    return _D

def stars(canvas): return set(load().get(canvas, []))

def is_approved(kind, aid):
    if kind == "anim":
        ch, an = aid.split("/"); c = CHAR.get(ch, ch.capitalize()); m = stars("mascots")
        return f"V2_03{c}{an.capitalize()}" in m or f"V2_03{c}Core10" in m
    return aid in stars("assets")

def check(kind, aid):
    if is_approved(kind, aid): return True
    msg = f"NOT STARRED: {kind} {aid} has no approval star on the design canvas (the boss 2026-11-02: only starred assets go in videos)"
    if os.environ.get("REC_UNSTARRED"):
        warnings.warn(msg); return False
    raise NotApproved(msg)

def sync(paths):
    out = {"synced_at": __import__("datetime").datetime.now().astimezone().isoformat(timespec="seconds")}
    for canvas, p in zip(("mascots", "assets", "social"), paths):
        ids = []
        for f in (sorted(os.listdir(p)) if os.path.isdir(p) else [p]):
            fp = os.path.join(p, f) if os.path.isdir(p) else f
            d = json.load(open(fp)); d = d.get("data", d)
            if isinstance(d, dict) and d.get("approved"): ids.append(os.path.basename(fp)[:-5] if os.path.isdir(p) else d.get("id"))
        out[canvas] = sorted(set(ids))
    json.dump(out, open(FILE, "w"), indent=1); print({k: len(v) for k, v in out.items() if isinstance(v, list)})

if __name__ == "__main__":
    if sys.argv[1] == "sync": sync(sys.argv[2:5])
    elif sys.argv[1] == "check": print(is_approved(sys.argv[2], sys.argv[3]))
