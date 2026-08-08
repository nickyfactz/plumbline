---
name: plumbline-diagnose-engine
description: Internal Plumbline engine. Use only after the Plumbline router or a Plumbline phase wrapper selects diagnosis.
---

# Diagnose engine

## Outcome and completion

Identify the smallest evidence-backed root cause and the proportional next
action for the user's symptom. Complete Diagnosis with a reproducible signal,
ranked hypotheses or a clear evidence gap, root-cause evidence, fix boundary,
and verification result. Keep a small bug fix outside feature-plan ceremony
unless its scope genuinely escalates.

## Reproduce the exact symptom

Use the active checkout and a direct feedback signal for a small clear fix. For
a hard bug or performance regression, read the current code path, user
timeline, logs, tests, and bounded relevant history before broad archaeology.
Read `references/research-policy.md` and
`references/runtime-value-testing.md` when the diagnosis needs external facts
or a runtime proof gate.

Build and run the smallest deterministic loop that can go red on the exact
symptom: a focused test, CLI call, HTTP probe, trace replay, or narrow harness.
If no red-capable loop exists, name the missing artifact or environment access
and request the smallest useful addition.

Reproduce and minimize before theorizing. Rank three to five falsifiable
hypotheses and use one targeted probe per prediction. Keep temporary diagnostics
tagged, remove them, and rerun the original loop after the fix. Use repository
history selectively rather than automating `git bisect`.

Add a regression test only at a stable public seam that exercises the real
failure. When no correct seam exists, record the seam gap instead of creating
false confidence. Report root cause, evidence, fix boundary, and remaining
uncertainty.
