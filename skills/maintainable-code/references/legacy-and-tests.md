# Legacy code and test safety

Use when behavior is poorly protected, the code is difficult to isolate, or the reviewer cannot confidently predict the effect of a structural change.

## Treat unprotected behavior as legacy risk

The practical distinction is not code age. The risk is whether behavior can be changed with fast, trustworthy feedback.

Before recommending aggressive restructuring, identify what currently protects behavior:

- focused unit tests
- integration tests
- contract tests
- end-to-end tests
- static/type guarantees
- production assertions or invariants
- reproducible manual validation

A high coverage number alone is not evidence that the risky behavior is protected.

## Characterize uncertain behavior

When nobody can confidently state what code does today, first capture representative current behavior. Characterization tests are observation tools: they establish a baseline before deciding which behavior is desirable.

Do not silently “correct” suspicious behavior while creating characterization coverage. Mark it separately as a potential defect.

## Find seams

A seam is a boundary where behavior or a dependency can be substituted or observed without rewriting the entire surrounding system.

Useful seams include:

- function or constructor parameters
- interfaces/traits/protocols
- module/import boundaries
- adapters around external systems
- factories
- clock/randomness abstractions when nondeterminism blocks testing
- file/network/database boundaries
- command/query boundaries

Prefer the smallest seam that unlocks safe observation or substitution. Do not introduce a framework-sized dependency-injection system to test one collaborator.

## Sensing versus separation

Ask why testing is hard:

- **Sensing problem:** the behavior occurs but tests cannot observe it.
- **Separation problem:** a dependency prevents the code from running in a test harness.

Solve the specific problem. Expose useful outcomes for sensing; isolate only the dependency that blocks separation.

## Test shape

Prefer tests that communicate one behavioral scenario. Multiple related assertions are acceptable when they describe one outcome and failures remain diagnosable.

Avoid:

- tests that mirror private implementation structure
- excessive mocks that encode call choreography instead of behavior
- shared mutable fixtures that make tests order-dependent
- tests that require unrelated infrastructure for a local rule
- huge end-to-end suites as the only protection for core domain logic
- brittle snapshot/golden tests with no reviewable semantic signal

## Refactorability signal

When a small behavior change requires enormous test setup, many unrelated mocks, or widespread fixture edits, record that as design evidence. Test friction often reveals hidden coupling or oversized responsibilities.
