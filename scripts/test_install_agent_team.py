#!/usr/bin/env python3
"""Small stdlib smoke test for the project-local agent-team installer."""

from __future__ import annotations

import subprocess
import tempfile
import json
import sys
import tomllib
from pathlib import Path

from install_router import install as install_router
from install_agent_team import RECOMMENDED_PROFILES, ROLES, install


def run_git(*args: str, cwd: Path) -> None:
    subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def main() -> None:
    plugin_root = Path(__file__).resolve().parents[1]
    orchestration = (plugin_root / "references" / "subagent-orchestration.md").read_text(encoding="utf-8").lower()
    for marker in (
        "independent research",
        "architecture lenses",
        "qa lenses",
        "shares files",
        "clear join condition",
        "worker recommendation never creates a new delegation wave",
        "delegation-first ownership",
        "delegation_roles",
        "delegation_status",
        "bounded research",
        "worker instance as disposable",
        "fresh instance",
        "exact same unfinished assignment",
        "compact it in place first",
        "sufficient imported plan",
        "no appended chronology",
    ):
        assert marker in orchestration
    with tempfile.TemporaryDirectory() as raw_root:
        root = Path(raw_root)
        (root / ".git" / "info").mkdir(parents=True)
        install(
            plugin_root,
            root,
            model="gpt-5.6-luna",
            reasoning_effort="medium",
            max_threads=12,
            update_agents=True,
            propagate=True,
        )
        config = tomllib.loads((root / ".codex" / "config.toml").read_text(encoding="utf-8"))
        assert config["agents"]["enabled"] is True
        assert config["agents"]["max_concurrent_threads_per_session"] == 12
        assert "features" not in config
        assert "max_threads" not in config["agents"]
        assert "max_depth" not in config["agents"]
        for role in ROLES:
            data = tomllib.loads((root / ".codex" / "agents" / f"{role}.toml").read_text(encoding="utf-8"))
            assert data["model"] == "gpt-5.6-luna"
            assert data["model_reasoning_effort"] == "medium"
            assert data["sandbox_mode"]
            assert "spawn child" in data["developer_instructions"].lower()
            assert "main thread" in data["developer_instructions"].lower()
            assert "dispatch another worker" in data["developer_instructions"].lower()
        reviewer = tomllib.loads((root / ".codex" / "agents" / "code-reviewer.toml").read_text(encoding="utf-8"))
        assert "maintainable-code" in reviewer["developer_instructions"]
        qa = tomllib.loads((root / ".codex" / "agents" / "qa-auditor.toml").read_text(encoding="utf-8"))
        assert "acceptance" in qa["developer_instructions"].lower()
        assert "maintainable-code" not in qa["developer_instructions"]
        guidance = (root / "AGENTS.md").read_text(encoding="utf-8")
        assert "## Local agent team" in guidance
        assert "Delegated:" in guidance
        assert "Direct: <reason>" in guidance
        assert "model slugs" in guidance
        assert "reasoning efforts" in guidance
        assert "one compact line" in guidance
        assert "user-owned host setting" in guidance
        assert "main-mediated" in guidance
        assert "recommendations are advisory" in guidance
        assert "parallel wave" in guidance
        assert "personal or global agent files" in guidance
        assert "report-only roles" in guidance
        assert "no write set" in guidance
        assert "effective sandbox" in guidance
        assert "writable parent" in guidance
        assert "one lifecycle owner" in guidance
        assert "explicitly selected competing controller" in guidance
        assert "delegation is the default" in guidance
        assert "delegation_roles" in guidance
        assert "delegation_status" in guidance
        assert "bounded research" in guidance
        assert "configured model" in guidance
        assert "reread the applicable project-local config" in guidance
        assert "changed profile hash" in guidance
        assert "live user-owned dispatch profiles" in guidance
        assert "orchestrator thin" in guidance
        assert "compact decision packet" in guidance
        assert "worker instances as disposable" in guidance
        assert "fresh instance" in guidance
        assert "exact same unfinished assignment" in guidance
        assert "compact only when a live plan contains" in guidance
        assert "small direct work need no rewrite" in guidance
        assert "host-versioned inputs" in guidance
        assert "profile refresh" in guidance
        included = (root / ".worktreeinclude").read_text(encoding="utf-8")
        assert ".codex/agents/*.toml" in included
        ignored = (root / ".gitignore").read_text(encoding="utf-8")
        assert ".codex/" in ignored
        assert ".agents/skills/plumbline-router/" in ignored

    with tempfile.TemporaryDirectory() as raw_root:
        root = Path(raw_root)
        (root / ".git" / "info").mkdir(parents=True)
        install(plugin_root, root, roles=ROLES)
        config = tomllib.loads((root / ".codex" / "config.toml").read_text(encoding="utf-8"))
        assert config["agents"]["max_concurrent_threads_per_session"] == 12
        for role, (model, reasoning) in RECOMMENDED_PROFILES.items():
            data = tomllib.loads((root / ".codex" / "agents" / f"{role}.toml").read_text(encoding="utf-8"))
            assert data["model"] == model
            assert data["model_reasoning_effort"] == reasoning
            assert data["model"] not in {"sol", "luna"}
        assert RECOMMENDED_PROFILES["code-reviewer"] == ("gpt-5.6-luna", "high")
        reviewer_path = root / ".codex" / "agents" / "code-reviewer.toml"
        reviewer_path.write_text(
            reviewer_path.read_text(encoding="utf-8").replace('model = "gpt-5.6-luna"', 'model = "luna"'),
            encoding="utf-8",
        )
        audit = install(plugin_root, root, mode="audit", roles=("code-reviewer",))
        assert any("shorthand" in finding for finding in audit.findings)

    with tempfile.TemporaryDirectory() as raw_root:
        root = Path(raw_root)
        (root / ".git" / "info").mkdir(parents=True)
        install(
            plugin_root,
            root,
            model="gpt-5.6-luna",
            reasoning_effort="medium",
            roles=("researcher", "implementer"),
            update_agents=True,
        )
        guidance = (root / "AGENTS.md").read_text(encoding="utf-8")
        assert "- `researcher`" in guidance
        assert "- `implementer`" in guidance
        assert "- `backend-architect`" not in guidance
        assert "- `frontend-architect`" not in guidance
        assert "- `qa-auditor`" not in guidance

    with tempfile.TemporaryDirectory() as raw_root:
        root = Path(raw_root)
        (root / ".git" / "info").mkdir(parents=True)
        preview = install(
            plugin_root,
            root,
            model="gpt-5.6-luna",
            reasoning_effort="medium",
            roles=("researcher",),
            update_agents=True,
            propagate=True,
            dry_run=True,
        )
        assert preview.operations[root / ".codex" / "config.toml"] == "create"
        assert preview.changes[root / ".codex" / "config.toml"] == (
            "agents.enabled",
            "agents.max_concurrent_threads_per_session",
        )
        assert preview.operations[root / ".gitignore"] == "create"
        assert preview.operations[root / ".worktreeinclude"] == "create"
        assert not (root / ".codex" / "config.toml").exists()
        assert not (root / ".codex" / "agents" / "researcher.toml").exists()
        assert not (root / "AGENTS.md").exists()
        assert not (root / ".gitignore").exists()
        assert not (root / ".worktreeinclude").exists()

        result = subprocess.run(
            [
                sys.executable,
                str(plugin_root / "scripts" / "install_agent_team.py"),
                "--root",
                str(root),
                "--roles",
                "researcher",
                "--model",
                "gpt-5.6-luna",
                "--reasoning-effort",
                "medium",
                "--max-threads",
                "12",
                "--propagate",
                "--dry-run",
                "--format",
                "json",
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        payload = json.loads(result.stdout)
        assert payload["dry_run"] is True
        assert payload["writes_applied"] is False
        assert any(change["path"].endswith(".gitignore") for change in payload["changes"])

        router_result = subprocess.run(
            [
                sys.executable,
                str(plugin_root / "scripts" / "install_router.py"),
                "--root",
                str(root),
                "--dry-run",
                "--format",
                "json",
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        router_payload = json.loads(router_result.stdout)
        assert router_payload["dry_run"] is True
        assert router_payload["writes_applied"] is False
        assert router_payload["changes"][0]["operation"] == "create"

        router_target = install_router(plugin_root, root, dry_run=True)
        assert router_target.name == "SKILL.md"
        assert not router_target.exists()

    with tempfile.TemporaryDirectory() as raw_root:
        root = Path(raw_root)
        (root / ".git" / "info").mkdir(parents=True)
        router = root / ".agents" / "skills" / "plumbline-router" / "SKILL.md"
        router.parent.mkdir(parents=True)
        router.write_text("old router\n", encoding="utf-8")
        result = subprocess.run(
            [
                sys.executable,
                str(plugin_root / "scripts" / "install_router.py"),
                "--root",
                str(root),
                "--dry-run",
                "--format",
                "json",
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        payload = json.loads(result.stdout)
        assert payload["dry_run"] is True
        assert payload["writes_applied"] is False
        assert payload["requires_replace"] is True
        assert payload["changes"][0]["operation"] == "modify"
        assert payload["changes"][0]["requires_replace"] is True
        assert router.read_text(encoding="utf-8") == "old router\n"

    with tempfile.TemporaryDirectory() as raw_root:
        root = Path(raw_root)
        source = root / "source"
        source.mkdir()
        run_git("init", "-q", cwd=source)
        (source / "README.md").write_text("fixture\n", encoding="utf-8")
        run_git("add", "README.md", cwd=source)
        run_git(
            "-c",
            "user.name=Plumbline Smoke",
            "-c",
            "user.email=plumbline-smoke@example.invalid",
            "commit",
            "-qm",
            "fixture",
            cwd=source,
        )
        worktree = root / "worktree"
        run_git("worktree", "add", "-q", "-b", "plumbline-smoke", str(worktree), cwd=source)
        install(
            plugin_root,
            worktree,
            model="gpt-5.6-luna",
            reasoning_effort="medium",
            roles=("researcher",),
        )
        common_exclude = (source / ".git" / "info" / "exclude").read_text(encoding="utf-8")
        assert ".codex/" in common_exclude
        assert ".agents/skills/plumbline-router/" in common_exclude

    with tempfile.TemporaryDirectory() as raw_root:
        root = Path(raw_root)
        (root / ".git" / "info").mkdir(parents=True)
        existing = root / ".codex" / "agents" / "researcher.toml"
        existing.parent.mkdir(parents=True)
        existing.write_text("existing\n", encoding="utf-8")
        try:
            install(
                plugin_root,
                root,
                model="gpt-5.6-luna",
                reasoning_effort="medium",
                roles=("researcher",),
            )
        except FileExistsError:
            pass
        else:
            raise AssertionError("existing roles must require explicit replacement")
        assert not (root / ".codex" / "config.toml").exists()

    with tempfile.TemporaryDirectory() as raw_root:
        root = Path(raw_root)
        (root / ".git" / "info").mkdir(parents=True)
        (root / ".codex").mkdir(parents=True)
        config_path = root / ".codex" / "config.toml"
        config_path.write_text(
            "[features]\nmulti_agent = true\n\n[agents]\nmax_threads = 12\nmax_depth = 2\n",
            encoding="utf-8",
        )
        role_snapshots: dict[str, tuple[str, str, str, str]] = {}
        for index, role in enumerate(ROLES):
            model = f"custom-model-{index}"
            reasoning = "high" if index % 2 else "low"
            sandbox = "workspace-write" if role == "implementer" else "read-only"
            instructions = f"Custom instructions for {role}."
            text = f'''name = "{role}"
description = "Custom {role}"
model = "{model}"
model_reasoning_effort = "{reasoning}"
sandbox_mode = "{sandbox}"
developer_instructions = """
{instructions}
"""
custom_setting = "preserve-me"
'''
            path = root / ".codex" / "agents" / f"{role}.toml"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
            role_snapshots[role] = (model, reasoning, sandbox, instructions)

        before = {
            role: (root / ".codex" / "agents" / f"{role}.toml").read_text(encoding="utf-8")
            for role in ROLES
        }
        config_before = config_path.read_text(encoding="utf-8")
        audit = install(plugin_root, root, mode="audit", roles=ROLES)
        assert not audit.changes
        assert any("legacy features.multi_agent" in finding for finding in audit.findings)
        assert any("legacy agents.max_threads" in finding for finding in audit.findings)
        assert any("legacy agents.max_depth" in finding for finding in audit.findings)
        assert all(
            (root / ".codex" / "agents" / f"{role}.toml").read_text(encoding="utf-8") == before[role]
            for role in ROLES
        )
        assert config_path.read_text(encoding="utf-8") == config_before

        retune = install(plugin_root, root, mode="retune", roles=ROLES)
        assert not retune.changes
        assert any("legacy agents.max_threads" in finding for finding in retune.findings)
        assert all(
            (root / ".codex" / "agents" / f"{role}.toml").read_text(encoding="utf-8") == before[role]
            for role in ROLES
        )
        assert config_path.read_text(encoding="utf-8") == config_before

        migrated = install(
            plugin_root,
            root,
            mode="retune",
            roles=ROLES,
            max_threads=12,
            replace_config=True,
        )
        migrated_config = tomllib.loads(config_path.read_text(encoding="utf-8"))
        assert migrated_config["agents"]["enabled"] is True
        assert migrated_config["agents"]["max_concurrent_threads_per_session"] == 12
        assert "multi_agent" not in migrated_config.get("features", {})
        assert "max_threads" not in migrated_config["agents"]
        assert "max_depth" not in migrated_config["agents"]
        assert migrated.changes[config_path] == (
            "agents.enabled",
            "agents.max_concurrent_threads_per_session",
            "features.multi_agent",
            "agents.max_threads",
            "agents.max_depth",
        )

        updated = install(plugin_root, root, mode="retune", roles=ROLES, update_instructions=True)
        for role in ROLES:
            path = root / ".codex" / "agents" / f"{role}.toml"
            data = tomllib.loads(path.read_text(encoding="utf-8"))
            model, reasoning, sandbox, _instructions = role_snapshots[role]
            assert data["model"] == model
            assert data["model_reasoning_effort"] == reasoning
            assert data["sandbox_mode"] == sandbox
            assert data["custom_setting"] == "preserve-me"
            assert "spawn child" in data["developer_instructions"].lower()
            assert updated.changes[path] == ("developer_instructions",)

        profile_path = root / ".codex" / "agents" / "code-reviewer.toml"
        profile_before = profile_path.read_text(encoding="utf-8")
        profile_before_data = tomllib.loads(profile_before)
        profile_preview = install(
            plugin_root,
            root,
            mode="retune",
            roles=("code-reviewer",),
            model="gpt-5.6-luna",
            reasoning_effort="high",
            update_profile=True,
            dry_run=True,
        )
        assert profile_preview.changes[profile_path] == ("model", "model_reasoning_effort")
        assert profile_path.read_text(encoding="utf-8") == profile_before
        profile_update = install(
            plugin_root,
            root,
            mode="retune",
            roles=("code-reviewer",),
            model="gpt-5.6-luna",
            reasoning_effort="high",
            update_profile=True,
        )
        profile_data = tomllib.loads(profile_path.read_text(encoding="utf-8"))
        assert profile_update.changes[profile_path] == ("model", "model_reasoning_effort")
        assert profile_data["model"] == "gpt-5.6-luna"
        assert profile_data["model_reasoning_effort"] == "high"
        for field in ("name", "description", "developer_instructions", "sandbox_mode", "custom_setting"):
            assert profile_data[field] == profile_before_data[field]

    with tempfile.TemporaryDirectory() as raw_root:
        root = Path(raw_root)
        (root / ".git" / "info").mkdir(parents=True)
        install(
            plugin_root,
            root,
            model="gpt-5.6-luna",
            reasoning_effort="medium",
            roles=("researcher",),
            update_agents=True,
        )
        role_path = root / ".codex" / "agents" / "researcher.toml"
        config_path = root / ".codex" / "config.toml"
        role_before = role_path.read_text(encoding="utf-8")
        config_before = config_path.read_text(encoding="utf-8")
        agents = root / "AGENTS.md"
        stale_guidance = agents.read_text(encoding="utf-8").replace("delegation is the default", "delegation is available")
        agents.write_text(stale_guidance + "\n## Project notes\nKeep this text.\n", encoding="utf-8")

        preview = install(
            plugin_root,
            root,
            mode="initialize",
            roles=("researcher",),
            update_agents=True,
            refresh_agents=True,
            dry_run=True,
        )
        assert preview.requires_replace is False
        assert preview.changes == {agents: ("local agent-team guidance",)}
        assert role_path.read_text(encoding="utf-8") == role_before
        assert config_path.read_text(encoding="utf-8") == config_before

        install(
            plugin_root,
            root,
            mode="initialize",
            roles=("researcher",),
            update_agents=True,
            refresh_agents=True,
        )
        refreshed = agents.read_text(encoding="utf-8")
        assert "<!-- plumbline:managed-agent-team:start -->" in refreshed
        assert "## Project notes\nKeep this text." in refreshed
        assert role_path.read_text(encoding="utf-8") == role_before
        assert config_path.read_text(encoding="utf-8") == config_before

    with tempfile.TemporaryDirectory() as raw_root:
        root = Path(raw_root)
        (root / ".git" / "info").mkdir(parents=True)
        agents = root / "AGENTS.md"
        agents.write_text(
            "# Project\n\n## Local agent team\n\nCustom legacy guidance.\n\n## Notes\nKeep this text.\n",
            encoding="utf-8",
        )
        preview = install(
            plugin_root,
            root,
            mode="initialize",
            roles=("researcher",),
            update_agents=True,
            refresh_agents=True,
            dry_run=True,
        )
        assert preview.requires_replace is True
        assert preview.changes == {agents: ("local agent-team guidance",)}
        assert "Custom legacy guidance." in agents.read_text(encoding="utf-8")
        try:
            install(
                plugin_root,
                root,
                mode="initialize",
                roles=("researcher",),
                update_agents=True,
                refresh_agents=True,
            )
        except ValueError as exc:
            assert "--replace-agents-guidance" in str(exc)
        else:
            raise AssertionError("legacy guidance refresh must require explicit replacement")
        install(
            plugin_root,
            root,
            mode="initialize",
            roles=("researcher",),
            update_agents=True,
            refresh_agents=True,
            replace_guidance=True,
        )
        refreshed = agents.read_text(encoding="utf-8")
        assert "<!-- plumbline:managed-agent-team:start -->" in refreshed
        assert "# Project" in refreshed
        assert "## Notes\nKeep this text." in refreshed

    with tempfile.TemporaryDirectory() as raw_root:
        root = Path(raw_root)
        (root / ".git" / "info").mkdir(parents=True)
        path = root / ".codex" / "agents" / "researcher.toml"
        path.parent.mkdir(parents=True)
        path.write_text(
            'name = "researcher"\n'
            'description = "Existing researcher"\n'
            'developer_instructions = "Keep this custom instruction."\n'
            '\n[custom]\n'
            'setting = "preserve"\n',
            encoding="utf-8",
        )
        filled = install(
            plugin_root,
            root,
            mode="retune",
            roles=("researcher",),
            model="approved-model",
            reasoning_effort="medium",
            fill_missing=True,
        )
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        assert data["model"] == "approved-model"
        assert data["model_reasoning_effort"] == "medium"
        assert data["sandbox_mode"] == "read-only"
        assert data["developer_instructions"] == "Keep this custom instruction."
        assert data["custom"]["setting"] == "preserve"
        assert filled.changes[path] == ("model", "model_reasoning_effort", "sandbox_mode")

    with tempfile.TemporaryDirectory() as raw_root:
        root = Path(raw_root)
        (root / ".git" / "info").mkdir(parents=True)
        (root / ".codex").mkdir(parents=True)
        (root / ".codex" / "config.toml").write_text(
            "[features]\nmulti_agent = true\n\n[agents]\nmax_threads = 6\nmax_depth = 1\n",
            encoding="utf-8",
        )
        (root / ".codex" / "agents").mkdir(parents=True)
        (root / ".codex" / "agents" / "researcher.toml").write_text(
            'name = "researcher"\n'
            'description = "Researcher"\n'
            'model = "custom-model"\n'
            'model_reasoning_effort = "high"\n'
            'sandbox_mode = "read-only"\n'
            'developer_instructions = "Report-only; no write set; never spawn child agents."\n',
            encoding="utf-8",
        )
        router = root / ".agents" / "skills" / "plumbline-router" / "SKILL.md"
        router.parent.mkdir(parents=True)
        router.write_text("stale router\n", encoding="utf-8")
        agents = root / "AGENTS.md"
        agents.write_text("# Project\n\n## Local agent team\n\nDelegated wave:\n", encoding="utf-8")
        before_router = router.read_text(encoding="utf-8")
        before_agents = agents.read_text(encoding="utf-8")
        audit = install(plugin_root, root, mode="audit", roles=("researcher",))
        assert not audit.changes
        assert any("differs from current router template" in finding for finding in audit.findings)
        assert any("missing marker" in finding for finding in audit.findings)
        assert router.read_text(encoding="utf-8") == before_router
        assert agents.read_text(encoding="utf-8") == before_agents
        retune = install(plugin_root, root, mode="retune", roles=("researcher",))
        assert not retune.changes
        assert any("differs from current router template" in finding for finding in retune.findings)
        assert router.read_text(encoding="utf-8") == before_router
        assert agents.read_text(encoding="utf-8") == before_agents
    print("agent-team-installer-smoke=passed")


if __name__ == "__main__":
    main()
