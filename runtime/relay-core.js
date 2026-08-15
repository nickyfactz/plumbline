"use strict";

const crypto = require("crypto");
const fs = require("fs");
const path = require("path");
const { validatePlan } = require("./relay-readiness.js");
const { waitForSignal } = require("./relay-signal.js");


class RelayLockError extends Error {}


function stateKey(repositoryRoot, planPath) {
  return crypto.createHash("sha256").update(`${repositoryRoot}\0${planPath}`).digest("hex").slice(0, 24);
}


function acquireLock(stateRoot, key) {
  fs.mkdirSync(stateRoot, { recursive: true });
  const lockPath = path.join(stateRoot, `${key}.lock`);
  try {
    const fd = fs.openSync(lockPath, "wx");
    fs.writeFileSync(fd, JSON.stringify({ pid: process.pid, created_at: new Date().toISOString() }));
    fs.closeSync(fd);
  } catch (error) {
    if (error.code === "EEXIST") {
      try {
        const owner = JSON.parse(fs.readFileSync(lockPath, "utf8"));
        process.kill(owner.pid, 0);
      } catch (ownerError) {
        if (ownerError.code === "ESRCH") {
          fs.rmSync(lockPath, { force: true });
          return acquireLock(stateRoot, key);
        }
      }
      throw new RelayLockError("another relay controller owns this repository plan");
    }
    throw error;
  }
  return lockPath;
}


function writeState(stateRoot, key, state) {
  fs.mkdirSync(stateRoot, { recursive: true });
  const target = path.join(stateRoot, `${key}.json`);
  const temporary = `${target}.${process.pid}.tmp`;
  fs.writeFileSync(temporary, `${JSON.stringify(state, null, 2)}\n`, "utf8");
  fs.renameSync(temporary, target);
}


function readState(stateRoot, key) {
  try { return JSON.parse(fs.readFileSync(path.join(stateRoot, `${key}.json`), "utf8")); }
  catch { return null; }
}


function checkpoint(snapshot, id) {
  return snapshot.checkpoints.find((candidate) => candidate.id === id);
}


function validateTransition(before, after) {
  const reasons = [];
  if (!after.relay_ready) reasons.push(...after.reasons, "successor state is not Git-backed Relay Ready");
  const completed = checkpoint(after, before.current_checkpoint);
  if (!completed || completed.status !== "Complete") reasons.push("completed checkpoint is not durably Complete");

  if (after.ready_for_acceptance) {
    if (after.checkpoints.some((candidate) => candidate.status !== "Complete")) {
      reasons.push("Ready for Acceptance requires every checkpoint Complete");
    }
  } else {
    if (after.current_checkpoint === before.current_checkpoint) reasons.push("current checkpoint did not advance");
    const next = checkpoint(after, after.current_checkpoint);
    if (!next || !["Pending", "Ready"].includes(next.status)) reasons.push("successor checkpoint is not ready to run");
    for (const dependency of next?.dependencies ?? []) {
      if (checkpoint(after, dependency)?.status !== "Complete") reasons.push(`successor depends on incomplete ${dependency}`);
    }
  }
  return { valid: reasons.length === 0, reasons };
}


function boundaryState(base, status, reason = null) {
  return { ...base, status, reason, updated_at: new Date().toISOString() };
}


