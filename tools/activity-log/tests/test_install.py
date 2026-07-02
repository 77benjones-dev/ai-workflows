from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
INSTALLER = PACKAGE_ROOT / "scripts" / "install.py"
UNINSTALLER = PACKAGE_ROOT / "scripts" / "uninstall.py"


class InstallTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory(prefix="activity log package ")
        self.workspace = Path(self.temp_dir.name) / "workspace with spaces"
        self.workspace.mkdir()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def run_script(self, script: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(script), "--workspace", str(self.workspace), *args],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_default_run_is_a_dry_run(self) -> None:
        result = self.run_script(INSTALLER)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Dry run", result.stdout)
        self.assertFalse((self.workspace / "ACTIVITY_LOG.md").exists())
        self.assertFalse((self.workspace / "CONTEXT.md").exists())
        self.assertFalse((self.workspace / ".claude" / "settings.json").exists())
        self.assertFalse((self.workspace / ".codex" / "hooks.json").exists())

    def test_apply_installs_both_adapters_and_check_passes(self) -> None:
        result = self.run_script(INSTALLER, "--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.workspace / "ACTIVITY_LOG.md").exists())
        self.assertTrue((self.workspace / "CONTEXT.md").exists())
        self.assertTrue((self.workspace / "tools" / "activity-log" / "activity_logger.py").exists())
        self.assertTrue((self.workspace / "tools" / "activity-log" / "MILESTONE_TEMPLATE.md").exists())
        self.assertTrue((self.workspace / "tools" / "activity-log" / "AGENTS_SNIPPET.md").exists())

        claude = json.loads((self.workspace / ".claude" / "settings.json").read_text())
        codex = json.loads((self.workspace / ".codex" / "hooks.json").read_text())
        self.assertIn("hooks", claude)
        self.assertIn("hooks", codex)
        installed_logger = (self.workspace / "tools" / "activity-log" / "activity_logger.py").resolve()
        self.assertIn(f"'{installed_logger}'", json.dumps(codex))

        check = self.run_script(INSTALLER, "--check")
        self.assertEqual(check.returncode, 0, check.stdout + check.stderr)
        self.assertIn("Install check passed", check.stdout)

    def test_apply_preserves_existing_hooks_and_is_idempotent(self) -> None:
        claude_path = self.workspace / ".claude" / "settings.json"
        claude_path.parent.mkdir()
        claude_path.write_text(
            json.dumps(
                {
                    "hooks": {
                        "SessionStart": [
                            {
                                "matcher": "startup",
                                "hooks": [{"type": "command", "command": "printf existing"}],
                            }
                        ]
                    }
                },
                indent=2,
            )
            + "\n"
        )

        first = self.run_script(INSTALLER, "--apply")
        second = self.run_script(INSTALLER, "--apply")
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(second.returncode, 0, second.stderr)

        text = claude_path.read_text()
        self.assertIn("printf existing", text)
        self.assertEqual(text.count("activity_logger.py"), 3)
        self.assertTrue(list(claude_path.parent.glob("settings.json.backup.*")))

    def test_uninstall_removes_only_package_hooks_and_keeps_log(self) -> None:
        self.assertEqual(self.run_script(INSTALLER, "--apply").returncode, 0)
        claude_path = self.workspace / ".claude" / "settings.json"
        claude = json.loads(claude_path.read_text())
        claude["hooks"]["SessionStart"].append(
            {"matcher": "startup", "hooks": [{"type": "command", "command": "printf existing"}]}
        )
        claude_path.write_text(json.dumps(claude, indent=2) + "\n")

        dry_run = self.run_script(UNINSTALLER)
        self.assertEqual(dry_run.returncode, 0, dry_run.stderr)
        self.assertIn("Dry run", dry_run.stdout)
        self.assertTrue((self.workspace / "tools" / "activity-log" / "activity_logger.py").exists())

        result = self.run_script(UNINSTALLER, "--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.workspace / "ACTIVITY_LOG.md").exists())
        self.assertTrue((self.workspace / "CONTEXT.md").exists())
        self.assertIn("printf existing", claude_path.read_text())
        self.assertNotIn("activity_logger.py", claude_path.read_text())


if __name__ == "__main__":
    unittest.main()
