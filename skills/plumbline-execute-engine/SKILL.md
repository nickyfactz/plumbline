---
name: plumbline-execute-engine
description: Internal Plumbline engine. Use only after the Plumbline router or a Plumbline phase wrapper selects checkpoint execution.
---

# Execute engine

## Outcome and completion

Execute the approved work through every remaining checkpoint in dependency
order. A checkpoint boundary is an internal team handoff, not a user-prompt
stop. Normal Execute is full-plan mode; checkpoint-by-checkpoint mode exists
only when the user explicitly requests one checkpoint, a named pause, or
approval at each boundary.

Execute is complete only when every required checkpoint is `Complete`, the
stable delta has focused/full proof, the plan says `Ready for Acceptance`, and
the main thread has reported the remaining risk. `Blocked`, `Reopened`,
`CHANGES_REQUIRED`, `INCONCLUSIVE`, or any other failure classification is
unresolved work; it never satisfies completion. Execute does not delete
transient artifacts or publish; those belong to accepted-work Closeout.

Resolve `execution_mode` before traversal. A missing value means `continuous`.
**Checkpoint Relay:** when the plan explicitly sets `checkpoint_relay`, load
`references/checkpoint-relay.md` immediately and follow its complete branch for
adoption/readiness, controller versus checkpoint-task behavior, durability,
recovery, and acceptance. Continuous mode follows the execution loop below.

## Resume from the smallest sufficient evidence

At task start or resume, read the controlling plan's compact resume record,
external work order, or supplied execution artifact first. Use checkout/
worktree identity, HEAD or `last_verified_commit`, the artifact/plan-record
hash, and relevant local agent hashes as the resume fingerprint.

When the fingerprint is unchanged, read the compact record, Git delta, and next
action. At each checkpoint, read the exact checkpoint, its referenced contract
sections, changed files, relevant canonical documentation, and validation
commands. Read larger source/spec sections only when a referenced section or a
material trigger requires them. Resolve the Plumbline installation root once
at phase entry and use that root for all reference paths.

Reuse prior completion evidence when referenced inputs and the fingerprint are
unchanged. Reassess after a relevant source, specification, plan, config, or
agent change; a failed or newly relevant check; a contract-boundary change; a
defect; or stale-evidence concern. A new session, compaction, or conversational
resume alone does not invalidate evidence.

## Conditional artifact sufficiency preflight

Accept a user-supplied or repository-local specification, plan, work order, or
execution artifact when it defines enough scope, topology, proof, and next
action. A sufficient specification without a separate plan may receive a
companion plan recommendation, but execution can continue when the artifact
already defines the safe slice and acceptance. Missing Plumbline paths,
frontmatter, or checkpoint IDs are not blockers by themselves.

Report only adoption, a companion recommendation, competing candidates, or a
real blocker. Recommend Plan or Shape when the artifact lacks an executable
boundary or a material product decision remains unresolved.

## Traverse the full plan

This section applies to `continuous` mode. Relay traversal uses the same
checkpoint loop and evidence rules for one current checkpoint, then applies the
Relay boundary above.

After bounded work, review, focused proof, and main-thread integration complete
one checkpoint, update its resume record, select the next safe checkpoint, and
continue without waiting for a user prompt. Do not report `Ready for
Acceptance` between checkpoints. Continue independent safe checkpoints when
the topology permits, while a blocked or reopened checkpoint waits for its
resolution. A failed checkpoint attempt returns to Diagnose, then correction
of the same active candidate and checkpoint, followed by review. Do not revert
a candidate, close the objective, or select a successor merely because a
review found a defect or evidence is inconclusive.

Once an approved specification and plan are active, they are product-scope
authority for execution, but they cannot override Plumbline lifecycle
invariants. The main orchestrator resolves ordinary in-scope
ambiguity from the approved outcome, repository evidence, and a safe reversible
default, then records the decision, assumption, or residual risk. A worker's
`Shape question` label is an internal escalation; it does not itself invoke
Shape, end the goal, or pause for the user. Reopen Shape or stop only for an
explicit user gate, a destructive action outside approved authority, or a
contradiction with no safe in-scope default. When no safe default exists, block
only the affected checkpoint and continue independent work.

## Delegation-first ownership

For every approved Execute checkpoint, classify each bounded work unit before
doing it on the main thread. Delegation is the default whenever an approved
project-local role can own useful research, architecture, implementation,
review, testing, or another capability with a clear read, report, or write
boundary. Dispatch the matching role or roles before the main thread duplicates
that work. The main thread should not absorb a bounded task merely because it
can perform it.

Keep the main thread for product decisions, lifecycle and plan state, worker
joins and integration, Git, singleton build/deploy/restart/migration/publication
operations, and work too small or coupled to justify a worker. A direct action
must be already understood, trivial to verify, and have no independent
delegation boundary; record `Direct: <reason>` when using that fallback. If no
matching local role or host dispatch exists, state the capability reason and
continue directly rather than pausing the user.

