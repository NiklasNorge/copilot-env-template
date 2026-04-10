#!/usr/bin/env python3
"""Validate project skill folders and basic SKILL.md metadata."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / ".github" / "skills"


def read_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        raise ValueError("missing opening frontmatter delimiter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("missing closing frontmatter delimiter")
    raw = text[4:end]
    body = text[end + 5 :]
    data: dict[str, str] = {}
    current_key: str | None = None
    block_mode = False
    list_mode = False
    block_lines: list[str] = []
    for line in raw.splitlines():
        if list_mode and line.startswith("  - "):
            block_lines.append(line[4:])
            continue
        if list_mode:
            data[current_key or ""] = ", ".join(block_lines).strip()
            current_key = None
            list_mode = False
            block_lines = []
        if block_mode and (line.startswith("  ") or line == ""):
            block_lines.append(line[2:] if line.startswith("  ") else "")
            continue
        if block_mode:
            data[current_key or ""] = "\n".join(block_lines).strip()
            current_key = None
            block_mode = False
            block_lines = []
        if not line.strip():
            continue
        if re.match(r"^[A-Za-z0-9_-]+:\s*>-$", line):
            current_key = line.split(":", 1)[0]
            block_mode = True
            block_lines = []
            continue
        if ":" not in line:
            raise ValueError(f"cannot parse frontmatter line: {line}")
        key, value = line.split(":", 1)
        if value.strip() == "":
            current_key = key.strip()
            list_mode = True
            block_lines = []
            continue
        data[key.strip()] = value.strip()
    if block_mode:
        data[current_key or ""] = "\n".join(block_lines).strip()
    if list_mode:
        data[current_key or ""] = ", ".join(block_lines).strip()
    return data, body


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    if not SKILLS_DIR.exists():
        print(f"skills directory not found: {SKILLS_DIR}")
        return 1

    for skill_dir in sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir()):
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            errors.append(f"{skill_dir.name}: missing SKILL.md")
            continue

        try:
            metadata, body = read_frontmatter(skill_md.read_text(encoding='utf-8'))
        except Exception as exc:
            errors.append(f"{skill_dir.name}: invalid frontmatter: {exc}")
            continue

        name = metadata.get("name", "").strip('"')
        description = metadata.get("description", "")

        if not name:
            errors.append(f"{skill_dir.name}: missing frontmatter name")
        elif name != skill_dir.name:
            errors.append(f"{skill_dir.name}: frontmatter name '{name}' does not match directory name")

        if not description:
            errors.append(f"{skill_dir.name}: missing description")

        if len(body.strip()) < 120:
            warnings.append(f"{skill_dir.name}: body is very short")

        has_assets = any(child.name != "SKILL.md" for child in skill_dir.iterdir())
        if not has_assets and metadata.get("disable-model-invocation", "").lower() != "true":
            warnings.append(f"{skill_dir.name}: no helper assets beyond SKILL.md")

    if errors:
        print("Skill validation failed:\n")
        for error in errors:
            print(f"- {error}")
        if warnings:
            print("\nWarnings:")
            for warning in warnings:
                print(f"- {warning}")
        return 1

    print("Skill validation passed.")
    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"- {warning}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
