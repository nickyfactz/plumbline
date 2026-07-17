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
last_verified_commit: <sha or null>
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

Checkpoints are coherent milestones, not micro-task transcripts. `Blocked` and `Reopened` stop advancement. Update the plan before changing the active checkpoint, after evidence, and after every correction. A fresh task should recover from this file, the spec/source, `git status`, `git log`, and the last verified commit.

Treat `last_verified_commit` and checkpoint completion evidence as the baseline until a material trigger invalidates them. At the next checkpoint, inspect the current delta and referenced paths first. Reuse unchanged evidence instead of rereading whole documents or rerunning broad checks. Reassess when a task or checkout resumes, relevant source/spec/plan/config/agent files change, a new or failed check matters, a contract boundary changes, a defect appears, or the prior evidence may be stale.
