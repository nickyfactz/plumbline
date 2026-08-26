# Runtime-value testing

Tests are a risk-control decision, not a ritual. Start with behavioral proof obligations: the observable behavior, invariant, public/interface contract, meaningful regression risk, or durable edge case that must remain true. Add a permanent test when it protects stable behavior at a public seam or catches a plausible regression that other checks would miss. Prefer one valuable test over many implementation-coupled tests.

Good seams include a CLI/API boundary, user-visible workflow, public service contract, persisted state transition, or integration behavior with a known failure mode. Expected values should come from the specification, a worked example, or an independent known-good source.

Use three evidence classes. A diagnostic probe answers a hypothesis or
reproduction question and is working evidence, not an acceptance attempt. A
focused verification checks the smallest relevant correction path. Acceptance
evidence is the selected proof that closes the checkpoint, whether focused or
full. Keep diagnostic and focused outputs only while they aid the current
decision; record their compact conclusion rather than preserving every log,
manifest, package, or binary. A failure does not promote working output into a
durable attempt. Do not reseal, rebuild, or replay an expensive gate solely
because a diagnostic, launcher, harness, or evidence presentation changed when
the candidate, relevant inputs, contract, environment, and proof boundary are
unchanged.

Allowed outcomes are: a focused automated test; a static/type/lint check; a deterministic command or HTTP probe; manual UAT; a targeted review; or a documented no-test decision with the risk and compensating evidence. A literal configurable default, prose, private method, snapshot of incidental structure, or a trivial wiring change usually does not deserve a permanent test.

For bugs, test the minimized failure at a correct public seam when one exists. If no seam can reproduce the real issue, record the seam gap instead of adding false confidence. Never require red-green-refactor for every configuration, documentation, refactor, or maintenance change.

Throwaway prototypes and implementation-time diagnostics may use a one-command smoke run or documented observation instead of a permanent production test suite. They still need enough runtime evidence to answer the stated question. If prototype logic is promoted into a production seam, re-evaluate it under this gate rather than treating the throwaway probe as permanent coverage.

Implementation may reveal a new durable proof obligation. Add it to the existing
checkpoint evidence surface when it changes what completion means; do not create
a parallel testing artifact. Before completion, review only tests, probes,
snapshots, and checks introduced or materially changed by the candidate. Classify
each as retain for durable protection, generalize or consolidate, remove as
diagnostic-only, or retain with named residual risk. Test count and coverage are
signals for that review, not objectives or acceptance gates.

Before an expensive package, deployment, restart, or live-stack check, run the
cheapest applicable prerequisite probes first: verify required inputs or
resources, the target artifact or revision, target availability/readiness, and
the visibility of the relevant logs or signals. Keep these probes proportional
and omit them for purely local or static work. Before live observation, state a
bounded observation window and an escalation condition appropriate to the
environment. Stop when a prerequisite fails, the artifact is wrong, a named
stop condition occurs, or repeated observations add no new evidence; classify
the result and diagnose instead of retrying indefinitely. Do not hardcode a
universal retry count.

Reuse a still-valid build, package, deployment, or verification result. Create a
new output only when a relevant source/configuration input changed, the existing
object cannot prove the required behavior in the target environment, or reuse
would be less reliable than regeneration. At acceptance, keep the result and
the smallest useful command, revision, counts or failure tail, and artifact
pointer; the generated output itself remains scratch unless deployment,
recovery, audit, safety, or costly reproduction requires it.

## Deterministic operations

Keep known commands and singleton operations with the main thread or a named
project owner: builds, deployments, restarts, migrations, package publication,
and other actions that have one authoritative invocation or shared side effect.
Workers may recommend a command, inspect its result, or run disjoint checks;
they do not duplicate the owner operation. Record the command, owner, artifact,
and result at the main-thread join so downstream work uses one authoritative
state.
