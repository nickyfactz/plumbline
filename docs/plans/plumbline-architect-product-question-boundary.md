---
status: complete
feature: architect-to-shape product question boundary
specification: ../specs/plumbline-architect-product-question-boundary.md
source: null
base_commit: daf4a5647d429f574e883373ede73568f25282e7
current_checkpoint: CP-02
checkpoint_status: Complete
lifecycle_owner: Plumbline Closeout
last_verified_commit: daf4a5647d429f574e883373ede73568f25282e7
next_safe_action: Future separate work: specify and implement default full-plan Execute traversal; no remaining checkpoints in this plan.
ready_for_acceptance: true
---

# Architect-to-Shape Product Question Boundary Implementation Plan

## Feature Outcome

Make material architecture uncertainty actionable without handing low-level design decisions to the user or interrupting a long-running goal. The architect resolves technical choices, produces a compact acceptance matrix for material risks, and returns product questions to the main orchestrator. The main thread may ask the user within the active goal while preserving the plan, lifecycle owner, and independent work.

## Global Constraints

- Keep the behavior project-, language-, framework-, and provider-agnostic.
- Do not encode Python, Rust, FFI, packaging, migration, or repository-specific examples into shared guidance.
- Do not create a new skill, artifact type, agent role, dependency, tracker, monitor integration, or workflow hierarchy.
- Use the existing specification, plan, checkpoint, Shape, orchestration, and QA surfaces.
- Require the acceptance matrix only for material state, persistence, concurrency, security, public-contract, compatibility, recovery, or cross-boundary risk.
- Do not require user choices about modules, adapters, schemas, function signatures, test seams, concurrency primitives, or other implementation mechanisms.
- Preserve convention mode, imported-artifact adoption, lightweight direct work, and the existing main-thread Git boundary.
- A delegated architect must return to the main orchestrator; it must not own, end, or globally block a long-running goal.
- Model and reasoning settings remain adjustable recommendations and are outside this feature.
- Do not commit or push unless the user explicitly requests publication.

## Execution Topology

This is a tightly coupled documentation and evaluation change. The main thread will implement it directly; no delegation wave is needed.

Execute the checkpoints serially because CP-02 validates the exact wording and boundaries established by CP-01. Do not create a separate checkpoint for each guidance file or evaluation fixture.

## Shared Ownership

| Surface | Owner | Boundary |
| --- | --- | --- |
| Active specification and plan | Main thread | Only the main thread amends lifecycle state and product decisions |
| Shared guidance files | Main thread | Update as one coherent contract; no parallel edits |
| Evaluation prompts and expectations | Main thread | Generic behavior fixtures only |
| Runtime behavior | None in this feature | Guidance-only; no application or installer runtime changes |
| Usage monitoring | External monitor | No Plumbline coupling or telemetry changes |

## Checkpoint Index

1. **CP-01 - Encode the upstream architect, Shape, and main-orchestrator contract**
2. **CP-02 - Encode execution evidence behavior and validate lightweight workflow boundaries**

---

## CP-01: Encode the upstream architect, Shape, and main-orchestrator contract

**Status:** Complete

| Boundary | Guidance behavior and documentation only; no runtime code |
| --- | --- |
| Read set | Approved specification, current v1 design authority, existing Shape/autonomy/orchestration/Plan guidance |
| Write set | references/product-autonomy.md, references/subagent-orchestration.md, skills/plumbline-shape-engine/SKILL.md, skills/plumbline-plan-engine/SKILL.md |
| Ownership | Main thread owns all edits and the plan |
| Delegation | Direct; no worker needed |
| Acceptance | Technical ambiguity stays with the architect; product ambiguity returns to the main orchestrator as one plain-language question; applicable material risks become a compact scenario-to-proof matrix; the active goal remains intact |

### Outcome

The upstream lifecycle explains what happens before implementation when an architect discovers a product-relevant unknown inside an existing goal.

### Specification coverage

- Architect-first technical resolution.
- Product-question escalation.
- Delegated escalation inside an active goal.
- Conditional acceptance matrix.
- Main-orchestrator ownership.
- Non-specialist user question format.
- No language-specific or model-specific policy.

### Implementation work

1. Add the technical-versus-product uncertainty boundary to the autonomy guidance, including the rule that the architect resolves implementation mechanisms.
2. Add a structured architect escalation shape to the orchestration guidance:
   - affected checkpoint and overall objective;
   - plain-language question;
   - why it changes behavior or acceptance;
   - recommendation, alternatives, tradeoffs, and default;
   - whether the checkpoint is blocked;
   - safe independent work.
