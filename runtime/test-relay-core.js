#!/usr/bin/env node
"use strict";

const assert = require("assert");
const fs = require("fs");
const os = require("os");
const path = require("path");
const { execFileSync } = require("child_process");
const { RelayLockError, runAcceptance, runCheckpoint, stateKey } = require("./relay-core.js");
const { setControl, signalRelay } = require("./relay-signal.js");


function git(root, args) {
  return execFileSync("git", args, { cwd: root, encoding: "utf8" }).trim();
}


function planText(current = "CP-01", cp01 = "Ready", cp02 = "Pending") {
  return `---
status: active
objective: Prove relay core transitions.
source: source.md
execution_mode: checkpoint_relay
current_checkpoint: ${current}
checkpoint_status: ${current === "CP-01" ? cp01 : cp02}
next_safe_action: Execute ${current}.
ready_for_acceptance: false
---

## CP-01: First
**Status:** ${cp01}
| Dependencies | none |
| Acceptance | first proof exists |

## CP-02: Second
**Status:** ${cp02}
| Dependencies | CP-01 |
| Acceptance | second proof exists |
`;
}


function acceptancePlanText() {
  return planText("CP-02", "Complete", "Complete")
    .replace("ready_for_acceptance: false", "ready_for_acceptance: true");
}


function fixture() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "plumbline-relay-core-"));
  fs.mkdirSync(path.join(root, "state"));
  fs.writeFileSync(path.join(root, "source.md"), "# Source\n");
  fs.writeFileSync(path.join(root, "plan.md"), planText());
  git(root, ["init"]);
  git(root, ["config", "user.name", "Relay Test"]);
  git(root, ["config", "user.email", "relay@example.invalid"]);
  git(root, ["add", "."]);
  git(root, ["commit", "-m", "Create baseline"]);
  return root;
}


function host(root, onComplete, automatic = true, turnEndSignal = false, reconcile = null) {
  let starts = 0;
  return {
    starts: () => starts,
    repositoryRoot: () => root,
    capabilities: () => ({ automatic_relay: automatic, turn_end_signal: turnEndSignal }),
    startCheckpoint: async () => ({ session_id: `session-${++starts}` }),
    observeCompletion: async () => {
      onComplete?.();
      return { status: "completed" };
    },
    reconcileSession: reconcile ? async () => reconcile : undefined,
  };
}


