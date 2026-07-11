---
name: plumbline-diagnose-engine
description: Internal Plumbline engine. Use only after the Plumbline router or a Plumbline phase wrapper selects diagnosis.
---

# Diagnose engine

Keep diagnosis proportional. For a small clear fix, use the active checkout and a direct feedback signal. For a hard bug or performance regression, read the current code path, user timeline, logs, tests, and bounded relevant history before broad archaeology. Read `references/research-policy.md` and `references/runtime-value-testing.md` when useful.

First build and run the smallest deterministic feedback loop that can go red on the user's exact symptom: a focused test, CLI call, HTTP probe, trace replay, or narrow harness. If no red-capable loop can be built, say what is missing and ask for the smallest artifact or environment access needed.

Reproduce and minimize before theorizing. Rank three to five falsifiable hypotheses, then use one targeted probe per prediction. Do not automate `git bisect`. Tag temporary diagnostics, remove them, and rerun the original loop after the fix.

Add a regression test only at a stable public seam that exercises the real failure. If no correct seam exists, document that as an architectural finding rather than writing a false-confidence unit test. Verify the fix, report root cause and evidence, and keep a small bug fix out of feature specification/plan ceremony unless complexity genuinely escalates it.
