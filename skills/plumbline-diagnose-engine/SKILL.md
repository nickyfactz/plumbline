---
name: plumbline-diagnose-engine
description: Internal Plumbline engine. Use only after the Plumbline router or a Plumbline phase wrapper selects diagnosis.
---

# Diagnose engine

## Outcome and completion

Identify the minimum sufficient root cause, not merely the next error, and
choose the proportional next action for the user's symptom. Decide first
whether the question is local or a design question. A clear local defect gets
the bounded failure-path trace below. A product-wide property (performance,
latency, size, cost, output quality), a symptom that recurs in the same area
after correction, or a root-cause request about the system's behavior starts
with the step-back design review, then traces only what the review points to. For a runtime
blocker, regression, contract violation, repeated failure, or failed expensive
gate, complete a bounded failure-path trace before proposing the correction:
reproduce the symptom, inspect the relevant caller and callee or state owner,
compare observed behavior with the contract or invariant, and locate the fix
boundary at the owner of the broken behavior. Expand the trace only when a
shared caller, contract, or state transition makes it necessary. A trivial
local fix may stay lightweight when the report records `Local cause confirmed`
and why wider tracing is unnecessary.

## Step-back design review

The step-back review is distinct from a local trace. Dispatch one fresh,
high-effort architect (or perform it on the main thread when no architect role
exists) with no plan history, the design note as its starting point, and an
open investigation with an effort budget: it may read the whole path the
property depends on. Its mandate is to answer two questions: is the design the
cause, and what is the simplest design that meets the target, including what to
delete. It ranks causes by estimated impact and ends with `Root cause:` or
`Evidence gap:`; figures, timings, or inventories alone are not a result.

Trigger it for a product-wide property, for a third correction on the same area
for the same symptom, or from the acceptance-churn check. When it finds a
design change, update the design note first, then re-plan the affected
checkpoints; removing code is a first-class outcome. When it finds none,
correction continues and Execute's stall rules apply.

## Completion

Complete Diagnosis with a reproducible signal, the relevant failure path,
root-cause evidence, the violated contract or invariant, fix boundary,
verification result, and remaining uncertainty. A green rerun that only moves
the error is not diagnosis. Keep a small bug fix outside feature-plan ceremony
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

Reproduce and minimize before theorizing. Rank only the plausible falsifiable
hypotheses needed to explain the failure and use discriminating probes rather
than a fixed probe count. Diagnostic tests and probes are working artifacts:
remove them before checkpoint completion when they only locate the cause. If
they expose a durable regression, generalize the proof at a stable public seam;
when no correct seam exists, record the seam gap instead of creating false
confidence. Rerun the original loop after the fix. Use repository history
selectively rather than automating `git bisect`.

Keep diagnosis notes proportional. Update the active plan only with the current
root-cause conclusion, material blocker or residual, and next action. Command
logs, compiled outputs, repeated manifests, diagnostic captures, and correction
directories are disposable working material unless a named future consumer
needs the exact object. A failed probe does not turn them into an immutable
attempt; summarize what changed the decision, reuse still-valid artifacts, and
clean clearly task-owned superseded output before it accumulates.

Add a regression test only at a stable public seam that exercises the real
failure. When no correct seam exists, record the seam gap instead of creating
false confidence. Do not patch the reported error line solely to make the
current loop green before the failure path and fix boundary are understood,
except for immediate safety containment; mark containment provisional and
continue diagnosis. When Diagnose follows a failed Execute checkpoint, keep the
same candidate and checkpoint active. Same candidate means the same objective
and accepted behavior; the fix may remove or restructure earlier code. Return a correction path to Execute; do
not close the objective or select a successor. Environment and harness
failures may require repairing or replacing the evidence path before
implementation resumes. Report root cause, evidence, fix boundary, and
remaining uncertainty.
