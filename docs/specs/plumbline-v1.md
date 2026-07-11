# Plumbline Design Specification

**Status:** Approved for implementation  
**Version:** 1.0  
**Date:** 2026-07-11  
**Product:** Plumbline  
**Tagline:** Aligned engineering workflows for agentic development  
**Target platform:** OpenAI Codex plugin system  
**Predecessor:** `superpowers-personal`

---

## 1. Executive summary

Plumbline is a Codex-native engineering workflow plugin that keeps product intent, implementation, verification, and canonical repository documentation aligned without imposing heavyweight process on every change.

It combines the strongest parts of two existing approaches:

- Matt Pocock's small, focused, progressively disclosed skills; repository-first grilling; high-level testing seams; and separation between explicit orchestration and reusable discipline.
- Superpowers' automatic workflow guidance, evidence-driven execution, isolated subagent work, verification before completion, and structured movement from idea to implementation.

Plumbline deliberately removes the behaviors that make the current `superpowers-personal` deployment expensive or frustrating:

- No universal startup bootstrap.
- No "invoke a skill for every task" mandate.
- No automatic takeover merely because the plugin is installed.
- No universal Test-Driven Development (TDD) requirement.
- No tests for documentation, private implementation details, or literal configuration values unless they protect meaningful runtime behavior.
- No micro-task plans containing every line of code.
- No plugin-owned Git worktree system.
- No automatic GitHub issue, ticket, pull request, or remote workflow.
- No mandatory new sessions for ordinary phase transitions.
- No per-task multi-agent review ceremony for trivial work.
- No fixed repository documentation hierarchy imposed on established projects.
- No copied global agent team or installer that scatters files across user configuration.

Plumbline has two complementary interaction styles:

1. **Automatic guidance after explicit repository initialization.** A tiny repository-local router classifies ordinary prompts and enters the appropriate phase.
2. **Explicit side doors.** The user can invoke `$plumbline`, `$plumbline-shape`, `$plumbline-plan`, `$plumbline-review`, or another focused phase directly, including in repositories that have never been initialized.

The plugin is intended to feel polished and native inside Codex while leaving a minimal, reversible footprint in each repository.

---

## 2. Problem statement

Agentic coding workflows fail in two opposite ways.

At one extreme, an agent jumps directly into implementation from an underspecified idea, invents product behavior, misses repository conventions, and wanders across the codebase. At the other extreme, workflow plugins attempt to prevent every mistake through universal ceremonies: mandatory brainstorming, exhaustive plans, strict TDD for every change, custom worktree management, repeated reviews, and constant skill injection.

The supplied `superpowers-personal` archive demonstrates the second failure mode. It currently contains 15 top-level skills, approximately 17,700 words across `SKILL.md` files, more than 300 KB of skill content, a universal `using-superpowers` bootstrap, a separate agent-routing layer, custom worktree instructions, universal TDD guidance, exhaustive planning, custom installers, and global agent deployment. The result is reliable in some large flows but expensive in context, noisy in ordinary work, and too rigid for configuration, documentation, and small maintenance changes.

The resulting user problems are:

- Light changes enter heavyweight workflows.
- Agents ask technical architecture questions that the user should not need to answer.
- Brainstorming asks fewer useful product questions than a strong grilling session while still performing more ceremony.
- Plans become long code transcripts rather than durable execution maps.
- Plans are written once, then ignored after compaction or subagent dispatch.
- Universal TDD creates low-value tests that freeze prose, configuration values, private structure, and implementation details.
- Test suites grow without proportional regression protection.
- Plugin-managed worktrees create confusing and unsafe environment duplication.
- Long-running feature requirements disappear into summarized conversation context.
- Canonical documentation drifts from implementation and sends later agents down obsolete paths.
- Generic subagents inherit inappropriate models, reasoning effort, or personas.
- Installing several overlapping workflow plugins causes conflicting instructions rather than better results.
- Removing a workflow plugin leaves unclear repository residue.

Plumbline must solve these failures without becoming another elaborate methodology that blocks user work.

---

## 3. Product vision

> Plumbline lets a user describe the product outcome they want, then gives Codex enough structure, durable memory, and independent verification to deliver that outcome without losing alignment or forcing the user to manage software-engineering minutiae.

The user owns product intent. The agent owns engineering judgment.

Plumbline should be especially useful to a capable non-software-engineer or "vibe coder" who can make product decisions but should not be expected to decide module boundaries, adapter placement, schema normalization, test seams, state ownership, or contract shapes.

The plugin should also remain useful to experienced engineers who want direct control through explicit phase commands and who may supply existing specifications, plans, or handoffs from another model.

---

## 4. Goals

### G-1. Proportional workflow

Plumbline must apply the smallest process that safely fits the work. Small changes remain small. Substantial features receive durable structure.

### G-2. Product-directed autonomy

The agent must resolve ordinary technical decisions from canonical documentation, repository evidence, specialist agents, and current primary sources. The user should be asked only about choices that materially change product behavior, scope, experience, privacy, cost, destructive data handling, compatibility, or another difficult-to-reverse product consequence.

### G-3. Durable feature memory

For plan-based work, source material, specification, plan state, checkpoint evidence, deviations, and corrections must survive context compaction, session changes, and subagent boundaries through tracked repository artifacts and Git history.

### G-4. Repository alignment

Plumbline must adopt an established repository's documentation, architecture, terminology, validation, agent, and Git conventions. It may recommend repairs, but it must not impose a fixed structure merely because the repository has not used Plumbline before.

### G-5. Canonical truth

A completed change must not knowingly leave the repository's authoritative documentation describing an obsolete system state.

### G-6. Valuable testing

Testing should protect stable runtime behavior and plausible regressions, not implementation details, prose, or arbitrary constants. Plumbline must be biased against redundant, brittle, and low-value tests.

### G-7. Native Codex integration

Plumbline must use Codex's plugin, skill, subagent, configuration, and managed-worktree facilities rather than recreating them.

### G-8. Reversible adoption

Installation must be inert. Repository activation must be explicit. Automatic behavior must be removable through one obvious local kill switch. Offboarding must preserve useful project improvements by default.

### G-9. Context efficiency

Only the router and the currently relevant phase should enter context. The plugin must avoid universal bootstraps, duplicated doctrine, broad trigger descriptions, and accumulated subagent narration.

### G-10. User authority

Explicit user instructions override Plumbline's defaults. Plumbline may explain risk and residual uncertainty, but it must not argue the user into following a preferred process.

---

## 5. Non-goals

Plumbline v1 will not:

- Manage GitHub issues, tickets, pull requests, labels, or project boards.
- Require remote collaboration or production-support workflows.
- Create or maintain its own Git worktree directories.
- Implement a background worktree registry or cleanup service.
- Force a fixed `docs/` taxonomy on established repositories.
- Require every repository to use formal Domain-Driven Design artifacts.
- Require TDD for every feature, fix, refactor, configuration change, or documentation change.
- Require a permanent test for every function or method.
- Automatically reduce an entire legacy test suite.
- Automatically run `git bisect` or broad repository-history archaeology.
- Spawn recursive subagent organizations.
- Allow multiple implementation agents to edit overlapping files in parallel.
- Treat technical layers as separate product features.
- Split one user-defined feature into many micro-specifications or micro-plans for agent convenience.
- Use session-start hooks to activate itself.
- Mutate a repository during plugin installation.
- Fully roll back every useful artifact during offboarding.
- Provide a cross-platform compatibility abstraction for Claude Code, Gemini, or other harnesses in v1.

---

## 6. Design influences

### 6.1 What Plumbline adopts from Matt Pocock's skills

- Skills should be small, focused, and composable.
- Full instructions should load only when a skill is selected.
- Explicit orchestration and model-invoked reusable behavior should be separated when that improves invocation reliability.
- A user-invoked wrapper may be extremely small.
- Skill descriptions are part of the context budget and must earn every word.
- Branch-specific reference material belongs behind progressive-disclosure pointers.
- Grilling should ask one question at a time, recommend an answer, and research repository facts instead of asking the user.
- Testing should operate at stable public seams and protect behavior rather than implementation.
- Deep modules, clear interfaces, locality, and consistent domain language improve both human and agent reasoning.

### 6.2 What Plumbline adopts from Superpowers

- Feature work benefits from deliberate movement from idea to specification to implementation.
- Agents should verify evidence rather than claim success from intuition.
- Subagents can isolate noisy exploration and bounded implementation work.
- A feature plan should be executable in checkpoints.
- Independent review is valuable before acceptance.
- User acceptance and integration are separate from automated completion.
- Git history can preserve the evolution of a feature.

