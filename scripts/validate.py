#!/usr/bin/env python3
"""Run static structural and content checks for the Plumbline plugin.

This validates configuration and workflow intent; it does not prove effective
permissions or sandbox state in a spawned Codex session.
"""

from __future__ import annotations

import json
import re
import sys
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = {
    "plumbline",
    "plumbline-init",
    "plumbline-shape",
    "plumbline-spec",
    "plumbline-plan",
    "plumbline-execute",
    "plumbline-diagnose",
    "plumbline-review",
    "plumbline-closeout",
    "plumbline-agent-team",
    "plumbline-offboard",
}
ENGINES = {f"{name}-engine" for name in {
    "plumbline-shape",
    "plumbline-spec",
    "plumbline-plan",
    "plumbline-execute",
    "plumbline-diagnose",
    "plumbline-review",
    "plumbline-closeout",
}}
ENGINES.add("plumbline-plan-adoption-engine")
EXPECTED_SKILLS = PUBLIC | ENGINES
EXPLICIT = PUBLIC
AGENT_ROLES = {
    "researcher",
    "backend-architect",
    "frontend-architect",
    "implementer",
    "qa-auditor",
}
AGENT_SANDBOXES = {
    "researcher": "read-only",
    "backend-architect": "read-only",
    "frontend-architect": "read-only",
    "implementer": "workspace-write",
    "qa-auditor": "read-only",
}
CONTRACT_MARKERS = {
    "plumbline-init": (
        "wait for explicit approval",
        "personal/global custom-agent files",
        "user-owned",
        "scripts/install_agent_team.py",
        "dry-run",
        "gitignore",
        "preflight repository",
        "targeted",
        ".worktreeinclude",
        "writable parent",
        "available, not active",
        "refresh-agents",
        "replace-agents-guidance",
        "guidance-only refresh",
    ),
    "plumbline-agent-team": (
        ".codex/agents/",
        "personal/global agent files",
        "user-owned",
        "main-mediated",
        "recommendations are advisory",
        "spawn children",
        "scripts/install_agent_team.py",
        "dry-run",
        "gitignore",
        "selected roles",
        "report-only roles",
        "main-mediated",
        "parallel wave",
        "stable contract",
        "join condition",
        "cannot override lifecycle invariants",
        "CHANGES_REQUIRED",
        "same candidate",
        "successor objective",
        "advisory",
        "effective sandbox",
        "no write set",
        "router",
        "AGENTS schema drift",
        "proposed refresh",
        "repeat initialization",
        "replace-agents-guidance",
    ),
    "plumbline-execute-engine": (
        "last_verified_commit",
        "known unrelated baseline",
        "one lifecycle owner",
        "parallel wave",
        "compact resume record",
        "resume fingerprint",
        "does not invalidate evidence",
        "subagent-orchestration.md",
        "installation root",
        "compact state/transition line",
        "coherent boundary",
        "evidence-only",
        "stable-delta",
        "ready for acceptance",
        "recovery, validation, authorization, or ownership",
        "artifact sufficiency preflight",
        "user-supplied or repository-local",
        "companion plan",
        "exactly one current checkpoint",
        "timestamped sample",
        "delegation-first ownership",
        "delegation_roles",
        "delegation_status",
        "bounded work unit",
        "every required checkpoint is `Complete`",
        "blocked or reopened",
        "returns to Diagnose",
        "candidate or objective",
        "successor objective",
        "failure-path trace",
        "surface patch",
        "execution_mode",
        "missing value means `continuous`",
        "checkpoint_relay",
        "checkpoint-relay.md",
        "proof obligations",
        "test count and coverage are signals",
    ),
    "plumbline-diagnose-engine": (
        "same candidate",
        "correction path",
        "select a successor",
        "evidence path",
        "minimum sufficient root cause",
        "failure-path trace",
        "Local cause confirmed",
        "green rerun",
        "fix boundary",
        "diagnostic tests and probes",
        "durable regression",
    ),
    "plumbline-diagnose": (
        "minimum sufficient root cause",
        "trace the minimum sufficient root cause",
    ),
    "plumbline-plan-engine": (
        "evidence-only",
        "independent outcome",
        "do not split a coherent outcome",
        "compact checkpoint card",
        "kickoff or recovery-boundary commit",
        "planning is artifact-agnostic",
        "external plan or work order",
        "competing candidates",
        "current checkpoint",
        "ready independent",
        "parallel waves",
        "join condition",
        "cannot override Plumbline lifecycle invariants",
        "CHANGES_REQUIRED",
        "same candidate",
        "successor objective",
        "execution_mode: continuous",
        "execution_mode: checkpoint_relay",
        "checkpoint-relay.md",
        "proof obligation",
        "test-count target",
    ),
    "plumbline-plan-adoption-engine": (
        "smallest companion live plan",
        "relay_compatible",
        "adoptable",
        "insufficient",
        "source as authority",
        "checkpoint_relay",
        "relay-readiness.js",
        "main lifecycle owner",
        "Stage and commit only",
        "exactly one checkable result",
    ),
    "plumbline-spec-engine": (
        "controlling product specification",
        "sufficiency",
        "external",
        "do not require",
        "competing",
        "blocking product questions",
    ),
    "plumbline-review-engine": (
        "qa-auditor",
        "personal/global qa agent",
        "direct: qa-auditor unavailable",
        "workers never spawn children",
        "report-only",
        "no write set",
        "effective sandbox",
        "direct: delegation prohibited or effective read-only isolation unavailable",
        "delegated wave:",
        "small, low-risk",
        "main thread",
        "parallel wave",
        "CHANGES_REQUIRED",
        "reopens",
        "candidate terminality",
        "failure path",
        "adjacent proof",
        "implementation-shape",
        "test count or coverage",
    ),
    "plumbline-shape-engine": (
        "external research",
        "shaping handoff",
        "not yet specified",
        "one question at a time",
        "bounded batch",
        "❓ **Q1**",
        "➡️ **Recommendation:**",
        "decision frontier",
        "lightweight decision map",
        "highest-leverage frontier question",
        "personal or global agent",
        "optional prototype probe",
        "conversation, worked example",
        "no persistence by default",
        "existing handoff",
    ),
    "plumbline-closeout-engine": (
        "light closeout",
        "full closeout",
        "smallest closeout mode",
        "transient specification/plan cleanup",
        "execute owns implementation",
        "ready for acceptance",
        "transient cleanup",
        "acceptance-led",
        "does not require an active",
        "acceptance blocker",
        "accepted work",
        "Blocked",
        "Reopened",
        "refuses to retire",
        "explicit user approval",
        "candidate-scoped",
        "diagnostic-only evidence",
    ),
    "plumbline": (
        "one lifecycle owner",
        "do not stack a second lifecycle controller",
        "installed or enabled skills alone",
        "plumbline-init",
        "project-local Plumbline router",
        "versioned cache paths",
        "compact resume record",
        "controlling work order",
        "contract-complete work",
        "convention mode",
        "artifact sufficiency check",
        "controlling artifact set",
        "not a prerequisite",
        "explicitly invoked phase side door",
        "missing `execution_mode` means normal continuous",
        "checkpoint_relay",
    ),
}
WRAPPERS = {
    "plumbline-shape",
    "plumbline-spec",
    "plumbline-plan",
    "plumbline-execute",
    "plumbline-diagnose",
    "plumbline-review",
    "plumbline-closeout",
}
REFERENCES = {
    "work-classification.md",
    "product-autonomy.md",
    "research-policy.md",
    "artifact-lifecycle.md",
    "specification-template.md",
    "plan-schema.md",
    "runtime-value-testing.md",
    "subagent-orchestration.md",
    "worktree-readiness.md",
    "qa-audit.md",
    "canonical-documentation.md",
    "conflict-audit.md",
    "offboarding.md",
    "router-installation.md",
    "checkpoint-relay.md",
}
FRONTMATTER_FIELD = re.compile(r"^(name|description):\s*(.+?)\s*$", re.MULTILINE)
SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")


