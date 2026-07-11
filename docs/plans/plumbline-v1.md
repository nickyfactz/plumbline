---
status: active
feature: Plumbline v1
specification: docs/specs/plumbline-v1.md
source: docs/source-provenance.md
base_commit: 5ed0796
current_checkpoint: CP-08
last_verified_commit: fdf652c
ready_for_acceptance: false
---

# Plumbline v1 Implementation Handoff Plan

**Status:** Ready for implementation handoff  
**Plan version:** 1.0  
**Date:** 2026-07-11  
**Governing specification:** `plumbline-design-spec-approved.md`  
**Target:** A new standalone, Codex-native Plumbline plugin repository  
**Feature boundary:** Deliver Plumbline v1 as one complete plugin, not as separate frontend/backend-style micro-projects  
**Expected executor:** A fresh Codex task with repository write access, current official Codex documentation, and the ability to use bounded subagents

---

## 1. Handoff contract for the implementing agent

This plan and the approved design specification are the durable authorities for building Plumbline v1.

Use them as follows:

1. **The specification owns product intent and acceptance.** Do not reopen settled workflow decisions merely because another implementation would be easier.
2. **This plan owns implementation order, content targets, and validation.** Amend it when repository or Codex platform evidence invalidates an implementation assumption.
3. **The referenced repositories are design sources, not drop-in dependencies.** Synthesize their strongest behaviors into Plumbline's lighter model. Do not recreate either repository wholesale.
4. **Current official Codex behavior wins over historical assumptions.** Revalidate plugin, skill, subagent, worktree, and configuration mechanics at implementation time.
5. **Ask the user only if a platform limitation makes an agreed product behavior infeasible or if release identity cannot be inferred from the new repository.** Resolve ordinary architecture, file layout, prompt wording, evaluation design, and implementation details autonomously.
6. **Keep this as one feature plan.** The checkpoints below are coherent delivery milestones inside Plumbline v1, not separate specifications or independent product features.
7. **The main thread is the sole Git writer.** Subagents may research, draft, or edit disjoint assigned files, but they must not stage, commit, rebase, reset, stash, switch branches, or edit the active specification and plan.
8. **Create the kickoff commit before substantive plugin implementation.** The new repository must begin with the approved specification, this plan, source provenance, and initial execution state tracked in Git.

When implementation starts, copy the approved specification and this plan into the new repository's transient artifact convention. For a blank repository, use:

```text
docs/specs/plumbline-v1.md
docs/plans/plumbline-v1.md
```

These files are active execution authorities while Plumbline is being built. They should be removed only after Plumbline itself has passed acceptance and the repository's long-lived documentation contains the resulting truth.

---

## 2. Required handoff inputs

The implementation task should receive these inputs together:

1. `plumbline-design-spec-approved.md`
2. `plumbline-implementation-handoff-plan.md`
3. `superpowers-personal.zip` — the current customized predecessor, used for migration analysis and preservation of proven ideas
4. Access to the current default branches of:
   - `https://github.com/mattpocock/skills`
   - `https://github.com/obra/superpowers`
5. Access to current official Codex documentation:
   - Plugin authoring: `https://learn.chatgpt.com/docs/build-plugins`
   - Plugin use: `https://learn.chatgpt.com/docs/plugins`
   - Skill authoring: `https://learn.chatgpt.com/docs/build-skills`
   - Subagents: `https://learn.chatgpt.com/docs/agent-configuration/subagents`
   - Managed worktrees: `https://learn.chatgpt.com/docs/environments/git-worktrees`
   - `AGENTS.md`: `https://learn.chatgpt.com/docs/agent-configuration/agents-md`
   - Configuration reference: `https://learn.chatgpt.com/docs/config-file/config-reference`

Integrity values for the handoff files created in this conversation:

```text
plumbline-design-spec-approved.md
SHA-256: a5dc4d0c41ade03855a8673a08177238c32ed8ce1ee11efde210c7b94dc25245

superpowers-personal.zip
SHA-256: 586fb714bde49bb440e7c4d648f0144d88d5bf550be1386437feb95646429d7e
```

At kickoff, record the exact source commit SHAs used from both upstream repositories in the plan header or a short provenance section. Do not vendor their entire repositories into Plumbline.

---

## 3. Source synthesis and attribution rules

Plumbline is a deliberate synthesis, not a rename.

### 3.1 Primary design sources

Use Matt Pocock's repository primarily for:

- small, focused skill bodies;
- explicit versus model-invoked separation;
- progressive disclosure;
- one-question-at-a-time grilling;
- repository facts being researched instead of asked;
- public-seam testing and resistance to implementation-coupled tests;
- domain language and deep-module vocabulary;
- aggressive prompt pruning and single-source-of-truth discipline.

High-value source files include:

```text
skills/productivity/grilling/SKILL.md
skills/productivity/grill-me/SKILL.md
skills/productivity/writing-great-skills/SKILL.md
.agents/invocation.md
skills/engineering/grill-with-docs/SKILL.md
skills/engineering/to-spec/SKILL.md
skills/engineering/implement/SKILL.md
skills/engineering/tdd/SKILL.md
skills/engineering/diagnosing-bugs/SKILL.md
skills/engineering/code-review/SKILL.md
skills/engineering/research/SKILL.md
skills/engineering/domain-modeling/SKILL.md
skills/engineering/codebase-design/SKILL.md
```

Use Superpowers primarily for:

- automatic process guidance after activation;
- deliberate movement from idea to design to implementation;
- evidence before completion claims;
- checkpoint execution;
- isolated subagent work;
- independent review;
- systematic diagnosis techniques;
- user acceptance and branch closeout concepts.

High-value source files include:

```text
skills/using-superpowers/SKILL.md
skills/brainstorming/SKILL.md
skills/writing-plans/SKILL.md
skills/test-driven-development/SKILL.md
skills/systematic-debugging/SKILL.md
skills/dispatching-parallel-agents/SKILL.md
skills/subagent-driven-development/SKILL.md
skills/executing-plans/SKILL.md
skills/requesting-code-review/SKILL.md
skills/receiving-code-review/SKILL.md
skills/verification-before-completion/SKILL.md
skills/using-git-worktrees/SKILL.md
skills/finishing-a-development-branch/SKILL.md
skills/writing-skills/SKILL.md
```

Use `superpowers-personal.zip` primarily for:

- the proven five-role agent-team concept;
- repository-first agent override behavior;
- specialist discovery during brainstorming;
- backend, frontend, research, implementation, and QA role boundaries;
- current pain points to remove: universal bootstrap, duplicated routing doctrine, exhaustive plans, universal TDD, custom worktrees, global agent copying, and plan state living only in context.

### 3.2 Synthesis rules

- Extract behaviors and leading concepts; rewrite them in Plumbline's terminology and lighter policy.
- Do not preserve upstream hard gates that contradict the approved Plumbline specification.
- Do not copy long passages merely because they are well written.
- Keep every rule in one authoritative place wherever practical.
- If substantial upstream text or code is retained, preserve the required MIT notices.
- Add `THIRD_PARTY_NOTICES.md` naming Matt Pocock and Jesse Vincent / Prime Radiant and include the relevant MIT notices.
- Keep Plumbline's own license explicit. MIT is the natural default unless the repository owner selects another compatible license.
- Do not reuse Superpowers branding assets.

---

## 4. Non-negotiable implementation constraints

The implementing agent must preserve these constraints throughout every checkpoint:

- No session-start hooks.
- No universal “check skills before every response” bootstrap.
- No repository mutation during plugin installation.
- No global copying or symlinking of bundled skills.
- No automatic global installation of custom agents.
- No plugin-owned Git worktree creation, location, registry, or cleanup.
- No mandatory TDD for all code, configuration, documentation, or refactors.
- No permanent tests whose sole purpose is to freeze documentation wording, private structure, or literal configurable defaults.
- No issue tracker, ticket, pull request, label, or remote Git automation in v1.
- No automatic initialization from an ordinary prompt.
- No fixed canonical documentation taxonomy imposed on established repositories.
- No micro-plan decomposition by technical layer.
- No overlapping parallel implementer ownership.
- No subagent commits or active-plan edits.
- No full-suite QA rerun merely to duplicate closeout evidence.
- No broad Git-history archaeology or automatic `git bisect`.
- No hidden cleanup script or state database required to remove Plumbline's repository effect.
- Explicit user instructions override default workflow choices.

---

## 5. Target repository layout

Begin with a root-level plugin repository unless current Codex marketplace validation proves that the local marketplace must point at a nested plugin directory.

Preferred layout:

```text
plumbline/
├── .codex-plugin/
│   └── plugin.json
├── .agents/
│   └── plugins/
│       └── marketplace.json          # development marketplace only
├── assets/
│   ├── icon-small.svg
│   ├── icon-large.png
│   └── screenshots/
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
├── references/                       # preferred shared reference library; validate access
├── templates/
│   ├── router/
│   └── agents/
├── evals/
│   ├── fixtures/
│   ├── prompts/
│   ├── expected/
│   └── README.md
├── scripts/
│   ├── validate.py
│   └── measure-context.py
├── tests/
│   ├── test_structure.py
│   ├── test_metadata.py
│   ├── test_references.py
│   └── test_content_contracts.py
├── docs/
│   ├── architecture.md
│   ├── skill-authoring.md
│   ├── evaluation.md
│   └── migration-from-superpowers-personal.md
├── README.md
├── CHANGELOG.md
├── THIRD_PARTY_NOTICES.md
├── LICENSE
└── pyproject.toml                    # development-only validation dependencies
```

Only `.codex-plugin/plugin.json` belongs inside `.codex-plugin/`. Do not add hooks, MCP configuration, or connector files unless a later approved version requires them.

If a root-level local marketplace entry cannot reliably reference `./`, move the plugin package under `plugins/plumbline/` during the first checkpoint, before later paths become established. Record that deviation in this plan.

The installed plugin owns all reusable skills, references, templates, metadata, and assets. A user repository receives only approved local integration:

```text
.agents/skills/plumbline-router/       # activation and kill switch
.codex/agents/*.toml                   # optional, user-owned agent team
.worktreeinclude                       # optional, only when approved and needed
```

Do not copy the plugin's full skill tree into user repositories.

---

## 6. Skill architecture

### 6.1 Invocation model to prove before finalizing

Start with this preferred model:

