---
name: plumbline-agent-team
description: Initialize, audit, retune, or extend a repository-adapted Plumbline agent team for Codex or Claude Code without global installation.
disable-model-invocation: true
---

# Agent Team

This skill is explicit only. It is the project-local team setup and audit boundary. Determine the active host, then read `AGENTS.md`, the host's project-local agent directory, relevant host settings, `.gitignore`, `.git/info/exclude`, `.worktreeinclude`, and established agent conventions before proposing changes. Keep discovery targeted; do not enumerate the whole repository.

## Non-negotiable scope

The host adapter is explicit:

- Codex uses only project-local `.codex/agents/*.toml` and `.codex/config.toml`. Current Codex releases enable subagents by default; set or verify `agents.enabled = true` only when the project records that intent explicitly. Recommend `agents.max_concurrent_threads_per_session = 12` as an adjustable starting value and preserve an approved alternative such as 6. Offer an approval-gated migration for legacy `features.multi_agent`, `agents.max_threads`, or `agents.max_depth` entries. A role's explicit `model` field selects its model, including a legacy-compatible leaf worker; Plumbline does not force a v1 delegation path.
- Claude Code uses only project-local `.claude/agents/*.md`. Claude has no required Plumbline project config switch; Markdown frontmatter carries `model`, `effort`, `tools`, and `permissionMode`. Do not edit global Claude settings or enable `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`; Plumbline uses bounded subagents, not the separate experimental Agent Teams feature.

The global Codex config may be inspected for host capability and the current main model candidate, but personal/global agent files are never selected, copied, or used as fallbacks. Do not edit global settings, install a global team, or delete an old competing role.

A depth of one is a recommended delegation boundary, not a host setting Plumbline enforces. Claude applies the same recommended behavior by omitting the `Agent` tool from generated roles and stating it in every role prompt. Every worker instruction must say it cannot spawn children, own Git, or edit the active spec/plan. This main-mediated rule means every worker returns to the main thread; worker recommendations are advisory, and only the main thread selects and dispatches the next capability. Generated guidance must keep the orchestrator thin: delegate bounded read-heavy discovery before broad repository search, request a compact decision packet, and prevent the main thread from repeating worker exploration. When independent work is ready, the main thread may dispatch one parallel wave only after a stable contract, disjoint scopes, no result dependency, and a clear join condition are established. Give each worker only the exact read paths and anchored sections needed for its brief; do not pass full history or whole documentation trees when unchanged artifacts answer the question. Report-only roles (researcher, architect, code-reviewer, and QA) receive no write set. Codex `sandbox_mode = "read-only"` and Claude `permissionMode: plan` are intent; a writable or permissive parent may affect effective permissions and effective sandbox. Emit one compact dispatch line with role, configured model/reasoning or effort, and assignment; standard boundaries and routine status narration are omitted unless an exception matters. Inspect returned diffs; each approved write-capable role receives only its bounded write set.

Role profiles are reusable; worker instances are disposable. Retire a worker
after a terminal result and use a fresh instance for a new checkpoint, correction,
failure, or acceptance task, even when selecting the same role. A follow-up is
only for the exact same unfinished assignment when continuity materially helps;
all new work gets a fresh instance. Use the host's fresh-child path and Codex
`fork_turns="none"` when exposed. Never kill an active worker because it is
quiet or compacting.

Treat project-local role files and applicable host config as live dispatch inputs. Before each delegation wave, reread the selected files. A changed profile is a profile refresh: it updates the model, reasoning/effort, sandbox/permission, or instruction values used by new workers; it does not invalidate prior evidence or retune workers already running. If a role is missing in a worktree, refresh only the ignored project-local team files from the source checkout through the repository's propagation convention, reread them, and use `Direct: <reason>` only if the role is still unavailable. Never use global roles or copy secrets, dependencies, or source trees.

Worker reports cannot override lifecycle invariants. `CHANGES_REQUIRED` reopens
the same candidate checkpoint; an inconclusive, environment, or harness result
blocks it only when safe progress cannot continue beyond a bounded Diagnose
repair. Severity alone cannot abandon the objective or select a successor objective;
the main thread preserves the candidate and owns that decision.

## Starting model recommendation

For Codex, propose this role-aware starting profile when the host supports these
model IDs:

| Role | Model | Reasoning | Purpose |
| --- | --- | --- | --- |
| `frontend-architect` | `gpt-5.6-sol` | `medium` | UI and integration design |
| `backend-architect` | `gpt-5.6-sol` | `medium` | contracts and state ownership |
| `researcher` | `gpt-5.6-luna` | `medium` | bounded evidence gathering |
| `implementer` | `gpt-5.6-luna` | `high` | bounded implementation |
| `code-reviewer` | `gpt-5.6-luna` | `high` | adversarial maintainability review |
| `qa-auditor` | `gpt-5.6-luna` | `max` | acceptance and proof audit |

For Claude Code, preserve the same capability split with provider-native
values: `model: inherit` and the corresponding `effort` values. `inherit` is
the safe non-pinned default; when pinning a model, resolve the current Claude
alias or full model ID from the host model picker or Anthropic's official model
documentation/API. These are recommended starting points, not permanent policy;
users may adjust or hotswap them, and audit/retune preserves existing values.

