# Architect-to-Shape Product Question Boundary Specification

## Source and Status

- **Source:** Chat-derived product clarification from the Plumbline owner, informed by execution feedback from a long-running migration.
- **Status:** Implemented and verified; retained as a decision record.
- **Scope owner:** Plumbline workflow behavior.
- **Related design authority:** `docs/specs/plumbline-v1.md`, especially the product-autonomy, Shape, Specification, and Plan sections.
- **Next phase:** The architect-to-Shape behavior is complete. The Execute full-plan completion follow-up is tracked separately and is not part of this specification.

## Product Outcome

Reduce implementer guesses and avoidable main-thread repair by making material architecture decisions explicit before implementation, while keeping the user responsible for product behavior and experience decisions rather than low-level software design.

A non-specialist user should be able to answer the questions Plumbline asks. The architect should absorb technical complexity, research established approaches, and make ordinary engineering decisions without delegating that burden back to the user.

## Users and Workflows

This behavior coordinates five roles:

- **User:** decides desired behavior, experience, scope, privacy, compatibility, cost, and other material product consequences.
- **Architect:** resolves technical uncertainty, identifies relevant invariants, and translates material risks into implementable acceptance behavior.
- **Shape:** asks one plain-language product question only when user intent is genuinely required.
- **Plan:** preserves the decision as a checkpoint contract and maps it to proof.
- **Implementer and QA:** implement and independently verify the same contract without inventing missing product behavior.
- **Main orchestrator:** owns the active goal, user conversation, lifecycle, checkpoint advancement, and decision about whether independent work may continue.

The workflow applies to both initialized and uninitialized repositories and to user-supplied specifications or plans from outside Plumbline.

## Scope

This specification covers:

- recognizing when a technical uncertainty implies a material product decision;
- resolving ordinary technical ambiguity without asking the user for implementation choices;
- returning to Shape with one useful product question when the architect cannot safely infer behavior;
- creating a compact, conditional acceptance matrix for material stateful, security-sensitive, public-contract, persistence, concurrency, or cross-boundary work;
- carrying that matrix from architecture through planning, implementation, and QA.

The behavior is project-agnostic and applies across languages, frameworks, repositories, and model providers.

## Non-Goals

This specification does not:

- encode Rust, Python, FFI, package-layout, or migration-specific rules;
- require a matrix for mechanical, trivial, or low-risk work;
- create a new skill, artifact type, tracker, dependency, or agent hierarchy;
- require the user to choose modules, adapters, schemas, function signatures, test seams, or state-storage mechanisms;
- encode specific model slugs or reasoning levels;
- couple Plumbline to a usage monitor or cost-attribution system;
- force exhaustive state enumeration or exhaustive architecture design before useful work begins.

## Domain Language and Invariants

### Technical uncertainty

A question about how to implement or verify a behavior. The architect owns it when repository evidence, research, or a bounded prototype can settle it.

Examples include module boundaries, adapter placement, data structures, concurrency primitives, retry mechanisms, and test seams.

### Product uncertainty

A question whose answer changes what the user experiences, what the system promises, what data may be lost or exposed, compatibility, destructive handling, material cost, or another difficult-to-reverse outcome. Shape owns this question with the user.

### Material risk

A risk involving state ownership, persistence, concurrency, security, public contracts, compatibility, recovery, shutdown, or cross-boundary behavior where an incorrect assumption can invalidate acceptance.

### Acceptance matrix

A compact set of applicable scenarios mapping:

`scenario -> expected observable behavior, terminal owner/order, and proof`

It is part of an existing specification or checkpoint, not a new artifact. It is expanded only for material risk.

### Core invariants

1. The user decides product behavior; the agent decides ordinary implementation details.
2. The architect must resolve technical uncertainty before escalating to the user.
3. A user question must be phrased in observable product terms, not implementation jargon.
4. A missing answer blocks only when it materially changes product behavior or acceptance.
5. Non-blocking uncertainty remains an assumption, residual risk, or fog item.
6. The same accepted behavior must be visible to the plan, implementer, and QA reviewer.
7. The workflow remains proportional: no matrix or additional question for work that does not need it.
8. A delegated architect never becomes the owner of the long-running goal and never ends or blocks the goal as a whole merely because it found a product question.

## Required Behavior

### 1. Architect-first resolution

When a material risk is detected, the architect first:

