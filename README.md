# AI Workflows

Reusable AI workflow materials I have developed for product management and software development.

This repository is a public portfolio and reference library. It collects skills, prompts, examples, and working patterns I use to make AI-assisted work more structured, repeatable, and reviewable.

Everything here is sanitized for public sharing and intended to be useful without exposing private company, client, or machine-specific context.

## Why This Exists

Most AI workflow advice is a pile of prompt snippets. This repo is my working set: reusable instructions, skills, examples, and prompt patterns that turn repeated work into something easier to run, improve, and share.

This is not currently organized around public contributions. It is primarily a curated collection of my own AI workflow experiments, patterns, and reusable materials.

## What's Here

### Skills

- `skills/capability-advisor/` - Recommends the right delivery mechanism for a task or recurring need, such as a prompt, skill, agent, hook, cron, MCP, plugin, or existing tool.

### Prompts

- `prompts/prompt-architect/` - Turns a vague request into a copy-paste-ready prompt with role, inputs, constraints, output structure, variants, and stress tests.
- `prompts/prompt-tips.md` - A compact reference of prompting patterns with examples and product-management use cases.

### Examples

- `examples/CLAUDE.md` - A reference global Claude Code instruction file showing communication style, workflow preferences, and reusable operating rules.

## Usage

Copy the files you want into the location your tool expects, or symlink them from this repository.

For skills, each skill should use this shape:

```text
skills/example-skill/
  SKILL.md
  scripts/
  references/
```

## What Good Looks Like

The `capability-advisor` skill is a good example of the pattern this repo is aiming for. It does not just answer a question; it helps choose the right shape for future work. A one-off task might stay a prompt, a repeated workflow might become a skill, and a scheduled check might become an automation.

That matters because the mechanism is often the real design decision. The goal is not to turn every useful prompt into infrastructure. The goal is to make repeated AI work easier to run, easier to review, and easier to improve over time.

## Public Sharing Notes

Before publishing changes, check for:

- API keys, tokens, or credentials.
- Private repository names or internal URLs.
- Client, customer, or employer-specific details.
- Personal filesystem paths.
- Generated caches, logs, and local tool state.

## License

MIT. See `LICENSE`.