The bundled `maintainable-code` skill is model-invoked for implementation and
review. Implementers use its implementation branch; `code-reviewer` uses its
review branch before `qa-auditor` checks acceptance, proof, and documentation.

Use the role-aware starting profile above as the Codex recommendation only after
verifying the exact current host-supported IDs. The current release examples
are full Codex IDs, not `sol`/`luna` aliases. Use provider-native Claude values
rather than copying Codex IDs. Model and reasoning/effort choices remain
user-owned and adjustable. The installers do not call provider APIs or require
credentials; the setup proposal performs the lookup and passes the approved
values to the adapter.

Label the proposal as a recommended starting point, not a permanent team policy. The installers use the role-aware recommendation when no common override is supplied; an explicit common pair remains available for a reproducible baseline. Audit and retune preserve tuned values unless the user explicitly approves a change. Evaluate cheaper settings by accepted first-pass work and remediation cost, not nominal price alone.

## Operations

- **Initialize:** create only approved missing roles from the six shared archetypes in `templates/agents/`. On Codex, use `scripts/install_agent_team.py` for local TOML/config setup. On Claude Code, use `scripts/install_claude_agent_team.py` for local Markdown subagents; it makes no global settings change. Generate AGENTS role bullets from the selected roles. When propagation is approved, include the root `.gitignore` patch and `.worktreeinclude` in the same proposal. Existing roles require an explicit initialize replacement approval before `--replace`. If the user explicitly invokes initialization again, audit the managed `AGENTS.md` section and offer `--update-agents --refresh-agents` as a guidance-only update; it does not replace roles or config. An older unmarked section requires the exact dry-run plus explicit `--replace-agents-guidance`, and only that managed section may be replaced.
- **Audit:** read-only compare project agents, the repository-local router, and current repository docs; report stale facts, router or AGENTS schema drift, overlap, missing boundaries, required-field gaps, model/reasoning/effort/sandbox/permission drift, and capability gaps. Audit never needs `--replace` and never writes. A detected mismatch produces a proposed refresh, not an automatic overwrite. A later explicit initialization is the consent boundary for applying an approved guidance refresh.
- **Retune:** preserve every existing role field, including model, reasoning/effort, sandbox/permission, permissions, MCP, custom fields, and instructions. Use `--fill-missing` only to add absent required fields; it never overwrites a present value. Use `--update-instructions` only when the approved proposal explicitly changes the instruction field. Use `--update-profile` with explicit approved host-native model and reasoning/effort values to change only those profile fields; it does not replace role instructions or permissions.
- **Add:** add one specialist only for a demonstrated need; do not create a role for every technical layer.

Before approval, resolve current model values from the active host or the
provider's official model documentation/API, then show one role-by-role table
with `name`, purpose, exact host-native model value, reasoning/effort value,
sandbox/permission intent, and write access. Mark these values as the
recommended starting profile and explain that the user can adjust or hot-swap
them later. The adapter writes explicit values for reproducible local setup,
but those values are not immutable Plumbline policy. Do not invent slugs,
substitute `sol`/`luna` shorthand for Codex, or silently downgrade a user's
choice. Apply nothing before approval.

Before asking for approval, run the host-specific candidate installer with `--dry-run --format json` and include its exact file/operation/field manifest in the proposal: `install_agent_team.py` for Codex or `install_claude_agent_team.py` for Claude Code. The dry run is read-only and does not approve or apply changes.

After approval, audit and retune output must also report router freshness and AGENTS guidance drift without overwriting either file. A stale router produces a proposed refresh only; applying it requires the explicit router installer `--replace` path.

After approval, rerun the dry-run manifest; if the target changed, refresh the proposal before writing. Then rerun the host-specific installer in `initialize|audit|retune` mode. On an explicit repeat initialization, perform model discovery again and compare current project values with the resolved host values; if a refresh is approved, use `--mode retune --update-profile` with the exact selected model and reasoning/effort pair. This updates only those fields and preserves role instructions, permissions, sandbox/permission intent, and custom fields. Retune does not require `--replace`; its output reports the exact changed fields for every file. Use `--update-agents` and `--propagate` during first initialization only, when approved; use `--update-agents --refresh-agents` on an explicit repeat initialization to update only the managed guidance section. Validate every host role's required model, reasoning/effort, permission/sandbox, and no-child boundary, structurally valid user-owned host settings, AGENTS guidance, actual project-local discovery, ignore rules, and the manifest. Report one compact delegation-wave line with selected role names and host-native model plus reasoning/effort values; include effective values only when the host exposes a meaningful difference or the user asks, and use `Direct: <reason>` when no local role is available. If a matching local role is absent, stay on the main thread or report the capability gap; never fall back to a personal/global agent. Report that `.worktreeinclude` must be committed for future worktrees and that existing worktrees need explicit refresh. Run only a bounded, read-only discovery smoke test after approval.

## Completion

An audit is complete when it reports current role fields, instruction and
boundary drift, router/AGENTS guidance drift, and a read-only change proposal
without overwriting existing customization. Initialize or retune is complete
when the approved manifest is applied, exact changed fields are reported,
required host fields and no-child boundaries validate, project-local discovery
works, and worktree propagation is explained. The main thread remains the sole
dispatcher and Git owner after team setup.