- All globally bundled public skills are explicitly invokable.
- `plumbline`, `plumbline-init`, `plumbline-agent-team`, and `plumbline-offboard` set `allow_implicit_invocation: false`.
- Public phase skills are also explicit by default.
- The local `plumbline-router` is the only implicitly eligible repository skill.
- The router and `$plumbline` direct Codex to the selected public phase.

Before writing all phase content, prove whether an invoked router skill can reliably reach a public phase whose implicit invocation is disabled.

If it cannot, implement wrapper/engine pairs without changing the public command surface:

```text
plumbline-plan                 explicit public wrapper
plumbline-plan-engine          narrowly model-invoked internal engine
```

The public wrapper runs the engine. The local router selects the engine. Internal engine descriptions must contain the activation boundary and must not trigger from unrelated ordinary prompts. Do not make every public phase broadly implicit as a shortcut.

### 6.2 Skill size budgets

These are targets, not reasons to omit a necessary rule:

| Skill | Target `SKILL.md` words |
|---|---:|
| `plumbline` | 120–220 |
| `plumbline-init` | 350–600 |
| `plumbline-shape` | 250–450 |
| `plumbline-spec` | 300–500 |
| `plumbline-plan` | 350–550 |
| `plumbline-execute` | 450–750 |
| `plumbline-diagnose` | 300–500 |
| `plumbline-review` | 300–500 |
| `plumbline-closeout` | 300–500 |
| `plumbline-agent-team` | 400–650 |
| `plumbline-offboard` | 150–300 |
| local router | 80–180 |

Keep model-facing descriptions under roughly 35 words where possible. Put branch-specific detail in references. Measure total initial skill-description load and total phase-body load as part of the release gate.

---

## 7. Draft skill content contracts

The following drafts are behavioral baselines. The implementing agent may refine wording for clarity and invocation reliability, but must preserve the stated behavior and size discipline.

### 7.1 `$plumbline` — universal explicit front door

**Proposed description**

```yaml
name: plumbline
description: Enter Plumbline at the latest safe phase from an idea, design, plan, implementation, bug, review request, or accepted feature.
```

**Invocation policy:** explicit only.

**Draft body**

```markdown
# Plumbline

Assess the user's requested outcome, supplied artifacts, conversation state, and only the repository context needed to identify the current phase.

Choose the latest safe phase:

- direct work for small, clear, low-risk maintenance
- Diagnose for a defect, regression, failure, or performance problem
- Shape when product intent or important behavior remains unclear
- Specification when intent is understood but the active product contract is incomplete
- Plan when a sufficient design exists but execution checkpoints do not
- Execute when a sufficient specification and workable execution source exist
- Review when implementation exists and the user wants an independent assessment
- Closeout when the work has been accepted and integration or cleanup is requested

Honor existing artifacts regardless of which model or workflow produced them. Repair only blocking gaps. Ask the user only when a missing answer would invent a product decision.

State the selected phase in one sentence, then run only that Plumbline phase. Do not initialize the repository or enable future automatic routing.
```

**Key source influences:** Matt's tiny orchestration wrappers and invocation split; Plumbline's latest-safe-phase rule; rejection of Superpowers' universal startup behavior.

**Required evals:** rough idea → Shape; external design → Plan; accepted feature → Closeout; one-off invocation leaves no router.

### 7.2 `$plumbline-init` — repository initialization and reassessment

**Proposed description**

```yaml
name: plumbline-init
description: Initialize or reassess Plumbline for a repository through a read-only audit and one approved setup proposal.
```

**Invocation policy:** explicit only.

**Draft body**

```markdown
# Initialize Plumbline

Before inspecting the repository, check whether this conversation already contains unrelated active implementation work. If so, recommend a fresh task and stop unless the user explicitly says `continue here`.

Begin read-only. Determine whether the repository is new or established, then inspect only enough to understand:

- project instructions and documentation routing
- canonical document ownership and current conventions
- build, validation, UAT, and managed-worktree needs
- active specification and plan conventions
- project and personal custom agents
- multi-agent configuration and managed constraints
- competing workflow controllers

Adopt an established repository's structure. Do not scaffold a parallel docs hierarchy merely because Plumbline has not been used there.

For a new project, obtain approval for the concise product baseline: purpose, users, important behavior, priorities, constraints, and non-goals. Then design the technical baseline and canonical docs autonomously.

Present one selectable proposal. Possible items are:

- install the tiny local Plumbline router
- create or audit a project agent team
- configure ignored-file propagation into managed worktrees
- repair documentation routing
- offer reversible conflict settings for overlapping workflow plugins

Describe every file and configuration change. Apply nothing before approval. After applying selected items, validate discovery and report the single router directory that disables automatic behavior when removed. End initialization; recommend starting feature work in a fresh task.
```

**Owned references:** existing-repository assessment, new-project bootstrap, conflict audit, router installation, worktree propagation, configuration patching.

**Key source influences:** Matt's setup/router separation; Superpowers' automatic feel only after activation; Codex plugin/skill/agent configuration; user requirement for inert installation and minimal repo footprint.

### 7.3 `$plumbline-shape` — product shaping

**Proposed description**

```yaml
name: plumbline-shape
description: Shape a product concept through repository research, recommendations, and one product-level question at a time, without implementing it.
```

**Invocation policy:** explicit or router-selected.

**Draft body**

```markdown
# Shape

Turn a concept into a shared product understanding. Do not implement unless the user later requests another phase.

Start with repository evidence. Read the applicable project instructions and documentation router, then inspect the relevant code, contracts, tests, configuration, and history only as needed. Use a bounded researcher or architect when that keeps noisy discovery out of the main thread. Research current primary sources when a material decision depends on version-specific behavior, security guidance, standards, or unfamiliar technology.

Resolve technical questions yourself. Ask the user only about product behavior, scope, priorities, user experience, privacy, cost, destructive handling, compatibility, or another difficult-to-reverse consequence.

Ask one question at a time. For each blocking question provide:

- the recommended answer
- meaningful product-level alternatives
- the tradeoff
- the default Plumbline will use if the user delegates the choice

Open only relevant branches of the decision tree. Do not force a fixed questionnaire or three alternatives when one approach is clearly superior.

Preserve the user's feature boundary. Crossing frontend, backend, persistence, schema, security, or deployment seams does not create separate product features.

Shaping is complete when the product outcome, users, scope, important behavior, failure expectations, acceptance, and irreversible tradeoffs are sufficiently clear. It may end as discussion only. Create no specification unless the user requests it or the selected flow continues to Specification.
```

**Owned references:** product-question threshold, internal/external research policy, feature-integrity rule.

**Key source influences:** Matt's `grilling`; Superpowers brainstorming's repo exploration and alternatives; custom specialist discovery; Plumbline's product-directed autonomy.

### 7.4 `$plumbline-spec` — active feature specification

**Proposed description**

```yaml
name: plumbline-spec
description: Create or adopt one transient product specification from a conversation, attachment, handoff, or existing design without replaying completed shaping.
```

**Invocation policy:** explicit or router-selected.

**Draft body**

```markdown
# Specification

Create or adopt the active product contract for one feature.

First assess any supplied design, handoff, attachment, or conversation. Preserve confirmed product decisions and provenance. Do not require a Plumbline template or repeat shaping merely because another model produced the source.

Compare claims about the repository with current canonical documentation, code, tests, configuration, and relevant primary sources. Resolve ordinary technical conflicts autonomously while preserving requested product behavior. Ask only when a remaining conflict would invent or change a product decision.

Materialize chat-only or attachment-only requirements into repository files before long-running execution. Use the repository's existing transient-artifact convention; otherwise use `docs/specs/<feature>-source.*` for the original source when needed and `docs/specs/<feature>.md` for the active specification.

The specification owns:

- product outcome and users
- scope and non-goals
- domain language and invariants
- required behavior and failure behavior
- compatibility, data, privacy, and security constraints
- acceptance criteria
- testing and acceptance strategy
- expected canonical-document impact
- durable decisions, rejected alternatives, and material assumptions

Write in product and contract language, not as a file-by-file implementation plan. The specification is authoritative during implementation but is not canonical current-state documentation. Stop after writing and self-checking it when the user invoked this phase explicitly.
```

**Owned references:** imported-artifact handling, source safety, specification template, provenance and amendment policy.

**Key source influences:** Matt's `to-spec`, domain modeling, and no-interview synthesis; Superpowers design docs; user's transient-gospel requirement.

### 7.5 `$plumbline-plan` — live checkpoint plan

**Proposed description**

```yaml
name: plumbline-plan
description: Turn a sufficient specification or design into one live, checkpoint-based implementation plan with dependencies, ownership, verification, and recovery state.
```

**Invocation policy:** explicit or router-selected.

**Draft body**

```markdown
# Plan

Create the single live implementation plan for the complete feature.

Read the active specification or supplied design, the relevant canonical documents, and enough repository code to understand real ownership, dependencies, validation, and likely worktree needs. Do not plan from filenames alone.

Preserve the product feature boundary. Do not create separate frontend, backend, schema, testing, or documentation plans. Organize the feature into a small number of coherent checkpoints that produce meaningful, verifiable progress.

The plan must record:

- feature outcome and governing specification
- global constraints
- checkpoint order and dependencies
- shared contracts and main-thread-only files
- likely serial and parallel work packages with disjoint ownership
- runtime-protection decisions
- targeted verification and the smallest useful UAT surface
- canonical-document impact
- status, evidence, blockers, deviations, and corrections

Use exact paths when repository research supports them, but do not transcribe complete implementation code or break work into two-minute actions. A checkpoint is sized for coherent integration and review, not for agent convenience.

Map every acceptance criterion to at least one checkpoint. Mark technical assumptions and risks explicitly. Self-review for missing requirements, false parallelism, overlapping write sets, unsupported commands, and micro-slicing.

Plan-based work requires a kickoff commit containing the imported source, specification, and initial plan before production implementation. Stop after planning when this phase was explicitly requested.
```

**Owned references:** live-plan schema, checkpoint template, execution topology, plan self-review, compaction recovery.

**Key source influences:** Superpowers' executable plans and checkpoints; Matt's testing seams and concise skills; rejection of exhaustive code transcripts and micro-tasks.

### 7.6 `$plumbline-execute` — orchestrated implementation

**Proposed description**

```yaml
name: plumbline-execute
description: Implement one active Plumbline feature plan through durable checkpoints, bounded subagents, targeted verification, and Ready for Acceptance.
```

**Invocation policy:** explicit or router-selected.

**Draft body**

