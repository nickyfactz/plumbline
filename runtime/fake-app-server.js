#!/usr/bin/env node
"use strict";

const fs = require("fs");
const readline = require("readline");

const messages = [];
function send(message) { process.stdout.write(`${JSON.stringify(message)}\n`); }
function capture() { if (process.env.RELAY_CAPTURE) fs.writeFileSync(process.env.RELAY_CAPTURE, JSON.stringify(messages, null, 2)); }

readline.createInterface({ input: process.stdin }).on("line", (line) => {
  const message = JSON.parse(line);
  messages.push(message);
  capture();
  if (message.method === "initialize") return send({ id: message.id, result: { platformFamily: "windows", platformOs: "windows" } });
  if (message.method === "initialized") return;
  if (message.method === "skills/list") return send({ id: message.id, result: { data: [{ cwd: message.params.cwds[0], skills: [{ name: "plumbline:plumbline", enabled: true, path: process.env.RELAY_SKILL_PATH }] }] } });
  if (message.method === "thread/start") return send({ id: message.id, result: { thread: { id: "thread-1", sessionId: "thread-1" } } });
  if (message.method === "thread/name/set" || message.method === "thread/unsubscribe") return send({ id: message.id, result: {} });
  if (message.method === "thread/read") return send({ id: message.id, result: { thread: { id: message.params.threadId, turns: [{ id: "turn-1", status: "completed" }] } } });
  if (message.method === "turn/start") {
    send({ id: message.id, result: { turn: { id: "turn-1", status: "inProgress", items: [], error: null } } });
    setTimeout(() => send({ method: "turn/completed", params: { threadId: "thread-1", turn: { id: "turn-1", status: "completed", error: null } } }), 10);
  }
});
