#!/usr/bin/env python3
"""Check relative links and #anchors in Markdown files (GitHub slug rules).

Usage: md_links.py [--baseline FILE] --base <ref> | --all | FILE...
A baseline file lists known-broken links ("path: target" per line, '#' comments)
that are tolerated so the gate passes on main; remove lines as they get fixed.
Stale baseline entries are reported (not failed) so they get cleaned up.
"""
import os
import re
import sys
import unicodedata
from urllib.parse import unquote

sys.path.insert(0, os.path.dirname(__file__))
from mdcommon import files_from_args, iter_lines, report  # noqa: E402

LINK_RE = re.compile(r"(?<!!)\[(?:[^\]\\]|\\.)*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)|!\[[^\]]*\]\(\s*<?([^)\s>]+)>?[^)]*\)")
HEADING_RE = re.compile(r"^\s{0,3}(#{1,6})\s+(.*?)\s*#*\s*$")
HTML_ID_RE = re.compile(r"""<a\s+[^>]*(?:name|id)=["']([^"']+)["']""", re.I)
CODE_SPAN_RE = re.compile(r"`[^`]*`")


def slugify(heading):
    """GitHub heading slug: strip md formatting, lowercase, drop punctuation, spaces->'-'."""
    t = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", heading)
    t = t.replace("`", "")
    t = re.sub(r"<[^>]+>", "", t)
    t = t.strip().lower()
    out = []
    for ch in t:
        if ch.isalnum() or ch in "-_":
            out.append(ch)
        elif ch == " ":
            out.append("-")
        elif unicodedata.category(ch)[0] in "LNM":
            out.append(ch)
    return "".join(out)


_anchor_cache = {}


def anchors_of(path):
    if path in _anchor_cache:
        return _anchor_cache[path]
    seen, anchors = {}, set()
    try:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
    except OSError:
        text = ""
    for _, line, fenced in iter_lines(text):
        if fenced:
            continue
        m = HEADING_RE.match(line)
        if m:
            s = slugify(m.group(2))
            k = seen.get(s, 0)
            seen[s] = k + 1
            anchors.add(s if k == 0 else f"{s}-{k}")
        for h in HTML_ID_RE.findall(line):
            anchors.add(h)
    _anchor_cache[path] = anchors
    return anchors


def check_text(text, path, root="."):
    problems = []
    for n, line, fenced in iter_lines(text):
        if fenced:
            continue
        line = CODE_SPAN_RE.sub("", line)
        for m in LINK_RE.finditer(line):
            target = m.group(1) or m.group(2)
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("//"):
                continue
            file_part, _, frag = target.partition("#")
            file_part = unquote(file_part.split("?")[0])
            if file_part:
                dest = os.path.normpath(os.path.join(os.path.dirname(path), file_part))
                if file_part.startswith("/"):
                    dest = os.path.normpath(os.path.join(root, file_part.lstrip("/")))
                if not os.path.exists(dest):
                    problems.append((path, n, target, f"file not found: {dest}"))
                    continue
            else:
                dest = path
            if frag and dest.endswith(".md") and os.path.isfile(dest):
                if unquote(frag).lower() not in {a.lower() for a in anchors_of(dest)}:
                    problems.append((path, n, target, f"anchor '#{frag}' not found in {dest}"))
    return problems


def load_baseline(path):
    entries = set()
    if path and os.path.isfile(path):
        for l in open(path, encoding="utf-8"):
            l = l.strip()
            if l and not l.startswith("#"):
                entries.add(l)
    return entries


def main(argv):
    baseline = None
    if argv[:1] == ["--baseline"]:
        baseline, argv = argv[1], argv[2:]
    base = load_baseline(baseline)
    used, out = set(), []
    for f in files_from_args(argv):
        if not os.path.isfile(f):
            continue
        with open(f, encoding="utf-8") as fh:
            for path, n, target, why in check_text(fh.read(), f):
                key = f"{path}: {target}"
                if key in base:
                    used.add(key)
                else:
                    out.append(f"{path}:{n}: broken link '{target}' ({why})")
    for stale in sorted(base - used):
        print(f"note: baseline entry no longer needed or file not checked: {stale}")
    return report(out)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
