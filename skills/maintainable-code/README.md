# maintainable-code skill

`maintainable-code` is a model-invoked skill for both **implementation** and **review**.

It gives writers and reviewers one shared definition of good code shape:

- correct and behaviorally protected
- easy for humans to scan and understand
- localized around the concepts that own change
- appropriately abstracted rather than maximally abstracted
- explicit about state, side effects, and contracts
- safe to refactor
- performance-aware where runtime evidence matters

`SKILL.md` is a compact router plus shared doctrine. Each work mode has its own workflow file, and technical guidance is progressively disclosed only when that branch requires it.

## Why the skill is broader than a review checklist

A quality reviewer cannot permanently compensate for implementation guidance that arrives too late. The same principles should shape code while it is written and evaluate it afterward.

The skill therefore has four modes:

1. implementation
2. refactoring
3. review
4. audit

The implementation path includes a mandatory human-legibility gate and a self-review before completion. Review/audit uses the same criteria, which reduces the chance that writer and reviewer optimize for different definitions of quality.

## Recommended invocation wiring

The model-invoked `description` in `SKILL.md` is the first router. For repositories where code quality matters, also add an explicit pointer to the repository's always-loaded agent guidance.

Recommended `AGENTS.md` / equivalent pointer:

> **Maintainable code:** When writing, modifying, or reviewing production code, invoke the `maintainable-code` skill. Apply its implementation branch before and during edits and its review gate before declaring the work complete.

For a dedicated reviewer role:

> **Code review:** Invoke `maintainable-code` for design, human-legibility, refactor-safety, testability, and performance-shape review. Report evidence and consequences rather than style preferences.

For an implementation role:

> **Implementation quality:** Invoke `maintainable-code` when changing production code. Follow repository formatting and language idioms, apply the human-legibility gate, and self-review changed code before completion.

The pointer should stay short. The skill contains the details.

## Progressive disclosure layout

```text
maintainable-code/
├── SKILL.md
├── README.md
└── references/
    ├── implementation.md
    ├── refactoring-workflow.md
    ├── review-audit.md
    ├── tooling-bootstrap.md
    ├── human-legibility.md
    ├── design-shape.md
    ├── code-smells.md
    ├── refactoring-safety.md
    ├── legacy-and-tests.md
    ├── performance.md
    ├── reporting.md
    └── sources.md
```

### Reference triggers

Workflow branches:

- `implementation.md`: writing or modifying production code
- `refactoring-workflow.md`: behavior-preserving structural change
- `review-audit.md`: code review or larger quality/design audit

Technical references:

- `tooling-bootstrap.md`: formatter/linter missing, non-reproducible, duplicated, or being introduced to a new project
- `human-legibility.md`: every substantive implementation; readability, formatting, control flow, naming, visual density, navigation
- `design-shape.md`: module boundaries, interfaces, information hiding, decomposition, responsibility
- `code-smells.md`: functions/classes, duplication, coupling, state, long-horizon agent sediment
- `refactoring-safety.md`: before structural changes
- `legacy-and-tests.md`: uncertain or poorly protected behavior
- `performance.md`: hot paths, latency, throughput, memory, allocation, I/O, concurrency
- `reporting.md`: formal review/audit output
- `sources.md`: rationale and conceptual provenance

## Design sources

The skill reconciles the useful parts of:

- Robert C. Martin — *Clean Code*
- John Ousterhout — *A Philosophy of Software Design*
- Martin Fowler — *Refactoring*
- Michael Feathers — *Working Effectively with Legacy Code*
- pragmatic critiques of premature abstraction, style dogma, and performance-blind design

The skill deliberately treats metrics and smells as investigation prompts rather than hard verdicts.
