---
name: plumbline-plan-engine
description: Internal Plumbline engine. Use only after the Plumbline router or a Plumbline phase wrapper selects checkpoint planning.
---

# Plan engine

Create one live implementation plan for one product outcome. Read the active specification, repository instructions, canonical docs, current Git state, validation commands, and relevant code seams. Read references/plan-schema.md, references/artifact-lifecycle.md, and references/research-policy.md when available.

Planning is artifact-agnostic. Adopt a sufficient external specification, design, handoff, external plan or work order even when it has no Plumbline frontmatter or conventional path. A separate active specification is recommended only when the product contract is incomplete or recovery would materially benefit. If a supplied plan already contains scope, boundaries, checkpoints, proof, and the next safe action, adopt it instead of creating a competing plan. If several artifacts could control the same task, report the competing candidates and ambiguity; do not merge them silently.

Keep the feature whole. Use meaningful chronological checkpoints, usually a small handful rather than micro-tasks. Batch adjacent evidence-only, packaging, receipt, or documentation work into its parent implementation checkpoint. Create a separate checkpoint only when the work has an independent outcome or acceptance gate, rollback boundary, material risk/contract boundary, or owner. Do not split a coherent outcome only to narrate proof steps. Use the compact checkpoint card from references/plan-schema.md by default and expand only for material boundaries. Map every acceptance criterion to a checkpoint. Mark shared contracts and shared files so false parallelism is visible.

For a checkpoint involving material state, persistence, concurrency, security, a public contract, or cross-language ownership transfer, make the acceptance expose the applicable identity/ownership, transition and terminal-ordering, failure/recovery/cancellation or shutdown, compatibility, and runtime-proof requirements. Do not combine independently mutable state machines or ownership transfers unless they share one acceptance and rollback boundary. This is a risk filter, not a universal checklist, and must not create micro-checkpoints.

Use the repository's existing plan location only when a durable plan is warranted; for a blank repository default to docs/plans/<feature-slug>.md. Track statuses Pending, In Progress, Blocked, Complete, Reopened, and Superseded when using a Plumbline plan. Keep the plan resumable from the controlling source/spec/plan/Git state after compaction. Do not put full implementation code or two-minute task transcripts in it. Every plan artifact or announcement must support recovery, validation, authorization, or ownership.

Before saving a plan update, verify exactly one current checkpoint, matching frontmatter status, and a next_safe_action that points to that checkpoint. Classify unresolved items as Acceptance blocker, Residual risk, Operational follow-up, or Future enhancement; only the first blocks advancement. Treat changing telemetry as timestamped sample evidence rather than a reason to rewrite acceptance.

If implementation or review reveals a material contract, ownership, or state-transition invariant missing from the plan, mark the affected checkpoint Reopened and return to Plan or the applicable architect review before continuing. Keep a small implementation defect in Execute when the accepted contract remains unchanged.

Create a kickoff or recovery-boundary commit before implementation when the user or repository requires it, when work must survive multi-session/operator recovery, when a material ABI/schema/product contract is being established, or when an auditable approval boundary needs it. Otherwise, keep the intended source/spec/plan artifacts tracked but uncommitted until the first coherent boundary. Stage only intended files; never absorb unrelated dirty work. Explicit planning stops after the plan and its current recovery state. Tell the user to use the explicit `plumbline-execute` skill when ready.
