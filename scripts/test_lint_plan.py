#!/usr/bin/env python3
"""Unit tests for scripts/lint_plan.py."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lint_plan import MAX_LINES, lint  # noqa: E402

CLEAN = """---
status: active
feature: Export
specification: docs/specs/export.md
design: docs/specs/export.md#design
execution_mode: continuous
current_checkpoint: CP-01
checkpoint_status: In Progress
next_safe_action: Implement the export writer.
---

# Export plan

## Decisions

- 2026-01-05: user dropped the PDF format from scope.

## CP-01: Export a report as CSV
**Status:** In Progress
| Boundary | export module |
| Done when | a report downloads as valid CSV |
| Size | medium |
| Proof | pending |
| Next action | Implement the export writer. |

## CP-02: Final performance pass
**Status:** Pending
| Done when | export of 10k rows stays under 2 s (proposed: typical report size) |
| Proof | pending |
"""


def messages(text: str) -> list[str]:
    return [finding.message for finding in lint(text)]


class LintPlanTests(unittest.TestCase):
    def test_clean_plan_passes(self) -> None:
        self.assertEqual(messages(CLEAN), [])

    def test_unknown_frontmatter_key_is_rejected(self) -> None:
        text = CLEAN.replace("status: active\n", "status: active\nactive_operation: rebuild\n", 1)
        self.assertIn("unknown frontmatter key 'active_operation'", messages(text))

    def test_multiline_frontmatter_value_is_rejected(self) -> None:
        text = CLEAN.replace("feature: Export\n", "feature: |\n  Export\n", 1)
        self.assertTrue(any("one line" in message for message in messages(text)))

    def test_long_value_is_rejected(self) -> None:
        text = CLEAN.replace("next_safe_action: Implement the export writer.", "next_safe_action: " + "x" * 250, 1)
        self.assertTrue(any("exceeds 200" in message for message in messages(text)))

    def test_long_proof_cell_is_rejected(self) -> None:
        text = CLEAN.replace("| Proof | pending |\n| Next action", "| Proof | " + "y" * 320 + " |\n| Next action", 1)
        self.assertTrue(any("Proof cell" in message for message in messages(text)))

    def test_long_hex_is_flagged_outside_fences_only(self) -> None:
        digest = "0123456789abcdef0123456789abcdef"
        self.assertTrue(any("long hex" in message for message in messages(CLEAN + f"\nReceipt {digest}\n")))
        self.assertFalse(any("long hex" in message for message in messages(CLEAN + f"\n```\n{digest}\n```\n")))

    def test_short_commit_id_is_allowed(self) -> None:
        self.assertEqual(messages(CLEAN + "\nAccepted at 1a2b3c4d.\n"), [])

    def test_oversized_plan_is_rejected(self) -> None:
        text = CLEAN + "\n".join("- note" for _ in range(MAX_LINES))
        self.assertTrue(any("compact it in place" in message for message in messages(text)))

    def test_checkpoint_without_done_when_is_rejected(self) -> None:
        text = CLEAN + "\n## CP-03: Orphan\n**Status:** Pending\n| Proof | pending |\n"
        self.assertIn("checkpoint card has no 'Done when' row", messages(text))

    def test_missing_frontmatter_is_rejected(self) -> None:
        self.assertIn("missing YAML frontmatter", messages("# Plan\n"))


if __name__ == "__main__":
    unittest.main()
