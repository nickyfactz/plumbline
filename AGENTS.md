# Plumbline repository guidance

This repository contains the Plumbline plugin for Codex and Claude Code. Keep the plugin skills-first and repository-local: its optional continuity hook is bundled with the plugin, while installation must not create global skills, global agent files, project/global hook configuration, MCP servers, or a custom worktree system. The bundled hook must remain inert until the user explicitly invokes the Plumbline front door; it only restores a compact reminder after resume or compaction and never selects phases, runs setup, edits the repository, or dispatches agents.

## Project-local agent team

Use only project-local agent definitions when this checkout is explicitly initialized for delegated work: `.codex/agents/*.toml` for Codex or `.claude/agents/*.md` for Claude Code. The global Codex config may be inspected for host capability and a model candidate, but personal/global agent definitions are never selected or used as fallback. Do not edit global Claude settings or enable Claude Agent Teams automatically. Keep `.codex/config.toml`, `.codex/agents/`, `.claude/agents/`, and any installed local router untracked unless the user explicitly chooses otherwise.

For material multi-step work in a Git checkout, assume a `required` Git policy:
ask once at Execute entry to create main-thread checkpoint or batch commits,
assuming yes unless the user explicitly opts out. Record the starting `HEAD`,
keep unrelated dirty files out, and do not advance dependent checkpoints with
uncommitted plan-owned changes. Use checkpoint commits, `git show`, and focused
diffs as worker hydration context. If Git is absent, recommend establishing it
before Execute; an explicit opt-out is reported as Git-unanchored.

Keep the main thread thin: it owns product decisions, specifications, plans, integration, Git, singleton operations, and all delegation. Read only the controlling artifact, repository guidance, Git state, and named paths needed to route and integrate work. Before broad grep, repository archaeology, multi-file fact gathering, external research, or cross-seam review, dispatch the matching project-local role with a bounded brief. Ask read-heavy workers for a compact decision packet containing the conclusion, exact pointers, constraints, residual uncertainty, and next action; do not repeat their exploration on the main thread. Report-only roles receive no write set. Worker recommendations are advisory and return to the main thread; workers never invoke, hand off to, or dispatch another worker. Codex `sandbox_mode = "read-only"` and Claude `permissionMode: plan` are intent; a writable parent may affect effective permissions. Emit one compact dispatch line with selected roles, host-native model/reasoning or effort, and short assignments. Mention standard boundaries or effective values only for an exception, mismatch, or user question; omit routine starting, waiting, return, and unchanged-state narration. Inspect Git status/diff after return and report unexpected edits. Preserve project-local role values and never invent personal/global roles. Restore `delegation_roles` and `delegation_status` after compaction. Keep only already-understood tiny work or tightly coupled main-owned actions direct; use `Direct: <reason>` only when useful bounded work looked delegable but no matching local role remains available. Worker leaf behavior is a Plumbline orchestration boundary, not a required Codex depth setting. When independent work has stable contracts, disjoint scopes, no result dependency, and a clear join condition, the main thread may dispatch a parallel wave; otherwise keep it serial.
Keep in-flight workers active until the host reports a terminal result. Elapsed time, silence, compaction, or an intermediate status is not failure; reconcile observer timeouts before recovery, and replace work only after confirmed terminal/API/transport failure, explicit user stop, obsolete scope, or safety issue.

Reread the applicable project-local role and host-config files before each delegation wave. A changed profile refreshes new workers while already-running workers retain their creation profile. If a role is missing in a worktree, refresh only the ignored team files from the source checkout through the repository's propagation convention before using `Direct: <reason>`; never use global roles. Keep active plans as thin current-state projections: replace and prune status, accepted proof pointers, blockers, residuals/deferrals, and next action in place; remove attempt chronology and superseded context.

At phase entry or resume, state one lifecycle owner and keep it in the active plan's resume record. Repeat it only when ownership changes, a competing controller is selected, or the record is stale. An installed or enabled workflow is available capability, not active ownership; an explicitly selected competing controller owns its own checkpoint and closeout flow.

Use `$plumbline-init` for the combined router/team setup and `$plumbline-agent-team` explicitly for initialize, audit, retune, or add requests. Do not invoke setup for ordinary feature work.

When changing initialization or agent-team behavior, keep the flow read-only until explicit approval, show the role/model/reasoning/sandbox/config proposal, update the installer and validator together, and verify new managed-worktree propagation without copying secrets or dependencies.

When writing, modifying, or reviewing production code, invoke the bundled `maintainable-code` skill; implementers apply its implementation guidance and `code-reviewer` applies its adversarial review gate.

When a user explicitly invokes Plumbline initialization again, audit the managed `AGENTS.md` guidance and offer the guidance-only refresh path. Preview `--update-agents --refresh-agents` before writing; preserve content outside the managed block, and require explicit `--replace-agents-guidance` approval for an older unmarked section. Do not refresh guidance during ordinary feature work, audit, or retune.

## Verification

Run `python scripts/validate.py`, `python scripts/test_install_agent_team.py`, and `python scripts/test_install_claude_agent_team.py` for setup or packaging changes. Use `git diff --check` before handoff. Do not commit or push unless the user asks.