### 6.3 What Plumbline rejects from both approaches when too heavy

- Universal workflow activation.
- Mandatory full design for trivial changes.
- Exhaustive user interviews about technical details.
- Two-to-five-minute plan steps.
- Complete implementation code inside plans.
- Fresh session or handoff as the default phase transition.
- Universal red-green-refactor enforcement.
- Per-task implementer plus specification reviewer plus quality reviewer loops.
- Plugin-owned worktree lifecycle.
- Automatic issue-tracker publication.
- Repeated doctrine across skills, agents, and repository instructions.

---

## 7. Product principles

### P-1. Alignment over control

Plumbline keeps work aligned; it does not own the user's project.

### P-2. Evidence before ceremony

A workflow step exists only when it changes behavior or preserves evidence. Ritual without a concrete risk is removed.

### P-3. Latest safe phase

When the user supplies an existing design, plan, handoff, implementation, or accepted feature, Plumbline enters at the latest defensible phase. It does not restart upstream work merely to establish procedural ownership.

### P-4. Product questions to the user; engineering questions to the agent

The user is not expected to debate module boundaries, data ownership, test seams, composition patterns, or function signatures.

### P-5. One feature, one line of execution

A feature is the complete product outcome. Frontend, backend, schema, persistence, security, and documentation work are checkpoints inside that feature, not separate plans.

### P-6. Durable active artifacts; clean final repository

Specifications and plans are tracked and authoritative during implementation, then removed after accepted closeout. Canonical docs retain the resulting truth.

### P-7. Main-thread orchestration

The main thread owns the feature. Subagents are bounded workers and reviewers, not autonomous workflow controllers.

### P-8. Repository truth is discovered, not embedded

Agent personas and skills point to canonical documents and real code. They do not carry mutable copies of repository architecture.

### P-9. Defaults are recommendations, not overrides

Worktrees, review, testing, and acceptance have strong defaults. Explicit user direction remains authoritative.

### P-10. Easy exit

One local router directory activates automatic behavior. Removing it stops automatic behavior.

---

## 8. Terminology

**Activation hook** — The tiny repository-local `plumbline-router` skill whose presence opts a repository into automatic Plumbline routing.

**Canonical documentation** — Long-lived project-owned documentation describing the repository's actual current design, contracts, capabilities, constraints, and operating state.

**Checkpoint** — A coherent, reviewable, verifiable milestone inside one feature plan.

**Designed work** — Feature work with meaningful product ambiguity, durable contracts, cross-cutting architecture, migration, security, data, or compatibility risk.

**Direct work** — Small, clear, low-risk maintenance that does not need a tracked specification or plan.

**Feature** — The end-to-end product capability or outcome requested by the user.

**Imported source** — A user-supplied design, handoff, attachment, or kickoff prompt that originates outside the active repository.

**Implementation plan** — The single live execution control plane for one feature. It records checkpoint order, dependencies, ownership, progress, evidence, blockers, deviations, and corrections.

**Ready for Acceptance** — The state after implementation, planned verification, independent completion audit, and acceptance-surface preparation are complete, but before user acceptance and final closeout.

**Scoped work** — A localized feature with a clear product outcome but enough implementation breadth to benefit from a worktree and checkpoint plan.

**Specification** — The transient product contract governing an active feature: outcome, scope, behavior, constraints, and acceptance criteria.

**Transient artifact** — An imported source, specification, plan, or execution report that is authoritative only while the feature is active and is removed after accepted closeout.

**Work package** — A bounded assignment delegated to a subagent within a checkpoint. It is not a separate feature, specification, plan, or Git authority.

---

## 9. Operating modes

### 9.1 Installed only

Installing Plumbline must not change repository behavior.

In this state:

- No repository is inspected.
- No skill automatically takes over ordinary prompts.
- No files are created.
- No configuration is changed.
- No agents are installed.
- No plugin conflicts are analyzed.
- No hooks run.

The user may still explicitly invoke `$plumbline` or any public phase skill for one-off use.

### 9.2 Explicit one-off

An explicit invocation provides consent for the current task only.

One-off use may:

- Inspect the current repository.
- Use existing project or global agents.
- Use bounded built-in read-only subagents when useful.
- Create tracked transient artifacts for substantial work.
- Use a managed worktree for scoped or designed implementation.
- Carry a feature through closeout.

One-off use must not:

- Create the repository activation hook.
- Modify `AGENTS.md` for Plumbline activation.
- Initialize or rewrite an agent team without approval.
- Disable competing plugins.
- Leave automatic behavior enabled afterward.

### 9.3 Initialized repository

After explicit `$plumbline-init` and user approval, the local router may automatically classify ordinary repository prompts and enter the appropriate phase.

Automatic behavior remains proportional:

- Direct work remains direct.
- Scoped features use the structured feature flow.
- Designed features begin with shaping or specification.
- Bugs use diagnosis, not feature ceremony by default.
- Explicit user instructions override classification.

---

## 10. Public skill surface

Plumbline exposes namespaced skill names to avoid collisions with other workflow plugins.

| Skill | Purpose | Automatic eligibility |
|---|---|---|
| `$plumbline` | Universal explicit front door; enter at the latest safe phase | Explicit only |
| `$plumbline-init` | Initialize or reassess a repository | Explicit only |
| `$plumbline-shape` | Explore and settle product intent | Router-selected or explicit |
| `$plumbline-spec` | Create or adopt the active feature specification | Router-selected or explicit |
| `$plumbline-plan` | Create the live checkpoint implementation plan | Router-selected or explicit |
| `$plumbline-execute` | Implement and advance the live plan | Router-selected or explicit |
| `$plumbline-diagnose` | Diagnose bugs and regressions | Router-selected or explicit |
| `$plumbline-review` | Perform an independent report-only audit | Router-selected or explicit |
| `$plumbline-closeout` | Reconcile, clean up, and integrate accepted work | Router-selected or explicit |
| `$plumbline-agent-team` | Initialize, audit, retune, or extend project agents | Explicit only |
| `$plumbline-offboard` | Explain and optionally apply repository deactivation cleanup | Explicit only |

User-facing display names may be shorter: Plumbline, Setup, Shape, Specification, Plan, Execute, Diagnose, Review, Closeout, Agent Team, and Offboard.

### 10.1 Universal front door

`$plumbline` must:

1. Assess the prompt, conversation, supplied artifacts, and minimal repository context.
2. Determine the latest safe phase.
3. State the selected phase in one brief sentence.
4. Load only that phase's focused behavior.
5. Ask only blocking product questions.
6. Avoid replaying earlier phases that have already been adequately completed.

Examples:

- A rough product idea routes to Shape.
- A sufficient external design routes to Plan.
- A sufficient design plus execution topology routes to Execute.
- An existing implementation routes to Review.
- A UAT-approved feature routes to Closeout.

### 10.2 Explicit phase precedence

An explicit phase command is evidence that the user intends to enter there.

The phase must be honored unless meaningful progress is impossible without a missing product decision. Nonblocking gaps are resolved through repository research and engineering judgment.

### 10.3 Internal invocation architecture

The implementation must preserve both goals:

- Phase skills are individually invokable.
- Globally installed phase skills do not begin automatically in uninitialized repositories.

The preferred implementation is narrow model-facing phase descriptions that trigger only when selected by the local router, the `$plumbline` front door, or explicit phase invocation. If Codex invocation evaluations show that this is unreliable, use tiny explicit wrappers plus internal phase engines without changing the public command surface.

---

## 11. Repository activation and initialization

### 11.1 Explicit initialization only

The plugin must never initialize itself from an ordinary feature prompt.

The user must explicitly invoke:

```text
$plumbline-init
```

### 11.2 Fresh-thread guard

Initialization performs repository-wide workflow, documentation, agent, and configuration assessment. It must not begin inside a thread containing unrelated active implementation work unless the user explicitly overrides the guard.

Before repository inspection, `$plumbline-init` should detect substantial unrelated active work and respond with a concise warning:

```text
Plumbline initialization may displace useful context from this active task.
Start a fresh task and invoke $plumbline-init there, or reply "continue here"
to proceed in this thread.
```

The guard must not inspect the repository, compact the conversation, or create a handoff before warning.

### 11.3 Read-only assessment first

Initialization begins read-only and identifies:

- Existing `AGENTS.md` or equivalent project instruction files.
- Documentation routers and canonical document ownership.
- Architecture, contracts, capabilities, security, runbooks, and decision records.
- Current specification and plan conventions.
- Build, test, validation, and UAT commands.
- Existing local and global custom agents.
- Multi-agent configuration and managed policy constraints.
- Worktree setup and local dependency requirements.
- Competing workflow controllers and overlapping skills.
- Whether the repository is new, established, weakly documented, or internally contradictory.

