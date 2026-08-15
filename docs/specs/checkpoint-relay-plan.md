---
status: ready_for_acceptance
feature: Checkpoint Relay
specification: "external:C:/Users/nickd/Desktop/PLUMBLINE_CHECKPOINT_RELAY_SPEC.md"
source: "C:/Users/nickd/Desktop/PLUMBLINE_CHECKPOINT_RELAY_SPEC.md"
source_sha256: "6AAA7C31E46B57A7391E0372528CE7E22D6DAAEB1008208D55DD447ADBA5E4AB"
base_commit: "53d1ef09894e7173d7c3cedb75c269af488394f0"
target_branch: experiment/checkpoint-relay
execution_mode: continuous
current_checkpoint: CP-R9
checkpoint_status: Complete
lifecycle_owner: Plumbline Execute
last_verified_commit: "53d1ef09894e7173d7c3cedb75c269af488394f0"
next_safe_action: Review CP-R9 evidence and accept or request changes.
delegation_roles: "Direct: no approved project-local roles"
delegation_status: direct
ready_for_acceptance: true
---

# Checkpoint Relay live implementation plan

## Source and authority

The external implementation handoff named in frontmatter is the approved
product and architecture contract. Its SHA-256 records the adopted source
version. This companion plan carries only execution, recovery, and evidence
state; it does not replace or reinterpret the source.

Fixed boundaries:

- continuous Execute remains the default;
- relay mode is explicit, additive, and fail-closed;
- shared lifecycle policy remains host-neutral;
- Codex is the only automatic adapter in this experiment;
- Claude keeps existing behavior and receives only an unsupported/manual
  capability scaffold;
- automatic relay requires a normalized, durable, Git-backed execution
  contract;
- the relay sidecar never owns product decisions, plan edits, evidence
  classification, Git, acceptance, or retries;
- no relay runtime implementation begins before CP-00 is accepted.

## Execution topology

`CP-00 -> CP-R1 -> CP-R2 -> CP-R3 -> CP-R4 -> CP-R5 -> CP-R6 -> CP-R7 -> CP-R8 -> CP-R9 -> Ready for Acceptance`

All post-preflight checkpoints depend on CP-00. CP-R2 precedes relay core work.
Shared contracts, schemas, and moving runtime integration remain serial. Later
independent static/review lenses may run in parallel only when their scopes are
disjoint and the main-thread join is explicit.

## CP-00: Mandatory feasibility preflight

**Status:** Complete

| Boundary | Architecture review, baseline regressions, supported-host probes, disposable fixtures, and evidence only; no relay runtime implementation |
|---|---|
| Acceptance | CP-00A through CP-00K pass, or the experiment stops with a named hard failure |
| Done when | The overall gate is classified from observed evidence and every required result is recorded below |
| Evidence | Commands, official interface references, fixture paths, observed native-app behavior, and residual limitations |
| Next action | Start CP-R1 shared execution-mode policy |

### CP-00 evidence matrix

