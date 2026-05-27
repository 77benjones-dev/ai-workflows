# AI Workflows

Skills, instructions, agents, and other resources for agentic PM and development workflows.

This repository is intentionally public-friendly. It keeps reusable skills, prompts, examples, and helper scripts separated from machine-specific configuration.

## Contents

- `skills/` - Agent skills, each in its own folder with a `SKILL.md`.
- `prompts/` - Prompt templates that are not tied to a specific tool.
- `examples/` - Small examples showing how these workflows are meant to be used.
- `scripts/` - Optional helper scripts.

## Usage

Copy the files you want into the location your tool expects, or symlink them from this repository.

For skills, each skill should use this shape:

```text
skills/example-skill/
  SKILL.md
  scripts/
  references/
```

## Public Sharing Notes

Before publishing changes, check for:

- API keys, tokens, or credentials.
- Private repository names or internal URLs.
- Client, customer, or employer-specific details.
- Personal filesystem paths.
- Generated caches, logs, and local tool state.

## License

MIT. See `LICENSE`.
