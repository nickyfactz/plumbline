"use strict";

const fs = require("fs");
const path = require("path");
const readline = require("readline");
const { spawn, execFileSync } = require("child_process");


class AppServerError extends Error {}


function defaultCommand() {
  if (process.platform !== "win32") return ["codex", "app-server", "--listen", "stdio://"];
  try {
    const launcher = execFileSync("where.exe", ["codex.cmd"], { encoding: "utf8", windowsHide: true })
      .split(/\r?\n/)
      .find((candidate) => candidate && fs.existsSync(candidate));
    const entrypoint = launcher && path.join(path.dirname(launcher), "node_modules", "@openai", "codex", "bin", "codex.js");
    if (entrypoint && fs.existsSync(entrypoint)) return [process.execPath, entrypoint, "app-server", "--listen", "stdio://"];
  } catch {}
  throw new AppServerError("the Windows Codex CLI Node entrypoint was not found behind codex.cmd");
}


class AppServerClient {
  constructor({ command = defaultCommand(), environment = process.env } = {}) {
    this.command = command;
    this.environment = environment;
    this.nextId = 1;
    this.pending = new Map();
    this.notifications = [];
    this.waiters = [];
    this.stderr = "";
  }

  async connect() {
    const [executable, ...args] = this.command;
    this.process = spawn(executable, args, { env: this.environment, stdio: ["pipe", "pipe", "pipe"], windowsHide: true });
    this.process.stderr.on("data", (chunk) => { this.stderr = `${this.stderr}${chunk}`.slice(-16000); });
    this.process.on("exit", (code) => {
      const error = new AppServerError(`Codex App Server exited with code ${code}: ${this.stderr.trim()}`);
      for (const { reject, timer } of this.pending.values()) { clearTimeout(timer); reject(error); }
      this.pending.clear();
      for (const waiter of this.waiters) { clearTimeout(waiter.timer); waiter.reject(error); }
      this.waiters = [];
    });
    readline.createInterface({ input: this.process.stdout }).on("line", (line) => this.handleLine(line));
    await this.request("initialize", {
      clientInfo: { name: "plumbline_checkpoint_relay", title: "Plumbline Checkpoint Relay", version: "0.1.0" },
    });
    this.notify("initialized", {});
    return this;
  }

  send(message) {
    if (!this.process?.stdin.writable) throw new AppServerError("Codex App Server stdin is unavailable");
    this.process.stdin.write(`${JSON.stringify(message)}\n`);
  }

  request(method, params = {}, timeoutMs = 30000) {
    const id = this.nextId++;
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        this.pending.delete(id);
        reject(new AppServerError(`${method} timed out after ${timeoutMs}ms`));
      }, timeoutMs);
      this.pending.set(id, { method, resolve, reject, timer });
      this.send({ id, method, params });
    });
  }

  notify(method, params = {}) {
    this.send({ method, params });
  }

  handleLine(line) {
    let message;
    try { message = JSON.parse(line); } catch { return; }
    if (message.id !== undefined && (message.result !== undefined || message.error !== undefined)) {
      const pending = this.pending.get(message.id);
      if (!pending) return;
      clearTimeout(pending.timer);
      this.pending.delete(message.id);
      if (message.error) pending.reject(new AppServerError(`${pending.method}: ${message.error.message ?? JSON.stringify(message.error)}`));
      else pending.resolve(message.result);
      return;
    }
    if (message.id !== undefined && message.method) {
      this.send({ id: message.id, error: { code: -32601, message: "Plumbline Relay does not handle interactive server requests" } });
      return;
    }
    if (!message.method) return;
    const index = this.waiters.findIndex((waiter) => waiter.method === message.method && waiter.predicate(message.params));
    if (index >= 0) {
      const [waiter] = this.waiters.splice(index, 1);
      clearTimeout(waiter.timer);
      waiter.resolve(message.params);
    } else {
      this.notifications.push(message);
      if (this.notifications.length > 200) this.notifications.shift();
    }
  }

  waitFor(method, predicate = () => true, timeoutMs = 24 * 60 * 60 * 1000) {
    const index = this.notifications.findIndex((message) => message.method === method && predicate(message.params));
    if (index >= 0) return Promise.resolve(this.notifications.splice(index, 1)[0].params);
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        this.waiters = this.waiters.filter((waiter) => waiter.timer !== timer);
        reject(new AppServerError(`${method} notification timed out after ${timeoutMs}ms`));
      }, timeoutMs);
      this.waiters.push({ method, predicate, resolve, reject, timer });
    });
  }

  close() {
    if (!this.process || this.process.exitCode !== null) return;
    this.process.stdin.end();
    setTimeout(() => this.process?.kill(), 1000).unref();
  }
}


class CodexHostAdapter {
  constructor(options = {}) {
    this.client = options.client ?? new AppServerClient(options);
    this.turnTimeoutMs = options.turnTimeoutMs ?? 24 * 60 * 60 * 1000;
    this.frontDoor = options.frontDoor ?? null;
  }

  capabilities() {
    return {
      automatic_relay: true,
      fresh_root_context: true,
      native_app_visibility: true,
      native_thread_naming: true,
      completion_signal: true,
      turn_end_signal: true,
      manual_user_steer_compatible: true,
    };
  }

