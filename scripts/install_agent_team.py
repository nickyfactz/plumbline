#!/usr/bin/env python3
"""Initialize, audit, or retune a project-local Plumbline agent team."""

from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path


ROLES = (
    "researcher",
    "backend-architect",
    "frontend-architect",
    "implementer",
    "qa-auditor",
)
MODES = ("initialize", "audit", "retune")
SANDBOXES = {
    "researcher": "read-only",
    "backend-architect": "read-only",
    "frontend-architect": "read-only",
    "implementer": "workspace-write",
    "qa-auditor": "read-only",
}
REQUIRED_AGENT_FIELDS = (
    "name",
    "description",
    "developer_instructions",
    "model",
    "model_reasoning_effort",
    "sandbox_mode",
)
CONFIG_FIELDS = (
    "features.multi_agent",
    "agents.max_threads",
    "agents.max_depth",
)
WORKTREE_FILES = (
    ".codex/config.toml",
    ".codex/agents/*.toml",
    ".agents/skills/plumbline-router/**",
)
LOCAL_IGNORE_FILES = (
    ".codex/",
    ".agents/skills/plumbline-router/",
)
ROUTER_RELATIVE_PATH = ".agents/skills/plumbline-router/SKILL.md"
ROLE_DESCRIPTIONS = {
    "researcher": "repository or external fact-finding",
    "backend-architect": "backend contracts, persistence, and ownership",
    "frontend-architect": "UI state, accessibility, and integration seams",
    "implementer": "an approved bounded write set",
    "qa-auditor": "independent read-only review",
}


def _agent_section(roles: tuple[str, ...]) -> str:
    role_lines = "\n".join(f"- `{role}` for {ROLE_DESCRIPTIONS[role]}." for role in roles)
    return f"""## Local agent team

Use `$plumbline-init` for the combined router/team setup and `$plumbline-agent-team` explicitly for initialize, audit, retune, or add requests. Do not invoke setup for ordinary feature work. Use only the project-local agents in `.codex/agents/` when work benefits from delegation:

{role_lines}

Keep direct low-risk or contract-complete work in the main thread. The main thread owns product decisions, active specs and plans, integration, and Git. Give workers context-bounded briefs with anchored read sections and disjoint write sets; do not pass full history or whole documentation trees when unchanged artifacts answer the question. The report-only roles (researcher, architect, and QA) receive no write set. Their `sandbox_mode = "read-only"` is intent; a writable parent is normal for a goal and may affect the child's effective sandbox. At each delegation wave, emit one compact line such as `Delegated wave: researcher [model=<slug>, reasoning=<effort>] — Boundary: report-only; no write set; no child agents`; report selected role names with configured model slugs and reasoning efforts, include effective model, reasoning, or sandbox values only when observable and materially different, and do not repeat unchanged configuration on resume. Inspect Git status/diff after the child returns, and never silently integrate unexpected edits. Only the approved implementer receives a bounded write set. Workers never spawn child agents. Do not use personal or global agent files as fallbacks. If no local role is available, state `Direct: <reason>` and continue on the main thread.
Delegation is main-mediated: every worker returns to the main thread, worker recommendations are advisory, and only the main thread selects and dispatches the next capability. Workers never invoke, hand off to, or dispatch another worker. When independent work is ready, the main thread may use one parallel wave only with a stable contract, disjoint scopes, no result dependency, and a clear join condition; otherwise keep it serial.
Keep `features.multi_agent = true` in project `.codex/config.toml`. Treat `agents.max_threads` and `agents.max_depth` as user-owned host settings; the setup template recommends 6 and 1 as starting values, but approved alternatives are preserved. Every role TOML must carry explicit `model`, `model_reasoning_effort`, and `sandbox_mode` values approved during setup.
Treat the approved model and reasoning values as adjustable starting points, not permanent policy: prefer the cheapest effective setting supported by the task, revisit it with evidence, and preserve tuned role fields during audit/retune unless explicitly approved.

Before dispatch, identify one lifecycle owner. Installed or enabled skills are available capabilities, not active ownership; an explicitly selected competing controller owns its own checkpoint and closeout flow.
"""
AGENT_GUIDANCE_MARKERS = (
    ".codex/agents/",
    "Workers never spawn child agents",
    "personal or global agent files",
    "Delegated wave:",
    "Direct: <reason>",
    "model slugs",
    "reasoning efforts",
    "one compact line",
    "recommended starting values",
    "main-mediated",
    "recommendations are advisory",
    "parallel wave",
    "report-only roles",
    "no write set",
    "effective sandbox",
    "writable parent",
    "one lifecycle owner",
    "explicitly selected competing controller",
    "cheapest effective setting",
)


