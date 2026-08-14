#!/usr/bin/env python3
"""Small stdlib smoke test for the project-local Claude agent installer."""

from __future__ import annotations

import tempfile
from pathlib import Path

from install_claude_agent_team import ROLES, install


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
        assert "- `researcher`" in guidance
        assert "main-mediated" in guidance
        assert "recommendations are advisory" in guidance
        assert "parallel wave" in guidance
        assert "delegation is the default" in guidance
        assert "delegation_roles" in guidance
        assert "delegation_status" in guidance
        assert "bounded research" in guidance
        assert "configured model" in guidance
        assert ".claude/agents/" in (root / ".gitignore").read_text(encoding="utf-8")
        assert ".claude/agents/*.md" in (root / ".worktreeinclude").read_text(encoding="utf-8")
        assert not (root / ".claude" / "settings.json").exists()

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

    print("claude-agent-team-installer-smoke=passed")


if __name__ == "__main__":
    main()