  repositoryRoot(planPath) {
    return execFileSync("git", ["rev-parse", "--show-toplevel"], {
      cwd: path.dirname(planPath), encoding: "utf8", stdio: ["ignore", "pipe", "pipe"],
    }).trim();
  }

  async ensureConnected() {
    if (!this.connected) {
      await this.client.connect();
      this.connected = true;
    }
  }

  async resolveFrontDoor(cwd) {
    await this.ensureConnected();
    if (this.frontDoor) {
      if (!fs.existsSync(this.frontDoor.path)) throw new AppServerError("configured Plumbline front door does not exist");
      return this.frontDoor;
    }
    const result = await this.client.request("skills/list", { cwds: [cwd], forceReload: true });
    const skills = result.data?.find((entry) => path.resolve(entry.cwd) === path.resolve(cwd))?.skills ?? [];
    const skill = skills.find((candidate) =>
      (candidate.name === "plumbline" || candidate.name.endsWith(":plumbline")) && candidate.enabled !== false);
    const skillPath = skill?.path ?? skill?.skillPath;
    if (!skill || !skillPath || !fs.existsSync(skillPath)) throw new AppServerError("installed Plumbline front door was not discoverable for the repository");
    return { name: skill.name, path: skillPath };
  }

  async startCheckpoint(request) {
    await this.ensureConnected();
    const skill = await this.resolveFrontDoor(request.repository_root);
    const started = await this.client.request("thread/start", {
      cwd: request.repository_root,
      serviceName: "plumbline_checkpoint_relay",
    });
    const threadId = started.thread.id;
    await this.client.request("thread/name/set", {
      threadId,
      name: `Plumbline Relay ${request.checkpoint_id}`,
    });
    const relativePlan = path.relative(request.repository_root, request.plan_path).replaceAll("\\", "/");
    const prompt = `[PLUMBLINE_RELAY_CHECKPOINT checkpoint=${request.checkpoint_id}] $${skill.name} Execute only ${request.checkpoint_id} from ${relativePlan} in explicit checkpoint_relay mode. This task was dispatched by the relay controller: do not start another relay controller. Recover from repository guidance, the controlling source/plan, current Git state, and retained evidence; do not use or request earlier checkpoint conversation history. Complete and verify only the current checkpoint, promote every downstream-relevant correction or decision into its authoritative artifact, establish the plan-required Git recovery boundary, update the durable plan to exactly one legal successor or Ready for Acceptance, and stop without beginning downstream work.`;
    const turn = await this.client.request("turn/start", {
      threadId,
      cwd: request.repository_root,
      input: [
        { type: "text", text: prompt },
        { type: "skill", name: skill.name, path: skill.path },
      ],
    });
    return {
      session_id: started.thread.sessionId ?? threadId,
      thread_id: threadId,
      turn_id: turn.turn.id,
    };
  }

  async startAcceptance(request) {
    await this.ensureConnected();
    const skill = await this.resolveFrontDoor(request.repository_root);
    const started = await this.client.request("thread/start", {
      cwd: request.repository_root,
      serviceName: "plumbline_checkpoint_relay",
    });
    const threadId = started.thread.id;
    await this.client.request("thread/name/set", { threadId, name: "Plumbline Relay Acceptance" });
    const relativePlan = path.relative(request.repository_root, request.plan_path).replaceAll("\\", "/");
    const prompt = `[PLUMBLINE_RELAY_ACCEPTANCE] $${skill.name} Review ${relativePlan} as the completed checkpoint_relay plan. Recover from repository guidance, authoritative artifacts, current Git state, and retained evidence only. Present the concise acceptance boundary and residual risk; do not infer or manufacture user acceptance. If the user explicitly accepts in this task, continue through normal Plumbline Closeout in this same task. Do not create another task merely for Closeout.`;
    const turn = await this.client.request("turn/start", {
      threadId,
      cwd: request.repository_root,
      input: [{ type: "text", text: prompt }, { type: "skill", name: skill.name, path: skill.path }],
    });
    return { session_id: started.thread.sessionId ?? threadId, thread_id: threadId, turn_id: turn.turn.id };
  }

  async observeCompletion(session) {
    const params = await this.client.waitFor(
      "turn/completed",
      (candidate) => candidate.threadId === session.thread_id && candidate.turn?.id === session.turn_id,
      this.turnTimeoutMs,
    );
    const status = params.turn.status;
    try { await this.client.request("thread/unsubscribe", { threadId: session.thread_id }); } catch {}
    return { status, error: params.turn.error ?? null };
  }

  async readThread(threadId) {
    await this.ensureConnected();
    return this.client.request("thread/read", { threadId, includeTurns: true });
  }

  async reconcileSession(state) {
    try {
      const result = await this.readThread(state.host_thread_id ?? state.host_session_id);
      const turns = result.thread?.turns ?? [];
      const latest = turns.at(-1);
      if (!latest) return { status: "unknown" };
      if (["inProgress", "running"].includes(latest.status)) return { status: "active" };
      if (latest.status === "completed") return { status: "completed", turn_id: latest.id };
      return { status: latest.status ?? "unknown" };
    } catch {
      return { status: "unknown" };
    }
  }

  close() {
    this.client.close();
  }
}


module.exports = { AppServerClient, AppServerError, CodexHostAdapter, defaultCommand };
