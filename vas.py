#!/usr/bin/env python3
"""
Vietnam Agentic Skills (VAS) - CLI & Antigravity Installer
Author: Huy Tran (https://github.com/huytran1120)
License: MIT

Zero-dependency tool to search, inspect, install, and manage 2,650+ agentic skills
specifically designed for Google Antigravity and AI coding agents. No npm/npx required.
"""

import sys
import os
import json
import shutil
import argparse
import re
from pathlib import Path

# ANSI colors
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'

    @classmethod
    def disable(cls):
        cls.HEADER = ''
        cls.BLUE = ''
        cls.CYAN = ''
        cls.GREEN = ''
        cls.YELLOW = ''
        cls.RED = ''
        cls.BOLD = ''
        cls.DIM = ''
        cls.RESET = ''

if not sys.stdout.isatty():
    Colors.disable()

# Base directories
REPO_ROOT = Path(__file__).resolve().parent
SKILLS_DIR = REPO_ROOT / "skills"
INDEX_FILE = REPO_ROOT / "skills_index.json"
MANIFEST_NAME = ".vas-manifest.json"

# Antigravity target paths
HOME = Path.home()
ANTIGRAVITY_WORKSPACE_TARGET = Path(".agents/skills")
ANTIGRAVITY_WORKSPACE_ALT = Path(".gemini/skills")
ANTIGRAVITY_GLOBAL_TARGET = HOME / ".gemini" / "antigravity" / "skills"
ANTIGRAVITY_GLOBAL_ALT = HOME / ".agents" / "skills"


def load_index():
    """Load skills index from skills_index.json with fallback to local scan."""
    if INDEX_FILE.exists():
        try:
            with open(INDEX_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"{Colors.YELLOW}Warning: Failed to read {INDEX_FILE}: {e}{Colors.RESET}", file=sys.stderr)
    return scan_skills_locally()


def scan_skills_locally():
    """Scan skills directory and build an in-memory index."""
    skills = []
    if not SKILLS_DIR.exists():
        return skills

    for entry in sorted(SKILLS_DIR.iterdir()):
        if entry.is_dir():
            skill_md = entry / "SKILL.md"
            if skill_md.exists():
                skill_id = entry.name
                metadata = extract_skill_metadata(skill_md, skill_id)
                skills.append(metadata)
            else:
                # Check for subdirectories (e.g. security/aws-compliance-checker)
                for subentry in sorted(entry.iterdir()):
                    if subentry.is_dir() and (subentry / "SKILL.md").exists():
                        sub_id = f"{entry.name}/{subentry.name}"
                        metadata = extract_skill_metadata(subentry / "SKILL.md", sub_id)
                        skills.append(metadata)
    return skills


