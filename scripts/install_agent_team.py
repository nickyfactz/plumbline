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
    "agents.enabled",
    "agents.max_concurrent_threads_per_session",
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
AGENT_GUIDANCE_HEADING = "## Local agent team"
AGENT_GUIDANCE_START = "<!-- plumbline:managed-agent-team:start -->"
AGENT_GUIDANCE_END = "<!-- plumbline:managed-agent-team:end -->"
ROLE_DESCRIPTIONS = {
    "researcher": "repository or external fact-finding",
    "backend-architect": "backend contracts, persistence, and ownership",
    "frontend-architect": "UI state, accessibility, and integration seams",
    "implementer": "an approved bounded write set",
    "qa-auditor": "independent read-only review",
}


def _agent_section(roles: tuple[str, ...]) -> str:
    role_lines = "\n".join(f"- `{role}` for {ROLE_DESCRIPTIONS[role]}." for role in roles)
    return f"""{AGENT_GUIDANCE_START}
## Local agent team

Use `$plumbline-init` for the combined router/team setup and `$plumbline-agent-team` explicitly for initialize, audit, retune, or add requests. Do not invoke setup for ordinary feature work. Use only the project-local agents in `.codex/agents/` for bounded work that an approved role can own:

{role_lines}

Keep direct low-risk or contract-complete work in the main thread. The main thread owns product decisions, active specs and plans, integration, and Git. Give workers context-bounded briefs with anchored read sections and disjoint write sets; do not pass full history or whole documentation trees when unchanged artifacts answer the question. The report-only roles (researcher, architect, and QA) receive no write set. Their `sandbox_mode = "read-only"` is intent; a writable parent is normal for a goal and may affect the child's effective sandbox. At each delegation wave, reread the applicable project-local config and selected role files, then emit one compact line such as `Delegated wave: researcher [model=<slug>, reasoning=<effort>] — Boundary: report-only; no write set; no child agents`; report selected role names with current configured model slugs and reasoning efforts, include effective model, reasoning, or sandbox values only when observable and materially different, and do not repeat unchanged configuration on resume. A changed profile hash refreshes new dispatches; workers already running retain their creation profile. Inspect Git status/diff after the child returns, and never silently integrate unexpected edits. Each write-capable role receives only its approved bounded write set. Workers never spawn child agents. Do not use personal or global agent files as fallbacks. If a role is missing in the active worktree, refresh only the ignored project-local config/role files from the source checkout through `.worktreeinclude`, reread them, and use `Direct: <reason>` only if it remains unavailable. If no local role is available, state `Direct: <reason>` and continue on the main thread.
Delegation is main-mediated: every worker returns to the main thread, worker recommendations are advisory, and only the main thread selects and dispatches the next capability. Workers never invoke, hand off to, or dispatch another worker. When independent work is ready, the main thread may use one parallel wave only with a stable contract, disjoint scopes, no result dependency, and a clear join condition; otherwise keep it serial.
For Execute checkpoints, delegation is the default: when an approved project-local role can own useful bounded research, architecture, implementation, review, testing, or another capability with a clear boundary, dispatch that role before the main thread duplicates the work. Use its configured model, reasoning effort, and sandbox intent; do not invent or substitute a personal/global role. Record `delegation_roles` and `delegation_status` in the checkpoint resume record and restore them after compaction. Keep product decisions, lifecycle/plan state, joins, integration, Git, singleton operations, or tiny coupled actions on the main thread; otherwise a missing role is an explicit `Direct: <reason>` fallback.
Keep current Codex collaboration enabled through `agents.enabled = true`. Treat `agents.max_concurrent_threads_per_session` as a user-owned host setting; the setup template recommends 6 as a starting value, but approved alternatives are preserved. Legacy `features.multi_agent`, `agents.max_threads`, and `agents.max_depth` values are migration candidates, not Plumbline requirements. Every role TOML must carry explicit `model`, `model_reasoning_effort`, and `sandbox_mode` values approved during setup.
Treat project-local role files as live user-owned dispatch profiles: manual edits to model, reasoning, sandbox, or instructions apply to new workers without an audit or retune, while workers already running keep their original values. Audit/retune approval remains required for installer-managed changes. Never let dispatch overwrite the current project-local values.

Before dispatch, identify one lifecycle owner. Installed or enabled skills are available capabilities, not active ownership; an explicitly selected competing controller owns its own checkpoint and closeout flow.
{AGENT_GUIDANCE_END}
"""
AGENT_GUIDANCE_MARKERS = (
    AGENT_GUIDANCE_START,
    AGENT_GUIDANCE_END,
    ".codex/agents/",
    "Workers never spawn child agents",
    "personal or global agent files",
    "Delegated wave:",
    "Direct: <reason>",
    "model slugs",
    "reasoning efforts",
    "one compact line",
    "recommended starting value",
    "main-mediated",
    "recommendations are advisory",
    "parallel wave",
    "report-only roles",
    "no write set",
    "effective sandbox",
    "writable parent",
    "one lifecycle owner",
    "explicitly selected competing controller",
    "delegation is the default",
    "delegation_roles",
    "delegation_status",
    "reread the applicable project-local config",
    "changed profile hash",
    "refresh only the ignored project-local",
    "live user-owned dispatch profiles",
)


