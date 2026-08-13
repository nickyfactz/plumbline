#!/usr/bin/env node
"use strict";

const crypto = require("crypto");
const fs = require("fs");
const os = require("os");
const path = require("path");

const MAX_STATE_AGE_MS = 30 * 24 * 60 * 60 * 1000;
const REMINDER =
  "Plumbline was explicitly activated earlier in this session. This is a continuity reminder, not a new invocation: read the active plan or resume record, preserve its lifecycle owner and phase, and continue the approved work. Do not rerun setup or start a new phase unless the user asks.";

function stateRoot() {
  return (
    process.env.PLUGIN_DATA ||
    process.env.CLAUDE_PLUGIN_DATA ||
    path.join(os.tmpdir(), "plumbline-session-state")
  );
}

function normalizedCwd(value) {
  if (typeof value !== "string" || !value.trim()) return "";
  const resolved = path.resolve(value);
  return process.platform === "win32" ? resolved.toLowerCase() : resolved;
}

function sessionKey(input) {
  const sessionId = typeof input.session_id === "string" ? input.session_id.trim() : "";
  const cwd = normalizedCwd(input.cwd);
  if (!sessionId || !cwd) return null;
  const digest = crypto
    .createHash("sha256")
    .update(`${sessionId}\0${cwd}`)
    .digest("hex");
  return {
    cwd,
    sessionId,
    file: path.join(stateRoot(), `session-${digest}.json`),
  };
}

function readInput() {
  return new Promise((resolve) => {
    let data = "";
    process.stdin.setEncoding("utf8");
    process.stdin.on("data", (chunk) => {
      data += chunk;
    });
    process.stdin.on("end", () => {
      try {
        resolve(JSON.parse(data));
      } catch (_error) {
        resolve(null);
      }
    });
  });
}

function isFrontDoor(prompt) {
  if (typeof prompt !== "string") return false;
  return /^\s*(?:\$plumbline(?=\s|$)|\$plumbline:plumbline(?=\s|$)|\/plumbline:plumbline(?=\s|$))/i.test(prompt);
}

function isDeactivation(prompt) {
  if (typeof prompt !== "string") return false;
  return /^\s*(?:\$plumbline-(?:closeout|offboard)(?=\s|$)|\/plumbline:plumbline-(?:closeout|offboard)(?=\s|$)|(?:\$plumbline(?::plumbline)?|\/plumbline:plumbline)\s+(?:off|stop|deactivate)(?=\s|$))/i.test(prompt);
}

function arm(input) {
  const identity = sessionKey(input);
  if (!identity) return;
  fs.mkdirSync(stateRoot(), { recursive: true });
  fs.writeFileSync(
    identity.file,
    JSON.stringify({
      cwd: identity.cwd,
      sessionId: identity.sessionId,
      armedAt: Date.now(),
    }) + "\n",
    "utf8"
  );
}

function disarm(input) {
  const identity = sessionKey(input);
  if (!identity) return;
  try {
    fs.unlinkSync(identity.file);
  } catch (_error) {
    // A missing marker already means that continuity is inactive.
  }
}

function isArmed(input) {
  const identity = sessionKey(input);
  if (!identity) return false;
  try {
    const state = JSON.parse(fs.readFileSync(identity.file, "utf8"));
    const armedAt = Number(state.armedAt);
    const currentCwd = normalizedCwd(state.cwd);
    if (
      state.sessionId !== identity.sessionId ||
      currentCwd !== identity.cwd ||
      !Number.isFinite(armedAt) ||
      Date.now() - armedAt > MAX_STATE_AGE_MS
    ) {
      fs.unlinkSync(identity.file);
      return false;
    }
    return true;
  } catch (_error) {
    return false;
  }
}

function emitReminder() {
  process.stdout.write(
    JSON.stringify({
      hookSpecificOutput: {
        hookEventName: "SessionStart",
        additionalContext: REMINDER,
      },
    })
  );
}

async function main() {
  const input = await readInput();
  if (!input || typeof input !== "object") return;

  if (input.hook_event_name === "UserPromptSubmit") {
    if (isDeactivation(input.prompt)) disarm(input);
    else if (isFrontDoor(input.prompt)) arm(input);
    return;
  }

  if (
    input.hook_event_name === "SessionStart" &&
    /^(resume|compact)$/i.test(input.source || "") &&
    isArmed(input)
  ) {
    emitReminder();
  }
}

main().catch(() => {
  // Hooks are a best-effort continuity aid; they never block the session.
  process.exitCode = 0;
});
