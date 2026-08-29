# Subagent orchestration

Load this reference only when a delegation wave is materially useful. Execute keeps the dispatch invariant in its phase body and does not load this detailed doctrine for direct work.

## Lifecycle ownership

Record one owner in the active plan and report it only when ownership changes, a competing controller is selected, or the record is stale. Installed or enabled skills alone are not active ownership. One system owns checkpoint selection, plan advancement, review sequencing, and closeout for a task. If another explicitly selected orchestration loop already owns those responsibilities, do not stack a second lifecycle controller; use Plumbline only for the selected phase contract. When Plumbline owns the lifecycle, supporting skills may contribute bounded research, implementation, or review work but may not advance the plan or closeout independently.

## Thin orchestrator

The main thread reads only enough to identify the controlling artifact, current
state, delegation boundaries, and join condition. Delegate before broad grep,
repository archaeology, multi-file fact gathering, external research, or a
cross-seam review when a matching project-local role can return a bounded answer.
Do not make the main thread reproduce a worker's exploration after it returns;
inspect only the exact facts needed for product judgment, integration, safety,
or resolving a contradiction.

Keep a task direct when the target and answer are already known, the read is a
small coupled part of a main-owned integration or Git action, or dispatch would
cost more context than the work. Main-thread capability is not itself a reason
to stay direct.

## Selection and depth

Use only a matching project-local definition under `.codex/agents/` for Codex or `.claude/agents/` for Claude Code. Check `.codex/config.toml` for Codex capability settings; Claude project agents do not require a Plumbline project config. Global config may explain host capability or provide a model candidate, but personal/global agent files are never selected or used as fallback. If useful bounded work has no local role, keep it on the main thread and report `Direct: <reason>` once. At a delegation wave, state the selected role names, host-native model and reasoning/effort values, and short assignments in one compact line.

Worker leaf behavior is a Plumbline orchestration boundary, not a Codex depth-setting requirement. Claude roles express the same boundary by omitting the `Agent` tool. The main thread may create direct workers; workers must never create children, delegate further, or form a second agent hierarchy.

Delegation is hub-and-spoke: every worker returns evidence to the main thread. A worker recommendation is advisory; only the main thread selects the next capability, builds the next brief, and dispatches it. Workers never invoke, hand off to, or dispatch another worker. This rule does not require visible `main -> worker -> main` telemetry or a graph artifact.

## Worker lifetime

Treat an in-flight worker as active until the host reports a terminal result.
Do not kill, abandon, or duplicate it because of elapsed time, silence,
compaction, or an intermediate status. An observer or polling timeout means
`status unknown`: reconcile the host-native task state before deciding what to
do. Continue independent work while a worker remains active. Replace a worker
only after a confirmed API, transport, host-reported timeout, or other
terminal failure, an explicit user stop, obsolete work, or a safety/scope
violation. Preserve any recoverable result and do not restart the same work
merely to make progress appear faster. This is host-neutral guidance; a host's
own hard lifecycle limit remains a host boundary, not a reason to duplicate
work before its state is reconciled.

## Profile refresh and worktree drift

Treat project-local role files and applicable host config as live dispatch
inputs. Before each delegation wave, reread the selected files. If a profile
hash changed, use its current model, reasoning/effort, sandbox/permission, and
instruction values for new workers, update the compact resume fingerprint, and
keep prior evidence unless a material input changed. Workers already running
retain the profile used when they were created; a changed hash is a profile
refresh, not role loss or evidence invalidation.

If a selected role is missing in the active worktree, inspect the source
checkout and its `.worktreeinclude` propagation before falling back to
`Direct: <reason>`. Refresh only the ignored project-local config and role
files from that source checkout, then reread them. This is an explicit
on-demand refresh for an existing worktree, not a new worktree system;
never copy secrets, dependencies, source trees, or personal/global roles.

## Capability versus assignment

A role has two separate boundaries:

- Assignment: researcher, architect, code-reviewer, and QA roles are report-only and receive no write set. A brief asking them to edit source, tests, scripts, documentation, or Git state is invalid and returns to the main thread. Implementers use the bundled `maintainable-code` skill while writing; `code-reviewer` uses its review branch before QA.
- Capability: Codex `sandbox_mode = read-only` and Claude `permissionMode: plan` are role intent. The parent goal may remain writable or permissive, and the host can apply that live state to the child. Do not claim hard read-only isolation from the role file alone.

At each delegation wave, emit one compact line such as `Delegated: researcher
[model=<slug>, reasoning=<effort>] — map the persistence owner`. Include every
selected role, its configured model/reasoning or effort, and a short assignment.
Mention report-only, write-set, permission, or no-child boundaries only when an
exception, effective mismatch, or user question makes them material. Do not add
separate starting, waiting, returned, or unchanged-configuration narration;
integrate the worker's result into the next substantive update. After a child
returns, inspect Git status and the diff; report only an unexpected edit or
material result. Use `Direct: delegation prohibited or effective read-only
isolation unavailable` when a hard isolation requirement cannot be met.

