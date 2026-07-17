---
name: plumbline-execute-engine
description: Internal Plumbline engine. Use only after the Plumbline router or a Plumbline phase wrapper selects checkpoint execution.
---

# Execute engine

Read the active source, specification, plan, current checkpoint, Git status, canonical docs, and repository validation commands before changing files. Recover from those artifacts rather than chat memory. Keep one active checkpoint and never advance while it is `Blocked` or `Reopened`.

Use Codex-managed worktrees for scoped/designed feature work when the host provides them. Never create, remove, register, or clean up worktrees from Plumbline instructions. Direct work and small fixes may stay on the active checkout. Inspect repository-owned environment setup before proposing changes; use absolute tools and environment variables, and treat borrowed resources as read-only.

The main thread is the only Git writer. Subagents receive bounded briefs with disjoint write sets, a named contract, expected evidence, and a no-Git/no-active-plan-edit rule. Serialize any shared-file or shared-contract work. Pause if a worker expands its write set.

Before each checkpoint that could benefit from delegation, inspect the project-local `.codex/agents/` and `.codex/config.toml`. Select the matching local `researcher`, architect, `implementer`, or `qa-auditor` only when the brief is bounded and the local configuration is valid. Report-only roles (researcher, architect, and QA) get no write set; reject briefs that ask them to edit source, tests, scripts, documentation, or Git state. Their `sandbox_mode = "read-only"` is intent, not proof; a writable parent is normal for a goal and may affect the child's effective sandbox. State `Delegated: <role>` plus `Boundary: report-only; no write set` before dispatch, and record configured/effective sandbox values when observable. Inspect Git status/diff after the worker returns and never silently integrate unexpected edits. Use `Direct: delegation prohibited or effective read-only isolation unavailable` only when hard read-only isolation is required. Never select personal/global custom agents or any global fallback. Workers never spawn children; `agents.max_depth = 1` is the project recommendation.

At each checkpoint: re-read the relevant contract, implement the smallest vertical slice, run the narrowest meaningful checks, apply the runtime-value test gate from `references/runtime-value-testing.md`, integrate worker changes, record evidence and deviations in the plan, then commit once. A test is valuable when it protects stable public behavior or a plausible regression; a non-test check, manual UAT, static validation, or justified no-test outcome is allowed. Do not add tests that freeze prose, private structure, or literal configuration defaults.

Stop for product decisions, destructive uncertainty, missing environment capability, or failed validation. Report the exact blocker and preserve the current checkpoint state.
