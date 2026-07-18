# QA audit

QA is an independent report-only check. Standard review asks whether the implementation satisfies the active spec, plan, public behavior, security expectations, verification evidence, and canonical-document impact. Deep review adds adversarial edge cases and targeted non-mutating probes.

Do not write tests, edit code, update snapshots, install dependencies, or rerun a full suite merely to duplicate closeout evidence. Keep small, low-risk, direct, documentation-only, and process reviews on the main thread; prefer a fresh `qa-auditor` when migration, security, concurrency, data, public-contract, high-risk runtime behavior, a plan requirement, or an explicit independent review justifies it. A probe must answer a named uncertainty and stop when it does.

Use the verdicts:

- `PASS` — evidence supports completeness;
- `PASS_WITH_RESIDUAL_RISK` — acceptable with named bounded uncertainty;
- `CHANGES_REQUIRED` — concrete defect or missing acceptance behavior;
- `INCONCLUSIVE` — required evidence or environment unavailable.

For planned work, create a criterion-to-diff/evidence matrix. If UAT finds a defect, identify the affected checkpoint, preserve the original evidence, record what it missed, and reopen only that checkpoint.
