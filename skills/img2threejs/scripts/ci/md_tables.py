#!/usr/bin/env python3
"""Detect GFM tables that will not render.

Usage: md_tables.py --base <ref> | --all | FILE...
Checks: rows starting with '||', empty/invalid delimiter cells, header vs
delimiter column-count mismatch.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from mdcommon import files_from_args, iter_lines, report  # noqa: E402

DELIM_CELL = re.compile(r"^\s*:?-+:?\s*$")


def split_row(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    return [c for c in re.split(r"(?<!\\)\|", s)]


def looks_like_delim(line):
    s = line.strip()
    return "|" in s and re.fullmatch(r"[\s|:\-]+", s) is not None and "-" in s


def check_text(text, name="<text>"):
    problems = []
    lines = list(iter_lines(text))
    for idx, (n, line, fenced) in enumerate(lines):
        if fenced:
            continue
        if line.lstrip().startswith("||"):
            problems.append(f"{name}:{n}: table row starts with '||' (renders as broken table); use a single '|'")
            continue
        if looks_like_delim(line) and idx > 0:
            pn, prev, pf = lines[idx - 1]
            if pf or "|" not in prev:
                continue
            cells = split_row(line)
            bad = [c for c in cells if not DELIM_CELL.match(c)]
            if bad:
                problems.append(f"{name}:{n}: delimiter row has empty/invalid cell(s) {bad!r}")
                continue
            if len(split_row(prev)) != len(cells):
                problems.append(f"{name}:{n}: header has {len(split_row(prev))} columns but delimiter row has {len(cells)}")
    return problems


def main(argv):
    problems = []
    for f in files_from_args(argv):
        if os.path.isfile(f):
            with open(f, encoding="utf-8") as fh:
                problems += check_text(fh.read(), f)
    return report(problems)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
