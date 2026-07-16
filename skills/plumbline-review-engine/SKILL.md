---
name: plumbline-review-engine
description: Internal Plumbline engine. Use only after the Plumbline router or a Plumbline phase wrapper selects independent review.
---

# Review engine

Report only. Choose `standard` for the normal completion audit or `deep` when the user requests stronger adversarial scrutiny. Read the active specification and plan, the requested fixed point or current diff, repository standards, canonical docs, and validation evidence. If project-local `.codex/agents/qa-auditor.toml` is present and the project config is valid, dispatch a fresh read-only `qa-auditor` with a bounded brief and state `Delegated: qa-auditor`. Never select a personal/global QA agent or another global fallback. If the local role is absent, state `Direct: qa-auditor unavailable` and perform the report on the main thread. Workers never spawn children.

Check behavior, security, failure/recovery, acceptance-criterion coverage, valuable regression protection, and documentation truth. Use a specification-to-diff matrix for planned features. Review at public seams, not private implementation details. A targeted non-mutating probe is allowed only to settle a material uncertainty; do not write tests, edit code, update snapshots, install dependencies, or duplicate the whole closeout suite.

Return one evidence-bound verdict:

- `PASS` — no material gap found;
- `PASS_WITH_RESIDUAL_RISK` — acceptable with a named, bounded uncertainty;
- `CHANGES_REQUIRED` — a concrete defect or missing requirement blocks acceptance;
- `INCONCLUSIVE` — required evidence or environment is unavailable.

Quote paths, commands, and observed results. Do not manufacture style findings. If QA or UAT finds a defect in planned work, identify the affected checkpoint and the evidence that prior validation missed; the execution flow must reopen it.
