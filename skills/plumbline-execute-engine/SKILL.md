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
Continuous mode retains the full-plan behavior in this engine. An explicit
`checkpoint_relay` value selects the host-neutral stop/handoff contract in
`references/checkpoint-relay.md`: execute only the current checkpoint in this
root conversation, establish its durable handoff, and stop before downstream
work begins. Before automatic Relay, use the internal
`plumbline-plan-adoption-engine` when an otherwise sufficient source needs a
normalized companion, then require `runtime/relay-readiness.js` to report
`relay_ready: true`. Never infer Relay from plan size or silently change the
mode. Continuous execution does not require this preflight.

For automatic Relay, distinguish the controller from its fresh checkpoint
task. A checkpoint assignment containing `[PLUMBLINE_RELAY_CHECKPOINT ...]`
executes that checkpoint and never starts another controller. Otherwise, when
the installed host exposes the Codex automatic adapter, the lifecycle-owning
conversation runs `node <plugin-root>/runtime/run-relay.js --plan <plan>` once
and does not duplicate checkpoint work itself. On a host without that adapter,
execute the current checkpoint and report the manual fresh-conversation
boundary. Do not invent a background service or repository hook.

Before a Relay checkpoint stops, perform one semantic durability check: could a
fresh root conversation execute the named successor from the repository alone?
Promote only downstream-relevant decisions, corrections, assumptions,
constraints, and discovered invariants into their existing authoritative
specification, plan, or canonical documentation. Keep proof and next action in
the active plan. Do not create a generic handoff file, copy the transcript, or
record local implementation minutiae that the successor can recover from code.
If required context exists only in conversation, the checkpoint is not
complete.

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

## Main-thread delegation and parallel waves

The main thread selects, briefs, dispatches, integrates, and advances every
capability. Workers return evidence to the main thread; their recommendations
are advisory. Use only project-local roles under `.codex/agents/` or
`.claude/agents/`. Give report-only roles (researcher, architect, and QA) no
write set. Give each write-capable role only its bounded write set. Keep Git,
active-plan edits, integration, and lifecycle ownership in the main thread. Workers return
to that hub, workers never spawn children, and they do not create another
delegation hierarchy.

Load `references/subagent-orchestration.md` immediately before the first
material delegation wave. That reference owns the detailed rules for role
selection, fresh versus reused workers, parallel readiness, report shape,
runtime capsules, and read/write boundaries. Before dispatch, inspect the
relevant project-local roles and host config; reuse the result while the
checkout/worktree and those file hashes are unchanged. Recheck after a
fingerprint change or explicit request. Use `Direct: <reason>` when no
suitable local role exists or hard read-only isolation is required but
unavailable. For Codex, inspect `.codex/config.toml` as the host capability
source. Never select personal/global custom agents as fallback.

At each delegation wave, report one compact line containing every selected role,
its configured host-native model and reasoning/effort, including the configured
model slug and reasoning effort when the host exposes them, and the existing
boundary, for example:

`Delegated wave: researcher [model=<host-native-model>, reasoning=<effort>] - Boundary: report-only; no write set; no child agents`

Include effective model, reasoning/effort, or effective sandbox/permission only
when the host exposes a meaningful difference or the user asks. Codex
`agents.max_depth = 1` is a recommended starting value, not a Plumbline limit;
Claude expresses the same recommended boundary by omitting the `Agent` tool.
Inspect Git status and diff after every worker returns and classify unexpected
edits before integrating them. A main-mediated parallel wave still requires the
contract is stable, scopes are disjoint, no result dependency, and a clear
main-thread join condition;
shared interfaces, schemas, migrations, generated artifacts, and moving review
deltas remain serial. Fresh workers are the default; reuse requires continuity
to be valuable for the same outcome, contract, write set, and acceptance.

## Delegation-first ownership

For every approved Execute checkpoint, classify each bounded work unit before
doing it on the main thread. Delegation is the default whenever an approved
project-local role can own useful research, architecture, implementation,
review, testing, or another capability with a clear read, report, or write
boundary. Dispatch the matching role or roles before the main thread duplicates
that work. Use the role definitions selected for this repository and preserve
their configured model, reasoning/effort, and sandbox/permission intent; do not
invent or substitute personal/global roles. The main thread should not absorb a
bounded task merely because it can perform it.

Keep the main thread for product decisions, lifecycle and plan state, worker
joins and integration, Git, singleton build/deploy/restart/migration/publication
operations, and work too small or coupled to justify a worker. A direct action
must be already understood, trivial to verify, and have no independent
delegation boundary; record `Direct: <reason>` when using that fallback. If no
matching local role or host dispatch exists, state the capability reason and
continue directly rather than pausing the user.

For a Plumbline-managed plan, keep `delegation_roles` and
`delegation_status` in the active checkpoint resume record. Use
`not-applicable`, `not-dispatched`, `direct`, `dispatched`, `returned`, or
`integrating`. For an imported plan, use its existing equivalent compact state
instead of rewriting the artifact only to add these fields. On every compaction
or conversational resume, restore the delegation state before continuing. If a
bounded task has no dispatched or returned role, dispatch it before the main
thread repeats that work.

## Dispatch the contract, not the whole history

Before a material role dispatch, synthesize the transient contract capsule
defined by `references/subagent-orchestration.md` from the exact checkpoint and
specification sections. Put it in the prompt, not in a new file. The capsule
names the observable outcome, owners/invariants, partial-failure boundary,
applicable edge behavior, proof, boundary, non-goals, and assumptions. Add a
bounded write set for a writing role and a report-only boundary for a reporting
role. The worker chooses mechanics or analysis within that envelope and uses
repository conventions plus a safe reversible default. Return a contract gap
only when the missing choice changes observable behavior or contradicts the
approved plan.

For a corrective dispatch caused by a blocker, regression, repeated failure,
or failed expensive gate, include the minimum sufficient root-cause capsule:
symptom and reproduction, relevant failure path, contract or invariant,
broken owner, fix boundary, proof, and exclusions. Do not dispatch a patch for
the reported error line alone when the path is still unknown. A safety
containment may be dispatched as provisional work, but it does not satisfy
checkpoint acceptance until Diagnose establishes the cause.

Give every worker the checkpoint outcome, acceptance criteria, anchored read
set, disjoint write set, relevant paths, expected validation, report format,
and the report-only/no-write-set/no-child boundaries from the orchestration
reference.
Pass only the anchored context needed for the current task. Reports name
changed files, behavior, checks, failures, residual risk, and follow-up without
large successful logs. For material state, persistence, concurrency, security,
public contracts, or cross-boundary ownership, carry the applicable
scenario-to-proof matrix into the plan and worker briefs; omit it for
mechanical or low-risk work. A construction-policy skill may constrain
implementation choices, but it does not become a lifecycle controller, add
checkpoints, or weaken acceptance.

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
