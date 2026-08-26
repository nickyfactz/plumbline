---
name: plumbline-plan-engine
description: Internal Plumbline engine. Use only after the Plumbline router or a Plumbline phase wrapper selects checkpoint planning.
---

# Plan engine

## Outcome and completion

Create one live implementation plan for one product outcome. The plan is the
execution itinerary, not a task transcript or an implementation diary.

Planning is artifact-agnostic. Accept a sufficient external plan or work order
without forcing it into Plumbline's file shape.

Use `execution_mode: continuous` for a new Plumbline plan unless the user
explicitly selects Checkpoint Relay. A missing mode in an imported plan also
means continuous. When Relay is selected, record
`execution_mode: checkpoint_relay`, load `references/checkpoint-relay.md`, and
plan explicit durable checkpoint boundaries. Do not infer Relay from plan size,
host capability, or checkpoint count, and do not put host transport details in
the shared plan.

Planning is complete when one controlling plan records the outcome, scope,
non-goals, checkpoint dependency order, proof, current checkpoint, lifecycle
owner, and one safe next action. Stop after planning; the user or router selects
the explicit `plumbline-execute` phase when implementation is wanted.

Plans cannot override Plumbline lifecycle invariants. A failed acceptance result
keeps the same candidate and objective active until it is accepted or the user
explicitly defers or abandons it; an ordinary diagnostic failure remains
working state rather than becoming a new attempt record.

Apply the plan schema's execution-economy rule: a plan may add stricter proof
requirements, but it must not mandate reseal, rebuild, or replay for every
diagnostic correction when durable inputs and the proof boundary are unchanged.

## Read the controlling inputs

Read the active specification, supplied design or work order, repository
guidance, canonical documentation, current Git state, validation commands, and
the relevant code seams. When creating or updating a Plumbline plan, read
`references/plan-schema.md` and `references/artifact-lifecycle.md`. Read
`references/research-policy.md` when the plan depends on external capability
evidence. Resolve the repository's existing plan location before choosing a
blank-repository default of `docs/plans/<feature-slug>.md`.

Adopt a sufficient external specification, design, handoff, plan, or work order
even when it has no Plumbline frontmatter or conventional path. A companion
specification or plan is useful only when it materially improves product
clarity or recovery. When several artifacts could control the same task, name
the competing candidates and the ambiguity; keep one controlling source rather
than silently merging them.

## Shape meaningful checkpoints

Keep the product outcome whole and use a small number of meaningful
checkpoints. Batch adjacent evidence-only, packaging, receipt, and
documentation work into its parent implementation checkpoint. Split only for
an independent outcome or acceptance gate, rollback boundary, material
contract/risk boundary, or distinct owner.

Prefer a **vertical slice**: one observable behavior carried through the
relevant storage, service, interface, and proof seams. Internal implementation
may still proceed in layers; the checkpoint is complete when the behavior works
as a whole. For each slice, state its observable outcome, completion condition,
proof, dependencies, write/review scope, and main-thread join condition.

Use a horizontal checkpoint when a shared contract, migration, build
foundation, authentication seam, or other prerequisite genuinely must precede
the behavior. Label the prerequisite, identify the downstream slice it
unlocks, and keep it minimal. For broad refactors, use expand, migrate in
bounded batches, then contract. Never split or merge work merely to satisfy a
planning label. Do not split a coherent outcome only to narrate proof steps.

Map every acceptance criterion to a checkpoint. Mark shared contracts and
shared files so false parallelism is visible. Within that topology, identify
ready independent research, architecture, review, or implementation work and
its main-thread join condition for safe parallel waves. Parallelism is useful
only when it shortens the path without weakening the contract.

Use the compact checkpoint card from `references/plan-schema.md` by default.
Expand it only for a material boundary. Every plan should answer:

- What observable behavior or prerequisite is this checkpoint delivering, and what proof obligation makes it complete?
- What proves completion, and what is the `Done when` condition?
- What does it depend on, own, or share?
- What must the main thread join before downstream work begins?

Keep the live plan as a current-state projection, not an append-only diary.
Rewrite the compact card and resume fields in place with current decisions,
status, evidence pointers, residuals, and next action. Summarize the conclusion
from raw attempts, transcripts, logs, and superseded approaches, then clean that
clearly task-owned working material unless a named future consumer needs it.
Prefer pointers to
source paths, functions, commits, canonical docs, reusable artifacts, and
required audit evidence over copied output. Every update replaces and prunes
stale state in the same edit. Collapse completed checkpoints to status, accepted
outcome/proof pointer, and live residuals; keep execution detail only for the
current checkpoint. Remove legacy attempt chronology and agent lifecycle history
instead of marking it non-authoritative.