@dataclass(frozen=True)
class InstallReport:
    changes: dict[Path, tuple[str, ...]]
    findings: tuple[str, ...] = ()
    operations: dict[Path, str] = field(default_factory=dict)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text if text.endswith("\n") else text + "\n")


def _ensure_lines(path: Path, lines: tuple[str, ...], *, apply: bool = True) -> bool:
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    existing = set(text.splitlines())
    missing = [line for line in lines if line not in existing]
    if not missing:
        return False
    if text and not text.endswith("\n"):
        text += "\n"
    if apply:
        _write(path, text + "\n".join(missing) + "\n")
    return True


def _repo_root(value: Path) -> Path:
    root = value.resolve()
    if not (root / ".git").exists():
        raise ValueError(f"not a Git repository: {root}")
    return root


def _git_dir(repo: Path) -> Path:
    marker = repo / ".git"
    if marker.is_dir():
        return marker
    text = marker.read_text(encoding="utf-8").strip()
    if not text.startswith("gitdir:"):
        raise ValueError(f"unsupported Git worktree marker: {marker}")
    git_dir = (repo / text.split(":", 1)[1].strip()).resolve()
    common_dir = git_dir / "commondir"
    if common_dir.is_file():
        return (git_dir / common_dir.read_text(encoding="utf-8").strip()).resolve()
    return git_dir


def _set_table_values(text: str, table: str, values: dict[str, str]) -> str:
    lines = text.splitlines()
    header = f"[{table}]"
    try:
        start = next(i for i, line in enumerate(lines) if line.strip() == header)
    except StopIteration:
        if lines and lines[-1].strip():
            lines.append("")
        lines.append(header)
        lines.extend(f"{key} = {value}" for key, value in values.items())
        return "\n".join(lines) + "\n"

    end = next(
        (i for i in range(start + 1, len(lines)) if re.match(r"^\s*\[[^\]]+\]\s*$", lines[i])),
        len(lines),
    )
    for key, value in values.items():
        pattern = re.compile(rf"^\s*{re.escape(key)}\s*=")
        match = next((i for i in range(start + 1, end) if pattern.match(lines[i])), None)
        if match is None:
            lines.insert(start + 1, f"{key} = {value}")
            end += 1
        else:
            lines[match] = f"{key} = {value}"
    return "\n".join(lines).rstrip() + "\n"


def _toml_string(value: str) -> str:
    if "\r" in value or "\n" in value:
        raise ValueError("TOML string values cannot contain newlines")
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _load_text(path: Path) -> tuple[str, dict]:
    text = path.read_text(encoding="utf-8")
    try:
        return text, tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        raise ValueError(f"invalid TOML at {path}: {exc}") from exc


def _config_values(data: dict) -> dict[str, object]:
    return {
        "features.multi_agent": data.get("features", {}).get("multi_agent"),
        "agents.max_threads": data.get("agents", {}).get("max_threads"),
        "agents.max_depth": data.get("agents", {}).get("max_depth"),
    }


