#!/usr/bin/env python3
"""Small stdlib smoke test for the project-local Claude agent installer."""

from __future__ import annotations

import tempfile
from pathlib import Path

from install_claude_agent_team import RECOMMENDED_EFFORTS, RECOMMENDED_PROFILES, ROLES, install


def main() -> None:
    plugin_root = Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory() as raw_root:
        root = Path(raw_root)
        (root / ".git" / "info").mkdir(parents=True)
        report = install(
            plugin_root,
            root,
            model="inherit",
            effort="medium",
            roles=("researcher", "implementer"),
            update_agents=True,
            propagate=True,
        )
        assert report.changes
        researcher = (root / ".claude" / "agents" / "researcher.md").read_text(encoding="utf-8")
        implementer = (root / ".claude" / "agents" / "implementer.md").read_text(encoding="utf-8")
        assert 'model: "inherit"' in researcher
        assert "permissionMode: plan" in researcher
        assert '"Agent"' not in researcher
        assert "Never invoke the Agent tool" in researcher
        assert "main thread" in researcher
        assert "dispatch another worker" in researcher
        assert "permissionMode: default" in implementer
        assert '"Edit"' in implementer and '"Write"' in implementer
        guidance = (root / "AGENTS.md").read_text(encoding="utf-8")
        claude_instructions = (root / "CLAUDE.md").read_text(encoding="utf-8")
        assert "@AGENTS.md" in claude_instructions
        assert "- `researcher`" in guidance
        assert "main-mediated" in guidance
        assert "recommendations are advisory" in guidance
        assert "parallel wave" in guidance
        assert "delegation is the default" in guidance
        assert "delegation_roles" in guidance
        assert "delegation_status" in guidance
        assert "bounded research" in guidance
        assert "configured model" in guidance
        assert "Reread the selected" in guidance
        assert "orchestrator thin" in guidance
        assert "compact decision packet" in guidance
        assert "running workers keep" in guidance
        assert "worker instances as disposable" in guidance
        assert "fresh instance" in guidance
        assert "exact same unfinished assignment" in guidance
        assert "compact only when a live plan contains" in guidance
        assert "small direct work need no rewrite" in guidance
        assert "provider-versioned inputs" in guidance
        assert "profile refresh" in guidance
        assert "@agent-<role>" in guidance
        assert "hot-reloads" in guidance
        assert "Codex-only" in guidance
        assert "source checkout" in guidance
        assert ".claude/agents/" in (root / ".gitignore").read_text(encoding="utf-8")
        assert ".claude/agents/*.md" in (root / ".worktreeinclude").read_text(encoding="utf-8")
        assert not (root / ".claude" / "settings.json").exists()

        role_path = root / ".claude" / "agents" / "researcher.md"
        role_before = role_path.read_text(encoding="utf-8")
        agents = root / "AGENTS.md"
        stale_guidance = agents.read_text(encoding="utf-8").replace("delegation is the default", "delegation is available")
        agents.write_text(stale_guidance + "\n## Project notes\nKeep this text.\n", encoding="utf-8")
        preview = install(
            plugin_root,
            root,
            mode="initialize",
            roles=("researcher", "implementer"),
            update_agents=True,
            refresh_agents=True,
            dry_run=True,
        )
        assert preview.requires_replace is False
        assert preview.changes == {agents: ("local Claude agent-team guidance",)}
        assert role_path.read_text(encoding="utf-8") == role_before
        install(
            plugin_root,
            root,
            mode="initialize",
            roles=("researcher", "implementer"),
            update_agents=True,
            refresh_agents=True,
        )
        refreshed = agents.read_text(encoding="utf-8")
        assert "<!-- plumbline:managed-agent-team:start -->" in refreshed
        assert "## Project notes\nKeep this text." in refreshed
        assert role_path.read_text(encoding="utf-8") == role_before

    with tempfile.TemporaryDirectory() as raw_root:
        root = Path(raw_root)
        (root / ".git" / "info").mkdir(parents=True)
        install(plugin_root, root, roles=ROLES)
        for role, (model, effort) in RECOMMENDED_PROFILES.items():
            path = root / ".claude" / "agents" / f"{role}.md"
            text = path.read_text(encoding="utf-8")
            assert f'model: "{model}"' in text
            assert f"effort: {effort}" in text
        reviewer = (root / ".claude" / "agents" / "code-reviewer.md").read_text(encoding="utf-8")
        assert "maintainable-code" in reviewer

    with tempfile.TemporaryDirectory() as raw_root:
        root = Path(raw_root)
        (root / ".git" / "info").mkdir(parents=True)
        agents = root / "AGENTS.md"
        agents.write_text(
            "# Project\n\n## Local Claude agent team\n\nCustom legacy guidance.\n\n## Notes\nKeep this text.\n",
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
        claude = root / "CLAUDE.md"
        assert preview.changes == {
            agents: ("local Claude agent-team guidance",),
            claude: ("@AGENTS.md import",),
        }
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
            raise AssertionError("legacy Claude guidance refresh must require explicit replacement")
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
        assert "@AGENTS.md" in (root / "CLAUDE.md").read_text(encoding="utf-8")

    with tempfile.TemporaryDirectory() as raw_root:
        root = Path(raw_root)
        (root / ".git" / "info").mkdir(parents=True)
        preview = install(plugin_root, root, roles=("researcher",), dry_run=True)
        assert preview.operations[root / ".claude" / "agents" / "researcher.md"] == "create"
        assert not (root / ".claude").exists()

    with tempfile.TemporaryDirectory() as raw_root:
        root = Path(raw_root)
        (root / ".git" / "info").mkdir(parents=True)
        install(plugin_root, root, roles=("researcher",), model="inherit", effort="low")
        path = root / ".claude" / "agents" / "researcher.md"
        before = path.read_text(encoding="utf-8")
        audit = install(plugin_root, root, mode="audit", roles=ROLES)
        assert not audit.changes
        assert any("missing project-local Claude role" in finding for finding in audit.findings)
        custom = before.replace('model: "inherit"', 'model: "custom-claude"').replace("effort: low", "effort: high")
        path.write_text(custom.replace("Never invoke the Agent tool or spawn child agents.", "Custom instructions."), encoding="utf-8")
        retune = install(plugin_root, root, mode="retune", roles=("researcher",))
        assert not retune.changes
        assert 'model: "custom-claude"' in path.read_text(encoding="utf-8")
        assert "effort: high" in path.read_text(encoding="utf-8")
        before_profile = path.read_text(encoding="utf-8")
        profile_preview = install(
            plugin_root,
            root,
            mode="retune",
            roles=("researcher",),
            model="approved-claude-model",
            effort="max",
            update_profile=True,
            dry_run=True,
        )
        assert profile_preview.changes[path] == ("model", "effort")
        assert path.read_text(encoding="utf-8") == before_profile
        profile_update = install(
            plugin_root,
            root,
            mode="retune",
            roles=("researcher",),
            model="approved-claude-model",
            effort="max",
            update_profile=True,
        )
        assert profile_update.changes[path] == ("model", "effort")
        refreshed = path.read_text(encoding="utf-8")
        assert 'model: "approved-claude-model"' in refreshed
        assert 'effort: "max"' in refreshed
        assert "Custom instructions." in refreshed

    with tempfile.TemporaryDirectory() as raw_root:
        root = Path(raw_root)
        (root / ".git" / "info").mkdir(parents=True)
        install(plugin_root, root, roles=ROLES)
        researcher_path = root / ".claude" / "agents" / "researcher.md"
        researcher_path.write_text(
            researcher_path.read_text(encoding="utf-8").replace('model: "sonnet"', 'model: "gpt-5.6-luna"'),
            encoding="utf-8",
        )
        audit = install(plugin_root, root, mode="audit", roles=("researcher",))
        assert any("Codex/OpenAI value" in finding for finding in audit.findings)

    print("claude-agent-team-installer-smoke=passed")


if __name__ == "__main__":
    main()