### 11.4 Single selectable proposal

Initialization presents one proposal with individually selectable changes. Examples:

- Install the local automatic router.
- Audit or initialize the project agent team.
- Configure worktree propagation for local router and agent files.
- Add or repair lightweight documentation routing.
- Establish canonical documentation for a new project.
- Offer reversible conflict configuration for overlapping workflow plugins.
- Repair an incompatible multi-agent setting.

No change is applied until the user approves the selected items.

### 11.5 Existing repository behavior

For an established project, Plumbline must adopt existing conventions.

It may recommend minimal repairs such as:

- Linking an existing docs router from `AGENTS.md`.
- Adding a missing docs index without relocating content.
- Clarifying which document owns a topic.
- Marking obsolete plans as historical or removing stale active links.
- Resolving duplicated or contradictory canonical statements.

It must not rename, move, merge, or restructure canonical documents without explicit approval.

### 11.6 New project behavior

For a blank or effectively undocumented project, initialization should guide the user through a concise product baseline:

- Purpose.
- Intended users.
- Core outcomes and workflows.
- Priorities.
- Constraints.
- Non-goals.

After the user approves that product baseline, the agent owns the technical baseline: domain language, architecture, contracts, engineering conventions, validation, and an appropriate canonical documentation structure. No second mandatory full-document approval gate is required before implementation, though the user may request review.

The exact documentation tree must be derived from the project. A small utility may need only a few documents. A complex agent runtime may require architecture, capabilities, contracts, security, and runbook areas.

### 11.7 Activation hook

The default automatic-routing footprint is one repository-local skill:

```text
.agents/
└── skills/
    └── plumbline-router/
        └── SKILL.md
```

An optional `agents/openai.yaml` may be added only if Codex invocation metadata requires it.

The router must contain only:

- Confirmation that the repository opted in.
- Direct/scoped/designed classification.
- Phase selection.
- User-override precedence.
- A handoff to the selected plugin-owned phase.

It must not copy the full Plumbline methodology into the repository.

### 11.8 Local ownership and removal

The activation router is untracked by default and added to `.git/info/exclude` when appropriate. Deleting `.agents/skills/plumbline-router/` disables automatic Plumbline behavior for that repository.

### 11.9 Initialization completion

Initialization ends after applying the approved setup and reporting what was changed. It does not immediately begin an unrelated feature implementation. A new task is recommended so Codex reloads skills, agents, and instructions coherently.

---

## 12. Workflow classification

Every initialized-repository prompt receives a lightweight evidence pass, not a full workflow.

### 12.1 Direct path

Use for clear, low-risk work such as:

- Documentation or comments.
- Formatting or copy changes.
- Mechanical renames.
- Small metadata changes.
- Clearly requested configuration defaults.
- Localized obvious fixes.
- Maintenance that does not alter a durable runtime contract.

Default flow:

```text
Inspect → change → targeted validation → report
```

Direct work does not create a specification, plan, kickoff commit, feature worktree, completion audit, or transient cleanup unless the user explicitly requests them or evidence reveals greater complexity.

### 12.2 Scoped feature path

Use for a clear product feature whose implementation is localized enough to avoid a long shaping session but substantial enough to benefit from isolation and checkpoint tracking.

Default flow:

```text
Minimal inspection → concise specification → checkpoint plan → managed worktree
→ kickoff commit → execution → completion audit → acceptance → closeout
```

### 12.3 Designed feature path

Use when product intent or durable consequences require shaping, including:

- Ambiguous user behavior or success criteria.
- Multiple plausible product experiences.
- New domain concepts or invariants.
- Public interface, schema, protocol, or persistent data changes.
- Security, authorization, privacy, migration, concurrency, or compatibility decisions.
- Cross-cutting architectural ownership changes.
- Material cost or service-dependency choices.

Default flow:

```text
Shape → specification → checkpoint plan → managed worktree → kickoff commit
→ execution → completion audit → acceptance → closeout
```

### 12.4 Bug path

Bug reports use Diagnose first. Small repairs may remain on the active checkout with no feature plan. Diagnosis escalates to a scoped or designed feature flow only when the repair becomes substantial or requires new product decisions.

### 12.5 Automatic escalation

When lightweight inspection reveals hidden complexity, Plumbline automatically escalates to the appropriate path, briefly explains the evidence, and asks the first blocking product question when one exists.

---

## 13. Shaping phase

### 13.1 Purpose

Shape converts a concept into shared product understanding. It can be used as a standalone thinking tool and must not assume implementation will follow.

### 13.2 Research-first behavior

Before asking a question, the agent determines whether the answer can be found in:

- Existing code and tests.
- Canonical documentation and decision records.
- Configuration and schemas.
- Relevant repository history.
- Current primary external sources when version-specific or security-sensitive facts materially affect a decision.

Repository facts should not consume user questions.

### 13.3 User question policy

Questions must be one at a time and concern product decisions such as:

- Who the capability is for.
- What the user should accomplish.
- Important behavior and failure experience.
- Scope and non-goals.
- Product tradeoffs among simplicity, flexibility, privacy, speed, cost, and polish.
- Destructive or difficult-to-reverse outcomes.

Each meaningful question includes:

- The agent's recommended answer.
- Credible alternatives.
- Tradeoffs expressed in product terms.
- A default when the user delegates the decision.

The agent should not ordinarily ask the user about module boundaries, schema normalization, adapters, state ownership, test seams, function signatures, or similar technical details.

### 13.4 Completion

Shaping ends when all relevant product branches are resolved sufficiently to support a coherent specification. It does not use a fixed questionnaire and does not open irrelevant branches.

The user may stop after shaping without creating any repository artifact.

---

## 14. Specification phase

### 14.1 Purpose

The specification is the active feature's product contract. It captures why and what, not a line-by-line implementation design.

### 14.2 Inputs

`$plumbline-spec` may synthesize from:

- The current shaping conversation.
- A user-authored design.
- A ChatGPT or Claude handoff.
- An issue description.
- A PDF, Markdown file, document, image, or other attachment.
- An existing repository specification.

Plumbline must not require that it conducted the original shaping.

### 14.3 Sufficiency assessment

The phase quickly separates the input into:

- Confirmed product decisions.
- Engineering proposals.
- Current-state claims.
- Assumptions.
- Acceptance criteria.
- Open product questions.

It reconciles these against current repository evidence. Ordinary technical discrepancies are resolved autonomously. A user question is asked only when a remaining conflict changes product behavior or another difficult-to-reverse consequence.

### 14.4 Imported-source materialization

Source material required for implementation must be available to future sessions, managed worktrees, and subagents.

Plumbline must materialize chat-only or attachment-only requirements into the repository's transient artifact area before execution. It should preserve the original source when safe, reasonably sized, and free of secrets; otherwise it creates a faithful Markdown transcription or assessment with provenance.

Default paths, when the repository has no convention:

```text
docs/specs/<feature>-source.<ext>
docs/specs/<feature>.md
```

The source is normally immutable. The specification may be amended deliberately.

### 14.5 Specification content

A default specification contains:

```markdown
# <Feature> Specification

## Source and Status
## Product Outcome
## Users and Workflows
## Scope
## Non-Goals
## Domain Language and Invariants
## Required Behavior
## Failure and Recovery Behavior
## Compatibility, Data, Privacy, and Security Constraints
## Acceptance Criteria
## Testing and Acceptance Strategy
## Canonical Documentation Impact
## Decisions and Rejected Alternatives
## Assumptions and Residual Questions
```

Sections are included only when relevant. The document must not contain artificially long user-story lists, complete implementation code, or exhaustive file inventories.

### 14.6 Authority and amendment

During implementation:

- The specification governs product outcome, scope, behavior, and acceptance.
- Technical implementation changes usually affect the plan, not the specification.
- Product behavior, scope, or acceptance changes require a specification amendment.
- Product-changing amendments require user approval.
- No acceptance criterion may disappear silently.

### 14.7 Approval behavior

A designed feature produced through Plumbline shaping normally pauses for concise user review of the specification before implementation planning.

A supplied design that the user explicitly asks to plan or implement is treated as already intended for use. Plumbline does not demand redundant approval unless it discovers a blocking product conflict.

---

## 15. Planning phase

### 15.1 Purpose

The implementation plan is the live execution control plane for the complete user-defined feature.

It must be chronological, checkpointable, testable, and resumable. It must not be a code transcript or a collection of microscopic tasks.

