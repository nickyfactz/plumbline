---
name: plumbline-agent-team
description: Initialize, audit, retune, or extend a repository-adapted Codex agent team without global installation.
disable-model-invocation: true
---

# Agent Team

This skill is explicit only. It is the project-local team setup and audit boundary. Read `AGENTS.md`, `.codex/agents/`, `.codex/config.toml`, `.gitignore`, `.git/info/exclude`, `.worktreeinclude`, and established agent conventions before proposing changes. Keep discovery targeted; do not enumerate the whole repository.

## Non-negotiable scope

Project-local `.codex/agents/*.toml` and `.codex/config.toml` are the only agent definitions and team settings Plumbline may select. The global `config.toml` may be inspected for host capability and the current main model candidate, but personal/global agent files are never selected, copied, or used as fallbacks. Do not edit global settings, install a global team, or delete an old competing role.

Set or verify project-local `features.multi_agent = true`, an approved `agents.max_threads`, and `agents.max_depth = 1`. A depth of one lets the main thread use direct workers while preventing worker-created children. Every worker instruction must say it cannot spawn children, own Git, or edit the active spec/plan. Give each worker only the exact read paths and anchored sections needed for its brief; do not pass full history or whole documentation trees when unchanged artifacts answer the question. Report-only roles (researcher, architect, and QA) receive no write set. Their `sandbox_mode = "read-only"` is intent; a writable parent is normal for a goal and may affect the effective sandbox. State the boundary when observable and inspect returned diffs; only the approved implementer receives a write set.

## Operations

- **Initialize:** create only approved missing roles from the five archetypes in `templates/agents/`, plus exact local config, AGENTS guidance, ignore, and worktree propagation changes. Generate AGENTS role bullets from the selected roles. When propagation is approved, include the root `.gitignore` patch and `.worktreeinclude` in the same proposal. Existing roles require an explicit initialize replacement approval before `--replace`.
- **Audit:** read-only compare project agents, the repository-local router, and current repository docs; report stale facts, router or AGENTS schema drift, overlap, missing boundaries, required-field gaps, model/reasoning/sandbox drift, and capability gaps. Audit never needs `--replace` and never writes. A detected mismatch produces a proposed refresh, not an automatic overwrite.
- **Retune:** preserve every existing role field, including `model`, `model_reasoning_effort`, sandbox, permissions, MCP, custom fields, and `developer_instructions`. Use `--fill-missing` only to add absent required fields; it never overwrites a present value. Use `--update-instructions` only when the approved proposal explicitly changes the instruction field.
- **Add:** add one specialist only for a demonstrated need; do not create a role for every technical layer.

Before approval, show one role-by-role table with `name`, purpose, model slug, reasoning effort, sandbox, and write access. The recommended template uses the current approved model/reasoning explicitly in every TOML. Do not invent slugs or silently downgrade a user's choice. Apply nothing before approval.

Before asking for approval, run the candidate `install_agent_team.py` command with `--dry-run --format json` and include its exact file/operation/field manifest in the proposal. The dry run is read-only and does not approve or apply changes.

After approval, audit and retune output must also report router freshness and AGENTS guidance drift without overwriting either file. A stale router produces a proposed refresh only; applying it requires the explicit router installer `--replace` path.

After approval, rerun the dry-run manifest; if the target changed, refresh the proposal before writing. Then rerun without `--dry-run` using `scripts/install_agent_team.py --mode initialize|audit|retune`. Retune does not require `--replace`; its output reports the exact changed fields for every file. `--update-instructions` replaces only `developer_instructions` with the approved Plumbline body while retaining the other TOML fields and custom keys. Use `--update-agents` and `--propagate` during initialize only, when approved. Validate every TOML's required model, reasoning, sandbox, and no-child boundary, local settings, AGENTS guidance, actual project-local discovery, and the manifest. Report one compact delegation-wave line with selected role names, configured model slugs, and reasoning efforts; include effective values only when the host exposes a meaningful difference or the user asks, and use `Direct: <reason>` when no local role is available. If a matching local role is absent, stay on the main thread or report the capability gap; never fall back to a personal/global agent. Report that `.worktreeinclude` must be committed for future worktrees and that existing worktrees need explicit refresh. Run only a bounded, read-only discovery smoke test after approval.
