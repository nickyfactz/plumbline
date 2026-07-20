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
        "max_depth = 1",
        "scripts/install_agent_team.py",
        ".worktreeinclude",
        "writable parent",
        "available, not active",
    ),
    "plumbline-agent-team": (
        ".codex/agents/",
        "personal/global agent files",
        "max_depth = 1",
        "spawn children",
        "scripts/install_agent_team.py",
        "report-only roles",
        "effective sandbox",
        "no write set",
        "router",
        "AGENTS schema drift",
        "proposed refresh",
    ),
    "plumbline-execute-engine": (
        ".codex/agents/",
        "personal/global custom agents",
        "delegated wave:",
        "model slug",
        "reasoning effort",
        "workers never spawn children",
        "report-only roles",
        "effective sandbox",
        "no write set",
        "last_verified_commit",
        "known unrelated baseline failure",
        "one lifecycle owner",
        "compact resume record",
        "installation root",
        "compact state/transition line",
        "coherent implementation commit",
        "evidence-only follow-up commits",
    ),
    "plumbline-plan-engine": (
        "evidence-only",
        "independent outcome",
        "do not split a coherent outcome",
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
    ),
    "plumbline-shape-engine": (
        "external research",
        "shaping handoff",
        "not yet specified",
        "one question at a time",
        "personal or global agent",
    ),
    "plumbline": (
        "one lifecycle owner",
        "do not stack a second lifecycle controller",
        "installed or enabled skills alone",
        "versioned cache paths",
        "compact resume record",
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
    if any(key in data for key in ("hooks", "apps", "mcpServers")):
        error(errors, "v1 manifest must not declare hooks, apps, or MCP servers")
    interface = data.get("interface", {})
    for key in ("displayName", "shortDescription", "longDescription", "developerName", "category", "capabilities", "defaultPrompt"):
        if not interface.get(key):
            error(errors, f"manifest interface missing {key}")
    for key in ("composerIcon", "logo"):
        asset = ROOT / interface.get(key, "")
        if not asset.is_file():
            error(errors, f"manifest asset missing: {key}")


def validate_marketplace(errors: list[str]) -> None:
    path = ROOT / ".agents" / "plugins" / "marketplace.json"
    if not path.is_file():
        error(errors, "missing repo marketplace")
        return
    data = json.loads(path.read_text(encoding="utf-8"))
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
    router = ROOT / "templates" / "router" / "SKILL.md"
    _name, _description, body = frontmatter(router, errors)
    if len(re.findall(r"\b[\w'-]+\b", body)) > 180:
        error(errors, "router exceeds the 180-word budget")
    router_text = router.read_text(encoding="utf-8")
    if "plumbline-router" not in router_text:
        error(errors, "router template is missing its activation identity")
    if "installed `plumbline` front door" not in router_text:
        error(errors, "router template must hand off to the installed Plumbline front door")
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
        if role != "implementer":
            instructions = data.get("developer_instructions", "").lower()
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
        if config.get("features", {}).get("multi_agent") is not True:
            error(errors, "templates/agents/config.toml: multi_agent must be true")
        if config.get("agents", {}).get("max_threads") != 6:
            error(errors, "templates/agents/config.toml: max_threads must be 6")
        if config.get("agents", {}).get("max_depth") != 1:
            error(errors, "templates/agents/config.toml: max_depth must be 1")

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
    for name in ("validate.py", "install_router.py", "install_agent_team.py", "test_install_agent_team.py"):
        path = ROOT / "scripts" / name
        try:
            source = path.read_text(encoding="utf-8")
            compile(source, str(path), "exec")
            if name == "install_agent_team.py":
                for marker in ("MODES = (\"initialize\", \"audit\", \"retune\")", "class InstallReport", "def _retune", "def _audit_router", "def _audit_agents_guidance", "update_instructions", "Delegated wave:", "model slugs", "reasoning efforts"):
                    if marker not in source:
                        error(errors, f"scripts/{name}: missing preservation marker {marker}")
        except (OSError, SyntaxError) as exc:
            error(errors, f"scripts/{name}: {exc}")


def main() -> int:
    errors: list[str] = []
    validate_manifest(errors)
    validate_marketplace(errors)
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
    print("- marketplace: root plugin path ./")
    print("- scope: static configuration/workflow intent; not effective child-permission enforcement")
    return 0


if __name__ == "__main__":
    sys.exit(main())
