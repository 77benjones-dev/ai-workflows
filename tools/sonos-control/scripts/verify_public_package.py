#!/usr/bin/env python3
"""Basic public-package verification for sonos-control."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEXT_EXTENSIONS = {".md", ".py", ".txt"}

PATTERNS = {
    "local_user_path": re.compile(r"/Users/|~/"),
    "email": re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}"),
    "secret_marker": re.compile(r"api[_-]?key|token|password|bearer|cookie|private[_-]?key|secret", re.I),
    "private_lan_ip": re.compile(r"\b192\.168\.68\.\d+\b"),
}


def iter_text_files() -> list[Path]:
    return [
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and path.suffix in TEXT_EXTENSIONS
        and path != Path(__file__).resolve()
        and ".venv" not in path.parts
        and "__pycache__" not in path.parts
    ]


def main() -> int:
    failures: list[str] = []
    for path in iter_text_files():
        text = path.read_text(encoding="utf-8")
        for name, pattern in PATTERNS.items():
            for match in pattern.finditer(text):
                if name == "secret_marker" and match.group(0).lower() == "credentials":
                    continue
                failures.append(f"{path.relative_to(ROOT)}: {name}: {match.group(0)}")

    required = [
        ROOT / "README.md",
        ROOT / "SETUP.md",
        ROOT / "AGENTS_SNIPPET.md",
        ROOT / "core" / "codex_sonos.py",
        ROOT / "requirements.txt",
    ]
    for path in required:
        if not path.exists():
            failures.append(f"missing required file: {path.relative_to(ROOT)}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    if "github.com/steipete/sonoscli" not in readme:
        failures.append("README.md must credit github.com/steipete/sonoscli")

    if failures:
        print("Public package verification failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Public package verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
