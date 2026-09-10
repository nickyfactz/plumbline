# Offline validation record

Validated during scaffold creation on September 5, 2026.

## Executed

`python bench.py selftest` completed with **20 passing harness test methods**. The final run output is in [selftest-output.txt](selftest-output.txt).

Those tests verify:

- All three unfinished starters preserve their existing behavior and fail the new requested feature.
- All three supplied reference implementations pass their complete external grades.
- Six deliberately defective reference variants are rejected, covering cancellation precedence, retry deduplication, null clearing, shadowed-layer validation, unauthorized update, and cross-workspace paths.
- Mixed root/worker pricing, cumulative usage deduplication, reasoning as an output subset, request-level long-context pricing, missing children, unknown models, and root-only fallback handling.
- Failed-attempt cost inclusion, undefined cost with zero passes, suppression of incomplete prices, and incomplete actual-debit coverage.
- Explicit baseline mode, completion markers, scoped permission configuration, and rejection of unsupported Ponytail evidence claims.
- A **simulated** two-attempt Codex transport campaign from staging through final grading/reporting, copied-credential deletion, and a second controller run that makes no duplicate attempts.

The fixture grading surface comprises 36 held-out test methods (13 jobs, 12 configuration, 11 authorization) and 10 pre-existing regression methods. Some methods exercise additional seeded or table-driven cases. These are test-method counts, not 46 independent task observations or a measured agent pass rate.

Python sources also passed syntax compilation. Documentation, JSON files, and the packaged archive were checked for missing local targets and archive corruption.

## Not executed here

No authenticated Luna, Terra, Sol, or Astra attempt was run. No actual subscription credit or dollar charge was measured. The native installed Codex permission model, native plugin lifecycle, fresh-session child telemetry, your Windows environment, and your custom Ponytail hook still require the documented local preflight.

The simulated process intentionally leaves both candidate features unfinished, producing FAIL results. Those FAIL lines in the test log demonstrate grader execution; they are **not** benchmark results for any real model or for Plumbline.

A hook matcher and a hash receipt are not substitutes for native hook execution evidence. A custom permission profile definition is not proof that every host tool enforces it. The first-pair controller gate checks these facts on the actual machine before continuing the matrix.