| Test | Status | Required result | Evidence |
|---|---|---|---|
| CP-00A Host boundary architecture | Passed | A future Claude adapter can replace only the host adapter | Shared policy remains plan/state based; Codex transport belongs behind one adapter; continuous mode and a manual/unsupported Claude adapter form the second implementation seam. No current shared skill or reference imports Codex transport. |
| CP-00B Claude compatibility baseline | Passed | Existing non-relay Claude behavior has no material regression | `python scripts/validate.py`, `python scripts/test_install_claude_agent_team.py`, and `python scripts/test_plumbline_hook.py` passed. A live Claude CLI/app was unavailable; the later cross-host checkpoint retains live Claude UAT. |
| CP-00C App Server capability | Passed | Supported interfaces create/name/start/observe a fresh repository thread | Codex CLI 0.144.0; official App Server protocol; `thread/start`, `thread/name/set`, `turn/start`, streamed completion, and Desktop task listing all succeeded for thread `01a002d7-f2d7-7682-9dd7-be521a9f7d49`. |
| CP-00D Desktop first-class thread | Passed | Externally created thread is usable in normal Codex Desktop | Desktop task listing returned the named persistent task `Plumbline Relay CP-00 App Server Probe` with the expected `E:\\Plumbline` cwd and completed prompt. No database or UI scraping was used. |
| CP-00E Active-turn Desktop behavior | Passed with limitation | Running task remains visible and safely steerable, or has a bounded acceptable limitation | `turn/steer` changed active thread `01a002d8-bba1-72e2-89ed-400fb95281a7` from `BEFORE_STEER` to final `AFTER_STEER`. Desktop listed it during execution but reported cross-process status as `notLoaded`; the App Server stream remained authoritative for live status. |
| CP-00F Fresh-context isolation | Passed | CP-02 receives durable state but not CP-01 conversational canary | Fresh root thread `01a002da-85e1-7ca0-9177-89ae3ef9b72e` recovered `current_checkpoint=CP-00` and the source hash from the live plan without receiving either earlier probe conversation. |
| CP-00G Project/Plumbline continuity | Passed | Fresh thread receives repository guidance, plugin, config, permissions, and Git state | `thread/start` returned `E:\\Plumbline`, global and repository `AGENTS.md` instruction sources, read-only sandbox, approval policy, and the current repository state. `skills/list` discovered installed Plumbline `0.1.15+codex.20260814221127`; explicit skill-item injection returned `PLUMBLINE_FRONT_DOOR_INJECTED`. The front door is intentionally absent from model auto-selection because it declares `disable-model-invocation: true`; the adapter must inject it explicitly. No project-local agent/config files exist in this checkout, so no fallback was invented. |
| CP-00H Manual user steer | Passed with Remote limitation | Native steer preserves controller identity and creates CP-02 once | Codex Remote submitted normal follow-up turns on the same task `01a002e2-b903-7d81-b8f1-572dfeb9e581`; the exact correction persisted `desktop-steer-confirmed`, preserved controller/thread identity, completed CP-01, and selected CP-02 once. App Server `thread/read` observed the completed turns and valid boundary. The exact correction was not an in-flight `turn/steer`; that transport operation was proven separately in CP-00E. Relay must observe durable turns/artifacts and must not keep a competing active turn open while awaiting user input. |
| CP-00I Application restart | Waived — risk accepted | Restart preserves usable checkpoint history without duplicate CP-01 | On 2026-08-14 the user explicitly accepted this residual risk because externally created tasks are already visible and durable in Desktop, and declined interruption of in-flight tasks. Revisit only if restart recovery fails in later use. |
| CP-00J Two-checkpoint relay | Passed | Exactly two fresh checkpoint threads reach Ready for Acceptance | Disposable Git fixture at `C:\\Users\\nickd\\AppData\\Local\\Temp\\plumbline-checkpoint-relay-cp00`, baseline `2cd4aec636fa5d2b1196c294ffc738d2bf095dad`, advanced through exactly two root tasks: CP-01 `01a002e2-b903-7d81-b8f1-572dfeb9e581` and fresh CP-02 `01a002ea-6c5f-7112-a6da-80d16ea42bc3`. CP-02 recovered only from `AGENTS.md`, plan, state, and Git; recorded both durable thread identities; reached `ready_for_acceptance`; passed focused validation and `git diff --check`; and created no commit. |
| CP-00K Plan adoption/readiness | Passed | Native and external plans classify correctly and only normalized Git-backed state becomes Relay Ready | Disposable probe `C:\\Users\\nickd\\AppData\\Local\\Temp\\plumbline-relay-readiness-cp00k` classified a committed native plan as `relay_compatible` and ready; classified a sufficient external work order as `adoptable`; generated the smallest source-referencing companion; rejected that dirty companion as not ready; accepted it only after a separate lifecycle-owned baseline commit; and classified `Improve the project.` as `insufficient`. The probe never performed Git integration. |

### CP-00 stop conditions

Current classification: **Passed with one explicitly accepted residual risk.**
CP-00A-H and J-K passed. CP-00I restart behavior is waived by the user for this
experiment and remains later UAT; no other hard failure was observed.

Transport findings that constrain the later adapter:

- use `skills/list` to discover the current versioned Plumbline path;
- inject the front door as an explicit `skill` input item because
  `disable-model-invocation: true` intentionally keeps it out of model-driven
  selection;
- use the creating App Server stream as live-status authority because the
  Desktop cross-process index can report an active external task as
  `notLoaded`;
- treat Codex Remote/Desktop follow-ups as durable turns on the same task and
  observe them through `thread/read`; do not keep a competing active turn open
  while waiting for user input;
- never read or write Codex persistence directly.

- programmatically created threads cannot participate in normal Codex Desktop;
- supported interfaces cannot provide an unambiguous fresh-thread completion
  signal;
- native steering creates controller conflict or duplicate checkpoint work;
- required behavior needs direct Codex database manipulation or UI scraping;
- Claude continuous usage acquires a Codex dependency or relay side effect;
- plan normalization must reinterpret settled product intent;
- duplicate-controller risk remains unresolved.

## CP-R1: Shared execution-mode contract

**Status:** Complete

Add host-neutral `continuous | checkpoint_relay` policy, preserve the continuous
default, define manual fallback, and prove shared lifecycle text contains no
Codex transport concepts.

**Evidence:** Added the host-neutral `checkpoint-relay.md` contract, optional
plan-schema mode with continuous default, Plan/Execute/front-door routing, and
architecture/static validation. `python scripts/validate.py`, hook smoke, and
`git diff --check` passed.

## CP-R2: Plan adoption and Relay Readiness

**Status:** Complete

