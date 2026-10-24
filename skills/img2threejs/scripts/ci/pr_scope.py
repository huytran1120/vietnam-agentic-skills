#!/usr/bin/env python3
"""PR scope gate: the conventional-commit type in the PR title must match the diff.

Usage: pr_scope.py --title TITLE --base REF [--repo OWNER/NAME --pr N]
- `docs:` / `docs(scope):` PRs may only touch docs-like paths; otherwise FAIL.
- Stacked-PR warning (never fails): commits of this PR that also sit in another
  open PR's head. Uses `gh` read-only; skipped silently if unavailable.
"""
import fnmatch
import json
import re
import subprocess
import sys

TYPE_RE = re.compile(r"^\s*([a-zA-Z]+)(\([^)]*\))?(!)?:\s")
DOCS_PATTERNS = ["*.md", "docs/*", "assets/*", ".github/pull_request_template.md",
                 ".github/ISSUE_TEMPLATE/*", ".github/PULL_REQUEST_TEMPLATE/*"]


def commit_type(title):
    m = TYPE_RE.match(title or "")
    return m.group(1).lower() if m else None


def is_docs_path(path):
    return any(fnmatch.fnmatch(path, p) for p in DOCS_PATTERNS)


def scope_problems(title, files):
    if commit_type(title) != "docs":
        return []
    bad = [f for f in files if not is_docs_path(f)]
    if not bad:
        return []
    shown = "\n".join(f"  - {f}" for f in bad[:20])
    more = f"\n  ... and {len(bad) - 20} more" if len(bad) > 20 else ""
    return [f"PR title says 'docs' but the diff touches {len(bad)} non-docs file(s) "
            f"(of {len(files)} changed):\n{shown}{more}\n"
            "Allowed for docs PRs: *.md, docs/, assets/, PR/issue templates. "
            "Retitle (feat:/fix:/chore:) or split the non-docs changes into their own PR."]


def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True, check=True).stdout.splitlines()


def stacked_overlap(own_commits, others):
    """others: list of {number, commits:[oid]}; returns {number: [shared oids]}."""
    own = set(own_commits)
    res = {}
    for o in others:
        shared = sorted(own & set(o.get("commits", [])))
        if shared:
            res[o["number"]] = shared
    return res


def stacked_warnings(base, repo, pr):
    try:
        own = git("rev-list", f"{base}..HEAD")
        raw = subprocess.run(
            ["gh", "pr", "list", "--repo", repo, "--state", "open", "--limit", "100",
             "--json", "number,commits"],
            capture_output=True, text=True, check=True, timeout=60).stdout
        others = [{"number": p["number"], "commits": [c["oid"] for c in p["commits"]]}
                  for p in json.loads(raw) if str(p["number"]) != str(pr)]
    except Exception as e:  # gh missing, no token, API error: skip gracefully
        print(f"note: stacked-PR check skipped ({type(e).__name__})")
        return []
    return [f"::warning::possible stacked PR: {len(c)} commit(s) of this PR are also in open PR #{n} "
            f"(e.g. {c[0][:10]}). Target main with only your own commits, or wait for #{n} to merge."
            for n, c in stacked_overlap(own, others).items()]


def main(argv):
    a = dict(zip(argv[::2], argv[1::2]))
    title, base = a.get("--title", ""), a.get("--base", "origin/main")
    files = [f for f in git("diff", "--name-only", f"{base}...HEAD")]
    probs = scope_problems(title, files)
    if a.get("--repo") and a.get("--pr"):
        for w in stacked_warnings(base, a["--repo"], a["--pr"]):
            print(w)
    for p in probs:
        print(f"::error::{p}" if a.get("--gha") else p)
    print(f"type={commit_type(title)!r} files={len(files)} -> {'FAIL' if probs else 'ok'}")
    return 1 if probs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
