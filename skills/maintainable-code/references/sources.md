# Conceptual sources and reconciled disagreements

This skill intentionally synthesizes several schools of software design rather than enforcing one book literally. It applies the same design model prospectively during implementation and retrospectively during review.

## Robert C. Martin — Clean Code

Retained strongly:

- meaningful names and readable intent
- cohesive functions and modules
- explicit side effects
- duplication of knowledge as maintenance risk
- continuous cleanup
- tests as a refactoring safety net
- code should be optimized for reading and future change

Relaxed or made context-dependent:

- extremely short functions
- aggressive class/function decomposition
- hostility toward comments
- low parameter counts as a metric
- one-assertion-style testing rules
- object-oriented and exception-centric preferences as universal defaults

## John Ousterhout — A Philosophy of Software Design

Used to correct mechanical Clean Code application:

- complexity is the core design problem
- change amplification, cognitive load, and hidden dependencies are stronger signals than line counts
- prefer deep modules with simple interfaces
- hide design knowledge inside the module that owns it
- avoid excessive decomposition and pass-through layers
- comments are valuable for abstractions, rationale, invariants, and non-obvious constraints
- invest strategically in design rather than stacking tactical patches

## Martin Fowler — Refactoring

Used for change mechanics:

- refactoring is behavior-preserving restructuring
- improve design through small, safe transformations
- code smells are prompts to investigate, not automatic verdicts
- tests and short feedback loops make incremental restructuring safer

## Michael Feathers — Working Effectively with Legacy Code

Used for unsafe or untested areas:

- treat code without trustworthy behavioral protection as dangerous to change
- characterize existing behavior before redesigning uncertain code
- identify or create seams to observe behavior and break hard dependencies
- make the smallest safe change that improves future changeability

## Modern pragmatic corrections

### Duplication versus the wrong abstraction

Do not enforce “Don’t Repeat Yourself” mechanically. Similar syntax may represent different concepts. An abstraction that accumulates caller-specific flags and branches can be more expensive than temporary duplication. Re-introducing duplication can reveal the correct boundary.

### Comments

Prefer self-explanatory mechanics, but preserve information code cannot express well: rationale, invariants, protocol assumptions, units, ownership, performance constraints, concurrency contracts, and surprising tradeoffs.

### Performance

Object decomposition, dynamic dispatch, allocation, and indirection may materially harm hot paths. Use profiling and workload evidence. Maintainability remains important, but performance-sensitive code may need specialized shape.

### Language idioms

Apply principles through the host language. Rust `Result`, Go explicit errors, functional composition, data-oriented design, actors, or ownership types can express good design without following Java-oriented exception and object patterns.

### Tests

Prefer one coherent behavioral scenario per test. Multiple related assertions are fine when they describe the same outcome and remain diagnosable. Test value and refactor safety matter more than assertion counts.

## Public supplemental references

- John Ousterhout and Robert Martin discussion: https://github.com/johnousterhout/aposd-vs-clean-code
- John Ousterhout, A Philosophy of Software Design: https://web.stanford.edu/~ouster/cgi-bin/book.php
- Martin Fowler, Refactoring: https://refactoring.com/
- Martin Fowler, Definition of Refactoring: https://martinfowler.com/bliki/DefinitionOfRefactoring.html
- Sandi Metz, The Wrong Abstraction: https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction
- Dan Abramov, Goodbye, Clean Code: https://overreacted.io/goodbye-clean-code/
- Casey Muratori, Clean Code, Horrible Performance: https://www.computerenhance.com/p/clean-code-horrible-performance
