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
However, material quality findings remain part of acceptance: unclear ownership,
behavior-obscuring code, unsafe structure, excessive change amplification, or
meaningful future risk can require changes. Subjective polish, fringe unproven
edge cases, and non-material defensive additions are named residuals and must
not reopen an otherwise complete MVP. For each residual, report a concise
pointer, why it is non-blocking now, the relevant risk, and a revisit trigger.
Deep QA adds adversarial acceptance edge cases and targeted non-mutating probes.

For high-risk or expensive reviews, inspect the stable assigned delta as a whole
and batch material findings from the same boundary before another correction
cycle. Keep ordinary reviews proportional; this does not require an exhaustive
repository audit.

Do not write tests, edit code, update snapshots, install dependencies, or rerun a full suite merely to duplicate closeout evidence. Keep small, low-risk, direct, documentation-only, and process reviews on the main thread; prefer a fresh `qa-auditor` when migration, security, concurrency, data, public-contract, high-risk runtime behavior, a plan requirement, or an explicit independent review justifies it. Use a fresh reviewer for each materially changed delta; reuse a reviewer only to clarify evidence for an unchanged delta. A probe must answer a named uncertainty and stop when it does.

Use the verdicts:

- `PASS` — evidence supports completeness;
- `PASS_WITH_RESIDUAL_RISK` — acceptable with named bounded uncertainty;
- `CHANGES_REQUIRED` — concrete defect or missing acceptance behavior;
- `INCONCLUSIVE` — required evidence or environment unavailable.

For planned work, create a criterion-to-diff/evidence matrix and reuse the checkpoint's compact scenario-to-proof matrix when one exists. Review only applicable rows; do not turn a mechanical change into a universal lifecycle checklist. Independent QA lenses may run in one main-mediated parallel wave against the same stable delta when their review scopes are disjoint; otherwise review serially. If a check fails, classify its origin as one of: product defect, contract gap, environment failure, test-harness failure, known unrelated baseline failure, or unavailable evidence. Do not count environment or harness retries as implementation remediation. If UAT finds a product or contract defect, identify the affected checkpoint, preserve the original evidence, record what it missed, and reopen only that checkpoint.
