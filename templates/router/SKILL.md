---
name: plumbline-router
description: Route ordinary repository prompts through Plumbline only after this repository explicitly installed this local router.
---

# Plumbline Router

This is the repository's only automatic Plumbline activation boundary. It exists only after explicit `$plumbline-init` approval; deleting it disables automatic routing.

For ordinary prompts, hand control to the installed `plumbline` front door. It selects exactly one safe phase and owns lifecycle decisions; do not copy phase doctrine into this repository-local shim.

Honor explicit overrides. Never auto-initialize, set up teams, dispatch workers, or advance a plan from this shim. If the plugin is disabled or unavailable, use the normal workflow.

The selected phase owns delegation and reports its own role, model, reasoning, and boundary values. This shim never selects global agents or creates child workers.
