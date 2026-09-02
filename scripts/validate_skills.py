#!/usr/bin/env python3
"""Validate the repository's distributable Codex skill structure."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
NAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}$")


def frontmatter(text: str) -> dict[str, str] | None:
    if not text.startswith("---\n"):
        return None
    try:
        block = text.split("\n---\n", 1)[0].removeprefix("---\n")
    except IndexError:
        return None
    values: dict[str, str] = {}
    for line in block.splitlines():
        if ":" not in line:
            return None
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def main() -> int:
    errors: list[str] = []
    if not SKILLS.is_dir():
        errors.append("skills directory is missing")
    else:
        for directory in sorted(path for path in SKILLS.iterdir() if path.is_dir()):
            skill_file = directory / "SKILL.md"
            korean_file = directory / "SKILL.ko.md"
            if not skill_file.is_file():
                errors.append(f"{directory.relative_to(ROOT)}: SKILL.md is missing")
                continue
            if not korean_file.is_file():
                errors.append(f"{directory.relative_to(ROOT)}: SKILL.ko.md is missing")
                continue
            metadata = frontmatter(skill_file.read_text(encoding="utf-8"))
            korean_metadata = frontmatter(korean_file.read_text(encoding="utf-8"))
            if metadata is None:
                errors.append(f"{skill_file.relative_to(ROOT)}: invalid YAML frontmatter")
                continue
            if korean_metadata is None:
                errors.append(f"{korean_file.relative_to(ROOT)}: invalid YAML frontmatter")
                continue
            name = metadata.get("name", "")
            description = metadata.get("description", "")
            if name != directory.name:
                errors.append(f"{skill_file.relative_to(ROOT)}: name must equal folder name")
            if not NAME_PATTERN.fullmatch(name):
                errors.append(f"{skill_file.relative_to(ROOT)}: invalid skill name")
            if not description:
                errors.append(f"{skill_file.relative_to(ROOT)}: description is required")
            if korean_metadata.get("name", "") != name:
                errors.append(f"{korean_file.relative_to(ROOT)}: name must match SKILL.md")
            if not korean_metadata.get("description", ""):
                errors.append(f"{korean_file.relative_to(ROOT)}: description is required")
            if "[TODO" in skill_file.read_text(encoding="utf-8"):
                errors.append(f"{skill_file.relative_to(ROOT)}: unfinished TODO marker")
            if "[TODO" in korean_file.read_text(encoding="utf-8"):
                errors.append(f"{korean_file.relative_to(ROOT)}: unfinished TODO marker")

    if errors:
        print("Skill validation failed:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print("Skill validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
