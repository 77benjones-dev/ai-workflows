# AI Workflows

Reusable AI workflow materials I have developed for product management and software development.

This repository is a public portfolio and reference library. It collects skills, prompts, examples, and working patterns I use to make AI-assisted work more structured, repeatable, and reviewable.

Everything here is sanitized for public sharing and intended to be useful without exposing private company, client, or machine-specific context.

## Why This Exists

Most AI workflow advice is a pile of prompt snippets. This repo is my working set: reusable instructions, skills, examples, and prompt patterns that turn repeated work into something easier to run, improve, and share.

This is not currently organized around public contributions. It is primarily a curated collection of my own AI workflow experiments, patterns, and reusable materials.

## What's Here

### Tools

- `tools/activity-log/` - Adds a cross-session markdown journal, narrative milestone template, and workspace hooks for Claude Code and Codex.
- `tools/sonos-control/` - Adds local-network Sonos discovery and control commands for terminal-based AI agents without OpenClaw or cloud APIs.

### Skills

- `skills/analyzing-youtube-videos/` - Retrieves timestamped YouTube captions and turns videos into evidence-aware learning reports.
- `skills/cc-capability-advisor/` - Recommends the right Claude Code delivery mechanism for a task or recurring need, such as a prompt, skill, agent, hook, cron, MCP, plugin, or existing tool.
- `skills/codex-capability-advisor/` - Recommends the simplest Codex app, workspace, automation, skill, plugin, MCP, or API mechanism for a recurring need.
- `skills/new-project/` - Scaffolds lightweight project context files for new or existing initiatives.
- `skills/public-workflow-prep/` - Sanitizes skills, prompts, agent instructions, and workflow packages for public sharing in this repo.

### Product Manager Workflows

- `product-manager-skills/` - Groups product-management skills, examples, and references, including Jira issue creation and one-pager/story workflows.

### Prompts

- `prompts/prompt-compendium.md` - A practical reference of prompting techniques, frameworks, and examples for better AI outputs.
- `prompts/prompt-architect/` - Turns a vague request into a copy-paste-ready prompt with role, inputs, constraints, output structure, variants, and stress tests.

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

## License

MIT. See `LICENSE`.
