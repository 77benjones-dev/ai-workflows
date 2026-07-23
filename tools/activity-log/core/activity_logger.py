#!/usr/bin/env python3
"""Maintain activity journals and context snapshots from Claude Code and Codex hooks."""

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
LOG_FILENAME = "ACTIVITY_LOG.md"
CONTEXT_FILENAME = "CONTEXT.md"
IGNORED_PATHS = {
    LOG_PATH,
}
IGNORED_FILENAMES = {
    LOG_FILENAME,
    CONTEXT_FILENAME,
}


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


def default_state() -> dict[str, Any]:
    return {"logs": {}}


def load_state(data: dict[str, Any], platform: str) -> dict[str, Any]:
    path = state_path(data, platform)
    if not path.exists():
        return default_state()
    try:
        value = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return default_state()
    if not isinstance(value, dict):
        return default_state()
    if "logs" not in value:
        value = {
            "logs": {
                str(LOG_PATH): {
                    "edited_paths": value.get("edited_paths", []),
                    "checkpoint_logged": value.get("checkpoint_logged", False),
                }
            }
        }
    return value


def save_state(data: dict[str, Any], platform: str, state: dict[str, Any]) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    state_path(data, platform).write_text(json.dumps(state, indent=2) + "\n")


def timestamp() -> tuple[str, str]:
    now = datetime.now().astimezone()
    return now.strftime("%Y-%m-%d"), now.strftime("%H:%M")


def append_log_line(log_path: Path, line: str) -> None:
    day, _ = timestamp()
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.touch(exist_ok=True)
    content = log_path.read_text()
    heading = f"## {day}"
    prefix = "" if content.endswith("\n") or not content else "\n"
    if heading not in content:
        prefix += f"\n{heading}\n\n"
    log_path.write_text(f"{content}{prefix}{line}\n")


def workspace_path(raw_path: Any, cwd: Any = None) -> Path | None:
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
        resolved.relative_to(workspace_root)
    except (OSError, ValueError):
        return None
    if (
        resolved.name in IGNORED_FILENAMES
        or resolved in {path.resolve() for path in IGNORED_PATHS}
        or state_dir in resolved.parents
    ):
        return None
    return resolved


def nearest_log_path(start: Path) -> Path:
    """Find the nearest existing project log, falling back to the workspace log."""

    try:
        resolved = start.resolve()
        workspace_root = WORKSPACE_ROOT.resolve()
        resolved.relative_to(workspace_root)
    except (OSError, ValueError):
        return LOG_PATH

    current = resolved if resolved.is_dir() else resolved.parent
    while True:
        candidate = current / LOG_FILENAME
        if candidate.exists():
            return candidate
        if current == workspace_root:
            return LOG_PATH
        if current.parent == current:
            return LOG_PATH
        current = current.parent


def context_path_for_log(log_path: Path) -> Path:
    return log_path.with_name(CONTEXT_FILENAME)


def path_relative_to_log(path: Path, log_path: Path) -> str:
    try:
        return path.resolve().relative_to(log_path.parent.resolve()).as_posix()
    except (OSError, ValueError):
        try:
            return path.resolve().relative_to(WORKSPACE_ROOT.resolve()).as_posix()
        except (OSError, ValueError):
            return path.name


def extract_edited_paths(data: dict[str, Any]) -> list[Path]:
    tool_input = data.get("tool_input")
    if not isinstance(tool_input, dict):
        return []

    raw_paths: list[Any] = []
    raw_paths.append(tool_input.get("file_path"))
    raw_paths.append(tool_input.get("path"))

    # Codex apply_patch payloads can expose only the patch text. Keep parsing
    # narrow so the log records explicit patch file headers without guessing.
    patch = tool_input.get("patch")
    if isinstance(patch, str):
        for line in patch.splitlines():
            for marker in ("*** Add File: ", "*** Update File: ", "*** Delete File: ", "*** Move to: "):
                if line.startswith(marker):
                    raw_paths.append(line.removeprefix(marker))

    paths: list[Path] = []
    for raw_path in raw_paths:
        resolved = workspace_path(raw_path, data.get("cwd"))
        if resolved and resolved not in paths:
            paths.append(resolved)
    return paths


def log_state(state: dict[str, Any], log_path: Path) -> dict[str, Any]:
    logs = state.setdefault("logs", {})
    if not isinstance(logs, dict):
        logs = {}
        state["logs"] = logs
    entry = logs.setdefault(str(log_path), {"edited_paths": [], "checkpoint_logged": False})
    if not isinstance(entry, dict):
        entry = {"edited_paths": [], "checkpoint_logged": False}
        logs[str(log_path)] = entry
    if not isinstance(entry.get("edited_paths"), list):
        entry["edited_paths"] = []
    return entry


def project_title(log_path: Path) -> str:
    if log_path.exists():
        for line in log_path.read_text().splitlines():
            if line.startswith("# "):
                title = line.removeprefix("# ").strip()
                for suffix in (" Activity Log", " - Activity Log"):
                    if title.endswith(suffix):
                        title = title[: -len(suffix)]
                return title.strip() or log_path.parent.name.replace("-", " ").title()
    return log_path.parent.name.replace("-", " ").title()


def last_prefixed_line(lines: list[str], prefixes: tuple[str, ...]) -> str | None:
    for line in reversed(lines):
        stripped = line.strip()
        for prefix in prefixes:
            if stripped.startswith(prefix):
                return stripped.removeprefix(prefix).strip()
    return None


def last_date_heading(lines: list[str]) -> str:
    for line in reversed(lines):
        stripped = line.strip()
        if stripped.startswith("## ") and len(stripped) >= 13:
            return stripped.removeprefix("## ").strip()
    return timestamp()[0]