Implement `plumbline-plan-adoption-engine` and deterministic readiness
classification before relay core work. Preserve external source authority and
require one current checkpoint, legal dependencies/action, and a coherent Git
baseline.

**Evidence:** Added internal `plumbline-plan-adoption-engine`, dependency-free
normalized readiness validation, Git-backed source/plan enforcement, and smoke
coverage for dirty rejection, accepted baseline, and invalid next action. Full
static, hook, Codex-team, Claude-team, readiness, and diff checks passed.

## CP-R3: Relay core

**Status:** Complete

Implement the deterministic host-neutral controller, transition validation,
single-controller lock, fail-closed state, and disposable host-local transport
state. No model calls or product interpretation.

**Evidence:** Added a dependency-free relay controller with one host-local lock,
atomic state, readiness and fingerprint checks, deterministic transition
validation, explicit pause/manual states, and no retry behavior. Fake-host tests
cover success, manual fallback, stale/no-advance pause, and duplicate lock
rejection.

## CP-R4: Codex host adapter

**Status:** Complete

Implement only the Codex operations proven by CP-00 behind the host seam.

**Evidence:** Added the stdio App Server adapter and runner using only
initialize, `skills/list`, `thread/start`, `thread/name/set`, `turn/start`,
`turn/completed`, `thread/read`, and `thread/unsubscribe`. It discovers the
installed namespaced Plumbline front door and injects that exact skill item.
Fake-host tests passed, and a live no-model App Server probe resolved the
installed `plumbline:plumbline` front door.

## CP-R5: Codex signal bridge

**Status:** Complete

Wake the relay only to reread durable state after a relevant turn; never edit
the plan, advance a checkpoint, or start a successor directly from the signal.

**Evidence:** Added a plugin `Stop` hook that writes one atomic host-local wake
marker only when repository and task identity match an active relay state. The
controller alone consumes the marker and rereads the plan. Ordinary and
mismatched sessions are inert. Smoke coverage proves a later user turn can
complete an unchanged checkpoint without opening a competing turn.

## CP-R6: Durable handoff enforcement

**Status:** Complete

Require downstream-relevant decisions and corrections to exist in existing
authoritative artifacts before a relay-mode checkpoint stops.

**Evidence:** Execute now performs one fresh-task durability test at the Relay
boundary and promotes only successor-relevant state into existing
authoritative artifacts. It explicitly rejects transcript copying and generic
handoff-file creation.

## CP-R7: Recovery and duplicate protection

**Status:** Complete

Cover controller/process/Desktop restart, stale state, fingerprint drift,
disconnects, pause/stop, and ambiguous identity. Stop before duplicate dispatch.

**Evidence:** Relay state now records a Git/source/plan fingerprint and task
identity. Restart adopts only a legal durable transition; active, unknown, or
drifted state pauses before dispatch. Live/malformed locks fail closed, dead
owners are reclaimable, App Server failure pauses without retry, and host-local
`--pause`/`--stop` controls wake a waiting controller without editing the plan.

## CP-R8: Acceptance and closeout

**Status:** Complete

Use the smallest acceptance-thread policy supported by observed implementation
complexity and retain normal explicit acceptance/Closeout ownership.

**Evidence:** The runner now traverses legal checkpoint handoffs serially and
then creates one fresh Acceptance task. Its prompt forbids inferred acceptance
and tells the same task to run normal Closeout only after the user explicitly
accepts. A structured relay marker prevents nested controllers. Core and
adapter smoke tests cover the acceptance boundary.

## CP-R9: Cross-host regression and documentation

**Status:** Complete

Repeat Claude and Codex continuous regressions, complete relay UAT, validate
packaging, and document automatic Codex versus manual unsupported-host behavior.

**Evidence:** Full static validation, Codex and Claude agent-team installers,
continuity/relay hook smoke, readiness, relay-core, fake App Server adapter, and
`git diff --check` passed. Disposable native UAT repository
`plumbline-relay-uat-cpr9b` created CP-01 task
`01a00308-8b28-7df0-b4c5-b4958eccdbc6`, committed `f6049c5`, created fresh
CP-02 task `01a0030b-289e-73c3-8ca6-c7effaad254b`, committed `8010e16`, then
created Acceptance task `01a0030c-e51c-7562-9c25-9513eb55e0ef`. Acceptance
reran exact proof, found clean Git, and stopped at `acceptance_pending` without
inferring acceptance or starting Closeout. The initial UAT exposed and removed
an adapter sandbox override; the passing run inherited host/project permissions.

## Residual questions

These are engineering findings to resolve during CP-00, not product questions:

- the supported Codex App Server transport and completion signal available in
  the installed host version;
- the writable host-local data location available to the plugin/runtime;
- whether thread naming and Desktop active-turn steering are fully supported or
  bounded limitations;
- whether the relay runtime can remain dependency-free or should use an
  already-provided host runtime.
