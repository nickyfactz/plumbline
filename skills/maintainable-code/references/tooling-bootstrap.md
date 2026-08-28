# Tooling bootstrap

Use this reference when a repository lacks a clear formatter and/or linter for a language being modified, or when quality tooling exists but is not wired into a repeatable project command.

The goal is **boring automation**, not a style framework.

A formatter makes presentation deterministic. A linter/static analyzer catches suspicious or non-idiomatic constructs. These tools support human legibility; they do not replace design review or the human-legibility rules.

## Bootstrap policy

For each language materially changed by the task:

1. Detect the language, build system, package manager, lockfile, toolchain files, existing formatter/linter configs, project scripts, and Continuous Integration (CI) checks.
2. Reuse existing project tooling when it is functional. Do not install a competing formatter or overlapping lint stack because another tool is personally preferred.
3. If the formatter is missing, choose the ecosystem-standard or low-configuration formatter.
4. If the linter/static analyzer is missing, choose the ecosystem-standard or recommended/default rule set.
5. Install tools as repository-local development dependencies or toolchain components when the ecosystem supports that model. Avoid machine-global dependencies that another contributor or CI runner would not automatically receive.
6. Add the smallest configuration necessary for deterministic execution. Prefer tool defaults.
7. Add stable project commands for:
   - **format/write** — apply formatting
   - **format/check** — verify formatting without changing files
   - **lint/check** — run the recommended/default lint or static-analysis baseline
8. Use the repository's existing task runner or package scripts when one exists. Do not add a new task framework merely to wrap one command.
9. Run the tools on the current repository and distinguish:
   - issues introduced by the current change
   - pre-existing findings
   - generated/vendor code that should normally be excluded
10. Wire non-mutating checks into CI when the task scope permits and the repository has CI. Do not make a large legacy repository fail on thousands of unrelated pre-existing warnings merely to complete a local feature.
11. Record any intentional suppression with a local reason. Prefer fixing the code or configuring one justified exception over broad disable directives.

**Complete when:** contributors and agents can discover and run one deterministic formatter check and one useful lint/static-analysis check for each materially maintained language without knowing local machine setup.

## Configuration philosophy

Default to **minimal configuration**.

Good reasons to configure:

- generated, vendored, build-output, or fixture paths must be excluded
- repository line endings or language edition/version must be declared
- framework/runtime globals genuinely change lint semantics
- a default rule is demonstrably wrong for the codebase
- an additional correctness rule catches a known recurring defect class
- formatter behavior must match already-established repository style to avoid repository-wide churn

Weak reasons to configure:

- personal preferences about quotes, braces, semicolons, import grouping, or line length when the default is already readable
- enabling every available lint rule
- forcing subjective complexity thresholds
- making warnings errors before an existing repository has a clean baseline
- adding plugins because they are popular rather than because they protect a real invariant
- duplicating rules already enforced by the compiler, formatter, or another analyzer

Do not configure the linter to fight the formatter. Let the formatter own mechanical layout.

## Fresh-project defaults

These are defaults only when the repository has no established alternative.

### Rust

Prefer the standard Rust toolchain:

- formatter: `rustfmt`
- linter/static analysis: Clippy

When managed by `rustup`, ensure the components are available rather than adding unrelated project dependencies.

Typical commands:

```text
cargo fmt --all
cargo fmt --all -- --check
cargo clippy --workspace --all-targets
```

Add `--all-features` only when exercising all features is valid for the repository.

Treat `-D warnings` as an opt-in project policy, not an automatic default for an established codebase. Compiler/toolchain upgrades can introduce new warnings unrelated to the current patch.

Keep `rustfmt.toml` absent or minimal unless the repository has a demonstrated formatting requirement. Prefer stable formatter options.

### Python

Prefer Ruff for a fresh repository because it provides both a formatter and linter with a small formatter configuration surface.

Install it using the repository's existing Python dependency workflow (`uv`, Poetry, pip/requirements, etc.) as a development dependency.

Typical commands:

```text
ruff format .
ruff format --check .
ruff check .
```

Start from Ruff's defaults. Do not enable `ALL` as a generic quality policy.

Prefer `pyproject.toml` when the project already uses it. Add configuration only for target Python version, excludes, or justified repository-specific behavior.

Type checking is a separate concern. Reuse an existing Pyright/mypy setup; do not introduce strict typing project-wide as part of formatter bootstrap unless requested.

### JavaScript / TypeScript

First reuse existing Prettier, ESLint, Biome, framework-specific linting, or repository scripts.

