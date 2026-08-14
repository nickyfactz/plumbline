#!/usr/bin/env python3
"""Initialize, audit, or retune project-local Claude Code subagents."""

from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from pathlib import Path

from install_agent_team import (
    AGENT_GUIDANCE_END,
    AGENT_GUIDANCE_START,
    InstallReport,
    ROLE_DESCRIPTIONS,
    ROLES,
    _ensure_lines,
    _git_dir,
    _guidance_block_bounds,
    _guidance_has_markers,
    _repo_root,
    _replace_guidance_section,
    _write,
)


MODES = ("initialize", "audit", "retune")
AGENT_ROOT = Path(".claude") / "agents"
LOCAL_IGNORE_FILES = (".claude/agents/",)
WORKTREE_FILES = (".claude/agents/*.md",)
REQUIRED_FIELDS = ("name", "description", "model", "effort", "tools", "permissionMode")

ROLE_TOOLS = {
    "researcher": ("Read", "Glob", "Grep"),
    "backend-architect": ("Read", "Glob", "Grep"),
    "frontend-architect": ("Read", "Glob", "Grep"),
    "implementer": ("Read", "Glob", "Grep", "Edit", "Write", "Bash"),
    "qa-auditor": ("Read", "Glob", "Grep"),
}
ROLE_PERMISSION_MODES = {
    "researcher": "plan",
    "backend-architect": "plan",
    "frontend-architect": "plan",
    "implementer": "default",
    "qa-auditor": "plan",
}
CLAUDE_GUIDANCE_MARKERS = (
    AGENT_GUIDANCE_START,
    AGENT_GUIDANCE_END,
    ".claude/agents/",
    "main-mediated",
    "recommendations are advisory",
    "parallel wave",
    "delegation is the default",
    "delegation_roles",
    "delegation_status",
    "bounded research",
    "configured model",
)


def _template_data(plugin: Path, role: str) -> dict:
    path = plugin / "templates" / "agents" / f"{role}.toml"
    try:
        return tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise ValueError(f"invalid agent template: {path}: {exc}") from exc


def _yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _tools_value(tools: tuple[str, ...]) -> str:
    return "[" + ", ".join(_yaml_string(tool) for tool in tools) + "]"


def _body(plugin: Path, role: str) -> str:
    template = _template_data(plugin, role)
    return (
        str(template["developer_instructions"]).strip()
        + "\n"
        + "This is a project-local Claude Code subagent. Use only the tools listed above. "
        + "Never invoke the Agent tool or spawn child agents. Return all results to the main thread. "
        + "Recommendations are advisory; never hand off to or dispatch another worker."
    )


def _render_agent(plugin: Path, role: str, model: str, effort: str) -> str:
    template = _template_data(plugin, role)
    lines = [
        "---",
        f"name: {role}",
        f"description: {_yaml_string(str(template['description']))}",
        f"tools: {_tools_value(ROLE_TOOLS[role])}",
        f"model: {_yaml_string(model)}",
        f"permissionMode: {ROLE_PERMISSION_MODES[role]}",
        f"effort: {effort}",
        "---",
        "",
        _body(plugin, role),
        "",
    ]
    return "\n".join(lines)