def _config_changes(before: str | None, after: str) -> tuple[str, ...]:
    if before is None:
        return CONFIG_FIELDS
    old = _config_values(tomllib.loads(before))
    new = _config_values(tomllib.loads(after))
    return tuple(field for field in CONFIG_FIELDS if old[field] != new[field])


def _ensure_config(
    repo: Path,
    max_threads: int,
    max_depth: int,
    replace: bool,
    *,
    apply: bool = True,
) -> tuple[Path, tuple[str, ...]]:
    target = repo / ".codex" / "config.toml"
    desired = {"features.multi_agent": True, "agents.max_threads": max_threads, "agents.max_depth": max_depth}
    if not target.exists():
        if apply:
            _write(
                target,
                "# Plumbline project-local agent settings. Workers never spawn children.\n"
                "# Recommended starting values are 6 threads and depth 1; approved alternatives are valid.\n"
                "# Thread and depth values remain approved, user-owned host settings.\n"
                "[features]\n"
                "multi_agent = true\n\n"
                "[agents]\n"
                f"max_threads = {max_threads}\n"
                f"max_depth = {max_depth}\n",
            )
        return target, CONFIG_FIELDS

    before, data = _load_text(target)
    current = _config_values(data)
    if current == desired:
        return target, ()
    if not replace:
        raise ValueError(
            f"project config differs at {target}; show and approve the exact patch, then rerun with --replace-config"
        )
    text = _set_table_values(before, "features", {"multi_agent": "true"})
    text = _set_table_values(text, "agents", {"max_threads": str(max_threads), "max_depth": str(max_depth)})
    if apply:
        _write(target, text)
    return target, _config_changes(before, text)


def _prepare_agents_guidance(repo: Path, roles: tuple[str, ...]) -> tuple[Path, str]:
    target = repo / "AGENTS.md"
    text = target.read_text(encoding="utf-8") if target.is_file() else "# AGENTS.md\n"
    if "## Local agent team" in text:
        if not all(value in text for value in AGENT_GUIDANCE_MARKERS):
            raise ValueError(f"existing Local agent team section needs a reviewed manual patch: {target}")
        return target, text
    return target, text.rstrip() + "\n\n" + _agent_section(roles)


def _render_agent(template: Path, model: str, reasoning_effort: str) -> tuple[str, dict]:
    model_value = _toml_string(model)[1:-1]
    reasoning_value = _toml_string(reasoning_effort)[1:-1]
    text = template.read_text(encoding="utf-8")
    text = text.replace("{{MODEL}}", model_value).replace("{{REASONING_EFFORT}}", reasoning_value)
    if "{{" in text or "}}" in text:
        raise ValueError(f"unresolved template placeholder in {template}")
    try:
        return text, tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        raise ValueError(f"rendered template is invalid TOML: {template}: {exc}") from exc


def _template_data(template_root: Path, role: str) -> dict:
    path = template_root / f"{role}.toml"
    try:
        return tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        raise ValueError(f"invalid agent template: {path}: {exc}") from exc


def _validate_agent_data(data: dict, role: str, path: Path) -> list[str]:
    findings: list[str] = []
    for field in REQUIRED_AGENT_FIELDS:
        if not isinstance(data.get(field), str) or not data[field].strip():
            findings.append(f"{path}: missing required field {field}")
    if data.get("name") not in (None, role):
        findings.append(f"{path}: name is {data['name']!r}, expected {role!r}")
    instructions = data.get("developer_instructions", "")
    if isinstance(instructions, str) and "spawn child" not in instructions.lower():
        findings.append(f"{path}: missing no-child boundary")
    return findings


def _agent_changes(before: dict | None, after: dict) -> tuple[str, ...]:
    if before is None:
        return REQUIRED_AGENT_FIELDS
    return tuple(field for field in REQUIRED_AGENT_FIELDS if before.get(field) != after.get(field))