def error(errors: list[str], message: str) -> None:
    errors.append(message)


def frontmatter(path: Path, errors: list[str]) -> tuple[str, str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        error(errors, f"{path.relative_to(ROOT)}: missing YAML frontmatter")
        return "", "", text
    end = text.find("\n---", 4)
    if end < 0:
        error(errors, f"{path.relative_to(ROOT)}: unterminated YAML frontmatter")
        return "", "", text
    head = text[4:end]
    values = dict(FRONTMATTER_FIELD.findall(head))
    if not values.get("name") or not values.get("description"):
        error(errors, f"{path.relative_to(ROOT)}: name and description are required")
    return values.get("name", ""), values.get("description", ""), text[end + 4 :]


def validate_manifest(errors: list[str]) -> None:
    path = ROOT / ".codex-plugin" / "plugin.json"
    if not path.is_file():
        error(errors, "missing .codex-plugin/plugin.json")
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    for key in ("name", "version", "description", "author", "skills", "interface"):
        if key not in data:
            error(errors, f"manifest missing {key}")
    if data.get("name") != "plumbline" or not SEMVER.fullmatch(data.get("version", "")):
        error(errors, "manifest name/version is invalid")
    if data.get("skills") != "./skills/":
        error(errors, "manifest skills must be ./skills/")
    if data.get("hooks") != "./hooks/hooks.json":
        error(errors, "manifest hooks must be ./hooks/hooks.json")
    if any(key in data for key in ("apps", "mcpServers")):
        error(errors, "Plumbline must not declare apps or MCP servers")
    interface = data.get("interface", {})
    for key in ("displayName", "shortDescription", "longDescription", "developerName", "category", "capabilities", "defaultPrompt"):
        if not interface.get(key):
            error(errors, f"manifest interface missing {key}")
    for key in ("composerIcon", "logo"):
        asset = ROOT / interface.get(key, "")
        if not asset.is_file():
            error(errors, f"manifest asset missing: {key}")


def validate_claude_manifest(errors: list[str]) -> None:
    path = ROOT / ".claude-plugin" / "plugin.json"
    if not path.is_file():
        error(errors, "missing .claude-plugin/plugin.json")
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        error(errors, f".claude-plugin/plugin.json: invalid JSON: {exc}")
        return
    for key in ("name", "description", "version", "author", "skills"):
        if key not in data:
            error(errors, f"Claude plugin manifest missing {key}")
    if data.get("name") != "plumbline" or not SEMVER.fullmatch(data.get("version", "")):
        error(errors, "Claude plugin manifest name/version is invalid")
    if not isinstance(data.get("author"), dict) or not data.get("author", {}).get("name"):
        error(errors, "Claude plugin manifest author.name is required")
    expected = [f"./skills/{name}" for name in sorted(PUBLIC)]
    if sorted(data.get("skills", [])) != expected:
        error(errors, "Claude plugin manifest must expose only the public Plumbline skills")


def validate_hooks(errors: list[str]) -> None:
    path = ROOT / "hooks" / "hooks.json"
    script = ROOT / "hooks" / "plumbline-session.js"
    relay_script = ROOT / "hooks" / "plumbline-relay-signal.js"
    if not path.is_file() or not script.is_file() or not relay_script.is_file():
        error(errors, "continuity hook files are required")
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        error(errors, f"hooks/hooks.json: invalid JSON: {exc}")
        return
    hooks = data.get("hooks")
    if not isinstance(hooks, dict) or set(hooks) != {"UserPromptSubmit", "SessionStart", "Stop"}:
        error(errors, "hooks/hooks.json must contain only UserPromptSubmit, SessionStart, and Stop")
        return
    for event in ("UserPromptSubmit", "SessionStart", "Stop"):
        groups = hooks.get(event)
        if not isinstance(groups, list) or len(groups) != 1:
            error(errors, f"hooks/hooks.json: {event} must have one matcher group")
            continue
        group = groups[0]
        if event == "SessionStart" and group.get("matcher") != "^(resume|compact)$":
            error(errors, "hooks/hooks.json: SessionStart must match only resume and compact")
        handlers = group.get("hooks")
        if not isinstance(handlers, list) or len(handlers) != 1:
            error(errors, f"hooks/hooks.json: {event} must have one command handler")
            continue
        handler = handlers[0]
        command = handler.get("command", "")
        expected_script = "plumbline-relay-signal.js" if event == "Stop" else "plumbline-session.js"
        if handler.get("type") != "command" or expected_script not in command:
            error(errors, f"hooks/hooks.json: {event} must run {expected_script}")
        if "CLAUDE_PLUGIN_ROOT" not in command:
            error(errors, f"hooks/hooks.json: {event} must resolve from the installed plugin root")
    source = script.read_text(encoding="utf-8")
    for marker in (
        "UserPromptSubmit",
        "SessionStart",
        "not a new invocation",
        "session_id",
        "cwd",
        "delegation_roles",
        "delegation_status",
    ):
        if marker not in source:
            error(errors, f"hooks/plumbline-session.js: missing marker {marker}")
    relay_source = relay_script.read_text(encoding="utf-8")
    for marker in ("signalRelay",):
        if marker not in relay_source:
            error(errors, f"hooks/plumbline-relay-signal.js: missing marker {marker}")


def validate_marketplace(errors: list[str]) -> None:
    path = ROOT / ".agents" / "plugins" / "marketplace.json"
    if not path.is_file():
        error(errors, "missing repo marketplace")
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("name") != "plumbline":
        error(errors, "repo marketplace name must be plumbline")
    if data.get("interface", {}).get("displayName") != "Plumbline":
        error(errors, "repo marketplace displayName must be Plumbline")
    entries = [entry for entry in data.get("plugins", []) if entry.get("name") == "plumbline"]
    if len(entries) != 1:
        error(errors, "marketplace must contain one Plumbline entry")
        return
    entry = entries[0]
    if entry.get("source", {}).get("path") != "./":
        error(errors, "root plugin marketplace path must be ./")
    for key in ("installation", "authentication"):
        if key not in entry.get("policy", {}):
            error(errors, f"marketplace policy missing {key}")
    if entry.get("category") != "Coding":
        error(errors, "marketplace category must be Coding")
    if not (ROOT / ".codex-plugin" / "plugin.json").is_file():
        error(errors, "marketplace root does not contain the plugin manifest")


def validate_claude_marketplace(errors: list[str]) -> None:
    path = ROOT / ".claude-plugin" / "marketplace.json"
    if not path.is_file():
        error(errors, "missing Claude marketplace")
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        error(errors, f".claude-plugin/marketplace.json: invalid JSON: {exc}")
        return
    if data.get("name") != "plumbline":
        error(errors, "Claude marketplace name must be plumbline")
    if not isinstance(data.get("owner"), dict) or not data.get("owner", {}).get("name"):
        error(errors, "Claude marketplace owner.name is required")
    entries = [entry for entry in data.get("plugins", []) if entry.get("name") == "plumbline"]
    if len(entries) != 1:
        error(errors, "Claude marketplace must contain one Plumbline entry")
        return
    entry = entries[0]
    if entry.get("source") != "./":
        error(errors, "Claude marketplace root plugin source must be ./")
    if entry.get("category") != "development":
        error(errors, "Claude marketplace category must be development")
    expected = [f"./skills/{name}" for name in sorted(PUBLIC)]
    if sorted(entry.get("skills", [])) != expected:
        error(errors, "Claude marketplace must expose only the public Plumbline skills")
    if not (ROOT / ".claude-plugin" / "plugin.json").is_file():
        error(errors, "Claude marketplace root does not contain the plugin manifest")


def validate_skills(errors: list[str]) -> None:
    skills_root = ROOT / "skills"
    actual = {path.name for path in skills_root.iterdir() if path.is_dir()}
    if actual != EXPECTED_SKILLS:
        error(errors, f"skill set differs; missing={sorted(EXPECTED_SKILLS - actual)}, extra={sorted(actual - EXPECTED_SKILLS)}")
    for name in sorted(EXPECTED_SKILLS):
        skill_root = skills_root / name
        skill_path = skill_root / "SKILL.md"
        policy_path = skill_root / "agents" / "openai.yaml"
        if not skill_path.is_file() or not policy_path.is_file():
            error(errors, f"{name}: SKILL.md and agents/openai.yaml are required")
            continue
        front_name, _description, body = frontmatter(skill_path, errors)
        if front_name != name:
            error(errors, f"{name}: frontmatter name does not match folder")
        text = skill_path.read_text(encoding="utf-8")
        if "[TODO:" in text or "session-start" in text.lower() or "using-superpowers" in text.lower():
            error(errors, f"{name}: contains forbidden placeholder/bootstrap text")
        if name in PUBLIC and "disable-model-invocation: true" not in text:
            error(errors, f"{name}: public entry skills must remain explicit-only for Claude Code")
        policy = policy_path.read_text(encoding="utf-8")
        expected = "false" if name in EXPLICIT else "true"
        if f"allow_implicit_invocation: {expected}" not in policy:
            error(errors, f"{name}: expected allow_implicit_invocation={expected}")
        if name in ENGINES and "Internal Plumbline engine" not in text:
            error(errors, f"{name}: engine marker missing")
        if name in WRAPPERS and "user-facing wrapper" not in text:
            error(errors, f"{name}: wrapper marker missing")
        for reference in re.findall(r"references/([a-z0-9-]+\.md)", text):
            if not (ROOT / "references" / reference).is_file():
                error(errors, f"{name}: missing referenced file {reference}")
        if "must use TDD" in text or "always use TDD" in text:
            error(errors, f"{name}: contains universal TDD language")
        for marker in CONTRACT_MARKERS.get(name, ()):
            if marker.lower() not in text.lower():
                error(errors, f"{name}: missing contract marker {marker}")


def validate_references_and_templates(errors: list[str]) -> None:
    actual = {path.name for path in (ROOT / "references").glob("*.md")}
    if actual != REFERENCES:
        error(errors, f"reference set differs; missing={sorted(REFERENCES - actual)}, extra={sorted(actual - REFERENCES)}")
    relay_contract = (ROOT / "references" / "checkpoint-relay.md").read_text(encoding="utf-8")
    for marker in (
        "A missing `execution_mode` means `continuous`",
        "checkpoint_relay",
        "automatic",
        "manual",
        "Ordinary continuous Execute remains unchanged",
        "PLUMBLINE_RELAY_CHECKPOINT",
        "runtime/run-relay.js",
        "semantic durability check",
        "generic handoff file",
        "existing authoritative",
    ):
        if marker not in relay_contract:
            error(errors, f"references/checkpoint-relay.md: missing {marker}")
    for forbidden in ("App Server", "thread/start", "turn/start"):
        if forbidden in relay_contract:
            error(errors, f"references/checkpoint-relay.md: host transport leaked into shared contract: {forbidden}")
    orchestration = (ROOT / "references" / "subagent-orchestration.md").read_text(encoding="utf-8")
    for marker in (
        ".codex/agents/",
        "personal/global agent files",
        "Delegated wave:",
        "reasoning=<effort>",
        "report-only",
        "no write set",
        "never create children",
        "fork_turns",
        "root-cause capsule",
        "parallel only after shared contracts are stable",
    ):
        if marker.lower() not in orchestration.lower():
            error(errors, f"references/subagent-orchestration.md: missing {marker}")
    reference_markers = {
        "runtime-value-testing.md": ("behavioral proof obligations", "test count and coverage"),
        "plan-schema.md": ("behavioral proof obligations", "test-count or coverage"),
        "qa-audit.md": ("proof obligation", "main thread decides deletion"),
    }
    for name, markers in reference_markers.items():
        source = (ROOT / "references" / name).read_text(encoding="utf-8").lower()
        for marker in markers:
            if marker.lower() not in source:
                error(errors, f"references/{name}: missing {marker}")
    router = ROOT / "templates" / "router" / "SKILL.md"
    _name, _description, body = frontmatter(router, errors)
    if len(re.findall(r"\b[\w'-]+\b", body)) > 180:
        error(errors, "router exceeds the 180-word budget")
    router_text = router.read_text(encoding="utf-8")
    if "plumbline-router" not in router_text:
        error(errors, "router template is missing its activation identity")
    for marker in (
        "invoke the installed `$plumbline` front door",
        "Never substitute a `plumbline-*-engine` skill",
        "Direct: Plumbline front door unavailable",
    ):
        if marker not in router_text:
            error(errors, f"router template is missing handoff marker {marker}")
    agents_root = ROOT / "templates" / "agents"
    actual_roles = {path.stem for path in agents_root.glob("*.toml") if path.name != "config.toml"}
    if actual_roles != AGENT_ROLES:
        error(errors, f"agent template set differs; missing={sorted(AGENT_ROLES - actual_roles)}, extra={sorted(actual_roles - AGENT_ROLES)}")
    for role in sorted(AGENT_ROLES):
        path = agents_root / f"{role}.toml"
        if not path.is_file():
            error(errors, f"missing agent template: {path.relative_to(ROOT)}")
            continue
        try:
            data = tomllib.loads(path.read_text(encoding="utf-8"))
        except tomllib.TOMLDecodeError as exc:
            error(errors, f"{path.relative_to(ROOT)}: invalid TOML: {exc}")
            continue
        for key in ("name", "description", "developer_instructions", "model", "model_reasoning_effort", "sandbox_mode"):
            if not isinstance(data.get(key), str) or not data[key].strip():
                error(errors, f"{path.relative_to(ROOT)}: missing {key}")
        source = path.read_text(encoding="utf-8")
        if data.get("name") != role:
            error(errors, f"{path.relative_to(ROOT)}: name must be {role}")
        if data.get("model") != "{{MODEL}}" or "{{MODEL}}" not in source:
            error(errors, f"{path.relative_to(ROOT)}: model placeholder is required")
        if data.get("model_reasoning_effort") != "{{REASONING_EFFORT}}" or "{{REASONING_EFFORT}}" not in source:
            error(errors, f"{path.relative_to(ROOT)}: reasoning placeholder is required")
        if data.get("sandbox_mode") != AGENT_SANDBOXES[role]:
            error(errors, f"{path.relative_to(ROOT)}: sandbox must be {AGENT_SANDBOXES[role]}")
        if "never spawn child agents" not in data.get("developer_instructions", "").lower():
            error(errors, f"{path.relative_to(ROOT)}: child-spawn boundary is required")
        instructions = data.get("developer_instructions", "").lower()
        if "main thread" not in instructions or "dispatch another worker" not in instructions:
            error(errors, f"{path.relative_to(ROOT)}: main-mediated delegation boundary is required")
        if role != "implementer":
            if "report-only" not in instructions:
                error(errors, f"{path.relative_to(ROOT)}: report-only boundary is required")
            if "no write set" not in instructions:
                error(errors, f"{path.relative_to(ROOT)}: no-write-set boundary is required")

    config_path = agents_root / "config.toml"
    try:
        config = tomllib.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        error(errors, f"{config_path.relative_to(ROOT)}: invalid or missing TOML: {exc}")
    else:
        agents = config.get("agents", {})
        if agents.get("enabled") is not True:
            error(errors, "templates/agents/config.toml: agents.enabled must be true")
        max_threads = agents.get("max_concurrent_threads_per_session")
        if type(max_threads) is not int or max_threads < 1:
            error(
                errors,
                "templates/agents/config.toml: max_concurrent_threads_per_session must be a positive integer",
            )
        for table, key in (("features", "multi_agent"), ("agents", "max_threads"), ("agents", "max_depth")):
            if key in config.get(table, {}):
                error(errors, f"templates/agents/config.toml: legacy {table}.{key} must not be present")

    worktreeinclude = agents_root / "worktreeinclude"
    try:
        include_text = worktreeinclude.read_text(encoding="utf-8")
    except OSError as exc:
        error(errors, f"{worktreeinclude.relative_to(ROOT)}: missing: {exc}")
    else:
        for pattern in (".codex/config.toml", ".codex/agents/*.toml", ".agents/skills/plumbline-router/**"):
            if pattern not in include_text:
                error(errors, f"{worktreeinclude.relative_to(ROOT)}: missing {pattern}")


def validate_scripts(errors: list[str]) -> None:
    for name in (
        "validate.py",
        "install_router.py",
        "install_agent_team.py",
        "test_install_agent_team.py",
        "install_claude_agent_team.py",
        "test_install_claude_agent_team.py",
        "test_plumbline_hook.py",
        "test_checkpoint_relay.py",
    ):
        path = ROOT / "scripts" / name
        try:
            source = path.read_text(encoding="utf-8")
            compile(source, str(path), "exec")
            if name == "install_agent_team.py":
                for marker in ("MODES = (\"initialize\", \"audit\", \"retune\")", "class InstallReport", "ROLE_DESCRIPTIONS", "def _retune", "def _audit_router", "def _audit_agents_guidance", "update_instructions", "dry_run", "output_format", "Delegated wave:", "model slugs", "reasoning efforts"):
                    if marker not in source:
                        error(errors, f"scripts/{name}: missing preservation marker {marker}")
            elif name == "install_claude_agent_team.py":
                for marker in ("AGENT_ROOT", "ROLE_TOOLS", "permissionMode", "def _retune", "dry_run", "claude_settings_modified", "experimental_agent_teams_enabled"):
                    if marker not in source:
                        error(errors, f"scripts/{name}: missing Claude adapter marker {marker}")
            elif name == "install_router.py":
                for marker in ("dry_run", "output_format", "router template", "requires_replace"):
                    if marker not in source:
                        error(errors, f"scripts/{name}: missing dry-run marker {marker}")
            elif name == "test_plumbline_hook.py":
                for marker in ("SessionStart", "UserPromptSubmit", "compact", "front door", "isolation"):
                    if marker.lower() not in source.lower():
                        error(errors, f"scripts/{name}: missing hook test marker {marker}")
            elif name == "test_checkpoint_relay.py":
                for marker in ("relay_ready", "relay_compatible", "git", "next_safe_action"):
                    if marker not in source:
                        error(errors, f"scripts/{name}: missing Relay test marker {marker}")
        except (OSError, SyntaxError) as exc:
            error(errors, f"scripts/{name}: {exc}")

    for name in (
        "relay-readiness.js",
        "relay-core.js",
        "relay-signal.js",
        "test-relay-core.js",
        "codex-app-server.js",
        "run-relay.js",
        "fake-app-server.js",
        "test-codex-adapter.js",
    ):
        path = ROOT / "runtime" / name
        if not path.is_file():
            error(errors, f"runtime/{name}: missing")
            continue
        source = path.read_text(encoding="utf-8")
        if name == "relay-core.js":
            for marker in ("RelayLockError", "automatic_relay", "manual_boundary", "handoff_ready", "validateTransition"):
                if marker not in source:
                    error(errors, f"runtime/{name}: missing relay-core marker {marker}")
        elif name == "codex-app-server.js":
            for marker in ("initialize", "initialized", "thread/start", "thread/name/set", "turn/start", "turn/completed", "thread/read", "skills/list"):
                if marker not in source:
                    error(errors, f"runtime/{name}: missing App Server marker {marker}")


def main() -> int:
    errors: list[str] = []
    validate_manifest(errors)
    validate_claude_manifest(errors)
    validate_hooks(errors)
    validate_marketplace(errors)
    validate_claude_marketplace(errors)
    validate_skills(errors)
    validate_references_and_templates(errors)
    validate_scripts(errors)
    if errors:
        print("Plumbline validation failed:")
        for message in errors:
            print(f"- {message}")
        return 1
    print(f"Plumbline validation passed: {ROOT}")
    print(f"- skills: {len(EXPECTED_SKILLS)} ({len(PUBLIC)} public, {len(ENGINES)} internal engines)")
    print(f"- references: {len(REFERENCES)}")
    print("- Codex marketplace: plumbline; root plugin path ./")
    print("- Claude marketplace: plumbline; public skills plus project-local agent adapter")
    print("- scope: static configuration/workflow intent; not effective child-permission enforcement")
    return 0


if __name__ == "__main__":
    sys.exit(main())
