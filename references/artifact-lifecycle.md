# Artifact lifecycle

Plumbline uses four artifact classes:

1. Imported source - a design, handoff, attachment, or kickoff prompt from outside the repository. Preserve provenance and hash; treat it as immutable evidence.
2. Active specification - the approved product contract for the current feature. It is tracked, authoritative during execution, and amended only for explicit product decisions.
3. Live implementation plan - the thin current-state control plane. It records checkpoint status, current ownership/dependencies, accepted proof pointers, blockers, residuals or deferrals, and the next action. Keep it current by replacing stale state as work advances.
4. Canonical documentation - long-lived project-owned docs describing the repository's actual current system. It is not a diary and is not automatically replaced by a transient plan.

These artifact classes describe responsibilities, not required filenames or formats. A user-supplied external specification, plan, handoff, or work order may be adopted in place. Select one controlling artifact set for the current task; unrelated active artifacts elsewhere in the repository are not blockers.

A repository-local shaping handoff is a pre-specification state of the active specification, not a fifth artifact class. After explicit user approval, it uses the repository's existing transient specification location, records only durable shaping decisions and concise research evidence, and is promoted in place when the specification phase begins. It is never a second active specification.

A throwaway Shape prototype is transient scratch evidence, not a fifth artifact class. Keep it clearly marked and out of production; record only its material finding in the existing handoff or specification, and never promote its code automatically.

Imported source, specs, and plans are lifecycle-owned and may be transient. They may be removed at accepted closeout only after the user explicitly accepts the result and canonical docs contain the resulting truth. Retained specifications and plans may instead become decision records when they remain useful; retention does not make them canonical current-state documentation. Git history must retain deleted artifacts. Never use closeout to hide a disagreement between code and docs; investigate it and record the resolution.

Durable state is the compact current truth a fresh agent needs to regain its
bearings and resume safely: plan status, accepted proof summary, blockers and
residuals, next action, and useful pointers to canonical docs, source paths,
functions, commits, reusable artifacts, or required audit evidence. If an
artifact does not materially improve that rehydration, it has little reason to
be durable. Keep this truth in the controlling plan or existing canonical
surface; do not create a parallel evidence ledger.

Generated execution outputs are working material by default. Builds, packages,
binaries, command logs, diagnostic captures, repeated manifests, correction
directories, and intermediate receipts live only while they help reach or
reproduce the current conclusion. Preserve a detailed or large output only when
an identifiable future consumer needs that exact object for deployment,
recovery, audit, safety, or otherwise costly reproduction. Otherwise summarize
the material result in the plan, retain a useful pointer when one exists, and
clean clearly task-owned output after acceptance or supersession. Never remove
shared or user-owned artifacts merely because Plumbline no longer needs them.

Git is the default recovery interface for material work when the repository is
Git-controlled. Anchor the starting state and each accepted checkpoint to a
main-thread commit under the plan's `required` policy, so a worker can recover
from `HEAD`, `git show`, and a focused diff instead of rereading the repository.
Do not stage unrelated dirty work, ignored setup, secrets, or generated scratch.
If Git is absent, recommend establishing it before Execute; continue without it
only after the user explicitly opts out and mark the weaker recovery boundary.

A failed result is not automatically a durable evidence attempt. Preserve an
immutable failure record only when the operation already served a real
acceptance, audit, safety, or destructive-operation boundary. A corrected run
supersedes its conclusion without erasing what happened. Ordinary diagnostics,
harness repairs, and receipt formatting remain replaceable working material and
must not mint lifecycle history merely because they failed. If a safety rollback
is required, preserve the source candidate in durable Git history before
removing it from the active source; an ignored build or transient binary is not
candidate retention.

Changing only a launcher, harness, receipt, or evidence presentation does not
invalidate an unchanged implementation candidate or reusable build. Repeat an
expensive gate only when a relevant input, candidate, contract, proof boundary,
environment, or risk/ownership boundary changed.

Every process artifact, announcement, or receipt must support recovery, validation, authorization, or ownership. Omit it when it serves none of those purposes.
