# Sonos Control Setup

Use this workflow to add local Sonos control to an AI-agent workspace.

## Preview Install

1. Choose a target workspace:

   ```bash
   export WORKSPACE="/path/to/workspace"
   ```

2. Create a tool folder:

   ```bash
   mkdir -p "$WORKSPACE/tools/sonos-control"
   ```

3. Copy the package files:

   ```bash
   cp core/codex_sonos.py "$WORKSPACE/tools/sonos-control/codex_sonos.py"
   cp requirements.txt "$WORKSPACE/tools/sonos-control/requirements.txt"
   cp AGENTS_SNIPPET.md "$WORKSPACE/tools/sonos-control/AGENTS_SNIPPET.md"
   ```

4. Install dependencies:

   ```bash
   cd "$WORKSPACE/tools/sonos-control"
   python3 -m venv .venv
   .venv/bin/pip install -r requirements.txt
   ```

5. Test passive discovery:

   ```bash
   .venv/bin/python codex_sonos.py discover --json
   ```

6. Add the relevant lines from `AGENTS_SNIPPET.md` to the workspace's agent instructions.

## First Safe Agent Request

Ask the agent:

```text
Run a passive Sonos discovery and tell me which rooms are visible. Do not change playback, grouping, or volume.
```

Once discovery works, try:

```text
What is playing in [room name]?
```

Then:

```text
Pause [room name].
```

## Troubleshooting

- If `discover` returns no rooms, try `discover --scan --json`.
- If discovery still fails, find a speaker IP from your router or Sonos app and use `--ip`.
- Make sure the agent machine is on the same local network/VLAN as the Sonos speakers.
- VPNs, guest Wi-Fi, and router multicast filtering can prevent discovery.
