#!/usr/bin/env python3
"""Maintain a workspace-wide activity journal from Claude Code and Codex hooks."""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
LOG_PATH = WORKSPACE_ROOT / "ACTIVITY_LOG.md"
STATE_DIR = WORKSPACE_ROOT / "scratch" / "tmp" / "activity-log"
IGNORED_PATHS = {LOG_PATH}


def read_hook_input() -> dict[str, Any]:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    value = json.loads(raw)
    return value if isinstance(value, dict) else {}


def session_id(data: dict[str, Any]) -> str:
    value = data.get("session_id") or data.get("conversation_id") or "unknown-session"
    return "".join(character for character in str(value) if character.isalnum() or character in "-_")[:120]


def state_path(data: dict[str, Any], platform: str) -> Path:
    return STATE_DIR / f"{platform}-{session_id(data)}.json"


def load_state(data: dict[str, Any], platform: str) -> dict[str, Any]:
    path = state_path(data, platform)
    if not path.exists():
        return {"edited_paths": [], "checkpoint_logged": False}
    try:
        value = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return {"edited_paths": [], "checkpoint_logged": False}
    return value if isinstance(value, dict) else {"edited_paths": [], "checkpoint_logged": False}


def save_state(data: dict[str, Any], platform: str, state: dict[str, Any]) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    state_path(data, platform).write_text(json.dumps(state, indent=2) + "\n")


def timestamp() -> tuple[str, str]:
    now = datetime.now().astimezone()
    return now.strftime("%Y-%m-%d"), now.strftime("%H:%M")


def append_log_line(line: str) -> None:
    day, _ = timestamp()
    LOG_PATH.touch(exist_ok=True)
    content = LOG_PATH.read_text()
    heading = f"## {day}"
    prefix = "" if content.endswith("\n") or not content else "\n"
    if heading not in content:
        prefix += f"\n{heading}\n\n"
    LOG_PATH.write_text(f"{content}{prefix}{line}\n")


def workspace_relative_path(raw_path: Any, cwd: Any) -> str | None:
    if not isinstance(raw_path, str) or not raw_path:
        return None
    path = Path(raw_path).expanduser()
    if not path.is_absolute():
        base = Path(cwd) if isinstance(cwd, str) and cwd else Path.cwd()
        path = base / path
    try:
        resolved = path.resolve()
        workspace_root = WORKSPACE_ROOT.resolve()
        state_dir = STATE_DIR.resolve()
        relative = resolved.relative_to(workspace_root)
    except (OSError, ValueError):
        return None
    # Resolve both sides because macOS temp paths can use /var and /private/var
    # aliases. Without normalization, valid workspace files can look external.
    if resolved in {ignored.resolve() for ignored in IGNORED_PATHS} or state_dir in resolved.parents:
        return None
    return relative.as_posix()


def extract_edited_paths(data: dict[str, Any]) -> list[str]:
    tool_input = data.get("tool_input")
    if not isinstance(tool_input, dict):
        return []

    raw_paths: list[Any] = [tool_input.get("file_path"), tool_input.get("path")]

    # Codex apply_patch payloads can expose only the patch text. Parse explicit
    # patch headers so the log records files without guessing from free text.
    patch = tool_input.get("patch")
    if isinstance(patch, str):
        for line in patch.splitlines():
            for marker in ("*** Add File: ", "*** Update File: ", "*** Delete File: ", "*** Move to: "):
                if line.startswith(marker):
                    raw_paths.append(line.removeprefix(marker))

    paths: list[str] = []
    for raw_path in raw_paths:
        relative = workspace_relative_path(raw_path, data.get("cwd"))
        if relative and relative not in paths:
            paths.append(relative)
    return paths


def start(data: dict[str, Any], platform: str) -> None:
    if not LOG_PATH.exists():
        return
    recent = "\n".join(LOG_PATH.read_text().splitlines()[-28:])
    context = (
        "Workspace continuity: read ACTIVITY_LOG.md before substantive work. "
        "Use project-specific logs for detailed repo history when present.\n\n"
        f"Recent workspace activity:\n{recent}"
    )
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": context}}))


def edit(data: dict[str, Any], platform: str) -> None:
    state = load_state(data, platform)
    edited_paths = state.setdefault("edited_paths", [])
    if not isinstance(edited_paths, list):
        edited_paths = []
        state["edited_paths"] = edited_paths

    _, time = timestamp()
    changed = False
    for path in extract_edited_paths(data):
        if path in edited_paths:
            continue
        append_log_line(f"- `{time}` [{platform}] edited `{path}`")
        edited_paths.append(path)
        changed = True
    if changed:
        save_state(data, platform, state)


def stop(data: dict[str, Any], platform: str) -> None:
    state = load_state(data, platform)
    edited_paths = state.get("edited_paths")
    if not isinstance(edited_paths, list) or not edited_paths or state.get("checkpoint_logged"):
        return
    _, time = timestamp()
    append_log_line(f"- `{time}` [{platform}] activity checkpoint after {len(edited_paths)} logged file edit(s)")
    state["checkpoint_logged"] = True
    save_state(data, platform, state)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("event", choices=("start", "edit", "stop"))
    parser.add_argument("--platform", choices=("claude", "codex"), required=True)
    args = parser.parse_args()

    try:
        data = read_hook_input()
        {"start": start, "edit": edit, "stop": stop}[args.event](data, args.platform)
    except Exception as error:  # Hooks should never interrupt normal workspace work.
        if os.environ.get("ACTIVITY_LOG_DEBUG") == "1":
            raise
        print(f"activity-log hook skipped: {error}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