**Delegation:** before any material worker wave, fresh/reuse decision,
parallel wave, corrective dispatch, or report-only assignment, load
`references/subagent-orchestration.md` and follow it completely. That reference
owns project-local role selection, model/reasoning telemetry, no-child and
read/write boundaries, context capsules, parallel readiness, worker reports,
and post-return Git inspection. Emit its compact delegated-wave line at every
dispatch.

For a Plumbline-managed plan, keep `delegation_roles` and
`delegation_status` in the active checkpoint resume record. Use
`not-applicable`, `not-dispatched`, `direct`, `dispatched`, `returned`, or
`integrating`. For an imported plan, use its existing equivalent compact state
instead of rewriting the artifact only to add these fields. On every compaction
or conversational resume, restore the delegation state before continuing. If a
bounded task has no dispatched or returned role, dispatch it before the main
thread repeats that work.

## Checkpoint execution loop

For each checkpoint:

1. Read the exact checkpoint and referenced contract sections, then inspect the
   current delta and last verified state.
2. Apply the delegation-first ownership rule above, then dispatch or perform
   the bounded work unit. For a blocker or failed validation, complete the
   minimum sufficient failure-path trace before correction. Choose the smallest
   complete solution: avoid
   speculative abstractions and dependencies while retaining required behavior,
   companion surfaces, failure/recovery paths, compatibility, and proof.
3. Run the narrowest meaningful checks and apply
   `references/runtime-value-testing.md`. A focused test, static check,
   deterministic probe, manual UAT, targeted review, or justified no-test
   decision can be valid evidence.
   Compare the result with the checkpoint's proof obligations before stopping.
   Record material durable behavior discovered during implementation as an
   additional obligation. For checks introduced or materially changed by this
   candidate, state whether they protect durable behavior, were generalized or
   consolidated, or were diagnostic-only; test count and coverage are signals,
   not completion criteria.
4. Integrate worker changes at the main thread, obtain report-only QA after a
   stable implementer delta when risk warrants it, and record material evidence
   and deviations in the controlling artifact.
5. Update exactly one current checkpoint, matching status, and
   `next_safe_action`, then select the next dependency-safe checkpoint.

Batch adjacent evidence-only, packaging, or receipt work into the parent
checkpoint when it has no independent acceptance, rollback, risk, contract, or
ownership boundary. Create a commit only at a coherent boundary when the user
or repository requires it, recovery needs it, or the checkpoint establishes a
material contract or authorization boundary.

Keep known commands and singleton operations with the main thread or named
project owner: builds, deployments, restarts, migrations, package publication,
and other actions with one authoritative side effect. Workers may recommend or
inspect those operations, but they do not duplicate them.

Batch compatible same-seam corrective fixes before repeating expensive package,
build, deployment, restart, or live-stack gates. Repeat a gate when a fix
changes the contract or ownership, invalidates prior evidence, crosses a risk
boundary, or requires immediate runtime recovery. Restore a safe runtime state
first when necessary, then resume the smallest complete verification path. Do
not batch independent symptom patches before the shared cause and fix boundary
are understood.

Before an expensive live check, run the cheapest applicable prerequisite probes
and state a bounded observation window plus an environment-appropriate
escalation condition. Stop when a prerequisite fails, the artifact is wrong, a
named stop condition occurs, or further observations add no evidence. Diagnose
instead of retrying indefinitely; never use a universal retry count.

## Classify evidence before stopping

Classify each failed or incomplete result once as a product defect, contract
gap, environment failure, test-harness failure, known unrelated baseline
failure, or unavailable evidence. A new checkpoint-invalidating product or
contract failure sets the affected checkpoint to `Reopened`. An inconclusive,
environment, or harness failure sets it to `Blocked` until Diagnose repairs
the evidence path or the main thread records why it cannot proceed. A known
unrelated baseline failure may be recorded and bypassed when it does not
affect the plan. None of these states abandons the candidate or objective.
Severity controls urgency, not terminality. A successor objective requires
accepted work or explicit user-approved defer/abandonment; a worker or plan
clause cannot authorize it.

Before advancing or saving plan state, verify exactly one current checkpoint,
matching status, and a `next_safe_action` for it. Record rolling telemetry as
timestamped sample evidence and keep stable acceptance separate from changing
counts. Use a compact state/transition line only when phase, owner, evidence,
or next action changes; unchanged resumes do not need repeated route,
doctrine, lifecycle, or checkpoint narration. If a correction produces a new
failure before the relevant contract and owner path are validated, return to
the same Diagnose boundary instead of stacking another surface patch.

## Ownership and phase boundary

Record one lifecycle owner in the active plan. Report it only when ownership
changes, a competing controller is selected, or the record is stale. An
installed skill or enabled plugin is available capability, not active
ownership. If another explicitly selected orchestration loop owns checkpoint
selection, advancement, review sequencing, or closeout, Plumbline does not
stack a second lifecycle controller.

Execute owns implementation, focused/full proof, acceptance-required canonical
documentation, dependency-aware traversal, and the stable-delta review needed
to reach `Ready for Acceptance` after the complete plan. Closeout begins only
after acceptance and owns final integration, transient cleanup, plan retirement,
worktree/branch handling, and publishing preparation. Every process artifact or
announcement must support recovery, validation, authorization, or ownership;
omit ceremony that serves none of those purposes.
