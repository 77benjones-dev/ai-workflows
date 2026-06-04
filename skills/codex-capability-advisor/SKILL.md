---
name: codex-capability-advisor
description: Use when deciding whether a recurring need belongs in a Codex skill, AGENTS.md rule, app automation, thread heartbeat, plugin, connector, MCP server, subagent, background thread, worktree, saved prompt, API workflow, or an existing tool.
---

# Codex Capability Advisor

Recommend the smallest useful delivery mechanism for a task or recurring need. Return a decision with rationale and a concrete handoff. Do not build the artifact unless the user asks.

Assume the user works primarily in the Codex desktop app with its current default frontier model. As of May 2026, OpenAI documents GPT-5.5 as the flagship model for complex reasoning and coding. Verify the current default before making model-specific recommendations.

## Core principles

1. Match the trigger first. Manual work, session follow-up, recurring schedule, external event, and universal doctrine need different mechanisms.
2. Prefer composition over a single oversized artifact. Common answers are automation + skill, plugin + skill, or AGENTS.md + skill.
3. Keep one-offs as prompts. Graduate repeated work into an artifact only after the repetition is clear.
4. Use existing tools before building integrations. Search available skills, plugins, connectors, and MCP tools before recommending custom code.
5. Keep app features and API features separate. A Codex desktop automation is not a production webhook service.

## Triage tree

Walk top-to-bottom. Use the first strong match as the primary mechanism, then add companions.

```text
Can a tool the user already has solve this with little setup?
  YES -> Use that tool. Stop.
  NO  -> Continue.

Is this a one-off with low stakes and no likely repeat?
  YES -> Prompt it directly. Do not create an artifact.
  NO  -> Continue.

Should the rule guide every task in a folder or repository?
  YES -> AGENTS.md doctrine.
  NO  -> Continue.

What triggers the work?
  Manual, when the user asks
    -> Skill for a reusable workflow.
    -> Saved prompt for stable text used across tools.

  Repeated follow-up inside the current conversation
    -> Thread automation (heartbeat), optionally invoking a skill.

  Independent recurring schedule
    -> Standalone app automation, usually invoking a skill.

  Separate task that can run in parallel
    -> Background Codex thread. Use a worktree if it may edit code.

  Event in a Codex session
    -> Hook or rule, only when the event truly needs automatic action.

  External event, webhook, or production workload
    -> Existing automation platform, OpenAI API, Codex SDK, or another deployed service.
```

After choosing the trigger, check:

- Does the work need repo isolation? Add a worktree.
- Does it need durable reference material? Add a reference file.
- Does it need external data or actions? Search plugins, connectors, and MCP tools.
- Does it need multiple reusable capabilities packaged together? Consider a plugin.
- Does it need context isolation or parallel exploration? Consider subagents.

## Common compositions

| Need | Primary | Companions |
| --- | --- | --- |
| Reusable manual workflow | Skill | Reference files |
| Weekly project sweep | Standalone app automation | Skill, worktree |
| Poll until a deploy or PR changes | Thread automation | Skill, GitHub plugin |
| Parallel coding task | Background thread | Worktree, local environment |
| Universal repo rule | AGENTS.md | Skill for the detailed procedure |
| External-system workflow | Existing plugin or connector | Skill for orchestration |
| Several reusable skills plus integration setup | Plugin | Skills, app mapping, MCP config |
| Production or webhook-driven agent | OpenAI API or Codex SDK | Deployed service, evals |

## Capability reference

### Prompt directly

Pick when the need is one-off, low effort, and unlikely to repeat. Avoid saving infrastructure before a pattern exists.

### Saved prompt

Pick when the wording is reusable across Codex, ChatGPT, Claude Code, or another tool, but no runtime logic is needed.

Store versioned prompts in a workspace folder such as `prompts/`. Graduate to a skill when the workflow needs steps, branches, bundled references, or tool-aware instructions.

### Skill

Pick when Codex should keep a reusable workflow on hand for repeated work.

A skill is a folder with `SKILL.md` and optional `scripts/`, `references/`, `assets/`, and `agents/openai.yaml`. The YAML description controls discovery. Put repo-scoped skills in `.agents/skills/` and personal reusable skills in `$HOME/.agents/skills/`. Codex follows symlinked skill folders.

Prefer a skill over a long AGENTS.md section when the procedure applies only to certain tasks.

### Reference file

Pick when a workflow needs stable content such as a voice guide, rubric, schema, taxonomy, or examples. Pair it with a skill or AGENTS.md rule. Keep long or frequently edited context out of the skill body.

### AGENTS.md doctrine

Pick when an instruction should guide every Codex task in a folder tree. Use it for repo layout, verification expectations, coding conventions, and durable working rules.

Prefer a skill when the content is optional, lengthy, or task-specific. Prefer a hook when an action must fire automatically.

### Rules and permissions

Pick when Codex needs predictable command approval behavior or sandbox boundaries. Adjust configuration narrowly. Do not weaken permissions globally to avoid a small amount of friction.

### Hook

Pick when an action must fire on a Codex lifecycle or tool event. Use hooks sparingly. A hook is stronger than guidance because it runs automatically.

Do not use a hook for a wall-clock schedule. Use an app automation.

### Standalone app automation

Pick when Codex should run independent background tasks on a schedule and report findings to the app inbox. Use a worktree when the automation may edit a Git repository and should stay isolated from unfinished local work.

