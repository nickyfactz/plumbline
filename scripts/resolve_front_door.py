#!/usr/bin/env python3
"""Resolve Plumbline from skill paths advertised by the current host session."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def resolve_front_door(skill_paths: list[Path]) -> Path:
    """Validate one active installation; callers supply live catalog paths only."""
    roots: set[Path] = set()
    for path in skill_paths:
        skill = path.resolve(strict=True)
        if skill.name != "SKILL.md" or skill.parent.parent.name != "skills":
            raise ValueError(f"not a plugin skill path: {path}")
        root = skill.parent.parent.parent
        manifest = json.loads(
            (root / ".codex-plugin/plugin.json").read_text(encoding="utf-8")
        )
        if not isinstance(manifest, dict) or manifest.get("name") != "plumbline":
            raise ValueError(f"not a Plumbline installation: {root}")
        if (
            not isinstance(manifest.get("version"), str)
            or not manifest["version"]
            or manifest.get("skills") != "./skills/"
        ):
            raise ValueError(f"unsupported Plumbline manifest: {root}")
        roots.add(root)
    if len(roots) != 1:
        raise ValueError(
            "expected exactly one active Plumbline installation; refresh the host catalog"
        )
    root = roots.pop()
    front_door = (root / "skills/plumbline/SKILL.md").resolve(strict=True)
    if not front_door.is_relative_to(root):
        raise ValueError("Plumbline front door escaped the active installation")
    text = front_door.read_text(encoding="utf-8")
    header, separator, _body = text.partition("\n---")
    names = [
        line.partition(":")[2].strip().strip("\"'")
        for line in header.splitlines()
        if line.startswith("name:")
    ]
    if not text.startswith("---\n") or not separator or names != ["plumbline"]:
        raise ValueError("active front door has invalid skill metadata")
    return front_door


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-path", type=Path, action="append", required=True)
    args = parser.parse_args()
    try:
        print(resolve_front_door(args.skill_path))
    except (OSError, ValueError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
