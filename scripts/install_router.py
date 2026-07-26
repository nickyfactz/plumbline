#!/usr/bin/env python3
"""Install the approved repository-local Plumbline router."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def install(
    plugin_root: Path,
    target_root: Path,
    replace: bool = False,
    *,
    dry_run: bool = False,
) -> Path:
    template = (plugin_root / "templates" / "router" / "SKILL.md").resolve()
    repo = target_root.resolve()
    target = (repo / ".agents" / "skills" / "plumbline-router" / "SKILL.md").resolve()
    if template.parent.parent.parent != plugin_root.resolve():
        raise ValueError("plugin root is invalid")
    if not template.is_file():
        raise FileNotFoundError(template)
    if target.exists() and not replace and not dry_run:
        raise FileExistsError(f"{target} already exists; use --replace to overwrite it")
    if not target.is_relative_to(repo):
        raise ValueError("router target escaped the repository root")
    if not dry_run:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(template.read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
    return target


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Target repository root")
    parser.add_argument("--replace", action="store_true", help="Replace an existing router")
    parser.add_argument("--dry-run", action="store_true", help="Preview the exact router change without writing")
    parser.add_argument("--format", choices=("text", "json"), default="text", dest="output_format")
    args = parser.parse_args()
    plugin_root = Path(__file__).resolve().parents[1]
    target = (args.root.resolve() / ".agents" / "skills" / "plumbline-router" / "SKILL.md").resolve()
    template = (plugin_root / "templates" / "router" / "SKILL.md").resolve()
    existing = target.is_file()
    matches_template = existing and target.read_text(encoding="utf-8") == template.read_text(encoding="utf-8")
    operation = "none" if matches_template else ("modify" if target.exists() else "create")
    requires_replace = target.exists() and not matches_template and not args.replace
    try:
        target = install(plugin_root, args.root, args.replace, dry_run=args.dry_run)
    except (FileExistsError, FileNotFoundError, ValueError) as exc:
        parser.error(str(exc))
    if args.output_format == "json":
        print(
            json.dumps(
                {
                    "dry_run": args.dry_run,
                    "writes_applied": not args.dry_run,
                    "changes": []
                    if operation == "none"
                    else [
                        {
                            "path": str(target),
                            "operation": operation,
                            "fields": ["router template"],
                            "requires_replace": requires_replace,
                        }
                    ],
                    "requires_replace": requires_replace,
                },
                indent=2,
            )
        )
        return
    if args.dry_run:
        suffix = " (existing copy; --replace is required to apply)" if requires_replace else ""
        message = "matches the current template" if operation == "none" else "would update"
        print(f"Preview: repository-local router {message}: {target}{suffix}")
    else:
        print(f"Installed repository-local router: {target}")
    print("Remove .agents/skills/plumbline-router/ to disable automatic routing.")


if __name__ == "__main__":
    main()
