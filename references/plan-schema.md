# Live plan schema

For a blank repository, begin the live plan with:

```yaml
---
status: active
feature: <name>
specification: <relative path>
source: <relative path or null>
base_commit: <initial or recovery-boundary sha, or null>
git_policy: required | optional | forbidden
execution_mode: continuous | checkpoint_relay
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

`git_policy` defaults to `required` for material multi-step work when the
checkout is Git-controlled, and to `optional` for trivial direct work. Use
`forbidden` only when the user explicitly opts out. A sufficient imported plan
may express the same policy in its own terms; do not reject it for lacking this
field.

`execution_mode` is optional for imported or older plans. A missing value means
`continuous`, which preserves full-plan traversal. Use `checkpoint_relay` only
when the user explicitly selects fresh root-conversation boundaries between
checkpoints. Do not infer it from plan size or silently change it. Resolve the
automatic or manual host boundary through `checkpoint-relay.md`; the shared
plan contains no host transport details.

For a Plumbline-managed feature, keep one controlling feature and one plan. A sufficient external plan or work order may serve that role without being rewritten into Plumbline's schema. Each checkpoint should use a compact card by default:

```markdown
## CP-01: <Meaningful outcome>
**Status:** Pending | In Progress | Blocked | Complete | Reopened | Superseded
| Boundary | <write, ownership, and risk boundary> |
| Acceptance | <proof that makes the outcome complete> |
| Done when | <observable completion condition> |
| Proof | <compact accepted result and useful pointer; pending while unresolved> |
| Next action | <one safe next step> |
```

Expand the card with Outcome, Specification coverage, Dependencies, Execution topology, Shared ownership, Likely files and seams, Runtime protection, Verification, Canonical documentation impact, Completion criterion, Completion evidence, and Current material deviations only when a security, schema, rollback, public-contract, process-owner, irreversible, or similarly material boundary needs the detail. Execution topology may identify ready independent work, dependency edges, disjoint scopes, and a main-thread join condition; it does not name a fixed role map or create a scheduler artifact.

### Non-overridable failure transitions

`CHANGES_REQUIRED` from review sets the affected checkpoint to `Reopened`.
`INCONCLUSIVE`, environment failures, and test-harness failures set it to
`Blocked` only when they prevent safe progress and cannot be repaired inside
the current execution flow. An ordinary diagnostic or bounded evidence-path
repair leaves the checkpoint `In Progress`; it updates plan state only when the
current conclusion, blocker, residual, or next action materially changes. A
failed command does not abandon its candidate or objective, and `Blocked` or
`Reopened` never counts as checkpoint or plan completion. Severity sets urgency;
it does not decide terminality. A successor objective, `Superseded` status, or
abandonment requires accepted work or explicit user-approved defer/abandonment.
Plan text cannot override these transitions.

Execution economy is also a lifecycle constraint. An imported or generated plan
may require stricter product, safety, or acceptance evidence, but it cannot
mandate reseal, rebuild, or replay for every diagnostic or evidence-only
correction when the durable contract, sealed artifact, and proof boundary are
unchanged. Treat that clause as a plan defect and narrow the cadence before
execution. Repeat the full gate when a durable input, artifact, contract,
ownership, or risk boundary changes, or when acceptance explicitly requires it.

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

Treat `Acceptance` and `Proof` as behavioral proof obligations: name observable
behavior, an invariant, a public/interface contract, a meaningful regression
risk, or a durable edge case. A test is one evidence method, not the obligation;
do not set test-count or coverage targets.

The frontmatter fields current_checkpoint, checkpoint_status, lifecycle_owner, last_verified_commit, next_safe_action, delegation_roles, and delegation_status are the single compact resume record. Update them together when the active checkpoint, safe next action, or delegation state changes; do not create a second checkpoint receipt. Checkpoints are coherent milestones, not micro-task transcripts. Blocked and Reopened stop advancement of that checkpoint; Execute may continue independent checkpoints when their dependencies permit, but neither status satisfies completion or authorizes closeout. Update the record after a checkpoint transition, evidence invalidation or material new evidence, a verified-commit change, a next-action change, or a material correction/blocker. Reconcile the expanded body at the same meaningful boundary; do not rewrite it after every command.

The active plan is a current-state projection, not an append-only diary. Rewrite
checkpoint cards and resume fields in place so they retain current status,
accepted decisions, latest evidence pointers, residual risks or deviations,
and the next safe action. Summarize the material conclusion from raw attempts,
transcripts, command logs, and superseded approaches, then discard or clean
clearly task-owned working material unless an identifiable future consumer
needs it. Point
to source paths, functions, commits, canonical docs, reusable artifacts, or
required audit evidence instead of copying their contents into the plan.
Each plan update is replace-and-prune: patch the new truth and remove the stale
status, superseded approach, prior next action, and resolved blocker in the same
edit. A completed or superseded checkpoint collapses to its status, accepted
outcome/proof pointer, and any still-live residual; only the current checkpoint
keeps execution detail. The active plan contains no attempt chronology, daily
progress log, completed-command list, transcript, or agent lifecycle history.
When chronology is genuinely required, link the exact relevant section of an
existing audit or operational record without copying it. Compact legacy history
out at the next meaningful plan update.

Apply two checks after every plan mutation. **Idempotence:** writing the same
current state again produces no additional text. **Rehydration:** a fresh agent
can identify the current outcome, active checkpoint, blockers/residuals, trusted
proof pointers, and next action without reading superseded events.

In `continuous` mode, the current checkpoint is the resume location, not an implicit Execute stop. Unless the user explicitly selects checkpoint-by-checkpoint control or the plan names a user approval gate, Execute advances through the remaining dependency order automatically and may batch ready independent work into main-mediated parallel waves. In explicit `checkpoint_relay` mode, complete the current checkpoint, establish the durable handoff defined by `checkpoint-relay.md`, and stop before the successor starts in the same root conversation. For delegated checkpoints, `delegation_roles` and `delegation_status` preserve the dispatch obligation across compaction; use `not-applicable` for checkpoints with no useful delegated unit. `Ready for Acceptance` is a final-plan state after every required checkpoint is complete, not a per-checkpoint status.

Treat checkout/worktree identity, HEAD/last_verified_commit, the plan-record hash, the applicable host configuration hash, and selected project-local role-file hashes as the resume fingerprint. For Codex, the applicable files include `.codex/config.toml` and selected role TOMLs; for Claude Code, they include selected `.claude/agents/*.md` files. Treat last_verified_commit and checkpoint completion evidence as the baseline until that fingerprint or a material contract/evidence input changes. A task resume, compaction, or conversational reminder alone does not invalidate it. At the next checkpoint, inspect the current delta and referenced paths first. Reuse unchanged evidence instead of rereading whole documents or rerunning broad checks. A role/config hash change alone is a dispatch-profile refresh: update the fingerprint and use current values for new workers without automatically invalidating checkpoint evidence or reopening the plan. Reassess when a changed config affects capability or permission materially, a new or failed check matters, a contract boundary changes, a defect appears, or the prior evidence may be stale.

A trusted host continuity hook may reintroduce a compact reminder after resume or compaction. It is not a new invocation and never replaces this resume record, changes the lifecycle owner, or advances the checkpoint; read the record and current delta first.

When `git_policy` is `required`, Execute establishes a clean recovery boundary
before the first material checkpoint and after every accepted checkpoint. The
main thread creates commits at coherent checkpoint or batch boundaries by
default and states that policy once; the user may explicitly opt out. Commit
only plan-owned changes; keep unrelated dirty work, scratch, and secrets out of
the commit. Record the resulting commit in the plan's `last_verified_commit` or
proof pointer before advancing. Do not advance to a dependent checkpoint with
uncommitted plan-owned changes. Ask before push, force-push, history rewriting,
or external publication. If Git is absent, recommend establishing it before
Execute; an explicit opt-out continues with a visible Git-unanchored warning.
`optional` permits a dirty working tree, while `forbidden` suppresses Git
actions by explicit user choice.

The plan-record hash used for proof reuse must cover durable contract inputs, not
mutable checkpoint status, evidence logs, telemetry, or correction notes. Those
records update recovery state without automatically invalidating prior proof.

Every plan artifact or status announcement must support recovery, validation, authorization, or ownership. Omit ceremony that serves none of those purposes.

This projection and retention guidance applies only when a live plan is useful
or already controls the work. Small direct changes and sufficient imported work
orders do not need a Plumbline plan, checkpoint receipt, evidence directory, or
cleanup phase merely to satisfy this schema.

Whenever the plan is written, verify that exactly one current checkpoint is named, its frontmatter status matches the checkpoint, and next_safe_action points to that checkpoint. Do not leave a later checkpoint active while an earlier checkpoint is unresolved unless the plan explicitly records the dependency and current owner.

## Artifact adoption and open items

Do not require this frontmatter or checkpoint format for an external artifact that already provides sufficient scope, boundaries, proof, and next action. If a companion plan improves recovery, recommend it; do not block execution solely because it is absent.

Label unresolved items as Acceptance blocker, Residual risk, Operational follow-up, or Future enhancement. An Acceptance blocker or an unresolved `Blocked`/`Reopened` checkpoint prevents Ready for Acceptance. Preserve non-blocking categories as explicit residual state rather than reopening planning to eliminate them.

Rolling telemetry is sample evidence, not automatically durable truth. Record the observation date or generation/window and stable assertions separately from changing counts; do not rewrite acceptance merely because a live count moved.
