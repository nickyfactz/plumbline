#!/usr/bin/env python3
"""Router setup and installed front-door regression checks; no model calls."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from install_router import GUIDANCE_END, GUIDANCE_START, ROUTER_PATH, install
from resolve_front_door import resolve_front_door

PLUGIN = Path(__file__).resolve().parents[1]


def git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(root), *args], check=True, capture_output=True, text=True
    ).stdout.strip()


class RouterSetup(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="plumbline-router-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo"
        self.root.mkdir()
        git(self.root, "init", "-q")
        git(self.root, "config", "user.name", "Plumbline Test")
        git(self.root, "config", "user.email", "test@example.invalid")
        git(self.root, "commit", "--allow-empty", "-qm", "fixture")

    def test_router_only_setup_is_ignored_and_idempotent(self) -> None:
        agents = self.root / "AGENTS.md"
        agents.write_text("# Project\n\nKeep my rules.\n", encoding="utf-8")
        (self.root / ".worktreeinclude").write_text(
            "local-data.json\n", encoding="utf-8"
        )
        (self.root / ".gitignore").write_text("build/\n", encoding="utf-8")
        preview = install(PLUGIN, self.root, propagate=True, dry_run=True)
        self.assertFalse((self.root / ROUTER_PATH).exists())
        self.assertEqual(
            agents.read_text(encoding="utf-8"), "# Project\n\nKeep my rules.\n"
        )
        applied = install(PLUGIN, self.root, propagate=True)
        self.assertEqual(preview.changes, applied.changes)
        self.assertEqual(preview.operations, applied.operations)
        guidance = agents.read_text(encoding="utf-8")
        self.assertIn("Keep my rules.", guidance)
        self.assertIn("even if `plumbline-router` is absent", guidance)
        self.assertIn(
            "If the file is absent, automatic Plumbline routing is off", guidance
        )
        self.assertEqual(guidance.count(GUIDANCE_START), 1)
        self.assertIn(
            "local-data.json",
            (self.root / ".worktreeinclude").read_text(encoding="utf-8"),
        )
        self.assertIn("build/", (self.root / ".gitignore").read_text(encoding="utf-8"))
        self.assertFalse((self.root / ".codex").exists())
        self.assertEqual(
            git(self.root, "check-ignore", ROUTER_PATH.as_posix()),
            ROUTER_PATH.as_posix(),
        )
        self.assertFalse(install(PLUGIN, self.root, propagate=True).changes)

    def test_custom_router_requires_replace_before_any_write(self) -> None:
        router = self.root / ROUTER_PATH
        router.parent.mkdir(parents=True)
        router.write_text("user router\n", encoding="utf-8")
        preview = install(PLUGIN, self.root, propagate=True, dry_run=True)
        self.assertTrue(preview.requires_replace)
        with self.assertRaises(FileExistsError):
            install(PLUGIN, self.root, propagate=True)
        self.assertFalse((self.root / "AGENTS.md").exists())
        install(PLUGIN, self.root, replace=True, propagate=True)
        self.assertEqual(
            router.read_text(encoding="utf-8"),
            (PLUGIN / "templates/router/SKILL.md").read_text(encoding="utf-8"),
        )

    def test_invalid_guidance_fails_before_router_write(self) -> None:
        agents = self.root / "AGENTS.md"
        for text in (
            GUIDANCE_START,
            GUIDANCE_END,
            GUIDANCE_END + "\n" + GUIDANCE_START,
        ):
            agents.write_text(text, encoding="utf-8")
            with self.assertRaises(ValueError):
                install(PLUGIN, self.root)
            self.assertFalse((self.root / ROUTER_PATH).exists())

    def test_claude_router_only_imports_shared_guidance(self) -> None:
        install(PLUGIN, self.root, host="claude")
        self.assertIn(
            "@AGENTS.md", (self.root / "CLAUDE.md").read_text(encoding="utf-8")
        )
        self.assertFalse((self.root / ".claude/agents").exists())

    def test_non_git_router_setup_keeps_its_original_support(self) -> None:
        target = Path(self.temp.name) / "non-git"
        target.mkdir()
        install(PLUGIN, target)
        self.assertTrue((target / ROUTER_PATH).is_file())
        self.assertFalse((target / ".git").exists())
        self.assertIn(
            "plumbline-router/", (target / ".gitignore").read_text(encoding="utf-8")
        )
        with self.assertRaises(ValueError):
            install(PLUGIN, target, propagate=True)

    def test_setup_in_an_existing_worktree_uses_shared_git_ignore(self) -> None:
        worktree = Path(self.temp.name) / "existing-worktree"
        git(self.root, "worktree", "add", "--detach", "-q", str(worktree))
        install(PLUGIN, worktree, propagate=True)
        self.assertTrue((worktree / ROUTER_PATH).is_file())
        self.assertEqual(
            git(worktree, "check-ignore", ROUTER_PATH.as_posix()),
            ROUTER_PATH.as_posix(),
        )
        self.assertIn(
            "plumbline-router/",
            (self.root / ".git/info/exclude").read_text(encoding="utf-8"),
        )

    def test_setup_rejects_targets_outside_checkout(self) -> None:
        outside = Path(self.temp.name) / "outside.md"
        outside.write_text("Keep me.\n", encoding="utf-8")
        try:
            (self.root / "AGENTS.md").symlink_to(outside)
        except OSError as exc:
            self.skipTest(f"host cannot create symlinks: {exc}")
        with self.assertRaises(ValueError):
            install(PLUGIN, self.root)
        self.assertFalse((self.root / ROUTER_PATH).exists())
        self.assertEqual(outside.read_text(encoding="utf-8"), "Keep me.\n")

    def test_template_cannot_escape_plugin_root(self) -> None:
        plugin = Path(self.temp.name) / "plugin"
        template = plugin / "templates/router/SKILL.md"
        template.parent.mkdir(parents=True)
        outside = Path(self.temp.name) / "outside-template.md"
        outside.write_text("outside instructions\n", encoding="utf-8")
        try:
            template.symlink_to(outside)
        except OSError as exc:
            self.skipTest(f"host cannot create symlinks: {exc}")
        with self.assertRaises(ValueError):
            install(plugin, self.root)
        self.assertFalse((self.root / ROUTER_PATH).exists())

    def test_cli_preview_lists_all_router_setup_paths(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(PLUGIN / "scripts/install_router.py"),
                "--root",
                str(self.root),
                "--propagate",
                "--dry-run",
                "--format",
                "json",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(result.stdout)
        paths = {
            Path(change["path"]).relative_to(self.root).as_posix()
            for change in payload["changes"]
        }
        self.assertEqual(
            paths,
            {
                ROUTER_PATH.as_posix(),
                "AGENTS.md",
                ".git/info/exclude",
                ".gitignore",
                ".worktreeinclude",
            },
        )
        self.assertFalse(payload["writes_applied"])
        self.assertFalse((self.root / ROUTER_PATH).exists())

    def test_new_worktree_receives_durable_guidance_and_copyable_router(self) -> None:
        install(PLUGIN, self.root, propagate=True)
        git(self.root, "add", "AGENTS.md", ".gitignore", ".worktreeinclude")
        git(self.root, "commit", "-qm", "router activation")
        self.assertNotIn(ROUTER_PATH.as_posix(), git(self.root, "ls-files"))
        worktree = Path(self.temp.name) / "worktree"
        git(self.root, "worktree", "add", "--detach", "-q", str(worktree))
        self.assertIn(
            GUIDANCE_START, (worktree / "AGENTS.md").read_text(encoding="utf-8")
        )
        self.assertFalse((worktree / ROUTER_PATH).exists())
        # Simulate the documented local host copy; plain Git never copies ignored files.
        for pattern in (
            (worktree / ".worktreeinclude").read_text(encoding="utf-8").splitlines()
        ):
            for source in self.root.glob(pattern + "/*"):
                if source.is_file():
                    relative = source.relative_to(self.root)
                    git(self.root, "check-ignore", str(relative))
                    target = worktree / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, target)
        self.assertTrue((worktree / ROUTER_PATH).is_file())
        self.assertFalse(git(worktree, "status", "--porcelain"))
        (worktree / ROUTER_PATH).unlink()
        self.assertFalse((worktree / ROUTER_PATH).exists())
        self.assertIn(
            "do not recreate it", (worktree / "AGENTS.md").read_text(encoding="utf-8")
        )


class FrontDoorResolution(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="plumbline-front-door-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.active = self.make_plugin("active")

    def make_plugin(self, name: str) -> Path:
        root = self.root / name
        (root / ".codex-plugin").mkdir(parents=True)
        (root / ".codex-plugin/plugin.json").write_text(
            json.dumps(
                {"name": "plumbline", "version": "1.0.0", "skills": "./skills/"}
            ),
            encoding="utf-8",
        )
        for skill in ("plumbline", "plumbline-execute-engine"):
            path = root / "skills" / skill / "SKILL.md"
            path.parent.mkdir(parents=True)
            path.write_text(
                f"---\nname: {skill}\n---\nReal instructions.\n", encoding="utf-8"
            )
        return root

    def test_missing_catalog_front_door_resolves_from_visible_engine(self) -> None:
        self.make_plugin("newer-but-not-active-cache")
        visible = self.active / "skills/plumbline-execute-engine/SKILL.md"
        self.assertEqual(
            resolve_front_door([visible, visible]),
            self.active / "skills/plumbline/SKILL.md",
        )

    def test_absent_or_ambiguous_active_plugin_fails(self) -> None:
        other = self.make_plugin("other")
        for paths in (
            [],
            [
                self.active / "skills/plumbline/SKILL.md",
                other / "skills/plumbline/SKILL.md",
            ],
        ):
            with self.assertRaises(ValueError):
                resolve_front_door(paths)

    def test_invalid_or_missing_plugin_and_front_door_fail(self) -> None:
        visible = self.active / "skills/plumbline-execute-engine/SKILL.md"
        manifest = self.active / ".codex-plugin/plugin.json"
        original = manifest.read_text(encoding="utf-8")
        for invalid in (
            "[]",
            "{}",
            '{"name":"other"}',
            "broken json",
            '{"name":"plumbline","version":1,"skills":"./skills/"}',
            '{"name":"plumbline","version":"1","skills":"../skills"}',
        ):
            manifest.write_text(invalid, encoding="utf-8")
            with self.assertRaises(ValueError):
                resolve_front_door([visible])
        manifest.write_text(original, encoding="utf-8")
        front = self.active / "skills/plumbline/SKILL.md"
        front.write_text("---\nname: wrong\n---\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            resolve_front_door([visible])
        front.unlink()
        with self.assertRaises(OSError):
            resolve_front_door([visible])
        manifest.unlink()
        with self.assertRaises(OSError):
            resolve_front_door([visible])

    def test_cli_loads_actual_packaged_front_door(self) -> None:
        visible = PLUGIN / "skills/plumbline-execute-engine/SKILL.md"
        result = subprocess.run(
            [
                sys.executable,
                str(PLUGIN / "scripts/resolve_front_door.py"),
                "--skill-path",
                str(visible),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            Path(result.stdout.strip()), PLUGIN / "skills/plumbline/SKILL.md"
        )

    def test_front_door_cannot_escape_active_installation(self) -> None:
        outside = self.root / "outside.md"
        outside.write_text("---\nname: plumbline\n---\n", encoding="utf-8")
        front = self.active / "skills/plumbline/SKILL.md"
        front.unlink()
        try:
            front.symlink_to(outside)
        except OSError as exc:
            self.skipTest(f"host cannot create symlinks: {exc}")
        with self.assertRaises(ValueError):
            resolve_front_door(
                [self.active / "skills/plumbline-execute-engine/SKILL.md"]
            )


if __name__ == "__main__":
    unittest.main()
