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
    pats, found, i = None, [], 0
    while i < len(a):
        if a[i] == "--banned-file": pats = load(a[i + 1]); i += 2
        elif a[i] == "--text": found += hits(pats, a[i + 1], "text"); i += 2
        elif a[i] == "--stdin": found += hits(pats, sys.stdin.read(), a[i + 1]); i += 2
        elif a[i] == "--files":
            for f in a[i + 1:]:
                try: found += hits(pats, open(f, errors="ignore").read(), f)
                except IsADirectoryError: pass
            break
        elif a[i] == "--identity": i += 1
        else: i += 1
    if pats is None: print("BLOCKED: no --banned-file"); return 2
    for h in found: print("BLOCKED", h)
    print("CLEAN" if not found else f"BLOCKED: {len(found)} hit(s)"); return 1 if found else 0
if __name__ == "__main__": sys.exit(main(sys.argv[1:]))