Before completing a plan mutation, verify idempotence and rehydration: writing
the same current state again adds nothing, and a fresh agent can recover the
active outcome, blockers/residuals, trusted proof pointers, and next action
without superseded events.

## Add risk-shaped proof

For a checkpoint involving material state, persistence, concurrency, security,
a public contract, or cross-boundary ownership transfer, expose the applicable
identity/ownership, transition and terminal-ordering, failure/recovery/
cancellation or shutdown, compatibility, and runtime-proof requirements in one
compact scenario-to-proof matrix. Include only relevant rows. This is a risk
filter, not a universal checklist and not a reason to create micro-checkpoints.

Carry that matrix into the implementer and QA briefs when it exists. For a
material checkpoint, make the checkpoint card or matrix sufficient to form a
transient dispatch contract: outcome, invariants and owners, operation or
partial-failure boundary, edge behavior, proof, write set, non-goals, and
assumptions. Keep it in the prompt; it is not a new durable artifact.

Identify known proof obligations before implementation from acceptance criteria,
invariants, contracts, and meaningful regression risks. A new durable behavior
discovered during implementation may extend the existing proof/evidence surface;
do not create a second testing artifact or a test-count target.

## Resolve uncertainty at the right level

Resolve technical boundaries, names, module placement, test seams, and ordinary
implementation choices from repository evidence and safe reversible defaults.
If an architect finds a material product uncertainty, return a structured
escalation to the main orchestrator. The main thread may use the existing Shape
conversation inside the active goal, preserve the lifecycle owner, and block
only the dependent checkpoint while independent work continues. The escalation
does not end the goal or create a competing plan.

## Maintain resumable state

Use statuses `Pending`, `In Progress`, `Blocked`, `Complete`, `Reopened`, and
`Superseded` when the plan is Plumbline-managed. Keep the compact resume fields
and the body synchronized. Before saving a plan update, verify exactly one
current checkpoint, matching frontmatter status, and a `next_safe_action` that
points to it. Classify unresolved items as Acceptance blocker, Residual risk,
Operational follow-up, or Future enhancement. `Blocked` and `Reopened` stop the
affected checkpoint and never count as completion. An Acceptance blocker or an
unresolved `Blocked`/`Reopened` checkpoint prevents `Ready for Acceptance`; it
does not authorize abandoning the objective. Use `Superseded` only after
accepted work or an explicit user-approved defer or abandonment.

## Preserve the objective, compact the evidence

Normalize checkpoint outcomes as follows: `CHANGES_REQUIRED` from review
reopens the affected checkpoint. `INCONCLUSIVE`, environment failures, and
harness failures block it only when they prevent safe progress beyond a bounded
repair; otherwise keep the checkpoint in progress while Diagnose repairs or
replaces the evidence path. The same candidate returns through correction and
review. P0/P1 severity does not automatically mean rejection, rollback,
abandonment, or fresh owner selection. Reject a plan clause that maps severity
directly to those terminal actions. If safety requires a rollback, preserve the
candidate in durable Git history before the main thread rolls it back; an
ignored patch or build output is disposable working material, not candidate
retention. A successor objective is not eligible while the current objective
is unresolved.

For a checkpoint with useful delegated work, reserve the compact
`delegation_roles`/`delegation_status` fields for Execute to carry delegation
across compaction. Use `not-applicable` when no bounded role-owned unit exists;
an imported plan may use its existing equivalent state instead of being
rewritten into this schema.

Treat changing telemetry as timestamped sample evidence rather than a reason to
rewrite stable acceptance. Keep the plan recoverable from the controlling
source, specification, Git state, and last verified evidence after compaction.
Every artifact or announcement must support recovery, validation,
authorization, or ownership; omit the rest.

Create a kickoff or recovery-boundary commit only when the user or repository
requires it, recovery across sessions needs it, a material contract is being
established, or an auditable approval boundary calls for it. Otherwise keep
source, specification, and plan changes uncommitted until the first coherent
boundary. Stage only intended files and preserve unrelated dirty work.

Unless the user explicitly requests checkpoint-by-checkpoint execution or a
checkpoint contains a deliberate approval gate, the checkpoint sequence is the
full execution itinerary. Checkpoints are internal team handoffs, not implicit
user pauses.
