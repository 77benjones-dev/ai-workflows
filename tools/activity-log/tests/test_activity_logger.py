from __future__ import annotations

import importlib.util
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
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
        LOGGER.IGNORED_FILENAMES = {LOGGER.LOG_FILENAME, LOGGER.CONTEXT_FILENAME}
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
        self.assertEqual(
            LOGGER.extract_edited_paths(data),
            [(self.root / "notes.md").resolve(), (self.root / "nested" / "new.md").resolve()],
        )

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
        for path in (LOGGER.LOG_PATH, self.root / "CONTEXT.md", Path("/tmp/external.md")):
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
        self.assertTrue((self.root / "CONTEXT.md").exists())
        self.assertIn("Files:** `notes.md`", (self.root / "CONTEXT.md").read_text())

    def test_state_file_contains_logged_path(self) -> None:
        data = {
            "session_id": "session-1",
            "cwd": str(self.root),
            "tool_input": {"file_path": str(self.root / "notes.md")},
        }
        LOGGER.edit(data, "claude")
        state = json.loads(LOGGER.state_path(data, "claude").read_text())
        self.assertEqual(state["logs"][str(LOGGER.LOG_PATH.resolve())]["edited_paths"], ["notes.md"])

    def test_edit_routes_to_nearest_project_log(self) -> None:
        project = self.root / "projects" / "example"
        project.mkdir(parents=True)
        project_log = project / "ACTIVITY_LOG.md"
        project_log.write_text("# Example Activity Log\n")

        data = {
            "session_id": "session-1",
            "cwd": str(project),
            "tool_input": {"file_path": str(project / "notes.md")},
        }
        LOGGER.edit(data, "claude")

        self.assertIn("edited `notes.md`", project_log.read_text())
        self.assertNotIn("notes.md", LOGGER.LOG_PATH.read_text())

    def test_start_prefers_context_snapshot(self) -> None:
        (self.root / "CONTEXT.md").write_text("# Test Context\n\n## Current work\nReady.\n")
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            LOGGER.start({"cwd": str(self.root)}, "codex")

        payload = json.loads(stdout.getvalue())
        context = payload["hookSpecificOutput"]["additionalContext"]
        self.assertIn("Read CONTEXT.md first", context)
        self.assertIn("Ready.", context)

    def test_init_project_creates_log_and_context(self) -> None:
        project = self.root / "new-project"
        LOGGER.init_project(project)

        self.assertTrue((project / "ACTIVITY_LOG.md").exists())
        self.assertTrue((project / "CONTEXT.md").exists())
        self.assertIn("Created project activity log", (project / "ACTIVITY_LOG.md").read_text())


if __name__ == "__main__":
    unittest.main()