```markdown
# Execute

Implement the active feature as the main-thread orchestrator and sole Git writer.

Use a Codex-managed worktree for scoped or designed feature work unless the user explicitly chooses the active checkout. Do not create, relocate, or remove worktrees yourself. Verify the environment can use the repository's existing dependencies and required shared resources before implementation.

For plan-based work, confirm the kickoff commit exists. Before each checkpoint re-read the governing specification, current plan state, relevant canonical documents, and Git state.

Execute the checkpoint's dependency topology:

- stabilize shared contracts serially before parallel consumers
- prefer matching project agents, then personal agents, then bounded built-ins
- give every implementer a precise deliverable, read set, disjoint write set, prohibited files, validation, and report contract
- never allow subagents to stage, commit, move Git state, or edit the specification and plan
- pause affected work when ownership or dependency assumptions change

The main thread inspects and integrates all returned work. Run checkpoint-level targeted validation, apply the runtime-value test decision, update plan status and evidence, record deviations and canonical impact, then create one coherent checkpoint commit. Do not advance while the checkpoint is Blocked or Reopened.

When all checkpoints are complete, prepare the smallest meaningful acceptance surface. Run the planned completion checks and dispatch a fresh standard QA audit unless the user overrides it. Repair confirmed findings through focused corrective commits and reopened checkpoints.

End at Ready for Acceptance. Do not delete transient artifacts or integrate accepted work until the user completes UAT, explicitly approves the result, or instructs closeout.
```

**Owned references:** managed-worktree policy, borrowed-resource safety, single-Git-writer orchestration, subagent briefs, runtime-value testing, checkpoint recovery, Ready for Acceptance.

**Key source influences:** Superpowers subagent-driven execution, parallel dispatch, verification; custom agent routing; Codex managed worktrees; user requirements for tracked live plan state.

### 7.7 `$plumbline-diagnose` — proportional diagnosis

**Proposed description**

```yaml
name: plumbline-diagnose
description: Diagnose a bug, regression, test failure, or performance problem with a tight evidence loop and proportional history or planning.
```

**Invocation policy:** explicit or router-selected.

**Draft body**

```markdown
# Diagnose

Start from the user's exact symptom and the current repository. Keep small bugs light; escalate only when evidence shows broader work is needed.

Build the smallest practical feedback signal that can distinguish the reported failure from success: an existing focused test, command, request, trace, browser flow, log probe, or minimal reproduction. Do not insist on constructing an elaborate harness when current evidence already establishes the cause.

Inspect the responsible code path, contracts, configuration, and relevant canonical documents. Form and test falsifiable hypotheses. Change one diagnostic variable at a time and remove temporary instrumentation before completion.

Use the user's timeline. Consult Git only when a bounded lookup by path, symbol, contract, feature term, or known-good range is likely to resolve uncertainty. Do not scan history wholesale or run automatic bisection.

Prefer a regression test only when it exercises the real failure through a stable seam and adds unique runtime protection. Otherwise use the most appropriate targeted verification and state the residual risk.

A small repair may remain in the active checkout without a specification or plan. If diagnosis reveals substantial feature behavior, migration, security, or cross-cutting work, recommend or enter the appropriate Plumbline phase. An explicit second-opinion request routes to Review without manufacturing a retroactive plan.
```

**Owned references:** feedback-loop options, hypothesis discipline, bounded Git history, runtime-protection decision, escalation threshold.

**Key source influences:** Matt's tight-loop diagnosis; Superpowers systematic debugging; user rejection of mandatory heavy archaeology and auto-bisect.

### 7.8 `$plumbline-review` — independent audit

**Proposed description**

```yaml
name: plumbline-review
description: Perform an independent, report-only QA audit of planned work, a difficult bug fix, or an external implementation, with optional deep mode.
```

**Invocation policy:** explicit or router-selected.

**Draft body**

```markdown
# Review

Perform an independent audit. Do not implement fixes.

Use a fresh `qa-auditor` when available. For planned work, review the imported source, active specification, live plan, fixed base-to-head diff, checkpoint evidence, relevant canonical documents, and recorded verification. For no-plan work, use the user's claim, symptom or intent, diagnosis when present, diff, contracts, and focused evidence.

The default is a standard audit: inspect governing artifacts and code first, build a requirement and risk map, then run only the smallest non-mutating probe needed to settle a material uncertainty. Do not repeat a full closeout suite merely to claim independence. Deep audit requires explicit invocation or user approval.

Try to falsify correctness and readiness. Look for omitted requirements, thin implementation, edge cases, blast radius, hidden coupling, invalid assumptions, data or security risk, brittle or redundant tests, and stale canonical documentation.

Remain evidence-bound. Do not manufacture findings, enforce personal style, or demand tests without a plausible regression. Every blocking finding must include concrete evidence, a failure scenario, blast radius, and the minimum condition that would resolve it.

Return one verdict: PASS, PASS_WITH_RESIDUAL_RISK, CHANGES_REQUIRED, or INCONCLUSIVE. The report is the terminal output. Only a separate user instruction such as `address the confirmed findings` authorizes repair work.
```

**Owned references:** standard/deep audit rubric, probe policy, verdict format, planned-feature coverage matrix, sticky-bug review.

**Key source influences:** Matt's independent standards/spec review; Superpowers requesting/receiving review; custom QA persona; user's adversarial-but-grounded requirement.

### 7.9 `$plumbline-closeout` — acceptance, reconciliation, and integration

**Proposed description**

```yaml
name: plumbline-closeout
description: Close accepted work by reconciling canonical truth, removing transient artifacts, preserving history, and integrating through the user's chosen Codex or Git flow.
```

**Invocation policy:** explicit or router-selected.

**Draft body**

```markdown
# Closeout

Close work only after successful UAT, explicit approval, or a clear instruction to integrate.

If QA or UAT exposes a defect, reopen the affected checkpoint or add one bounded corrective checkpoint to the same plan. Do not close while planned work remains Blocked or Reopened.

For accepted plan-based work:

1. Recheck changes made after the completion audit.
2. Confirm the final implementation satisfies the specification and every acceptance criterion.
3. Reconcile each affected canonical document with the repository's actual current design, contracts, capabilities, security, and operating state.
4. Ensure no durable truth exists only in the imported source, specification, or plan.
5. Remove the imported source and active transient specification and plan.
6. Remove active-artifact routing entries.
7. Run final proportional verification after cleanup.
8. Create the coherent closeout commit.
9. Integrate through the user's requested Handoff, local merge, branch, or remote workflow.

Preserve kickoff, checkpoint, and corrective commits by default. Do not squash or rewrite history unless instructed. Do not create or remove worktrees yourself.

Run a lightweight agent-drift check only when the feature changed a significant domain term, technical surface, or canonical path referenced by project agents. Recommend an agent audit only with concrete evidence.
```

**Owned references:** acceptance states, canonical reconciliation, transient cleanup, integration options, agent drift.

**Key source influences:** Superpowers branch finishing and verification; Codex Handoff; user's transient cleanup and preserved-history requirements.

### 7.10 `$plumbline-agent-team` — project agent configuration

**Proposed description**

```yaml
name: plumbline-agent-team
description: Initialize, audit, retune, or extend an untracked project-local Codex agent team while preserving user-selected models and repository truth.
```

**Invocation policy:** explicit only; callable as a selectable branch of Init.

**Draft body**

```markdown
# Agent Team

Support four operations: initialize, audit, retune, and add a specialist.

Begin read-only. Inspect project and personal custom agents, project instructions, the documentation router, current technical surfaces, multi-agent configuration, managed policy, and worktree propagation.

Prefer project-local agents under `.codex/agents/`. Treat bundled archetypes as quality rubrics and generation scaffolds, not managed copies. Generated agents must combine:

- stable role discipline from Plumbline
- repository vocabulary, real technical surfaces, and canonical-document pointers
- user-controlled model, reasoning, sandbox, and tool choices

Do not embed mutable ownership maps, target architecture, or copied canonical documents in agent prompts.

When auditing existing agents, evaluate role selection, overlap, stale repository truth, Plumbline compatibility, operational configuration, context cost, and output quality. Preserve healthy custom behavior and all intentional model settings by default. Patch surgically; replace the instruction body only when old workflow rules and stale repository truth are too entangled to clean safely.

Present one reviewable proposal before writing. Configure local ignore rules and managed-worktree propagation only with approval. Change `.codex/config.toml` only when a concrete incompatible value exists, such as disabled multi-agent support or zero spawn depth.

After applying changes, parse every TOML and run one bounded read-only smoke test proving role discovery and configuration without modifying repository files.
```

**Owned references:** archetype rubric, agent audit, config checks, model preservation, ignore/worktree propagation, smoke test.

**Key source influences:** current custom TOMLs; Codex subagent configuration; user requirement for flexible model-cost tuning.

### 7.11 `$plumbline-offboard` — simple repository deactivation

**Proposed description**

```yaml
name: plumbline-offboard
description: Explain and optionally apply the minimal cleanup needed to deactivate Plumbline in a repository while preserving useful project assets.
```

**Invocation policy:** explicit only.

**Draft body**

```markdown
# Offboard Plumbline

Begin read-only and produce a cleanup map.

The required kill switch is removal of `.agents/skills/plumbline-router/`. Removing that directory disables automatic Plumbline routing for the repository.

Identify optional Plumbline-specific integration such as router propagation patterns, namespaced instruction blocks, or previously approved workflow-conflict settings. Offer exact reversible changes, but apply nothing without approval.

Preserve by default:

- canonical project documentation and decisions
- project-local custom agents
- generic worktree preparation and shared-environment configuration
- useful validation, UAT, and development scripts
- source code, tests, and Git history

Do not attempt to reconstruct and reverse every historical setup action. Do not restore another workflow controller automatically. Include short manual steps for users who remove the plugin before running this skill.
```

**Owned references:** cleanup map and conflict restoration.

### 7.12 Local `plumbline-router` — activation hook and kill switch

This is a generated repository-local skill, not a bundled public command.

**Proposed description**

```yaml
name: plumbline-router
description: Route repository changes through Plumbline after this project has explicitly opted in, while keeping direct work lightweight.
```

**Invocation policy:** implicitly eligible.

**Draft body**

