#!/usr/bin/env python3
"""Render the README plugin table from the img2 catalog.

Usage: plugin_table.py [--catalog URL|FILE] [--readme FILE] [--write | --check]
Replaces the text between <!-- plugins:start --> and <!-- plugins:end -->.
No flag prints the rendered table. --check exits 1 on drift; --write updates the file.
"""
import argparse
import json
import re
import sys
import urllib.request

CATALOG_URL = "https://raw.githubusercontent.com/img2threejs/img2/main/catalog.json"
START, END = "<!-- plugins:start -->", "<!-- plugins:end -->"
HEADER = ["Plugin / source README", "Adds", "Access", "Install after harness setup"]


def load_catalog(src):
    if re.match(r"https?://", src):
        with urllib.request.urlopen(src, timeout=30) as r:  # noqa: S310 (fixed https URL)
            data = json.load(r)
    else:
        with open(src, encoding="utf-8") as f:
            data = json.load(f)
    plugins = data.get("plugins") if isinstance(data, dict) else None
    if not isinstance(plugins, list):
        raise ValueError("catalog has no 'plugins' list")
    for p in plugins:
        for k in ("id", "description", "source", "access"):
            if not p.get(k):
                raise ValueError(f"catalog plugin missing '{k}': {p!r}")
    return plugins


def cell(text):
    return " ".join(str(text).split()).replace("|", "\\|")


def render(plugins):
    rows = [
        "| " + " | ".join(HEADER) + " |",
        "|---|---|---|---|",
    ]
    for p in sorted(plugins, key=lambda p: p["id"]):
        access = p["access"].capitalize()
        if p["access"] != "public":
            access = f"**{access} — authorized Git access required**"
        rows.append(
            f"| [{cell(p['id'])}](https://github.com/{p['source']}) | {cell(p['description'])} "
            f"| {access} | `img2 add {p['id']} --yes` |"
        )
    return "\n".join(rows)


def replace_block(text, table, start=START, end=END):
    i, j = text.find(start), text.find(end)
    if i < 0 or j < i:
        raise ValueError(f"README needs {start} ... {end} markers")
    return text[: i + len(start)] + "\n" + table + "\n" + text[j:]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--catalog", default=CATALOG_URL, help="catalog URL or local file")
    ap.add_argument("--readme", default="README.md")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--write", action="store_true")
    g.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    try:
        table = render(load_catalog(a.catalog))
        with open(a.readme, encoding="utf-8") as f:
            old = f.read()
        new = replace_block(old, table)
    except (OSError, ValueError, json.JSONDecodeError) as e:
        print(f"plugin_table: {e}", file=sys.stderr)
        return 2
    if a.check:
        if new != old:
            print(f"{a.readme}: plugin table differs from the catalog; run plugin_table.py --write")
            return 1
        print("plugin table matches the catalog")
    elif a.write:
        if new != old:
            with open(a.readme, "w", encoding="utf-8") as f:
                f.write(new)
            print(f"{a.readme}: plugin table updated")
        else:
            print("plugin table already up to date")
    else:
        print(table)
    return 0


if __name__ == "__main__":
    sys.exit(main())
