# Code smells and agent sediment

Use this reference when inspecting functions, classes, naming, control flow, duplication, state, or code accumulated through long-running implementation work.

A smell is a prompt to investigate. It becomes a finding only when evidence connects it to maintenance or runtime cost.

## Functions and methods

Investigate functions that combine several of these traits:

- high-level policy mixed with low-level parsing, I/O, formatting, or mutation
- several independent phases separated by comments
- many branches that represent different jobs rather than one algorithm
- hidden state changes or surprising side effects
- temporal prerequisites that callers must remember
- many parameters because the operation crosses several concepts
- boolean/mode flags that select substantially different behaviors
- repeated defensive checks caused by an unclear contract
- long-lived mutable locals whose state must be mentally simulated

Length alone is not a finding. A longer cohesive algorithm can be clearer than ten conjoined helpers.

## Classes and modules

Investigate:

- low cohesion: different method groups use different fields/dependencies
- “manager”, “service”, “util”, or “processor” modules that own unrelated policy
- constructors that perform I/O, registration, global mutation, or other work
- objects exposing data and also expecting callers to manipulate their internals
- internal implementation details repeated through getters/setters or public fields
- pass-through layers that add names but hide no complexity

Size alone is not a finding. Ask how many independent reasons the module has to change.

## Naming and semantic clarity

Flag names when they materially obscure intent:

- generic containers such as `data`, `info`, `result`, `manager`, `handler` where a domain concept exists
- multiple words for the same domain concept
- one word reused for unrelated meanings
- names that conceal units, direction, ownership, or state where those distinctions matter
- functions named like queries that mutate state
- comments required only because identifiers and structure fail to reveal the operation

Prefer domain language and stable concepts over implementation trivia.

## Duplication and wrong abstraction

Distinguish:

- **duplicate syntax:** code looks similar
- **duplicate knowledge:** two places encode the same rule or decision

Duplicate knowledge is the stronger smell.

Do not extract an abstraction merely because two blocks look alike. Warning signs of a wrong abstraction include:

- growing option sets
- caller-specific branches inside a “shared” helper
- parameters that exist only for one caller
- conditionals selecting subtly different algorithms
- shared code that changes for unrelated consumers

When an abstraction has become wrong, consider inlining it, allowing temporary duplication, then extracting the stable concept revealed by current requirements.

## Coupling and change amplification

Look for:

- one feature edit touching many unrelated layers because knowledge is scattered
- deep call chains that expose internal object structure
- shared mutable globals or service locators hiding dependencies
- framework types flowing deep into domain code
- modules that must be modified together despite having separate interfaces
- order-dependent calls with no explicit state model
- cross-module access to internals “just this once”

Trace actual callers before recommending a new boundary.

## Control flow and state

Investigate:

- deeply nested branches where guard conditions could expose the main path
- state machines encoded as booleans and ad hoc combinations
- repeated type switches distributed across the system
- retries/fallbacks that can re-enter logic unexpectedly
- error paths that mutate partial state
- swallowed errors or logs used as a substitute for failure semantics
- cleanup/resource ownership spread across multiple scopes

Prefer explicit state and ownership when the language supports them.

## Agent sediment

Long-horizon coding agents commonly leave structurally valid but incoherent sediment. Search deliberately for:

- repeated patches around the same symptom instead of a repaired model
- compatibility branches for implementations that no longer exist
- fallback paths added after failures but never removed after the root cause changed
- wrapper/helper proliferation created to finish local tasks
- duplicate implementations produced by different worktrees or agents
- new configuration flags used to avoid resolving a design decision
- dead feature scaffolding and abandoned TODO paths
- tests coupled to internal structure because they were written to satisfy the latest patch
- comments describing an earlier implementation
- “temporary” adapters that became permanent architecture
- multiple sources of truth created during migrations

When several patches orbit the same concept, stop proposing another patch and reconstruct the intended model.


## Visual density

When the concern is formatting, scanability, expression density, nesting, naming for human readers, or navigation burden, use [`human-legibility.md`](human-legibility.md) rather than duplicating those rules here.

Visual density becomes a design finding when it materially increases cognitive load or obscures control flow, state, side effects, or domain meaning.

## Findings that are usually too weak alone

Do not report these without consequence:

- function over N lines
- class over N lines
- more than N parameters
- one implementation behind an interface
- two similar blocks of code
- a comment that could theoretically be deleted
- a nested conditional that remains easy to read
- a private helper used once
- a literal that is obvious in context