@dataclass(frozen=True)
class InstallReport:
    changes: dict[Path, tuple[str, ...]]
    findings: tuple[str, ...] = ()
    operations: dict[Path, str] = field(default_factory=dict)
    requires_replace: bool = False


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


def _remove_table_values(text: str, table: str, keys: tuple[str, ...]) -> str:
    lines = text.splitlines()
    header = f"[{table}]"
    try:
        start = next(i for i, line in enumerate(lines) if line.strip() == header)
    except StopIteration:
        return text
    end = next(
        (i for i in range(start + 1, len(lines)) if re.match(r"^\s*\[[^\]]+\]\s*$", lines[i])),
        len(lines),
    )
    patterns = tuple(re.compile(rf"^\s*{re.escape(key)}\s*=") for key in keys)
    lines = [
        line
        for index, line in enumerate(lines)
        if not (start < index < end and any(pattern.match(line) for pattern in patterns))
    ]
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
        "agents.enabled": data.get("agents", {}).get("enabled"),
        "agents.max_concurrent_threads_per_session": data.get("agents", {}).get(
            "max_concurrent_threads_per_session"
        ),
        "features.multi_agent": data.get("features", {}).get("multi_agent"),
        "agents.max_threads": data.get("agents", {}).get("max_threads"),
        "agents.max_depth": data.get("agents", {}).get("max_depth"),
    }


def _config_changes(before: str | None, after: str) -> tuple[str, ...]:
    if before is None:
        new = _config_values(tomllib.loads(after))
        return tuple(field for field in CONFIG_FIELDS if new[field] is not None)
    old = _config_values(tomllib.loads(before))
    new = _config_values(tomllib.loads(after))
    return tuple(field for field in CONFIG_FIELDS if old[field] != new[field])


def _ensure_config(
    repo: Path,
    max_threads: int,
    replace: bool,
    *,
    apply: bool = True,
) -> tuple[Path, tuple[str, ...]]:
    target = repo / ".codex" / "config.toml"
    desired = {
        "agents.enabled": True,
        "agents.max_concurrent_threads_per_session": max_threads,
        "features.multi_agent": None,
        "agents.max_threads": None,
        "agents.max_depth": None,
    }
    if not target.exists():
        text = (
            "# Plumbline project-local agent settings. Workers return to the main thread.\n"
            "# Codex enables subagents by default; this explicit switch keeps project intent visible.\n"
            "# The concurrency value is a recommended starting point and remains user-owned.\n"
            "[agents]\n"
            "enabled = true\n"
            f"max_concurrent_threads_per_session = {max_threads}\n"
        )
        if apply:
            _write(target, text)
        return target, _config_changes(None, text)

    before, data = _load_text(target)
    current = _config_values(data)
    if current == desired:
        return target, ()
    if not replace:
        raise ValueError(
            f"project config differs at {target}; show and approve the exact patch, then rerun with --replace-config"
        )
    text = _remove_table_values(before, "features", ("multi_agent",))
    text = _remove_table_values(text, "agents", ("max_threads", "max_depth"))
    text = _set_table_values(
        text,
        "agents",
        {"enabled": "true", "max_concurrent_threads_per_session": str(max_threads)},
    )
    if apply:
        _write(target, text)
    return target, _config_changes(before, text)


def _guidance_section_bounds(text: str, heading: str) -> tuple[int, int] | None:
    heading_match = re.search(rf"(?m)^{re.escape(heading)}[ \t]*$", text)
    if not heading_match:
        return None
    following = text[heading_match.end() :]
    next_heading = re.search(r"(?m)^## (?!#)", following)
    end = heading_match.end() + next_heading.start() if next_heading else len(text)
    return heading_match.start(), end