## Code quality and acceptance review

For material implementation code, dispatch a fresh report-only `code-reviewer`
before `qa-auditor`. The code-reviewer invokes `maintainable-code` and reports
concrete maintainability, design, human-legibility, safe-change, and material
performance findings. QA then checks acceptance behavior, proof coverage, and
documentation alignment against the approved contract. A code-reviewer finding
returns to the implementer before QA; a missing role is a main-thread fallback.

## Delegation-first ownership

For an approved Execute checkpoint, delegation is the default whenever an
approved project-local role can own useful research, architecture,
implementation, review, testing, or another capability with a clear read,
report, or write boundary. Dispatch the matching role or roles before the main
thread duplicates that work. Preserve each selected role's configured model,
reasoning/effort, and sandbox/permission intent; do not invent or substitute a
personal/global role. This supports one bounded worker or a dependency-safe
parallel wave without a fixed role map.

Keep the main thread for product decisions, lifecycle and plan state, worker
joins and integration, Git, singleton operations, and work too small or coupled
to justify a worker. A direct action must be already understood, trivial to
verify, and have no independent delegation boundary. Emit `Direct: <reason>`
only when a useful bounded unit looked delegable but no matching local role or
host dispatch exists; tiny or inherently main-owned actions need no narration.
Continue directly rather than pausing the user.

For a Plumbline-managed plan, persist `delegation_roles` and
`delegation_status` in the active checkpoint resume record. Use
`not-applicable`, `not-dispatched`, `direct`, `dispatched`, `returned`, or
`integrating`. For an imported plan, use its existing equivalent compact state
instead of rewriting the artifact only to add these fields. Restore the state
after compaction or conversational resume before continuing; a bounded task
without a dispatched or returned role must be delegated before the main thread
repeats it.

When a brief permits adding or materially changing a test, probe, snapshot, or
validation check, require the worker report to name the proof obligation it
supports and identify diagnostic evidence that should not survive the
checkpoint. The main thread owns the final disposition.

## Worker briefs

Treat each independent assignment as a fresh worker context by default. Reuse a
worker only when continuity materially benefits the same active slice with the
same outcome, contract, write set, and acceptance condition. A changed
objective, seam, contract, write set, acceptance condition, or materially new
failure requires a fresh context; previous worker conclusions are context, not
evidence. The main thread makes this reuse decision explicitly without adding
user-facing ceremony. A completed worker is retired for default dispatch and
must not be awakened for unrelated follow-up work.

When continuity is genuinely useful, begin the reused-worker brief with a
reset capsule: current assignment, current commit or artifact, exact failure or
question, write set, acceptance condition, and exclusions. Tell the worker to
inspect the current repository and treat its prior conclusions as untrusted.
Keep this policy host-neutral; do not encode a provider-specific follow-up,
fork, or worker-retirement API.

When a Codex dispatch surface exposes `fork_turns`, pass `fork_turns="none"`
for a fresh independent worker. This is a per-dispatch context choice, not a
project config or agent-file setting: the worker still receives its role,
project guidance, bounded brief, and checkout. Use inherited turns only when
continuity is intentionally valuable, and fall back to the fresh-worker brief
when the host does not expose this parameter. Do not claim that the setting was
applied unless the dispatch surface exposes or confirms it.

For live or recovery work, add an optional transient runtime-state capsule to
fresh or reused worker briefs: verified commit or deployed artifact, active
symptom, last known-good observation, exact write set, acceptance condition,
and exclusions. Omit it for non-runtime work and refresh it only after a
material code, artifact, deployment, restart, or failure-state change.

Give each worker a context-bounded brief containing:

- the checkpoint outcome and acceptance criteria;
- the exact read set, anchored sections, and disjoint write set;
- relevant contract and repository paths;
- the current diff or last verified commit only when relevant;
- expected validation and report format;
- explicit limits: no Git operations, no active-plan edits, no unrelated cleanup.

Ask read-heavy workers for a decision packet, not an exploration transcript:
the answer or recommendation, exact paths/symbols/URLs needed to verify it,
material constraints, residual uncertainty, and the suggested next bounded
action. Omit search narration, large excerpts, exhaustive file inventories, and
successful command logs. The main thread passes only the relevant packet fields
into downstream briefs; workers still return to the main thread and never
delegate further.

For an implementer dispatch involving material behavior, include a compact contract capsule derived from the anchored specification and plan sections: the observable outcome, invariants and owners, operation or partial-failure boundary, applicable edge behavior, proof, bounded write set, non-goals, and recorded assumptions. This is prompt content only; do not create a new handoff artifact. The capsule is a design envelope, not an implementation recipe: the implementer chooses mechanics inside it, resolves ordinary technical ambiguity with existing conventions and a safe reversible default, and does not invent observable product behavior or ask the user to choose implementation details. Return a contract gap to the main thread only when the missing choice would change observable behavior or contradict the approved plan.