async function runCheckpoint({ planPath, stateRoot, host }) {
  const absolutePlan = path.resolve(planPath);
  const before = validatePlan(absolutePlan);
  const repositoryRoot = host.repositoryRoot(absolutePlan);
  const key = stateKey(repositoryRoot, absolutePlan);
  const lockPath = acquireLock(stateRoot, key);
  const base = {
    schema_version: 1,
    repository_root: repositoryRoot,
    plan_path: absolutePlan,
    plan_sha256: before.plan_sha256,
    plan_fingerprint: before.fingerprint,
    checkpoint_id: before.current_checkpoint,
    host_session_id: null,
  };

  try {
    const previous = readState(stateRoot, key);
    if (previous?.status === "stopped") return previous;
    if (!before.relay_ready) {
      const state = boundaryState(base, "paused", before.reasons.join("; ") || "Relay Readiness failed");
      writeState(stateRoot, key, state);
      return state;
    }
    const current = checkpoint(before, before.current_checkpoint);
    if (!current || ["Blocked", "Reopened"].includes(current.status)) {
      const state = boundaryState(base, "paused", "current checkpoint is not dispatchable");
      writeState(stateRoot, key, state);
      return state;
    }
    if (current.approval_gate) {
      const state = boundaryState(base, "paused", "current checkpoint requires user approval");
      writeState(stateRoot, key, state);
      return state;
    }
    if (!host.capabilities().automatic_relay) {
      const state = boundaryState(base, "manual_boundary", "automatic relay is unavailable; start a fresh root conversation manually");
      writeState(stateRoot, key, state);
      return state;
    }

    if (
      previous &&
      ["awaiting_completion", "awaiting_signal"].includes(previous.status) &&
      previous.checkpoint_id !== before.current_checkpoint
    ) {
      const recoveredTransition = validateTransition({ current_checkpoint: previous.checkpoint_id }, before);
      if (!recoveredTransition.valid) {
        const state = boundaryState(base, "paused", recoveredTransition.reasons.join("; "));
        writeState(stateRoot, key, state);
        return state;
      }
      const state = boundaryState(
        { ...previous, plan_sha256: before.plan_sha256, plan_fingerprint: before.fingerprint, checkpoint_id: before.current_checkpoint },
        before.ready_for_acceptance ? "ready_for_acceptance" : "handoff_ready",
      );
      writeState(stateRoot, key, state);
      return state;
    }

    if (
      previous &&
      ["awaiting_completion", "awaiting_signal"].includes(previous.status) &&
      previous.checkpoint_id === before.current_checkpoint
    ) {
      if (previous.plan_fingerprint !== before.fingerprint) {
        const state = boundaryState(base, "paused", "active relay fingerprint changed without a legal checkpoint transition");
        writeState(stateRoot, key, state);
        return state;
      }
      const recovered = await host.reconcileSession?.(previous);
      if (recovered?.status === "active") {
        const state = boundaryState(previous, "paused", "the prior checkpoint task is still active; duplicate dispatch refused");
        writeState(stateRoot, key, state);
        return state;
      }
      if (recovered?.status !== "completed") {
        const state = boundaryState(previous, "paused", "the prior checkpoint task could not be reconciled safely");
        writeState(stateRoot, key, state);
        return state;
      }
      writeState(stateRoot, key, boundaryState(previous, "awaiting_signal", "recovered completed task without a durable transition"));
      const wake = await waitForSignal(stateRoot, key, previous.host_session_id);
      if (wake.control) return readState(stateRoot, key);
      const recoveredPlan = validatePlan(absolutePlan);
      const recoveredTransition = validateTransition({ current_checkpoint: previous.checkpoint_id }, recoveredPlan);
      if (!recoveredTransition.valid) {
        const state = boundaryState(previous, "paused", recoveredTransition.reasons.join("; "));
        writeState(stateRoot, key, state);
        return state;
      }
      const state = boundaryState(
        { ...previous, plan_sha256: recoveredPlan.plan_sha256, plan_fingerprint: recoveredPlan.fingerprint, checkpoint_id: recoveredPlan.current_checkpoint },
        recoveredPlan.ready_for_acceptance ? "ready_for_acceptance" : "handoff_ready",
      );
      writeState(stateRoot, key, state);
      return state;
    }

    writeState(stateRoot, key, boundaryState(base, "dispatching"));
    const session = await host.startCheckpoint({
      repository_root: repositoryRoot,
      plan_path: absolutePlan,
      checkpoint_id: before.current_checkpoint,
      objective: before.objective,
      next_safe_action: before.next_safe_action,
    });
    const active = { ...base, host_session_id: session.session_id, host_thread_id: session.thread_id ?? session.session_id };
    writeState(stateRoot, key, boundaryState(active, "awaiting_completion"));
    const completion = await host.observeCompletion(session);
    if (completion.status !== "completed") {
      const state = boundaryState(active, "paused", `host completion was ${completion.status}`);
      writeState(stateRoot, key, state);
      return state;
    }

    let after = validatePlan(absolutePlan);
    let transition = validateTransition(before, after);
    while (
      !transition.valid &&
      after.plan_sha256 === before.plan_sha256 &&
      host.capabilities().turn_end_signal === true
    ) {
      writeState(stateRoot, key, boundaryState(active, "awaiting_signal", "checkpoint task ended without a durable transition"));
      const wake = await waitForSignal(stateRoot, key, session.session_id);
      if (wake.control) return readState(stateRoot, key);
      after = validatePlan(absolutePlan);
      transition = validateTransition(before, after);
    }
    if (!transition.valid) {
      const state = boundaryState(active, "paused", transition.reasons.join("; "));
      writeState(stateRoot, key, state);
      return state;
    }
    const state = boundaryState(
      { ...active, plan_sha256: after.plan_sha256, plan_fingerprint: after.fingerprint, checkpoint_id: after.current_checkpoint },
      after.ready_for_acceptance ? "ready_for_acceptance" : "handoff_ready",
    );
    writeState(stateRoot, key, state);
    return state;
  } catch (error) {
    const state = boundaryState(base, "paused", `relay transport or recovery failure: ${error.message}`);
    writeState(stateRoot, key, state);
    return state;
  } finally {
    fs.rmSync(lockPath, { force: true });
  }
}


