"use strict";

const fs = require("fs");
const os = require("os");
const path = require("path");


function defaultStateRoot() {
  return process.env.PLUMBLINE_RELAY_STATE_ROOT || path.join(os.homedir(), ".codex", "plumbline", "relay");
}


function normalized(value) {
  if (typeof value !== "string" || !value.trim()) return "";
  const resolved = path.resolve(value);
  return process.platform === "win32" ? resolved.toLowerCase() : resolved;
}


function signalRelay(input, stateRoot = defaultStateRoot()) {
  if (input?.hook_event_name !== "Stop" || !fs.existsSync(stateRoot)) return false;
  for (const name of fs.readdirSync(stateRoot)) {
    if (!/^[a-f0-9]{24}\.json$/.test(name)) continue;
    try {
      const state = JSON.parse(fs.readFileSync(path.join(stateRoot, name), "utf8"));
      if (
        normalized(state.repository_root) !== normalized(input.cwd) ||
        state.host_session_id !== input.session_id ||
        !["awaiting_completion", "awaiting_signal"].includes(state.status)
      ) continue;
      const target = path.join(stateRoot, name.replace(/\.json$/, ".wake"));
      const temporary = `${target}.${process.pid}.tmp`;
      fs.writeFileSync(temporary, `${JSON.stringify({ session_id: input.session_id, turn_id: input.turn_id, signaled_at: new Date().toISOString() })}\n`);
      fs.renameSync(temporary, target);
      return true;
    } catch {}
  }
  return false;
}


function waitForSignal(stateRoot, key, sessionId, pollMs = 250) {
  const target = path.join(stateRoot, `${key}.wake`);
  const statePath = path.join(stateRoot, `${key}.json`);
  return new Promise((resolve) => {
    const poll = () => {
      try {
        const state = JSON.parse(fs.readFileSync(statePath, "utf8"));
        if (["paused", "stopped"].includes(state.status)) return resolve({ control: state.status });
      } catch {}
      try {
        const signal = JSON.parse(fs.readFileSync(target, "utf8"));
        fs.rmSync(target, { force: true });
        if (signal.session_id === sessionId) return resolve(signal);
      } catch {}
      setTimeout(poll, pollMs);
    };
    poll();
  });
}


function setControl(stateRoot, key, status) {
  if (!["paused", "stopped"].includes(status)) throw new Error("relay control must be paused or stopped");
  const target = path.join(stateRoot, `${key}.json`);
  const state = JSON.parse(fs.readFileSync(target, "utf8"));
  const temporary = `${target}.${process.pid}.tmp`;
  fs.writeFileSync(temporary, `${JSON.stringify({ ...state, status, reason: `user requested ${status}`, updated_at: new Date().toISOString() }, null, 2)}\n`);
  fs.renameSync(temporary, target);
  return { ...state, status };
}


module.exports = { defaultStateRoot, setControl, signalRelay, waitForSignal };
