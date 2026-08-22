---
name: plumbline-closeout-engine
description: Internal Plumbline engine. Use only after the Plumbline router or a Plumbline phase wrapper selects accepted-work closeout.
---

# Closeout engine

## Outcome and completion

Run Closeout after the user accepts the work or asks to integrate/clean up after
a ready-for-acceptance audit. Complete it when accepted work has the required
canonical documentation, transient cleanup decision, integration result, and
final branch/worktree/publishing preparation report. Closeout does not redo
first-time implementation proof.

Normal Closeout refuses to retire an objective with any required checkpoint in
`Blocked`, `Reopened`, `CHANGES_REQUIRED`, `INCONCLUSIVE`, or another unresolved
state. Preserve the failed attempt and return the work to Execute/Diagnose.
Only explicit user approval may defer or abandon the objective; do not infer
that decision from severity, rollback, or a proposed successor.

Execute owns implementation, focused/full proof, acceptance-required canonical
documentation, and stable-delta review until `Ready for Acceptance`. Closeout
then owns integration, transient cleanup, plan retirement, worktree/branch
handling, and publishing preparation.

## Acceptance-led preflight and open items

Identify the work from an external work order, specification, plan,
implementation, or explicit acceptance. An active Plumbline specification or
plan is helpful but not required for closeout; this flow does not require an active
Plumbline specification or plan. Report only a missing acceptance
signal, competing artifact set, or destructive cleanup decision that actually
blocks the requested operation.

Classify remaining items as Acceptance blocker, Residual risk, Operational
follow-up, or Future enhancement. An Acceptance blocker or any unresolved
`Blocked`/`Reopened` checkpoint prevents closeout; keep non-blocking categories
visible without starting a new planning cycle.

## Choose the smallest closeout mode that is sufficient

- Light closeout for bounded direct work, documentation/process changes, or already-documented work with no transient specification/plan cleanup. Read the current status/diff, focused validation, acceptance signal, documentation impact, and residual risk.
- Full closeout for work with an active specification or plan, migrations, security/privacy, compatibility, material runtime behavior, canonical documentation reconciliation, or transient artifact cleanup. Read the specification, plan, QA verdict, UAT evidence, Git history, current status, and repository documentation routing; prepare the coverage matrix when a specification-to-diff mapping is needed.

Keep required UAT and canonical-document checks in either mode. Read exact
sections identified by the selected mode and current artifacts; reuse unchanged
evidence instead of rereading unrelated large documents.

For tests, probes, or snapshots introduced or materially changed by the
candidate, carry a final disposition: retain durable protection, generalize or
consolidate, remove diagnostic-only evidence, or retain with named residual
risk. This is candidate-scoped; do not perform a repository-wide test cleanup.

Prepare a concise product-level UAT surface and hand off to Local when
validation is singleton, hardware-bound, exceptionally heavy, or cheaper
there. Reconcile canonical current-state documentation; investigate code/doc
disagreement instead of blindly overwriting either side. A justified no-change
result is valid.

Before deletion, produce the specification-to-diff coverage matrix, final
verification evidence, remaining risks, and exact transient paths. Delete
imported source, active specification, or live plan only after explicit user
acceptance. Preserve useful canonical docs, agents, tests, and Git history.
Integrate through the user's requested local flow. GitHub issues/PRs, history
rewrites, and custom worktree cleanup are outside Plumbline v1.
