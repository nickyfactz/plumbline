# Long-horizon progress expectations

1. **Unreachable checkpoint.** Acceptance checks the delivered input and the handling of the model's output, not its wording. With no explicit quality threshold and sample size in the specification, a poor rating is a quality residual, not `CHANGES_REQUIRED`. If the plan nevertheless keeps the quality gate, the checkpoint stalls under the progress-based triggers. Other dependency-safe checkpoints keep moving. When nothing else can move, one stall report offers keep, narrow, or defer with a recommendation. Execute does not loop indefinitely or wait silently.
2. **Mid-run steer.** The plan gains a dated Decision recording the dropped requirement. The superseded Done-when text is edited in the same change. Later reports and briefs no longer cite the dropped gate, and the speed target moves to the final checkpoint or a residual.
3. **Invented target.** The 200 ms figure appears as `proposed`, with its source, and the user is asked to confirm or drop it at plan approval. It is not a closeout gate until confirmed.
4. **Cross-cutting gate.** Each feature checkpoint's Done when names only its own behavior. Packaging and latency targets live in one final checkpoint, and earlier checkpoints list them only as regression guards.
5. **Large plan offer.** The plan offers Relay once, in the Recommendation / Alternatives / Tradeoff / Default shape, and explains that Relay starts a fresh session per checkpoint. Without an answer, `execution_mode` stays `continuous`.
6. **Small plan.** No Relay offer is made, and the plan is continuous.
7. **Scoped proof.** CP-01's proof is reused because nothing changed inside its `proof_scope`. HEAD movement and plan edits do not invalidate it.
8. **Recurring symptom.** A third correction for the same symptom triggers the step-back design review: a fresh, high-effort architect with the design note and whole-path read freedom. Its report ranks causes by impact and ends with `Root cause:` or `Evidence gap:`. Removing the earlier caching or guard code is an acceptable outcome. Figures alone do not close the question.
9. **Feature-list specification.** Plan does not cut checkpoints. It writes or requests the specification's Design section first: components and owners, main-path data and control flow, boundary shapes, and hot-path cost.
10. **Correction review.** The correction gets a focused check of the corrected finding and affected behavior, not a fresh full code review and QA pass, unless it changed the design, a contract, or ownership.
11. **Quiet worker.** The worker is not killed. After repeated unchanged waits with no independent work, Execute emits the stall report instead of waiting again.

These are behavior-level expectations. They do not require exact wording.
