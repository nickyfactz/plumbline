#!/usr/bin/env python3
"""Lint a Plumbline-managed live plan for size and current-state hygiene.

The limits follow references/plan-schema.md ("Plan size and lint"). This is a
static check of the plan file only; it does not judge plan quality.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ALLOWED_KEYS = frozenset(
    {
        "status",
        "feature",
        "specification",
        "design",
        "source",
        "base_commit",
        "git_policy",
        "execution_mode",
        "current_checkpoint",
        "checkpoint_status",
        "lifecycle_owner",
        "last_verified_commit",
        "next_safe_action",
        "delegation_roles",
        "delegation_status",
        "ready_for_acceptance",
    }
)
MAX_VALUE_CHARS = 200
MAX_PROOF_CHARS = 300
MAX_LINES = 600
MAX_BYTES = 48 * 1024
LONG_HEX = re.compile(r"\b[0-9a-fA-F]{16,}\b")
CHECKPOINT_HEADING = re.compile(r"^##\s+CP-\d+", re.MULTILINE)
KEY_LINE = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*:(.*)$")


@dataclass(frozen=True)
class Finding:
    line: int
    message: str

    def render(self, path: Path) -> str:
        return f"{path}:{self.line}: {self.message}"


def _frontmatter(lines: list[str]) -> tuple[list[tuple[int, str]], int]:
    """Return (line number, text) pairs inside the frontmatter and the body start index."""
    if not lines or lines[0].strip() != "---":
        return [], 0
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return [(number + 1, lines[number]) for number in range(1, index)], index + 1
    return [], 0


def lint(text: str) -> list[Finding]:
    findings: list[Finding] = []
    lines = text.splitlines()
    front, body_start = _frontmatter(lines)
    if not front:
        findings.append(Finding(1, "missing YAML frontmatter"))

    for number, raw in front:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw[:1].isspace():
            findings.append(Finding(number, "frontmatter values must be one line"))
            continue
        match = KEY_LINE.match(raw)
        if not match:
            findings.append(Finding(number, "unparseable frontmatter line"))
            continue
        key, value = match.group(1), match.group(2).strip()
        if key not in ALLOWED_KEYS:
            findings.append(Finding(number, f"unknown frontmatter key {key!r}"))
        if value in {"|", ">", "|-", ">-"}:
            findings.append(Finding(number, f"{key}: frontmatter values must be one line"))
        if len(value) > MAX_VALUE_CHARS:
            findings.append(Finding(number, f"{key}: value exceeds {MAX_VALUE_CHARS} characters"))

    if len(lines) > MAX_LINES:
        findings.append(Finding(len(lines), f"plan exceeds {MAX_LINES} lines; compact it in place"))
    size = len(text.encode("utf-8"))
    if size > MAX_BYTES:
        findings.append(Finding(1, f"plan is {size} bytes, above {MAX_BYTES}; compact it in place"))

    in_fence = False
    for number, raw in enumerate(lines, start=1):
        if number <= body_start:
            continue
        if raw.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for match in LONG_HEX.finditer(raw):
            findings.append(Finding(number, f"long hex string {match.group(0)[:12]}...; cite a short commit ID or a file pointer"))
        cells = [cell.strip() for cell in raw.strip().strip("|").split("|")] if raw.lstrip().startswith("|") else []
        if len(cells) >= 2 and cells[0] == "Proof" and len(cells[1]) > MAX_PROOF_CHARS:
            findings.append(Finding(number, f"Proof cell exceeds {MAX_PROOF_CHARS} characters"))

    headings = [match.start() for match in CHECKPOINT_HEADING.finditer(text)]
    for position, start in enumerate(headings):
        end = headings[position + 1] if position + 1 < len(headings) else len(text)
        section = text[start:end]
        if not re.search(r"^\|\s*Done when\s*\|", section, re.MULTILINE):
            number = text.count("\n", 0, start) + 1
            findings.append(Finding(number, "checkpoint card has no 'Done when' row"))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("plans", nargs="+", type=Path)
    args = parser.parse_args(argv)
    failed = False
    for path in args.plans:
        findings = lint(path.read_text(encoding="utf-8"))
        for finding in findings:
            print(finding.render(path))
        failed = failed or bool(findings)
    if not failed:
        print(f"Plan lint passed: {len(args.plans)} plan(s)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
