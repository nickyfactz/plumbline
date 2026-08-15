#!/usr/bin/env node
"use strict";

const { signalRelay } = require("../runtime/relay-signal.js");

let data = "";
process.stdin.setEncoding("utf8");
process.stdin.on("data", (chunk) => { data += chunk; });
process.stdin.on("end", () => {
  try { signalRelay(JSON.parse(data)); } catch {}
});
