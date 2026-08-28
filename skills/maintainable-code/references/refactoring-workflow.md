# Refactoring workflow

Use this branch for behavior-preserving structural change.

Read [`refactoring-safety.md`](refactoring-safety.md) before editing.

Load additional references only when their trigger applies:

- [`human-legibility.md`](human-legibility.md): readability, control flow, naming, expression shape, or navigation cleanup
- [`design-shape.md`](design-shape.md): module boundaries, responsibility, interfaces, decomposition, information hiding
- [`legacy-and-tests.md`](legacy-and-tests.md): weak or uncertain behavioral protection
- [`performance.md`](performance.md): hot-path or concurrency-sensitive structure
- [`code-smells.md`](code-smells.md): diagnosing the structural pressure that motivates the refactor

## Workflow

1. State the maintenance pressure being reduced.
2. Identify behavior that must remain unchanged.
3. Establish trustworthy validation around that behavior.
4. Make one meaningful, reversible structural move.
5. Run the narrowest relevant validation.
6. Reassess whether the move reduced the stated pressure.
7. Repeat only while each step remains justified.
8. Remove obsolete scaffolding made unnecessary by the new structure.
9. Apply the human-legibility gate to materially changed code.
10. Run broader validation before completion.

Do not smuggle feature changes or defect fixes into a refactor without naming and validating them separately.

Do not begin by mechanically splitting large functions. Clarify ownership and pressure first.

## Completion criterion

The refactor is complete when required behavior remains stable, the stated maintenance pressure is materially reduced, the result passes the same human-legibility gate as new implementation, and obsolete scaffolding created by the old structure is removed where safe.