async function main() {
  const root = fixture();
  const plan = path.join(root, "plan.md");
  const stateRoot = path.join(root, "state");
  const successfulHost = host(root, () => {
    fs.writeFileSync(plan, planText("CP-02", "Complete", "Ready"));
    git(root, ["add", "plan.md"]);
    git(root, ["commit", "-m", "Complete CP-01"]);
  });
  const handoff = await runCheckpoint({ planPath: plan, stateRoot, host: successfulHost });
  assert.equal(handoff.status, "handoff_ready");
  assert.equal(successfulHost.starts(), 1);

  const manualRoot = fixture();
  const manual = await runCheckpoint({
    planPath: path.join(manualRoot, "plan.md"),
    stateRoot: path.join(manualRoot, "state"),
    host: host(manualRoot, null, false),
  });
  assert.equal(manual.status, "manual_boundary");

  const staleRoot = fixture();
  const stale = await runCheckpoint({
    planPath: path.join(staleRoot, "plan.md"),
    stateRoot: path.join(staleRoot, "state"),
    host: host(staleRoot),
  });
  assert.equal(stale.status, "paused");
  assert.match(stale.reason, /did not advance/);

  const signalRoot = fixture();
  const signalPlan = path.join(signalRoot, "plan.md");
  const signalState = path.join(signalRoot, "state");
  const signalingHost = host(signalRoot, () => {
    setTimeout(() => {
      fs.writeFileSync(signalPlan, planText("CP-02", "Complete", "Ready"));
      git(signalRoot, ["add", "plan.md"]);
      git(signalRoot, ["commit", "-m", "Complete CP-01 after follow-up"]);
      signalRelay({ hook_event_name: "Stop", cwd: signalRoot, session_id: "session-1", turn_id: "turn-2" }, signalState);
    }, 25);
  }, true, true);
  const signaled = await runCheckpoint({ planPath: signalPlan, stateRoot: signalState, host: signalingHost });
  assert.equal(signaled.status, "handoff_ready");

  const driftRoot = fixture();
  const driftPlan = path.join(driftRoot, "plan.md");
  const driftState = path.join(driftRoot, "state");
  const driftKey = stateKey(driftRoot, driftPlan);
  const driftSnapshot = require("./relay-readiness.js").validatePlan(driftPlan);
  fs.writeFileSync(path.join(driftState, `${driftKey}.json`), JSON.stringify({
    repository_root: driftRoot,
    plan_path: driftPlan,
    plan_fingerprint: "different",
    checkpoint_id: "CP-01",
    host_session_id: "session-old",
    status: "awaiting_completion",
  }));
  const drift = await runCheckpoint({ planPath: driftPlan, stateRoot: driftState, host: host(driftRoot, null, true, true, { status: "completed" }) });
  assert.equal(drift.status, "paused");
  assert.match(drift.reason, /fingerprint changed/);
  assert(driftSnapshot.fingerprint);

  const activeRoot = fixture();
  const activePlan = path.join(activeRoot, "plan.md");
  const activeState = path.join(activeRoot, "state");
  const activeKey = stateKey(activeRoot, activePlan);
  const activeBefore = require("./relay-readiness.js").validatePlan(activePlan);
  fs.writeFileSync(path.join(activeState, `${activeKey}.json`), JSON.stringify({
    repository_root: activeRoot,
    plan_path: activePlan,
    plan_fingerprint: activeBefore.fingerprint,
    checkpoint_id: "CP-01",
    host_session_id: "session-old",
    host_thread_id: "thread-old",
    status: "awaiting_completion",
  }));
  const activeHost = host(activeRoot, null, true, true, { status: "active" });
  const active = await runCheckpoint({ planPath: activePlan, stateRoot: activeState, host: activeHost });
  assert.equal(active.status, "paused");
  assert.match(active.reason, /still active/);
  assert.equal(activeHost.starts(), 0);

  const recoveryRoot = fixture();
  const recoveryPlan = path.join(recoveryRoot, "plan.md");
  const recoveryState = path.join(recoveryRoot, "state");
  const recoveryKey = stateKey(recoveryRoot, recoveryPlan);
  const recoveryBefore = require("./relay-readiness.js").validatePlan(recoveryPlan);
  fs.writeFileSync(path.join(recoveryState, `${recoveryKey}.json`), JSON.stringify({
    repository_root: recoveryRoot,
    plan_path: recoveryPlan,
    plan_fingerprint: recoveryBefore.fingerprint,
    checkpoint_id: "CP-01",
    host_session_id: "session-old",
    status: "awaiting_completion",
  }));
  fs.writeFileSync(recoveryPlan, planText("CP-02", "Complete", "Ready"));
  git(recoveryRoot, ["add", "plan.md"]);
  git(recoveryRoot, ["commit", "-m", "Complete CP-01 before restart"]);
  const recovered = await runCheckpoint({ planPath: recoveryPlan, stateRoot: recoveryState, host: host(recoveryRoot) });
  assert.equal(recovered.status, "handoff_ready");

  const controlledRoot = fixture();
  const controlledPlan = path.join(controlledRoot, "plan.md");
  const controlledState = path.join(controlledRoot, "state");
  const controlledKey = stateKey(controlledRoot, controlledPlan);
  fs.writeFileSync(path.join(controlledState, `${controlledKey}.json`), JSON.stringify({ status: "awaiting_signal" }));
  setControl(controlledState, controlledKey, "stopped");
  const controlled = await runCheckpoint({ planPath: controlledPlan, stateRoot: controlledState, host: host(controlledRoot) });
  assert.equal(controlled.status, "stopped");

  const disconnectRoot = fixture();
  const disconnectedHost = host(disconnectRoot);
  disconnectedHost.startCheckpoint = async () => { throw new Error("App Server disconnected"); };
  const disconnected = await runCheckpoint({
    planPath: path.join(disconnectRoot, "plan.md"),
    stateRoot: path.join(disconnectRoot, "state"),
    host: disconnectedHost,
  });
  assert.equal(disconnected.status, "paused");
  assert.match(disconnected.reason, /App Server disconnected/);

  const acceptanceRoot = fixture();
  const acceptancePlan = path.join(acceptanceRoot, "plan.md");
  fs.writeFileSync(acceptancePlan, acceptancePlanText());
  git(acceptanceRoot, ["add", "plan.md"]);
  git(acceptanceRoot, ["commit", "-m", "Ready for acceptance"]);
  const acceptanceHost = host(acceptanceRoot);
  acceptanceHost.startAcceptance = async () => ({ session_id: "acceptance-session", thread_id: "acceptance-thread", turn_id: "acceptance-turn" });
  const acceptance = await runAcceptance({
    planPath: acceptancePlan,
    stateRoot: path.join(acceptanceRoot, "state"),
    host: acceptanceHost,
  });
  assert.equal(acceptance.status, "acceptance_pending");
  assert.match(acceptance.reason, /explicit user acceptance/);

  const duplicateRoot = fixture();
  const duplicatePlan = path.join(duplicateRoot, "plan.md");
  const key = stateKey(duplicateRoot, duplicatePlan);
  fs.writeFileSync(path.join(duplicateRoot, "state", `${key}.lock`), "occupied");
  await assert.rejects(
    runCheckpoint({ planPath: duplicatePlan, stateRoot: path.join(duplicateRoot, "state"), host: host(duplicateRoot) }),
    RelayLockError,
  );

  for (const target of [root, manualRoot, staleRoot, signalRoot, driftRoot, activeRoot, recoveryRoot, controlledRoot, disconnectRoot, acceptanceRoot, duplicateRoot]) fs.rmSync(target, { recursive: true, force: true });
  console.log("relay-core-smoke=passed");
}


main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