For a corrective dispatch caused by a blocker, regression, repeated failure, or failed expensive gate, add a minimum sufficient root-cause capsule to that brief: exact symptom and reproduction, relevant caller-to-callee or state-owner path, violated contract or invariant, root cause or explicit evidence gap, fix boundary, proof, and exclusions. The implementer may contain an immediate safety risk, but a patch that only suppresses the reported error is not a complete correction. The main thread widens the trace only when the evidence points to another shared caller, contract, or state transition.

Do not pass full conversation history or ask workers to reread entire instruction, plan, or documentation trees when the brief and unchanged artifacts already answer the question. Begin with the active plan's compact current-state capsule, exact checkpoint, anchored contract sections, and prior evidence pointers. Treat legacy attempt chronology as stale context: omit it from briefs and have the main thread compact it out at the next meaningful plan update. A worker may widen its read set only when it identifies a concrete missing fact and reports why. Keep normal reasoning at the configured medium level; reserve high effort for a named ABI, security, persistence, concurrency, ownership, or other material risk. Never let dispatch overwrite a user's project-local role values; rereading a manual profile edit is not an installer retune.

For a checkpoint involving material state, persistence, concurrency, security, a public contract, or cross-language ownership transfer, give the applicable architect a compact risk-contract brief before implementation. Ask for only the relevant identities and ownership, state transitions and terminal precedence, failure/recovery/cancellation or shutdown behavior, compatibility constraints, proof seams, and unresolved assumptions. Require the report to end with `Contract status: complete`, `safe assumption recorded`, or `product decision required`, followed by applicable scenario/proof rows and assumptions. The architect owns technical design; do not ask the user to choose implementation mechanisms. This is a conditional completeness check, not a universal checklist; do not dispatch an architect merely to fill it for mechanical or low-risk work.

If the architect cannot resolve an uncertainty without choosing a material product behavior, return a structured escalation to the main orchestrator. Include the affected checkpoint, overall objective, plain-language product question, why the answer changes observable behavior or acceptance, recommendation, realistic alternatives, tradeoff, default, whether the checkpoint is blocked, and safe independent work. The child does not ask the user directly, end the active goal, start a competing lifecycle, or turn a checkpoint question into a global stop. During Execute, this is an internal report: the main orchestrator uses the approved specification and plan, repository evidence, and a safe reversible default to resolve ordinary in-scope ambiguity and records the result. It does not invoke Shape or pause for the user unless an explicit user gate, destructive action, or contradiction with no safe default applies. Independent checkpoints continue when their dependencies permit.

For material risk, carry one compact scenario-to-proof matrix from the architect brief into the plan and downstream worker briefs. Add only applicable scenarios and omit the matrix for mechanical or otherwise low-risk work; it is not a universal checklist or a new artifact.

Run independent work packages in parallel only after shared contracts are stable and the main thread can name disjoint scopes, no result dependency, and a clear join condition. This applies equally to independent research, architecture lenses, QA lenses, and disjoint implementation checkpoints. Keep work serial when it shares files, public interfaces, schemas, migrations, generated artifacts, unstable contracts, or a moving review delta. The main thread classifies and integrates every result before dispatching downstream work; a worker recommendation never creates a new delegation wave.

Do not let parallel workers concurrently build, deploy, restart, or mutate a
shared or singleton runtime. The main thread or a named project owner performs
that operation; workers may inspect the result or run disjoint checks. Reuse
the resulting artifact and classify the operation's evidence at the main-thread
join.

Worker reports should name changed files, behavior, checks run, failures, residual risk, and follow-up without pasting large successful command logs. The main thread inspects and integrates the result, updates the plan, runs checkpoint verification, and summarizes evidence as command, outcome, counts or failure tail, and artifact path where applicable. Do not let agents create recursive agent organizations or write commits behind the main thread.

Workers treat compiled outputs, diagnostic captures, repeated manifests,
correction directories, and receipt variants as working scratch. Return the
current conclusion and a useful existing pointer; do not create a durable
evidence bundle unless the brief names its future deployment, recovery, audit,
safety, or costly-reproduction consumer. The main thread decides retention and
reuses an unchanged candidate across evidence-tooling corrections.

Review only after the implementer's bounded write set is integrated and the diff is stable. For a high-risk checkpoint, perform that first stable-delta review before the main thread makes material semantic repairs; return substantial corrections to the implementer or reopen the checkpoint instead of silently absorbing them. For corrective work, a green symptom check is insufficient when the failure is non-local or repeated: verify the reported failure path, contract or owner boundary, and one focused adjacent proof. Classify a newly discovered issue as an implementation defect, contract gap, or environment/harness failure; a contract or ownership change reopens planning, while a small bounded defect may remain in Execute. Batch related evidence-only or packaging work into the parent checkpoint when it has no independent acceptance, rollback, risk, contract, or ownership boundary. Every process artifact, announcement, or receipt must support recovery, validation, authorization, or ownership; omit it otherwise.
