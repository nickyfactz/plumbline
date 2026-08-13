---
name: plumbline
description: Enter Plumbline at the latest safe phase from an idea, design, plan, implementation, bug, review request, accepted feature, or an uninitialized repository that needs guarded setup.
disable-model-invocation: true
---

# Plumbline

You are the explicit front door. Inspect the user's request, supplied artifacts, conversation state, and only the repository context needed to identify the current phase.

First distinguish setup from phase work:

- If the user explicitly asks for initialization or setup, hand off to the explicit `plumbline-init` skill. In Codex this is `$plumbline-init`; in Claude Code it is `/plumbline:plumbline-init`. It remains read-only until the user approves its proposal.
- An explicitly invoked phase side door may run without a project-local router or agent team. Use convention mode: honor supplied artifacts and ordinary repository conventions, and keep execution on the main thread when no local role exists.
- If the front door is invoked in a repository without the project-local Plumbline router, offer setup for an ordinary unclassified request. If the request supplies a sufficient external specification, plan, handoff, or work order, assess that artifact set first and continue at the appropriate phase; setup is optional, not a prerequisite for the artifact-backed work.

If setup is declined, continue with the user's explicitly chosen phase or non-Plumbline work. Do not silently write files or create automatic routing.

Before choosing a phase, perform a task-scoped artifact sufficiency check:

- Inspect files or artifacts explicitly supplied or named by the user first.
- Then inspect the repository's existing conventional specification, plan, handoff, and documentation locations.
- Do not require Plumbline-generated paths, frontmatter, checkpoint IDs, or lifecycle fields.
- Select one controlling artifact set for this task; unrelated specifications or plans in the repository are not blockers.
- A sufficient external specification may proceed to Plan or Execute. A sufficient external plan or work order may proceed to Execute even without a separate specification.
- Recommend a companion artifact when it would improve recovery, but do not block a sufficient artifact solely because the companion is absent.
- Return to Shape only when a material product decision remains unresolved.

Report this preflight only when it adopts an external artifact, recommends a companion, finds competing candidates, or encounters a real blocker. Do not repeat it on an unchanged resume.

If the user supplies a controlling work order, active handoff, specification, or plan that already states enough scope, non-goals, behavior, acceptance/proof, current execution state, or closeout boundary for the requested phase, adopt it as the active contract. Resume at its latest safe phase instead of recreating settled shaping, specification, or planning. This fast path does not bypass a new product decision, contradictory repository evidence, a failed gate, or an explicit approval boundary.

Choose exactly one:

- direct work for small, clear, low-risk maintenance or contract-complete work that needs no phase advancement;
- Diagnose for a defect, regression, failure, or performance problem;
- Shape when product intent or important behavior is unclear;
- Specification when the product contract is incomplete or a supplied artifact needs adoption/normalization;
- Plan when a sufficient design exists but execution checkpoints do not;
- Execute when a sufficient plan, work order, or specification with execution topology exists;
- Review when implementation exists and an independent assessment is requested;
- Closeout when accepted work needs reconciliation or integration.

When Execute is selected for an approved plan, it owns the full remaining checkpoint traversal by default. Do not route an architect's in-scope uncertainty back to Shape merely because the worker phrased it as a product question; the main orchestrator resolves and records it unless an explicit user gate or genuine hard stop applies.

Honor existing artifacts regardless of which workflow produced them. Ask only questions whose answers would change product behavior, scope, experience, privacy, security, destructive handling, cost, compatibility, or another hard-to-reverse choice. At phase entry or resume, state one lifecycle owner: `Plumbline <phase>` or the explicitly selected competing controller. Installed or enabled skills alone are available capabilities, not active ownership. If another explicitly selected orchestration loop owns checkpoint selection, plan advancement, review sequencing, or closeout, do not stack a second lifecycle controller; use Plumbline only for the selected phase contract. Supporting skills may research, implement, or review, but may not advance the plan or closeout. When Plumbline owns the lifecycle, state the selected phase in one sentence, do direct work directly, and otherwise use exactly one matching internal engine. If the host cannot dispatch a nested skill, read that engine's sibling `SKILL.md` from the installed plugin and follow it directly. Do not initialize an already-installed repository or create automatic routing from the front door.

At first entry or resume, resolve the currently loaded Plumbline installation root once from this front door's path (`<plugin-root>/skills/plumbline/SKILL.md`), read `<plugin-root>/.codex-plugin/plugin.json` once for its version, and reuse both for the phase. Treat every `references/<file>` path as relative to that root. Never persist or chase absolute versioned cache paths in repository artifacts; if a resumed root is gone, resolve the current installation once and continue. Use an active plan's compact resume record when one exists; otherwise use the controlling external artifact and current Git state. Do not repeat routing, doctrine, lifecycle, or artifact preflight narration on an unchanged resume.

A trusted host continuity hook may remind the model after a resume or compaction that the user explicitly activated Plumbline earlier. Treat that as a continuity reminder, not a new invocation: read the active plan or resume record, preserve the recorded lifecycle owner and phase, and continue. Do not rerun setup, select a new phase, or create an artifact because the reminder appeared.

Reference routing: when shaping product intent or external capability questions, load `product-autonomy.md` and `research-policy.md`; when creating or adopting a specification, load `specification-template.md`, `artifact-lifecycle.md`, and `product-autonomy.md`; when creating or updating a checkpoint plan, load `plan-schema.md`, `artifact-lifecycle.md`, and `research-policy.md`; when executing or reviewing runtime proof, load `runtime-value-testing.md`; when dispatching or auditing workers, load `subagent-orchestration.md`; when reviewing acceptance, load `qa-audit.md`. Load only the references for the selected branch.
