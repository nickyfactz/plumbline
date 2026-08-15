#!/usr/bin/env python3
"""Focused smoke tests for normalized Relay Readiness."""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
READINESS = ROOT / "runtime" / "relay-readiness.js"


def git(root: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=root, check=True, capture_output=True, text=True)


def validate(plan: Path) -> dict[str, object]:
    result = subprocess.run(
        ["node", str(READINESS), str(plan)],
        cwd=plan.parent,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def main() -> None:
    if shutil.which("node") is None:
        raise RuntimeError("node is required for Checkpoint Relay")

    with tempfile.TemporaryDirectory() as raw_root:
        root = Path(raw_root)
        git(root, "init")
        git(root, "config", "user.name", "Plumbline Relay Test")
        git(root, "config", "user.email", "relay-test@example.invalid")
        source = root / "source.md"
        plan = root / "plan.md"
        source.write_text("# Settled source\n", encoding="utf-8")
        plan.write_text(
            """---
status: active
objective: Prove Relay readiness.
source: source.md
execution_mode: checkpoint_relay
current_checkpoint: CP-01
checkpoint_status: Ready
next_safe_action: Execute CP-01.
ready_for_acceptance: false
---

## CP-01: First
**Status:** Ready
| Dependencies | none |
| Acceptance | first proof exists |

## CP-02: Second
**Status:** Pending
| Dependencies | CP-01 |
| Acceptance | second proof exists |
""",
            encoding="utf-8",
        )

        assert validate(plan)["relay_ready"] is False
        git(root, "add", "source.md", "plan.md")
        git(root, "commit", "-m", "Create relay baseline")
        ready = validate(plan)
        assert ready["classification"] == "relay_compatible", ready
        assert ready["relay_ready"] is True

        plan.write_text(plan.read_text(encoding="utf-8").replace("Execute CP-01.", "Execute work."), encoding="utf-8")
        invalid = validate(plan)
        assert invalid["relay_ready"] is False
        assert "next_safe_action must name current_checkpoint" in invalid["reasons"]

        plan.write_text(plan.read_text(encoding="utf-8").replace("execution_mode: checkpoint_relay", "execution_mode: continuous"), encoding="utf-8")
        continuous = validate(plan)
        assert continuous["relay_ready"] is False
        assert "execution_mode must be checkpoint_relay" in continuous["reasons"]

    print("checkpoint-relay-readiness-smoke=passed")


if __name__ == "__main__":
    main()
