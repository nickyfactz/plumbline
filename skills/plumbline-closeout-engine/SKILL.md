---
name: plumbline-closeout-engine
description: Internal Plumbline engine. Use only after the Plumbline router or a Plumbline phase wrapper selects accepted-work closeout.
---

# Closeout engine

Closeout begins only when the user says the work is accepted or asks to integrate/clean up after a ready-for-acceptance audit. Execute owns implementation, focused/full proof, acceptance-required canonical documentation, and stable-delta review until Ready for Acceptance. Closeout does not redo first-time implementation proof; after acceptance it owns integration, transient cleanup, plan retirement, worktree/branch handling, and publishing preparation.

Closeout preflight is acceptance-led, not artifact-led. An external work order, specification, plan, implementation, or explicit user acceptance is sufficient to identify the work. This does not require an active Plumbline specification or plan, and does not create one merely to make closeout conform. Report only a missing acceptance signal, competing artifact set, or destructive cleanup decision that actually blocks the requested closeout.

Classify remaining open items before closeout. Only an Acceptance blocker prevents Ready for Acceptance; Residual risk, Operational follow-up, and Future enhancement remain visible without forcing a new planning cycle.

First choose the smallest closeout mode that preserves the required proof:

- Light closeout for bounded direct work, documentation/process changes, or already-documented work with no transient specification/plan cleanup. Read the current status/diff, focused validation, acceptance signal, documentation impact, and residual risk.
- Full closeout for work with an active specification or plan, migrations, security/privacy, compatibility, material runtime behavior, canonical documentation reconciliation, or transient artifact cleanup. Read the specification, plan, QA verdict, UAT evidence, Git history, current status, and repository documentation routing; prepare the coverage matrix when a specification-to-diff mapping is needed.

Do not skip a required UAT or canonical-document check merely to keep closeout light. Do not reread unrelated large documents when the selected mode and current artifacts identify the exact sections needed.

Prepare a concise product-level UAT surface and hand off to Local when validation is singleton, hardware-bound, exceptionally heavy, or cheaper there. Reconcile canonical current-state documentation; investigate code/doc disagreement instead of blindly overwriting either side. A justified no canonical change is valid.

Before deletion, produce the specification-to-diff coverage matrix, final verification evidence, remaining risks, and the exact transient paths. Delete imported source, active specification, and live plan only after explicit user acceptance. Preserve useful canonical docs, agents, tests, and Git history. Do not rewrite history, create GitHub issues/PRs, or run a custom worktree cleanup system. Integrate through the user's requested local flow; remote publishing is outside Plumbline v1.