3. Update Shape guidance so a delegated escalation is answered by the main orchestrator through the existing Shape conversation rather than by a child owning lifecycle or directly interrupting the goal.
4. Update Plan guidance so material risk is represented as an applicable scenario-to-proof matrix inside the existing checkpoint, without making a universal checklist or extra artifact.
5. Preserve existing artifact adoption, fog, residual-risk, and no-replanning behavior.

### Verification

- Read the resulting guidance as a generic stateful feature, a mechanical change, and an imported external plan.
- Confirm only the generic stateful feature receives the matrix.
- Confirm a delegated architect returns to the main orchestrator and does not terminate or globally block the goal.
- Run git diff --check.

### Completion criterion

The upstream guidance gives the main thread enough information to carry a product question through an active long-running goal while leaving low-level design with the architect.

### Completion evidence

- Updated file list and focused diff.
- Generic behavior review against the approved specification.
- git diff --check success.
- `python scripts/validate.py` passed.

CP-01 is complete. The next checkpoint keeps the same lifecycle owner and adds only downstream execution evidence guidance and proportional evaluation coverage.

---

## CP-02: Encode execution evidence behavior and validate lightweight workflow boundaries

**Status:** Complete

| Boundary | Guidance, evaluation, and static-validation changes only |
| --- | --- |
| Read set | CP-01 guidance, Execute/QA guidance, existing routing and resume fixtures |
| Write set | skills/plumbline-execute-engine/SKILL.md, references/qa-audit.md, relevant evals/prompts/ and evals/expected/ files |
| Ownership | Main thread owns all edits and validation |
| Dependencies | CP-01 complete and its wording stable |
| Acceptance | QA ordering and failure-origin classification are explicit; evaluation coverage proves the workflow remains proportional and goal-preserving |

### Outcome

The downstream execution contract uses the same matrix and distinguishes product defects from environment or harness noise without adding repetitive ceremony.

### Specification coverage

- Matrix propagation to implementer and QA.
- QA before expensive broad/package/live gates when practical.
- Product, contract, environment, harness, baseline, and unavailable-evidence classifications.
- Checkpoint-only blocking.
- No new artifact, hierarchy, model rule, or monitor coupling.

### Implementation work

1. Clarify Execute ordering:
   - focused proof may establish a stable delta;
   - high-risk QA should occur before expensive broad gates when practical;
   - substantial semantic corrections return to the bounded implementer or reopen the checkpoint.
2. Clarify validation-result handling:
   - classify the failure origin before rerunning;
   - record the classification and next action once;
   - do not count harness/environment retries as model remediation.
3. Keep QA report-only and independent, with the existing verdicts and checkpoint reopening behavior.
4. Add generic evaluation coverage for:
   - stateful interruption uncertainty;
   - security or trust-boundary rejection uncertainty;
   - mechanical work with no matrix;
   - technical ambiguity resolved by the architect;
   - product ambiguity returned as one Shape question;
   - a user who does not know;
   - an imported spec adopted without re-grilling;
   - an environment/harness failure kept separate from a product defect;
   - a delegated architect escalation that preserves the active goal and blocks only the dependent checkpoint.
5. Do not add a permanent runtime test suite for prompt wording. Use behavior-level fixtures and existing static validation.

### Verification

Run:

§§§text
python scripts/validate.py
python scripts/test_install_agent_team.py
git diff --check
§§§

Review every new fixture against the project-agnostic constraints. Confirm that the README and existing v1 design authority do not promise a universal matrix or a new required phase.

### Completion criterion

Execution and QA guidance consume the upstream contract consistently, and behavior-level fixtures prove that high-risk work receives stronger acceptance detail while small work remains lightweight.

### Completion evidence

- Updated guidance and evaluation files.
- Static validator output.
- Installer smoke test output.
- git diff --check output.
- A concise residual-risk note for any fixture limitation.

CP-02 completion evidence:

- Updated `skills/plumbline-execute-engine/SKILL.md`, `references/qa-audit.md`, and the existing resume/ownership behavior fixtures.
- `python scripts/validate.py` passed.
- `python scripts/test_install_agent_team.py` passed with `agent-team-installer-smoke=passed`.
- `git diff --check` and the focused untracked-artifact whitespace check passed.
- Shared guidance review found no project- or language-specific terms; the matrix remains conditional and no runtime test suite or new artifact type was added.

---

## Acceptance Map

| Specification acceptance criteria | Checkpoint |
| --- | --- |
| 1-7: matrix, technical/product distinction, question format, propagation, and appropriate escalation | CP-01 |
| 8: environment and harness distinction | CP-02 |
| 9-10: imported artifacts and no new coupling | CP-01 and CP-02 |
| 11-14: main-orchestrator return, active-goal preservation, checkpoint-only blocking, and lifecycle continuity | CP-01 and CP-02 |

