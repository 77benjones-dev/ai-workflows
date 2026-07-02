from __future__ import annotations

import subprocess
import sys
import unittest
import shutil
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
VERIFY = PACKAGE_ROOT / "scripts" / "verify_public_package.py"


class PublicPackageTest(unittest.TestCase):
    def test_public_package_scan_passes(self) -> None:
        for cache_dir in PACKAGE_ROOT.rglob("__pycache__"):
            shutil.rmtree(cache_dir)
        result = subprocess.run(
            [sys.executable, str(VERIFY)],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Public package scan passed", result.stdout)


if __name__ == "__main__":
    unittest.main()
