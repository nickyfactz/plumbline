# Design shape

Use this reference when judging module boundaries, architecture, responsibility, APIs, or decomposition.

## Complexity is the target

Treat complexity as the cost imposed on future change. Look for three symptoms:

- **change amplification:** a small conceptual change requires edits across many locations
- **cognitive load:** a maintainer must know too many unrelated facts at once
- **unknown unknowns:** dependencies or rules are hidden enough that the maintainer cannot tell what must change

A design improvement should reduce at least one of these without materially worsening the others.

## Prefer deep modules

A good module hides substantial implementation complexity behind a comparatively simple interface.

Look for shallow modules:

- pass-through wrappers whose interface is nearly as complicated as what they wrap
- one-line classes or services that merely rename another API
- chains of tiny helpers that must all be opened to understand one operation
- interfaces that expose configuration or sequencing details callers should not need to know

Do not split a coherent operation solely to make functions or files shorter. Extraction earns its existence when it creates a meaningful concept, hides complexity, improves reuse of knowledge, isolates volatility, or makes behavior materially easier to test or reason about.

## Hide knowledge, not just fields

Information hiding means one place owns a design decision.

Audit for knowledge duplicated across modules:

- protocol or file-format rules
- business calculations
- status/state mappings
- validation policy
- retry policy
- authorization rules
- serialization assumptions
- naming conventions encoded as parsing logic
- database/schema assumptions

Two modules may contain different code while still duplicating the same knowledge. This is more important than textual duplication.

## Cohesion and responsibility

Single responsibility is a change-cohesion test, not a one-method-per-class rule.

Ask:

- Which independent reasons could force this module to change?
- Do its methods operate on one coherent model or several unrelated subsets of state?
- Are orchestration, domain rules, persistence, transport, and presentation mixed in ways that make changes collide?
- Would splitting the module create stable boundaries, or merely more files and calls?

Prefer boundaries around knowledge and volatility, not runtime sequence alone.

## Avoid temporal decomposition

A sequence such as parse -> validate -> transform -> persist does not automatically imply four modules. If several stages share one body of domain knowledge, splitting by execution order can leak that knowledge across interfaces.

Group by what must be known, not merely what happens next.

## Make common cases simple

Good interfaces make ordinary use straightforward and hide exceptional machinery.

Look for:

- option/flag explosions
- callers repeatedly supplying the same combination of arguments
- special cases leaking through every layer
- public APIs that require internal sequencing knowledge
- state that can be constructed invalidly and repaired later

Prefer designs that eliminate invalid or exceptional states when practical rather than forcing every caller to remember a rule.

## Comments and contracts

Code can show mechanics; it cannot always show rationale, invariants, non-obvious constraints, units, concurrency guarantees, protocol assumptions, or why a simpler-looking approach is unsafe.

Preserve or add comments when they document those facts. Remove comments that narrate syntax, repeat names, or no longer match behavior.

## Design questions for an audit

1. What knowledge does this module own?
2. What complexity does its interface hide?
3. What internal decision has leaked to callers?
4. What concept is represented in more than one place?
5. What future change would cause shotgun edits?
6. Which abstraction is shallower than the code it replaced?
7. Which special case could be designed out of the interface?
8. Which split reduces cognitive load, and which split only increases navigation?