```markdown
# Plumbline Router

This repository has opted into Plumbline.

For an ordinary repository request, choose the smallest appropriate path:

- keep small, clear, low-risk maintenance direct
- use Plumbline Diagnose for defects and regressions
- use Shape when product intent is materially unclear
- use Specification when intent is clear but the product contract is incomplete
- use Plan when a sufficient design exists
- use Execute when an adequate execution source exists
- use Review for an independent assessment
- use Closeout after acceptance or an explicit integration request

Honor explicit phase requests and user workflow overrides. Enter at the latest safe phase. Ask only blocking product questions. Load one phase, not the whole workflow.
```

Prefer a single generated `SKILL.md`. Add `agents/openai.yaml` only if invocation evaluation proves it is needed. The generated file may include a short version comment, but must not contain the full Plumbline doctrine.

---
## 8. Shared reference library

The preferred design is one plugin-level `references/` library loaded through explicit pointers from phase skills. Validate that Codex skill execution can reliably read plugin-root references from installed plugin-cache paths. If not, co-locate each reference with its primary owner and use only short cross-skill pointers; do not duplicate large bodies of doctrine.

Create these references as needed:

### `references/work-classification.md`

Define direct, scoped, designed, diagnose, review, and closeout classification. Include examples and the escalation rule:

- start with a lightweight evidence pass;
- hidden complexity may escalate work automatically;
- user instructions override;
- direct work does not receive artifact or QA ceremony;
- technical breadth alone does not split one feature.

### `references/product-autonomy.md`

Define the blocking-question threshold. A user question is warranted only when alternatives materially alter:

- product behavior or scope;
- user experience;
- privacy or security posture;
- destructive data handling;
- compatibility expectations;
- material cost;
- another difficult-to-reverse product consequence.

Include the question format: recommendation, alternatives, product tradeoff, and default.

### `references/research-policy.md`

Define repository-first research and bounded external research:

- inspect canonical docs, code, tests, config, and relevant history before asking factual questions;
- use external primary sources for current/version-specific facts, standards, and security guidance;
- delegate noisy read-heavy work when useful;
- return conclusions and evidence, not exploration transcripts;
- stop when evidence is sufficient.

### `references/artifact-lifecycle.md`

Define the four artifact classes:

- imported source;
- active specification;
- live implementation plan;
- canonical documentation.

Specify authority, mutability, Git tracking, amendment rules, and closeout deletion. Make clear that transient artifacts are gospel during active execution but are not canonical current-state documentation.

### `references/specification-template.md`

Use the approved specification headings from the design spec. Include compact guidance for each section and rules for imported provenance, current-versus-target state, and user-approved product amendments.

### `references/plan-schema.md`

Define a practical live-plan format. Recommended frontmatter:

```yaml
---
status: active
feature: <name>
specification: <relative path>
source: <relative path or null>
base_commit: <sha after kickoff>
current_checkpoint: CP-01
last_verified_commit: <sha or null>
ready_for_acceptance: false
---
```

Recommended checkpoint template:

```markdown
## CP-01: <Meaningful outcome>

**Status:** Pending | In Progress | Blocked | Complete | Reopened | Superseded

### Outcome
### Specification coverage
### Dependencies
### Execution topology
### Shared ownership
### Likely files and seams
### Runtime protection
### Verification
### Canonical documentation impact
### Completion criterion
### Completion evidence
### Deviations and corrections
```

Do not turn the plan into a chronological diary. Git owns chronology; the plan owns resumable execution state.

### `references/runtime-value-testing.md`

Encode the new-test value gate:

1. Runtime contract through a stable seam.
2. Plausible future regression not already caught by ordinary checks.
3. Independent expected result.
4. Highest useful existing seam.
5. Unique protection rather than duplication.
6. Proportionate maintenance and execution cost.

Outcomes may be: new failing regression test, extension of an existing test, existing protection only, static/build/smoke verification, or no permanent test. Include explicit exclusions for documentation wording, comments, formatting, private structure, internal call counts, literal configurable defaults, and trusted generated output.

### `references/subagent-orchestration.md`

Define:

- project agent → personal agent → built-in fallback;
- main thread as sole Git writer;
- write-set ownership;
- serial shared-contract changes;
- disjoint parallel work packages;
- `NEEDS_OWNERSHIP_CHANGE` and other report statuses;
- no active spec/plan edits by subagents;
- concise file-based briefs and reports;
- integration gate before checkpoint completion.

### `references/worktree-readiness.md`

Define:

- managed worktree default for scoped/designed features;
- no plugin worktree creation/removal;
- repository-owned setup;
- preference for env vars/absolute tool paths over links;
- safe borrowed-resource links only from disposable worktree to stable external target;
- no dependency-mutating commands against a borrowed `.venv`;
- import-origin probe for shared Python environments;
- `.worktreeinclude` for small ignored files, not large assets or source symlinks;
- Local Handoff for singleton, hardware-bound, or exceptionally heavy UAT.

### `references/qa-audit.md`

Define standard and deep review, evidence hierarchy, targeted probe limits, verdicts, coverage matrix, test-value review, canonical consistency, and report-only behavior.

### `references/canonical-documentation.md`

Define adaptive repository documentation discovery, ownership mapping, current-state writing, non-diary rules, concrete impact identification, conflict investigation, closeout reconciliation, and low-noise agent-drift detection.

### `references/conflict-audit.md`

Classify complementary, adjacent, competing discipline, and competing workflow-controller overlaps. Define reversible proposals and forbid automatic disabling or uninstalling.

### `references/offboarding.md`

Define the single kill switch, optional cleanup, preservation defaults, conflict restoration choices, and manual post-uninstall steps.

---

## 9. Project agent archetype templates

Store plugin-owned templates under `templates/agents/` or `skills/plumbline-agent-team/assets/archetypes/`. Use placeholders for repository adaptation and user-selected model settings. The generated TOMLs are user-owned after creation.

Common placeholders:

```text
{{MODEL}}
{{REASONING_EFFORT}}
{{REPOSITORY_NAME}}
{{DOMAIN_SUMMARY}}
{{TECHNICAL_SURFACES}}
{{DOCUMENTATION_ROUTER}}
{{CANONICAL_POINTERS}}
{{VALIDATION_COMMANDS}}
```

Do not make the template renderer a complex code generator. The agent-team skill can synthesize TOML directly from these archetypes after reading the repository.

### 9.1 Researcher archetype

```toml
name = "researcher"
description = "Read-only researcher for {{REPOSITORY_NAME}} that resolves repository facts, discrepancies, dependency behavior, and material external questions with concise evidence."
model = "{{MODEL}}"
model_reasoning_effort = "{{REASONING_EFFORT}}"
sandbox_mode = "read-only"

developer_instructions = '''
You are the repository's read-only research specialist.

Read the applicable project instructions and {{DOCUMENTATION_ROUTER}}. Load only the canonical documents relevant to the assignment.

Primary responsibilities:
- establish current repository truth from files, symbols, tests, configuration, and relevant history
- investigate conflicts between documentation and implementation
- verify current or version-specific external facts through primary sources when material
- distinguish verified fact, inference, uncertainty, and recommendation

The repository's important vocabulary includes: {{DOMAIN_SUMMARY}}
Representative technical surfaces include: {{TECHNICAL_SURFACES}}. These are not exhaustive; follow evidence across adjacent areas when necessary.

Remain read-only. Do not decide product choices, authorize architecture, or implement fixes.

Return:
- answer or verdict
- concise evidence with paths, symbols, commands, or sources
- confidence and unresolved conflicts
- the next smallest useful investigation, only if needed
'''
```

### 9.2 Backend architect archetype

```toml
name = "backend-architect"
description = "Read-only backend and cross-runtime architecture specialist for {{REPOSITORY_NAME}}, focused on ownership, contracts, persistence, integrations, resilience, and migrations."
model = "{{MODEL}}"
model_reasoning_effort = "{{REASONING_EFFORT}}"
sandbox_mode = "read-only"

developer_instructions = '''
You are the repository's backend architecture specialist.

Read the applicable project instructions and {{DOCUMENTATION_ROUTER}}, then only the relevant architecture, contract, capability, security, and runbook documents.

Use the repository's vocabulary: {{DOMAIN_SUMMARY}}
Representative surfaces include: {{TECHNICAL_SURFACES}}. They define likely focus, not an exclusive inspection boundary.

Responsibilities:
- determine the smallest sound ownership boundary
- design deep interfaces and stable seams
- preserve domain invariants and provider isolation
- assess persistence, data flow, failure handling, resilience, compatibility, and migrations
- distinguish implemented current state from approved target state
- reuse established contracts where they remain suitable
- reject speculative layers, broad rewrites, and hypothetical abstractions

Resolve ordinary technical choices autonomously. Escalate only when alternatives materially change product behavior, cost, privacy, destructive handling, compatibility, or another difficult-to-reverse consequence.

Remain read-only. Return verdict, evidence, ownership and contract recommendation, tradeoffs, migration implications, and required validation.
'''
```

### 9.3 Frontend architect archetype

```toml
name = "frontend-architect"
description = "Read-only frontend and interaction architecture specialist for {{REPOSITORY_NAME}}, focused on user flows, state ownership, accessibility, UI contracts, and integration boundaries."
model = "{{MODEL}}"
model_reasoning_effort = "{{REASONING_EFFORT}}"
sandbox_mode = "read-only"

developer_instructions = '''
You are the repository's frontend architecture specialist.

Read the applicable project instructions and {{DOCUMENTATION_ROUTER}}, then the relevant product, capability, interaction, contract, and architecture documents.

Use the repository's vocabulary: {{DOMAIN_SUMMARY}}
Representative surfaces include: {{TECHNICAL_SURFACES}}. Inspect adjacent backend contracts when they determine user-visible behavior.

Responsibilities:
- map the complete user interaction and state flow
- place state and side effects at clear ownership seams
- preserve accessibility, loading, failure, recovery, and responsive behavior
- reuse established components and interaction patterns
- keep provider or transport details behind suitable adapters
- distinguish product requirements from presentation implementation
- avoid speculative design systems and unrelated refactors

Resolve ordinary technical choices autonomously. Escalate only product-level consequences.

Remain read-only. Return verdict, evidence, interaction and state decision, contract dependencies, edge cases, tradeoffs, and required validation.
'''
```

### 9.4 Implementer archetype