Pair complex automations with a skill. Invoke the skill explicitly in the automation prompt with `$skill-name`.

### Thread automation

Pick when Codex should return to the same conversation on a cadence. Thread automations preserve context and work well for deploy checks, PR polling, active research loops, and reminders to continue a review.

Prefer a standalone automation when each run should start fresh.

### Background thread

Pick when a task can proceed independently while the user or another thread works on something else. Use project threads for repo-scoped work. Use worktrees for speculative or parallel edits.

Prefer inline work when the result blocks the next step or the task is quick.

### Worktree

Pick when a coding task, background thread, or automation should not touch the current checkout. Worktrees are useful for parallel work, speculative changes, and review before integration.

Prefer the local checkout for small edits the user expects immediately.

### Local environment

Pick when a worktree or automation needs setup beyond the checked-in repo, such as dependency installation or environment bootstrapping. Keep setup scripts explicit and reviewable.

### Subagent

Pick when a bounded chunk of work benefits from context isolation or parallel execution. Good examples: broad repo exploration, independent reviews, and disjoint implementation tasks.

Do not use a subagent for quick synchronous work. Respect the runtime's delegation rules before spawning one.

### Goal

Pick when the user wants Codex to pursue a durable objective across extended work. Use goals for outcome tracking, not as a replacement for a task plan or recurring automation.

### Plugin

Pick when distributing reusable capabilities beyond one repo, bundling two or more related skills, or shipping skills with app integrations. Plugins can include skills and optional app mappings, MCP configuration, and presentation assets.

Prefer direct skill folders for local authoring and repo-scoped workflows.

### Existing plugin or connector

Pick when Codex already has access to the external system. Discover available tools first. Skills orchestrate work. Plugins and connectors provide access.

Do not build a custom MCP server until existing capabilities have been checked.

### MCP server

Pick when a frequently used external system needs typed, structured tools and no suitable plugin or connector exists. Build an MCP server only when multiple workflows will reuse it.

For occasional access, use an existing CLI, API script, or pasted export.

### Browser tooling

Pick the in-app browser for local web targets and app-side verification. Pick Chrome or computer-use tooling when the task requires interacting with a real browser session or desktop UI.

Use browser tooling for verification, not as a substitute for simpler file or API access.

### CLI, non-interactive mode, Codex SDK, or GitHub Action

Pick these when work must run outside the desktop app, integrate into scripts, or execute in CI. Use the Codex SDK for programmatic agent workflows. Use a GitHub Action for repository events handled in CI.

### OpenAI API or Agents SDK

Pick when the user is building a product feature, deployed agent, webhook-driven workflow, or batch system outside Codex. This is an application architecture decision, not a Codex workspace customization.

### Use an existing non-AI tool

Pick when email rules, calendar rules, Shortcuts, Zapier, Make, a spreadsheet formula, or the source system already solves the need. Say this clearly when it is the simplest path.

## Anti-patterns

Call these out when present:

- Building a skill for a one-off task -> prompt directly.
- Putting a task-specific procedure in AGENTS.md -> skill.
- Using AGENTS.md for event-triggered behavior -> hook.
- Using a hook for a recurring schedule -> app automation.
- Using a standalone automation when the current thread context matters -> thread automation.
- Running code-editing automation in the local checkout without considering isolation -> worktree.
- Building an MCP server before searching plugins and connectors -> discover existing access first.
- Packaging one small local skill as a plugin -> keep the direct skill folder.
- Using a background thread for work that blocks the next step -> do it inline.
- Assuming the current flagship model without checking when the recommendation is model-specific -> verify current docs or available model list.

## Output template

```text
**Goal**
[Restate the outcome in one sentence.]

**Best fit: [Primary mechanism]** with [companions]
- Why: [Tie the recommendation to the trigger and one other decision dimension.]
- Do this: [Give the concrete path, app action, or handoff.]

**Runner-up: [Alternative]**
- Pick this instead if: [Name the condition that flips the decision.]

**Why not [obvious alternative]**
[Name the anti-pattern briefly.]

**One question** (only when needed)
[Ask the single question that could change the recommendation.]
```

Skip runner-up and why-not sections when they add no value.

## Handoffs

- Build or update a skill -> use `skill-creator`.
- Find an existing skill -> use `find-skills`.
- Create or update an app automation -> use the Codex app automation tool.
- Create a background project thread -> use the Codex app thread tool.
- Add repo doctrine -> edit `AGENTS.md`.
- Add a plugin -> use `plugin-creator`.
- Use an external plugin or connector -> discover installed tools first.
- Build an OpenAI API workflow -> use current official OpenAI docs.

## Quality checklist

- Lead with one recommendation.
- Name the composition explicitly.
- Tie the recommendation to its trigger.
- Prefer the smallest useful mechanism.
- Search existing capabilities before proposing an integration.
- Keep Codex app, CLI, and API paths distinct.
- Add one concrete next action.

## Official references

- Codex app: https://developers.openai.com/codex/app
- App automations: https://developers.openai.com/codex/app/automations
- Skills: https://developers.openai.com/codex/skills
- Plugins: https://developers.openai.com/codex/plugins
- AGENTS.md: https://developers.openai.com/codex/guides/agents-md
- Subagents: https://developers.openai.com/codex/subagents
- Models: https://developers.openai.com/api/docs/models
