#!/usr/bin/env python3
"""Focused smoke test for explicit Plumbline continuity activation."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / "hooks" / "plumbline-session.js"
RELAY_HOOK = ROOT / "hooks" / "plumbline-relay-signal.js"


def run_hook(payload: dict[str, object], state_root: Path) -> str:
    environment = os.environ.copy()
    environment["PLUGIN_DATA"] = str(state_root)
    environment["CLAUDE_PLUGIN_ROOT"] = str(ROOT)
    completed = subprocess.run(
        ["node", str(HOOK)],
        cwd=ROOT,
        env=environment,
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        check=True,
    )
    assert not completed.stderr, completed.stderr
    return completed.stdout.strip()


def run_relay_hook(payload: dict[str, object], state_root: Path) -> str:
    environment = os.environ.copy()
    environment["PLUMBLINE_RELAY_STATE_ROOT"] = str(state_root)
    completed = subprocess.run(
        ["node", str(RELAY_HOOK)],
        cwd=ROOT,
        env=environment,
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        check=True,
    )
    assert not completed.stderr, completed.stderr
    return completed.stdout.strip()


def main() -> None:
    if shutil.which("node") is None:
        raise RuntimeError("node is required to test the optional continuity hook")

    with tempfile.TemporaryDirectory() as raw_root:
        root = Path(raw_root)
        project = root / "project"
        other_project = root / "other-project"
        project.mkdir()
        other_project.mkdir()
        state_root = root / "state"
        base = {"session_id": "session-1", "cwd": str(project)}

        # Ordinary prompts and phase side doors do not arm the hook.
        assert run_hook({**base, "hook_event_name": "UserPromptSubmit", "prompt": "Use Plumbline for this."}, state_root) == ""
        assert run_hook({**base, "hook_event_name": "UserPromptSubmit", "prompt": "$plumbline-shape decide this."}, state_root) == ""
        assert not state_root.exists()

        # Only the explicit front door arms the current session and repository.
        assert run_hook({**base, "hook_event_name": "UserPromptSubmit", "prompt": "$plumbline implement this."}, state_root) == ""
        assert len(list(state_root.glob("session-*.json"))) == 1

        compact = run_hook({**base, "hook_event_name": "SessionStart", "source": "compact"}, state_root)
        compact_payload = json.loads(compact)
        context = compact_payload["hookSpecificOutput"]["additionalContext"]
        assert "explicitly activated" in context
        assert "not a new invocation" in context
        assert "resume record" in context
        assert "delegation_roles" in context
        assert "delegation_status" in context

        resume = run_hook({**base, "hook_event_name": "SessionStart", "source": "resume"}, state_root)
        assert json.loads(resume)["hookSpecificOutput"]["hookEventName"] == "SessionStart"
        assert run_hook({**base, "hook_event_name": "SessionStart", "source": "startup"}, state_root) == ""

        # Session and repository identity provide isolation from activation elsewhere.
        assert run_hook({**base, "session_id": "session-2", "hook_event_name": "SessionStart", "source": "compact"}, state_root) == ""
        assert run_hook({**base, "cwd": str(other_project), "hook_event_name": "SessionStart", "source": "compact"}, state_root) == ""

        # Explicit closeout/offboarding clears the reminder for this session.
        assert run_hook({**base, "hook_event_name": "UserPromptSubmit", "prompt": "$plumbline-closeout"}, state_root) == ""
        assert run_hook({**base, "hook_event_name": "SessionStart", "source": "compact"}, state_root) == ""

        # Stop is inert unless this exact repository task belongs to an active relay.
        relay_root = root / "relay"
        relay_root.mkdir()
        stop = {**base, "hook_event_name": "Stop", "turn_id": "turn-1"}
        assert run_relay_hook(stop, relay_root) == ""
        assert not list(relay_root.glob("*.wake"))
        relay_state = {
            "repository_root": str(project),
            "host_session_id": "session-1",
            "status": "awaiting_signal",
        }
        (relay_root / "0123456789abcdef01234567.json").write_text(json.dumps(relay_state), encoding="utf-8")
        assert run_relay_hook({**stop, "session_id": "session-2"}, relay_root) == ""
        assert not list(relay_root.glob("*.wake"))
        assert run_relay_hook(stop, relay_root) == ""
        wake = json.loads((relay_root / "0123456789abcdef01234567.wake").read_text(encoding="utf-8"))
        assert wake["session_id"] == "session-1"
        assert wake["turn_id"] == "turn-1"

    print("plumbline-hook-smoke=passed")


if __name__ == "__main__":
    main()