```toml
name = "implementer"
description = "Bounded implementation specialist for {{REPOSITORY_NAME}} that edits only an assigned write set after the outcome and ownership are established."
model = "{{MODEL}}"
model_reasoning_effort = "{{REASONING_EFFORT}}"
sandbox_mode = "workspace-write"

developer_instructions = '''
You are a bounded implementation specialist.

Read the assigned brief first, then the referenced specification, checkpoint, project instructions, documentation router, and only the canonical documents needed for the task.

Implement the requested product behavior within the exact write set. Follow existing repository patterns and stable contracts. Make the smallest defensible change without speculative abstractions or unrelated cleanup.

Testing follows the task's runtime-protection decision. Add or change permanent tests only when they protect meaningful behavior at a stable seam. Run the assigned targeted validation.

You must not:
- stage or commit files
- rebase, merge, reset, stash, switch branches, or move HEAD
- edit the active specification or implementation plan
- modify files outside the write set
- change shared contracts without returning NEEDS_OWNERSHIP_CHANGE
- silently widen scope

Return one status: DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT, NEEDS_OWNERSHIP_CHANGE, or BLOCKED.

Report files changed, behavior delivered, commands and results, assumptions, concerns, and any required ownership expansion.
'''
```

### 9.5 QA auditor archetype

```toml
name = "qa-auditor"
description = "Independent QA auditor for {{REPOSITORY_NAME}} that tries to falsify correctness and readiness through requirements, edge cases, blast radius, tests, and canonical truth."
model = "{{MODEL}}"
model_reasoning_effort = "{{REASONING_EFFORT}}"
sandbox_mode = "read-only"

developer_instructions = '''
You are an independent QA auditor. You did not implement the change and do not owe the implementer agreement, encouragement, or deference.

Read the applicable project instructions, {{DOCUMENTATION_ROUTER}}, the assigned review package, and only the relevant canonical documents.

Mission:
Attempt to falsify the claim that the work is correct, complete, safe, and ready for its stated next step.

Inspect the actual source artifacts, specification, live plan, diff, code, tests, configuration, and verification evidence. Trace affected interfaces, callers, state transitions, failure paths, and realistic blast radius far enough to test the claim.

Look for omitted requirements, thin implementation, invalid assumptions, edge cases, concurrency hazards, partial failure, compatibility breakage, data-integrity or security risk, hidden coupling, accidental complexity, stale canonical documentation, and tests that are insensitive, redundant, brittle, or implementation-coupled.

Passing tests are evidence, not proof. Do not demand tests for prose, private structure, literal configurable defaults, or behavior already protected at a stronger seam.

You may run a small number of targeted non-mutating probes only to settle a material evidence gap. Do not install dependencies, mutate shared environments, write tests, update snapshots, start persistent services, run the full suite without concrete cause, or implement fixes.

Every blocking finding must include evidence, a plausible failure scenario, blast radius, why existing protection is insufficient, and the minimum condition needed to resolve or disprove it. Do not manufacture findings or substitute style preferences for defects.

Return:
- PASS, PASS_WITH_RESIDUAL_RISK, CHANGES_REQUIRED, or INCONCLUSIVE
- confidence and claim reviewed
- blocking findings
- nonblocking evidence-backed risks
- requirement coverage when applicable
- regression-protection assessment
- canonical-consistency assessment
- missing evidence and what would settle it
'''
```

### 9.6 Optional specialist catalog

Do not create these by default. Recommend them only when the repository has a recurring need that existing roles cannot cover cleanly:

- security auditor;
- data migration specialist;
- browser/runtime debugger;
- performance investigator;
- infrastructure architect.

A role is justified by repeated distinct work and selection value, not by a desire to make the team look comprehensive.

---

## 10. Plugin metadata and presentation requirements

Use current official plugin schema at implementation time. The initial manifest should be based on:

```json
{
  "name": "plumbline",
  "version": "0.1.0",
  "description": "Aligned engineering workflows for agentic development.",
  "skills": "./skills/",
  "license": "MIT",
  "keywords": [
    "agentic-development",
    "planning",
    "code-review",
    "subagents",
    "workflows",
    "codex"
  ],
  "interface": {
    "displayName": "Plumbline",
    "shortDescription": "Aligned engineering workflows for agentic development",
    "longDescription": "Shape product intent, create durable feature plans, coordinate bounded subagents, verify behavior, and keep canonical repository truth aligned without heavyweight process on every change.",
    "category": "Coding",
    "capabilities": ["Interactive", "Read", "Write"],
    "defaultPrompt": [
      "$plumbline Help me decide the right workflow for this change.",
      "$plumbline-shape Help me flesh out this feature idea.",
      "$plumbline-review Give me an independent second opinion on this change."
    ],
    "brandColor": "#2563EB",
    "composerIcon": "./assets/icon-small.svg",
    "logo": "./assets/icon-large.png",
    "screenshots": []
  }
}
```

Do not invent publisher or repository identity. Populate optional author, homepage, and repository fields from the actual new repository and owner when available.

Brand requirements:

- A clean plumb-line or plumb-bob visual metaphor.
- Distinct from Superpowers branding.
- Legible at small plugin-browser sizes.
- A restrained engineering-oriented color palette.
- Accessible contrast.
- At least one polished screenshot before public distribution, showing the skill list or initialization proposal without exposing private repository data.

Every skill should have `agents/openai.yaml` only where it adds invocation policy or useful UI metadata. Do not create boilerplate metadata files that add no behavior.

---

## 11. Validation and evaluation strategy

Plumbline is mostly instructions, so tests must focus on observable invocation and workflow behavior rather than prose snapshots.

### 11.1 Static validation

Create a small development-only validation harness that checks:

- `plugin.json` parses and required paths exist;
- all skill frontmatter contains unique names and concise descriptions;
- `agents/openai.yaml` files parse and invocation policies match the plan;
- every reference pointer resolves;
- no `hooks/`, installer, copied global skills, or global agent deployment script exists;
- local router template remains below its word budget;
- skill descriptions and bodies stay within agreed context budgets or document justified exceptions;
- agent archetype TOMLs parse after filling test placeholders;
- manifest icon paths exist;
- no template contains real credentials, personal paths, or stale AiriAI-specific architecture;
- `THIRD_PARTY_NOTICES.md` contains both upstream attributions;
- transient example artifacts are not presented as canonical docs.

Use Python 3.11+ with `pytest`, `tomllib`, and a minimal YAML dependency unless another smaller cross-platform validation stack is clearly superior.

### 11.2 Content-contract tests

Do not assert exact paragraphs. Check for behavioral invariants, for example:

- Init contains fresh-thread guard and no mutation before approval.
- Front door contains latest-safe-phase behavior and no initialization.
- Shape contains one-question-at-a-time and product-question threshold.
- Plan contains one-feature/one-plan, checkpoint topology, and kickoff requirement.
- Execute contains sole Git writer and disjoint ownership.
- Testing reference contains the value gate and default exclusions.
- Review is report-only and permits bounded probes.
- Closeout removes transient artifacts and preserves history.
- Offboard identifies the router directory as the kill switch.
- Agent templates prohibit Git operations for implementers and fixes for QA.

These tests protect workflow contracts, not wording.

### 11.3 Invocation evaluations

Build a fixture matrix that exercises the 25 scenarios in the approved specification. Each case should define:

```yaml
id: dormant-config-change
repo_fixture: uninitialized-small-repo
prompt: "Change the default timeout from 15 to 20."
expected:
  invoked_skill: null
  creates_spec: false
  creates_plan: false
  asks_question: false
```

When automated Codex execution is available, run each case in a fresh session against a disposable fixture repository and capture:

- selected skill or no skill;
- phase classification;
- files created;
- user questions;
- subagents dispatched;
- Git changes;
- whether unrelated skills were loaded;
- completion summary.

If fully automated invocation telemetry is unavailable, maintain a repeatable manual protocol with transcripts and pass/fail criteria. Do not claim invocation reliability from reading descriptions alone.

### 11.4 High-risk evaluation clusters

Prioritize these before writing all final content:

1. **Dormancy:** globally installed skills do not take over uninitialized repositories.
2. **Router reachability:** the local router can select one phase without loading all phases.
3. **Side doors:** explicit phase invocation works without initialization.
4. **Direct restraint:** trivial docs/config work stays direct.
5. **Imported artifact adoption:** a sufficient external design skips reshaping.
6. **Compaction recovery:** a new session resumes from source/spec/plan/Git.
7. **Plan integrity:** one feature remains one plan across multiple seams.
8. **Subagent ownership:** overlapping writes are prevented.
9. **Testing restraint:** no synthetic docs/config tests.
10. **Adversarial QA:** omitted acceptance criteria are found without manufactured nits.
11. **Closeout:** canonical docs are reconciled and transient artifacts removed.
12. **Kill switch:** deleting the local router stops automatic routing.

### 11.5 Acceptance mapping

Maintain a machine-readable or Markdown matrix mapping all 64 specification acceptance criteria to:

- implementing checkpoint;
- static test, behavior eval, or manual proof;
- evidence path;
- final status.

Do not mark Plumbline v1 complete while an acceptance criterion lacks evidence or an explicit approved waiver.

---
## 12. Execution topology and Git policy for building Plumbline

Treat Plumbline v1 as one feature with one specification and one live plan.

The main thread owns:

- source provenance;
- plan amendments;
- shared skill architecture;
- plugin manifest and marketplace state;
- integration across skill drafts;
- Git staging and commits;
- acceptance mapping;
- completion claims.

Good parallel subagent uses include:

- one researcher comparing current Codex plugin/skill behavior with the plan;
- separate read-only source analysts for Matt Pocock, upstream Superpowers, and `superpowers-personal.zip`;
- disjoint skill-draft work after common references and invocation architecture are stable;
- disjoint agent-archetype drafts;
- evaluator agents reviewing different fixture clusters;
- a fresh QA auditor for checkpoint or final review.

Do not parallelize:

- changes to `plugin.json` and marketplace layout while the packaging shape is unsettled;
- the same skill or reference file;
- shared invocation descriptions;
- the common artifact schema;
- shared agent-template rendering behavior;
- Git operations;
- active plan updates.

Each checkpoint normally ends in one main-thread commit. Intermediate commits are allowed only for a stable prerequisite that would otherwise make the checkpoint unsafe to continue, such as proving a required Codex invocation architecture before drafting all phase skills.

---

## 13. Implementation checkpoints

### CP-00 — Establish the implementation repository and kickoff baseline

**Outcome**

A clean new Git repository contains the approved specification, this live plan, source provenance, and an initial current-state README. No substantive Plumbline behavior exists yet.

**Dependencies**

None.

**Main-thread work**

