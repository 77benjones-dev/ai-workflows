from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SonosControlPackageTests(unittest.TestCase):
    def test_cli_help_runs(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "core" / "codex_sonos.py"), "--help"],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Control local Sonos speakers", result.stdout)

    def test_readme_credits_sonoscli(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("github.com/steipete/sonoscli", readme)
        self.assertIn("Peter Steinberger", readme)


if __name__ == "__main__":
    unittest.main()
