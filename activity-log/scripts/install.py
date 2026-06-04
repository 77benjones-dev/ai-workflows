#!/usr/bin/env python3
"""Install the public activity-log workflow into a local workspace."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from common import PACKAGE_ROOT, config_specs, copy_if_changed, has_command, logger_path, merge_hooks, read_json
from common import require_supported_runtime, resolve_workspace, write_json


def file_plan(workspace: Path) -> list[tuple[Path, Path, bool]]:
    return [
        (PACKAGE_ROOT / "core" / "activity_logger.py", logger_path(workspace), True),
        (
            PACKAGE_ROOT / "core" / "MILESTONE_TEMPLATE.md",
            workspace / "tools" / "activity-log" / "MILESTONE_TEMPLATE.md",
            True,
        ),
        (
            PACKAGE_ROOT / "AGENTS_SNIPPET.md",
            workspace / "tools" / "activity-log" / "AGENTS_SNIPPET.md",
            True,
        ),
        (PACKAGE_ROOT / "core" / "ACTIVITY_LOG.template.md", workspace / "ACTIVITY_LOG.md", False),
    ]


def report_plan(workspace: Path) -> None:
    print("Dry run. No files will be changed. Re-run with --apply to install.\n")
    for _, destination, overwrite in file_plan(workspace):
        if destination.exists():
            action = "keep" if not overwrite else "update if changed"
        else:
            action = "create"
        print(f"- {action}: {destination}")
    for path, _ in config_specs(workspace):
        print(f"- merge hooks: {path}")
    print(f"- review and add manually: {workspace / 'tools' / 'activity-log' / 'AGENTS_SNIPPET.md'}")


def apply_install(workspace: Path) -> None:
    for source, destination, overwrite in file_plan(workspace):
        if destination.exists() and not overwrite:
            print(f"Kept existing: {destination}")
            continue
        changed = copy_if_changed(source, destination)
        print(f"{'Installed' if changed else 'Already current'}: {destination}")

    for path, specs in config_specs(workspace):
        current = read_json(path)
        merged = merge_hooks(current, specs)
        if merged == current:
            print(f"Hooks already current: {path}")
            continue
        if path.exists():
            from common import backup

            print(f"Backup: {backup(path)}")
        write_json(path, merged)
        print(f"Updated hooks: {path}")

    print("\nNext steps:")
    print(f"1. Review and merge: {workspace / 'tools' / 'activity-log' / 'AGENTS_SNIPPET.md'}")
    print("2. Restart Claude Code or Codex in the workspace.")
    print("3. In Codex, run /hooks and trust the new workspace hooks.")


def check_install(workspace: Path) -> int:
    errors: list[str] = []
    for _, destination, _ in file_plan(workspace):
        if not destination.exists():
            errors.append(f"Missing: {destination}")
    for path, specs in config_specs(workspace):
        try:
            config = read_json(path)
        except RuntimeError as error:
            errors.append(str(error))
            continue
        for groups in specs.values():
            for group in groups:
                target = group["hooks"][0]["command"]
                if not has_command(config, target):
                    errors.append(f"Missing activity-log hook in: {path}: {target}")
    if errors:
        print("Install check failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Install check passed.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True, help="Workspace folder where the workflow should be installed.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true", help="Write the planned changes.")
    mode.add_argument("--check", action="store_true", help="Check an existing installation.")
    args = parser.parse_args()
    try:
        require_supported_runtime()
        workspace = resolve_workspace(args.workspace)
        if args.check:
            return check_install(workspace)
        if args.apply:
            apply_install(workspace)
        else:
            report_plan(workspace)
        return 0
    except RuntimeError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