def _frontmatter(text: str, path: Path) -> tuple[list[str], int, dict[str, object], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{path}: missing YAML frontmatter")
    try:
        closing = next(index for index in range(1, len(lines)) if lines[index].strip() == "---")
    except StopIteration as exc:
        raise ValueError(f"{path}: unterminated YAML frontmatter") from exc

    values: dict[str, object] = {}
    for line in lines[1:closing]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = re.match(r"^([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$", line)
        if not match:
            continue
        key, raw = match.groups()
        raw = raw.strip()
        if raw.startswith("[") and raw.endswith("]"):
            values[key] = [item.strip().strip("\"'") for item in raw[1:-1].split(",") if item.strip()]
        elif len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "\"'":
            values[key] = raw[1:-1]
        else:
            values[key] = raw
    body = "\n".join(lines[closing + 1:]).strip("\n")
    return lines, closing, values, body


def _yaml_value(value: object) -> str:
    if isinstance(value, (list, tuple)):
        return "[" + ", ".join(_yaml_string(str(item)) for item in value) + "]"
    return _yaml_string(str(value))


def _replace_body(text: str, body: str, path: Path) -> str:
    lines, closing, _values, _old_body = _frontmatter(text, path)
    return "\n".join(lines[: closing + 1]) + "\n\n" + body.strip("\n") + "\n"


def _append_missing_fields(text: str, missing: dict[str, object], path: Path) -> str:
    if not missing:
        return text
    lines, closing, _values, _body_text = _frontmatter(text, path)
    additions = [f"{key}: {_yaml_value(value)}" for key, value in missing.items()]
    return "\n".join(lines[:closing] + additions + lines[closing:]) + "\n"


def _validate_agent(path: Path, role: str, text: str) -> list[str]:
    try:
        _lines, _closing, values, body = _frontmatter(text, path)
    except ValueError as exc:
        return [str(exc)]
    findings = []
    for field in REQUIRED_FIELDS:
        if field not in values or not str(values[field]).strip():
            findings.append(f"{path}: missing required field {field}")
    if values.get("name") not in (None, role):
        findings.append(f"{path}: name is {values['name']!r}, expected {role!r}")
    tools = values.get("tools", [])
    if "Agent" in tools:
        findings.append(f"{path}: Agent tool would permit child delegation")
    if "spawn child" not in body.lower():
        findings.append(f"{path}: missing no-child boundary")
    if "main thread" not in body.lower() or "dispatch another worker" not in body.lower():
        findings.append(f"{path}: missing main-mediated delegation boundary")
    return findings


def _guidance(roles: tuple[str, ...]) -> str:
    role_lines = "\n".join(f"- `{role}` for {ROLE_DESCRIPTIONS[role]}." for role in roles)
    return f"""{AGENT_GUIDANCE_START}
## Local Claude agent team

Use only the approved project-local Claude Code subagents under `.claude/agents/` for bounded work that a role can own:

{role_lines}

The main thread owns product decisions, active specifications and plans, integration, and Git. Give subagents anchored briefs and disjoint write sets. Researcher, architect, and QA roles are report-only and receive no write set; their `permissionMode = plan` and restricted tools are intent, while the parent permission context can take precedence. Each write-capable role receives only its approved bounded write set. Delegation is main-mediated: every worker returns to the main thread, worker recommendations are advisory, and only the main thread selects and dispatches the next capability. Subagents never invoke the Agent tool or spawn children. When independent work is ready, the main thread may dispatch one parallel wave only with a stable contract, disjoint scopes, no result dependency, and a clear join condition; otherwise keep it serial. For Execute checkpoints, delegation is the default: when an approved project-local role can own useful bounded research, architecture, implementation, review, testing, or another capability with a clear boundary, dispatch that role before the main thread duplicates the work. Use its configured model, effort, and permission intent; do not invent or substitute a personal/global role. Record `delegation_roles` and `delegation_status` in the checkpoint resume record and restore them after compaction. Keep product decisions, lifecycle/plan state, joins, integration, Git, singleton operations, or tiny coupled actions on the main thread; otherwise a missing role is an explicit `Direct: <reason>` fallback. Report each delegation wave with role names, configured model values, effort values, and the report-only/no-write-set/no-child boundary. Claude model and effort choices are host-native starting points and remain adjustable; do not copy Codex model slugs into these files. Plumbline does not edit global Claude settings or enable experimental Agent Teams.
{AGENT_GUIDANCE_END}
"""


def _prepare_guidance(
    repo: Path,
    roles: tuple[str, ...],
    *,
    refresh: bool = False,
    replace_guidance: bool = False,
) -> tuple[Path, str, bool, str | None]:
    target = repo / "AGENTS.md"
    text = target.read_text(encoding="utf-8") if target.is_file() else "# AGENTS.md\n"
    section = _guidance_block_bounds(text, "## Local Claude agent team")
    if not section:
        return target, text.rstrip() + "\n\n" + _guidance(roles), False, None
    if not refresh:
        return target, text, False, None
    replacement = _guidance(roles)
    has_managed_markers = _guidance_has_markers(text, "## Local Claude agent team")
    if not has_managed_markers and not replace_guidance:
        proposed = _replace_guidance_section(text, "## Local Claude agent team", replacement)
        return (
            target,
            proposed,
            True,
            f"{target}: existing Claude guidance is an unmarked legacy section; previewed refresh requires --replace-agents-guidance",
        )
    return target, _replace_guidance_section(text, "## Local Claude agent team", replacement), False, None


def _audit(repo: Path, roles: tuple[str, ...]) -> InstallReport:
    findings: list[str] = []
    for role in roles:
        path = repo / AGENT_ROOT / f"{role}.md"
        if not path.exists():
            findings.append(f"{path}: missing project-local Claude role")
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            findings.append(f"{path}: could not read role: {exc}")
            continue
        findings.extend(_validate_agent(path, role, text))
    guidance = repo / "AGENTS.md"
    if not guidance.is_file():
        findings.append(f"{guidance}: missing `## Local Claude agent team` guidance")
    else:
        text = guidance.read_text(encoding="utf-8")
        section = _guidance_block_bounds(text, "## Local Claude agent team")
        if not section:
            findings.append(f"{guidance}: missing `## Local Claude agent team` guidance")
        else:
            section_text = text[section[0] : section[1]]
            findings.extend(
                f"{guidance}: Local Claude agent-team guidance missing marker {marker!r}"
                for marker in CLAUDE_GUIDANCE_MARKERS
                if marker not in section_text
            )
    return InstallReport({}, tuple(findings))


def _refresh_guidance(
    repo: Path,
    roles: tuple[str, ...],
    *,
    replace_guidance: bool,
    dry_run: bool,
) -> InstallReport:
    target, proposed, requires_replace, finding = _prepare_guidance(
        repo,
        roles,
        refresh=True,
        replace_guidance=replace_guidance,
    )
    if requires_replace and not dry_run:
        raise ValueError(finding or f"{target} requires explicit guidance replacement approval")
    current = target.read_text(encoding="utf-8") if target.is_file() else ""
    changes: dict[Path, tuple[str, ...]] = {}
    operations: dict[Path, str] = {}
    findings = [finding] if finding else []
    if current != proposed:
        changes[target] = ("local Claude agent-team guidance",)
        operations[target] = "modify" if target.exists() else "create"
        if not dry_run:
            _write(target, proposed)
    return InstallReport(changes, tuple(findings), operations, requires_replace=requires_replace)


def _retune(
    plugin: Path,
    repo: Path,
    roles: tuple[str, ...],
    *,
    model: str,
    effort: str,
    fill_missing: bool,
    update_instructions: bool,
    dry_run: bool,
) -> InstallReport:
    changes: dict[Path, tuple[str, ...]] = {}
    operations: dict[Path, str] = {}
    findings: list[str] = []
    for role in roles:
        path = repo / AGENT_ROOT / f"{role}.md"
        if not path.exists():
            findings.append(f"{path}: missing project-local Claude role; initialize it instead")
            continue
        try:
            before = path.read_text(encoding="utf-8")
            _lines, _closing, values, _body_text = _frontmatter(before, path)
        except (OSError, ValueError) as exc:
            findings.append(str(exc))
            continue

        after = before
        changed: list[str] = []
        if fill_missing:
            template = _template_data(plugin, role)
            defaults = {
                "name": role,
                "description": str(template["description"]),
                "model": model,
                "effort": effort,
                "tools": ROLE_TOOLS[role],
                "permissionMode": ROLE_PERMISSION_MODES[role],
            }
            missing = {key: value for key, value in defaults.items() if key not in values}
            after = _append_missing_fields(after, missing, path)
            changed.extend(missing)
        if update_instructions:
            updated = _replace_body(after, _body(plugin, role), path)
            if updated != after:
                after = updated
                changed.append("instructions")
        findings.extend(_validate_agent(path, role, after))
        if changed:
            if not dry_run:
                _write(path, after)
            changes[path] = tuple(dict.fromkeys(changed))
            operations[path] = "modify"
    return InstallReport(changes, tuple(findings), operations)


def _initialize(
    plugin: Path,
    repo: Path,
    roles: tuple[str, ...],
    *,
    model: str,
    effort: str,
    replace: bool,
    update_agents: bool,
    refresh_agents: bool,
    replace_guidance: bool,
    propagate: bool,
    dry_run: bool,
) -> InstallReport:
    for role in roles:
        target = repo / AGENT_ROOT / f"{role}.md"
        if target.exists() and not replace:
            raise FileExistsError(f"Claude role already exists; audit or retune it before replacing: {target}")

    changes: dict[Path, tuple[str, ...]] = {}
    operations: dict[Path, str] = {}
    for role in roles:
        target = repo / AGENT_ROOT / f"{role}.md"
        existed = target.exists()
        if not dry_run:
            _write(target, _render_agent(plugin, role, model, effort))
        changes[target] = ("name", "description", "model", "effort", "tools", "permissionMode", "instructions")
        operations[target] = "modify" if existed else "create"

    exclude = _git_dir(repo) / "info" / "exclude"
    if _ensure_lines(exclude, LOCAL_IGNORE_FILES, apply=not dry_run):
        changes[exclude] = ("ignore rules",)
        operations[exclude] = "modify" if exclude.exists() else "create"

    if update_agents:
        target, text, requires_replace, finding = _prepare_guidance(
            repo,
            roles,
            refresh=refresh_agents,
            replace_guidance=replace_guidance,
        )
        if requires_replace and not dry_run:
            raise ValueError(finding or f"{target} requires explicit guidance replacement approval")
        current = target.read_text(encoding="utf-8") if target.is_file() else ""
        if current != text:
            if not dry_run:
                _write(target, text)
            changes[target] = ("local Claude agent-team guidance",)
            operations[target] = "modify" if target.exists() else "create"
        if finding:
            findings = [finding]
        else:
            findings = []
    else:
        findings = []

    if propagate:
        manifest = repo / ".worktreeinclude"
        if _ensure_lines(manifest, WORKTREE_FILES, apply=not dry_run):
            changes[manifest] = ("Claude agent propagation manifest",)
            operations[manifest] = "modify" if manifest.exists() else "create"
        gitignore = repo / ".gitignore"
        if _ensure_lines(gitignore, LOCAL_IGNORE_FILES, apply=not dry_run):
            changes[gitignore] = ("Claude agent ignore rules",)
            operations[gitignore] = "modify" if gitignore.exists() else "create"
    return InstallReport(changes, tuple(findings), operations, requires_replace=requires_replace if update_agents else False)


def install(
    plugin_root: Path,
    target_root: Path,
    *,
    mode: str = "initialize",
    model: str = "inherit",
    effort: str = "medium",
    roles: tuple[str, ...] = ROLES,
    replace: bool = False,
    fill_missing: bool = False,
    update_instructions: bool = False,
    update_agents: bool = False,
    refresh_agents: bool = False,
    replace_guidance: bool = False,
    propagate: bool = False,
    dry_run: bool = False,
) -> InstallReport:
    if mode not in MODES:
        raise ValueError(f"mode must be one of: {', '.join(MODES)}")
    if not roles or len(set(roles)) != len(roles) or any(role not in ROLES for role in roles):
        raise ValueError(f"roles must be selected from: {', '.join(ROLES)}")
    repo = _repo_root(target_root)
    plugin = plugin_root.resolve()
    if mode == "audit":
        if any((replace, fill_missing, update_instructions, update_agents, refresh_agents, replace_guidance, propagate)):
            raise ValueError("audit is read-only; remove mutation flags")
        return _audit(repo, roles)
    if mode == "retune":
        if replace or update_agents or refresh_agents or replace_guidance or propagate:
            raise ValueError("retune preserves existing roles; use initialize for replacement, guidance, or propagation")
        return _retune(
            plugin,
            repo,
            roles,
            model=model,
            effort=effort,
            fill_missing=fill_missing,
            update_instructions=update_instructions,
            dry_run=dry_run,
        )
    if refresh_agents:
        if not update_agents:
            raise ValueError("--refresh-agents requires --update-agents")
        if replace or propagate:
            raise ValueError("--refresh-agents is a guidance-only initialization update; remove role/worktree mutation flags")
        return _refresh_guidance(repo, roles, replace_guidance=replace_guidance, dry_run=dry_run)
    if replace_guidance:
        raise ValueError("--replace-agents-guidance requires --refresh-agents")
    if fill_missing or update_instructions:
        raise ValueError("initialize creates templates; use retune for preserve-existing updates")
    return _initialize(
        plugin,
        repo,
        roles,
        model=model,
        effort=effort,
        replace=replace,
        update_agents=update_agents,
        refresh_agents=refresh_agents,
        replace_guidance=replace_guidance,
        propagate=propagate,
        dry_run=dry_run,
    )


def _parse_roles(value: str) -> tuple[str, ...]:
    roles = tuple(item.strip() for item in value.split(",") if item.strip())
    if not roles or len(set(roles)) != len(roles) or any(role not in ROLES for role in roles):
        raise argparse.ArgumentTypeError(f"choose unique roles from: {', '.join(ROLES)}")
    return roles


def _print_report(mode: str, report: InstallReport, *, dry_run: bool, output_format: str) -> None:
    changes = [
        {
            "path": str(path),
            "operation": report.operations.get(path, "modify"),
            "fields": list(fields),
        }
        for path, fields in report.changes.items()
    ]
    payload = {
        "host": "claude",
        "mode": mode,
        "dry_run": dry_run,
        "writes_applied": not dry_run and mode != "audit",
        "changes": changes,
        "findings": list(report.findings),
        "requires_replace": report.requires_replace,
        "global_agents_selected": False,
        "claude_settings_modified": False,
        "experimental_agent_teams_enabled": False,
    }
    if output_format == "json":
        print(json.dumps(payload, indent=2))
        return
    print(f"Plumbline Claude agent-team {mode} {'preview' if dry_run else 'complete'}.")
    for change in changes:
        print(f"{change['operation'].title()} {change['path']}: {', '.join(change['fields'])}")
    for finding in report.findings:
        print(f"Finding: {finding}")
    if report.requires_replace:
        print("Approval required: rerun with --replace-agents-guidance after reviewing the proposed AGENTS.md refresh.")
    if mode == "audit":
        print("Audit was read-only; no files were written.")
    print("Global Claude settings and experimental Agent Teams were not changed.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Target repository root")
    parser.add_argument("--mode", choices=MODES, default="initialize")
    parser.add_argument("--model", default="inherit", help="Claude model alias or full model ID")
    parser.add_argument("--effort", "--reasoning-effort", dest="effort", default="medium")
    parser.add_argument("--roles", type=_parse_roles, default=ROLES, help="Comma-separated roles")
    parser.add_argument("--replace", action="store_true", help="Replace existing role files during initialize only")
    parser.add_argument("--fill-missing", action="store_true", help="Retune by adding missing frontmatter only")
    parser.add_argument("--update-instructions", action="store_true", help="Retune by explicitly updating instructions")
    parser.add_argument("--update-agents", action="store_true", help="Add the approved AGENTS.md section")
    parser.add_argument(
        "--refresh-agents",
        action="store_true",
        help="During an explicit initialization rerun, refresh only the managed AGENTS.md section",
    )
    parser.add_argument(
        "--replace-agents-guidance",
        action="store_true",
        help="Allow explicit replacement of a stale unmarked AGENTS.md team section",
    )
    parser.add_argument("--propagate", action="store_true", help="Add ignored-file worktree propagation")
    parser.add_argument("--dry-run", action="store_true", help="Preview exact changes without writing files")
    parser.add_argument("--format", choices=("text", "json"), default="text", dest="output_format")
    args = parser.parse_args()
    plugin_root = Path(__file__).resolve().parents[1]
    try:
        report = install(
            plugin_root,
            args.root,
            mode=args.mode,
            model=args.model,
            effort=args.effort,
            roles=args.roles,
            replace=args.replace,
            fill_missing=args.fill_missing,
            update_instructions=args.update_instructions,
            update_agents=args.update_agents,
            refresh_agents=args.refresh_agents,
            replace_guidance=args.replace_agents_guidance,
            propagate=args.propagate,
            dry_run=args.dry_run,
        )
    except (FileExistsError, OSError, ValueError) as exc:
        parser.error(str(exc))
    _print_report(args.mode, report, dry_run=args.dry_run, output_format=args.output_format)
    return 0


if __name__ == "__main__":
    sys.exit(main())
