# Live plan schema

For a blank repository, begin the live plan with:

```yaml
---
status: active
feature: <name>
specification: <relative path>
source: <relative path or null>
base_commit: <initial or recovery-boundary sha, or null>
current_checkpoint: CP-01
checkpoint_status: Pending
lifecycle_owner: Plumbline Plan
last_verified_commit: <sha or null>
next_safe_action: <one sentence>
delegation_roles: <selected local role names, Direct: reason, or null>
delegation_status: not-applicable | not-dispatched | direct | dispatched | returned | integrating
ready_for_acceptance: false
---
```

For a Plumbline-managed feature, keep one controlling feature and one plan. A sufficient external plan or work order may serve that role without being rewritten into Plumbline's schema. Each checkpoint should use a compact card by default:

```markdown
## CP-01: <Meaningful outcome>
**Status:** Pending | In Progress | Blocked | Complete | Reopened | Superseded
| Boundary | <write, ownership, and risk boundary> |
| Acceptance | <proof that makes the outcome complete> |
| Done when | <observable completion condition> |
| Evidence | <commands, artifacts, or UAT result> |
| Next action | <one safe next step> |
```

Expand the card with Outcome, Specification coverage, Dependencies, Execution topology, Shared ownership, Likely files and seams, Runtime protection, Verification, Canonical documentation impact, Completion criterion, Completion evidence, and Deviations and corrections only when a security, schema, rollback, public-contract, process-owner, irreversible, or similarly material boundary needs the detail. Execution topology may identify ready independent work, dependency edges, disjoint scopes, and a main-thread join condition; it does not name a fixed role map or create a scheduler artifact.

### Non-overridable failure transitions

`CHANGES_REQUIRED` sets the affected checkpoint to `Reopened`. `INCONCLUSIVE`,
environment failures, and test-harness failures set it to `Blocked` until the
evidence path is repaired or replaced through Diagnose. A failed attempt does
not abandon its candidate or objective, and `Blocked` or `Reopened` never
counts as checkpoint or plan completion. Severity sets urgency; it does not
decide terminality. A successor objective, `Superseded` status, or abandonment
requires accepted work or explicit user-approved defer/abandonment. Plan text
cannot override these transitions.

## Checkpoint shape

Prefer a **vertical slice**: one observable product behavior carried through the
relevant storage, service, interface, and proof seams. A slice may contain
internal layering such as schema, service, UI, and tests; the checkpoint is
complete when the behavior works as a whole, not when one technical layer is
finished in isolation.

Use a horizontal checkpoint when it is a real prerequisite, such as a shared
contract, migration, build foundation, or authentication seam. Label the
prerequisite, name the downstream slice it unlocks, and keep it minimal. For a
wide refactor, use expand, migrate in bounded batches, then contract. Never
split or merge work merely to satisfy the vocabulary of vertical slicing.

For every new or materially changed checkpoint, make the card answer four
questions: what will be observable, what proves it, what it depends on, and
what the main thread must join before downstream work starts. Use the smallest
card that answers those questions; do not turn it into a task transcript.

The frontmatter fields current_checkpoint, checkpoint_status, lifecycle_owner, last_verified_commit, next_safe_action, delegation_roles, and delegation_status are the single compact resume record. Update them together when the active checkpoint, safe next action, or delegation state changes; do not create a second checkpoint receipt. Checkpoints are coherent milestones, not micro-task transcripts. Blocked and Reopened stop advancement of that checkpoint; Execute may continue independent checkpoints when their dependencies permit, but neither status satisfies completion or authorizes closeout. Update the record after a checkpoint transition, evidence invalidation or material new evidence, a verified-commit change, a next-action change, or a material correction/blocker. Reconcile the expanded body at the same meaningful boundary; do not rewrite it after every command.

The current checkpoint is the resume location, not an implicit Execute stop. Unless the user explicitly selects checkpoint-by-checkpoint mode or the plan names a user approval gate, Execute advances through the remaining dependency order automatically and may batch ready independent work into main-mediated parallel waves. For delegated checkpoints, `delegation_roles` and `delegation_status` preserve the dispatch obligation across compaction; use `not-applicable` for checkpoints with no useful delegated unit. `Ready for Acceptance` is a final-plan state after every required checkpoint is complete, not a per-checkpoint status.

Treat checkout/worktree identity, HEAD/last_verified_commit, the plan-record hash, the applicable host configuration hash, and selected project-local role-file hashes as the resume fingerprint. For Codex, the applicable files include `.codex/config.toml` and selected role TOMLs; for Claude Code, they include selected `.claude/agents/*.md` files. Treat last_verified_commit and checkpoint completion evidence as the baseline until that fingerprint or a material contract/evidence input changes. A task resume, compaction, or conversational reminder alone does not invalidate it. At the next checkpoint, inspect the current delta and referenced paths first. Reuse unchanged evidence instead of rereading whole documents or rerunning broad checks. Reassess when the fingerprint changes, a new or failed check matters, a contract boundary changes, a defect appears, or the prior evidence may be stale.

A trusted host continuity hook may reintroduce a compact reminder after resume or compaction. It is not a new invocation and never replaces this resume record, changes the lifecycle owner, or advances the checkpoint; read the record and current delta first.

Every plan artifact or status announcement must support recovery, validation, authorization, or ownership. Omit ceremony that serves none of those purposes.

Whenever the plan is written, verify that exactly one current checkpoint is named, its frontmatter status matches the checkpoint, and next_safe_action points to that checkpoint. Do not leave a later checkpoint active while an earlier checkpoint is unresolved unless the plan explicitly records the dependency and current owner.

## Artifact adoption and open items

Do not require this frontmatter or checkpoint format for an external artifact that already provides sufficient scope, boundaries, proof, and next action. If a companion plan improves recovery, recommend it; do not block execution solely because it is absent.

Label unresolved items as Acceptance blocker, Residual risk, Operational follow-up, or Future enhancement. An Acceptance blocker or an unresolved `Blocked`/`Reopened` checkpoint prevents Ready for Acceptance. Preserve non-blocking categories as explicit residual state rather than reopening planning to eliminate them.

Rolling telemetry is sample evidence, not automatically durable truth. Record the observation date or generation/window and stable assertions separately from changing counts; do not rewrite acceptance merely because a live count moved.
