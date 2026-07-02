---
name: new-project
description: Scaffold a lightweight project workspace for product or delivery work. Use when starting a new initiative, backfilling context for an existing folder, or adding agent-readable project files before deeper one-pager, story, or ticket work begins.
---

# New Project Scaffolder

Create or backfill a small project workspace that helps humans and AI assistants resume work without rediscovering context. This skill is for product, research, content, or delivery initiatives. For software repositories, prefer the repo's own setup conventions.

## When To Use

Use when the user asks to:

- Create a new project or initiative folder.
- Scaffold a project workspace.
- Add project context files to an existing folder.
- Backfill agent-readable context for existing work.
- Start a product discovery, planning, or delivery stream.

Do not use for:

- One-off notes that do not need a project folder.
- Code repositories with their own README, AGENTS.md, or contribution guide.
- Ticket creation. Use a ticketing workflow after the project context exists.

## Defaults

If the user has a known workspace root, use it. Otherwise ask for the target parent folder.

Default project shape:

```text
projects/
  <Project Name>/
    PROJECT.md
    AGENTS.md
    ACTIVITY_LOG.md
    inputs/
    artifacts/
```

Use the project name as given unless the user asks for a slug. Human-readable folder names are fine.

## What This Skill Does

1. Detect whether the project folder already exists.
2. If it exists, inspect the folder before writing anything.
3. Read the two or three most informative files, such as one-pagers, briefs, PRDs, research notes, or recent markdown files.
4. Confirm only the missing details that materially affect scaffolding.
5. Create missing context files without overwriting existing files.
6. Optionally run shallow discovery across approved sources and add high-confidence links.
7. Report created files, skipped files, and the next useful step.

## Required Inputs

Infer what you can. Ask one concise question when required.

Minimum details:

- Project name.
- Target parent folder.
- Stream, initiative, or category, if relevant.
- Primary owner or decision maker, if known.
- Whether to run optional discovery.

If the user does not know the owner, stream, or status, write `TBD`.

## Existing Project Branch

When the folder already exists:

1. List the folder, including one level of subfolders.
2. Read the most informative files.
3. Identify current status, likely owner, useful source files, and unresolved asks.
4. Draft `PROJECT.md` in chat first if it would summarize existing work.
5. Write only after user approval when the folder contains substantive prior work.

Never overwrite existing context files. If a file exists, read it and leave it in place unless the user explicitly asks for an update.

## Optional Discovery

Ask before using external or private systems. The default is no external discovery.

Possible discovery sources:

- Local workspace search.
- Shared documents.
- Ticketing system.
- Team chat or decision logs.
- Email.
- Dashboards or research repositories.

Before using any source:

- Check access.
- Skip unavailable sources.
- Record skipped sources as unknown, not empty.

Add only high-confidence, useful links to `PROJECT.md`. Omit sources with no useful findings instead of writing "none found."

## Files To Create

### PROJECT.md

Create when missing. Keep it lean and useful.

```markdown
# <Project Name> - Project Context

## What this project is

<Two to four sentences explaining the problem, audience, and why now.>

**Stream:** <stream, initiative, or category>
**Status:** <Kickoff | Exploring | Shaping | In progress | Paused | Complete>
**Owner:** <name, role, or TBD>

## Open asks

- [ ] <Decision, missing source, or next question>

## Read these first

1. `<file>` - <why it matters>
2. `ACTIVITY_LOG.md` - chronology and decisions
3. `inputs/` - source material

## Related links

- [Title](https://example.com) - <why it matters>

## Watch-outs

- <Scope boundary, dependency, known gap, or adjacent project>
```

Omit sections that would contain only placeholders.

### AGENTS.md

Create when missing:

```markdown
# Agent Context

See [PROJECT.md](./PROJECT.md) for project context, reading order, open asks, and watch-outs.
```

### ACTIVITY_LOG.md

Create when missing:

```markdown
---
last modified: YYYY-MM-DD
---

# <Project Name> - Activity Log

**Stream:** <stream or TBD>
**Status:** Kickoff

## Sessions

### YYYY-MM-DD - Project created
- Folder scaffolded.
- Next: <concrete next step or TBD>
```

### inputs/

Create when no equivalent source-material folder exists. Treat folders such as `source/`, `research/`, `notes/`, or `knowledge/` as equivalent if the project already uses them.

### artifacts/

Create when missing. Use for generated deliverables worth keeping.

## Guardrails

- Do not create blank context files that another automation will overwrite.
- Do not create README files unless the user asks.
- Do not invent owners, status, metrics, commitments, or links.
- Do not add private URLs, secrets, or personal paths to public templates.
- Keep scaffolding small. Add only files that help the next session resume.
- Mention adjacent issues separately instead of expanding the project scope.

## Completion Report

Return:

- Project folder path.
- Files created.
- Files skipped because they already existed.
- Discovery sources used or skipped.
- Suggested next step, such as drafting a one-pager, generating stories, or answering open asks.
