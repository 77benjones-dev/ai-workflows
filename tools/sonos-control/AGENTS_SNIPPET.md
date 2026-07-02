# Sonos Control

This workspace has a local Sonos control tool at `tools/sonos-control/codex_sonos.py`.

## Commands

- Discover rooms: `tools/sonos-control/.venv/bin/python tools/sonos-control/codex_sonos.py discover --json`
- Check status: `tools/sonos-control/.venv/bin/python tools/sonos-control/codex_sonos.py status --name "[room name]" --json`
- Get volume: `tools/sonos-control/.venv/bin/python tools/sonos-control/codex_sonos.py volume --name "[room name]" get --json`
- Set volume: `tools/sonos-control/.venv/bin/python tools/sonos-control/codex_sonos.py volume --name "[room name]" set 15 --json`
- Playback: `tools/sonos-control/.venv/bin/python tools/sonos-control/codex_sonos.py play|pause|stop --name "[room name]" --json`

## Natural Language Requests

Music requests usually mean use this Sonos tool. Do not ask the user for the exact command when intent and room are clear.

Intent mapping:

- "play music in [room]", "turn on music in [room]", "resume music in [room]" -> run `tools/sonos-control/.venv/bin/python tools/sonos-control/codex_sonos.py play --name "[room]" --json`
- "pause music in [room]", "stop the music in [room]" -> run `tools/sonos-control/.venv/bin/python tools/sonos-control/codex_sonos.py pause --name "[room]" --json`; use `stop` only when the user explicitly says "stop" and pause is not what they mean
- "what's playing in [room]", "status of [room]" -> run `tools/sonos-control/.venv/bin/python tools/sonos-control/codex_sonos.py status --name "[room]" --json`
- "turn down [room]", "lower the volume in [room]" -> run `tools/sonos-control/.venv/bin/python tools/sonos-control/codex_sonos.py volume --name "[room]" down 2 --json`
- "turn up [room]", "raise the volume in [room]" -> run `tools/sonos-control/.venv/bin/python tools/sonos-control/codex_sonos.py volume --name "[room]" up 2 --json`
- "set [room] to [number]" or "volume [number] in [room]" -> run `tools/sonos-control/.venv/bin/python tools/sonos-control/codex_sonos.py volume --name "[room]" set [number] --json`
- "mute [room]" / "unmute [room]" -> run `tools/sonos-control/.venv/bin/python tools/sonos-control/codex_sonos.py volume --name "[room]" mute|unmute --json`

Discover room names with `discover --json`. Match room names case-insensitively. If the room is missing or ambiguous, run discovery before asking the user.

## Safety

- Prefer passive commands (`discover`, `status`, `volume get`, `group status`) unless the user explicitly asks to change playback, grouping, favorites, or volume.
- Check status after changing playback or volume.
- When changing volume without a requested target level, use small increments such as 2.
- If discovery fails, retry with `--scan`; if it still fails, ask for a known speaker IP and use `--ip`.
- If the user asks to play a specific song, artist, playlist, or favorite and the current queue/favorite is unclear, list favorites or ask for the exact source instead of guessing.