### 15.2 Feature integrity

Plumbline must preserve the feature boundary established during shaping or supplied by the user.

Crossing frontend, backend, schema, persistence, security, operations, or documentation boundaries does not create separate features or plans.

The plan may recommend splitting only when the request genuinely contains independent product outcomes with separate acceptance criteria that could be delivered or rejected independently. Technical inconvenience is not sufficient. The user decides whether to split.

### 15.3 Repository research

Before finalizing the plan, Plumbline investigates enough repository context to identify:

- Existing interfaces and module ownership.
- Files and surfaces likely to change.
- Shared contracts and generated outputs.
- Serial dependencies.
- Safe parallel work packages.
- Validation commands.
- Canonical documentation impact.
- Worktree environment requirements.
- UAT constraints.

### 15.4 Checkpoint design

A checkpoint is a meaningful implementation state, not a two-to-five-minute action.

A checkpoint must have:

- A coherent outcome.
- Explicit dependencies.
- Relevant specification coverage.
- Ownership and likely write surfaces.
- Serial or parallel execution topology.
- Targeted runtime protection.
- Verification.
- Canonical documentation impact.
- A checkable completion criterion.

### 15.5 Plan format

Default structure:

```markdown
---
status: active
specification: ../specs/<feature>.md
source: ../specs/<feature>-source.md
current_checkpoint: CP-01
base_commit: <feature base>
---

# <Feature> Implementation Plan

## Feature Outcome
## Global Constraints
## Execution Topology
## Shared Ownership
## Checkpoint Index

## CP-01: <Meaningful milestone>

**Status:** Pending

### Outcome
### Specification Coverage
### Dependencies
### Ownership and Work Packages
### Implementation Notes
### Runtime Protection
### Verification
### Canonical Documentation Impact
### Completion Criterion
### Completion Evidence
### Deviations and Blockers
```

### 15.6 Status model

Checkpoints use:

- `Pending`
- `In Progress`
- `Blocked`
- `Complete`
- `Reopened`
- `Superseded`

A checkpoint may not disappear silently. A superseded checkpoint records why it is no longer required and where its specification coverage moved.

### 15.7 Execution topology

The plan must identify likely parallel and serial work before execution.

Shared contracts, schemas, migrations, lockfiles, generated sources, registries, and other central assets have one owner. Parallel work begins only after dependent shared interfaces are stable.

The plan is a researched forecast, not an immutable guess. Hidden coupling discovered during implementation requires a plan amendment before execution continues under the new topology.

### 15.8 One active set

By default, one implementation worktree contains:

- One active imported source set.
- One active feature specification.
- One active implementation plan.

A second unrelated feature uses another managed worktree. Tightly related additions may share the feature only through explicit user direction and an updated specification.

---

## 16. Kickoff and durable execution memory

### 16.1 Mandatory kickoff commit

Every plan-based feature must create a kickoff commit before substantive production implementation.

The kickoff commit contains:

- Imported source material when applicable.
- The active specification.
- The initial implementation plan.
- Checkpoint dependencies and execution topology.
- Planned verification and canonical documentation impact.

It contains no substantive production implementation.

Direct and no-plan work are exempt.

### 16.2 Dirty-worktree safety

Plumbline must not silently include unrelated pre-existing changes in the kickoff commit. It must not stash, reset, discard, or absorb unrelated work without explicit user direction.

### 16.3 Compaction recovery

After compaction, session change, or handoff, the orchestrator resumes by reading:

1. The active specification.
2. The current plan state.
3. The relevant canonical documents.
4. The repository diff and recent checkpoint commits.

Conversation summaries are supplementary, not authoritative.

### 16.4 Plan updates

The plan is updated:

- When a checkpoint starts.
- When execution topology changes.
- When a blocker appears.
- When a technical deviation is selected.
- When a checkpoint completes.
- When QA or UAT reopens a checkpoint.
- When corrective evidence closes it again.

The plan records state and evidence, not a verbose chronological diary. Git owns chronology.

---

## 17. Execution phase

### 17.1 Orchestrator responsibility

The main thread is the feature orchestrator and sole Git authority.

It owns:

- Specification and plan state.
- Shared contracts.
- Work-package boundaries.
- Subagent dispatch.
- Integration.
- Git staging and commits.
- Checkpoint validation.
- Completion claims.

### 17.2 Subagent work packages

Subagents receive bounded briefs containing:

- Feature context.
- Paths to the active specification, plan checkpoint, and relevant canonical docs.
- Exact deliverable.
- Allowed write set.
- Prohibited files and actions.
- Focused validation.
- Required report content.

Subagents must not receive accumulated conversation history or unrelated prior-task summaries.

### 17.3 Single Git writer

Subagents must not:

- Stage or commit.
- Move `HEAD`.
- Rebase, merge, reset, or stash.
- Switch branches or worktrees.
- Edit the active specification or plan.
- Modify files outside their assigned write set.
- Change shared contracts without ownership reassignment.

The main thread alone integrates and commits.

### 17.4 Parallel execution

Parallel work is encouraged when it saves time and ownership is disjoint.

Parallel implementation is allowed only when:

- File ownership is disjoint.
- Public contract ownership is stable.
- Generated outputs do not collide.
- Dependency and lock files are not shared.
- Validation does not corrupt shared mutable state.
- One package can fail without invalidating another's assumptions.

When ownership is unclear, work is serialized.

An agent requiring an out-of-scope file reports `NEEDS_OWNERSHIP_CHANGE` rather than editing it. The orchestrator pauses affected work, updates the plan, assigns one owner, and resumes only when safe.

### 17.5 Checkpoint gate

Before advancing to the next checkpoint, the main thread:

1. Inspects all returned changes.
2. Confirms ownership compliance.
3. Integrates combined behavior.
4. Runs checkpoint-level validation.
5. Records deviations and evidence.
6. Updates canonical-document impact.
7. Marks the checkpoint complete only when its criterion is met.
8. Creates one coherent checkpoint commit.

### 17.6 Commit policy

Default plan-based history:

1. Kickoff commit.
2. One coherent commit per completed checkpoint.
3. Focused corrective commits for QA or UAT findings.
4. Closeout commit.

Intermediate commits are allowed only when a checkpoint is unusually large or a stable prerequisite deserves separate preservation.

Subagent assignments do not define commit boundaries.

History is preserved by default. Plumbline does not squash or rewrite checkpoint history unless the user or repository convention requests it.

---

## 18. Runtime testing policy

### 18.1 Testing objective

Tests exist to protect valuable runtime behavior against plausible regression. They are not proof that process was followed.

### 18.2 Test-value gate

A new permanent test should normally satisfy all of these:

1. **Runtime contract:** It observes behavior through a stable public interface or meaningful system boundary.
2. **Plausible regression:** A realistic future change could break the behavior while compilation or ordinary checks still pass.
3. **Independent oracle:** Expected behavior comes from the specification, invariant, protocol, or known example rather than repeating the implementation.
4. **Stable seam:** The test survives internal refactoring.
5. **Unique protection:** Existing tests do not already fail for the same regression.
6. **Proportionate cost:** The protection justifies setup, runtime, and maintenance.

### 18.3 Allowed outcomes

The runtime-testing decision may be:

- Add one failing regression test, then implement.
- Extend or parameterize an existing test.
- Rely on existing tests.
- Use type checking, schema validation, parsing, linting, build, or smoke checks.
- Perform focused manual UAT.
- Add no automated test and record why.
- Consolidate or remove redundant touched-area tests.

### 18.4 Default exclusions

Do not add tests solely to freeze:

- Documentation wording.
- Comments.
- Formatting.
- File placement.
- Private helper structure.
- Internal call counts or ordering.
- Literal current configuration defaults.
- Generated output with a trusted generator.
- Manifest values already validated by a parser or schema.

Configuration behavior may deserve tests when precedence, validation, failure handling, or runtime effects are durable contracts.

### 18.5 Bugs

For a bug fix, prefer a failing reproducer first when it exercises a stable runtime seam and provides durable protection. A typo, documentation bug, metadata issue, or transient environmental problem may be verified without a permanent test.

### 18.6 Test portfolio posture

- Test at the highest practical seam.
- Avoid duplicating the same behavior at every layer.
- Do not require one test per function or method.
- Coverage percentage alone does not justify a test.
- Review touched tests for brittleness, duplication, and implementation coupling.

A repository-wide test-suite reduction workflow is outside v1, though `$plumbline-review deep` may be used for a user-requested targeted test audit.

---

## 19. Diagnosis phase

### 19.1 Purpose

