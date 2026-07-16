---
name: plumbline-router
description: Route ordinary repository prompts through Plumbline only after this repository explicitly installed this local router.
---

# Plumbline Router

This is the repository's only automatic Plumbline activation boundary. It exists only after explicit `$plumbline-init` approval; deleting it disables automatic routing.

Read the request and minimum repository context. Select exactly one path:

- direct work for small, clear, low-risk maintenance;
- `$plumbline-diagnose-engine` for bugs, failures, regressions, or performance issues;
- `$plumbline-shape-engine` when product intent is unclear;
- `$plumbline-spec-engine` when intent is clear but the contract is untracked;
- `$plumbline-plan-engine` when a design exists but execution checkpoints do not;
- `$plumbline-execute-engine` when an active spec and plan exist;
- `$plumbline-review-engine` for an independent audit;
- `$plumbline-closeout-engine` for accepted work.

Preserve explicit user overrides. Never invoke initialization, team setup, or offboarding automatically. Do not load downstream doctrine before selecting. If Plumbline is disabled or the engine is unavailable, leave the request in the normal workflow.

Before a non-direct path, the engine checks project-local `.codex/agents/` and `.codex/config.toml`. Delegate bounded work only to a matching local role and state `Delegated: <role>`. Never select personal/global agents. If no local role exists, state `Direct: <reason>`. Workers never spawn children; `agents.max_depth = 1` is the ceiling.
