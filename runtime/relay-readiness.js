#!/usr/bin/env node
"use strict";

const crypto = require("crypto");
const fs = require("fs");
const path = require("path");
const { execFileSync } = require("child_process");

const STATUSES = new Set([
  "Pending",
  "Ready",
  "In Progress",
  "Blocked",
  "Complete",
  "Reopened",
  "Superseded",
]);

function parseFrontmatter(text) {
  text = text.replace(/\r\n/g, "\n");
  if (!text.startsWith("---\n")) return {};
  const end = text.indexOf("\n---", 4);
  if (end < 0) return {};
  const fields = {};
  for (const line of text.slice(4, end).split(/\r?\n/)) {
    const match = line.match(/^([a-z_]+):\s*(.*?)\s*$/);
    if (match) fields[match[1]] = match[2].replace(/^['"]|['"]$/g, "");
  }
  return fields;
}

function parseCheckpoints(text) {
  text = text.replace(/\r\n/g, "\n");
  const headers = [...text.matchAll(/^##\s+(CP-[A-Za-z0-9_.-]+)(?::[^\n]*)?$/gm)];
  return headers.map((header, index) => {
    const body = text.slice(header.index, headers[index + 1]?.index ?? text.length);
    const status = body.match(/^(?:\*\*Status:\*\*|- Status:)\s*(.+?)\s*$/m)?.[1];
    const dependencyText = body.match(/^(?:\| Dependencies \||- Depends on:)\s*(.*?)\s*(?:\||$)/m)?.[1] ?? "";
    const dependencies = /^(?:none|null|-)?$/i.test(dependencyText)
      ? []
      : dependencyText.split(/[, ]+/).filter((value) => /^CP-/.test(value));
    const acceptance = body.match(/^(?:\| Acceptance \||- Acceptance:)\s*(.*?)\s*(?:\||$)/m)?.[1];
    const approvalGate = /^(?:\| (?:Approval|User) gate \||- (?:Approval|User) gate:)\s*(?:required|yes|true)\b/im.test(body);
    return { id: header[1], status, dependencies, acceptance, approval_gate: approvalGate };
  });
}

function git(root, args) {
  return execFileSync("git", args, { cwd: root, encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] }).trim();
}

function repositoryFilesAreDurable(root, files) {
  try {
    git(root, ["rev-parse", "--verify", "HEAD"]);
    for (const file of files) {
      const relative = path.relative(root, file).replaceAll("\\", "/");
      git(root, ["ls-files", "--error-unmatch", "--", relative]);
      if (git(root, ["status", "--porcelain", "--", relative])) return false;
    }
    return true;
  } catch {
    return false;
  }
}

function validatePlan(planPath) {
  const absolutePlan = path.resolve(planPath);
  const root = git(path.dirname(absolutePlan), ["rev-parse", "--show-toplevel"]);
  const text = fs.readFileSync(absolutePlan, "utf8");
  const fields = parseFrontmatter(text);
  const checkpoints = parseCheckpoints(text);
  const reasons = [];

  if (fields.execution_mode !== "checkpoint_relay") reasons.push("execution_mode must be checkpoint_relay");
  if (!fields.objective) reasons.push("objective is required");
  if (!fields.current_checkpoint) reasons.push("current_checkpoint is required");
  if (!fields.checkpoint_status || !STATUSES.has(fields.checkpoint_status)) reasons.push("checkpoint_status is invalid");
  if (!fields.next_safe_action) reasons.push("next_safe_action is required");
  if (fields.current_checkpoint && !fields.next_safe_action?.includes(fields.current_checkpoint)) {
    reasons.push("next_safe_action must name current_checkpoint");
  }

  const ids = new Set(checkpoints.map((checkpoint) => checkpoint.id));
  const current = checkpoints.filter((checkpoint) => checkpoint.id === fields.current_checkpoint);
  if (current.length !== 1) reasons.push("exactly one current checkpoint section is required");
  if (current[0] && current[0].status !== fields.checkpoint_status) reasons.push("current checkpoint status does not match frontmatter");
  for (const checkpoint of checkpoints) {
    if (!STATUSES.has(checkpoint.status)) reasons.push(`${checkpoint.id} has an invalid status`);
    if (!checkpoint.acceptance) reasons.push(`${checkpoint.id} requires observable acceptance`);
    for (const dependency of checkpoint.dependencies) {
      if (!ids.has(dependency)) reasons.push(`${checkpoint.id} has unknown dependency ${dependency}`);
      const owner = checkpoints.find((candidate) => candidate.id === dependency);
      if (checkpoint.id === fields.current_checkpoint && owner?.status !== "Complete") {
        reasons.push(`${checkpoint.id} depends on incomplete ${dependency}`);
      }
    }
  }

  const sourceValues = [fields.source, fields.specification].filter((value) => value && value !== "null");
  if (sourceValues.length === 0) reasons.push("a source or specification reference is required");
  const sources = sourceValues.map((value) => path.resolve(path.dirname(absolutePlan), value));
  for (const source of sources) if (!fs.existsSync(source)) reasons.push(`source does not resolve: ${path.basename(source)}`);

  const structurallyCompatible = reasons.length === 0;
  const gitBacked = structurallyCompatible && repositoryFilesAreDurable(root, [absolutePlan, ...sources]);
  const gitHead = gitBacked ? git(root, ["rev-parse", "HEAD"]) : null;
  const sourceHashes = gitBacked
    ? sources.map((source) => crypto.createHash("sha256").update(fs.readFileSync(source)).digest("hex"))
    : [];
  const planHash = crypto.createHash("sha256").update(text).digest("hex");
  const fingerprint = gitBacked
    ? crypto.createHash("sha256").update(JSON.stringify({ root, gitHead, planHash, sourceHashes })).digest("hex")
    : null;
  return {
    classification: structurallyCompatible ? "relay_compatible" : "not_relay_compatible",
    relay_ready: structurallyCompatible && gitBacked,
    git_backed: gitBacked,
    current_checkpoint: fields.current_checkpoint ?? null,
    checkpoint_status: fields.checkpoint_status ?? null,
    objective: fields.objective ?? null,
    next_safe_action: fields.next_safe_action ?? null,
    ready_for_acceptance: fields.ready_for_acceptance === "true",
    checkpoint_count: checkpoints.length,
    checkpoints,
    plan_sha256: planHash,
    git_head: gitHead,
    fingerprint,
    reasons,
  };
}

if (require.main === module) {
  try {
    if (process.argv.length !== 3) throw new Error("usage: node runtime/relay-readiness.js <plan>");
    console.log(JSON.stringify(validatePlan(process.argv[2]), null, 2));
  } catch (error) {
    console.error(JSON.stringify({ classification: "error", relay_ready: false, error: error.message }));
    process.exitCode = 2;
  }
}

module.exports = { parseCheckpoints, parseFrontmatter, validatePlan };
