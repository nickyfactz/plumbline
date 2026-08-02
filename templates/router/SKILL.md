---
name: plumbline-router
description: Route ordinary repository prompts through Plumbline only after this repository explicitly installed this local router.
---

# Plumbline Router

This is the repository's only automatic Plumbline activation boundary. It exists only after explicit `$plumbline-init` approval; deleting it disables automatic routing.

For ordinary prompts, invoke the installed `$plumbline` front door by that exact skill name. It selects exactly one safe phase and owns lifecycle decisions; do not copy phase doctrine into this repository-local shim.

Honor explicit overrides. Never substitute a `plumbline-*-engine` skill, auto-initialize, set up teams, dispatch workers, or advance a plan from this shim. If `$plumbline` cannot be resolved, state `Direct: Plumbline front door unavailable`; do not claim Plumbline lifecycle ownership or execute checkpoints from this shim.

The selected phase owns delegation and reports its own role, model, reasoning, and boundary values. The main thread is the only worker dispatcher: worker recommendations are advisory and every worker returns to the main thread before another capability is selected. This shim never selects global agents or creates child workers.
