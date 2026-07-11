---
name: plumbline-router
description: Route ordinary repository prompts through Plumbline only after this repository explicitly installed this local router.
---

# Plumbline Router

This file is the repository's only automatic Plumbline activation boundary. It is present only after explicit `$plumbline-init` approval; deleting this directory disables automatic routing.

Read the user's request and the minimum repository context. Choose one path:

- direct work for small, clear, low-risk maintenance;
- `$plumbline-diagnose-engine` for a bug, regression, failure, or performance issue;
- `$plumbline-shape-engine` when product intent is unclear;
- `$plumbline-spec-engine` when intent is settled but the contract is not tracked;
- `$plumbline-plan-engine` when a sufficient design exists but execution checkpoints do not;
- `$plumbline-execute-engine` when an active spec and plan exist;
- `$plumbline-review-engine` for an independent audit;
- `$plumbline-closeout-engine` for accepted work.

Use only one path, preserve explicit user overrides, and never invoke initialization, agent-team setup, or offboarding automatically. Do not load downstream doctrine before selecting the phase. If the plugin is disabled or the selected engine is unavailable, leave the request in the user's normal workflow.
