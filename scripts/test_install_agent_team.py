#!/usr/bin/env python3
"""Small stdlib smoke test for the project-local agent-team installer."""

from __future__ import annotations

import subprocess
import tempfile
import tomllib
from pathlib import Path

from install_agent_team import ROLES, install


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
    with tempfile.TemporaryDirectory() as raw_root:
        root = Path(raw_root)
        (root / ".git" / "info").mkdir(parents=True)
        install(
            plugin_root,
            root,
            model="gpt-5.6-luna",
            reasoning_effort="medium",
            update_agents=True,
            propagate=True,
        )
        config = tomllib.loads((root / ".codex" / "config.toml").read_text(encoding="utf-8"))
        assert config["features"]["multi_agent"] is True
        assert config["agents"]["max_depth"] == 1
        for role in ROLES:
            data = tomllib.loads((root / ".codex" / "agents" / f"{role}.toml").read_text(encoding="utf-8"))
            assert data["model"] == "gpt-5.6-luna"
            assert data["model_reasoning_effort"] == "medium"
            assert data["sandbox_mode"]
            assert "spawn child" in data["developer_instructions"].lower()
        guidance = (root / "AGENTS.md").read_text(encoding="utf-8")
        assert "## Local agent team" in guidance
        assert "Delegated wave:" in guidance
        assert "Direct: <reason>" in guidance
        assert "model slugs" in guidance
        assert "reasoning efforts" in guidance
        assert "one compact line" in guidance
        assert "max_depth = 1" in guidance
        assert "personal or global agent files" in guidance
        assert "report-only roles" in guidance
        assert "no write set" in guidance
        assert "effective sandbox" in guidance
        assert "writable parent" in guidance
        assert "one lifecycle owner" in guidance
        assert "explicitly selected competing controller" in guidance
        included = (root / ".worktreeinclude").read_text(encoding="utf-8")
        assert ".codex/agents/*.toml" in included

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
        audit = install(plugin_root, root, mode="audit", roles=ROLES)
        assert not audit.changes
        assert all(
            (root / ".codex" / "agents" / f"{role}.toml").read_text(encoding="utf-8") == before[role]
            for role in ROLES
        )

        retune = install(plugin_root, root, mode="retune", roles=ROLES)
        assert not retune.changes
        assert all(
            (root / ".codex" / "agents" / f"{role}.toml").read_text(encoding="utf-8") == before[role]
            for role in ROLES
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
