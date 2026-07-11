#!/usr/bin/env python3
"""Install the approved repository-local Plumbline router."""

from __future__ import annotations

import argparse
from pathlib import Path


def install(plugin_root: Path, target_root: Path, replace: bool = False) -> Path:
    template = (plugin_root / "templates" / "router" / "SKILL.md").resolve()
    repo = target_root.resolve()
    target = (repo / ".agents" / "skills" / "plumbline-router" / "SKILL.md").resolve()
    if template.parent.parent.parent != plugin_root.resolve():
        raise ValueError("plugin root is invalid")
    if not template.is_file():
        raise FileNotFoundError(template)
    if target.exists() and not replace:
        raise FileExistsError(f"{target} already exists; use --replace to overwrite it")
    if not target.is_relative_to(repo):
        raise ValueError("router target escaped the repository root")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(template.read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
    return target


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Target repository root")
    parser.add_argument("--replace", action="store_true", help="Replace an existing router")
    args = parser.parse_args()
    plugin_root = Path(__file__).resolve().parents[1]
    try:
        target = install(plugin_root, args.root, args.replace)
    except (FileExistsError, FileNotFoundError, ValueError) as exc:
        parser.error(str(exc))
    print(f"Installed repository-local router: {target}")
    print("Remove .agents/skills/plumbline-router/ to disable automatic routing.")


if __name__ == "__main__":
    main()
