# Human legibility and code shape

Use this reference whenever writing, modifying, refactoring, or auditing source code for readability.

Human readability is an engineering requirement. A formatter can make syntax consistent while leaving code cognitively dense. Treat formatting as the baseline and **scanability** as the design goal.

## The target

A maintainer should be able to glance at a function and recover its rough shape before understanding every expression.

Good visual shape exposes things such as:

```text
validate

load state

derive decision

perform side effects

persist

return
```

The exact phases vary. The important property is that the code has visible conceptual paragraphs rather than reading as one continuous sentence.

## Canonical formatting comes first

Use the repository's existing formatter and configuration. Do not invent a competing style. If no formatter/linter baseline exists, bootstrap it via [`tooling-bootstrap.md`](tooling-bootstrap.md) rather than relying on manual formatting.

Common defaults when the repository does not specify otherwise:

- Rust: `rustfmt`; use Clippy separately for linting where configured
- Go: `gofmt` / `goimports`
- Python: repository-configured Ruff formatter or Black
- JavaScript / TypeScript: repository-configured Prettier or Biome
- C / C++: repository-configured `clang-format`
- C#: repository `.editorconfig` / `dotnet format`
- Java/Kotlin: repository formatter and IDE/Gradle rules

A canonical formatter solves spacing, indentation, wrapping, and brace consistency. It does not decide whether an expression, function, or control-flow structure is easy to understand.

Do not reformat unrelated files merely to satisfy personal preference.

## The squint test

Inspect the function without deeply decoding each expression.

Ask:

- Can the major phases be seen from whitespace and statement boundaries?
- Is the happy path visually discoverable?
- Are exceptional paths contained rather than dominating the indentation?
- Do names reveal the domain concepts being manipulated?
- Can important state changes and side effects be spotted?
- Does a reader need to mentally evaluate a large expression just to know what the statement means?
- Must the reader jump through many trivial helpers to reconstruct one operation?

If the basic shape is invisible until every expression is decoded, investigate visual complexity.

The squint test is a heuristic, not permission to split everything into tiny functions.

## Code has paragraphs

Use blank lines to separate conceptual phases.

Prefer:

```rust
validate_request(&request)?;

let profile = resolve_profile(&request)?;
let worker = create_worker(profile)?;

persist_worker(&worker).await?;
publish_worker_started(&worker).await?;

Ok(worker)
```

over a visually undifferentiated sequence when the statements represent distinct phases.

Do not insert blank lines after every statement. Group statements that belong to the same thought.

## Prefer one conceptual operation per statement

A statement becomes difficult to read when it simultaneously:

- retrieves state
- transforms it
- performs branching
- handles failure
- mutates another object
- performs I/O
- constructs the final result

Use meaningful intermediate values when they expose concepts or phases.

Dense:

```rust
let result = state.lock().await.workers.iter().filter(...).map(...).collect();
```

More legible when the stages matter:

```rust
let state = state.lock().await;

let active_workers = state
    .workers
    .iter()
    .filter(is_active_worker);

let worker_states = active_workers.map(resolve_worker_state);

let result = worker_states.collect();
```

Do not introduce intermediates that merely rename obvious syntax. Each name should remove mental work or expose a meaningful stage.

## Prefer vertical clarity over horizontal compression

Source code is not charged by the character.

Break complex expressions at semantic boundaries. Avoid packing nested calls, closures, conditionals, error conversion, and mutation into a single expression merely because the language allows it.

Do not optimize source code for model output tokens.

## Name conditions and domain concepts

When a Boolean expression represents an important idea, give the idea a name.

Prefer:

```rust
let retry_is_allowed =
    worker.is_enabled()
    && worker.retry_count < retry_policy.max_attempts()
    && worker.last_error.is_some();

if retry_is_allowed {
    ...
}
```

or, when the behavior belongs naturally to the type:

```rust
if worker.is_eligible_for_retry(&retry_policy) {
    ...
}
```

over forcing every reader to repeatedly decode the same condition.

Avoid abstracting a simple, local condition when the new name adds no information.

## Keep the happy path visible

Use the host language's idioms to prevent error and guard handling from burying the primary operation.

In Rust, pattern guards and early returns can often flatten nesting:

```rust
let Some(worker) = worker else {
    return Ok(());
};

if !worker.enabled {
    return Ok(());
}

let Some(profile) = &worker.profile else {
    return Ok(());
};

// primary operation
```

