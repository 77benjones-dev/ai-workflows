#!/usr/bin/env python3
"""Remove activity-log hooks and unchanged helper files from a workspace."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from common import PACKAGE_ROOT, backup, config_specs, read_json, remove_package_hooks, require_supported_runtime
from common import resolve_workspace, write_json


def installed_files(workspace: Path) -> list[tuple[Path, Path]]:
    return [
        (PACKAGE_ROOT / "core" / "activity_logger.py", workspace / "tools" / "activity-log" / "activity_logger.py"),
        (
            PACKAGE_ROOT / "core" / "MILESTONE_TEMPLATE.md",
            workspace / "tools" / "activity-log" / "MILESTONE_TEMPLATE.md",
        ),
        (PACKAGE_ROOT / "AGENTS_SNIPPET.md", workspace / "tools" / "activity-log" / "AGENTS_SNIPPET.md"),
    ]


def report_plan(workspace: Path) -> None:
    print("Dry run. No files will be changed. Re-run with --apply to uninstall.\n")
    for path, _ in config_specs(workspace):
        print(f"- remove package hooks: {path}")
    for _, destination in installed_files(workspace):
        print(f"- remove if unchanged: {destination}")
    print(f"- keep: {workspace / 'ACTIVITY_LOG.md'}")


def apply_uninstall(workspace: Path) -> None:
    for path, _ in config_specs(workspace):
        if not path.exists():
            continue
        current = read_json(path)
        cleaned = remove_package_hooks(current)
        if cleaned == current:
            continue
        print(f"Backup: {backup(path)}")
        write_json(path, cleaned)
        print(f"Removed package hooks: {path}")

    for source, destination in installed_files(workspace):
        if not destination.exists():
            continue
        if destination.read_bytes() != source.read_bytes():
            print(f"Kept modified file: {destination}")
            continue
        destination.unlink()
        print(f"Removed: {destination}")

    helper_dir = workspace / "tools" / "activity-log"
    if helper_dir.exists() and not any(helper_dir.iterdir()):
        helper_dir.rmdir()
    print(f"Kept activity history: {workspace / 'ACTIVITY_LOG.md'}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True, help="Workspace folder where the workflow is installed.")
    parser.add_argument("--apply", action="store_true", help="Write the planned changes.")
    args = parser.parse_args()
    try:
        require_supported_runtime()
        workspace = resolve_workspace(args.workspace)
        if args.apply:
            apply_uninstall(workspace)
        else:
            report_plan(workspace)
        return 0
    except RuntimeError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
