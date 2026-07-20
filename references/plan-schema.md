# Live plan schema

For a blank repository, begin the live plan with:

```yaml
---
status: active
feature: <name>
specification: <relative path>
source: <relative path or null>
base_commit: <kickoff sha>
current_checkpoint: CP-01
checkpoint_status: Pending
lifecycle_owner: Plumbline Plan
last_verified_commit: <sha or null>
next_safe_action: <one sentence>
ready_for_acceptance: false
---
```

Use one feature and one plan. Each checkpoint should use:

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

The frontmatter fields `current_checkpoint`, `checkpoint_status`, `lifecycle_owner`, `last_verified_commit`, and `next_safe_action` are the single compact resume record. Update them together when the active checkpoint or safe next action changes; do not create a second checkpoint receipt. Checkpoints are coherent milestones, not micro-task transcripts. `Blocked` and `Reopened` stop advancement. Update the plan before changing the active checkpoint, after evidence, and after every correction. A fresh task should read this record first, then the exact referenced sections, the spec/source, `git status`, `git log`, and the last verified commit.

Treat `last_verified_commit` and checkpoint completion evidence as the baseline until a material trigger invalidates them. At the next checkpoint, inspect the current delta and referenced paths first. Reuse unchanged evidence instead of rereading whole documents or rerunning broad checks. Reassess when a task or checkout resumes, relevant source/spec/plan/config/agent files change, a new or failed check matters, a contract boundary changes, a defect appears, or the prior evidence may be stale.
