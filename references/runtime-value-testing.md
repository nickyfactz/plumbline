# Runtime-value testing

Tests are a risk-control decision, not a ritual. Add a permanent test when it protects stable behavior at a public seam or catches a plausible regression that other checks would miss. Prefer one valuable test over many implementation-coupled tests.

Good seams include a CLI/API boundary, user-visible workflow, public service contract, persisted state transition, or integration behavior with a known failure mode. Expected values should come from the specification, a worked example, or an independent known-good source.

Allowed outcomes are: a focused automated test; a static/type/lint check; a deterministic command or HTTP probe; manual UAT; a targeted review; or a documented no-test decision with the risk and compensating evidence. A literal configurable default, prose, private method, snapshot of incidental structure, or a trivial wiring change usually does not deserve a permanent test.

For bugs, test the minimized failure at a correct public seam when one exists. If no seam can reproduce the real issue, record the seam gap instead of adding false confidence. Never require red-green-refactor for every configuration, documentation, refactor, or maintenance change.
