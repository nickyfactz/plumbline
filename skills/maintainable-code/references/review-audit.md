# Review and audit workflow

Use this branch for code review, post-implementation quality review, or a broader design/maintainability audit.

## 1. Establish the change surface

Identify:

- implementation area and intended responsibility
- important callers
- tests and behavioral protection
- external boundaries
- configuration and persistence
- runtime-sensitive paths
- repository-local conventions

**Complete when:** you can describe what the area owns, what depends on it, and which behaviors must remain stable.

## 2. Inspect maintenance pressure

Search for:

1. **change amplification:** one concept requires edits in many places
2. **mixed responsibility:** unrelated reasons to change live together
3. **hidden coupling:** callers depend on internals, ordering, globals, or implicit state
4. **leaky knowledge:** the same domain rule or protocol knowledge is encoded in several places
5. **cognitive load:** understanding a local change requires too much unrelated context
6. **wrong or shallow abstractions:** indirection adds surface area without hiding useful complexity
7. **unsafe change surfaces:** important behavior lacks trustworthy automated protection
8. **patch sediment:** old fixes, flags, fallbacks, compatibility paths, or dead branches obscure the current design
9. **human-legibility debt:** visual density, nesting, naming, expression shape, or poor conceptual grouping makes correct code difficult to scan
10. **hot-path hazards:** abstraction, allocation, I/O, locking, or data movement may be materially expensive where runtime evidence says performance matters
11. **missing mechanical quality gates:** maintained languages lack a reproducible formatter check or useful baseline linter/static analyzer, leaving basic quality dependent on agent/human memory

Load only the needed references:

- [`code-smells.md`](code-smells.md): functions, classes, naming, duplication, state, coupling, agent sediment
- [`human-legibility.md`](human-legibility.md): scanability, formatting, expression density, nesting, naming for humans, navigation burden
- [`design-shape.md`](design-shape.md): module/API boundaries, responsibility, information hiding, decomposition
- [`legacy-and-tests.md`](legacy-and-tests.md): weak test protection or uncertain behavior
- [`performance.md`](performance.md): runtime-sensitive findings
- [`refactoring-safety.md`](refactoring-safety.md): when recommending consequential structural change
- [`tooling-bootstrap.md`](tooling-bootstrap.md): formatter/linter coverage is absent, duplicated, overly customized, or non-reproducible

Do not create a finding merely because a function is long, a class is large, code is duplicated twice, a method has several arguments, comments exist, an interface has one implementation, or the reviewer prefers different whitespace.

**Complete when:** each candidate smell is tied to an actual consequence or discarded.

## 3. Diagnose before prescribing

For every material finding identify:

- **Evidence:** exact file/symbol/line or execution path
- **Shape:** what structural condition exists
- **Consequence:** why change, comprehension, testing, correctness, or performance becomes worse
- **Pressure:** what future change is likely to expose the problem
- **Direction:** the smallest design move likely to reduce the pressure
- **Safety:** tests, characterization, profiling, or staged migration needed before changing it

Prefer diagnosis over labels such as "God object", "not SOLID", or "unclean".

## 4. Rank by maintenance value

- **Critical:** credible correctness, data-loss, concurrency, or operational risk caused by the structure
- **High:** strong change amplification, hidden coupling, unprotected core behavior, or architectural pressure in actively changing code
- **Medium:** localized complexity, duplicated knowledge, confusing control flow, poor scanability, weak boundaries, or test friction with plausible maintenance cost
- **Low:** local readability or consistency improvement with limited downstream effect

Do not inflate severity to force cleanup.

For a formal report, read [`reporting.md`](reporting.md).

## Completion criterion

The review is complete only when every reported finding has concrete evidence, a maintenance or runtime consequence, a proportionate direction, and a validation path; human legibility has been explicitly assessed; high-risk areas in scope have been inspected; and pure taste differences have been removed.