Diagnose identifies the demonstrated root cause of a bug or regression before selecting the smallest defensible repair.

### 19.2 Default behavior

- Reproduce or characterize the symptom.
- Trace the current execution path.
- Compare code, tests, configuration, and canonical contracts.
- Form and test focused hypotheses.
- Repair proportionally.
- Add regression protection only when valuable.

### 19.3 Git history

History is a bounded diagnostic instrument, not a mandatory archaeology phase.

Use history when:

- The user reports that behavior previously worked.
- A known timeline, path, symbol, contract, or feature term can focus the search.
- A narrow lookup may distinguish competing root-cause hypotheses.
- A deleted historical specification or reopened checkpoint may clarify intended behavior.

Do not:

- Scan the entire repository history.
- Assume the latest commit caused the defect.
- Run automatic `git bisect`.
- Restore historical transient artifacts into the working tree by default.
- paste large logs and diffs into the main thread.

Current code and the user's observed timeline remain the primary evidence.

### 19.4 Escalation

Small bug fixes remain direct. A repair escalates to scoped or designed feature flow only when it materially changes product behavior, architecture, data, or implementation breadth.

---

## 20. Independent review

### 20.1 Review role

`$plumbline-review` is a report-only, independent audit. It does not implement fixes unless the user separately requests a repair flow after the report.

### 20.2 Automatic completion audit

Any feature with an active specification or plan receives a fresh `qa-auditor` completion audit before Ready for Acceptance, unless the user explicitly overrides that default.

Direct and no-plan work do not automatically spawn QA. The user may request a second opinion for any change, including a sticky bug implemented directly on `main`.

### 20.3 Standard and deep modes

**Standard audit** is the default:

- Read specification, plan, diff, canonical docs, and existing evidence first.
- Inspect implementation and tests.
- Run only a small number of targeted non-mutating probes when they resolve a material evidence gap.
- Do not rerun the full implementation closeout.

**Deep audit** is explicit or proposed with user approval:

- Trace a broader blast radius.
- Inspect more adjacent callers and contracts.
- Run additional targeted verification.
- Remain report-only and repository-read-only.

### 20.4 Adversarial QA posture

The default QA auditor must be hard to please but easy to convince with strong evidence.

It should attempt to falsify readiness by looking for:

- Omitted acceptance criteria.
- Thin or nominal implementations.
- Edge cases and partial failure.
- Blast-radius regressions.
- Invalid assumptions.
- Security, privacy, concurrency, and data-integrity risks.
- Unjustified complexity, duplication, coupling, and shallow abstractions.
- Low-sensitivity, redundant, or implementation-coupled tests.
- Canonical documentation drift.

It must not manufacture findings, enforce personal style, demand tests without value, or propose broad refactors without a concrete failure path.

### 20.5 Independent probes

The auditor may run focused existing tests, type checks, static analysis, import-origin probes, or minimal commands only to settle a specific uncertainty.

It must not:

- Write tests.
- Edit code or docs.
- Update snapshots.
- Run auto-fixing tools.
- Install dependencies.
- Mutate shared virtual environments.
- Run migrations.
- Start persistent services.
- Run the full suite merely for ceremony.

When evidence requires a costly environment, the auditor reports what remains unverified and what would settle it.

### 20.6 Planned-feature coverage matrix

The completion audit maps:

```text
source requirement
→ specification acceptance criterion
→ implementation checkpoint
→ diff evidence
→ verification or UAT evidence
→ canonical documentation impact
```

Every acceptance criterion and every non-superseded checkpoint must be accounted for.

### 20.7 Verdicts

- `PASS`
- `PASS_WITH_RESIDUAL_RISK`
- `CHANGES_REQUIRED`
- `INCONCLUSIVE`

A `CHANGES_REQUIRED` report returns to the main thread. No automatic repair begins without user instruction or prior explicit "review and fix" authority.

---

## 21. QA and UAT corrections

When QA or UAT invalidates a completed checkpoint:

1. Reopen the checkpoint in the existing plan.
2. Record the finding, source, affected acceptance criteria, blast radius, and required correction.
3. Perform the focused correction.
4. Run targeted verification.
5. Create a new corrective commit.
6. Record corrective evidence.
7. Mark the checkpoint complete again only when justified.

Do not amend or rewrite the earlier checkpoint commit to hide the defect.

When one finding spans several checkpoints, add one bounded corrective checkpoint to the same plan rather than creating a new feature plan.

The feature cannot return to Ready for Acceptance while any checkpoint is `Blocked` or `Reopened`.

---

## 22. Managed worktrees and environment readiness

### 22.1 Worktree ownership

Plumbline uses Codex-managed worktrees and Handoff. It does not run its own worktree creation, registry, or cleanup system.

Plumbline must not:

- Create repository-local `.worktrees/` directories.
- Run custom `git worktree add` or `git worktree remove` as its normal flow.
- Invent a second worktree naming or cleanup convention.
- Modify `.gitignore` solely for plugin-owned worktrees.

### 22.2 Isolation policy

- Scoped and designed feature work uses a managed worktree by default.
- Direct work and small bug fixes remain in the active checkout when safe.
- Larger or uncertain bug repairs may escalate to a worktree.
- Explicit user instruction to stay in the current checkout overrides the default.

### 22.3 Thin worktree principle

A managed worktree should be a thin source checkout attached safely to shared local infrastructure, not a complete clone of large models, packages, or environments.

Preference order:

1. Reference shared resources through configuration or environment variables.
2. Invoke shared tools or interpreters by absolute path.
3. Use a repository-owned setup script for a safe link.
4. Copy small ignored configuration through `.worktreeinclude`.
5. Create an isolated dependency environment only when sharing is unsafe or dependencies change.

### 22.4 Safe symlink policy

Symlinks are permitted for appropriate shared resources when:

- The link node is inside the disposable worktree.
- The target is stable and outside Codex's managed worktree root.
- The target exists and matches the expected resource type.
- Setup is idempotent.
- Existing real files are never overwritten.
- Cleanup removes only the link node and never follows the target.
- No reverse link points from shared storage into the worktree.

Large read-only model directories are better exposed through configuration when possible.

### 22.5 Shared virtual environments

A shared Python `.venv` may be borrowed when practical, but Plumbline must:

- Prefer invoking its interpreter by absolute path.
- Avoid dependency-mutating commands against the shared environment.
- Verify that relevant project imports resolve from the current worktree rather than the main checkout.
- Require an isolated environment when dependencies change or import resolution is unsafe.

### 22.6 Worktree readiness

Before planned implementation, Plumbline performs a small readiness check:

- Required toolchain is available.
- Essential local configuration is present.
- Shared resources are reachable.
- Project source resolves from the worktree.
- The likely targeted validation command runs.
- No obviously broken baseline blocks the feature.

It does not reinstall the entire repository or run the full suite by default.

### 22.7 Worktree propagation

Untracked local router and agent files may be propagated through the repository's existing setup mechanism. When no mechanism exists, initialization may offer an approved `.worktreeinclude` update for:

```text
.agents/skills/plumbline-router/**
.codex/agents/*.toml
```

Tracked files must not be listed. Existing worktrees are not assumed to update retroactively.

---

## 23. Acceptance and UAT

### 23.1 Ready for Acceptance

Before entering Ready for Acceptance, Plumbline must:

- Complete or supersede every plan checkpoint.
- Run the planned targeted verification.
- Complete the independent QA audit.
- Reconcile implementation against the specification.
- Update affected canonical documentation to the resulting implemented state.
- Prepare the smallest useful UAT surface.
- State what remains human-observable.

### 23.2 Minimal acceptance surface

The user should not have to reconstruct how to run a feature from an incomplete worktree.

The plan identifies the smallest executable surface that proves the product outcome, such as:

- A focused backend service.
- A single frontend route or component harness.
- A command-line scenario.
- A local integration adapter.
- A scripted conversation.
- A targeted runtime using shared models.
- The full product only when necessary.

The agent provides exact launch and product-level validation steps.

### 23.3 Worktree versus Local UAT

Preferred order:

1. Worktree UAT when the surface is already available or cheap.
2. Handoff to Local when the runtime is singleton, hardware-bound, exceptionally heavy, or unsafe to bridge.
3. For low-blast-radius work, integrate and validate in the normal local environment when the user accepts that tradeoff.

Plumbline should not defend an ideal deployment practice so aggressively that it blocks practical local development.

### 23.4 Acceptance authority

The feature is accepted when the user:

- Completes UAT successfully.
- Explicitly approves without manual UAT.
- Instructs Plumbline to integrate or merge.