## Validation Strategy

### Static validation

- python scripts/validate.py
- python scripts/test_install_agent_team.py
- git diff --check

The installer smoke test is retained as a regression check because agent-team boundaries are referenced by the guidance, but no installer behavior should change.

### Behavioral validation

Use the new generic evaluation fixtures as prompt/expectation pairs. The expected outcomes should check behavior, not exact wording:

- no technical question is passed to the user;
- product questions are plain-language and recommended;
- matrices appear only for material risk;
- delegated escalation returns to the main thread;
- only the dependent checkpoint blocks;
- environment failures are not labeled model defects.

### Runtime-value testing decision

No production runtime test is warranted. This feature changes workflow guidance and evaluation behavior, not application runtime. Focused static validation and behavior-level fixtures are the appropriate proof.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Matrix becomes a universal checklist | Keep it conditional, compact, and inside the existing checkpoint |
| Architect asks the user technical questions | Add explicit examples and require product-language escalation |
| Child architect interrupts a long-running goal | Return escalation to main orchestrator with safe-continuation status |
| Main thread blocks the whole goal for one local unknown | Allow only the dependent checkpoint to block |
| Harness failures look like model failures | Require compact failure-origin labels |
| Guidance becomes language-specific | Use generic state, trust-boundary, compatibility, and lifecycle categories |
| Extra QA adds ceremony | Trigger ordering only for high-risk work and expensive gates |
| Existing external plans are rejected | Preserve artifact-agnostic adoption behavior |

## Residual State and Next Action

- Product decision: settled by the approved specification.
- Technical design: ready for implementation.
- Open product blockers: none.
- Residual implementation risk: wording may be interpreted too broadly; evaluation fixtures must prove proportionality.
- Current checkpoint: CP-02 Complete.
- Lifecycle owner: Plumbline Execute.
- Next safe action: review the stable guidance delta and accept it before Closeout; no commit or push has been requested.
- Operational follow-up outside this plan: a normal Execute invocation should run all remaining serial checkpoints through plan completion; only an explicit checkpoint-by-checkpoint request should select slice mode. Reaching a checkpoint boundary must not end the session when later checkpoints remain.
- This execution-mode follow-up is not an acceptance blocker for the architect-to-Shape contract implemented here.

## Closeout Record

### Specification-to-diff coverage

| Specification criteria | Evidence and changed surfaces |
| --- | --- |
| 1-2: material-risk matrix; lightweight work stays proportional | `skills/plumbline-plan-engine/SKILL.md`, `skills/plumbline-execute-engine/SKILL.md`, `evals/prompts/resume-and-ownership.md`, and matching expectations |
| 3-5: architect resolves technical choices; Shape asks one plain-language product question | `references/product-autonomy.md`, `skills/plumbline-shape-engine/SKILL.md`, and the technical/product ambiguity fixtures |
| 6-7: matrix propagation and contract-gap escalation | `references/subagent-orchestration.md`, `skills/plumbline-plan-engine/SKILL.md`, and `references/qa-audit.md` |
| 8: environment and harness failures remain distinct | `skills/plumbline-execute-engine/SKILL.md`, `references/qa-audit.md`, and the gate-classification fixture |
| 9-10: imported artifacts and no new coupling | Existing artifact-adoption guidance retained; no new skill, artifact type, dependency, agent, tracker, or monitor integration added |
| 11-14: delegated escalation returns to the main thread and preserves the active goal | `references/product-autonomy.md`, `references/subagent-orchestration.md`, Shape/Plan/Execute guidance, and the active-goal escalation fixture |

### Final verification

- `python scripts/validate.py` passed.
- `python scripts/test_install_agent_team.py` passed with `agent-team-installer-smoke=passed`.
- `git diff --check` passed.
- Focused whitespace checks passed for the untracked specification and plan.
- Canonical documentation review found no current-state documentation requiring reconciliation; `README.md` and `docs/specs/plumbline-v1.md` remain accurate.

### Retained transient paths

- `docs/specs/plumbline-architect-product-question-boundary.md`
- `docs/plans/plumbline-architect-product-question-boundary.md`

These artifacts are retained as a decision record and recovery evidence. No deletion, commit, or remote publication was requested in this closeout invocation.

### Residual risk

The workflow change is validated through static checks and behavior-level fixtures, not a live model benchmark. The separate Execute full-plan traversal follow-up remains open for a future Shape/Specification/Plan cycle.
