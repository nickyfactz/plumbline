# Measurement contract

## Primary question

For a small fixed suite of implementation-ready tasks, does the deployed Plumbline workflow deliver more externally verified completions per unit of execution spend than stock Codex at the same root tier?

This measures an end-to-end mixed-model system. A Sol root delegating to Luna workers is meant to be cheaper than doing all work on Sol; pricing every worker as Sol would erase the intended economic benefit. Token count is diagnostic, never a reward.

## Outcome and grading

PASS requires every held-out contract test, the immutable legacy regression suite, candidate public tests, unchanged protected contract/configuration files, and no detected syntax or non-standard-library production import violation. A partial acceptance count remains useful diagnostic data but never becomes fractional completion. There is no subjective blended score.

Unfinished baselines deliberately pass the legacy tests and fail the requested new behavior. Each reference implementation must pass both suites. Six targeted defective solutions validate that the grader catches plausible errors. Graders assert behavior at public boundaries, not exact source formatting, private helper names, or a preferred implementation plan. The job-queue compatibility fixture includes its legacy persisted schema because preserving an existing database is an explicit contract.

The external grader is never mounted into a candidate repository or fed back during its attempt. It runs after the candidate stops. Models may write and run their own tests against the visible specification. The controller does not repair candidate code, provide hidden failures, or replay successful patches.

Status values separate PASS, FAIL, INVALID, TIMEOUT, BUDGET_EXHAUSTED, HOST_ERROR, HARNESS_ERROR, SETUP_ERROR, INTERRUPTED, and TELEMETRY_UNAVAILABLE. A candidate can pass behavior but have an unpriceable result; keep the pass visible and economic inference unavailable. Configured Plumbline with no observed activation is not evidence for the requested treatment.

`BUDGET_EXHAUSTED` is execution-incomplete, even when the post-stop external grader reports every acceptance check passing. The controller stops the live turn when a limit is reached, then grades the workspace that remains. That acceptance result is diagnostic evidence of the partial workspace, not a completed model run; no completion claim or verified-success time is inferred.

## Cost

For a completely measured group:

```text
observed cost per verified completion
    = sum(execution costs for all attempts, including failures) / verified passes
```

Zero passes means undefined, not zero dollars. Missing cost in any attempt means the complete-group price is unavailable. Do not delete failures or price only successful runs.

This is an observed descriptive statistic, not a guaranteed expected retry cost. Fresh repeats are not the same as user-guided remediation, and real repair attempts are not identically distributed. The kit does not claim to simulate human rework, discovery latency, or maintenance cost.

Execution-rate estimates use actual per-thread model IDs and separate uncached input, cached input, and billed output. Reasoning output is a subset, not an additional bill. Actual account units are separate evidence-backed imports; subscription percentage bars are not precise per-task dollar invoices. Setup, host probes, and the campaign-controller conversation are excluded from the per-task execution measure and must be disclosed separately. They are not assumed free.

Compare only matched task/model/repetition cohorts before claiming an A/B advantage. A budget-stopped campaign can have unequal partial cohorts; a favorable partial aggregate alone is not a winner. Fixed seeds balance arm order but do not make model outputs deterministic or reset provider caches.

## Timing

Wall time starts at candidate process launch and ends when it exits or is stopped. Successful verified time additionally includes external and final public grading. Failed attempts have no time-to-success. Setup and dependency preparation are outside timing; the fixtures have no package dependencies to install. Mean attempt time divided by observed pass rate is not advertised as a prediction of remediation time.

## Quality and claims

The completion marker is an explicit self-claim, not a grade. A COMPLETE marker followed by objective FAIL is a false completion. Missing markers are unknown, not automatically honest or dishonest. Infrastructure/integrity failures are separate from false-completion counts.

AST branch counts, changed files, size, and imports are descriptive diagnostics. They do not prove maintainability. No automatic judge is run or paid for in v1. A future blinded pass-versus-pass judge must use pinned criteria/model, counterbalanced order, and separate cost; it cannot rescue an objective failure.

## Scope and limits

All tasks use Python and two compact checkpoints. The suite intentionally does not measure frontend taste, large repositories, long-context recovery, multiday operations, or the whole Plumbline preparation lifecycle. A new model can plausibly reach a ceiling here; do not quietly add difficulty to make Plumbline win. Version the fixture suite when changing it.

The references and graders ship publicly with this kit. They are held out at runtime, not guaranteed absent from future training data. This is a local longitudinal engineering benchmark, not a contamination-free public leaderboard. Host read restrictions and model adherence are not certified defenses against malicious grader discovery.

The default A/B contrast includes the Plumbline plugin, its default project-local roles, generated guidance, and Nick's verified implementer-only Ponytail behavior. It identifies the deployed-stack effect, not the causal contribution of each component. A no-Ponytail campaign must be labeled separately.