"Looks good, merge it" is sufficient. No second ceremonial confirmation is required.

---

## 24. Canonical documentation

### 24.1 Repository-defined structure

Plumbline does not require fixed files such as `product.md`, `domain.md`, or `architecture.md` in established repositories.

It discovers which documents own:

- Product behavior.
- Domain language and invariants.
- Architecture and module ownership.
- Contracts and schemas.
- Capabilities.
- Security and trust boundaries.
- Operations and runbooks.
- Engineering and validation conventions.
- Durable decisions.

### 24.2 Lightweight routing

`AGENTS.md` remains a lightweight operational router containing high-level project rules, essential commands, and a pointer to the documentation index. It must not become the project encyclopedia.

A docs index should tell agents what to read for a task and distinguish canonical current-state documents from active transient implementation artifacts.

### 24.3 Canonical versus transient

Canonical docs:

- Describe the repository's actual current state.
- Are maintained in place.
- Use present-tense system truth.
- Contain enough technical detail for future agents to reason correctly.
- Do not track every commit, checkpoint, or temporary implementation state.

Specifications and plans:

- Govern an active implementation.
- May describe target behavior not yet implemented.
- Are not canonical.
- Are removed after accepted closeout.

Git history owns chronology.

### 24.4 Documentation impact

Plans identify concrete canonical-document impact. "Update docs" is not a generic task.

Valid outcomes include:

```text
Update docs/contracts/session-lifecycle.md because reconnect behavior changed.
```

or:

```text
No canonical documentation change: public behavior, ownership, contracts,
and operations remain unchanged.
```

### 24.5 Consistency gate

A change is not cleanly complete while Plumbline knowingly leaves an authoritative document describing obsolete behavior, ownership, contracts, or operating procedures.

Explicit user override may still proceed, but Plumbline must report the unresolved drift and must not claim a clean closeout.

### 24.6 Conflict handling

When code and canonical docs disagree, Plumbline investigates rather than assuming one is correct:

- Check specification, decisions, tests, configuration, and focused history.
- Determine whether code drifted, docs became stale, or both are incomplete.
- Correct the implementation, documentation, or both.
- Create a durable decision record only when future agents need the rationale.

### 24.7 No documentation tests

Plumbline must not create tests that freeze prose, headings, or literal documentation content. Documentation is maintained through review and consistency checks.

### 24.8 Agent drift

Closeout performs a lightweight, silent agent-drift check. It recommends `$plumbline-agent-team audit` only when a concrete mismatch exists, such as a removed docs path, deprecated domain term, materially changed technical surface, or conflicting authority statement.

No generic audit reminder is emitted.

---

## 25. Closeout

### 25.1 Trigger

Closeout begins after user acceptance or an explicit integration instruction.

### 25.2 Closeout steps

1. Recheck changes since the completion audit.
2. Confirm implementation still satisfies the specification.
3. Reconcile final canonical documentation.
4. Confirm no lasting truth exists only in the transient source, specification, or plan.
5. Remove imported source artifacts, specification, and plan.
6. Remove active-document routing entries.
7. Run final proportional verification.
8. Confirm no local-only environment paths, links, secrets, or borrowed resources were committed.
9. Create the closeout commit.
10. Integrate through the user-requested Codex Handoff or Git flow.
11. Leave managed-worktree retirement to Codex.

### 25.3 Final working tree

After closeout, the working tree contains:

- Current code.
- Valuable tests and validation.
- Current canonical documentation.
- Durable decision records when warranted.

It does not contain completed feature specifications, implementation plans, or imported kickoff sources.

### 25.4 Historical recoverability

The deleted artifacts remain available in Git through the kickoff and checkpoint history. Plumbline preserves that history by default.

---

## 26. Project agent team

### 26.1 Default location and ownership

Project agents live in:

```text
.codex/agents/*.toml
```

They are untracked by default and added to `.git/info/exclude` where appropriate. They are user-owned and remain useful without Plumbline.

### 26.2 Default archetypes

Plumbline ships quality archetypes for:

- `researcher`
- `backend-architect`
- `frontend-architect`
- `implementer`
- `qa-auditor`

The repository receives only roles that provide real value. A small project may need three. A security-sensitive project may add a specialist.

### 26.3 Repository adaptation

Generated or refreshed agents contain:

- Stable repository vocabulary.
- Broad actual technical surfaces relevant to selection.
- Canonical-document routing.
- Role boundaries and exclusions.
- Evidence and output expectations.

They must not embed:

- Exhaustive file inventories.
- Mutable ownership maps.
- Temporary migration state.
- Active specification target state.
- Long canonical-document excerpts.

The listed surfaces are representative, not exhaustive. A backend architect may inspect adjacent frontend contracts when necessary to assess ownership or blast radius.

### 26.4 User-controlled operating profile

Agent TOMLs preserve or ask for:

- Model slug.
- Reasoning effort.
- Sandbox mode.
- Tool and Model Context Protocol access.
- Cost-versus-quality preference.
- Useful personal behavior.

Plumbline never silently replaces a valid user-selected model or reasoning level.

### 26.5 Agent-team operations

`$plumbline-agent-team` supports:

- Initialize.
- Audit.
- Retune.
- Add a specialist.

Initialization includes the same workflow as a selectable part of `$plumbline-init`; the user does not need to invoke a second command.

### 26.6 Hybrid refresh policy

For existing agents:

- Preserve identity, model, effort, sandbox, permissions, and healthy custom behavior.
- Surgically patch healthy role definitions.
- Replace the instruction body only when stale repository truth and obsolete workflow rules are too entangled.
- Show the proposed diff before writing.

### 26.7 Capability audit

Agent-team setup checks:

- `features.multi_agent` availability.
- `agents.max_depth` and thread settings.
- Managed policy restrictions.
- Project and global role overlap.
- TOML validity.
- Model and sandbox suitability.
- Worktree propagation.
- Actual role discovery through a bounded smoke test.

Configuration changes are proposed precisely and require approval. Missing settings that already use healthy defaults are not written.

### 26.8 Runtime selection order

Plumbline prefers:

1. Matching project-local custom agent.
2. Matching personal custom agent.
3. Bounded built-in read-only agent for research or review.
4. Main-thread execution when no safe custom implementer exists.

Agent-team setup remains optional. One-off Plumbline work must degrade gracefully when subagents are disabled.

### 26.9 QA archetype

The default QA agent is independent, adversarial, evidence-bound, report-only, and read-only with permission to run targeted non-mutating probes. It must not act as an implementer.

---

## 27. Workflow-plugin conflict management

### 27.1 Conflict audit

Initialization distinguishes:

- Complementary skills.
- Adjacent disciplines.
- Competing testing or review policies.
- Competing workflow controllers.

A plugin such as Superpowers conflicts materially when it also owns feature discovery, planning, TDD, worktrees, subagent execution, review, and branch finishing.

### 27.2 Recommendation and patch

Plumbline recommends one primary workflow owner and offers a reversible configuration patch that disables overlapping automatic skills. It does not uninstall the other plugin or apply changes without approval.

The proposal must show:

- Current configuration.
- Proposed values.
- Behavior that stops.
- Useful skills that remain available explicitly.
- Rollback instructions.
- Any session hook or repository instruction that requires separate handling.

### 27.3 More is not better

Initialization should explain succinctly that installing multiple overlapping orchestration systems increases context pressure and contradictory behavior. It should not warn about unrelated specialist plugins.

---

## 28. Offboarding

### 28.1 Single kill switch

Removing:

```text
.agents/skills/plumbline-router/
```

stops automatic Plumbline behavior for the repository.

### 28.2 `$plumbline-offboard`

The offboarding skill is explicit and read-only by default. It reports:

- The activation hook to remove.
- Plumbline-specific instruction blocks.
- Competing-plugin settings that remain disabled.
- Optional agent files and propagation entries.
- Active transient artifacts that need intentional handling.
- Project improvements that should usually be preserved.

It may apply selected cleanup only after approval.

### 28.3 Preserve by default

Offboarding preserves:

- Canonical project documentation.
- Project-local agents.
- Generic environment and worktree setup.
- UAT launch actions.
- Valuable tests and validation improvements.
- Source code and Git history.

### 28.4 No uninstall state machine

Plumbline does not maintain a complex installation manifest or automatic rollback engine. Clearly namespaced changes use visible markers where inserted into shared files. Manual removal instructions remain documented for users who uninstall the plugin before running offboard.

---

## 29. Plugin packaging and presentation

### 29.1 Codex-native package

Plumbline is a first-class skills-only Codex plugin.

Required structure:

