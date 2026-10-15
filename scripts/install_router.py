#!/usr/bin/env python3
"""Install the approved repository-local Plumbline router and activation guidance."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from install_agent_team import InstallReport, _ensure_lines, _git_dir, _write

ROUTER_PATH = Path(".agents/skills/plumbline-router/SKILL.md")
ROUTER_IGNORE = (".agents/skills/plumbline-router/",)
ROUTER_INCLUDE = (".agents/skills/plumbline-router/**",)
GUIDANCE_START = "<!-- plumbline:managed-router:start -->"
GUIDANCE_END = "<!-- plumbline:managed-router:end -->"
GUIDANCE = f"""{GUIDANCE_START}
When `.agents/skills/plumbline-router/SKILL.md` exists in this checkout, read and
follow it before ordinary repository work unless the user explicitly overrides
routing. Read the file even if `plumbline-router` is absent from the skill list.
If the file is absent, automatic Plumbline routing is off; do not recreate it
during ordinary work. Use explicit Plumbline initialization to restore approved
local setup in a new clone, remote checkout, or existing worktree.
{GUIDANCE_END}
"""


def routing_guidance(text: str) -> str:
    """Replace only the router's managed block, preserving repository instructions."""
    if GUIDANCE_START not in text and GUIDANCE_END not in text:
        return text.rstrip() + "\n\n" + GUIDANCE
    if text.count(GUIDANCE_START) != 1 or text.count(GUIDANCE_END) != 1:
        raise ValueError(
            "AGENTS.md has incomplete or duplicate Plumbline router markers"
        )
    start = text.index(GUIDANCE_START)
    end = text.index(GUIDANCE_END) + len(GUIDANCE_END)
    if end < start:
        raise ValueError("AGENTS.md has reversed Plumbline router markers")
    return text[:start] + GUIDANCE.rstrip("\n") + text[end:]


def install(
    plugin_root: Path,
    target_root: Path,
    replace: bool = False,
    *,
    propagate: bool = False,
    host: str = "codex",
    dry_run: bool = False,
) -> InstallReport:
    repo = target_root.resolve()
    if not repo.is_dir():
        raise ValueError(f"router target root does not exist: {repo}")
    has_git = (repo / ".git").exists()
    if propagate and not has_git:
        raise ValueError("router worktree propagation requires a Git checkout")
    git_dir = _git_dir(repo) if has_git else repo
    exclude = git_dir / "info/exclude" if has_git else repo / ".gitignore"
    if not exclude.resolve().is_relative_to(git_dir):
        raise ValueError("router ignore target escaped the Git directory")
    plugin = plugin_root.resolve()
    template = (plugin / "templates/router/SKILL.md").resolve()
    if not template.is_relative_to(plugin):
        raise ValueError("router template escaped the plugin root")
    router = repo / ROUTER_PATH
    agents = repo / "AGENTS.md"
    targets = [router, agents]
    if propagate:
        targets.extend((repo / ".gitignore", repo / ".worktreeinclude"))
    if host == "claude":
        targets.append(repo / "CLAUDE.md")
    elif host != "codex":
        raise ValueError(f"unsupported router host: {host}")
    for target in targets:
        if target.exists() and not target.is_file():
            raise ValueError(f"router setup target is not a file: {target}")
        if not target.resolve().is_relative_to(repo):
            raise ValueError(
                f"router setup target escaped the repository root: {target}"
            )
    if exclude.exists() and not exclude.is_file():
        raise ValueError(f"router ignore target is not a file: {exclude}")

    desired = template.read_text(encoding="utf-8")
    current = router.read_text(encoding="utf-8") if router.is_file() else None
    requires_replace = current is not None and current != desired and not replace
    if requires_replace and not dry_run:
        raise FileExistsError(
            f"{router} already differs; use --replace to overwrite it"
        )
    guidance = routing_guidance(
        agents.read_text(encoding="utf-8") if agents.is_file() else "# AGENTS.md\n"
    )

    changes: dict[Path, tuple[str, ...]] = {}
    operations: dict[Path, str] = {}
    for target, proposed, fields in (
        (router, desired, ("router template",)),
        (agents, guidance, ("conditional router activation guidance",)),
    ):
        existing = target.read_text(encoding="utf-8") if target.is_file() else None
        if existing != proposed:
            changes[target] = fields
            operations[target] = "modify" if target.exists() else "create"
            if not dry_run:
                _write(target, proposed)

    lines = [(exclude, ROUTER_IGNORE, "router ignore rules")]
    if propagate:
        lines.extend(
            (
                (repo / ".gitignore", ROUTER_IGNORE, "router ignore rules"),
                (
                    repo / ".worktreeinclude",
                    ROUTER_INCLUDE,
                    "router propagation manifest",
                ),
            )
        )
    if host == "claude":
        lines.append((repo / "CLAUDE.md", ("@AGENTS.md",), "shared guidance import"))
    for target, additions, label in lines:
        operation = "modify" if target.exists() else "create"
        if _ensure_lines(target, additions, apply=not dry_run):
            changes[target] = (label,)
            operations[target] = operation
    return InstallReport(
        changes, operations=operations, requires_replace=requires_replace
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root", type=Path, default=Path.cwd(), help="Target checkout root"
    )
    parser.add_argument(
        "--replace", action="store_true", help="Replace a differing router"
    )
    parser.add_argument(
        "--propagate",
        action="store_true",
        help="Prepare ignored-file propagation for local Codex-managed worktrees",
    )
    parser.add_argument("--host", choices=("codex", "claude"), default="codex")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview all setup changes without writing",
    )
    parser.add_argument(
        "--format", choices=("text", "json"), default="text", dest="output_format"
    )
    args = parser.parse_args()
    try:
        report = install(
            Path(__file__).resolve().parents[1],
            args.root,
            args.replace,
            propagate=args.propagate,
            host=args.host,
            dry_run=args.dry_run,
        )
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    payload = {
        "dry_run": args.dry_run,
        "writes_applied": not args.dry_run,
        "changes": [
            {
                "path": str(path),
                "operation": report.operations[path],
                "fields": list(fields),
                "requires_replace": report.requires_replace
                if path == args.root.resolve() / ROUTER_PATH
                else False,
            }
            for path, fields in report.changes.items()
        ],
        "requires_replace": report.requires_replace,
    }
    if args.output_format == "json":
        print(json.dumps(payload, indent=2))
    else:
        for change in payload["changes"]:
            print(
                f"{'Preview' if args.dry_run else 'Applied'}: {change['operation']} {change['path']}"
            )
        if report.requires_replace:
            print(
                "The existing router requires --replace before any changes can be applied."
            )
        if args.propagate:
            print(
                "Commit AGENTS.md, .gitignore, and .worktreeinclude for future local managed worktrees; existing/remote/manual worktrees need explicit setup."
            )
        print("Remove .agents/skills/plumbline-router/ to disable automatic routing.")


if __name__ == "__main__":
    main()
