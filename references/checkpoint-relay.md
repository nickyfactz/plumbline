# Checkpoint Relay execution contract

Checkpoint Relay is an explicit execution mode for plans that should cross a
fresh root-conversation boundary after each completed checkpoint. It changes
checkpoint traversal, not product scope, planning authority, delegation, or
acceptance.

## Mode resolution

- A missing `execution_mode` means `continuous`.
- `continuous` preserves normal Execute behavior: traverse every remaining
  dependency-safe checkpoint in the current lifecycle.
- `checkpoint_relay` executes only the current checkpoint in the current root
  conversation, establishes a durable handoff, and stops before downstream
  work begins.
- Never infer Relay from plan size, checkpoint count, or host availability, and
  never silently change an existing plan's mode.

## Capability resolution

After an explicit Relay plan passes readiness, resolve one host capability:

- `automatic`: the host can start and observe a fresh root conversation;
- `manual`: the user must start the next root conversation.

Automatic capability changes only who starts the successor conversation. Both
paths use the same plan, transition rules, durable handoff, and acceptance
state. An unsupported or unavailable automatic adapter therefore degrades to a
manual boundary; it does not make the plan invalid or mutate the mode.

## Checkpoint boundary

A Relay checkpoint may hand off only when:

1. the current checkpoint is `Complete`;
2. its required proof is recorded;
3. downstream-relevant decisions, corrections, assumptions, constraints, and
   discovered invariants exist in authoritative artifacts;
4. exactly one dependency-safe successor is current, or the plan is `Ready for
   Acceptance`;
5. `checkpoint_status` and `next_safe_action` agree with that state; and
6. the repository has the recovery boundary required by the plan.

The current conversation then stops. It must not execute the successor
checkpoint, reinterpret arbitrary source prose, create an extra handoff file,
or treat transport state as repository authority.

If the automatic capability is available, the host adapter may start one fresh
root conversation from the normalized checkpoint request. Otherwise report the
completed checkpoint and tell the user to start a fresh conversation against
the same repository and invoke Plumbline to continue. Do not ask the user to
repeat settled context.

## Fail-closed states

`Blocked`, `Reopened`, failed or inconclusive proof, an approval gate, ambiguous
current state, an invalid dependency transition, or an unavailable recovery
boundary pauses Relay. A pause never advances the plan or starts another root
conversation. Ordinary continuous Execute remains unchanged.

The automatic controller keeps only disposable host-local task identity,
fingerprint, lock, wake, and control state. On restart it reconciles the prior
task before dispatch: a legal durable transition is adopted, an active or
unknown task stops duplicate work, and fingerprint drift pauses. `--pause` and
`--stop` change only host-local controller state; they never edit the plan.
Transport failure also pauses without retrying engineering work. A stale lock
is removed only when its recorded process is provably gone.
