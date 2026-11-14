# QA audit

For each test, probe, snapshot, or validation check added or materially changed
by the candidate, map it to a proof obligation and ask whether it proves
behavior at the right seam or only implementation shape. Recommend retain for
durable protection, generalize or consolidate, remove as diagnostic-only, or
retain with named residual risk. Recommend removal only when another evidence
path preserves confidence. Treat test growth without progress against the
original obligations as a reassessment signal, not a failure. QA recommends the
disposition; the main thread decides deletion.

QA is the acceptance-side independent report-only check and follows the
`code-reviewer` on material implementation deltas. It asks whether the
implementation satisfies the active spec and plan, whether observable behavior
and proof cover the success criteria, whether documentation matches the intended
design, and whether material product, public-contract, security, or failure-path
gaps remain. Code cleanliness, maintainability, and design-shape findings belong
to `code-reviewer`; QA does not duplicate that review or invent style findings.
Review findings are evidence, not automatic work orders. The main orchestrator
uses the accepted specification, current milestone, affected supported behavior,
and remaining implementation plan to decide relevance and timing, including for
material quality findings. A legitimate finding need not block forward progress;
a severity label or reviewer verdict alone does not establish a delivery gate.
Before assigning remediation, choose the appropriate disposition:

- Fix now: prevents the current milestone or necessary integration from working,
  materially regresses affected supported behavior, violates an applicable
  accepted requirement, or creates a concrete unacceptable security or
  data-integrity risk.
- Required in a later planned milestone: keep the accepted requirement in that
  milestone; it is unfinished required work, not an optional residual. This is
  valid only while current acceptance and dependency boundaries remain satisfied.
- Defer as an optional residual: legitimate but non-blocking robustness or design
  work, especially where planned downstream changes will replace or reshape it.
- Dismiss: unsupported, irrelevant, duplicated, or obsolete concerns.

Use the existing plan/open-items surface, not a new finding tracker. For each
residual, record the concern/pointer, why it does not block now, and a concrete
revisit trigger. Reassess relevance at that trigger; residuals are not the next
work queue or a mandatory cleanup phase. Advance when applicable acceptance and
required checks are satisfied; an empty residual list is not required. The
orchestrator cannot waive accepted requirements or call unverified behavior
complete. No findings is a valid review outcome.
Deep QA adds adversarial acceptance edge cases and targeted non-mutating probes.

For high-risk or expensive reviews, inspect the stable assigned delta as a whole
and batch material findings from the same boundary before another correction
cycle. The orchestrator consolidates necessary repairs into coherent work, then
scopes follow-up review to those repairs and affected behavior. Widen review for
materially new evidence, not merely because another correction landed. Reviewers
report new evidence to the orchestrator rather than expanding remediation scope
or reopening deferred findings independently. Keep ordinary reviews proportional;
this does not require an exhaustive repository audit.

Do not write tests, edit code, update snapshots, install dependencies, or rerun a full suite merely to duplicate closeout evidence. Keep small, low-risk, direct, documentation-only, and process reviews on the main thread; prefer a fresh `qa-auditor` when migration, security, concurrency, data, public-contract, high-risk runtime behavior, a plan requirement, or an explicit independent review justifies it. Run the full review once per checkpoint stable delta. A correction to that delta gets a focused check of the corrected findings and affected behavior, not a fresh full review, unless the correction changes the design, a contract, or ownership. Reuse a reviewer only to clarify evidence for an unchanged delta. A probe must answer a named uncertainty and stop when it does.

Use the verdicts:

- `PASS` — evidence supports completeness;
- `PASS_WITH_RESIDUAL_RISK` — acceptable with named bounded uncertainty;
- `CHANGES_REQUIRED` — concrete defect or missing acceptance behavior;
- `INCONCLUSIVE` — required evidence or environment unavailable.

For planned work, map applicable acceptance criteria to diff/evidence in the existing checkpoint surface; reuse its compact scenario-to-proof matrix when one exists rather than creating a second matrix or evidence artifact. Independent QA lenses may run in one main-mediated parallel wave against the same stable delta when their review scopes are disjoint; otherwise review serially. If a check fails, classify its origin as one of: product defect, contract gap, environment failure, test-harness failure, known unrelated baseline failure, or unavailable evidence. Do not count environment or harness retries as implementation remediation. If UAT finds a product or contract defect, identify the affected checkpoint, keep a pointer to the evidence that shows it, and record in one line what prior validation missed.

When the behavior under review depends on a model or another non-deterministic external system, QA checks what was delivered to that system and how its output was handled. QA does not grade output quality unless the specification sets an explicit threshold and sample size for it, and then only at the final checkpoint that owns that target. A poor answer from correctly delivered input is a quality residual, not a `CHANGES_REQUIRED` finding. The orchestrator applies the disposition above and reopens only a checkpoint whose acceptance is invalidated.
