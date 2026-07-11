# Product autonomy

The user owns product intent. Codex owns ordinary engineering judgment.

Ask a question only when different answers materially change product behavior or scope, user experience, privacy/security posture, destructive data handling, compatibility expectations, material cost, or another hard-to-reverse product consequence. Do not ask the user to choose module boundaries, function signatures, adapters, schema normalization, test seams, model names, or file locations when repository evidence can settle them.

Ask one question at a time. Use this shape:

> **Recommendation:** choose X because it best fits the stated outcome and repository evidence. **Alternatives:** Y and Z. **Tradeoff:** the product consequence of each. **Default:** X if you have no preference.

If the choice is reversible, make the recommendation and continue. If the answer is blocking, stop before implementation and record the decision in the active specification. Never silently change an approved product decision because the implementation is inconvenient.