def recent_edited_files(lines: list[str], edited_paths: list[str]) -> list[str]:
    files: list[str] = []
    for path in edited_paths:
        if path not in files:
            files.append(path)
    for line in reversed(lines):
        if " edited `" not in line:
            continue
        parts = line.split("`")
        if len(parts) >= 4 and parts[3] not in files:
            files.append(parts[3])
        if len(files) >= 6:
            break
    return files[:6]


def render_context(log_path: Path, edited_paths: list[str] | None = None) -> str:
    text = log_path.read_text() if log_path.exists() else ""
    lines = text.splitlines()
    title = project_title(log_path)
    decision = last_prefixed_line(lines, ("- Decision:", "Decision:"))
    next_step = last_prefixed_line(lines, ("- Next:", "Next:"))
    files = recent_edited_files(lines, edited_paths or [])
    files_text = ", ".join(f"`{path}`" for path in files) if files else "`ACTIVITY_LOG.md`"
    return (
        f"# {title} Context\n\n"
        "## Current work\n"
        f"**Last active:** {last_date_heading(lines)}\n"
        "**Status:** Recent activity is recorded in `ACTIVITY_LOG.md`.\n"
        f"**Last decision:** {decision or 'No recent decision recorded.'}\n"
        f"**Next step:** {next_step or 'Review `ACTIVITY_LOG.md` for the next concrete action.'}\n"
        f"**Files:** {files_text}\n"
    )


def init_project(project_path: Path) -> None:
    project_path.mkdir(parents=True, exist_ok=True)
    name = project_path.name.replace("-", " ").replace("_", " ").title()
    log_path = project_path / LOG_FILENAME
    context_path = project_path / CONTEXT_FILENAME
    day, _ = timestamp()
    if not log_path.exists():
        log_path.write_text(
            f"# {name} Activity Log\n\n"
            f"## {day}\n\n"
            "- Decision: Created project activity log.\n"
            "- Next: Use this log for future project handoffs.\n"
        )
    if not context_path.exists():
        context_path.write_text(render_context(log_path))


def start(data: dict[str, Any], platform: str) -> None:
    cwd = workspace_path(data.get("cwd") or str(WORKSPACE_ROOT), str(WORKSPACE_ROOT))
    log_path = nearest_log_path(cwd or WORKSPACE_ROOT)
    context_path = context_path_for_log(log_path)
    if context_path.exists():
        context_text = context_path.read_text()
        context = (
            "Workspace continuity: Read CONTEXT.md first. "
            "Use ACTIVITY_LOG.md only when deeper history is needed.\n\n"
            f"Project context from {path_relative_to_log(context_path, LOG_PATH)}:\n{context_text}"
        )
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": context}}))
        return

    if not log_path.exists():
        return
    lines = log_path.read_text().splitlines()
    recent = "\n".join(lines[-28:])
    context = (
        "Workspace continuity: read ACTIVITY_LOG.md before substantive work. "
        "Use project-specific logs for detailed repo history when present.\n\n"
        f"Recent activity from {path_relative_to_log(log_path, LOG_PATH)}:\n{recent}"
    )
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": context}}))


def edit(data: dict[str, Any], platform: str) -> None:
    state = load_state(data, platform)

    _, time = timestamp()
    changed = False
    for path in extract_edited_paths(data):
        log_path = nearest_log_path(path)
        entry = log_state(state, log_path)
        edited_paths = entry["edited_paths"]
        relative = path_relative_to_log(path, log_path)
        if relative in edited_paths:
            continue
        append_log_line(log_path, f"- `{time}` [{platform}] edited `{relative}`")
        edited_paths.append(relative)
        changed = True
    if changed:
        save_state(data, platform, state)


def stop(data: dict[str, Any], platform: str) -> None:
    state = load_state(data, platform)
    _, time = timestamp()
    logs = state.get("logs")
    target_logs: dict[str, Any] = logs if isinstance(logs, dict) else {}
    if not target_logs:
        cwd = workspace_path(data.get("cwd") or str(WORKSPACE_ROOT), str(WORKSPACE_ROOT))
        log_path = nearest_log_path(cwd or WORKSPACE_ROOT)
        target_logs = {str(log_path): {"edited_paths": [], "checkpoint_logged": False}}
        state["logs"] = target_logs

    changed = False
    for raw_log_path, _entry in target_logs.items():
        log_path = Path(raw_log_path)
        log_entry = log_state(state, log_path)
        edited_paths = log_entry.get("edited_paths")
        if not isinstance(edited_paths, list):
            edited_paths = []
            log_entry["edited_paths"] = edited_paths
        if edited_paths and not log_entry.get("checkpoint_logged"):
            append_log_line(log_path, f"- `{time}` [{platform}] activity checkpoint after {len(edited_paths)} logged file edit(s)")
            log_entry["checkpoint_logged"] = True
            changed = True
        if log_path.exists():
            context_path_for_log(log_path).write_text(render_context(log_path, edited_paths))
            changed = True
    if changed:
        save_state(data, platform, state)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("event", choices=("start", "edit", "stop", "init"))
    parser.add_argument("--platform", choices=("claude", "codex"), default="codex")
    parser.add_argument("--path")
    args = parser.parse_args()

    try:
        if args.event == "init":
            if not args.path:
                parser.error("init requires --path")
            init_project(Path(args.path).expanduser())
        else:
            data = read_hook_input()
            {"start": start, "edit": edit, "stop": stop}[args.event](data, args.platform)
    except Exception as error:  # Hooks should never interrupt normal workspace work.
        if os.environ.get("ACTIVITY_LOG_DEBUG") == "1":
            raise
        print(f"activity-log hook skipped: {error}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
