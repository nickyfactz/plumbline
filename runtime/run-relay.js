#!/usr/bin/env node
"use strict";

const path = require("path");
const { runAcceptance, runCheckpoint } = require("./relay-core.js");
const { CodexHostAdapter } = require("./codex-app-server.js");
const { defaultStateRoot, setControl } = require("./relay-signal.js");


function argument(name) {
  const index = process.argv.indexOf(name);
  return index >= 0 ? process.argv[index + 1] : null;
}


async function main() {
  const planPath = argument("--plan");
  if (!planPath) throw new Error("usage: node runtime/run-relay.js --plan <path> [--state-root <path>] [--pause|--stop]");
  const stateRoot = argument("--state-root") ?? defaultStateRoot();
  const adapter = new CodexHostAdapter();
  try {
    const control = process.argv.includes("--stop") ? "stopped" : process.argv.includes("--pause") ? "paused" : null;
    if (control) {
      const root = adapter.repositoryRoot(path.resolve(planPath));
      const { stateKey } = require("./relay-core.js");
      console.log(JSON.stringify(setControl(stateRoot, stateKey(root, path.resolve(planPath)), control), null, 2));
      return;
    }
    let state;
    do {
      state = await runCheckpoint({ planPath, stateRoot, host: adapter });
    } while (state.status === "handoff_ready");
    if (state.status === "ready_for_acceptance") {
      state = await runAcceptance({ planPath, stateRoot, host: adapter });
    }
    console.log(JSON.stringify(state, null, 2));
    if (state.status === "paused") process.exitCode = 2;
  } finally {
    adapter.close();
  }
}


main().catch((error) => {
  console.error(JSON.stringify({ status: "error", error: error.message }));
  process.exitCode = 2;
});
