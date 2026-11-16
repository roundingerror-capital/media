"""Privacy guard for anything that leaves the building (2026-10-26). Second line of defence next to safety_scan.py.
Checks text against the PRIVATE banned list (Database · Posts settings/privacy, saved to a file OUTSIDE the repo):
  python3 tools/privacy_guard.py --banned-file <list.json> --text "<any string>"     # e.g. a card's public fields
  python3 tools/privacy_guard.py --banned-file <list.json> --files a.py b.json        # files about to be committed
  python3 tools/privacy_guard.py --install <list.json>                                 # git hooks: pre-commit + commit-msg + pre-push
Exit 1 = blocked (prints what and where). The hooks block a commit whose staged diff or message, or a push whose commits, contain a banned term."""
import sys, os, re, json, subprocess, shutil
IDENTITY = "--identity" in sys.argv  # code, commits and repo files: identity terms only (bitrates like 192k are not size claims)
def load(path):
    d = json.load(open(path)); key = "identity_patterns" if IDENTITY else "banned_patterns"
    return [re.compile(p, re.I) for p in (d.get(key, d.get("banned_patterns")) if isinstance(d, dict) else d)]
def hits(pats, text, where):
    out = []
    for p in pats:
        for m in p.finditer(text): out.append(f"{where}: '{m.group(0)}'")
    return out
def main(a):
    if a[:1] == ["--install"]:
        src = os.path.abspath(a[1]); gd = subprocess.run(["git", "rev-parse", "--git-dir"], capture_output=True, text=True).stdout.strip()
        dst = os.path.join(gd, "re_banned.json"); shutil.copy(src, dst); me = os.path.abspath(__file__)
        for hook, cmd in (("pre-commit", f'git diff --cached -U0 | grep "^+" | python3 "{me}" --identity --banned-file "{dst}" --stdin "staged diff"'),
                          ("commit-msg", f'python3 "{me}" --identity --banned-file "{dst}" --files "$1"'),
                          ("pre-push", f'git log --format="%H %s%n%b" @{{u}}..HEAD 2>/dev/null | python3 "{me}" --identity --banned-file "{dst}" --stdin "commits to push"')):
            p = os.path.join(gd, "hooks", hook); open(p, "w").write("#!/bin/sh\n" + cmd + "\n"); os.chmod(p, 0o755)
        print("installed: pre-commit, commit-msg, pre-push (list copied inside .git, never committed)"); return 0
    # T-086 (2026-11-15): read every flag first, in any order. Before, --files swallowed everything after it, so
    # "--files x --identity" tried to open a file named "--identity" and crashed (exit 1, read as a finding).
    banned, texts, stdin_label, files, i = None, [], None, [], 0
    while i < len(a):
        if a[i] == "--banned-file" and i + 1 < len(a): banned = a[i + 1]; i += 2
        elif a[i] == "--text" and i + 1 < len(a): texts.append(a[i + 1]); i += 2
        elif a[i] == "--stdin" and i + 1 < len(a): stdin_label = a[i + 1]; i += 2
        elif a[i] == "--files":
            i += 1
            while i < len(a) and not a[i].startswith("--"): files.append(a[i]); i += 1
        else: i += 1  # --identity (read above) or anything unknown
    if banned is None: print("BLOCKED: no --banned-file"); return 2
    try: pats = load(banned)
    except (OSError, ValueError) as e: print(f"BLOCKED: banned list unreadable ({type(e).__name__})"); return 2
    found = []
    for t in texts: found += hits(pats, t, "text")
    if stdin_label is not None: found += hits(pats, sys.stdin.read(), stdin_label)
    for f in files:
        if os.path.isdir(f): continue
        if not os.path.exists(f): print(f"BLOCKED: file not found: {f}"); return 2
        found += hits(pats, open(f, errors="ignore").read(), f)
    for h in found: print("BLOCKED", h)
    print("CLEAN" if not found else f"BLOCKED: {len(found)} hit(s)"); return 1 if found else 0
if __name__ == "__main__": sys.exit(main(sys.argv[1:]))
