# QA audit

QA is an independent report-only check. Standard review asks whether the implementation satisfies the active spec, plan, public behavior, security expectations, verification evidence, and canonical-document impact. Deep review adds adversarial edge cases and targeted non-mutating probes.

Do not write tests, edit code, update snapshots, install dependencies, or rerun a full suite merely to duplicate closeout evidence. Keep small, low-risk, direct, documentation-only, and process reviews on the main thread; prefer a fresh `qa-auditor` when migration, security, concurrency, data, public-contract, high-risk runtime behavior, a plan requirement, or an explicit independent review justifies it. Use a fresh reviewer for each materially changed delta; reuse a reviewer only to clarify evidence for an unchanged delta. A probe must answer a named uncertainty and stop when it does.

Use the verdicts:

- `PASS` — evidence supports completeness;
- `PASS_WITH_RESIDUAL_RISK` — acceptable with named bounded uncertainty;
- `CHANGES_REQUIRED` — concrete defect or missing acceptance behavior;
- `INCONCLUSIVE` — required evidence or environment unavailable.

For planned work, create a criterion-to-diff/evidence matrix and reuse the checkpoint's compact scenario-to-proof matrix when one exists. Review only applicable rows; do not turn a mechanical change into a universal lifecycle checklist. Independent QA lenses may run in one main-mediated parallel wave against the same stable delta when their review scopes are disjoint; otherwise review serially. If a check fails, classify its origin as one of: product defect, contract gap, environment failure, test-harness failure, known unrelated baseline failure, or unavailable evidence. Do not count environment or harness retries as implementation remediation. If UAT finds a product or contract defect, identify the affected checkpoint, preserve the original evidence, record what it missed, and reopen only that checkpoint.
