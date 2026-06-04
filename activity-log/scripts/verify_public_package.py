#!/usr/bin/env python3
"""Scan the package for common public-sharing mistakes."""

from __future__ import annotations

import re
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".md", ".py", ".json", ".txt"}
PATTERNS = {
    "macOS home directory": re.compile("/" + "Users/"),
    "Linux home directory": re.compile("/" + "home/"),
    "OpenAI-style secret": re.compile("sk-" + r"[A-Za-z0-9_-]{16,}"),
    "GitHub token": re.compile("gh" + r"[pousr]_[A-Za-z0-9]{20,}"),
    "AWS access key": re.compile("AKIA" + r"[A-Z0-9]{16}"),
    "private key": re.compile("BEGIN " + r"(?:RSA |EC |OPENSSH )?PRIVATE KEY"),
}


def scan() -> list[str]:
    errors: list[str] = []
    for path in sorted(PACKAGE_ROOT.rglob("*")):
        relative = path.relative_to(PACKAGE_ROOT)
        if path.name == ".DS_Store":
            errors.append(f"Generated local state: {relative}")
            continue
        if "__pycache__" in path.parts:
            if path.is_dir():
                errors.append(f"Generated cache directory: {relative}")
            continue
        if path.suffix == ".pyc":
            errors.append(f"Generated cache file: {relative}")
            continue
        if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
            continue
        text = path.read_text(errors="replace")
        for label, pattern in PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{label}: {relative}")
    return errors


def main() -> int:
    errors = scan()
    if errors:
        print("Public package scan failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Public package scan passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
