---
name: plumbline-router
description: Route ordinary repository prompts through Plumbline only after this repository explicitly installed this local router.
---

# Plumbline Router

This is the repository's only automatic Plumbline activation boundary. It exists only after explicit `$plumbline-init` approval; deleting it disables automatic routing.

For ordinary prompts, invoke the installed Plumbline front door using the callable name advertised by the host (`$plumbline` when available).

If unavailable, take only currently visible `plumbline:*` skill paths, derive their plugin root from `<root>/skills/<skill>/SKILL.md`, and run `python "<root>/scripts/resolve_front_door.py" --skill-path "<visible-path>"` (repeat `--skill-path` per path). Read the returned front-door file and follow it, reporting `Plumbline: loaded installed front door directly` once. Resolve references from that installation. Never select cached versions by age or reuse saved cache paths.

If capabilities are absent, invalid, or ambiguous, report `Blocked: Plumbline routing unavailable` with the repair needed; stop before ordinary implementation. Honor explicit overrides. Never substitute a `plumbline-*-engine` skill, auto-initialize, set up teams, dispatch workers, or advance a plan from this shim. The real front door owns phase selection and lifecycle decisions.