def _replace_instructions(text: str, instructions: str) -> str:
    if '"""' in instructions or "'''" in instructions:
        raise ValueError("developer instructions cannot contain a triple quote")
    body = instructions.strip("\n")
    multiline = re.compile(
        r"(?ms)^(?P<prefix>[ \t]*developer_instructions[ \t]*=[ \t]*)(?P<quote>\"\"\"|''').*?(?P=quote)(?P<newline>\r?\n|$)"
    )
    match = multiline.search(text)
    if match:
        replacement = f"{match.group('prefix')}{match.group('quote')}\n{body}\n{match.group('quote')}{match.group('newline')}"
        return text[: match.start()] + replacement + text[match.end() :]
    single = re.compile(r"(?m)^(?P<prefix>[ \t]*developer_instructions[ \t]*=[ \t]*).*(?P<newline>\r?\n|$)")
    match = single.search(text)
    if match:
        replacement = f'{match.group("prefix")}"""\n{body}\n"""{match.group("newline")}'
        return text[: match.start()] + replacement + text[match.end() :]
    return _insert_root_block(text, f'developer_instructions = """\n{body}\n"""')


def _insert_root_block(text: str, block: str) -> str:
    lines = text.splitlines(keepends=True)
    table = next((index for index, line in enumerate(lines) if re.match(r"^\s*\[[^\]]+\]\s*$", line.strip())), None)
    if table is None:
        return f"{text.rstrip()}\n\n{block}\n"
    before = "".join(lines[:table]).rstrip()
    after = "".join(lines[table:])
    prefix = f"{before}\n\n" if before else ""
    return f"{prefix}{block}\n\n{after.lstrip()}"


def _append_missing_fields(text: str, fields: dict[str, str]) -> str:
    if not fields:
        return text
    additions = "\n".join(f"{field} = {_toml_string(value)}" for field, value in fields.items())
    return _insert_root_block(text, additions)


def _audit_config(repo: Path) -> list[str]:
    target = repo / ".codex" / "config.toml"
    if not target.exists():
        return [f"{target}: missing project-local config"]
    try:
        _text, data = _load_text(target)
    except ValueError as exc:
        return [str(exc)]
    values = _config_values(data)
    findings = []
    if values["features.multi_agent"] is not True:
        findings.append(f"{target}: features.multi_agent must be true")
    if type(values["agents.max_threads"]) is not int or values["agents.max_threads"] < 1:
        findings.append(f"{target}: agents.max_threads must be a positive integer")
    if type(values["agents.max_depth"]) is not int or values["agents.max_depth"] < 0:
        findings.append(f"{target}: agents.max_depth must be a non-negative integer")
    return findings


def _audit_router(plugin: Path, repo: Path) -> list[str]:
    target = repo / ROUTER_RELATIVE_PATH
    template = plugin / "templates" / "router" / "SKILL.md"
    if not target.exists():
        return [f"{target}: missing project-local router"]
    if not template.is_file():
        return [f"{template}: missing current router template"]
    try:
        target_text = target.read_text(encoding="utf-8")
        template_text = template.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"router audit could not read {target}: {exc}"]
    if target_text != template_text:
        return [
            f"{target}: differs from current router template {template}; review an explicit refresh, no file was changed"
        ]
    return []


def _audit_agents_guidance(repo: Path) -> list[str]:
    target = repo / "AGENTS.md"
    if not target.is_file():
        return [f"{target}: missing project agent-team guidance"]
    try:
        text = target.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"{target}: could not read project agent-team guidance: {exc}"]
    if "## Local agent team" not in text:
        return [f"{target}: missing `## Local agent team` guidance section"]
    return [
        f"{target}: Local agent team guidance missing marker {marker!r}"
        for marker in AGENT_GUIDANCE_MARKERS
        if marker not in text
    ]


