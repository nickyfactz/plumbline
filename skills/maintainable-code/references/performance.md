# Performance-aware design

Use when latency, throughput, memory, startup time, I/O, concurrency, or resource cost matters, or when a proposed cleanup changes execution shape in a hot path.

## Performance is observable behavior when users or system limits can feel it

Maintainability and performance are not enemies, but abstractions have runtime costs. Do not assume a stylistically cleaner design is performance-neutral.

First determine whether the code is performance-sensitive. Prefer measurements when available.

## Audit hot-path shape

Inspect for:

- avoidable algorithmic complexity
- repeated parsing, serialization, hashing, or conversion
- unnecessary allocations, copies, boxing, or temporary collections
- pointer-heavy/object-heavy traversal where data locality matters
- virtual/dynamic dispatch inside tight loops
- tiny abstraction layers that prevent batching or vectorization
- N+1 database/network access
- redundant I/O or filesystem work
- synchronous work on latency-sensitive paths
- lock contention or oversized critical sections
- task/thread explosion
- unbounded queues or fan-out
- repeated model/tokenization/inference setup in AI systems
- excessive logging/formatting on high-frequency paths

Do not report theoretical micro-costs in cold administrative code unless there is evidence they matter.

## Profile before and after meaningful changes

When feasible:

1. establish the relevant workload
2. capture baseline latency/throughput/memory/allocation data
3. identify the dominant cost
4. change the design
5. measure again

A benchmark should represent the production shape closely enough to answer the design question.

## Allow specialized code when justified

Duplication, larger functions, direct loops, specialized data structures, or fewer abstraction boundaries can be the correct design in performance-critical code.

The audit should still demand:

- clear invariants
- explicit ownership
- good names
- comments explaining non-obvious performance constraints
- benchmarks or profiling evidence where the tradeoff is material
- containment of specialized complexity behind a stable interface where possible

Avoid “cleaning up” hot code into an allocation-heavy or indirection-heavy object graph without measurement.