def extract_skill_metadata(skill_md_path, skill_id):
    """Extract YAML frontmatter name and description from SKILL.md without external dependencies."""
    name = skill_id
    description = ""
    category = "general"
    tags = []
    risk = "safe"

    try:
        with open(skill_md_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read(8192)

        match = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
        if match:
            fm_text = match.group(1)
            lines = fm_text.splitlines()
            i = 0
            while i < len(lines):
                line = lines[i]
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    i += 1
                    continue

                if line.startswith("name:"):
                    name = line.split(":", 1)[1].strip().strip('"\'')
                elif line.startswith("category:"):
                    category = line.split(":", 1)[1].strip().strip('"\'')
                elif line.startswith("risk:"):
                    risk = line.split(":", 1)[1].strip().strip('"\'')
                elif line.startswith("description:"):
                    val = line.split(":", 1)[1].strip()
                    if val in (">-", ">", "|", "|-") or not val:
                        desc_lines = []
                        i += 1
                        while i < len(lines) and (lines[i].startswith("  ") or not lines[i].strip()):
                            if lines[i].strip():
                                desc_lines.append(lines[i].strip())
                            i += 1
                        description = " ".join(desc_lines)
                        continue
                    else:
                        description = val.strip('"\'')
                elif line.startswith("tags:"):
                    val = line.split(":", 1)[1].strip()
                    if val.startswith("[") and val.endswith("]"):
                        tags = [t.strip().strip('"\'') for t in val[1:-1].split(",") if t.strip()]
                    else:
                        tag_lines = []
                        i += 1
                        while i < len(lines) and lines[i].startswith("  "):
                            t_stripped = lines[i].strip()
                            if t_stripped.startswith("- "):
                                tag_lines.append(t_stripped[2:].strip().strip('"\''))
                            i += 1
                        tags = tag_lines
                        continue
                i += 1
    except Exception:
        pass

    return {
        "id": skill_id,
        "name": name,
        "path": str(skill_md_path.parent.relative_to(REPO_ROOT)),
        "description": description or "No description available",
        "category": category,
        "tags": tags,
        "risk": risk
    }


def resolve_target_dir(target_type, custom_path=None):
    """Determine the destination folder for Antigravity skills."""
    if custom_path:
        dest = Path(custom_path).resolve()
    elif target_type == "global":
        dest = ANTIGRAVITY_GLOBAL_TARGET
    elif target_type == "global-agents":
        dest = ANTIGRAVITY_GLOBAL_ALT
    elif target_type == "gemini":
        dest = ANTIGRAVITY_WORKSPACE_ALT.resolve()
    else:  # default "workspace"
        dest = ANTIGRAVITY_WORKSPACE_TARGET.resolve()

    dest.mkdir(parents=True, exist_ok=True)
    return dest


def load_manifest(dest_dir):
    """Load the installed skills manifest in the destination directory."""
    manifest_file = dest_dir / MANIFEST_NAME
    if manifest_file.exists():
        try:
            with open(manifest_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_manifest(dest_dir, manifest_data):
    """Save the installed skills manifest."""
    manifest_file = dest_dir / MANIFEST_NAME
    try:
        with open(manifest_file, "w", encoding="utf-8") as f:
            json.dump(manifest_data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"{Colors.YELLOW}Warning: Could not save manifest: {e}{Colors.RESET}", file=sys.stderr)


# CLI Subcommands

def cmd_search(args):
    """Search skills by keywords in id, name, description, category, tags."""
    query = args.query.lower().strip()
    skills = load_index()
    results = []

    for s in skills:
        score = 0
        s_id = s.get("id", "").lower()
        s_name = s.get("name", "").lower()
        s_desc = s.get("description", "").lower()
        s_cat = s.get("category", "").lower()
        s_tags = [t.lower() for t in s.get("tags", [])]

        if query == s_id:
            score += 100
        elif query in s_id:
            score += 50
        if query in s_name:
            score += 40
        if query == s_cat:
            score += 30
        elif query in s_cat:
            score += 15
        if query in s_tags:
            score += 25
        if query in s_desc:
            score += 10

        if score > 0:
            results.append((score, s))

    results.sort(key=lambda x: x[0], reverse=True)
    matched = [s for _, s in results]

    print(f"\n{Colors.BOLD}Found {len(matched)} matching skill(s) for '{query}':{Colors.RESET}\n")

    display_count = min(len(matched), args.limit)
    for i, s in enumerate(matched[:display_count], 1):
        s_id = s.get("id", "unknown")
        s_cat = s.get("category", "general")
        s_desc = s.get("description", "").replace("\n", " ")
        if len(s_desc) > 90:
            s_desc = s_desc[:87] + "..."

        print(f"  {Colors.CYAN}{i:2d}. {Colors.BOLD}{s_id}{Colors.RESET} [{Colors.YELLOW}{s_cat}{Colors.RESET}]")
        print(f"      {Colors.DIM}{s_desc}{Colors.RESET}")

    if len(matched) > display_count:
        print(f"\n  {Colors.DIM}... and {len(matched) - display_count} more. Use --limit to show more.{Colors.RESET}")
    print()


def cmd_list(args):
    """List skills with optional category or tag filtering."""
    skills = load_index()
    filtered = skills

    if args.category:
        cat = args.category.lower()
        filtered = [s for s in filtered if s.get("category", "").lower() == cat]

    if args.tag:
        tag = args.tag.lower()
        filtered = [s for s in filtered if tag in [t.lower() for t in s.get("tags", [])]]

    print(f"\n{Colors.BOLD}Listing skills ({len(filtered)} total){Colors.RESET}")
    if args.category:
        print(f"  Category: {Colors.YELLOW}{args.category}{Colors.RESET}")
    if args.tag:
        print(f"  Tag: {Colors.YELLOW}{args.tag}{Colors.RESET}")
    print()

    limit = args.limit if args.limit > 0 else len(filtered)
    for i, s in enumerate(filtered[:limit], 1):
        s_id = s.get("id", "unknown")
        s_cat = s.get("category", "general")
        s_desc = s.get("description", "").replace("\n", " ")
        if len(s_desc) > 80:
            s_desc = s_desc[:77] + "..."
        print(f"  {Colors.CYAN}{i:3d}. {Colors.BOLD}{s_id:<32}{Colors.RESET} [{Colors.YELLOW}{s_cat:<16}{Colors.RESET}] {Colors.DIM}{s_desc}{Colors.RESET}")

    if len(filtered) > limit:
        print(f"\n  {Colors.DIM}... and {len(filtered) - limit} more. Use --limit {len(filtered)} to show all.{Colors.RESET}")
    print()


def cmd_show(args):
    """Show detailed metadata and preview SKILL.md of a skill."""
    skill_id = args.skill_id.strip()
    skills = load_index()
    skill = next((s for s in skills if s.get("id") == skill_id), None)

    # Fallback to local directory check
    skill_dir = SKILLS_DIR / skill_id
    if not skill and skill_dir.is_dir():
        skill_md = skill_dir / "SKILL.md"
        if skill_md.exists():
            skill = extract_skill_metadata(skill_md, skill_id)

    if not skill:
        print(f"{Colors.RED}Skill '{skill_id}' not found.{Colors.RESET}", file=sys.stderr)
        sys.exit(1)

    print(f"\n{Colors.HEADER}======================================================================{Colors.RESET}")
    print(f"{Colors.BOLD}Skill:{Colors.RESET}        {Colors.GREEN}{skill.get('id')}{Colors.RESET}")
    print(f"{Colors.BOLD}Name:{Colors.RESET}         {skill.get('name', 'N/A')}")
    print(f"{Colors.BOLD}Category:{Colors.RESET}     {Colors.YELLOW}{skill.get('category', 'N/A')}{Colors.RESET}")
    print(f"{Colors.BOLD}Risk Level:{Colors.RESET}   {skill.get('risk', 'safe')}")
    print(f"{Colors.BOLD}Source:{Colors.RESET}       {skill.get('source', 'personal/community')}")
    print(f"{Colors.BOLD}Tags:{Colors.RESET}         {', '.join(skill.get('tags', [])) or 'None'}")
    print(f"{Colors.BOLD}Path:{Colors.RESET}         {skill.get('path', 'N/A')}")
    print(f"{Colors.BOLD}Description:{Colors.RESET}  {skill.get('description', 'N/A')}")
    print(f"{Colors.HEADER}======================================================================{Colors.RESET}\n")

    # Read SKILL.md preview
    skill_path = REPO_ROOT / skill.get("path", f"skills/{skill_id}")
    skill_md = skill_path / "SKILL.md" if skill_path.is_dir() else skill_path
    if not skill_md.exists() and (SKILLS_DIR / skill_id / "SKILL.md").exists():
        skill_md = SKILLS_DIR / skill_id / "SKILL.md"

    if skill_md.exists():
        print(f"{Colors.BOLD}Preview of {skill_md.name}:{Colors.RESET}\n")
        try:
            with open(skill_md, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
                preview_lines = lines[:40]
                for line in preview_lines:
                    print(f"  {line.rstrip()}")
                if len(lines) > 40:
                    print(f"\n  {Colors.DIM}... ({len(lines) - 40} lines remaining in full file) ...{Colors.RESET}")
        except Exception as e:
            print(f"  {Colors.RED}Could not read SKILL.md: {e}{Colors.RESET}")
    print()


def cmd_categories(args):
    """List all categories with skill counts."""
    skills = load_index()
    cats = {}
    for s in skills:
        c = s.get("category", "uncategorized")
        cats[c] = cats.get(c, 0) + 1

    sorted_cats = sorted(cats.items(), key=lambda x: x[1], reverse=True)
    print(f"\n{Colors.BOLD}Vietnam Agentic Skills Categories ({len(sorted_cats)} total):{Colors.RESET}\n")
    for cat, count in sorted_cats:
        print(f"  - {Colors.YELLOW}{cat:<24}{Colors.RESET} ({count:3d} skills)")
    print(f"\n{Colors.DIM}Filter with: ./vas list --category <name>{Colors.RESET}\n")


def cmd_tags(args):
    """List popular tags with skill counts."""
    skills = load_index()
    tags = {}
    for s in skills:
        for t in s.get("tags", []):
            tags[t] = tags.get(t, 0) + 1

    sorted_tags = sorted(tags.items(), key=lambda x: x[1], reverse=True)
    limit = args.limit if args.limit > 0 else 50
    print(f"\n{Colors.BOLD}Top Tags in Vietnam Agentic Skills (showing {min(limit, len(sorted_tags))} of {len(tags)}):{Colors.RESET}\n")
    for tag, count in sorted_tags[:limit]:
        print(f"  - {Colors.CYAN}{tag:<24}{Colors.RESET} ({count:3d} skills)")
    print(f"\n{Colors.DIM}Filter with: ./vas list --tag <tag>{Colors.RESET}\n")


def cmd_install(args):
    """Install skill(s) into Antigravity workspace or global configuration."""
    dest_dir = resolve_target_dir(args.target, args.dest)
    manifest = load_manifest(dest_dir)
    skills = load_index()
    skills_by_id = {s.get("id"): s for s in skills}

    targets_to_install = []

    if args.all:
        confirm = input(f"{Colors.RED}{Colors.BOLD}WARNING:{Colors.RESET} Installing all {len(skills)} skills into {dest_dir}? [y/N]: ")
        if confirm.lower() != 'y':
            print("Aborted.")
            return
        targets_to_install = list(skills_by_id.keys())
    elif args.category:
        cat = args.category.lower()
        matched = [s.get("id") for s in skills if s.get("category", "").lower() == cat]
        if not matched:
            print(f"{Colors.RED}No skills found in category '{args.category}'.{Colors.RESET}")
            return
        print(f"Selected {len(matched)} skill(s) in category '{args.category}'.")
        targets_to_install.extend(matched)
    elif args.tag:
        tag = args.tag.lower()
        matched = [s.get("id") for s in skills if tag in [t.lower() for t in s.get("tags", [])]]
        if not matched:
            print(f"{Colors.RED}No skills found with tag '{args.tag}'.{Colors.RESET}")
            return
        print(f"Selected {len(matched)} skill(s) with tag '{args.tag}'.")
        targets_to_install.extend(matched)
    elif args.skill_ids:
        targets_to_install.extend(args.skill_ids)
    else:
        print(f"{Colors.RED}Error: Provide skill ID(s), --category, --tag, or --all.{Colors.RESET}")
        return

    print(f"\n{Colors.BOLD}Installing {len(targets_to_install)} skill(s) to Antigravity:{Colors.RESET}")
    print(f"  Target: {Colors.CYAN}{dest_dir}{Colors.RESET}")
    print(f"  Mode:   {Colors.YELLOW}{args.mode}{Colors.RESET}\n")

    installed_count = 0
    for s_id in targets_to_install:
        s_id = s_id.strip()
        # Locate source skill directory
        source_dir = None
        if s_id in skills_by_id:
            rel_path = skills_by_id[s_id].get("path", f"skills/{s_id}")
            candidate = REPO_ROOT / rel_path
            if candidate.is_dir():
                source_dir = candidate

        if not source_dir:
            direct_candidate = SKILLS_DIR / s_id
            if direct_candidate.is_dir():
                source_dir = direct_candidate

        if not source_dir or not (source_dir / "SKILL.md").exists():
            print(f"  {Colors.RED}✗{Colors.RESET} Skill '{s_id}' not found or missing SKILL.md. Skipped.")
            continue

        target_skill_dir = dest_dir / source_dir.name
        # Remove existing if present
        if target_skill_dir.exists() or target_skill_dir.is_symlink():
            if target_skill_dir.is_symlink() or target_skill_dir.is_file():
                target_skill_dir.unlink()
            else:
                shutil.rmtree(target_skill_dir)

        try:
            if args.mode == "link":
                # Create relative symlink for portability, fallback to absolute
                try:
                    rel_target = os.path.relpath(source_dir.resolve(), target_skill_dir.parent.resolve())
                    os.symlink(rel_target, target_skill_dir)
                except ValueError:
                    os.symlink(source_dir.resolve(), target_skill_dir)
                mode_label = "linked"
            else:
                # Copy tree
                shutil.copytree(source_dir, target_skill_dir)
                mode_label = "copied"

            manifest[s_id] = {
                "installed_at": target_skill_dir.stat().st_mtime,
                "mode": args.mode,
                "source": str(source_dir.resolve()),
                "category": skills_by_id.get(s_id, {}).get("category", "general")
            }
            installed_count += 1
            print(f"  {Colors.GREEN}✓{Colors.RESET} {s_id} ({mode_label})")
        except Exception as e:
            print(f"  {Colors.RED}✗{Colors.RESET} Failed to install {s_id}: {e}")

    save_manifest(dest_dir, manifest)
    print(f"\n{Colors.GREEN}{Colors.BOLD}Done! Successfully installed {installed_count} skill(s) for Antigravity.{Colors.RESET}")
    print(f"{Colors.DIM}Antigravity will progressively discover these skills from {dest_dir}.{Colors.RESET}\n")


def cmd_uninstall(args):
    """Uninstall skill(s) from Antigravity workspace or global configuration."""
    dest_dir = resolve_target_dir(args.target, args.dest)
    manifest = load_manifest(dest_dir)

    to_remove = args.skill_ids
    if not to_remove:
        print(f"{Colors.RED}Specify skill ID(s) to uninstall.{Colors.RESET}")
        return

    print(f"\n{Colors.BOLD}Uninstalling from {dest_dir}:{Colors.RESET}\n")
    removed_count = 0
    for s_id in to_remove:
        target_skill_dir = dest_dir / s_id
        if target_skill_dir.exists() or target_skill_dir.is_symlink():
            try:
                if target_skill_dir.is_symlink() or target_skill_dir.is_file():
                    target_skill_dir.unlink()
                else:
                    shutil.rmtree(target_skill_dir)
                manifest.pop(s_id, None)
                removed_count += 1
                print(f"  {Colors.GREEN}✓{Colors.RESET} Removed {s_id}")
            except Exception as e:
                print(f"  {Colors.RED}✗{Colors.RESET} Error removing {s_id}: {e}")
        else:
            print(f"  {Colors.YELLOW}-{Colors.RESET} {s_id} is not installed in {dest_dir}")

    save_manifest(dest_dir, manifest)
    print(f"\n{Colors.GREEN}Removed {removed_count} skill(s).{Colors.RESET}\n")


def cmd_status(args):
    """Show currently installed skills in Antigravity."""
    dest_dir = resolve_target_dir(args.target, args.dest)
    manifest = load_manifest(dest_dir)

    print(f"\n{Colors.BOLD}Antigravity Skills Status in:{Colors.RESET} {Colors.CYAN}{dest_dir}{Colors.RESET}\n")

    # Detect skills on disk
    skills_on_disk = []
    if dest_dir.exists():
        for item in sorted(dest_dir.iterdir()):
            if item.is_dir() or item.is_symlink():
                if (item / "SKILL.md").exists() or item.name in manifest:
                    is_link = item.is_symlink()
                    skills_on_disk.append((item.name, is_link))

    if not skills_on_disk:
        print(f"  {Colors.YELLOW}No skills currently installed.{Colors.RESET}")
        print(f"  Install some with: ./vas install <skill_id> --target {args.target}")
    else:
        print(f"  Total installed: {Colors.GREEN}{len(skills_on_disk)}{Colors.RESET}\n")
        for name, is_link in skills_on_disk:
            tag = f"{Colors.BLUE}[symlink]{Colors.RESET}" if is_link else f"{Colors.YELLOW}[copied]{Colors.RESET}"
            cat = manifest.get(name, {}).get("category", "")
            cat_label = f"[{cat}]" if cat else ""
            print(f"  - {Colors.BOLD}{name:<32}{Colors.RESET} {tag} {Colors.DIM}{cat_label}{Colors.RESET}")
    print()


def cmd_init(args):
    """Initialize the current working directory as an Antigravity workspace with .agents/skills."""
    target_dir = Path(".agents/skills").resolve()
    target_dir.mkdir(parents=True, exist_ok=True)
    meta_skill_dir = target_dir / "vietnam-agentic-skills"
    meta_skill_dir.mkdir(parents=True, exist_ok=True)

    meta_skill_md = meta_skill_dir / "SKILL.md"
    content = f"""---
name: vietnam-agentic-skills
description: >-
  Use this skill to search, inspect, and install curated agentic skills from the
  Vietnam Agentic Skills (VAS) catalog into this Antigravity project.
---

# Vietnam Agentic Skills (VAS)

This workspace is enabled with Vietnam Agentic Skills catalog.

## Commands

Search skills:
`python3 {REPO_ROOT}/vas.py search <keyword>`

Install a skill to this workspace:
`python3 {REPO_ROOT}/vas.py install <skill_id> --target workspace`

List categories:
`python3 {REPO_ROOT}/vas.py categories`
"""
    with open(meta_skill_md, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\n{Colors.GREEN}{Colors.BOLD}✓ Antigravity workspace initialized!{Colors.RESET}")
    print(f"  Created: {Colors.CYAN}{target_dir}{Colors.RESET}")
    print(f"  Installed meta-skill: {Colors.BOLD}vietnam-agentic-skills{Colors.RESET}\n")


def cmd_sync(args):
    """Rebuild skills_index.json from the skills directory."""
    print(f"\n{Colors.BOLD}Scanning skills directory to rebuild index...{Colors.RESET}")
    scanned = scan_skills_locally()
    print(f"Scanned {len(scanned)} skills.")

    try:
        with open(INDEX_FILE, "w", encoding="utf-8") as f:
            json.dump(scanned, f, indent=2, ensure_ascii=False)
        print(f"{Colors.GREEN}✓ Successfully saved {INDEX_FILE}{Colors.RESET}\n")
    except Exception as e:
        print(f"{Colors.RED}✗ Error writing index: {e}{Colors.RESET}\n")


def cmd_antigravity_guide(args):
    """Print architectural guide on using VAS with Google Antigravity."""
    print(f"""
{Colors.HEADER}{Colors.BOLD}======================================================================
  Google Antigravity & Vietnam Agentic Skills (VAS) Guide
======================================================================{Colors.RESET}

{Colors.BOLD}1. How Antigravity Discovers Skills:{Colors.RESET}
   Antigravity scans skills progressively using hierarchical priority:
   - Priority 1: Workspace root `.agents/skills/<skill_name>/SKILL.md` (or `.gemini/skills/`)
   - Priority 2: Workspace declared configs `skills.json`
   - Priority 3: Global discovery `~/.gemini/antigravity/skills/` or `~/.gemini/config/skills/`
   - Priority 4: Built-in application skills

{Colors.BOLD}2. Progressive Disclosure in Antigravity:{Colors.RESET}
   Only the YAML frontmatter (`name` & `description`) is injected into the initial context.
   The full playbook is loaded into memory ONLY when Antigravity decides it is relevant.
   This allows you to keep thousands of skills available without bloating prompt tokens!

{Colors.BOLD}3. Common Workflows (Zero NPX):{Colors.RESET}
   - Search for a skill:
     {Colors.CYAN}./vas search security{Colors.RESET}
   - View details:
     {Colors.CYAN}./vas show 007{Colors.RESET}
   - Install to current workspace:
     {Colors.CYAN}./vas install 007 --target workspace --mode link{Colors.RESET}
   - Install to global Antigravity (available in all projects):
     {Colors.CYAN}./vas install docker-security --target global{Colors.RESET}
   - Batch install an entire category:
     {Colors.CYAN}./vas install --category ai-ml --target workspace{Colors.RESET}
   - Check installed skills:
     {Colors.CYAN}./vas status{Colors.RESET}
   - Remove a skill:
     {Colors.CYAN}./vas uninstall 007{Colors.RESET}

{Colors.HEADER}======================================================================{Colors.RESET}
""")


def main():
    parser = argparse.ArgumentParser(
        prog="vas",
        description="Vietnam Agentic Skills (VAS) - Catalog and Antigravity Installer"
    )
    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")

    # search
    p_search = subparsers.add_parser("search", help="Search skills by keyword")
    p_search.add_argument("query", help="Keyword to search for")
    p_search.add_argument("--limit", type=int, default=20, help="Max results to display (default: 20)")
    p_search.set_defaults(func=cmd_search)

    # list
    p_list = subparsers.add_parser("list", help="List skills with optional filters")
    p_list.add_argument("--category", "-c", help="Filter by category")
    p_list.add_argument("--tag", "-t", help="Filter by tag")
    p_list.add_argument("--limit", "-l", type=int, default=50, help="Max skills to show (default: 50)")
    p_list.set_defaults(func=cmd_list)

    # show / info
    p_show = subparsers.add_parser("show", aliases=["info"], help="Display skill details and preview")
    p_show.add_argument("skill_id", help="Exact skill ID")
    p_show.set_defaults(func=cmd_show)

    # categories
    p_cats = subparsers.add_parser("categories", help="List all skill categories")
    p_cats.set_defaults(func=cmd_categories)

    # tags
    p_tags = subparsers.add_parser("tags", help="List popular skill tags")
    p_tags.add_argument("--limit", type=int, default=50, help="Max tags to display")
    p_tags.set_defaults(func=cmd_tags)

    # install
    p_install = subparsers.add_parser("install", help="Install skills into Antigravity")
    p_install.add_argument("skill_ids", nargs="*", help="Skill ID(s) to install")
    p_install.add_argument("--target", choices=["workspace", "global", "global-agents", "gemini"], default="workspace",
                           help="Installation target (default: workspace -> .agents/skills)")
    p_install.add_argument("--mode", choices=["copy", "link"], default="link",
                           help="Installation mode: link (symlink, zero disk space, auto updates) or copy (default: link)")
    p_install.add_argument("--dest", help="Custom destination directory")
    p_install.add_argument("--category", "-c", help="Install all skills in this category")
    p_install.add_argument("--tag", "-t", help="Install all skills with this tag")
    p_install.add_argument("--all", action="store_true", help="Install ALL catalog skills")
    p_install.set_defaults(func=cmd_install)

    # uninstall / remove
    p_uninst = subparsers.add_parser("uninstall", aliases=["remove"], help="Uninstall skills from Antigravity")
    p_uninst.add_argument("skill_ids", nargs="+", help="Skill ID(s) to uninstall")
    p_uninst.add_argument("--target", choices=["workspace", "global", "global-agents", "gemini"], default="workspace")
    p_uninst.add_argument("--dest", help="Custom destination directory")
    p_uninst.set_defaults(func=cmd_uninstall)

    # status
    p_status = subparsers.add_parser("status", help="Show installed skills in Antigravity")
    p_status.add_argument("--target", choices=["workspace", "global", "global-agents", "gemini"], default="workspace")
    p_status.add_argument("--dest", help="Custom destination directory")
    p_status.set_defaults(func=cmd_status)

    # init
    p_init = subparsers.add_parser("init", help="Initialize workspace for Antigravity")
    p_init.set_defaults(func=cmd_init)

    # sync
    p_sync = subparsers.add_parser("sync", help="Rebuild skills_index.json")
    p_sync.set_defaults(func=cmd_sync)

    # guide
    p_guide = subparsers.add_parser("guide", help="Antigravity integration guide")
    p_guide.set_defaults(func=cmd_antigravity_guide)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
