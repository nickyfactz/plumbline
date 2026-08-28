---
name: maintainable-code
description: Shape and review production code for human legibility, maintainability, safe change, and performance-aware design. Use when writing, implementing, modifying, refactoring, or reviewing code; planning implementation structure; performing code-quality or architecture audits; or investigating code that is difficult to understand or change.
---

# Maintainable code

Shape code for the cost and risk of its **next change**.

The code must serve two audiences:

1. the runtime, which needs correct and appropriate behavior
2. the human maintainer, who needs to understand and change that behavior safely

Do not optimize source code for model token economy, syntactic cleverness, or compliance with a style doctrine. Prefer code whose intent, control flow, ownership, and important tradeoffs are recoverable by a human reader.

## Governing principles

Use these as defaults, not laws:

- **Clarity:** intent should be recoverable without reconstructing the author's entire mental model.
- **Scanability:** visual shape should reveal rough control flow and conceptual stages before every expression is decoded.
- **Locality:** a conceptual change should require edits near the concept that owns it.
- **Depth:** prefer stable interfaces that hide meaningful complexity over swarms of shallow wrappers.
- **Cohesion:** code that changes for the same reason should tend to live together.
- **Information hiding:** important design decisions and domain knowledge should have clear ownership.
- **Explicitness:** dependencies, state transitions, side effects, invariants, and failure behavior should be visible at the appropriate boundary.
- **Evidence:** preserve duplication, comments, larger functions, direct code, or specialized implementations when they are clearer or safer than the proposed abstraction.
- **Behavior preservation:** a refactor changes structure, not externally observable behavior, unless behavior change is explicitly in scope.
- **Testability:** difficult-to-test code is evidence about coupling, not permission to distort a good runtime design.
- **Performance awareness:** abstraction is not free; profile or benchmark when runtime cost is material.
- **Repository fit:** repository-local conventions and host-language idioms outrank generic style preferences.

## Choose one work branch

Load only the branch that matches the current task:

- **Writing or modifying production code:** read [`references/implementation.md`](references/implementation.md).
- **Behavior-preserving structural refactor:** read [`references/refactoring-workflow.md`](references/refactoring-workflow.md).
- **Code review or larger quality/design audit:** read [`references/review-audit.md`](references/review-audit.md).

Do not load the other workflow branches unless the task genuinely crosses modes.

## Shared anti-dogma rules

- Prefer **one coherent operation** over an arbitrary function-length limit.
- Prefer **semantic whitespace and meaningful locals** over compressing source for fewer lines or tokens.
- Prefer **one behavioral scenario** over a literal one-assertion-per-test rule.
- Prefer **useful rationale and contract comments** over a blanket "comments are failures" stance.
- Prefer **stable abstractions discovered from pressure** over eliminating every instance of duplication immediately.
- Prefer **deep modules** over splitting code until navigation itself becomes the complexity.
- Prefer **language-native error, ownership, and composition models** over importing one paradigm into every language.
- Prefer **measured hot-path efficiency** over stylistic purity when the two conflict.
- Prefer **repository consistency** over introducing a new personal formatting system.

## Universal completion gate

No branch is complete until:

- required behavior is validated at a level proportionate to the change
- a reproducible formatter and useful baseline linter/static-analysis path exists for materially maintained languages, and their checks pass at the repository's agreed baseline
- materially changed code is human-scannable
- important state, side effects, and contracts are understandable
- no material design debt was introduced merely to finish the task
- intentionally retained complexity has a concrete reason
