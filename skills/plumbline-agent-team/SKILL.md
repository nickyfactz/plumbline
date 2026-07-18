---
name: plumbline-agent-team
description: Initialize, audit, retune, or extend a repository-adapted Codex agent team without global installation.
---

# Agent Team

This skill is explicit only. It is the project-local team setup and audit boundary. Read `AGENTS.md`, `.codex/agents/`, `.codex/config.toml`, `.gitignore`, `.git/info/exclude`, `.worktreeinclude`, and established agent conventions before proposing changes.

## Non-negotiable scope

Project-local `.codex/agents/*.toml` and `.codex/config.toml` are the only agent definitions and team settings Plumbline may select. The global `config.toml` may be inspected for host capability and the current main model candidate, but personal/global agent files are never selected, copied, or used as fallbacks. Do not edit global settings, install a global team, or delete an old competing role.

Set or verify project-local `features.multi_agent = true`, an approved `agents.max_threads`, and `agents.max_depth = 1`. A depth of one lets the main thread use direct workers while preventing worker-created children. Every worker instruction must say it cannot spawn children, own Git, or edit the active spec/plan. Report-only roles (researcher, architect, and QA) receive no write set. Their `sandbox_mode = "read-only"` is intent; a writable parent is normal for a goal and may affect the effective sandbox. State the boundary when observable and inspect returned diffs; only the approved implementer receives a write set.

## Operations

- **Initialize:** create only approved missing roles from the five archetypes in `templates/agents/`, plus exact local config, AGENTS guidance, ignore, and worktree propagation changes. Existing roles require an explicit initialize replacement approval before `--replace`.
- **Audit:** read-only compare project agents, the repository-local router, and current repository docs; report stale facts, router or AGENTS schema drift, overlap, missing boundaries, required-field gaps, model/reasoning/sandbox drift, and capability gaps. Audit never needs `--replace` and never writes. A detected mismatch produces a proposed refresh, not an automatic overwrite.
- **Retune:** preserve every existing role field, including `model`, `model_reasoning_effort`, sandbox, permissions, MCP, custom fields, and `developer_instructions`. Use `--fill-missing` only to add absent required fields; it never overwrites a present value. Use `--update-instructions` only when the approved proposal explicitly changes the instruction field.
- **Add:** add one specialist only for a demonstrated need; do not create a role for every technical layer.

Before approval, show one role-by-role table with `name`, purpose, model slug, reasoning effort, sandbox, and write access. The recommended template uses the current approved model/reasoning explicitly in every TOML. Do not invent slugs or silently downgrade a user's choice. Apply nothing before approval.

After approval, audit and retune output must also report router freshness and AGENTS guidance drift without overwriting either file.

After approval, use `scripts/install_agent_team.py --mode initialize|audit|retune`. Retune does not require `--replace`; its output reports the exact changed fields for every file. `--update-instructions` replaces only `developer_instructions` with the approved Plumbline body while retaining the other TOML fields and custom keys. Use `--update-agents` and `--propagate` during initialize only, when approved. Validate every TOML's required model, reasoning, sandbox, and no-child boundary, local settings, AGENTS guidance, actual project-local discovery, and the manifest. Report one compact delegation-wave line with selected role names, configured model slugs, and reasoning efforts; include effective values when the host exposes them, and use `Direct: <reason>` when no local role is available. If a matching local role is absent, stay on the main thread or report the capability gap; never fall back to a personal/global agent. Report that `.worktreeinclude` must be committed for future worktrees and that existing worktrees need explicit refresh. Run only a bounded, read-only discovery smoke test after approval.
