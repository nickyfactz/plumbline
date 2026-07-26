---
name: plumbline
description: Enter Plumbline at the latest safe phase from an idea, design, plan, implementation, bug, review request, accepted feature, or an uninitialized repository that needs guarded setup.
---

# Plumbline

You are the explicit front door. Inspect the user's request, supplied artifacts, conversation state, and only the repository context needed to identify the current phase.

Before phase selection, check whether the current repository has the project-local Plumbline router at `.agents/skills/plumbline-router/SKILL.md`. If it is absent, setup takes precedence: hand off to `$plumbline-init`, which remains read-only until the user approves its proposal. This applies even when the user only invokes `$plumbline` for ordinary work in a new repository. If the user says `init` or setup, give the same direct handoff; do not silently write files. If setup is declined, continue only with the user's explicitly chosen non-Plumbline work.

If the user supplies a controlling work order, active handoff, specification, or plan that already states the scope, non-goals, current checkpoint, acceptance/proof, lifecycle owner, and closeout boundary, adopt it as the active contract. Resume at its latest safe phase instead of recreating settled shaping, specification, or planning. This fast path does not bypass a new product decision, contradictory repository evidence, a failed gate, or an explicit approval boundary.

Choose exactly one:

- direct work for small, clear, low-risk maintenance or contract-complete work that needs no phase advancement;
- Diagnose for a defect, regression, failure, or performance problem;
- Shape when product intent or important behavior is unclear;
- Specification when intent is understood but the product contract is incomplete;
- Plan when a sufficient design exists but execution checkpoints do not;
- Execute when a sufficient specification and plan exist;
- Review when implementation exists and an independent assessment is requested;
- Closeout when accepted work needs reconciliation or integration.

Honor existing artifacts regardless of which workflow produced them. Ask only questions whose answers would change product behavior, scope, experience, privacy, security, destructive handling, cost, compatibility, or another hard-to-reverse choice. At phase entry or resume, state one lifecycle owner: `Plumbline <phase>` or the explicitly selected competing controller. Installed or enabled skills alone are available capabilities, not active ownership. If another explicitly selected orchestration loop owns checkpoint selection, plan advancement, review sequencing, or closeout, do not stack a second lifecycle controller; use Plumbline only for the selected phase contract. Supporting skills may research, implement, or review, but may not advance the plan or closeout. When Plumbline owns the lifecycle, state the selected phase in one sentence, do direct work directly, and otherwise invoke exactly one matching internal engine. Do not initialize an already-installed repository or create automatic routing from the front door.

At first entry or resume, resolve the currently loaded Plumbline installation root once from this front door's path (`<plugin-root>/skills/plumbline/SKILL.md`), read `<plugin-root>/.codex-plugin/plugin.json` once for its version, and reuse both for the phase. Treat every `references/<file>` path as relative to that root. Never persist or chase absolute versioned cache paths in repository artifacts; if a resumed root is gone, resolve the current installation once and continue. Use the active plan's compact resume record as the checkpoint summary; do not repeat routing, doctrine, or lifecycle narration on an unchanged resume.

Reference routing: Shape uses `product-autonomy.md` and `research-policy.md`; Specification uses `specification-template.md`, `artifact-lifecycle.md`, and `product-autonomy.md`; Plan uses `plan-schema.md`, `artifact-lifecycle.md`, and `research-policy.md`; Execute uses `runtime-value-testing.md`; Review uses `qa-audit.md`. Load only the phase's referenced files.
