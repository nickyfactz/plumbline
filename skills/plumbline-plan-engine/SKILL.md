---
name: plumbline-plan-engine
description: Internal Plumbline engine. Use only after the Plumbline router or a Plumbline phase wrapper selects checkpoint planning.
---

# Plan engine

Create one live implementation plan for one product outcome. Read the active specification, repository instructions, canonical docs, current Git state, validation commands, and relevant code seams. Read references/plan-schema.md, references/artifact-lifecycle.md, and references/research-policy.md when available.

Keep the feature whole. Use meaningful chronological checkpoints, usually a small handful rather than micro-tasks. Batch adjacent evidence-only, packaging, receipt, or documentation work into its parent implementation checkpoint. Create a separate checkpoint only when the work has an independent outcome or acceptance gate, rollback boundary, material risk/contract boundary, or owner. Do not split a coherent outcome only to narrate proof steps. Use the compact checkpoint card from references/plan-schema.md by default and expand only for material boundaries. Map every acceptance criterion to a checkpoint. Mark shared contracts and shared files so false parallelism is visible.

Use the repository's existing plan location; for a blank repository default to docs/plans/<feature-slug>.md. Track statuses Pending, In Progress, Blocked, Complete, Reopened, and Superseded. Keep the plan resumable from source/spec/plan/Git state after compaction. Do not put full implementation code or two-minute task transcripts in it. Every plan artifact or announcement must support recovery, validation, authorization, or ownership.

Create a kickoff or recovery-boundary commit before implementation when the user or repository requires it, when work must survive multi-session/operator recovery, when a material ABI/schema/product contract is being established, or when an auditable approval boundary needs it. Otherwise, keep the intended source/spec/plan artifacts tracked but uncommitted until the first coherent boundary. Stage only intended files; never absorb unrelated dirty work. Explicit planning stops after the plan and its current recovery state. Tell the user to run $plumbline-execute when ready.
