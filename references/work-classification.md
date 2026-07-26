# Work classification

Start with the smallest evidence pass that can classify the request. User instructions override the default classification, and hidden complexity may escalate the work after repository research.

| Class | Use when | Default handling |
| --- | --- | --- |
| Direct | Small, clear, low-risk maintenance such as a typo, one config value, or a local docs correction; or a supplied work order whose scope, proof, owner, and closeout are already complete | Work in place; do not recreate Plumbline artifacts or ceremony unless evidence exposes a missing product decision or phase boundary |
| Scoped | A clear product outcome crosses a few files or needs isolated implementation | Use a short specification/plan and a Codex-managed worktree when available |
| Designed | Product ambiguity, durable contracts, migrations, privacy/security, compatibility, or broad seams matter | Shape or adopt a design, then create one spec and one checkpoint plan |
| Diagnose | A defect, regression, failure, or performance problem is the outcome | Build the smallest red-capable signal and find the root cause |
| Review | The user wants an independent correctness/completeness audit | Report only; do not mutate the work |
| Closeout | Accepted work needs docs reconciliation, transient cleanup, or local integration | Preserve history and ask before destructive cleanup |

Technical breadth alone does not split one feature into multiple plans. A complete work order can keep a broad implementation task direct when no product decision or plan advancement remains. If a direct change reveals hidden risk, state the escalation and why. Direct work stays direct when the evidence supports it.