def _audit(plugin: Path, repo: Path, roles: tuple[str, ...]) -> InstallReport:
    findings = _audit_config(repo)
    findings.extend(_audit_router(plugin, repo))
    findings.extend(_audit_agents_guidance(repo))
    for role in roles:
        path = repo / ".codex" / "agents" / f"{role}.toml"
        if not path.exists():
            findings.append(f"{path}: missing project-local role")
            continue
        try:
            _text, data = _load_text(path)
        except ValueError as exc:
            findings.append(str(exc))
            continue
        findings.extend(_validate_agent_data(data, role, path))
    return InstallReport({}, tuple(findings))


def _retune(
    plugin: Path,
    repo: Path,
    roles: tuple[str, ...],
    *,
    model: str | None,
    reasoning_effort: str | None,
    fill_missing: bool,
    update_instructions: bool,
    max_threads: int,
    max_depth: int,
    replace_config: bool,
    dry_run: bool,
) -> InstallReport:
    if fill_missing and (model is None or reasoning_effort is None):
        raise ValueError("--fill-missing requires --model and --reasoning-effort")
    changes: dict[Path, tuple[str, ...]] = {}
    operations: dict[Path, str] = {}
    findings = _audit_config(repo)
    findings.extend(_audit_router(plugin, repo))
    findings.extend(_audit_agents_guidance(repo))
    if replace_config:
        config_existed = (repo / ".codex" / "config.toml").exists()
        config_path, config_fields = _ensure_config(repo, max_threads, max_depth, True, apply=not dry_run)
        if config_fields:
            changes[config_path] = config_fields
            operations[config_path] = "modify" if config_existed else "create"
            findings = [finding for finding in findings if not finding.startswith(str(config_path))]

    template_root = plugin / "templates" / "agents"
    for role in roles:
        path = repo / ".codex" / "agents" / f"{role}.toml"
        if not path.exists():
            findings.append(f"{path}: missing project-local role; initialize it instead")
            continue
        try:
            before_text, before_data = _load_text(path)
        except ValueError as exc:
            findings.append(str(exc))
            continue
        if before_data.get("name") not in (None, role):
            findings.extend(_validate_agent_data(before_data, role, path))
            continue

        template = _template_data(template_root, role)
        after_text = before_text
        changed: list[str] = []
        missing: dict[str, str] = {}
        if fill_missing:
            for field in REQUIRED_AGENT_FIELDS:
                value = before_data.get(field)
                if field not in before_data:
                    if field == "model":
                        missing[field] = model or ""
                    elif field == "model_reasoning_effort":
                        missing[field] = reasoning_effort or ""
                    elif field == "sandbox_mode":
                        missing[field] = SANDBOXES[role]
                    elif field == "developer_instructions":
                        after_text = _replace_instructions(after_text, str(template[field]))
                        changed.append(field)
                    else:
                        missing[field] = str(template.get(field, ""))
            after_text = _append_missing_fields(after_text, missing)
            changed.extend(missing)
        if update_instructions:
            instruction = str(template["developer_instructions"])
            if before_data.get("developer_instructions") != instruction:
                after_text = _replace_instructions(after_text, instruction)
                if "developer_instructions" not in changed:
                    changed.append("developer_instructions")

        if not changed:
            findings.extend(_validate_agent_data(before_data, role, path))
            continue
        try:
            _after_text, after_data = _load_text_from_value(path, after_text)
        except ValueError as exc:
            findings.append(str(exc))
            continue
        findings.extend(_validate_agent_data(after_data, role, path))
        if not dry_run:
            _write(path, after_text)
        changes[path] = tuple(dict.fromkeys(changed))
        operations[path] = "modify"
    return InstallReport(changes, tuple(findings), operations)


def _load_text_from_value(path: Path, text: str) -> tuple[str, dict]:
    try:
        return text, tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        raise ValueError(f"retuned TOML is invalid at {path}: {exc}") from exc


