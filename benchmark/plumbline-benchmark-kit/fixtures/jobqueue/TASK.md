# JQ-1: cancellation and idempotent retry

Implement this small feature without changing the existing Store/CLI interfaces.
No real background worker, scheduler, sleep, HTTP server, or async framework is required.
All states below are lowercase strings. Methods return the current `get()` dictionary
unless stated otherwise. Invalid transitions raise StateError; missing jobs raise KeyError.
The existing `db` SQLite connection remains available for callers and diagnostic probes.

## Acceptance contract
J01. `cancel(job_id)`: queued -> cancelled; running -> cancelling. Repeating cancel
on cancelling or cancelled is a successful no-op. All other states raise StateError.
J02. `ack_cancel(job_id)`: cancelling -> cancelled; cancelled is a successful no-op;
all other states raise StateError. Update both the job and its active attempt.
J03. Once cancellation is requested, complete/fail must raise StateError and leave
cancelling unchanged. Terminal complete/failed/cancelled jobs cannot start.
J04. `retry(job_id, request_id)` creates the next queued attempt only from failed,
keeping the job id and failed history. Attempt numbers increase by one.
J05. Retry keys are scoped to the job and persisted. Replaying an already successful
key is a no-op in ANY later state and returns the current job, not a stale snapshot.
A fresh key on a non-failed job raises StateError and is not consumed. An empty or
non-string key raises ValueError. The same key on another job is independent.
J06. Job, attempt history, and successful retry-key registration change atomically.
A SQLite write failure must roll everything back; the same request can succeed later.
J07. Two Store instances (one per thread, same file) concurrently retrying the same
failed job with the same key both succeed without duplicate attempts. No timing sleeps
are required. Serializing SQLite writes is acceptable.
J08. Reopening a Store on the same file preserves all new state and keys. Existing
pre-feature database files continue to work; initialization can run repeatedly.
J09. Existing submit/start/complete/fail/get/history signatures and CLI output remain
compatible. Preserve `history()` ordering and exact number/state record shape.
J10. Extend CLI actions with cancel, ack-cancel and retry. Retry requires
`--request-id KEY`. Successful output is the same one-line JSON job shape.

Add meaningful regression tests. All acceptance checks operate at these public seams;
there is no prescribed private schema, abstraction, or implementation recipe.
