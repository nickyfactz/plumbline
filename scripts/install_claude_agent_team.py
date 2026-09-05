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
CLAUDE_GUIDANCE_FILE = Path("CLAUDE.md")
CLAUDE_AGENTS_IMPORT = "@AGENTS.md"
LOCAL_IGNORE_FILES = (".claude/agents/",)
WORKTREE_FILES = (".claude/agents/*.md",)
REQUIRED_FIELDS = ("name", "description", "model", "effort", "tools", "permissionMode")

ROLE_TOOLS = {
    "researcher": ("Read", "Glob", "Grep"),
    "backend-architect": ("Read", "Glob", "Grep"),
    "frontend-architect": ("Read", "Glob", "Grep"),
    "implementer": ("Read", "Glob", "Grep", "Edit", "Write", "Bash"),
    "code-reviewer": ("Read", "Glob", "Grep"),
    "qa-auditor": ("Read", "Glob", "Grep"),
}
ROLE_PERMISSION_MODES = {
    "researcher": "plan",
    "backend-architect": "plan",
    "frontend-architect": "plan",
    "implementer": "default",
    "code-reviewer": "plan",
    "qa-auditor": "plan",
}
RECOMMENDED_PROFILES = {
    "frontend-architect": ("opus", "low"),
    "backend-architect": ("opus", "low"),
    "researcher": ("sonnet", "low"),
    "implementer": ("sonnet", "high"),
    "code-reviewer": ("sonnet", "high"),
    "qa-auditor": ("opus", "medium"),
}
RECOMMENDED_EFFORTS = {
    role: effort for role, (_model, effort) in RECOMMENDED_PROFILES.items()
}
CLAUDE_EFFORTS = {"low", "medium", "high", "xhigh", "max"}
CLAUDE_PERMISSION_MODES = {
    "default",
    "acceptEdits",
    "auto",
    "dontAsk",
    "bypassPermissions",
    "plan",
    "manual",
}
CLAUDE_GUIDANCE_MARKERS = (
    AGENT_GUIDANCE_START,
    AGENT_GUIDANCE_END,
    ".claude/agents/",
    "main-mediated",
    "recommendations are advisory",
    "parallel wave",
    "explicit user instructions as authoritative",
    "material Execute work",
    "materially reduces main-thread context",
    "delegation_roles",
    "delegation_status",
    "bounded research",
    "configured model",
    "Reread the selected",
    "running workers keep",
    "worker instances as disposable",
    "fresh instance",
    "exact same unfinished assignment",
    "source checkout",
    "orchestrator thin",
    "compact decision packet",
    "maintainable-code",
    "code-reviewer",
    "provider-versioned inputs",
    "profile refresh",
    "model aliases",
    "@agent-<role>",
    "hot-reloads",
    "Codex-only",
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


def _profile(role: str, model: str | None, effort: str | None) -> tuple[str, str]:
    if (model is None) != (effort is None):
        raise ValueError("--model and --effort must be supplied together")
    return (model, effort) if model is not None else RECOMMENDED_PROFILES[role]


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


def _set_frontmatter_values(text: str, values: dict[str, object], path: Path) -> str:
    lines, closing, _existing, _body_text = _frontmatter(text, path)
    for key, value in values.items():
        pattern = re.compile(rf"^\s*{re.escape(key)}\s*:")
        match = next((index for index in range(1, closing) if pattern.match(lines[index])), None)
        replacement = f"{key}: {_yaml_value(value)}"
        if match is None:
            lines.insert(closing, replacement)
            closing += 1
        else:
            lines[match] = replacement
    return "\n".join(lines).rstrip() + "\n"


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
    model = values.get("model")
    if isinstance(model, str) and (model in {"sol", "luna"} or model.startswith("gpt-")):
        findings.append(
            f"{path}: model {model!r} appears to be a Codex/OpenAI value; use a Claude alias, full ID, or inherit"
        )
    effort = values.get("effort")
    if effort not in CLAUDE_EFFORTS:
        findings.append(f"{path}: effort must be one of: {', '.join(sorted(CLAUDE_EFFORTS))}")
    permission_mode = values.get("permissionMode")
    if permission_mode not in CLAUDE_PERMISSION_MODES:
        findings.append(
            f"{path}: permissionMode must be one of: {', '.join(sorted(CLAUDE_PERMISSION_MODES))}"
        )
    tools = values.get("tools", [])
    if not isinstance(tools, list) or any(not isinstance(tool, str) for tool in tools):
        findings.append(f"{path}: tools must be a YAML list of tool names")
        tools = []
    if "Agent" in tools:
        findings.append(f"{path}: Agent tool would permit child delegation")
    if role != "implementer" and any(tool in {"Edit", "Write", "Bash"} for tool in tools):
        findings.append(f"{path}: report-only role must not expose Edit, Write, or Bash tools")
    if role == "implementer" and not {"Edit", "Write"}.issubset(tools):
        findings.append(f"{path}: implementer must expose Edit and Write tools")
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

Treat explicit user instructions as authoritative over Plumbline defaults and
process preferences, but interpret them in the context of the user's stated
outcome, approved artifacts, and repository evidence. Do not follow an
ambiguous instruction literally when doing so would contradict the apparent
goal, approved contract, or safety boundary. Resolve ordinary ambiguity with a
safe reversible default; ask a focused product question only when competing
interpretations would materially change behavior.

When Git is established, material multi-step Execute work uses a required Git
policy by default. Create main-thread commits at coherent checkpoint or batch
boundaries unless the user explicitly opts out; state the policy once without
blocking for approval. Record `HEAD`, keep unrelated dirty files, scratch, and
secrets out, and do not advance dependent checkpoints with uncommitted
plan-owned changes. Use checkpoint commits, `git show`, and focused diffs for
worker hydration. Ask before push, force-push, history rewriting, or external
publication. If Git is absent, recommend establishing it before Execute and
report an explicit opt-out as Git-unanchored.

Maintainable code: when writing, modifying, or reviewing production code,
invoke the `maintainable-code` skill. Implementers apply its implementation and
human-legibility guidance; `code-reviewer` applies its adversarial review gate.

Keep the orchestrator thin. The main thread reads only the controlling artifact, repository guidance, Git state, and named paths needed to route and integrate work. Before broad repository search, multi-file fact gathering, external research, or cross-seam review, dispatch a matching project-local role with a bounded question when it can return a bounded result that materially reduces main-thread context or improves quality; keep small, tightly coupled, and inherently main-owned work direct. Ask read-heavy workers for a compact decision packet: conclusion, exact paths/symbols/URLs, constraints, residual uncertainty, and next action; omit search narration, large excerpts, exhaustive inventories, and successful logs. Keep work direct only when its answer and target are already known, it is tightly coupled to a main-owned product/integration/Git/singleton action, or dispatch costs more context than the task.
Give subagents anchored briefs and disjoint write sets. Researcher, architect, code-reviewer, and QA roles are report-only and receive no write set; their `permissionMode = plan` and restricted tools are intent, while the parent permission context can take precedence. Implementers use the bundled `maintainable-code` skill while writing; code-reviewer uses its review branch before QA. Each write-capable role receives only its approved bounded write set. Delegation is main-mediated: every worker returns to the main thread, worker recommendations are advisory, and only the main thread selects and dispatches the next capability. Subagents never invoke the Agent tool or spawn children. When independent work is ready, the main thread may dispatch one parallel wave only with a stable contract, disjoint scopes, no result dependency, and a clear join condition; otherwise keep it serial. For material Execute work, prefer a matching project-local role for useful bounded research, architecture, implementation, review, testing, or another capability with a clear boundary, especially read-heavy or independent work that can safely run in parallel. Dispatch that role before the main thread duplicates the work. Reread the selected `.claude/agents/*.md` before each wave; changed values apply to new subagents, while running workers keep their creation profile. Use current project-local values; never substitute a personal/global role. If a role is absent in the active worktree, refresh only the ignored project-local agent files from the source checkout through the repository's propagation convention, then use `Direct: <reason>` only if it remains unavailable. Record `delegation_roles` and `delegation_status` in the compact checkpoint resume record and restore them after compaction. Emit one compact dispatch line with role names, configured models/efforts, and short assignments; omit routine status and standard-boundary narration. Tiny and inherently main-owned actions need no `Direct:` note. Claude model and effort choices remain adjustable; do not copy Codex model slugs into these files. Claude's automatic delegation matches descriptions; name a role in the dispatch prompt or use `@agent-<role>` for an explicit one-task invocation. `--agent` makes that role the main session agent, not a worker dispatch. Claude Code hot-reloads edits to an existing `.claude/agents/` directory; restart or start a fresh session after creating the directory for the first time. Plumbline does not edit global Claude settings or enable experimental Agent Teams.
When `AGENTS.md` contains provider-specific instructions, follow only provider-neutral or Claude-labeled guidance; do not apply Codex-only TOML, model, or configuration syntax.
Model values are provider-versioned inputs. Before initialization or an explicit
profile refresh, resolve the current Claude alias or full model ID from the host
model picker or Anthropic's official model documentation/API; use that
provider-native value. `inherit` is the non-pinned fallback, not a claim about
the current model suite, and Codex IDs never cross providers. A profile refresh
changes only explicitly approved `model` and `effort` fields; preserve the other
role fields and workers already running.
Keep an in-flight worker active until the host reports a terminal result. Do not kill, abandon, or duplicate work because of elapsed time, silence, compaction, or an intermediate status; reconcile an observer timeout before recovery. Replace work only after a confirmed terminal/API/transport failure, explicit user stop, obsolete scope, or safety issue.
Treat role profiles as reusable but worker instances as disposable: retire each terminal worker and dispatch a fresh instance for any new checkpoint, correction, failure, or acceptance task, even when selecting the same role. A follow-up is only for the exact same unfinished assignment when continuity materially helps; all new work gets a fresh instance. Use the host's fresh-child path. Never kill an active worker because it is quiet or compacting.
Before delegation or a material plan write, compact only when a live plan contains duplicate cards, an attempt diary, raw evidence, or superseded status; retain the current outcome, proof pointers, blockers or residuals, and next action. Clean plans, sufficient imported plans, and small direct work need no rewrite. After a material mutation, verify one current card per checkpoint and one current checkpoint in the resume record.
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


def _prepare_claude_import(repo: Path, *, agents_created: bool = False) -> tuple[Path, str] | None:
    """Return a CLAUDE.md proposal that imports the shared AGENTS.md guidance."""
    agents = repo / "AGENTS.md"
    if not agents.is_file() and not agents_created:
        return None
    target = repo / CLAUDE_GUIDANCE_FILE
    text = target.read_text(encoding="utf-8") if target.is_file() else "# CLAUDE.md\n"
    if any(line.strip() == CLAUDE_AGENTS_IMPORT for line in text.splitlines()):
        return target, text
    return target, text.rstrip() + f"\n\n{CLAUDE_AGENTS_IMPORT}\n"


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
            claude = repo / CLAUDE_GUIDANCE_FILE
            if not claude.is_file():
                findings.append(f"{claude}: missing {CLAUDE_AGENTS_IMPORT} import for Claude project guidance")
            else:
                claude_text = claude.read_text(encoding="utf-8")
                if not any(line.strip() == CLAUDE_AGENTS_IMPORT for line in claude_text.splitlines()):
                    findings.append(f"{claude}: missing {CLAUDE_AGENTS_IMPORT} import for Claude project guidance")
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
    pointer = _prepare_claude_import(repo, agents_created=True)
    if pointer:
        pointer_target, pointer_proposed = pointer
        pointer_current = pointer_target.read_text(encoding="utf-8") if pointer_target.is_file() else ""
        if pointer_current != pointer_proposed:
            changes[pointer_target] = (CLAUDE_AGENTS_IMPORT + " import",)
            operations[pointer_target] = "modify" if pointer_target.exists() else "create"
            if not dry_run:
                _write(pointer_target, pointer_proposed)
    return InstallReport(changes, tuple(findings), operations, requires_replace=requires_replace)


def _retune(
    plugin: Path,
    repo: Path,
    roles: tuple[str, ...],
    *,
    model: str | None,
    effort: str | None,
    fill_missing: bool,
    update_instructions: bool,
    update_profile: bool,
    dry_run: bool,
) -> InstallReport:
    if update_profile and (model is None or effort is None):
        raise ValueError("--update-profile requires --model and --effort")
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
        role_model, role_effort = _profile(role, model, effort)
        if fill_missing:
            template = _template_data(plugin, role)
            defaults = {
                "name": role,
                "description": str(template["description"]),
                "model": role_model,
                "effort": role_effort,
                "tools": ROLE_TOOLS[role],
                "permissionMode": ROLE_PERMISSION_MODES[role],
            }
            missing = {key: value for key, value in defaults.items() if key not in values}
            after = _append_missing_fields(after, missing, path)
            changed.extend(missing)
        if update_profile:
            profile_values = {"model": role_model, "effort": role_effort}
            profile_changes = {
                field: value
                for field, value in profile_values.items()
                if values.get(field) != value
            }
            if profile_changes:
                after = _set_frontmatter_values(after, profile_changes, path)
                changed.extend(profile_changes)
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
    model: str | None,
    effort: str | None,
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
        role_model, role_effort = _profile(role, model, effort)
        if not dry_run:
            _write(target, _render_agent(plugin, role, role_model, role_effort))
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
        pointer = _prepare_claude_import(repo, agents_created=True)
        if pointer:
            pointer_target, pointer_proposed = pointer
            pointer_current = pointer_target.read_text(encoding="utf-8") if pointer_target.is_file() else ""
            if pointer_current != pointer_proposed:
                if not dry_run:
                    _write(pointer_target, pointer_proposed)
                changes[pointer_target] = (CLAUDE_AGENTS_IMPORT + " import",)
                operations[pointer_target] = "modify" if pointer_target.exists() else "create"
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
    model: str | None = None,
    effort: str | None = None,
    roles: tuple[str, ...] = ROLES,
    replace: bool = False,
    fill_missing: bool = False,
    update_instructions: bool = False,
    update_profile: bool = False,
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
        if any((replace, fill_missing, update_instructions, update_profile, update_agents, refresh_agents, replace_guidance, propagate)):
            raise ValueError("audit is read-only; remove mutation flags")
        return _audit(repo, roles)
    if mode == "retune":
        if replace or update_agents or refresh_agents or replace_guidance or propagate:
            raise ValueError("retune preserves existing roles; use --update-profile, --update-instructions, or initialize for replacement, guidance, or propagation")
        return _retune(
            plugin,
            repo,
            roles,
            model=model,
            effort=effort,
            fill_missing=fill_missing,
            update_instructions=update_instructions,
            update_profile=update_profile,
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
    if fill_missing or update_instructions or update_profile:
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
        print("Approval required: rerun with --replace-agents-guidance after reviewing the proposed Claude guidance refresh.")
    if mode == "audit":
        print("Audit was read-only; no files were written.")
    print("Global Claude settings and experimental Agent Teams were not changed.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Target repository root")
    parser.add_argument("--mode", choices=MODES, default="initialize")
    parser.add_argument("--model", help="Current Claude model alias or full model ID")
    parser.add_argument("--effort", "--reasoning-effort", dest="effort", help="Claude reasoning effort")
    parser.add_argument("--roles", type=_parse_roles, default=ROLES, help="Comma-separated roles")
    parser.add_argument("--replace", action="store_true", help="Replace existing role files during initialize only")
    parser.add_argument("--fill-missing", action="store_true", help="Retune by adding missing frontmatter only")
    parser.add_argument("--update-instructions", action="store_true", help="Retune by explicitly updating instructions")
    parser.add_argument(
        "--update-profile",
        action="store_true",
        help="Retune only the explicitly approved model and effort fields",
    )
    parser.add_argument(
        "--update-agents",
        action="store_true",
        help="Add approved Claude guidance in AGENTS.md and import it from CLAUDE.md",
    )
    parser.add_argument(
        "--refresh-agents",
        action="store_true",
        help="During an explicit initialization rerun, refresh only managed Claude guidance and its CLAUDE.md import",
    )
    parser.add_argument(
        "--replace-agents-guidance",
        action="store_true",
        help="Allow explicit replacement of a stale unmarked Claude guidance section",
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
            update_profile=args.update_profile,
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
