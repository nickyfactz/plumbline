# Refactoring safety

Use before prescribing or performing structural changes.

## Refactoring means behavior preservation

A refactor changes internal structure while preserving externally observable behavior. A cleanup that intentionally changes behavior is a redesign or feature/fix and should be named and validated separately.

Keep two questions distinct:

1. Is the current structure expensive or risky to maintain?
2. What behavior is allowed to change?

Do not smuggle behavior changes into a maintainability refactor.

## Prefer small reversible transformations

Large rewrites make it difficult to know which structural change caused a regression. Prefer a sequence in which the system remains working after each meaningful step.

Useful sequence:

1. establish tests or characterization around behavior at risk
2. make one structural move
3. run the narrowest relevant validation
4. simplify names/interfaces exposed by the move
5. repeat
6. run broader validation before completion

For a report, describe the sequence when the proposed refactor is risky enough that “extract this class” is not a safe instruction by itself.

## Refactor toward pressure, not aesthetics

A refactor should answer a real pressure:

- make a recurring change local
- hide volatile implementation details
- remove duplicated knowledge
- make an invariant explicit
- isolate a hard dependency
- eliminate a special case
- simplify a public interface
- separate behavior with independent reasons to change
- make critical behavior observable/testable

Avoid speculative extension points and generic frameworks without demonstrated variation.

## Preserve working abstractions until evidence says otherwise

An abstraction should survive because it hides useful complexity, not because effort was invested in it.

If shared code becomes branch-heavy and caller-specific:

1. identify where callers genuinely differ
2. consider inlining the abstraction back into callers
3. remove irrelevant branches from each caller
4. observe the actual duplication that remains
5. extract only the stable shared concept

Temporary duplication is acceptable when it reveals the correct boundary.

## Refactoring order

A safe default order is:

1. clarify names and tests around the area
2. isolate side effects and external boundaries
3. reduce hidden dependencies
4. move duplicated knowledge toward one owner
5. reshape module boundaries
6. remove obsolete compatibility and dead paths
7. optimize navigation and local readability

Do not begin by mechanically splitting functions; that can freeze the wrong boundaries into more files.

## Validation

Match validation to risk:

- unit tests for pure/local behavior
- integration or contract tests for boundaries
- characterization tests for uncertain legacy behavior
- end-to-end tests for critical user/system flows
- static analysis/type checks for structural guarantees
- benchmarks/profiling for hot-path changes
- concurrency/stress tests for ordering and shared-state changes

A proposed refactor without a plausible validation path should be reported as higher risk.
