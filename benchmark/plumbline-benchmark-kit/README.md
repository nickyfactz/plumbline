# Plumbline Benchmark Kit · v1.0

A small execution benchmark for **verified completion per unit of real usage**, comparing stock Codex with a pinned Plumbline deployment. This is a working scaffold with starter repositories, neutral specifications and plans, external graders, reference solutions, a Python runner, and a Codex controller skill.

**Start with [START_HERE.md](START_HERE.md).** Open this folder in Codex and invoke `$plumbline-benchmark`.

## Tasks

| Fixture | Implementation boundary | Main correctness surface | Held-out test methods |
|---|---|---|---:|
| `jobqueue` | SQLite-backed jobs and a small command-line interface | Cancellation precedence, durable retry keys, duplicate retries, rollback, stale attempts | 13 |
| `configscope` | Configuration resolver, serializer, command-line interface | Missing versus null, inheritance, provenance, validation, round trips, caller isolation | 12 |
| `docaccess` | In-memory document service and request adapter | Workspace isolation, role checks, direct service calls, bulk atomicity, revoked access | 11 |

Each task has two meaningful checkpoints, an existing passing legacy test suite, and a specified observable contract. All use Python 3.11+ standard-library code. No framework installation, external service, browser, or network request is needed to solve or grade a task. Test-method counts are diagnostics, not point weights; some methods cover many generated cases.

## Benchmark boundary

Both arms receive identical source, `TASK.md`, `PLAN.md`, and task prompt. Plumbline setup adds only the approved workflow guidance and project-local roles/router before timing. The runner invokes the pinned plugin's own initialization scripts rather than asking a model to generate setup each time. Setup is deterministic and excluded from the execution metric.

Each attempt gets a fresh Git repository, a fresh operating-system Codex process, and an isolated `CODEX_HOME`. No conversation resume, agent history, or peer solution is provided. Root sessions run serially to reduce contention; Plumbline can use its normal internal worker concurrency.

Root tiers are Luna, Terra, Sol, and Astra, at medium reasoning. Plumbline's current role defaults remain unchanged, including Luna high implementers and code reviewers and Luna max QA. `baseline_mode: stock` does not disable native subagents; `single` is available as an explicitly different series.

The deployment revision is pinned to `a592eec`. Future campaigns may use a different revision, but never change it within a campaign. See [sources](docs/SOURCES.md).

## Main outputs

- Binary externally verified `PASS` plus explicit failure/infrastructure statuses.
- Observed execution spend per verified completion, counting failed attempts.
- Separate evidence-backed imported account debits, when available.
- Wall time, time to verified success, completion claims, failed acceptance checks.
- Input, cached input, output, reasoning-output subsets, root/worker models, and worker counts.
- Final patches, commits, source/configuration hashes, grader details, and raw local telemetry.
- Descriptive source-size and syntax/import diagnostics. No points for fewer tokens, smaller code, more workers, or more commits.

Missing worker usage, unknown prices, or unsupported telemetry suppress the price comparison; the report does not replace missing values with zero. API-rate estimates are not represented as a subscription invoice. [Telemetry details](docs/TELEMETRY.md).

## Contents

```text
.agents/skills/plumbline-benchmark/   Codex campaign-controller skill
fixtures/                           Three unfinished but runnable starter projects
graders/                            External contract checks; never copied into candidates
reference/                          Known-good implementations; never copied into candidates
plumbline_bench/                     Runner, isolated grading, telemetry, reporting
pricing/                            Dated model rate snapshot
prompts/                            Identical scored task prompt
tests/                              Offline fixture, mutation, parser and transport tests
docs/                               Host setup, methodology, evidence and limitations
bench.py                            Command-line entry point
config.example.json                 Safe bounded configuration template
```

The kit itself stays outside candidate workspaces. Run state defaults to a sibling `plumbline-benchmark-runs` folder. Logs and temporary Codex homes are local sensitive material; do not publish them indiscriminately.

## Manual commands

```bash
python bench.py selftest
python bench.py init-config
# Resolve local authentication/Ponytail as described in docs/HOST_SETUP.md.
python bench.py doctor
python bench.py prepare --preset full
python bench.py run --max-runs 2
# Inspect the first matched pair, then continue the same campaign.
python bench.py run
python bench.py report
```

On Windows, `py -3.11` or a resolved Python 3.11+ executable may replace `python`. `codex_command` is an argument array: it can use an absolute executable path, but is not a shell command string. An alternative config goes before the subcommand: `python bench.py --config my-config.json doctor`.

## Deliberate limitations

This is a compact personal engineering regression suite, not an adversarial agent-security evaluator or a general software-engineering leaderboard. External graders are held out from task prompts and run in a separate process; filesystem read isolation depends on the host and is not certified. No paid runs, Windows-native execution, or your actual Ponytail hook were exercised during scaffold creation. Local host compatibility must be checked before a long campaign.

The runner starts one fresh **Codex app-server session over stdio per cell**, not visible desktop tabs. Desktop is the controller interface; app-server execution is the measured host and is disclosed in every campaign. A desktop-only product change may not affect this benchmark until its app-server execution path changes.

See [methodology](docs/METHODOLOGY.md), [host setup](docs/HOST_SETUP.md), [validation](docs/VALIDATION.md), and [repeat/compare guidance](docs/REPEAT_AND_COMPARE.md).
