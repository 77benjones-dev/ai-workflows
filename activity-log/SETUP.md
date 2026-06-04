# Set Up the Activity Log Package

This file is written for an AI agent helping a user install the package.

## Goal

Install the activity-log workflow into a user-selected workspace without overwriting existing logs, agent instructions, or unrelated hook configuration.

## Safety Rules

- Preview the install before applying it.
- Ask the user to approve the dry-run plan before using `--apply`.
- Do not edit `AGENTS.md` automatically. Read the generated snippet and merge it thoughtfully after user approval.
- Preserve existing `ACTIVITY_LOG.md` content.
- Preserve existing Claude Code and Codex hooks.
- Review changed config files after installation.
- Do not install on Windows. This release is tested on macOS and Linux only.

## Steps

1. Confirm the target workspace path with the user.
2. Check that Python 3.10 or newer is available:

   ```bash
   python3 --version
   ```

3. Preview the install:

   ```bash
   python3 scripts/install.py --workspace "/path/to/workspace"
   ```

4. Show the user the planned changes and ask for approval.
5. Apply the install:

   ```bash
   python3 scripts/install.py --workspace "/path/to/workspace" --apply
   ```

6. Review:

   ```text
   <workspace>/.claude/settings.json
   <workspace>/.codex/hooks.json
   <workspace>/tools/activity-log/AGENTS_SNIPPET.md
   ```

7. Merge the snippet into the workspace `AGENTS.md` only after the user approves the wording and location.
8. Check the installation:

   ```bash
   python3 scripts/install.py --workspace "/path/to/workspace" --check
   ```

9. Tell the user to restart Claude Code or Codex in the workspace.
10. Tell Codex users to run `/hooks` and review or trust the new hooks.

## Expected Behavior

- `ACTIVITY_LOG.md` exists at the workspace root.
- Hook commands point to the target workspace, including when its path contains spaces.
- Existing config is preserved.
- Re-running the installer does not duplicate hooks.
- Config files receive timestamped backups before existing content is changed.
- `AGENTS.md` remains unchanged until the user or agent deliberately merges the snippet.

## Uninstall

Preview removal first:

```bash
python3 scripts/uninstall.py --workspace "/path/to/workspace"
```

After user approval:

```bash
python3 scripts/uninstall.py --workspace "/path/to/workspace" --apply
```

The uninstaller keeps `ACTIVITY_LOG.md` and preserves modified helper files.
