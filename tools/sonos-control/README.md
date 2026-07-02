# Sonos Control

A small local-network Sonos control package for Codex, Claude Code, or another terminal-based AI agent.

It lets an agent discover speakers, inspect status, pause/play, adjust volume, inspect groups, and list/open Sonos favorites without using OpenClaw, Sonos cloud APIs, or a separate Go CLI binary.

## Credit

This workflow was inspired by the public Sonos CLI package by Peter Steinberger:

- Repository/module: `github.com/steipete/sonoscli/cmd/sonos@latest`
- Homepage: `https://sonoscli.sh`

That project is a fuller standalone Go CLI. This package is a lightweight Python/SoCo adaptation designed to be copied into an AI-agent workspace and called directly from Codex or Claude Code.

## What It Installs

```text
<workspace>/
  tools/sonos-control/
    codex_sonos.py
    requirements.txt
    AGENTS_SNIPPET.md
```

You can also run it directly from this package folder without installing it into another workspace.

## Requirements

- Python 3.10 or newer
- A Sonos system reachable from the same local network
- Local network access to Sonos speakers
- Python package: `soco`

## Quick Start

From this package folder:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python core/codex_sonos.py discover --json
```

Then target a room by name:

```bash
.venv/bin/python core/codex_sonos.py status --name "Kitchen" --json
.venv/bin/python core/codex_sonos.py pause --name "Kitchen" --json
.venv/bin/python core/codex_sonos.py volume --name "Kitchen" set 15 --json
.venv/bin/python core/codex_sonos.py group --name "Kitchen" status --json
.venv/bin/python core/codex_sonos.py favorites --name "Kitchen" list --json
```

If discovery is flaky, target a known speaker IP:

```bash
.venv/bin/python core/codex_sonos.py status --ip 192.168.1.50 --json
```

## Agent Usage Pattern

Add the contents of [AGENTS_SNIPPET.md](AGENTS_SNIPPET.md) to your project-level `AGENTS.md` or `CLAUDE.md`.

The snippet teaches an agent how to translate natural-language requests such as "play music in the kitchen," "turn down the office," or "what's playing in the living room?" into concrete Sonos commands.

For safety, ask the agent to default to passive checks:

- `discover`
- `status`
- `volume get`
- `group status`

Only let it change playback, volume, favorites, queues, or grouping when you explicitly ask.

## Notes

- The CLI first tries Sonos discovery and then retries with SoCo's local network scan if multicast discovery returns no speakers.
- Transport commands are sent to the group coordinator because grouped Sonos rooms may reject playback commands when called on a satellite.
- `--json` is recommended for agent calls.
- This package intentionally does not store credentials or call external music-service APIs.

## Verify This Package

```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
python3 scripts/verify_public_package.py
```
