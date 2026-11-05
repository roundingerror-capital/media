#!/usr/bin/env python3
"""scan_review: the boss's Ignore flow for the publisher's safety scan (T-103, the boss 2026-11-05:
"put the frame with the issue ... a red box ... so I can just click ignore, ignore, ignore").

  build <hits_dir> <card.json> <sha256> <preview_url> <out_dir>
      After safety_scan.py --hits-dir blocked a video: writes <out_dir>/scan_review.json (the card's new
      scan_review field) and <out_dir>/frames/<card id>__<hit id>.json (one Posts "scan_frames" doc per
      number hit: a 360 px JPEG as a data URI, ~25 KB). A flag the boss already ignored on this same video
      (same sha256) and that the new scan finds again keeps its "ignored" entry.
  match <hits_dir> <card.json> <sha256>
      Exit 0 = every hit of this scan is a number flag the boss ignored on this exact file (sha256), so
      the publisher may go on. Exit 1 = anything else (a new flag, a private-list hit, another file).
      Prints counts only, never matched text.

If ANY hit is a private-list hit, nothing is shown: no frames, no figure text (Penny fixes the video).
Matching: same kind; number flags = same figure (spaces dropped) and start time within 0.30 s;
text flags = same text field and same figure. Private-list hits are never ignorable."""
import sys, os, json, base64, datetime


def _key(h):
    return (h.get("kind"), str(h.get("token", "")).replace(" ", ""), h.get("field"))


def _same(a, b):
    if _key(a) != _key(b):
        return False
    if a.get("kind") == "number":
        return abs(float(a.get("t", 0)) - float(b.get("t", 0))) <= 0.30
    return True


def _prior(card, sha):
    r = card.get("scan_review") or {}
    if r.get("sha256") != sha:
        return [], {}
    return r.get("hits") or [], r.get("ignored") or {}


def build(hits_dir, card_p, sha, preview_url, out):
    card = json.load(open(card_p)); card = card.get("data", card)
    cid = card.get("id") or card.get("_id") or os.path.basename(card_p)[:-5]
    hits = json.load(open(os.path.join(hits_dir, "hits.json")))
    old_hits, old_ign = _prior(card, sha)
    now = datetime.datetime.now(__import__("zoneinfo").ZoneInfo("America/New_York")).isoformat(timespec="seconds")  # ET, like every timestamp we write
    ignored = {}
    for h in hits:
        for o in old_hits:
            if o.get("id") in old_ign and _same(h, o) and h.get("kind") != "private":
                ignored[h["id"]] = old_ign[o["id"]]
                break
    os.makedirs(os.path.join(out, "frames"), exist_ok=True)
    priv = any(h.get("kind") == "private" for h in hits)
    clean = []
    for h in hits:
        c = {k: v for k, v in h.items() if k != "frame"}
        if priv or h.get("kind") == "private":  # a private-list hit anywhere: no figure text and no frames at all
            c = {k: h[k] for k in ("id", "kind", "t", "field") if k in h}  # never any text
        clean.append(c)
        fr = h.get("frame")
        if not priv and h.get("kind") == "number" and fr and os.path.exists(os.path.join(hits_dir, fr)):
            img = "data:image/jpeg;base64," + base64.b64encode(open(os.path.join(hits_dir, fr), "rb").read()).decode()
            json.dump({"img": img, "card": cid, "hit": h["id"], "sha256": sha, "at": now},
                      open(os.path.join(out, "frames", f"{cid}__{h['id']}.json"), "w"))
    rev = {"at": now, "by": "publisher", "sha256": sha, "preview_url": preview_url, "hits": clean[:40],
           "more": max(0, len(clean) - 40), "ignored": ignored}
    json.dump(rev, open(os.path.join(out, "scan_review.json"), "w"), indent=1)
    left = sum(1 for h in clean if h.get("kind") != "private" and h["id"] not in ignored)
    print(f"flags {len(clean)} · already ignored {len(ignored)} · to check {left} · private {sum(1 for h in clean if h.get('kind') == 'private')} · frames {len(os.listdir(os.path.join(out, 'frames')))}")


def match(hits_dir, card_p, sha):
    card = json.load(open(card_p)); card = card.get("data", card)
    hits = json.load(open(os.path.join(hits_dir, "hits.json")))
    old_hits, old_ign = _prior(card, sha)
    if not (card.get("scan_review") or {}).get("cleared"):
        print("NOT CLEARED: the boss has not ignored every flag on this video"); return 1
    bad = 0
    for h in hits:
        if h.get("kind") == "private" or not any(o.get("id") in old_ign and _same(h, o) for o in old_hits):
            bad += 1
    print(f"hits {len(hits)} · covered by the boss's ignores {len(hits) - bad} · new {bad}")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "build" and len(a) == 6:
        build(*a[1:])
    elif a and a[0] == "match" and len(a) == 4:
        sys.exit(match(*a[1:]))
    else:
        print(__doc__); sys.exit(2)