1. Initialize the new repository and inspect its actual Git and Codex environment.
2. Copy the approved specification to `docs/specs/plumbline-v1.md`.
3. Copy this plan to `docs/plans/plumbline-v1.md` and add live frontmatter using the plan schema.
4. Attach or make the predecessor archive available without unpacking it into tracked source. Record its SHA-256.
5. Pin the upstream source commit SHAs used for Matt Pocock and Superpowers.
6. Record the official Codex documentation access date and URLs.
7. Create a concise `README.md` stating that the repository is building Plumbline, with no installation instructions that imply the plugin already works.
8. Decide and record the development toolchain for static validation. Python 3.11 plus `pytest` and a minimal YAML parser is the recommended default.
9. Create `.gitignore` for development outputs only. Do not add user-repository setup behavior here.
10. Commit the kickoff baseline before plugin implementation.

**Likely files**

```text
docs/specs/plumbline-v1.md
docs/plans/plumbline-v1.md
README.md
.gitignore
```

**Validation**

- `git status` is clean after the kickoff commit.
- Both artifacts are readable from a fresh task without conversation history.
- Source SHAs and integrity values are recorded.
- The plan's `current_checkpoint` becomes `CP-01`.

**Completion criterion**

A fresh agent can explain the product, implementation order, and source baseline using repository files alone.

**Suggested commit**

```text
docs: establish Plumbline v1 specification and plan
```

---

### CP-01 — Build the Codex-native plugin shell and validation foundation

**Outcome**

Plumbline appears as a polished but behaviorally minimal plugin in a local Codex marketplace. The package follows current official structure, can be installed/enabled/disabled, and has a small automated structural validation suite.

**Dependencies**

CP-00 complete.

**Research first**

- Use current `@plugin-creator` or current official plugin docs to validate the manifest and marketplace shape.
- Prove whether a root-level plugin with marketplace `source.path: "./"` works. If not, move to `plugins/plumbline/` now and amend all later paths.
- Confirm which manifest interface fields are accepted by the current Codex version.
- Confirm how skill enable/disable controls appear in the plugin browser.

**Work packages that may run in parallel after layout is fixed**

1. **Brand package:** create original small and large Plumbline assets and marketplace copy.
2. **Validation harness:** implement static structure, metadata, reference, context-budget, and template-parse tests.
3. **Source attribution:** draft `THIRD_PARTY_NOTICES.md`, license, and source-influence documentation.

These packages have disjoint write sets. The main thread owns `plugin.json`, marketplace wiring, and final integration.

**Implementation requirements**

- Create `.codex-plugin/plugin.json` with name `plumbline`, version `0.1.0`, `skills: "./skills/"`, polished interface metadata, and no hooks/apps/MCP declarations.
- Create the local development marketplace using current official schema.
- Create skill directories and minimal placeholder frontmatter only for discovery testing. Do not fill them with boilerplate doctrine yet.
- Add `agents/openai.yaml` only where invocation policy or user-facing metadata is needed.
- Create original iconography and validate paths.
- Add the development validation toolchain and initial tests.
- Add `LICENSE`, `THIRD_PARTY_NOTICES.md`, `CHANGELOG.md`, and a minimal contributor/development section.
- Do not create installer scripts that copy global skills or agents.

**Validation**

- Plugin installs through the configured local marketplace and appears under the expected display name.
- Plugin can be enabled and disabled from Codex.
- A new session discovers the skill names.
- Installation creates no files in an unrelated fixture repository.
- Static validation passes.
- No session hook or global-copy installer exists.
- Brand assets render at plugin-browser scale.

**Specification acceptance covered**

AC 1–2, 62–64 in structural form; complete behavior follows later.

**Completion criterion**

A user can install, inspect, enable, and disable a polished Plumbline package, but no automatic workflow can yet affect repository work.

**Suggested commit**

```text
chore: scaffold the Plumbline Codex plugin
```

---

### CP-02 — Prove invocation architecture and implement the activation boundary

**Outcome**

Plumbline is dormant when merely installed, works through explicit one-off commands, and can be activated for one repository through a tiny local router whose deletion is the kill switch.

**Dependencies**

CP-01 complete.

**Serial prerequisite**

Before drafting all phase skills, implement a minimal front door, one minimal phase, and a fixture router. Run invocation experiments to choose one architecture:

1. public explicit phases directly reachable from the router; or
2. public wrappers plus narrow internal engines.

Record the result and why it is reliable. Do not continue by assumption.

**Implementation requirements**

- Implement the concise `$plumbline` front door.
- Implement the local router template and generation mechanics.
- Ensure the router is the only repository-level automatic activation mechanism.
- Ensure explicit one-off use never creates the router.
- Ensure uninitialized repositories do not receive automatic phase invocation from globally installed descriptions.
- Implement minimal phase-selection contracts and latest-safe-phase precedence.
- Honor explicit phase commands and direct user overrides.
- Create an initial kill-switch/offboard proof by deleting the router in a fixture repository.
- Keep the router below its word budget and free of full workflow doctrine.
- Verify whether the router can remain a single `SKILL.md`; add `agents/openai.yaml` only if required.

**Fixture evaluations**

- Dormant config change in uninitialized repo.
- Explicit `$plumbline-shape` in uninitialized repo.
- Explicit `$plumbline` with rough idea.
- Explicit `$plumbline` with sufficient design.
- Initialized direct documentation typo.
- Initialized feature concept.
- Router deletion.
- Plugin disabled while router remains.

**Validation**

- Only one phase is selected per prompt.
- Direct work remains direct.
- One-off use leaves no activation state.
- Router removal stops automatic behavior.
- Plugin disable prevents Plumbline execution even if the local router remains.
- Skill-description context report remains within budget.

**Specification acceptance covered**

AC 1, 3, 6–14, 59–61.

**Completion criterion**

The consent model is proven in real Codex sessions: install is inert, explicit side doors work, and repository auto-routing exists only after the local router is present.

**Suggested commit**

```text
feat: establish Plumbline routing and activation
```

---

### CP-03 — Implement initialization, agent-team setup, conflict handling, and offboarding

**Outcome**

A user can explicitly initialize a new or established repository through one read-only assessment and approved proposal, optionally create or refresh project agents, detect workflow conflicts, and later remove Plumbline's automatic effect through one obvious kill switch.

**Dependencies**

CP-02 invocation model stable.

**Main-thread-owned shared decisions**

- repository assessment result schema;
- exact router installation and local ignore strategy;
- configuration patch presentation;
- worktree propagation behavior;
- single selectable proposal format.

**Parallel work packages after shared schema is stable**

1. Draft the five agent archetypes in disjoint files.
2. Build established-repository fixtures, including an AiriAI-like docs tree.
3. Build new-project fixtures with no docs or agents.
4. Build conflict fixtures with Superpowers and overlapping TDD/review skills.
5. Draft offboarding and manual post-uninstall guidance.

**Implementation requirements**

- Implement the fresh-thread guard before repository inspection.
- Implement read-only assessment of instructions, docs, agents, config, worktrees, active artifacts, and competing controllers.
- Adopt existing canonical structures and terminology.
- For new projects, gather only the concise product baseline before technical scaffolding.
- Present one individually selectable proposal and mutate nothing before approval.
- Generate the local router under `.agents/skills/plumbline-router/`.
- Prefer untracked local integration. Use `.git/info/exclude` for local-only agent files and router paths where appropriate.
- Validate whether an untracked `.worktreeinclude` is honored; if not, explain and request approval for the smallest tracked propagation file.
- Implement `$plumbline-agent-team` initialize/audit/retune/add behavior.
- Preserve existing model slugs, reasoning, sandbox, permissions, and healthy custom preferences by default.
- Inspect `features.multi_agent`, `agents.max_depth`, and relevant managed-policy constraints. Offer exact approved patches only when needed.
- Implement the five repository-adapted archetypes and bounded discovery smoke test.
- Detect global/project role overlap without deleting either copy.
- Implement workflow conflict classification and reversible disable proposals.
- Validate the current Codex format for disabling individual skills/plugins before offering patches.
- Implement `$plumbline-offboard` as read-only by default with optional selected cleanup.

**Validation**

- Init invoked in a busy thread stops before inspection.
- Established AiriAI-like docs are adopted, not reorganized.
- New project setup asks product questions, then creates an appropriate baseline only after approval.
- Existing agent model slugs survive audit unchanged.
- Stale architecture copied into an agent is detected and removed from the proposed body.
- Disabled multi-agent config produces a precise proposal, not a silent edit.
- Generated TOMLs parse and one agent responds under its intended role without modifying files.
- Superpowers conflict is explained; no settings change before approval.
- Offboarding removes or identifies only Plumbline-specific integration and preserves useful docs/agents/tooling.

**Specification acceptance covered**

AC 4–7, 46–47, 52–58, 63–64; conflict scenario 24 and kill-switch scenario 25.

**Completion criterion**

A user can initialize, audit, retune, or offboard a repository with a clear proposal and minimal footprint, and project-local agents are actually discoverable when approved.

**Suggested commit**

```text
feat: add repository setup and agent-team management
```

---

### CP-04 — Implement shaping, specification, planning, and durable feature memory

**Outcome**

Plumbline can take a rough idea or external handoff, settle only necessary product decisions, create one authoritative transient specification and one live checkpoint plan, and preserve them through a mandatory kickoff commit and simulated compaction.

**Dependencies**

CP-02 routing stable; CP-03 initialization and project-context discovery available.

**Shared contracts to stabilize first**

- imported-source handling and provenance;
- specification template;
- live-plan schema and checkpoint statuses;
- default transient paths and repository-convention override;
- attachment size/secret-safety policy;
- kickoff commit boundary.

**Parallel work packages after those contracts are stable**

1. Shape skill and product-autonomy reference.
2. Specification skill and imported-artifact fixtures.
3. Plan skill and checkpoint topology fixtures.
4. Compaction/recovery evaluation harness.

The main thread integrates terminology and ensures no duplicated policy.

**Implementation requirements**

- Implement one-question-at-a-time shaping with recommendations and repository-first research.
- Keep technical architecture decisions inside the agent unless product consequences remain.
- Allow shaping to stop without creating files.
- Adopt sufficient external designs without re-grilling.
- Materialize chat-only and attachment-only requirements before long-running work.
- Preserve original source/provenance and avoid wholesale template rewrites.
- Protect secrets and avoid committing unsafe or unreasonably large binary attachments; create a safe Markdown extraction/assessment when required.
- Implement one feature/one spec/one plan.
- Create meaningful chronological checkpoints across technical seams without splitting the product outcome.
- Record dependencies, shared ownership, parallel groups, runtime protection, verification, canonical impact, and UAT surface.
- Map all acceptance criteria to checkpoints.
- Require the kickoff commit before production implementation.
- Update plan state and `last_verified_commit` as checkpoints progress.
- Implement recovery instructions that use only source/spec/plan/Git state after a fresh session.
- Do not include full implementation code or two-minute task sequences in plans.

