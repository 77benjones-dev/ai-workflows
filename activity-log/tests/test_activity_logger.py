from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "core" / "activity_logger.py"
SPEC = importlib.util.spec_from_file_location("activity_logger", SCRIPT)
assert SPEC and SPEC.loader
LOGGER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LOGGER)


class ActivityLoggerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory(prefix="activity logger ")
        self.root = Path(self.temp_dir.name)
        LOGGER.WORKSPACE_ROOT = self.root
        LOGGER.LOG_PATH = self.root / "ACTIVITY_LOG.md"
        LOGGER.STATE_DIR = self.root / "scratch" / "tmp" / "activity-log"
        LOGGER.IGNORED_PATHS = {LOGGER.LOG_PATH}
        LOGGER.LOG_PATH.write_text("# Test Log\n")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_extracts_paths_from_apply_patch_payload(self) -> None:
        data = {
            "cwd": str(self.root),
            "tool_input": {
                "patch": "*** Begin Patch\n*** Update File: notes.md\n*** Add File: nested/new.md\n*** End Patch\n"
            },
        }
        self.assertEqual(LOGGER.extract_edited_paths(data), ["notes.md", "nested/new.md"])

    def test_edit_dedupes_paths_within_a_session(self) -> None:
        data = {
            "session_id": "session-1",
            "cwd": str(self.root),
            "tool_input": {"file_path": str(self.root / "notes.md")},
        }
        LOGGER.edit(data, "claude")
        LOGGER.edit(data, "claude")
        self.assertEqual(LOGGER.LOG_PATH.read_text().count("edited `notes.md`"), 1)

    def test_edit_ignores_workspace_log_and_external_files(self) -> None:
        for path in (LOGGER.LOG_PATH, Path("/tmp/external.md")):
            LOGGER.edit(
                {"session_id": "session-1", "cwd": str(self.root), "tool_input": {"file_path": str(path)}},
                "codex",
            )
        self.assertEqual(LOGGER.LOG_PATH.read_text(), "# Test Log\n")

    def test_stop_logs_one_checkpoint_only_after_an_edit(self) -> None:
        data = {
            "session_id": "session-1",
            "cwd": str(self.root),
            "tool_input": {"file_path": str(self.root / "notes.md")},
        }
        LOGGER.stop(data, "codex")
        LOGGER.edit(data, "codex")
        LOGGER.stop(data, "codex")
        LOGGER.stop(data, "codex")
        self.assertEqual(LOGGER.LOG_PATH.read_text().count("[codex] activity checkpoint"), 1)

    def test_state_file_contains_logged_path(self) -> None:
        data = {
            "session_id": "session-1",
            "cwd": str(self.root),
            "tool_input": {"file_path": str(self.root / "notes.md")},
        }
        LOGGER.edit(data, "claude")
        state = json.loads(LOGGER.state_path(data, "claude").read_text())
        self.assertEqual(state["edited_paths"], ["notes.md"])


if __name__ == "__main__":
    unittest.main()