def _initialize(
    plugin: Path,
    repo: Path,
    roles: tuple[str, ...],
    *,
    model: str | None,
    reasoning_effort: str | None,
    max_threads: int,
    max_depth: int,
    replace: bool,
    replace_config: bool,
    update_agents: bool,
    propagate: bool,
    dry_run: bool,
) -> InstallReport:
    if model is None or reasoning_effort is None:
        raise ValueError("initialize requires --model and --reasoning-effort")
    for role in roles:
        target = repo / ".codex" / "agents" / f"{role}.toml"
        if target.exists() and not replace:
            raise FileExistsError(f"agent already exists; audit or retune it before replacing: {target}")

    changes: dict[Path, tuple[str, ...]] = {}
    operations: dict[Path, str] = {}
    guidance = _prepare_agents_guidance(repo, roles) if update_agents else None
    config_target = repo / ".codex" / "config.toml"
    config_existed = config_target.exists()
    config_path, config_fields = _ensure_config(repo, max_threads, max_depth, replace_config, apply=not dry_run)
    if config_fields:
        changes[config_path] = config_fields
        operations[config_path] = "modify" if config_existed else "create"

    template_root = plugin / "templates" / "agents"
    for role in roles:
        target = repo / ".codex" / "agents" / f"{role}.toml"
        before_data = None
        if target.exists():
            try:
                _before_text, before_data = _load_text(target)
            except ValueError:
                before_data = None
        text, after_data = _render_agent(template_root / f"{role}.toml", model, reasoning_effort)
        operation = "modify" if target.exists() else "create"
        if not dry_run:
            _write(target, text)
        changes[target] = _agent_changes(before_data, after_data)
        operations[target] = operation

    git_exclude = _git_dir(repo) / "info" / "exclude"
    git_exclude_existed = git_exclude.exists()
    if _ensure_lines(git_exclude, LOCAL_IGNORE_FILES, apply=not dry_run):
        changes[git_exclude] = ("ignore rules",)
        operations[git_exclude] = "modify" if git_exclude_existed else "create"
    if guidance:
        target, text = guidance
        current = target.read_text(encoding="utf-8") if target.is_file() else ""
        if current != text:
            operation = "modify" if target.exists() else "create"
            if not dry_run:
                _write(target, text)
            changes[target] = ("local agent-team guidance",)
            operations[target] = operation
    if propagate:
        manifest = repo / ".worktreeinclude"
        manifest_existed = manifest.exists()
        if _ensure_lines(manifest, WORKTREE_FILES, apply=not dry_run):
            changes[manifest] = ("propagation manifest",)
            operations[manifest] = "modify" if manifest_existed else "create"
        gitignore = repo / ".gitignore"
        gitignore_existed = gitignore.exists()
        if _ensure_lines(gitignore, LOCAL_IGNORE_FILES, apply=not dry_run):
            changes[gitignore] = ("ignore rules",)
            operations[gitignore] = "modify" if gitignore_existed else "create"
    return InstallReport(changes, operations=operations)


