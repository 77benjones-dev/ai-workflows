#!/usr/bin/env python3
"""Shared install helpers for the public activity-log package."""

from __future__ import annotations

import copy
import json
import os
import shlex
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
MARKER = "# activity-log-package"


def require_supported_runtime() -> None:
    if sys.version_info < (3, 10):
        raise RuntimeError("Python 3.10 or newer is required.")
    if os.name == "nt":
        raise RuntimeError("Windows is not supported yet. This release is tested on macOS and Linux.")


def resolve_workspace(raw_workspace: str) -> Path:
    workspace = Path(raw_workspace).expanduser().resolve()
    if not workspace.is_dir():
        raise RuntimeError(f"Workspace directory does not exist: {workspace}")
    return workspace


def logger_path(workspace: Path) -> Path:
    return workspace / "tools" / "activity-log" / "activity_logger.py"


def command(workspace: Path, event: str, platform: str) -> str:
    return f"python3 {shlex.quote(str(logger_path(workspace)))} {event} --platform {platform} {MARKER}"


def config_specs(workspace: Path) -> list[tuple[Path, dict[str, list[dict[str, Any]]]]]:
    claude = {
        "SessionStart": [
            {
                "matcher": "startup|resume|clear|compact",
                "hooks": [{"type": "command", "command": command(workspace, "start", "claude"), "async": False}],
            }
        ],
        "PostToolUse": [
            {
                "matcher": "Edit|Write|MultiEdit",
                "hooks": [{"type": "command", "command": command(workspace, "edit", "claude"), "async": False}],
            }
        ],
        "Stop": [{"hooks": [{"type": "command", "command": command(workspace, "stop", "claude"), "async": False}]}],
    }
    codex = {
        "SessionStart": [
            {
                "matcher": "startup|resume|clear|compact",
                "hooks": [
                    {
                        "type": "command",
                        "command": command(workspace, "start", "codex"),
                        "statusMessage": "Loading workspace activity log",
                    }
                ],
            }
        ],
        "PostToolUse": [
            {
                "matcher": "Edit|Write",
                "hooks": [
                    {
                        "type": "command",
                        "command": command(workspace, "edit", "codex"),
                        "statusMessage": "Recording workspace edit",
                    }
                ],
            }
        ],
        "Stop": [
            {
                "hooks": [
                    {
                        "type": "command",
                        "command": command(workspace, "stop", "codex"),
                        "statusMessage": "Recording workspace checkpoint",
                    }
                ]
            }
        ],
    }
    return [(workspace / ".claude" / "settings.json", claude), (workspace / ".codex" / "hooks.json", codex)]


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        value = json.loads(path.read_text())
    except json.JSONDecodeError as error:
        raise RuntimeError(f"Cannot update invalid JSON file: {path}: {error}") from error
    if not isinstance(value, dict):
        raise RuntimeError(f"Expected a JSON object in: {path}")
    return value


def has_command(config: dict[str, Any], target: str) -> bool:
    hooks = config.get("hooks", {})
    if not isinstance(hooks, dict):
        return False
    for groups in hooks.values():
        if not isinstance(groups, list):
            continue
        for group in groups:
            if not isinstance(group, dict):
                continue
            handlers = group.get("hooks", [])
            if isinstance(handlers, list) and any(
                isinstance(handler, dict) and handler.get("command") == target for handler in handlers
            ):
                return True
    return False


def merge_hooks(config: dict[str, Any], specs: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    merged = copy.deepcopy(config)
    hooks = merged.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        raise RuntimeError("Expected the existing 'hooks' value to be a JSON object.")
    for event, groups in specs.items():
        target_groups = hooks.setdefault(event, [])
        if not isinstance(target_groups, list):
            raise RuntimeError(f"Expected hooks.{event} to be a JSON array.")
        for group in groups:
            handler = group["hooks"][0]
            if not has_command(merged, handler["command"]):
                target_groups.append(copy.deepcopy(group))
    return merged


def remove_package_hooks(config: dict[str, Any]) -> dict[str, Any]:
    cleaned = copy.deepcopy(config)
    hooks = cleaned.get("hooks")
    if not isinstance(hooks, dict):
        return cleaned
    for event in list(hooks):
        groups = hooks[event]
        if not isinstance(groups, list):
            continue
        remaining_groups = []
        for group in groups:
            if not isinstance(group, dict):
                remaining_groups.append(group)
                continue
            handlers = group.get("hooks")
            if not isinstance(handlers, list):
                remaining_groups.append(group)
                continue
            remaining_handlers = [
                handler
                for handler in handlers
                if not (isinstance(handler, dict) and MARKER in str(handler.get("command", "")))
            ]
            if remaining_handlers:
                updated_group = copy.deepcopy(group)
                updated_group["hooks"] = remaining_handlers
                remaining_groups.append(updated_group)
        if remaining_groups:
            hooks[event] = remaining_groups
        else:
            del hooks[event]
    if not hooks:
        cleaned.pop("hooks", None)
    return cleaned


def backup(path: Path) -> Path:
    stamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    destination = path.with_name(f"{path.name}.backup.{stamp}")
    shutil.copy2(path, destination)
    return destination


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def copy_if_changed(source: Path, destination: Path) -> bool:
    if destination.exists() and destination.read_bytes() == source.read_bytes():
        return False
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        backup(destination)
    shutil.copy2(source, destination)
    return True
