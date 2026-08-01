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
ready_for_acceptance: false
---
```

For a Plumbline-managed feature, keep one controlling feature and one plan. A sufficient external plan or work order may serve that role without being rewritten into Plumbline's schema. Each checkpoint should use a compact card by default:

```markdown
## CP-01: <Meaningful outcome>
**Status:** Pending | In Progress | Blocked | Complete | Reopened | Superseded
| Boundary | <write, ownership, and risk boundary> |
| Acceptance | <proof that makes the outcome complete> |
| Evidence | <commands, artifacts, or UAT result> |
| Next action | <one safe next step> |
```

Expand the card with Outcome, Specification coverage, Dependencies, Execution topology, Shared ownership, Likely files and seams, Runtime protection, Verification, Canonical documentation impact, Completion criterion, Completion evidence, and Deviations and corrections only when a security, schema, rollback, public-contract, process-owner, irreversible, or similarly material boundary needs the detail.

The frontmatter fields current_checkpoint, checkpoint_status, lifecycle_owner, last_verified_commit, and next_safe_action are the single compact resume record. Update them together when the active checkpoint or safe next action changes; do not create a second checkpoint receipt. Checkpoints are coherent milestones, not micro-task transcripts. Blocked and Reopened stop advancement of that checkpoint; Execute may continue independent checkpoints when their dependencies permit. Update the record after a checkpoint transition, evidence invalidation or material new evidence, a verified-commit change, a next-action change, or a material correction/blocker. Reconcile the expanded body at the same meaningful boundary; do not rewrite it after every command.

The current checkpoint is the resume location, not an implicit Execute stop. Unless the user explicitly selects checkpoint-by-checkpoint mode or the plan names a user approval gate, Execute advances through the remaining serial/dependency order automatically. `Ready for Acceptance` is a final-plan state after every required checkpoint is complete, not a per-checkpoint status.

Treat checkout/worktree identity, HEAD/last_verified_commit, the plan-record hash, the applicable host configuration hash, and selected project-local role-file hashes as the resume fingerprint. For Codex, the applicable files include `.codex/config.toml` and selected role TOMLs; for Claude Code, they include selected `.claude/agents/*.md` files. Treat last_verified_commit and checkpoint completion evidence as the baseline until that fingerprint or a material contract/evidence input changes. A task resume, compaction, or conversational reminder alone does not invalidate it. At the next checkpoint, inspect the current delta and referenced paths first. Reuse unchanged evidence instead of rereading whole documents or rerunning broad checks. Reassess when the fingerprint changes, a new or failed check matters, a contract boundary changes, a defect appears, or the prior evidence may be stale.

Every plan artifact or status announcement must support recovery, validation, authorization, or ownership. Omit ceremony that serves none of those purposes.

Whenever the plan is written, verify that exactly one current checkpoint is named, its frontmatter status matches the checkpoint, and next_safe_action points to that checkpoint. Do not leave a later checkpoint active while an earlier checkpoint is unresolved unless the plan explicitly records the dependency and current owner.

## Artifact adoption and open items

Do not require this frontmatter or checkpoint format for an external artifact that already provides sufficient scope, boundaries, proof, and next action. If a companion plan improves recovery, recommend it; do not block execution solely because it is absent.

Label unresolved items as Acceptance blocker, Residual risk, Operational follow-up, or Future enhancement. Only an Acceptance blocker prevents Ready for Acceptance. Preserve the other categories as explicit residual state rather than reopening planning to eliminate them.

Rolling telemetry is sample evidence, not automatically durable truth. Record the observation date or generation/window and stable assertions separately from changing counts; do not rewrite acceptance merely because a live count moved.