For a fresh project with no established tooling, prefer **Biome** when its language/framework support covers the project: it provides formatting and linting with recommended lint rules enabled by default and avoids maintaining two overlapping style tools.

Install it as a development dependency with the repository's package manager.

Typical commands are conceptually:

```text
biome format --write .
biome format .
biome lint .
# or a repository script wrapping biome check
```

Use the tool's current CLI syntax/version when implementing; do not copy commands blindly from this reference.

Keep `biome.json` minimal. Prefer the recommended lint preset, not the all-rules preset.

When the repository already uses ESLint/Prettier, retain them rather than migrating during unrelated feature work. For a new ESLint setup, start from ESLint's recommended configuration and use Prettier only for formatting if Biome is not being used.

Do not run two formatters over the same files.

### Go

Use the tools shipped with Go:

- formatter: `gofmt` / `go fmt`
- baseline suspicious-construct analysis: `go vet`

Typical commands:

```text
go fmt ./...
go vet ./...
go test ./...
```

Go formatting is intentionally low-configuration. Do not add a competing formatter.

Additional analyzers such as Staticcheck may be valuable, but they are an explicit quality upgrade rather than required formatter bootstrap.

### C# / .NET

Prefer the .NET SDK facilities already available to the project:

- formatter/style application: `dotnet format`
- compiler/Roslyn analyzers: use the analyzers already included/enabled by the SDK and project settings

Typical verification:

```text
dotnet format --verify-no-changes
dotnet build
dotnet test
```

`dotnet format` reads `.editorconfig` when present and otherwise has defaults. Start without a large custom `.editorconfig`; add only project-relevant rules.

Do not automatically enable every analyzer or highest analysis mode on an established project.

### C / C++

Prefer existing build-system integration.

When absent:

- formatter: `clang-format`
- static analysis: `clang-tidy`

These ecosystems require more project-specific build/compiler knowledge than Go/Rust/Python formatting. Bootstrap conservatively: choose a well-known base style or preserve apparent repository style, generate a small config, and ensure `clang-tidy` receives the correct compile database.

Do not mass-format an established C/C++ repository merely because `.clang-format` was missing.

### Java / Kotlin

Prefer existing Gradle/Maven/IDE-enforced tooling.

For a fresh Java project, a deterministic formatter such as Google Java Format (often wired through the build) is preferable to hand-maintaining formatting rules. Add static analysis only through a small recommended baseline compatible with the build.

For Kotlin, prefer the repository's established formatter/linter such as ktfmt/ktlint and existing compiler/static-analysis setup.

Because Java/Kotlin build ecosystems vary, do not inject a large plugin stack without checking the project's build conventions.

### Other languages

Find the ecosystem's canonical formatter and broadly accepted baseline analyzer/linter.

Prefer, in order:

1. language/toolchain built-in
2. de facto standard with minimal configuration
3. repository/framework standard
4. a configurable general-purpose tool only when the above do not fit

Document the selected commands in the project rather than relying on global machine state.

## Existing repository migration

Do not turn "install a formatter" into an unrelated whole-repository rewrite.

If formatting the entire repository creates a huge diff:

1. add/configure the tool
2. decide whether a one-time mechanical formatting commit is explicitly in scope
3. otherwise restrict formatting enforcement to touched code/files when practical
4. record the remaining baseline debt
5. plan a separate mechanical formatting change if full normalization is desired

A formatting-only migration should be separated from behavioral changes when possible because mixed diffs are harder to review and blame.

## CI behavior

CI should run **check modes**, not rewrite source.

A good baseline pipeline verifies:

1. formatter produces no diff
2. lint/static analysis passes at the agreed baseline
3. tests/build pass

Keep local write/fix commands separate from CI verification commands.

When tools support safe autofix, agents may use it locally and then inspect the diff. Do not blindly apply unsafe or semantics-changing fixes.

## Agent installation discipline

Before installing anything, inspect the environment and repository.

- Respect the active package manager and lockfile.
- Prefer exact/reproducible tool versions through the ecosystem's normal lock/toolchain mechanism.
- Do not change production runtime dependencies to add development tooling when a dev/tool dependency mechanism exists.
- Do not replace existing tooling during an unrelated task.
- Do not install globally just because it is simpler for the current machine.
- Do not disable large rule groups to get a green check.
- Explain any new tool/config in the repository's normal contributor documentation or scripts when needed for discoverability.
- After bootstrap, use the tool on every subsequent relevant implementation/refactor invocation.

The automation should reduce decisions for humans, not create a second subsystem they must maintain.
