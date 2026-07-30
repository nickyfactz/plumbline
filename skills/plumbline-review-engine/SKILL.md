---
name: plumbline-review-engine
description: Internal Plumbline engine. Use only after the Plumbline router or a Plumbline phase wrapper selects independent review.
---

# Review engine

Report only. Choose `standard` for the normal completion audit or `deep` when the user requests stronger adversarial scrutiny. Read the active specification and plan, the requested fixed point or current diff, repository standards, canonical docs, and validation evidence. For small, low-risk, direct, documentation-only, or process questions, perform the standard audit on the main thread without dispatching QA merely for ceremony. Dispatch a fresh report-only `qa-auditor` for migrations, security, concurrency, data, public contracts, high-risk runtime behavior, a plan-required review, or an explicit independent-review request. When dispatching, emit one line such as `Delegated wave: qa-auditor [model=<slug>, reasoning=<effort>] — Boundary: report-only; no write set; no child agents`; include effective values only when the host exposes them. Its `sandbox_mode = "read-only"` is intent; a writable parent is normal and may affect the effective sandbox. Record configured/effective values when observable, inspect the diff after the child returns, and never claim hard isolation from the TOML alone. A worker that authored the patch cannot count as its independent reviewer. Never select a personal/global QA agent or another global fallback. If the local role is absent, state `Direct: qa-auditor unavailable` and perform the report on the main thread. If hard read-only isolation is required but unavailable, state `Direct: delegation prohibited or effective read-only isolation unavailable` and perform the report directly. Workers never spawn children.

Treat minimality as subordinate to completeness: a smaller diff is not a pass if it omits required behavior, companion surfaces, failure/recovery paths, compatibility, or meaningful proof. Check behavior, security, failure/recovery, acceptance-criterion coverage, valuable regression protection, and documentation truth. Use a specification-to-diff matrix for planned features. Review at public seams, not private implementation details. A targeted non-mutating probe is allowed only to settle a material uncertainty; do not write tests, edit code, update snapshots, install dependencies, or duplicate the whole closeout suite.

Return one evidence-bound verdict:

- `PASS` — no material gap found;
- `PASS_WITH_RESIDUAL_RISK` — acceptable with a named, bounded uncertainty;
- `CHANGES_REQUIRED` — a concrete defect or missing requirement blocks acceptance;
- `INCONCLUSIVE` — required evidence or environment is unavailable.

Quote paths, commands, and observed results. Do not manufacture style findings. If QA or UAT finds a defect in planned work, identify the affected checkpoint and the evidence that prior validation missed; the execution flow must reopen it.