Do not apply early returns mechanically. The goal is readable control flow and obvious lifecycle behavior.

## Control nesting deliberately

Investigate nesting when the reader must retain several conditions to understand the current block.

Before extracting a helper, consider:

1. guard clauses
2. clearer state representation
3. named conditions
4. `match`/pattern matching where idiomatic
5. reducing mixed responsibilities
6. then extraction if a coherent sub-operation deserves a name

Nesting depth is not itself a defect.

## Method chains and pipelines

Fluent code is useful when it expresses one coherent pipeline.

Keep a chain together when every stage is easy to scan and the transformation remains conceptually uniform.

Break the chain when:

- closures contain meaningful branching
- stages change abstraction level
- error conversion becomes non-trivial
- mutation or I/O is hidden inside the pipeline
- an intermediate result is important to debugging
- a stage deserves a domain name
- the chain becomes a visual wall

## Closures and callbacks

Nested closures often save names at the cost of indentation and debugging clarity.

Extract a closure when the extracted operation has a useful name or independently meaningful contract. Do not create `handle_item_inner()` merely to shorten the parent function.

## Naming for humans

Prefer names that preserve the domain vocabulary.

Be suspicious of context-poor names such as:

- `data`
- `info`
- `obj`
- `tmp`
- `val`
- `mgr`
- `proc`
- `handler`
- `ctx` or `cfg` outside narrow conventional scopes

Short conventional names are fine when their meaning is obvious locally. Optimize identifier length for comprehension, not token economy.

A longer precise identifier is often cheaper than a comment explaining an abbreviation.

## Comments

Formatting cannot express every design fact.

Use comments for:

- why a simpler-looking approach is unsafe
- invariants
- units and boundary assumptions
- ownership/lifecycle constraints
- concurrency requirements
- protocol or compatibility reasons
- performance tradeoffs
- intentional deviations from an obvious implementation

Avoid comments that narrate syntax or compensate for names/control flow that can be made clear directly.

Use headings inside very large functions sparingly. If comments are the only way to divide several unrelated jobs, investigate the function's responsibility.

## Abstraction level affects visual readability

A function is harder to scan when domain policy is interleaved with raw serialization, SQL, socket writes, UI formatting, or framework plumbing.

Prefer the top-level operation to read in concepts appropriate to its role:

```rust
validate_worker(worker)?;

let retry_policy = resolve_retry_policy(worker);

send_worker_start(worker).await?;
record_worker_started(worker);

Ok(retry_policy)
```

Lower-level implementation detail can remain below that boundary.

Do not hide important performance or ownership semantics behind deceptively simple names.

## Navigation is part of readability

Excessive extraction can make code locally pretty and globally unreadable.

A reader should not have to open ten one-line helpers to understand one coherent algorithm.

Before extracting, ask:

- Does this create a concept worth naming?
- Does it hide real complexity?
- Does it isolate volatility or a side effect?
- Does it remove duplicated knowledge?
- Does it improve independent testing enough to justify navigation?
- Will the caller read more like the domain?

If not, keep the operation local and improve its internal shape.

## Review findings for human-legibility debt

A legibility finding should explain the cognitive consequence, not merely state a formatting preference.

Useful evidence:

- the primary operation is buried under four nested guard/error levels
- a 20-stage method chain contains mutation, I/O, and nested branching
- five unrelated phases have no visual or semantic boundaries
- domain concepts are repeatedly represented by generic temporary names
- the function jumps between domain policy and raw infrastructure mechanics
- dozens of tiny pass-through helpers make local behavior impossible to reconstruct without navigation
- comments are acting as section dividers for independent responsibilities

Weak evidence:

- a function exceeds an arbitrary line count
- a line could be shorter
- a blank line could be added
- the reviewer prefers another brace style
- a descriptive local could theoretically be inlined

## Implementation gate

Before considering changed code complete:

1. run or satisfy the repository formatter
2. inspect the diff after formatting
3. apply the squint test to materially changed functions
4. simplify dense expressions that hide concepts
5. make important names and side effects explicit
6. remove accidental visual noise introduced by the change
7. ensure extraction has not created excessive navigation
8. preserve comments that carry rationale or contracts
9. confirm the result still follows repository idioms

The goal is code a human can safely read and modify, not code that merely parses cleanly.
