---
name: plumbline-review-engine
description: Internal Plumbline engine. Use only after the Plumbline router or a Plumbline phase wrapper selects independent review.
---

# Review engine

## Outcome and completion

Produce one evidence-bound, report-only assessment of the requested stable
delta. Complete Review with a verdict, findings tied to paths and evidence,
acceptance coverage, residual risk, and any affected checkpoint. Review leaves
the repository unchanged.

## Select the review depth

Choose `standard` for the normal completion audit or `deep` when the user asks
for stronger adversarial scrutiny. Read the active specification and plan, the
requested fixed point or current diff, repository standards, canonical docs, and
validation evidence. Review at public seams and use a specification-to-diff
matrix for planned features.

Keep small, low-risk, direct, documentation-only, and process reviews on the
main thread. For material implementation code, dispatch a fresh report-only
`code-reviewer` first and wait for its stable-delta quality verdict before
dispatching `qa-auditor`. The code reviewer invokes the bundled
`maintainable-code` skill and owns maintainability, design,
human-legibility, and safe-change scrutiny; `qa-auditor` owns acceptance,
behavior/proof, and documentation alignment. Dispatch a fresh report-only
`qa-auditor` for acceptance of migrations, security, concurrency, data, public
contracts, high-risk runtime behavior, a plan-required review, or an explicit
independent-review request. Use the existing one-line `Delegated:` report with
role, host-native model, reasoning/effort, and the short review assignment.
Mention the standard report-only/no-write-set/no-child boundary only for an
exception or mismatch. These two reviews are serial when QA depends on the
reviewed code delta; independent QA lenses may share one parallel wave only
against one stable delta with disjoint scopes and a clear join condition.

Use project-local roles only. If `code-reviewer` is absent, report
`Direct: code-reviewer unavailable` and keep its quality review on the main
thread; if `qa-auditor` is absent, report `Direct: qa-auditor unavailable` and
keep acceptance review on the main thread. If hard read-only isolation is required but unavailable, report
`Direct: delegation prohibited or effective read-only isolation unavailable`.
Codex `sandbox_mode = "read-only"` and Claude `permissionMode: plan` express
intent; inspect the effective sandbox and result rather than claiming isolation
from the role file.
The author of a patch is not its independent reviewer. Workers return findings
to the main thread, workers never spawn children, and they do not invoke or
dispatch another worker. Personal/global QA agents are not fallback reviewers.

For a high-risk or expensive stable delta, inspect the assigned boundary as a
whole and return material same-boundary findings together before correction.
Keep the focused adjacent-proof rule for ordinary proportional reviews; this is
not an exhaustive repository audit.

## Check completeness and risk

For candidate-introduced or materially changed tests, probes, or snapshots, map
each to a proof obligation, distinguish behavior from implementation-shape
assertions, and flag diagnostic-only or redundant evidence for disposition. Do
not use test count or coverage as acceptance gates.

Treat minimality as a constraint inside completeness: a small diff passes only
when it covers required behavior, companion surfaces, failure/recovery paths,
compatibility, and meaningful proof. Check behavior, security,
failure/recovery, acceptance coverage, valuable regression protection, and
documentation truth. Use a targeted non-mutating probe only to settle a named
material uncertainty. Keep tests, snapshots, dependencies, and closeout
changes outside a report-only review.

Return one verdict:

- `PASS` — no material gap found;
- `PASS_WITH_RESIDUAL_RISK` — acceptable with a named, bounded uncertainty;
- `CHANGES_REQUIRED` — a concrete defect or missing requirement blocks acceptance;
- `INCONCLUSIVE` — required evidence or environment is unavailable.

Quote paths, commands, and observed results. Do not manufacture style findings. If QA or UAT finds a defect in planned work, identify the affected checkpoint and the evidence that prior validation missed; the execution flow must reopen it.

`CHANGES_REQUIRED` reopens the affected checkpoint and `INCONCLUSIVE` blocks
it for Diagnose. For corrective work, a green symptom check is insufficient
when the failure is non-local or repeated: verify the reported failure path,
contract or owner boundary, and one focused adjacent proof. Finding severity,
including P0 or P1, controls urgency but does not decide candidate terminality.
Review may block acceptance; it cannot abandon the objective, authorize a
safety rollback without durable retention, or select a successor.
