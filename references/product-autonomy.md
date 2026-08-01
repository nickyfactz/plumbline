# Product autonomy

The user owns product intent. Codex owns ordinary engineering judgment.

Ask a question only when different answers materially change product behavior or scope, user experience, privacy/security posture, destructive data handling, compatibility expectations, material cost, or another hard-to-reverse product consequence. Do not ask the user to choose module boundaries, function signatures, adapters, schema normalization, test seams, model names, or file locations when repository evidence can settle them.

Separate technical uncertainty from product uncertainty. The architect should resolve implementation mechanisms, state ownership, lifecycle details, compatibility mechanics, and proof seams from repository evidence, research, and reversible defaults. Escalate only the remaining material product decision: the behavior, scope, user experience, trust boundary, compatibility promise, or other consequence the user actually owns.

Ask one question at a time. Use this shape:

> **Recommendation:** choose X because it best fits the stated outcome and repository evidence. **Alternatives:** Y and Z. **Tradeoff:** the product consequence of each. **Default:** X if you have no preference.

If the choice is reversible, make the recommendation and continue. If the answer is blocking, stop before implementation and record the decision in the active specification. Never silently change an approved product decision because the implementation is inconvenient.

When a delegated architect discovers a material product question inside an active goal, return it to the main orchestrator rather than asking the user from the child or taking lifecycle control. The escalation should identify the affected checkpoint and overall objective, explain the user-visible consequence in plain language, and include the recommendation, realistic alternatives, tradeoff, default, whether only that checkpoint is blocked, and what independent work can continue. The main orchestrator uses the existing Shape conversation, preserves the active goal and plan, and records the answer or residual uncertainty in the controlling artifact.