def _guidance_block_bounds(text: str, heading: str) -> tuple[int, int] | None:
    section = _guidance_section_bounds(text, heading)
    if not section:
        return None
    start_match = re.search(rf"(?m)^{re.escape(AGENT_GUIDANCE_START)}[ \t]*$", text)
    end_match = re.search(rf"(?m)^{re.escape(AGENT_GUIDANCE_END)}[ \t]*$", text)
    if start_match and end_match and start_match.start() <= section[0] <= end_match.end():
        return start_match.start(), end_match.end()
    return section


def _guidance_has_markers(text: str, heading: str) -> bool:
    section = _guidance_section_bounds(text, heading)
    if not section:
        return False
    start_match = re.search(rf"(?m)^{re.escape(AGENT_GUIDANCE_START)}[ \t]*$", text)
    end_match = re.search(rf"(?m)^{re.escape(AGENT_GUIDANCE_END)}[ \t]*$", text)
    return bool(start_match and end_match and start_match.start() <= section[0] <= end_match.end())


def _replace_guidance_section(text: str, heading: str, replacement: str) -> str:
    bounds = _guidance_block_bounds(text, heading)
    if not bounds:
        return text.rstrip() + "\n\n" + replacement.strip() + "\n"
    before = text[: bounds[0]].rstrip("\n")
    after = text[bounds[1] :].lstrip("\n")
    result = before + "\n\n" + replacement.strip()
    if after:
        result += "\n\n" + after
    return result.rstrip() + "\n"


def _prepare_agents_guidance(
    repo: Path,
    roles: tuple[str, ...],
    *,
    refresh: bool = False,
    replace_guidance: bool = False,
) -> tuple[Path, str, bool, str | None]:
    target = repo / "AGENTS.md"
    text = target.read_text(encoding="utf-8") if target.is_file() else "# AGENTS.md\n"
    section = _guidance_block_bounds(text, AGENT_GUIDANCE_HEADING)
    if not section:
        return target, text.rstrip() + "\n\n" + _agent_section(roles), False, None
    if not refresh:
        return target, text, False, None

    replacement = _agent_section(roles)
    has_managed_markers = _guidance_has_markers(text, AGENT_GUIDANCE_HEADING)
    if not has_managed_markers and not replace_guidance:
        proposed = _replace_guidance_section(text, AGENT_GUIDANCE_HEADING, replacement)
        return (
            target,
            proposed,
            True,
            f"{target}: existing guidance is an unmarked legacy section; previewed refresh requires --replace-agents-guidance",
        )
    return target, _replace_guidance_section(text, AGENT_GUIDANCE_HEADING, replacement), False, None


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
        return []
    try:
        _text, data = _load_text(target)
    except ValueError as exc:
        return [str(exc)]
    values = _config_values(data)
    findings = []
    if values["agents.enabled"] is False:
        findings.append(f"{target}: agents.enabled=false disables project subagents")
    concurrency = values["agents.max_concurrent_threads_per_session"]
    if concurrency is not None and (type(concurrency) is not int or concurrency < 1):
        findings.append(f"{target}: agents.max_concurrent_threads_per_session must be a positive integer")
    for field in ("features.multi_agent", "agents.max_threads", "agents.max_depth"):
        if values[field] is not None:
            findings.append(f"{target}: legacy {field} is no longer required; offer an approved config migration")
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
    section = _guidance_block_bounds(text, AGENT_GUIDANCE_HEADING)
    if not section:
        return [f"{target}: missing `## Local agent team` guidance section"]
    section_text = text[section[0] : section[1]]
    return [
        f"{target}: Local agent team guidance missing marker {marker!r}"
        for marker in AGENT_GUIDANCE_MARKERS
        if marker not in section_text
    ]


