#!/usr/bin/env node
"use strict";

const assert = require("assert");
const fs = require("fs");
const os = require("os");
const path = require("path");
const { CodexHostAdapter } = require("./codex-app-server.js");


async function main() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "plumbline-codex-adapter-"));
  const capture = path.join(root, "capture.json");
  const skillPath = path.resolve(__dirname, "../skills/plumbline/SKILL.md");
  const adapter = new CodexHostAdapter({
    command: [process.execPath, path.join(__dirname, "fake-app-server.js")],
    environment: { ...process.env, RELAY_CAPTURE: capture, RELAY_SKILL_PATH: skillPath },
    turnTimeoutMs: 5000,
  });
  adapter.repositoryRoot = () => root;
  const session = await adapter.startCheckpoint({
    repository_root: root,
    plan_path: path.join(root, "docs", "plan.md"),
    checkpoint_id: "CP-04",
    objective: "Test request normalization",
    next_safe_action: "Execute CP-04",
  });
  assert.deepEqual(session, { session_id: "thread-1", thread_id: "thread-1", turn_id: "turn-1" });
  assert.equal((await adapter.observeCompletion(session)).status, "completed");
  assert.equal((await adapter.reconcileSession({ host_thread_id: "thread-1" })).status, "completed");
  const acceptance = await adapter.startAcceptance({
    repository_root: root,
    plan_path: path.join(root, "docs", "plan.md"),
    objective: "Test acceptance",
  });
  assert.equal((await adapter.observeCompletion(acceptance)).status, "completed");
  adapter.close();

  const messages = JSON.parse(fs.readFileSync(capture, "utf8"));
  assert.equal(messages[0].method, "initialize");
  assert(messages.some((message) => message.method === "initialized"));
  const start = messages.find((message) => message.method === "thread/start");
  assert.equal(start.params.cwd, root);
  assert.equal(start.params.approvalPolicy, undefined);
  assert.equal(start.params.sandbox, undefined);
  const turn = messages.find((message) => message.method === "turn/start");
  assert.equal(turn.params.approvalPolicy, undefined);
  assert.equal(turn.params.sandboxPolicy, undefined);
  assert.equal(turn.params.input[1].type, "skill");
  assert.equal(turn.params.input[1].name, "plumbline:plumbline");
  assert.equal(turn.params.input[1].path, skillPath);
  assert.match(turn.params.input[0].text, /^\[PLUMBLINE_RELAY_CHECKPOINT checkpoint=CP-04\] \$plumbline:plumbline /);
  assert.match(turn.params.input[0].text, /do not start another relay controller/i);
  assert.match(turn.params.input[0].text, /Execute only CP-04/);
  assert.match(turn.params.input[0].text, /stop without beginning downstream work/);
  assert(!turn.params.input[0].text.includes("previous conversation"));
  const acceptanceTurn = messages.filter((message) => message.method === "turn/start").at(-1);
  assert.match(acceptanceTurn.params.input[0].text, /do not infer or manufacture user acceptance/i);
  assert.match(acceptanceTurn.params.input[0].text, /^\[PLUMBLINE_RELAY_ACCEPTANCE\]/);
  assert.match(acceptanceTurn.params.input[0].text, /Closeout in this same task/);
  fs.rmSync(root, { recursive: true, force: true });
  console.log("codex-adapter-smoke=passed");
}


main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
