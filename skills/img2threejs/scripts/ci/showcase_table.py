#!/usr/bin/env python3
"""Render the README demo table from the showcase gallery's demos.json.

Usage: showcase_table.py [--catalog URL|FILE] [--readme FILE] [--limit N] [--write | --check]
Lists the newest N demos whose status is final (the gallery's own order), between
<!-- showcase:start --> and <!-- showcase:end -->. Work in progress stays in the gallery only.
No flag prints the rendered table. --check exits 1 on drift; --write updates the file.
"""
import argparse
import json
import re
import sys
import urllib.request

from plugin_table import cell, replace_block

CATALOG_URL = "https://img2threejs.io/demos.json"
START, END = "<!-- showcase:start -->", "<!-- showcase:end -->"
LIMIT = 12
REQUIRED = ("id", "title", "subjectClass", "status", "updatedAt", "url", "sourceUrl")


def load_demos(src):
    if re.match(r"https?://", src):
        req = urllib.request.Request(src, headers={"User-Agent": "img2threejs-readme-sync"})
        with urllib.request.urlopen(req, timeout=30) as r:  # noqa: S310 (fixed https URL)
            data = json.load(r)
    else:
        with open(src, encoding="utf-8") as f:
            data = json.load(f)
    demos = data.get("demos") if isinstance(data, dict) else None
    if not isinstance(demos, list):
        raise ValueError("demos.json has no 'demos' list")
    for d in demos:
        for k in REQUIRED:
            if not d.get(k):
                raise ValueError(f"demo missing '{k}': {d.get('id', d)!r}")
    return demos


def render(demos, limit=LIMIT):
    final = [d for d in demos if d["status"] == "final"]
    final.sort(key=lambda d: d["updatedAt"], reverse=True)  # stable: keeps the gallery's order on ties
    rows = [
        "| Demo | Subject | Built with | View | Source |",
        "| --- | --- | --- | --- | --- |",
    ]
    for d in final[:limit]:
        version = f"`{d['version']}`" if d.get("version") else "—"
        rows.append(
            f"| {cell(d['title'])} | {cell(d['subjectClass'])} | {version} "
            f"| [Live]({d['url']}) | [code]({d['sourceUrl']}) |"
        )
    return "\n".join(rows)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--catalog", default=CATALOG_URL, help="demos.json URL or local file")
    ap.add_argument("--readme", default="README.md")
    ap.add_argument("--limit", type=int, default=LIMIT)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--write", action="store_true")
    g.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    try:
        table = render(load_demos(a.catalog), a.limit)
        with open(a.readme, encoding="utf-8") as f:
            old = f.read()
        new = replace_block(old, table, START, END)
    except (OSError, ValueError, json.JSONDecodeError) as e:
        print(f"showcase_table: {e}", file=sys.stderr)
        return 2
    if a.check:
        if new != old:
            print(f"{a.readme}: demo table differs from the gallery; run showcase_table.py --write")
            return 1
        print("demo table matches the gallery")
    elif a.write:
        if new != old:
            with open(a.readme, "w", encoding="utf-8") as f:
                f.write(new)
            print(f"{a.readme}: demo table updated")
        else:
            print("demo table already up to date")
    else:
        print(table)
    return 0


if __name__ == "__main__":
    sys.exit(main())
