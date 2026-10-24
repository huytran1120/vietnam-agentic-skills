#!/usr/bin/env python3
"""Fail if SKILL.md (always-loaded agent router) exceeds its word budget.

Budget lives in scripts/ci/skill-budget.json. To raise it intentionally, edit
"max_words" in that file in the same PR and justify the growth in the PR
description (SKILL.md is loaded into every agent context).
Usage: skill_budget.py [CONFIG]
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def word_count(path):
    with open(path, encoding="utf-8") as fh:
        return len(fh.read().split())  # same as `wc -w`


def check(config_path):
    cfg = json.load(open(config_path, encoding="utf-8"))
    path = cfg["file"]  # relative to the repo root (cwd)
    n = word_count(path)
    if n > cfg["max_words"]:
        return [f"{cfg['file']} has {n} words, over the budget of {cfg['max_words']} "
                f"(+{n - cfg['max_words']}). It is loaded into every agent context: trim it, move detail "
                f"to docs/, or raise max_words in {os.path.relpath(config_path)} deliberately and justify it in the PR."]
    print(f"{cfg['file']}: {n} words (budget {cfg['max_words']})")
    return []


if __name__ == "__main__":
    probs = check(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "skill-budget.json"))
    for p in probs:
        print(p)
    sys.exit(1 if probs else 0)