```text
plumbline/
├── .codex-plugin/
│   └── plugin.json
├── skills/
│   ├── plumbline/
│   ├── plumbline-init/
│   ├── plumbline-shape/
│   ├── plumbline-spec/
│   ├── plumbline-plan/
│   ├── plumbline-execute/
│   ├── plumbline-diagnose/
│   ├── plumbline-review/
│   ├── plumbline-closeout/
│   ├── plumbline-agent-team/
│   └── plumbline-offboard/
├── assets/
├── README.md
├── CHANGELOG.md
├── LICENSE
└── CONTRIBUTING.md
```

Only `plugin.json` belongs under `.codex-plugin/`. Skills, references, templates, and assets remain at the plugin root.

### 29.2 No hooks or connector surface in v1

Plumbline v1 contains no session hooks, browser extensions, connectors, or bundled MCP server. This keeps installation inert and permissions understandable.

### 29.3 Skill metadata

Each public skill includes `agents/openai.yaml` for:

- Display name.
- Short description.
- Iconography where useful.
- Brand color.
- Default prompt.
- Explicit invocation policy.

Descriptions must be short and branch-specific. Generic workflow triggers belong only in the repository-local router.

### 29.4 Plugin manifest

The manifest includes:

- Stable `plumbline` identifier.
- Semantic version.
- Accurate product description.
- Author, repository, homepage, license, and keywords.
- `skills: "./skills/"`.
- Polished interface metadata.
- Composer icon and logo.
- Starter prompts.
- Screenshots before public release.
- Only capabilities actually required.

### 29.5 Plugin-browser experience

The plugin must:

- Appear correctly in Codex plugin browsing surfaces.
- Be installable through a configured marketplace.
- Be enableable and disableable as one unit.
- Expose individual readable skills.
- Require a new task/session after installation or update.
- Avoid custom scripts that separately copy skills into user skill directories.
- Avoid global agent installation during plugin install.

### 29.6 Branding

The visual language should use a simple plumb-line or plumb-bob motif that remains legible at small icon sizes and communicates alignment rather than enforcement. Final palette and artwork are implementation details, but the result must look intentional in the plugin browser rather than like a repackaged Superpowers overlay.

---

## 30. Context-efficiency requirements

### 30.1 No global bootstrap

There is no Plumbline equivalent to `using-superpowers` and no "1% chance" invocation rule.

### 30.2 Router size

The repository router should fit in a single small `SKILL.md`, target under 4 KB, and contain no detailed phase methodology.

### 30.3 Phase skill size

Each phase `SKILL.md` should contain only the common path, completion criterion, and pointers to branch-specific references. Target approximately 500–1,200 words per phase before references; shorter is preferred when behavior remains reliable.

### 30.4 Progressive disclosure

Examples of branch references:

- Plan execution topology.
- Runtime test-value gate.
- Shared-resource worktree safety.
- Imported artifact handling.
- Standard versus deep QA.
- Existing-project versus new-project initialization.
- Agent archetype generation.

A reference is loaded only when its branch is reached.

### 30.5 Single source of doctrine

Rules such as test value, worktree safety, QA evidence, and agent refresh must have one authoritative home. Other skills point to or invoke that behavior rather than restating it.

### 30.6 Subagent context

Subagents receive file-backed briefs and return concise reports. Large diffs, logs, exploration transcripts, and accumulated history should be handed off as files rather than pasted into the main thread.

### 30.7 Direct-path target

A direct edit in an initialized repository should require only the local router and ordinary repository context. It must not load shaping, planning, testing, worktree, review, and closeout instructions.

---

## 31. Migration from `superpowers-personal`

### 31.1 Retire

The following concepts are removed as top-level runtime controllers:

| Current element | Plumbline treatment |
|---|---|
| `using-superpowers` | Remove entirely; no session bootstrap |
| `agent-routing` | Replace with native agent descriptions and bounded delegation policy |
| `using-git-worktrees` | Remove; use Codex-managed worktrees and Handoff |
| `test-driven-development` | Replace with runtime-value testing inside Execute and Diagnose |
| `writing-plans` | Replace with checkpoint plans, not code transcripts |
| `subagent-driven-development` | Fold into Execute orchestration |
| `executing-plans` | Fold into Execute |
| `dispatching-parallel-agents` | Fold into plan topology and Execute ownership rules |
| `requesting-code-review` | Replace with `$plumbline-review` |
| `receiving-code-review` | Replace with explicit post-audit repair behavior |
| `finishing-a-development-branch` | Replace with Closeout and harness-native integration |
| custom agent installer scripts | Remove |
| global default agent copying | Remove |
| repository override templates | Replace with agent archetype generation/audit |

### 31.2 Preserve and simplify

| Current strength | Plumbline destination |
|---|---|
| Brainstorm before ambiguous work | Shape |
| Systematic diagnosis | Diagnose, lighter and current-state first |
| Evidence before completion | Execute, Review, and Closeout |
| Isolated subagent context | Bounded work packages |
| Independent review | Adversarial QA audit |
| Verification commands | Checkpoint evidence and Ready for Acceptance |
| Git history | Kickoff, checkpoint, correction, and closeout commits |

### 31.3 Installer cleanup

The existing PowerShell and shell installers that copy skills and agents into several global locations must be removed. Plugin distribution and enablement are owned by Codex's plugin browser and marketplace.

### 31.4 Agent migration

Existing backend, frontend, researcher, implementer, and QA TOMLs are audited using the hybrid refresh policy. Hardcoded repository facts and old Superpowers ceremony are removed; user model and cost settings are preserved.

### 31.5 License and attribution

Implementation must retain applicable license notices and attribution for any text or code copied from upstream projects. Plumbline should synthesize principles rather than wholesale-copying large prompts when a smaller original design is clearer.

---

## 32. Safety and integrity requirements

- Never commit secrets from imported attachments, `.env` files, agent TOMLs, or local configuration.
- Never delete a shared symlink target during worktree cleanup.
- Never mutate a shared dependency environment during ordinary borrowed-environment use.
- Never mix unrelated dirty changes into feature commits without approval.
- Never disable another plugin without explicit approval.
- Never claim clean closeout with known canonical-doc drift.
- Never allow a QA auditor to silently implement fixes.
- Never let two parallel implementers own the same file, contract, generated output, migration sequence, lockfile, or mutable test resource.
- Never drop a specification requirement because it is inconvenient.
- Never convert an accidental implementation choice into canonical truth without investigation.
- Never create repository activation during a one-off explicit invocation.
- Never perform broad destructive Git operations as part of diagnosis or offboarding without explicit intent.

---

## 33. Acceptance criteria for Plumbline v1

### Installation and activation

1. Installing the plugin creates no repository files and does not automatically invoke Plumbline in an uninitialized repository.
2. The plugin appears in the Codex plugin browser with complete metadata, iconography, starter prompts, and enable/disable controls.
3. `$plumbline` works as a one-off in an uninitialized repository and leaves automatic routing disabled afterward.
4. `$plumbline-init` applies the fresh-thread guard before repository inspection.
5. Initialization presents one selectable proposal and performs no mutation before approval.
6. An initialized repository contains only the small local router by default.
7. Removing the router directory disables automatic routing.

### Routing and phase entry

8. A small config or docs change remains direct and produces no spec, plan, worktree, or QA ceremony.
9. A rough feature concept routes to Shape.
10. A sufficient external design routes to Plan without replaying a full grill.
11. A sufficient plan routes to Execute.
12. An existing implementation routes to Review when requested.
13. Explicit phase invocation overrides automatic routing and asks only blocking questions.
14. Uninitialized repositories do not receive automatic phase invocation from globally installed skill descriptions.

### Shaping and product autonomy

15. Shape researches repository facts before asking the user.
16. Shape asks one product question at a time and includes a recommendation.
17. Shape does not ask the user to decide ordinary architecture or implementation details.
18. Shape may stop without creating artifacts.

### Specifications and plans

19. Imported chat or attachment requirements are materialized into tracked transient artifacts before long-running execution.
20. Every plan-based feature has one specification and one live plan.
21. Plans use meaningful checkpoints, not micro-tasks or separate frontend/backend plans.
22. The plan records serial dependencies, parallel ownership, verification, and canonical-doc impact.
23. A kickoff commit exists before production implementation.
24. After simulated compaction or a new session, execution resumes correctly from the specification, plan, and Git state.
25. Checkpoint status and evidence are updated before advancing.
26. QA or UAT defects reopen the affected checkpoint and produce a corrective commit.

### Subagents and Git

