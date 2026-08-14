# Artifact lifecycle

Plumbline uses four artifact classes:

1. Imported source - a design, handoff, attachment, or kickoff prompt from outside the repository. Preserve provenance and hash; treat it as immutable evidence.
2. Active specification - the approved product contract for the current feature. It is tracked, authoritative during execution, and amended only for explicit product decisions.
3. Live implementation plan - the execution control plane. It records checkpoints, owners, dependencies, evidence, blockers, deviations, and recovery state. Keep it current as work advances.
4. Canonical documentation - long-lived project-owned docs describing the repository's actual current system. It is not a diary and is not automatically replaced by a transient plan.

These artifact classes describe responsibilities, not required filenames or formats. A user-supplied external specification, plan, handoff, or work order may be adopted in place. Select one controlling artifact set for the current task; unrelated active artifacts elsewhere in the repository are not blockers.

A repository-local shaping handoff is a pre-specification state of the active specification, not a fifth artifact class. After explicit user approval, it uses the repository's existing transient specification location, records only durable shaping decisions and concise research evidence, and is promoted in place when the specification phase begins. It is never a second active specification.

A throwaway Shape prototype is transient scratch evidence, not a fifth artifact class. Keep it clearly marked and out of production; record only its material finding in the existing handoff or specification, and never promote its code automatically.

Imported source, specs, and plans are lifecycle-owned and may be transient. They may be removed at accepted closeout only after the user explicitly accepts the result and canonical docs contain the resulting truth. Retained specifications and plans may instead become decision records when they remain useful; retention does not make them canonical current-state documentation. Git history must retain deleted artifacts. Never use closeout to hide a disagreement between code and docs; investigate it and record the resolution.

Failed evidence attempts are immutable supporting records. A corrected attempt
supersedes their conclusion; it does not erase or reinterpret the earlier
result. If a safety rollback is required, the main thread must preserve the
candidate in durable Git history before removing it from the active source.
An ignored patch, build directory, or transient target artifact is not enough
to retain a candidate or recover the active objective.

Every process artifact, announcement, or receipt must support recovery, validation, authorization, or ownership. Omit it when it serves none of those purposes.
