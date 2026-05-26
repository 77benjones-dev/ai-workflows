# AGENTS.md

## Repository Purpose

This repo stores reusable agent instructions, Codex skills, Claude guidance, examples, scripts, and prompt templates for software development workflows.

Keep it public-friendly. Assume anything committed here may be shared.

## Important Paths

- `claude/` Claude project guidance and reusable instructions
- `codex/skills/` Codex skills, each with its own `SKILL.md`
- `prompts/` reusable prompt templates
- `examples/` small usage examples
- `scripts/` optional helper scripts

## Working Style

- Prefer clear, reusable guidance over machine-specific instructions.
- Keep examples small and easy to copy.
- Avoid client names, private repository names, internal URLs, credentials, and personal paths.
- Do not add generated caches, logs, or local tool state.
- Keep tool-specific guidance in the matching tool folder when possible.

## Verification

This repo usually does not require a build.

Before finishing:

- scan changed text for secrets or private details
- check Markdown readability
- verify any referenced paths match the repo layout
- run script-specific checks only when scripts are changed

## Publishing Checklist

Before publishing changes, check for:

- API keys, tokens, or credentials
- private repository names or internal URLs
- client, customer, or employer-specific details
- personal filesystem paths
- generated caches, logs, and local tool state
