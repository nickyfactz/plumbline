# Plumbline repository guidance

This repository contains the Plumbline Codex plugin. Keep the plugin skills-only and repository-local: installation must not create global skills, global agent files, hooks, MCP servers, or a custom worktree system.

## Project-local agent team

Use only agent definitions under `.codex/agents/` when this checkout is explicitly initialized for delegated work. The global Codex config may be inspected for host capability and a model candidate, but personal/global agent definitions are never selected or used as fallback. Keep `.codex/config.toml`, `.codex/agents/`, and any installed local router untracked unless the user explicitly chooses otherwise.

The main thread owns product decisions, specifications, plans, integration, and Git. Give workers bounded briefs and disjoint write sets. The report-only roles (researcher, architect, and QA) receive no write set. Their `sandbox_mode = "read-only"` is intent; a writable parent is normal for a goal and may affect the child's effective sandbox. At each delegation wave, report the selected role names with configured model slugs and reasoning efforts in one compact line; include configured/effective sandbox values when observable, and state the report-only/no-write-set/no-child boundary. Inspect Git status/diff after the child returns, and never silently integrate unexpected edits. Only the approved implementer receives a write set. Workers never spawn child agents. Project `agents.max_depth = 1` is the recommendation. If no local role is available, state `Direct: <reason>` and continue on the main thread.

At phase entry or resume, state one lifecycle owner and keep it in the active plan's resume record. Repeat it only when ownership changes, a competing controller is selected, or the record is stale. An installed or enabled workflow is available capability, not active ownership; an explicitly selected competing controller owns its own checkpoint and closeout flow.

Use `$plumbline-init` for the combined router/team setup and `$plumbline-agent-team` explicitly for initialize, audit, retune, or add requests. Do not invoke setup for ordinary feature work.

When changing initialization or agent-team behavior, keep the flow read-only until explicit approval, show the role/model/reasoning/sandbox/config proposal, update the installer and validator together, and verify new managed-worktree propagation without copying secrets or dependencies.

## Verification

Run `python scripts/validate.py` and `python scripts/test_install_agent_team.py` for setup or packaging changes. Use `git diff --check` before handoff. Do not commit or push unless the user asks.