def install(
    plugin_root: Path,
    target_root: Path,
    *,
    mode: str = "initialize",
    model: str | None = None,
    reasoning_effort: str | None = None,
    roles: tuple[str, ...] = ROLES,
    max_threads: int = 6,
    max_depth: int = 1,
    replace: bool = False,
    replace_config: bool = False,
    fill_missing: bool = False,
    update_instructions: bool = False,
    update_agents: bool = False,
    propagate: bool = False,
    dry_run: bool = False,
) -> InstallReport:
    repo = _repo_root(target_root)
    plugin = plugin_root.resolve()
    if mode not in MODES:
        raise ValueError(f"mode must be one of: {', '.join(MODES)}")
    if not roles or len(set(roles)) != len(roles) or any(role not in ROLES for role in roles):
        raise ValueError(f"roles must be selected from: {', '.join(ROLES)}")
    if max_threads < 1:
        raise ValueError("max_threads must be at least 1")
    if max_depth < 0:
        raise ValueError("max_depth must be non-negative")
    if mode == "audit":
        if any((replace, replace_config, fill_missing, update_instructions, update_agents, propagate)):
            raise ValueError("audit is read-only; remove mutation flags")
        return _audit(plugin, repo, roles)
    if mode == "retune":
        if replace:
            raise ValueError("retune preserves existing roles; use --update-instructions or --fill-missing")
        if update_agents or propagate:
            raise ValueError("retune only changes roles; use initialize for AGENTS/worktree setup")
        return _retune(
            plugin,
            repo,
            roles,
            model=model,
            reasoning_effort=reasoning_effort,
            fill_missing=fill_missing,
            update_instructions=update_instructions,
            max_threads=max_threads,
            max_depth=max_depth,
            replace_config=replace_config,
            dry_run=dry_run,
        )
    if fill_missing or update_instructions:
        raise ValueError("initialize creates templates; use retune for preserve-existing updates")
    return _initialize(
        plugin,
        repo,
        roles,
        model=model,
        reasoning_effort=reasoning_effort,
        max_threads=max_threads,
        max_depth=max_depth,
        replace=replace,
        replace_config=replace_config,
        update_agents=update_agents,
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
    if output_format == "json":
        print(
            json.dumps(
                {
                    "mode": mode,
                    "dry_run": dry_run,
                    "writes_applied": not dry_run and mode != "audit",
                    "changes": changes,
                    "findings": list(report.findings),
                    "global_agents_selected": False,
                },
                indent=2,
            )
        )
        return
    print(f"Plumbline agent-team {mode} {'preview' if dry_run else 'complete'}.")
    if report.changes:
        for path, fields in report.changes.items():
            operation = report.operations.get(path, "modify")
            print(f"{operation.title()} {path}: {', '.join(fields)}")
    else:
        print("Changed: none")
    for finding in report.findings:
        print(f"Finding: {finding}")
    if mode == "audit":
        print("Audit was read-only; no files were written.")
    print("Global/personal agent files were not selected.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Target repository root")
    parser.add_argument("--mode", choices=MODES, default="initialize")
    parser.add_argument("--model", help="Approved model slug for new or missing project fields")
    parser.add_argument("--reasoning-effort", help="Approved reasoning effort for new or missing project fields")
    parser.add_argument("--roles", type=_parse_roles, default=ROLES, help="Comma-separated roles")
    parser.add_argument("--max-threads", type=int, default=6)
    parser.add_argument("--max-depth", type=int, default=1)
    parser.add_argument("--replace", action="store_true", help="Replace existing role files during initialize only")
    parser.add_argument("--replace-config", action="store_true", help="Apply the approved project config patch")
    parser.add_argument("--fill-missing", action="store_true", help="Retune by adding missing fields only")
    parser.add_argument("--update-instructions", action="store_true", help="Retune by explicitly updating instructions")
    parser.add_argument("--update-agents", action="store_true", help="Add the approved AGENTS.md section")
    parser.add_argument("--propagate", action="store_true", help="Add ignored-file worktree propagation")
    parser.add_argument("--dry-run", action="store_true", help="Preview the exact changes without writing files")
    parser.add_argument("--format", choices=("text", "json"), default="text", dest="output_format")
    args = parser.parse_args()
    plugin_root = Path(__file__).resolve().parents[1]
    try:
        report = install(
            plugin_root,
            args.root,
            mode=args.mode,
            model=args.model,
            reasoning_effort=args.reasoning_effort,
            roles=args.roles,
            max_threads=args.max_threads,
            max_depth=args.max_depth,
            replace=args.replace,
            replace_config=args.replace_config,
            fill_missing=args.fill_missing,
            update_instructions=args.update_instructions,
            update_agents=args.update_agents,
            propagate=args.propagate,
            dry_run=args.dry_run,
        )
    except (FileExistsError, OSError, ValueError, tomllib.TOMLDecodeError) as exc:
        parser.error(str(exc))
    _print_report(args.mode, report, dry_run=args.dry_run, output_format=args.output_format)
    return 0


if __name__ == "__main__":
    sys.exit(main())
