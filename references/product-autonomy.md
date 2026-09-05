# Product autonomy

The user owns product intent. The active host's main thread owns ordinary engineering judgment.

Treat explicit user instructions as authoritative over Plumbline defaults and process preferences, but interpret them in the context of the user's stated outcome, approved artifacts, and repository evidence. Do not follow an ambiguous instruction literally when doing so would contradict the apparent goal, approved contract, or safety boundary. Resolve ordinary ambiguity with a safe reversible default; ask a focused product question only when competing interpretations would materially change behavior.

Ask a question only when different answers materially change product behavior or scope, user experience, privacy/security posture, destructive data handling, compatibility expectations, material cost, or another hard-to-reverse product consequence. Do not ask the user to choose module boundaries, function signatures, adapters, schema normalization, test seams, model names, or file locations when repository evidence can settle them.

Separate technical uncertainty from product uncertainty. The architect should resolve implementation mechanisms, state ownership, lifecycle details, compatibility mechanics, and proof seams from repository evidence, research, and reversible defaults. Escalate only the remaining material product decision: the behavior, scope, user experience, trust boundary, compatibility promise, or other consequence the user actually owns.

Ask one question at a time by default. During Shape, use a small batch only
when the questions are independent frontier decisions whose answers do not
change one another's meaning. Use this shape for every question:

> **Recommendation:** choose X because it best fits the stated outcome and repository evidence. **Alternatives:** Y and Z. **Tradeoff:** the product consequence of each. **Default:** X if you have no preference.

If the choice is reversible, make the recommendation and continue. During Shape or before plan approval, if the answer is blocking, stop before implementation and record the decision in the active specification. Once an approved specification and plan are under Execute, they are delegated product authority: the main orchestrator resolves ordinary in-scope ambiguity with the approved outcome, repository evidence, and a safe reversible default, then records the decision or residual risk. A worker's product-question label does not itself reopen Shape or stop execution. Never silently change an approved product decision because the implementation is inconvenient; stop only for an explicit user gate, destructive action, or contradiction with no safe in-scope default.

When a delegated architect discovers a material product question inside an active goal, return it to the main orchestrator rather than asking the user from the child or taking lifecycle control. The escalation should identify the affected checkpoint and overall objective, explain the user-visible consequence in plain language, and include the recommendation, realistic alternatives, tradeoff, default, whether only that checkpoint is blocked, and what independent work can continue. The main orchestrator uses the existing Shape conversation, preserves the active goal and plan, and records the answer or residual uncertainty in the controlling artifact.

## Plain-language recovery

When the user signals confusion or asks for a re-explanation, pause the current
decision long enough to restate the overall outcome, the current choice, the
realistic alternatives, and the tradeoff in plain language. Reuse the project's
established terms and the controlling artifact's relevant section. Treat this
as an explanation request, not as a new phase, product decision, or document
creation trigger. Resume the existing work once the user has the needed
context; ask a new product question only if the explanation exposes a genuine
choice they own.
