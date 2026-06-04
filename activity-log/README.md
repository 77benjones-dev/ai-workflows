# Activity Log

A small cross-session continuity system for Claude Code and Codex.

AI sessions are short-lived. Projects are not. This package adds a plain-markdown workspace journal so an agent can see what changed, why it changed, and where to resume.

## What It Installs

```text
<workspace>/
  ACTIVITY_LOG.md
  tools/activity-log/
    activity_logger.py
    MILESTONE_TEMPLATE.md
    AGENTS_SNIPPET.md
  .claude/settings.json
  .codex/hooks.json
```

The installer merges activity-log hooks into existing Claude Code and Codex config files. It does not overwrite existing activity history or edit `AGENTS.md` automatically.

## How It Works

The package uses a hybrid model:

- Hooks record a deduplicated trail of edited files and lightweight activity checkpoints.
- A session-start hook surfaces recent workspace history.
- Agent instructions ask the agent to add narrative milestones after substantive work.

The hooks tell you what changed. Narrative milestones explain why it changed.

Milestones can capture the goal, decisions, process, resources used, dead ends, verification, next step, and story notes. That makes the log useful for resuming work, writing retrospectives, extracting reusable workflows, and reconstructing an article outline later.

## Install

Preview the changes first:

```bash
python3 scripts/install.py --workspace "/path/to/workspace"
```

Apply the install:

```bash
python3 scripts/install.py --workspace "/path/to/workspace" --apply
```

Check an existing installation:

```bash
python3 scripts/install.py --workspace "/path/to/workspace" --check
```

The easiest path is to download this folder, open your agent in the package directory, and ask:

```text
Follow SETUP.md to install the activity-log package into my workspace.
Preview the changes first. Do not apply them until I approve the plan.
```

See [SETUP.md](SETUP.md) for the full agent-readable workflow.

## Uninstall

Preview the removal:

```bash
python3 scripts/uninstall.py --workspace "/path/to/workspace"
```

Apply it:

```bash
python3 scripts/uninstall.py --workspace "/path/to/workspace" --apply
```

Uninstall removes only package-owned hook entries and unchanged helper files. It leaves `ACTIVITY_LOG.md` in place so your history is preserved.

## Requirements

- Python 3.10 or newer
- macOS or Linux
- Claude Code, Codex, or both

The package uses only the Python standard library. It does not require Node, `jq`, Git, Homebrew, or a specific shell.

Windows is not supported in this first release. Windows support needs separate command quoting and tested `commandWindows` hook entries.

## Activation Notes

- Restart Claude Code or Codex in the target workspace after installation.
- Codex users must run `/hooks` and review or trust the new workspace hooks.
- Review hook scripts before trusting them. Hooks execute local commands as part of the agent lifecycle.

## What It Does Not Do

- It does not send data to an external service.
- It does not record full transcripts.
- It does not overwrite an existing `ACTIVITY_LOG.md`.
- It does not edit `AGENTS.md` automatically.
- It does not generate automatic transcript summaries.

Narrative milestones still depend on agent behavior. The edit trail is the automated baseline.

## Verify This Package

```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
python3 scripts/verify_public_package.py
```