def _refresh_agents_guidance(
    repo: Path,
    roles: tuple[str, ...],
    *,
    replace_guidance: bool,
    dry_run: bool,
) -> InstallReport:
    target, proposed, requires_replace, finding = _prepare_agents_guidance(
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
        changes[target] = ("local agent-team guidance",)
        operations[target] = "modify" if target.exists() else "create"
        if not dry_run:
            _write(target, proposed)
    return InstallReport(changes, tuple(findings), operations, requires_replace=requires_replace)


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
        config_path, config_fields = _ensure_config(repo, max_threads, True, apply=not dry_run)
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
    replace: bool,
    replace_config: bool,
    update_agents: bool,
    refresh_agents: bool,
    replace_guidance: bool,
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
    guidance = (
        _prepare_agents_guidance(
            repo,
            roles,
            refresh=refresh_agents,
            replace_guidance=replace_guidance,
        )
        if update_agents
        else None
    )
    if guidance and guidance[2] and not dry_run:
        raise ValueError(guidance[3] or f"{guidance[0]} requires explicit guidance replacement approval")
    config_target = repo / ".codex" / "config.toml"
    config_existed = config_target.exists()
    config_path, config_fields = _ensure_config(repo, max_threads, replace_config, apply=not dry_run)
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
    findings: list[str] = []
    if guidance:
        target, text, requires_replace, finding = guidance
        current = target.read_text(encoding="utf-8") if target.is_file() else ""
        if current != text:
            operation = "modify" if target.exists() else "create"
            if not dry_run:
                _write(target, text)
            changes[target] = ("local agent-team guidance",)
            operations[target] = operation
        if finding:
            findings.append(finding)
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
    return InstallReport(changes, tuple(findings), operations, requires_replace=guidance[2] if guidance else False)


def install(
    plugin_root: Path,
    target_root: Path,
    *,
    mode: str = "initialize",
    model: str | None = None,
    reasoning_effort: str | None = None,
    roles: tuple[str, ...] = ROLES,
    max_threads: int = 6,
    replace: bool = False,
    replace_config: bool = False,
    fill_missing: bool = False,
    update_instructions: bool = False,
    update_agents: bool = False,
    refresh_agents: bool = False,
    replace_guidance: bool = False,
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
    if mode == "audit":
        if any((replace, replace_config, fill_missing, update_instructions, update_agents, refresh_agents, replace_guidance, propagate)):
            raise ValueError("audit is read-only; remove mutation flags")
        return _audit(plugin, repo, roles)
    if mode == "retune":
        if replace:
            raise ValueError("retune preserves existing roles; use --update-instructions or --fill-missing")
        if update_agents or refresh_agents or replace_guidance or propagate:
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
            replace_config=replace_config,
            dry_run=dry_run,
        )
    if refresh_agents:
        if not update_agents:
            raise ValueError("--refresh-agents requires --update-agents")
        if replace or replace_config or propagate:
            raise ValueError("--refresh-agents is a guidance-only initialization update; remove role/config/worktree mutation flags")
        return _refresh_agents_guidance(repo, roles, replace_guidance=replace_guidance, dry_run=dry_run)
    if replace_guidance:
        raise ValueError("--replace-agents-guidance requires --refresh-agents")
    if fill_missing or update_instructions:
        raise ValueError("initialize creates templates; use retune for preserve-existing updates")
    return _initialize(
        plugin,
        repo,
        roles,
        model=model,
        reasoning_effort=reasoning_effort,
        max_threads=max_threads,
        replace=replace,
        replace_config=replace_config,
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
    if output_format == "json":
        print(
            json.dumps(
                {
                    "mode": mode,
                    "dry_run": dry_run,
                    "writes_applied": not dry_run and mode != "audit",
                    "changes": changes,
                    "findings": list(report.findings),
                    "requires_replace": report.requires_replace,
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
    if report.requires_replace:
        print("Approval required: rerun with --replace-agents-guidance after reviewing the proposed AGENTS.md refresh.")
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
    parser.add_argument("--replace", action="store_true", help="Replace existing role files during initialize only")
    parser.add_argument("--replace-config", action="store_true", help="Apply the approved project config patch")
    parser.add_argument("--fill-missing", action="store_true", help="Retune by adding missing fields only")
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
            replace=args.replace,
            replace_config=args.replace_config,
            fill_missing=args.fill_missing,
            update_instructions=args.update_instructions,
            update_agents=args.update_agents,
            refresh_agents=args.refresh_agents,
            replace_guidance=args.replace_agents_guidance,
            propagate=args.propagate,
            dry_run=args.dry_run,
        )
    except (FileExistsError, OSError, ValueError, tomllib.TOMLDecodeError) as exc:
        parser.error(str(exc))
    _print_report(args.mode, report, dry_run=args.dry_run, output_format=args.output_format)
    return 0


if __name__ == "__main__":
    sys.exit(main())
