#!/usr/bin/env python3
"""
Agent Skills Validator (Zero-Dependency)
Compliant with https://agentskills.io specification
"""

import sys
import os
import re
import unicodedata
from pathlib import Path

MAX_SKILL_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
MAX_COMPATIBILITY_LENGTH = 500

def parse_frontmatter(content: str):
    """Parse YAML frontmatter without external dependencies."""
    if not content.startswith("---"):
        raise ValueError("SKILL.md must start with YAML frontmatter (---)")
    
    parts = content.split("---", 2)
    if len(parts) < 3:
        raise ValueError("SKILL.md frontmatter not properly closed with ---")
    
    fm_str = parts[1]
    body = parts[2].strip()
    
    metadata = {}
    lines = fm_str.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue
        
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip()
            
            # Check multiline block scalar
            if val in (">-", ">", "|", "|-") or not val:
                desc_lines = []
                i += 1
                while i < len(lines) and (lines[i].startswith("  ") or not lines[i].strip()):
                    if lines[i].strip():
                        desc_lines.append(lines[i].strip())
                    i += 1
                metadata[key] = " ".join(desc_lines)
                continue
            elif val.startswith("[") and val.endswith("]"):
                metadata[key] = [v.strip().strip('"\'') for v in val[1:-1].split(",") if v.strip()]
            else:
                metadata[key] = val.strip('"\'')
        i += 1

    return metadata, body


def validate(skill_dir: Path) -> list:
    errors = []
    skill_dir = Path(skill_dir).resolve()
    
    if not skill_dir.exists():
        return [f"Path does not exist: {skill_dir}"]
    if not skill_dir.is_dir():
        return [f"Not a directory: {skill_dir}"]
    
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        skill_md = skill_dir / "skill.md"
    if not skill_md.exists():
        return ["Missing required file: SKILL.md"]
    
    try:
        content = skill_md.read_text(encoding="utf-8", errors="ignore")
        metadata, _ = parse_frontmatter(content)
    except Exception as e:
        return [f"Frontmatter parsing error: {e}"]
    
    # 1. Validate Name
    name = metadata.get("name")
    if not name or not isinstance(name, str) or not name.strip():
        errors.append("Field 'name' must be a non-empty string")
    else:
        name = unicodedata.normalize("NFKC", name.strip())
        if len(name) > MAX_SKILL_NAME_LENGTH:
            errors.append(f"Skill name '{name}' exceeds {MAX_SKILL_NAME_LENGTH} chars ({len(name)})")
        if name != name.lower():
            errors.append(f"Skill name '{name}' must be lowercase")
        if name.startswith("-") or name.endswith("-"):
            errors.append("Skill name cannot start or end with a hyphen")
        if "--" in name:
            errors.append("Skill name cannot contain consecutive hyphens")
        if not all(c.isalnum() or c == "-" for c in name):
            errors.append(f"Skill name '{name}' contains invalid characters (only letters, digits, single hyphens allowed)")
        if skill_dir.name != name:
            errors.append(f"Directory name '{skill_dir.name}' must match skill name '{name}'")
            
    # 2. Validate Description
    desc = metadata.get("description")
    if not desc or not isinstance(desc, str) or not desc.strip():
        errors.append("Field 'description' must be a non-empty string")
    elif len(desc) > MAX_DESCRIPTION_LENGTH:
        errors.append(f"Description exceeds {MAX_DESCRIPTION_LENGTH} chars ({len(desc)})")
        
    return errors


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate.py <path_to_skill_directory>")
        sys.exit(1)
        
    target_dir = Path(sys.argv[1])
    errors = validate(target_dir)
    
    if not errors:
        print(f"✓ Valid Agent Skill: {target_dir.name}")
        sys.exit(0)
    else:
        print(f"✗ Validation Failed for {target_dir.name}:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