27. The main thread is the only Git writer.
28. Parallel implementers have disjoint write sets and cannot move Git state.
29. Ownership expansion pauses affected work and updates the plan.
30. One coherent checkpoint commit is created after integration and validation.
31. Git history is preserved by default through closeout.

### Testing and review

32. Direct config or documentation changes do not receive synthetic permanent tests.
33. New tests satisfy the runtime-value gate or the plan records another verification choice.
34. Planned features receive an independent standard QA audit before Ready for Acceptance unless explicitly overridden.
35. QA is report-only and adversarial without manufacturing findings.
36. QA can run targeted non-mutating probes but does not repeat the full closeout suite or write tests.
37. `$plumbline-review` can audit a no-plan bug fix on the active checkout.
38. Deep review requires explicit invocation or user approval.

### Worktrees and UAT

39. Scoped and designed features default to Codex-managed worktrees.
40. Direct work and small fixes may remain in the active checkout.
41. Worktree setup can borrow large models, caches, and environments without copying the full repository payload.
42. Shared virtual-environment use verifies imports resolve from the worktree.
43. Plumbline does not create or remove its own worktrees.
44. UAT uses the smallest useful surface and may hand off to Local when practical.
45. Low-risk work may be integrated and validated in Local when the user accepts the tradeoff.

### Documentation and closeout

46. Established documentation structures are adopted rather than replaced.
47. New projects receive an appropriate baseline only after product approval.
48. Canonical docs describe current state and do not become commit diaries.
49. Known canonical drift blocks a clean closeout claim unless the user explicitly overrides and accepts the residual issue.
50. Accepted closeout deletes imported source, specification, and plan from the final working tree.
51. Deleted artifacts remain recoverable in Git history.
52. Offboarding preserves canonical docs, agents, and useful tooling by default.

### Agent team

53. Initialization can audit, refresh, or create a project-local agent team as a selectable option.
54. Existing model slugs, reasoning levels, sandboxes, and useful preferences are preserved by default.
55. Generated agents reference canonical docs rather than embedding mutable architecture truth.
56. Agent-team setup detects disabled multi-agent configuration and proposes an exact approved patch.
57. A bounded smoke test proves project-agent discovery without modifying the repository.
58. Agent-drift recommendations appear only for concrete, significant drift.

### Context and polish

59. Ordinary direct work does not load unrelated phase skills.
60. The local router remains small and contains no full workflow doctrine.
61. Phase bodies use progressive disclosure and avoid duplicated rules.
62. No custom installer duplicates plugin skills into global skill folders.
63. No session hook activates Plumbline.
64. The README explains installed-only, one-off, initialized, and offboarding modes in user-facing language.

---

## 34. Evaluation scenarios

Implementation must include behavioral evaluations for at least these scenarios:

1. **Dormant install:** "Add a config value" in an uninitialized repo does not invoke Plumbline automatically.
2. **One-off shape:** `$plumbline-shape` explores an idea and stops without repository mutation.
3. **One-off imported design:** `$plumbline` receives a design attachment and routes directly to Plan.
4. **Fresh-thread guard:** Init invoked during unrelated active implementation stops before inspection.
5. **Established docs:** Init recognizes an AiriAI-like `architecture/`, `capabilities/`, `contracts/`, `runbooks/`, and `security/` structure and does not replace it.
6. **New project:** Init obtains product approval, then scaffolds an appropriate minimal canonical baseline.
7. **Direct edit:** A documentation typo remains direct.
8. **Hidden complexity:** A seemingly small authentication config change reveals a durable security behavior and escalates with one product-level question.
9. **No re-grill:** A sufficient Claude handoff proceeds to Plan with a compact assessment.
10. **Kickoff durability:** Feature source/spec/plan are committed before code.
11. **Compaction recovery:** A simulated new session resumes the correct checkpoint without relying on chat history.
12. **Parallel ownership:** Frontend and backend work run concurrently only after the shared contract is stable.
13. **Ownership collision:** A subagent requesting a shared contract change stops and reports ownership expansion.
14. **Testing restraint:** A default configuration change does not receive a literal-value test.
15. **Useful regression test:** A runtime reconnect bug receives one stable regression test at the highest practical seam.
16. **Completion gap:** QA detects an acceptance criterion absent from the diff despite all recorded tests passing.
17. **Sticky bug review:** `$plumbline-review` audits a no-plan main-branch fix without manufacturing a spec.
18. **Targeted QA probe:** Auditor reruns one relevant existing test and does not run the full suite.
19. **UAT correction:** A failed UAT reopens a checkpoint and appends a corrective commit.
20. **Heavy local runtime:** Worktree verification uses shared models and Handoff to Local for UAT.
21. **Canonical drift:** Closeout detects a stale contract document and updates it before clean completion.
22. **Transient cleanup:** Accepted closeout removes spec and plan while Git can still recover them.
23. **Agent audit:** Existing AiriAI-style TOMLs are refreshed without changing model slugs.
24. **Conflict detection:** Superpowers overlap is explained and a reversible disable proposal is offered but not applied.
25. **Kill switch:** Removing the local router stops automatic behavior while phase skills remain explicitly usable.

---

## 35. Implementation constraints and technical validation

These are implementation decisions, not unresolved product questions:

1. Validate the exact Codex behavior for a local router invoking phase skills whose implicit invocation is disabled. Use narrow implicit phase engines or wrapper/engine pairs only if required.
2. Validate the minimum router file set. Prefer one `SKILL.md`; add `agents/openai.yaml` only when necessary.
3. Validate local skill and custom-agent propagation into newly created managed worktrees.
4. Validate how plugin-specific skill disabling and competing-plugin configuration are represented in the current Codex configuration schema.
5. Validate that project-local agent discovery and model selection can be smoke-tested without repository mutation.
6. Validate Windows and Unix behavior for safe borrowed-resource links and path resolution.
7. Define a robust method for checking that shared Python environments import project source from the active worktree.
8. Define file-size and secret-safety handling for imported binary source attachments.
9. Build invocation evaluations before finalizing descriptions. The router must not select several phases simultaneously.
10. Use current official Codex plugin and skill schemas at implementation time rather than assuming the predecessor manifest remains valid.

None of these require additional product input unless validation reveals that the agreed user experience cannot be implemented with current Codex capabilities.

---

## 36. Proposed implementation sequence after approval

The implementation plan should organize work into a small number of coherent checkpoints, likely:

1. **Plugin skeleton and brand:** Manifest, marketplace, assets, metadata, public skill shells, and development installation.
2. **Routing and activation:** Universal front door, local router generation, dormant behavior, initialization, and offboarding.
3. **Feature artifacts:** Shape, Spec, Plan, tracked source handling, kickoff commit, checkpoint state, and compaction recovery.
4. **Execution and worktrees:** Orchestration, bounded subagents, single Git writer, parallel ownership, environment readiness, and UAT surfaces.
5. **Testing, diagnosis, review, and closeout:** Runtime-value testing, adversarial QA, corrections, canonical reconciliation, and cleanup.
6. **Agent team:** Archetypes, audit/refresh, model preservation, config checks, and worktree propagation.
7. **Migration and validation:** Superpowers-personal mapping, conflict audit, scenario evaluations, documentation, and packaging polish.

The final implementation plan must research the actual repository before committing to these boundaries. This list is an umbrella sequence, not a mandate to create separate product features.

---

## 37. Review status

Approved by the user on 2026-07-11 for implementation planning and handoff.

No additional product-level blocker emerged during review. The remaining uncertainties are Codex implementation mechanics and evaluation details listed in Section 35. They should be resolved during implementation without reopening product shaping unless they make the agreed interaction model infeasible.

The companion implementation authority is `plumbline-implementation-handoff-plan.md`.

---

## 38. Reference material

Design influences and platform constraints were informed by:

- Matt Pocock, `mattpocock/skills`: https://github.com/mattpocock/skills
- Obra / Prime Radiant, `obra/superpowers`: https://github.com/obra/superpowers
- OpenAI Codex skills documentation: https://learn.chatgpt.com/docs/build-skills
- OpenAI Codex plugin documentation: https://learn.chatgpt.com/docs/plugins
- OpenAI Codex plugin authoring documentation: https://learn.chatgpt.com/docs/build-plugins
- OpenAI Codex subagent documentation: https://learn.chatgpt.com/docs/agent-configuration/subagents
- OpenAI Codex worktree documentation: https://learn.chatgpt.com/docs/environments/git-worktrees
- OpenAI Codex `AGENTS.md` documentation: https://learn.chatgpt.com/docs/agent-configuration/agents-md
- OpenAI Codex configuration reference: https://learn.chatgpt.com/docs/config-file/config-reference

