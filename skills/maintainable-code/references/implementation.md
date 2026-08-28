# Implementation workflow

Use this branch when writing or modifying production code.

## 1. Establish the local contract

Before editing, identify:

- repository-local instructions and formatter/linter configuration
- behavior being added or changed
- the module that should own the behavior
- callers and external boundaries affected
- existing tests and invariants that must remain valid
- whether the path is performance-, concurrency-, persistence-, or protocol-sensitive

If ownership, module boundaries, interface shape, or decomposition is non-trivial, read [`design-shape.md`](design-shape.md).

**Complete when:** the intended owner, behavior, and important constraints are explicit enough to implement without inventing architecture mid-edit.

## 2. Ensure the quality toolchain exists

Identify the formatter and linter/static-analysis path for each language materially changed by the task.

If the repository lacks a working formatter or useful baseline linter/analyzer, read [`tooling-bootstrap.md`](tooling-bootstrap.md) and bootstrap the minimal conventional toolchain before substantive implementation.

If tooling already exists, use it. Do not replace or duplicate it during unrelated work.

**Complete when:** the relevant formatter/check and lint/static-analysis commands are known and reproducible for the repository.

## 3. Load the legibility contract

Before the first substantive implementation edit, read [`human-legibility.md`](human-legibility.md).

Use the repository's canonical formatter. Formatting is the baseline, not the finish line.

Shape the code so a maintainer can visually recover:

- major phases of the operation
- happy path and exceptional paths
- domain concepts
- state transitions and side effects
- boundaries between policy and implementation detail

Prefer meaningful intermediate values, semantic whitespace, explicit state, and coherent control flow over dense expressions or token-minimized source.

## 4. Keep structure proportional

During implementation, watch for:

- a function accumulating independent jobs
- a helper that merely renames another call
- repeated business knowledge in multiple places
- boolean/mode flags creating several behaviors behind one name
- invalid state combinations callers must remember
- framework/infrastructure details leaking into domain code
- speculative extension points unsupported by current variation
- another patch being added around a model already surrounded by patches

When one of these appears materially, read [`code-smells.md`](code-smells.md).

Do not mechanically extract functions or abstractions to satisfy a metric. Extraction earns its existence when it names a coherent concept, hides complexity, localizes knowledge, isolates volatility, or materially improves comprehension/testability.

## 5. Preserve a short feedback loop

Add or update the narrowest trustworthy tests for changed behavior.

- If existing behavior is poorly protected, uncertain, or difficult to isolate, read [`legacy-and-tests.md`](legacy-and-tests.md).
- If changing existing structure as part of the implementation, read [`refactoring-safety.md`](refactoring-safety.md).
- If the path is latency-, throughput-, memory-, allocation-, I/O-, lock-, or concurrency-sensitive, read [`performance.md`](performance.md).

Validate incrementally rather than waiting until the end of a large patch.

## 6. Self-review the diff

Before completion, inspect the changed code as if reviewing another engineer's patch.

Check for:

1. change amplification
2. mixed responsibilities
3. hidden coupling
4. duplicated knowledge or wrong abstractions
5. excessive cognitive load
6. unclear contracts, state, or side effects
7. visual density or poor scanability
8. patch sediment or obsolete paths
9. weak behavioral protection
10. performance-sensitive structure that needs measurement

Fix material issues introduced or exposed by the change when doing so remains within task scope. Record larger pre-existing debt rather than silently expanding into a rewrite.

## Completion criterion

Implementation is complete when behavior is validated; repository formatting/linting requirements pass where available; changed code passes the human-legibility gate; material new design debt has not been introduced; and intentionally retained complexity has a clear reason.