**Evaluation cases**

- Shape only, no artifacts.
- External ChatGPT/Claude design routes to Plan.
- Chat-only design becomes tracked source/spec.
- A cross-frontend/backend feature remains one plan.
- A plan with 15 micro-checkpoints fails self-review and is consolidated.
- Hidden shared contract prevents false parallelization.
- Fresh session resumes the current checkpoint.
- Source/spec/plan are committed before code.

**Validation**

- Plan and spec templates pass content-contract tests.
- No acceptance criterion is unmapped.
- Compaction recovery succeeds without original chat history.
- Kickoff commit contains no substantive production implementation.
- Explicit `$plumbline-plan` stops after planning.

**Specification acceptance covered**

AC 15–25, with correction mechanics completed in CP-06.

**Completion criterion**

A substantial feature can be started from a rough idea or imported design and resumed after total conversation loss using tracked artifacts and Git alone.

**Suggested commit**

```text
feat: add shaping and durable feature planning
```

---

### CP-05 — Implement checkpoint execution, worktree guidance, subagent orchestration, and runtime-value testing

**Outcome**

Plumbline can execute one active feature plan through coherent checkpoints, safe parallel work packages, Codex-managed worktrees, targeted validation, live plan updates, and meaningful checkpoint commits.

**Dependencies**

CP-04 artifact contracts complete; CP-03 project-agent behavior available.

**Shared contracts to stabilize first**

- work-package brief and report schema;
- ownership/write-set semantics;
- checkpoint integration gate;
- runtime-value test decision;
- worktree readiness and borrowed-resource rules;
- Ready for Acceptance preconditions.

**Parallel work packages after shared contracts are stable**

1. Worktree readiness and cross-platform borrowed-resource research.
2. Runtime-value testing reference and fixtures.
3. Subagent brief/report templates.
4. Execute skill draft.

The main thread owns the final orchestration flow and all Git-related instructions.

**Implementation requirements**

- Default scoped/designed feature execution to Codex-managed worktrees.
- Keep direct work and small fixes eligible for the active checkout.
- Never create or remove worktrees from Plumbline instructions.
- Inspect repository-owned environment setup before recommending changes.
- Prefer environment variables and absolute tool/interpreter paths over symlinks.
- Permit safe borrowed-resource symlinks only when the target is external to disposable worktree roots and cleanup cannot follow the link into shared assets.
- For shared `.venv` use, prohibit dependency mutation and verify imports resolve to worktree source.
- Use `.worktreeinclude` for small ignored local files only; do not use it to copy models, package trees, or source symlinks.
- Use Handoff to Local when UAT is singleton, hardware-bound, exceptionally heavy, or cheaper to validate there.
- Enforce main-thread-only Git operations.
- Define disjoint write sets and stable contracts before parallel implementation.
- Pause work on ownership expansion instead of allowing “small” out-of-scope edits.
- Re-read spec/plan/docs before each checkpoint.
- Integrate subagent changes, run checkpoint validation, update plan evidence, then commit once per checkpoint.
- Implement the runtime-value test gate and explicitly allow non-test verification outcomes.
- Do not advance while a checkpoint is Blocked or Reopened.
- Prepare the smallest meaningful UAT surface rather than assuming a full-stack boot.

**Cross-platform validation**

- Windows and Unix path resolution.
- Safe link creation and removal behavior in disposable fixtures.
- Shared model/cache path outside worktree.
- Shared Python interpreter imports current worktree source.
- Worktree with local agents/router propagation.
- Local Handoff UAT instructions.

**Behavioral evaluations**

- Parallel frontend/backend packages after a serial contract checkpoint.
- Two agents requesting the same file causes serialization.
- Implementer attempts Git operation and is stopped by role contract.
- Literal config default receives no permanent test.
- Runtime reconnect behavior receives one valuable regression test.
- Plan updates before checkpoint advancement.

**Specification acceptance covered**

AC 27–33, 39–45; planned QA is completed in CP-06.

**Completion criterion**

A multi-seam feature can run through a realistic plan with safe parallelism, lightweight worktree use, valuable verification, live checkpoint state, and coherent Git history.

**Suggested commit**

```text
feat: add checkpoint execution and managed worktree guidance
```

---

### CP-06 — Implement diagnosis, adversarial review, UAT corrections, canonical reconciliation, and closeout

**Outcome**

Plumbline can diagnose proportionally, perform independent standard/deep QA, reopen plans after QA/UAT findings, reach Ready for Acceptance, reconcile canonical truth, remove transient artifacts, and integrate accepted work without rewriting history.

**Dependencies**

CP-04 artifact lifecycle and CP-05 execution complete.

**Parallel work packages**

1. Diagnose skill and bounded-history fixtures.
2. Review skill, QA rubric, and auditor fixture package.
3. Canonical-document impact and closeout fixtures.
4. UAT correction/reopened-checkpoint fixtures.

The main thread integrates the acceptance state machine and ensures review remains report-only.

**Implementation requirements**

- Implement proportional diagnosis with smallest practical feedback signal.
- Use current code and user timeline first; bound Git history by evidence.
- Do not automate bisection.
- Keep small bug fixes eligible for direct/no-plan work.
- Implement standard and deep review modes.
- Prefer a fresh `qa-auditor` subagent when available.
- Permit only targeted non-mutating probes that settle material uncertainty.
- Prevent QA from writing tests, editing code, updating snapshots, installing dependencies, or duplicating full closeout suites.
- Produce evidence-bound PASS / PASS_WITH_RESIDUAL_RISK / CHANGES_REQUIRED / INCONCLUSIVE verdicts.
- Require planned features to receive a standard completion audit before Ready for Acceptance unless explicitly overridden.
- Allow explicit second-opinion review of no-plan bug fixes.
- Reopen affected checkpoints after QA/UAT defects and append focused corrective commits.
- Preserve original completion evidence and record what prior validation missed.
- Generate a specification-to-diff coverage matrix before Ready for Acceptance.
- Prepare concise product-level UAT steps and support Handoff to Local.
- Treat canonical docs as current-state authorities, not diaries.
- Identify exact canonical impact; allow “no canonical change” when justified.
- Investigate code/doc disagreement instead of blindly overwriting either side.
- On accepted closeout, reconcile canonical truth, remove source/spec/plan, run final proportional verification, commit cleanup, and integrate through the user's requested flow.
- Preserve kickoff/checkpoint/corrective history by default.
- Recommend agent drift audit only for concrete significant drift.

**Evaluation cases**

- Sticky no-plan bug review on active checkout.
- Auditor detects an acceptance criterion missing from an otherwise green diff.
- Auditor reruns one focused test and stops.
- Auditor does not manufacture a style finding.
- Failed UAT reopens the correct checkpoint.
- Corrective commit closes the checkpoint again.
- Heavy runtime hands off to Local for UAT.
- Stale canonical contract blocks clean closeout.
- Closeout removes transient docs while `git show` can recover them.
- No-plan direct work closes without plan cleanup ceremony.

**Specification acceptance covered**

AC 26, 34–38, 44–52.

**Completion criterion**

Plumbline can independently prove or challenge feature completeness, incorporate corrections into durable plan state, and leave an accepted repository with current canonical truth and no active plan sprawl.

**Suggested commit**

```text
feat: add diagnosis review and accepted closeout
```

---

### CP-07 — Complete migration guidance, conflict compatibility, and end-to-end behavioral hardening

**Outcome**

The full Plumbline workflow is tested against the predecessor's failure modes, the 25 required scenarios, context-budget goals, plugin conflicts, and representative new/existing repositories.

**Dependencies**

All functional skills implemented.

**Parallel work packages**

1. Full invocation evaluation matrix.
2. Context and duplication audit.
3. `superpowers-personal` migration map.
4. Windows/worktree environment matrix.
5. Agent-team audit against the supplied AiriAI-style TOMLs.

The main thread owns final skill wording, invocation descriptions, and any architecture adjustment caused by evidence.

**Implementation requirements**

- Run all 25 specification scenarios in fresh fixture sessions.
- Add edge cases for ambiguous phase selection, explicit user override, plugin disabled state, and missing subagent capability.
- Measure initial descriptions, selected phase bodies, and loaded references.
- Prune no-op, duplicated, overly negative, or sedimentary instructions.
- Verify direct work does not load or enact unrelated phases.
- Verify each side door works independently in an uninitialized repository.
- Verify local router behavior in Local and newly created managed worktrees.
- Audit the five generated agent templates against current custom TOMLs and Plumbline requirements.
- Validate reversible conflict proposals against current Codex configuration.
- Write `docs/migration-from-superpowers-personal.md` mapping every predecessor skill and file to keep, replace, fold, or remove.
- Include explicit advice against running Plumbline and Superpowers as simultaneous automatic controllers.
- Verify no old Superpowers names, paths, branding, or mandatory TDD language remain unintentionally.
- Update the 64-criterion evidence matrix.

**Context targets**

- Total public skill descriptions remain materially smaller than the predecessor's trigger surface.
- Local router remains under 180 words unless an eval demonstrates a necessary exception.
- No public skill body becomes a hidden monolith.
- The selected phase and references provide enough behavior without preloading downstream phases.

**Validation**

- All static tests pass.
- All required behavioral cases pass or have an explicit evidence-backed deviation approved by the user.
- A fresh QA auditor reviews the complete plugin diff against the specification and plan.
- Any QA finding is handled through focused corrective commits and reopened plan state.

**Specification acceptance covered**

All ACs, with emphasis on 8–14, 53–64 and all evaluation scenarios.

**Completion criterion**

Plumbline demonstrably delivers the lighter workflow rather than merely describing it, and the known predecessor failure modes do not reappear in the tested scenarios.

**Suggested commit**

```text
test: harden Plumbline workflow behavior
```

---

### CP-08 — Release polish, user documentation, UAT, and repository closeout

**Outcome**

Plumbline v1 is ready for real installation and user acceptance through the Codex plugin browser, with polished documentation, release metadata, screenshots, complete evidence, and a clean final repository after acceptance.

**Dependencies**

CP-07 complete and QA verdict acceptable.

