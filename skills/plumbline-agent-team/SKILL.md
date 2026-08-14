---
name: plumbline-agent-team
description: Initialize, audit, retune, or extend a repository-adapted Plumbline agent team for Codex or Claude Code without global installation.
disable-model-invocation: true
---

# Agent Team

This skill is explicit only. It is the project-local team setup and audit boundary. Determine the active host, then read `AGENTS.md`, the host's project-local agent directory, relevant host settings, `.gitignore`, `.git/info/exclude`, `.worktreeinclude`, and established agent conventions before proposing changes. Keep discovery targeted; do not enumerate the whole repository.

## Non-negotiable scope

The host adapter is explicit:

- Codex uses only project-local `.codex/agents/*.toml` and `.codex/config.toml`. Set or verify `features.multi_agent = true`; recommend `agents.max_threads = 6` and `agents.max_depth = 1` as starting values, but treat both as user-owned host settings. Preserve an approved alternative such as 12 threads or another supported depth. This keeps the main parent's collaboration tools available for explicit project roles, including a selected Luna role even when Luna is absent from the standard v2 picker. The role's explicit `model` field selects Luna; the feature flag only keeps collaboration available. It does not select Luna by itself.
- Claude Code uses only project-local `.claude/agents/*.md`. Claude has no required Plumbline project config switch; Markdown frontmatter carries `model`, `effort`, `tools`, and `permissionMode`. Do not edit global Claude settings or enable `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`; Plumbline uses bounded subagents, not the separate experimental Agent Teams feature.

The global Codex config may be inspected for host capability and the current main model candidate, but personal/global agent files are never selected, copied, or used as fallbacks. Do not edit global settings, install a global team, or delete an old competing role.

A depth of one is a recommended delegation boundary, not a host setting Plumbline enforces. Claude applies the same recommended behavior by omitting the `Agent` tool from generated roles and stating it in every role prompt. Every worker instruction must say it cannot spawn children, own Git, or edit the active spec/plan. This main-mediated rule means every worker returns to the main thread; worker recommendations are advisory, and only the main thread selects and dispatches the next capability. When independent work is ready, the main thread may dispatch one parallel wave only after a stable contract, disjoint scopes, no result dependency, and a clear join condition are established. Give each worker only the exact read paths and anchored sections needed for its brief; do not pass full history or whole documentation trees when unchanged artifacts answer the question. Report-only roles (researcher, architect, and QA) receive no write set. Codex `sandbox_mode = "read-only"` and Claude `permissionMode: plan` are intent; a writable or permissive parent may affect effective permissions and effective sandbox. State the boundary when observable and inspect returned diffs; each approved write-capable role receives only its bounded write set.

## Starting model recommendation

During setup, recommend a role-aware starting profile aimed at the cheapest effective model and reasoning effort for each function: lower-cost settings for bounded research and mechanical work, and higher settings only when the task has material architecture, persistence, concurrency, security, ownership, or acceptance risk. Use the host's available model candidates and the user's project evidence; do not hard-code a model slug or reasoning policy into the shared role instructions. Codex proposals use model slugs and reasoning efforts; Claude proposals use a model alias or `inherit` and a Claude `effort` value.

Label the proposal as a recommended starting point, not a permanent team policy. Model and reasoning/effort values are adjustable and hotswappable by explicit user choice or later evidence. If the installer applies one common pair to several roles, say that it is a reproducible baseline rather than claiming it is optimal for every role. Audit and retune preserve tuned values unless the user explicitly approves a change. Evaluate cheaper settings by accepted first-pass work and remediation cost, not nominal price alone.

## Operations

- **Initialize:** create only approved missing roles from the five shared archetypes in `templates/agents/`. On Codex, use `scripts/install_agent_team.py` for local TOML/config setup. On Claude Code, use `scripts/install_claude_agent_team.py` for local Markdown subagents; it makes no global settings change. Generate AGENTS role bullets from the selected roles. When propagation is approved, include the root `.gitignore` patch and `.worktreeinclude` in the same proposal. Existing roles require an explicit initialize replacement approval before `--replace`. If the user explicitly invokes initialization again, audit the managed `AGENTS.md` section and offer `--update-agents --refresh-agents` as a guidance-only update; it does not replace roles or config. An older unmarked section requires the exact dry-run plus explicit `--replace-agents-guidance`, and only that managed section may be replaced.
- **Audit:** read-only compare project agents, the repository-local router, and current repository docs; report stale facts, router or AGENTS schema drift, overlap, missing boundaries, required-field gaps, model/reasoning/effort/sandbox/permission drift, and capability gaps. Audit never needs `--replace` and never writes. A detected mismatch produces a proposed refresh, not an automatic overwrite. A later explicit initialization is the consent boundary for applying an approved guidance refresh.
- **Retune:** preserve every existing role field, including model, reasoning/effort, sandbox/permission, permissions, MCP, custom fields, and instructions. Use `--fill-missing` only to add absent required fields; it never overwrites a present value. Use `--update-instructions` only when the approved proposal explicitly changes the instruction field.
- **Add:** add one specialist only for a demonstrated need; do not create a role for every technical layer.

Before approval, show one role-by-role table with `name`, purpose, host-native model value, reasoning/effort value, sandbox/permission intent, and write access. Mark these values as the recommended starting profile and explain that the user can adjust or hot-swap them later. The adapter writes explicit values for reproducible local setup, but those values are not immutable Plumbline policy. Do not invent slugs or silently downgrade a user's choice. Apply nothing before approval.

Before asking for approval, run the host-specific candidate installer with `--dry-run --format json` and include its exact file/operation/field manifest in the proposal: `install_agent_team.py` for Codex or `install_claude_agent_team.py` for Claude Code. The dry run is read-only and does not approve or apply changes.

After approval, audit and retune output must also report router freshness and AGENTS guidance drift without overwriting either file. A stale router produces a proposed refresh only; applying it requires the explicit router installer `--replace` path.

After approval, rerun the dry-run manifest; if the target changed, refresh the proposal before writing. Then rerun the host-specific installer in `initialize|audit|retune` mode. Retune does not require `--replace`; its output reports the exact changed fields for every file and preserves existing model, effort/reasoning, permission/sandbox, custom fields, and instructions unless explicitly approved. Use `--update-agents` and `--propagate` during first initialization only, when approved; use `--update-agents --refresh-agents` on an explicit repeat initialization to update only the managed guidance section. Validate every host role's required model, reasoning/effort, permission/sandbox, and no-child boundary, structurally valid user-owned host settings, AGENTS guidance, actual project-local discovery, ignore rules, and the manifest. Report one compact delegation-wave line with selected role names and host-native model plus reasoning/effort values; include effective values only when the host exposes a meaningful difference or the user asks, and use `Direct: <reason>` when no local role is available. If a matching local role is absent, stay on the main thread or report the capability gap; never fall back to a personal/global agent. Report that `.worktreeinclude` must be committed for future worktrees and that existing worktrees need explicit refresh. Run only a bounded, read-only discovery smoke test after approval.

## Completion

An audit is complete when it reports current role fields, instruction and
boundary drift, router/AGENTS guidance drift, and a read-only change proposal
without overwriting existing customization. Initialize or retune is complete
when the approved manifest is applied, exact changed fields are reported,
required host fields and no-child boundaries validate, project-local discovery
works, and worktree propagation is explained. The main thread remains the sole
dispatcher and Git owner after team setup.
