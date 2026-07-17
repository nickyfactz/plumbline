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

Honor explicit overrides. Never auto-initialize, set up teams, or load downstream doctrine. If disabled or unavailable, use the normal workflow.

Before non-direct work, check local roles/config and delegate only a match. State `Delegated: <role>` or `Direct: <reason>`. Report-only roles get no write set; sandbox intent may be affected by a writable parent. Inspect diffs. Never use global agents or child workers; `agents.max_depth = 1`.