- inspects repository code, tests, specifications, and canonical documentation;
- researches current external standards or established patterns when needed;
- uses a bounded prototype or focused probe when behavior is cheaper to observe than debate;
- identifies the smallest set of scenarios that can affect acceptance;
- chooses a reversible technical default when product behavior is unaffected;
- records assumptions and residual uncertainty.

The architect must not return to Shape merely because a low-level technical choice is unfamiliar or because several implementation approaches are possible.

### 2. Product-question escalation

Return to Shape only when the remaining uncertainty changes a material product outcome and cannot be safely inferred from evidence or a reversible default.

Shape asks one question at a time using:

- **Context:** what situation needs a decision;
- **Plain-language question:** what the user will experience or what promise the product should make;
- **Recommendation:** the architect's preferred behavior and why;
- **Alternatives:** credible product-level alternatives;
- **Tradeoff:** the consequence of each option;
- **Default:** the recommended choice if the user has no preference.

The question must explicitly explain why it is being asked and must not ask the user to select an implementation mechanism.

For example, ask whether an interrupted operation should appear as pending and retryable or failed and user-retryable. Do not ask the user to choose between idempotency keys, an outbox, a saga, or a particular state-machine implementation.

If the user does not know, preserve that uncertainty, recommend the safest reversible default, and continue with independent decisions where possible. Stop only if the product behavior genuinely cannot proceed without the answer.

### 2a. Delegated escalation inside an active goal

When an architect is dispatched for a scoped checkpoint inside a long-running goal, it must return a structured escalation to the main orchestrator rather than directly changing lifecycle ownership or ending the goal. The escalation includes:

- the affected checkpoint and the overall feature objective it serves;
- the plain-language product question;
- why the answer changes observable behavior or acceptance;
- the architect's recommendation, alternatives, tradeoffs, and default;
- whether the current checkpoint is blocked;
- which independent work remains safe to continue.

The main orchestrator reconciles the question against the active specification and the overall objective. It may answer from an already-approved product decision, ask the user through the existing Shape conversation, record a residual assumption, or pause only the affected checkpoint. It must not terminate the `/goal`, discard the active plan, start a competing lifecycle, or force the user to restart shaping for the entire feature.

If the question is material but local to the checkpoint, the main orchestrator may keep the broader goal active while that checkpoint is `Blocked` or `Reopened` and continue independent checkpoints when their dependencies permit. A user-facing Shape question is an escalation within the active goal, not a new goal.

### 3. Conditional acceptance matrix

For a material checkpoint, the architect or planner creates a compact matrix containing only applicable cases. Possible categories include:

- normal completion;
- cancellation, timeout, or bounded shutdown;
- late, duplicate, or reordered input;
- partial failure and recovery;
- already-issued or in-flight effects;
- compatibility or migration behavior;
- security rejection, authorization failure, or integrity mismatch;
- restart or process interruption.

Each selected row states the expected observable behavior, ownership or terminal ordering when relevant, and the proof that will establish it.

The matrix remains inside the active specification or checkpoint card. It must not become a separate checklist or require exhaustive enumeration.

### 4. Propagation through execution

The plan maps each matrix row to a checkpoint acceptance criterion or proof seam. The implementer receives the applicable rows in the bounded brief. QA reviews the same rows independently after the stable implementer delta is integrated.

A missing or contradictory row is a contract issue. It returns to architecture or Shape as appropriate; it is not silently resolved by expanding the implementer's write set.

### 5. Gate and evidence behavior

For high-risk work, perform independent QA after focused proof and before expensive broad, package, or live-stack gates when practical. A cheap focused check may still run before QA when it helps establish the stable delta.

When a gate fails, classify the result compactly as one of:

- product defect;
- acceptance or contract gap;
- environment;
- test harness;
- known unrelated baseline;
- evidence unavailable.

Record the classification and next action once. Do not treat environment or harness retries as model remediation or create a new ceremony receipt for every retry.

## Failure and Recovery Behavior

- If the architect cannot infer a material product behavior, return to Shape with one recommended, plain-language question.
- If the architect is a delegated checkpoint worker, return that question and its impact to the main orchestrator; do not ask it as an autonomous lifecycle owner or end the active goal.
- If the question is actually about implementation, resolve it within architecture and do not expose it to the user.
- If the user declines or cannot answer, preserve the uncertainty as fog or a residual assumption and continue when the decision is non-blocking.
- If the decision is blocking, keep the checkpoint from advancing and record the reason.
- A blocked checkpoint does not make the whole long-running goal blocked when independent work can proceed safely.
- If implementation or QA reveals a missing product behavior, amend the specification with explicit user approval.
- If implementation reveals a missing technical invariant while product intent remains settled, return to architecture or Plan rather than re-grilling the user.
- If a failure is caused by the environment or harness, preserve the product evidence and repair or rerun the relevant check without reopening product design.

