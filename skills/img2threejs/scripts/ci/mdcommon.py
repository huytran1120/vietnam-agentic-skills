"""Shared helpers for the docs-quality gates (stdlib only)."""
import re
import subprocess
import sys

FENCE_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")


def iter_lines(text):
    """Yield (lineno, line, in_fence). Fence markers themselves count as in_fence."""
    fence = None
    for n, line in enumerate(text.splitlines(), 1):
        m = FENCE_RE.match(line)
        if fence is None:
            if m:
                fence = m.group(1)[0]
                yield n, line, True
                continue
            yield n, line, False
        else:
            yield n, line, True
            if m and m.group(1)[0] == fence and not line.strip().strip(fence):
                fence = None


def strip_frontmatter_lines(text):
    """Return text with a leading YAML front matter block blanked (line numbers kept)."""
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return "\n".join([""] * (i + 1) + lines[i + 1:])
    return text


def changed_files(base, pattern_suffix=".md"):
    out = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=ACMR", f"{base}...HEAD"],
        capture_output=True, text=True, check=True).stdout
    return [f for f in out.splitlines() if f.endswith(pattern_suffix)]


def files_from_args(argv):
    """argv: either explicit files, or `--base <ref>` to use the git diff."""
    if len(argv) >= 2 and argv[0] == "--base":
        return changed_files(argv[1])
    if argv == ["--all"]:
        out = subprocess.run(["git", "ls-files", "*.md"], capture_output=True,
                             text=True, check=True).stdout
        return out.splitlines()
    return argv


def report(problems):
    for p in problems:
        print(p)
    if problems:
        print(f"\n{len(problems)} problem(s) found.", file=sys.stderr)
    return 1 if problems else 0