**Implementation requirements**

- Finalize `README.md` around user-facing modes:
  - installed only;
  - explicit one-off;
  - initialized automatic routing;
  - side-door commands;
  - agent-team setup;
  - offboarding.
- Include a simple command reference and examples.
- Explain minimal repository footprint and kill switch.
- Explain transient specs/plans versus canonical docs.
- Explain managed worktree behavior without teaching a custom worktree system.
- Document conflict detection and reversible settings.
- Finalize `CHANGELOG.md`, semantic version, license, notices, repository fields, and publisher metadata inferred from the actual project.
- Capture clean screenshots for the plugin browser and initialization proposal.
- Install the plugin from the development marketplace into a clean Codex environment.
- Test enable, disable, update, and remove flows.
- Run the final 64-criterion acceptance matrix.
- Produce a concise user UAT script.
- Obtain explicit acceptance before deleting the active Plumbline specification and implementation plan from the repository.
- After acceptance, reconcile long-lived architecture/evaluation docs, remove transient spec/plan, run final static and targeted behavioral checks, and create the closeout commit.

**Recommended user UAT**

1. Install Plumbline through the plugin browser and start a new task.
2. In an uninitialized fixture repo, make a normal config request and confirm no automatic Plumbline takeover.
3. Invoke `$plumbline-shape` and confirm it works one-off without activation.
4. Invoke `$plumbline-init` in a clean fixture and approve only the router.
5. Start a new task and give a rough feature prompt; confirm automatic Shape behavior.
6. Give an external design and confirm it enters Plan without a full re-grill.
7. Make a direct docs tweak and confirm no spec/plan ceremony.
8. Invoke `$plumbline-review` on a prepared bug fix and inspect the independent report.
9. Delete `.agents/skills/plumbline-router/` and confirm automatic routing stops.
10. Disable the plugin in Codex and confirm no Plumbline skill runs.

**Validation**

- Plugin browser metadata and assets are polished.
- Install/update/disable/remove behavior works in current Codex.
- README matches actual behavior.
- All acceptance evidence is current at the release commit.
- No active transient plan/spec remains after user acceptance.
- Git history preserves kickoff, checkpoint, QA correction, and closeout evidence.

**Specification acceptance covered**

All 64 acceptance criteria.

**Completion criterion**

The user accepts Plumbline v1 in real Codex use, and the repository's final working tree contains the plugin, long-lived docs, evals, and no active implementation artifacts.

**Suggested commits**

Before UAT:

```text
release: prepare Plumbline v1 for acceptance
```

After accepted closeout:

```text
docs: reconcile Plumbline v1 and close implementation
```

---
## 14. Predecessor migration map

Use this map during CP-07. It is an implementation aid, not a requirement to preserve old file boundaries.

| `superpowers-personal` element | Plumbline treatment |
|---|---|
| `skills/using-superpowers` | Remove. Its universal bootstrap is replaced by inert install plus the optional local router. Preserve only user-instruction precedence. |
| `skills/agent-routing` | Remove as a runtime skill. Fold the narrow resolution order and controller ownership into `subagent-orchestration.md`; let `.codex/agents/*.toml` descriptions drive role selection. |
| `skills/brainstorming` | Replace with `plumbline-shape` and `plumbline-spec`. Preserve repo exploration, one question at a time, recommendations, and specialist discovery. Remove universal gating, mandatory design for config/docs changes, forced three approaches, and automatic plan transition. |
| `skills/writing-plans` | Replace with `plumbline-plan`. Preserve requirement coverage and executable verification. Remove two-to-five-minute steps, complete code blocks, universal TDD steps, one-task-per-commit, and forced execution choice menu. |
| `skills/test-driven-development` | Do not preserve as a universal skill. Extract valuable public-seam, regression, and anti-pattern guidance into `runtime-value-testing.md`. |
| `skills/systematic-debugging` | Replace with `plumbline-diagnose`. Preserve evidence, reproduction, hypotheses, targeted instrumentation, and cleanup. Remove universal heavy phases, automatic bisection, and refusal to reason when a perfect loop is impractical. |
| `skills/dispatching-parallel-agents` | Fold into `subagent-orchestration.md` and Execute. Preserve independent domains and integration review; add hard write-set and single-Git-writer rules. |
| `skills/subagent-driven-development` | Replace with Execute's checkpoint orchestration. Preserve bounded briefs, isolated context, status reporting, and final review. Remove fresh-agent-per-micro-task and mandatory per-task dual review. |
| `skills/executing-plans` | Fold into Execute. Preserve checkpoint continuation and stop conditions. Remove separate-session bias. |
| `skills/requesting-code-review` | Replace with `plumbline-review`. |
| `skills/receiving-code-review` | Fold a small evidence-first response rule into Execute's corrective loop; do not expose as a separate top-level skill unless evals show an independent use case. |
| `skills/verification-before-completion` | Fold into checkpoint completion, Ready for Acceptance, QA, and Closeout. Preserve evidence-before-claim discipline. |
| `skills/using-git-worktrees` | Remove. Replace with managed-worktree and environment-readiness reference. |
| `skills/finishing-a-development-branch` | Replace with `plumbline-closeout`. Preserve acceptance/integration distinction and destructive confirmation; remove custom worktree cleanup and fixed GitHub choices. |
| `skills/writing-skills` | Replace with project development docs informed by Matt's `writing-great-skills` and official Codex guidance. It need not ship as a public Plumbline user skill in v1. |
| `agents/codex/researcher.toml` | Use as input to the new researcher archetype; remove hardcoded repository facts and verbose output. |
| `agents/codex/backend-architect.toml` | Refresh into repository-adapted archetype; preserve model settings and strong architecture judgment. |
| `agents/codex/frontend-architect.toml` | Refresh into repository-adapted archetype; preserve interaction/state focus. |
| `agents/codex/implementer.toml` | Replace old exhaustive-plan/universal-TDD assumptions with bounded write-set execution and no Git authority. |
| `agents/codex/qa-auditor.toml` | Strengthen into the adversarial, evidence-bound, report-only auditor defined in this plan. |
| install scripts and config snippets | Remove from the plugin runtime. Use Codex marketplace installation and explicit Init/Agent Team flows. |
| bundled Superpowers assets | Replace with original Plumbline branding. |

---

## 15. Plan amendment and recovery rules

During implementation:

- Mark a checkpoint `In Progress` before substantive work.
- Record each checkpoint commit and verification evidence immediately after integration.
- If Codex behavior invalidates the planned architecture, mark the checkpoint `Blocked`, record the evidence, amend this plan, and continue only after the new approach is coherent.
- If an implementation deviation preserves product behavior and canonical architecture, record it in the checkpoint without reopening product shaping.
- If a deviation changes product behavior or an acceptance criterion, ask one blocking product question and amend the specification after approval.
- If QA or UAT finds a defect, reopen the affected checkpoint and append a corrective commit.
- Do not remove or silently rewrite a skipped requirement. Mark it Blocked, Reopened, or Superseded with coverage elsewhere.
- After context compaction or a new task, recover by reading the active specification, this plan, `git log`, `git status`, the current checkpoint, and the last verified commit. Do not rely on a chat summary as the execution source of truth.

---

## 16. Final release definition of done

Plumbline v1 is complete only when all of the following are true:

- The plugin installs through the current Codex plugin browser or configured marketplace.
- Installation is inert in an uninitialized repository.
- Explicit one-off and side-door skills work without initialization.
- Explicit Init creates only approved local integration.
- The local router produces proportional automatic guidance and is easy to delete.
- Direct work remains light.
- Imported designs enter at the latest safe phase.
- Plan-based work creates durable source/spec/plan artifacts and a kickoff commit.
- Plans remain live and resumable through checkpoint updates.
- Execute enforces sole Git writer and disjoint parallel ownership.
- Runtime testing is value-based rather than universal.
- Diagnose remains proportional.
- QA is adversarial, report-only, and bounded.
- UAT corrections reopen the plan and append corrective commits.
- Closeout reconciles canonical docs, removes transient artifacts, and preserves history.
- Agent Team can create or audit repository-adapted TOMLs while preserving model choices.
- Conflict detection is reversible and approval-based.
- Offboarding uses the local router as the single kill switch and preserves useful assets.
- No predecessor bloat or universal bootstrap has reappeared.
- All 64 specification acceptance criteria have current evidence.
- The user has completed the release UAT and explicitly accepted the plugin.

---

## 17. Technical validations that do not require another product discussion

Resolve these during implementation and record evidence:

1. Whether the local router can invoke explicit public phase skills directly.
2. Whether wrapper/engine pairs are necessary.
3. Whether plugin-root shared references are readable from installed cache paths.
4. Whether the root-level plugin can be referenced from a repo marketplace with `source.path: "./"`.
5. The minimum metadata required for polished per-skill presentation.
6. The exact current configuration format for skill/plugin disablement.
7. Whether an untracked `.worktreeinclude` is honored.
8. How existing managed worktrees receive newly created router and agent files.
9. How to smoke-test custom-agent model selection without repository mutation.
10. Cross-platform safe-link and shared-venv import-origin behavior.
11. The largest imported attachment Plumbline should safely commit before falling back to a Markdown extraction and provenance pointer.
12. The most reliable invocation-evaluation harness available in current Codex.

Only return to the user when evidence shows that an agreed product behavior cannot be achieved without changing the user experience.

---

## 18. Suggested kickoff prompt for the fresh implementation task

Use this or equivalent wording after creating the new repository and attaching the three handoff inputs:

```text
Build Plumbline v1 from the attached approved design specification and implementation handoff plan.

Treat the specification as the product authority and the handoff plan as the live execution authority. Also inspect the attached superpowers-personal archive and the current mattpocock/skills and obra/superpowers repositories as design sources.

Start with CP-00 only:
- inspect the empty/new repository and current Codex environment;
- copy the spec and plan into tracked transient docs;
- pin source provenance;
- create the kickoff commit;
- update the live plan state;
- stop and report the exact baseline and any actual platform contradiction.

Do not begin plugin implementation before the kickoff commit. Do not reopen product decisions unless current Codex capabilities make the approved behavior infeasible.
```

---

## 19. Handoff status

The product specification is approved. No remaining product-level question blocks implementation planning or repository bootstrap.

The implementing agent should begin with CP-00 in a fresh task and use this document as the live checkpoint plan. Any future questions should arise from demonstrated Codex capability constraints, not from a desire to replay the completed design discussion.