## Compatibility, Data, Privacy, and Security Constraints

- Guidance must remain language- and framework-agnostic.
- No model, reasoning, sandbox, or agent role becomes mandatory because of this behavior.
- Existing external specifications, plans, and repository conventions remain valid.
- No user prompt, transcript, secret, or unrelated repository content is copied into a new artifact unnecessarily.
- Security, privacy, authorization, integrity, and destructive behavior remain product-relevant escalation triggers when their consequences affect the user or system boundary.
- The optional usage monitor remains independent and may consume evidence only through its own observation or optional generic receipts.

## Acceptance Criteria

1. A material stateful or trust-boundary example produces a compact applicable scenario-to-proof matrix before implementation.
2. A mechanical or low-risk example does not produce a matrix or additional product question.
3. A technical design choice that does not alter product behavior is resolved by the architect without user escalation.
4. A genuine product ambiguity returns to Shape as one plain-language question with recommendation, alternatives, tradeoffs, and default.
5. The question explains why the user is being asked and does not ask for a low-level implementation choice.
6. The matrix is available to the plan, implementer, and QA reviewer through the existing artifacts and briefs.
7. Missing contract behavior causes an appropriate architecture, Plan, or Shape return rather than an unbounded implementer guess.
8. Environment and harness failures remain distinguishable from product defects and contract gaps.
9. Existing imported specifications and plans can be adopted without re-grilling settled decisions.
10. No new mandatory artifact type, agent, dependency, tracker, model policy, or monitor integration is introduced.
11. A checkpoint architect's product question returns to the main orchestrator with its checkpoint impact and safe-continuation status.
12. The main orchestrator can ask the user without ending the active goal or restarting whole-feature shaping.
13. A material unanswered question blocks only the dependent checkpoint unless the overall objective genuinely depends on it.
14. The active specification, plan, and lifecycle owner remain intact while the question is resolved.

## Testing and Acceptance Strategy

Use focused workflow fixtures rather than repository-specific implementation tests:

- a generic stateful operation with ambiguous interruption behavior;
- a generic security or package boundary with an incomplete rejection rule;
- a mechanical change that should remain direct;
- a technical choice that repository evidence can settle;
- a product ambiguity that requires one user-facing Shape question;
- a user who answers that they do not know;
- an imported specification that already settles behavior;
- an environment failure that must not be reported as an implementation defect.

Validate with the existing static validator, targeted skill/evaluation fixtures, and `git diff --check`. Do not require a full model benchmark or cost claim to accept the workflow change.

## Canonical Documentation Impact

If approved, update only the existing guidance surfaces that carry this behavior:

- `references/product-autonomy.md`;
- `references/subagent-orchestration.md`;
- `skills/plumbline-shape-engine/SKILL.md`;
- `skills/plumbline-plan-engine/SKILL.md`;
- `skills/plumbline-execute-engine/SKILL.md`;
- `references/qa-audit.md` if failure-origin wording is added;
- relevant evaluation prompts and expected behavior;
- README behavior guidance if the user-facing contract changes.

Do not create a separate permanent architecture manual for this refinement. The current v1 specification remains the broader design authority.

## Decisions and Rejected Alternatives

### Decisions

- Technical ambiguity belongs to the architect.
- Product ambiguity belongs to Shape and the user.
- Material risk uses a compact acceptance matrix.
- Questions must be understandable to a non-specialist product owner.
- Evidence and gate failures retain their origin classification.

### Rejected alternatives

- Asking the user to choose technical mechanisms.
- Requiring a universal architecture checklist.
- Adding language-specific rules based on one Python-to-Rust migration.
- Adding more agent hierarchy or a dedicated acceptance persona.
- Making model slugs or reasoning levels part of the contract.
- Coupling Plumbline to the external usage monitor.
- Splitting every stateful implementation into additional checkpoints.

## Assumptions and Residual Questions

- The existing Shape and Plan engines can carry the matrix without a new artifact type.
- The host can return to the Shape side door when the architect identifies a product ambiguity.
- A compact matrix can be kept small enough that it reduces rework without recreating ceremony.
- The evaluation fixtures will be sufficient to detect whether implementers make fewer unsupported assumptions.
- No additional product decision is required to draft this behavior; implementation requires explicit approval of this specification.