async function runAcceptance({ planPath, stateRoot, host }) {
  const absolutePlan = path.resolve(planPath);
  const snapshot = validatePlan(absolutePlan);
  const repositoryRoot = host.repositoryRoot(absolutePlan);
  const key = stateKey(repositoryRoot, absolutePlan);
  const lockPath = acquireLock(stateRoot, key);
  const base = {
    schema_version: 1,
    repository_root: repositoryRoot,
    plan_path: absolutePlan,
    plan_sha256: snapshot.plan_sha256,
    plan_fingerprint: snapshot.fingerprint,
    checkpoint_id: snapshot.current_checkpoint,
  };
  try {
    if (!snapshot.relay_ready || !snapshot.ready_for_acceptance || snapshot.checkpoints.some((item) => item.status !== "Complete")) {
      const state = boundaryState(base, "paused", "acceptance requires a Git-backed plan with every checkpoint Complete");
      writeState(stateRoot, key, state);
      return state;
    }
    if (!host.startAcceptance) {
      const state = boundaryState(base, "manual_boundary", "start a fresh acceptance conversation manually");
      writeState(stateRoot, key, state);
      return state;
    }
    const session = await host.startAcceptance({ repository_root: repositoryRoot, plan_path: absolutePlan, objective: snapshot.objective });
    writeState(stateRoot, key, boundaryState({ ...base, host_session_id: session.session_id, host_thread_id: session.thread_id }, "awaiting_acceptance_summary"));
    const completion = await host.observeCompletion(session);
    const state = completion.status === "completed"
      ? boundaryState({ ...base, host_session_id: session.session_id, host_thread_id: session.thread_id }, "acceptance_pending", "explicit user acceptance remains required")
      : boundaryState(base, "paused", `acceptance task completion was ${completion.status}`);
    writeState(stateRoot, key, state);
    return state;
  } catch (error) {
    const state = boundaryState(base, "paused", `acceptance transport failure: ${error.message}`);
    writeState(stateRoot, key, state);
    return state;
  } finally {
    fs.rmSync(lockPath, { force: true });
  }
}


module.exports = {
  RelayLockError,
  acquireLock,
  readState,
  runAcceptance,
  runCheckpoint,
  stateKey,
  validateTransition,
  writeState,
};
