---
name: capability-advisor
description: Recommend the right Claude Code delivery mechanism (or combination) for a task or recurring need. Covers every CC capability — saved prompt, slash command, skill, knowledge file, subagent, specialized agent, hook, cron, scheduled wakeup, background task, plan mode, in-session task list, MCP (use or build), plugin, output style, status line, keybinding, model override, permissions, CLAUDE.md doctrine, memory, worktree, @-file reference — plus off-CC paths (custom GPT/Gem, Anthropic API, Agent SDK, Zapier, "use a tool you already pay for"). Use when the user asks "should this be a skill?", "skill vs prompt vs agent vs hook vs cron", "how should I run this", "should this run on a schedule", "is there already something for this", or invokes /capability-advisor. Output: best-fit + composition (usually multiple capabilities work together), runner-up, why-not on the obvious wrong answer, concrete handoff.
---

# /capability-advisor — Delivery Mechanism Advisor

Take a task, problem, or recurring need and recommend the right delivery mechanism (or combination of mechanisms). The deliverable is a **decision** with rationale, not the thing itself. Building the thing is downstream and usually handed off to another skill.

## When to use

- "Should this be a skill or just a saved prompt?"
- "What's the best way to build [X]?"
- "Skill vs. agent vs. hook vs. cron — which fits here?"
- "Should this run on a schedule?"
- "Is there already something that does this, or should I build something?"
- User has a recurring need and isn't sure how to solidify it
- User has a one-off and isn't sure if it's worth building anything at all
- Invoked as `/capability-advisor`

**Do not use** when the user already knows what they want to build and just wants to build it. Route them directly to the relevant scaffolding skill (`new-project`, `prompt-architect`, `update-config`, etc.).

## Core principles

1. **The answer is usually a combination.** Skill + Knowledge files. Skill + Cron. Hook + Slash command. Subagent + Worktree. Treat the matrix as ingredients, not menu items. Lead with the *primary* capability, then list the companions.

2. **Match the trigger first, the workflow second.** Trigger type collapses the option space fastest. Manual = skill or slash command. Event = hook. Scheduled-recurring = cron. Scheduled-once = wakeup. Once you know the trigger, the workflow shape is the secondary question.

3. **Simpler beats fancier.** A saved prompt beats a skill if it does the job. A skill beats a custom MCP if pasted data works. A slash command beats a skill if there's no logic. Build complexity only when the simpler option fails.

4. **Don't build what you already pay for.** Airtable formulas, Salesforce flows, Notion AI, Zapier, email rules. Most under-recommended option. Recommend it loudly when it fits.

## Triage tree (run this first)

Walk top-to-bottom. The first match is your primary capability. Then check the **Composition** section to see what to pair it with.

```
Is the user already paying for a tool that does this (Airtable, Zapier, Salesforce, email rules)?
  YES → "Don't build it" + name the tool. Stop.
  NO ↓

Does the user already know which mechanism they want?
  YES → route them to the scaffolding skill. Don't re-litigate.
  NO ↓

What's the trigger?
  ┌─ Manual ("when I ask")
  │   ├─ Runs in Claude Code?
  │   │    YES → Skill (workflow logic) or Slash command (flat prompt)
  │   │    NO  → Saved prompt template, Custom GPT, or Anthropic API
  │   └─ Just one-off, won't repeat?
  │        YES → Just-prompt-it (no artifact)
  │
  ├─ Event-based ("when X happens in my session")
  │   → Hook (PreToolUse / PostToolUse / Stop / SessionStart / etc.)
  │
  ├─ Scheduled-recurring ("every Monday at 8am", "every 5 minutes")
  │   → Cron + (Skill OR Slash command for the body)
  │
  ├─ Scheduled-once ("at 3pm today", "in 2 hours")
  │   → Scheduled Wakeup
  │
  └─ Driven by external system (incoming webhook, customer action)
      → Off-CC: Anthropic API call, Agent SDK service, or Zapier/Make
```

After the trigger, ask:
- **Where does output land?** Chat reply, file write, external system update, action taken (PR, Slack post, Jira create)?
- **Is the work delegated?** If a chunk of work is heavy enough to warrant context isolation, pair the primary with a Subagent or Specialized agent.
- **Is there durable content the workflow leans on?** Style guides, taxonomies, examples → Knowledge file pair.

## Composition patterns (the real answers)

Solo capabilities are rare. These combos cover ~80% of recommendations:

| Pattern | Primary | Companions | Example |
|---|---|---|---|
| Recurring automation | Cron | Skill, Knowledge files | Slack sweep every weekday 8am |
| Reusable workflow | Skill | Knowledge files, Subagent | `pr-description-writer` + PR template knowledge file |
| Heavy research delegation | Skill | Specialized agent, Background task | A prep skill spawning multiple researcher agents in parallel |
| Auto-behavior | Hook | Slash command body, Skill | "After every Stop, run drift-check" |
| Speculative code change | Subagent | Worktree isolation | Refactor proposal in isolated branch |
| Doctrine-driven workflow | Skill | CLAUDE.md rule | "Always read context first" |
| One-shot reminder | Scheduled Wakeup | Memory entry (so context survives) | "Check the deploy at 3pm" |
| Cross-tool reuse | Saved prompt | Custom GPT, Gem | Vendor scorecard rubric |

When you make a recommendation, **state the primary mechanism first, then name the companions inline.** Don't make the user go shopping.

## Decision dimensions

Use these to disambiguate when triage is ambiguous. Ask the user only the 1-2 that materially change the recommendation:

1. **Trigger** — manual / event-in-session / scheduled-recurring / scheduled-once / external-webhook
2. **Frequency** — one-off / occasional (monthly+) / recurring (weekly+) / high-volume (daily+)
3. **Where it runs** — Claude Code / chat tool (ChatGPT, Claude.ai, Gemini) / Anthropic API / external automation tool
4. **Audience** — just me / my team / the public
5. **Inputs** — pasted text / file in repo / external fetch (web, MCP) / structured form
6. **Output destination** — chat reply / file written / external system mutated / action taken
7. **Complexity** — single prompt / multi-step deterministic / multi-step agentic with judgment
8. **State** — stateless / project context only / cross-session memory needed / cross-session continuity needed
9. **Sensitivity** — public / internal / contains PII or secrets

**Never interrogate the user with all 9.** Identify the 2-3 that flip the answer and ask one consolidated question if needed. Default to assumptions otherwise.

## Capability reference

Organized by role. Most recommendations combine one capability from **Trigger** with one from **Workflow**, plus optional **Content** and **Config** companions.

### Triggers (when does the work fire?)

#### Manual invocation (default)
The user types a message, types a slash command, or says a phrase a skill description matches. No artifact required for "manual" itself, but the *thing being triggered* is usually a skill or slash command.

#### Hook (event-based, in-session)
**Pick when:** "every time X happens in a Claude Code session" — file edit, tool call, prompt submit, session start/stop, agent stop, pre-compact, notification.
**Events available:** PreToolUse, PostToolUse, UserPromptSubmit, Stop, SubagentStop, SessionStart, SessionEnd, PreCompact, Notification.
**Location:** `.claude/settings.json` (project), `~/.claude/settings.json` (user).
**Handoff:** `update-config`.
**Trap:** "from now on, do X" is *always* a hook, never memory or a skill. Memory can't fire. Skills don't auto-trigger without phrasing.
**Not for:** wall-clock time. Use Cron.

#### Cron (recurring schedule)
**Pick when:** wall-clock recurrence — "every weekday at 8am", "every Monday morning", "first of each month", "every 5 minutes".
**Tool:** `CronCreate` (also `CronList`, `CronDelete`).
**Pairs with:** a Skill or Slash command holding the actual workflow logic. Cron's job is just "fire X at this time."
**Pick over `loop` skill when:** you want fires that survive across sessions, not in-session polling.
**DST/timezone:** specify timezone explicitly when creating the cron. If you can't, write the cron in UTC and accept that "8am local" drifts an hour twice a year.
**Common pattern:** Cron + Skill is the standard combo for recurring automation.

#### Scheduled Wakeup (one-shot future trigger)
**Pick when:** one fire, then done. "Remind me in 2 hours", "check the deploy at 3pm", "follow up tomorrow morning."
**Tool:** `ScheduleWakeup`.
**Pick over Cron when:** it's a one-time fire.
**Pick over `loop` skill when:** you know the time, not "until something changes."

#### `loop` skill (in-session polling)
**Pick when:** you want recurring action *within the current session*, not surviving across sessions. "Check the build every 5 minutes until it's green."
**Pick over Cron when:** you only care while you're working right now.

#### External trigger (webhook, customer action, system event)
**Pick when:** the trigger originates outside Claude Code — Salesforce event, customer email, GitHub webhook, scheduled job in another system.
**Mechanism:** Anthropic API or Agent SDK called by the external system. Not Claude Code.
**Pair with:** a small classifier prompt or workflow defined in code, deployed wherever the trigger lives.

### Workflow (what does the work look like?)

#### Just-prompt-it (no artifact)
**Pick when:** one-off, low effort, low stakes, won't repeat in 30 days.
**Skip when:** you've prompted variations 3+ times. That's a skill or saved prompt waiting to happen.

#### Saved prompt template
**Pick when:** runs 3-10 times, stable prompt with variable inputs, used in chat tools (ChatGPT, Claude.ai, Gemini), or you want versioned reference.
**Location:** `<workspace>/prompts/<name>-v<N>.md` (or wherever you keep saved prompts).
**Handoff:** `prompt-architect`.

#### Slash command (markdown only)
**Pick when:** runs in Claude Code, single-purpose, body is mostly the prompt itself, no decision logic or branching.
**Location:** `.claude/commands/<name>.md`. Can have frontmatter (description, allowed-tools).
**Pick over Skill when:** no auto-trigger needed, no knowledge files, no multi-step logic.
**Trap:** if the command branches on input, reads context, or hands off, it's a skill.

#### Skill
**Pick when:** runs in Claude Code, has a description that should auto-trigger on phrasing, has workflow logic (steps, modes, branching), references knowledge files, or wraps a recurring decision pattern.
**Location:** `.claude/skills/<name>/SKILL.md`. Description field drives auto-routing.
**Pick over Slash command when:** auto-trigger matters, or workflow has branches/stages.
**Pick over Saved prompt when:** runtime is Claude Code AND there's logic, not just text.
**Handoff:** scaffold manually (no `new-skill` skill exists yet, flag as backlog).

#### Subagent (Agent tool, ad-hoc)
**Pick when:** a chunk of work would consume too much context in the main thread (broad codebase search, large file reads, parallel research), is independent enough to delegate, happens occasionally.
**No artifact.** Just call `Agent` with a `subagent_type` (`general-purpose`, `Explore`, etc.) when needed.
**Pick over Specialized agent when:** the task is rare or one-off.

#### Specialized agent type
**Pick when:** a specific kind of subagent gets invoked repeatedly, benefits from a constrained tool set, deserves its own description for routing.
**Location:** `.claude/agents/<name>.md` with frontmatter (description, tools, model).
**Pick over Skill when:** work is delegated and isolated — the parent gets a single message back, not turn-by-turn collaboration.
**Pick over Subagent when:** "I do this kind of delegation often enough to give it a name."

#### Plan mode
**Pick when:** the work is non-trivial implementation and you want explicit review before execution. Code changes that span multiple files, architectural decisions, anything where "let me confirm the approach first" matters.
**Mechanism:** `EnterPlanMode` or invoking the `Plan` agent.
**Pair with:** the actual implementation that follows, often in a Worktree.
**Skip when:** the change is small or fully specified.

#### Background task
**Pick when:** a Bash command or Agent will take long enough that blocking hurts (builds, long tests, multi-minute MCP sweeps, parallel research the main agent doesn't need synchronously).
**Mechanism:** `run_in_background: true` on Bash or Agent calls.
**Skip when:** you need the result before your next step.

#### In-session task list
**Pick when:** a multi-step (3+) workflow benefits from explicit progress tracking, especially if you'll context-switch or be interrupted.
**Tools:** `TaskCreate`, `TaskUpdate`, `TaskList`.
**Not persistent across sessions.** For cross-session work, use ACTIVITY_LOG.md instead.

#### Worktree (isolated agent run)
**Pick when:** an agent will make code changes you want isolated from your current branch — speculative refactors, parallel agent runs that would conflict, experiments you might throw away.
**Mechanism:** `isolation: "worktree"` on Agent calls.
**Skip when:** the agent is read-only or making changes you'd accept directly.

### Content (what does the workflow read?)

#### Knowledge file (companion to skills/agents/CLAUDE.md)
**Pick when:** stable reference content (style guides, taxonomies, schemas, persona definitions, canonical examples) one or more skills should load on demand.
**Not a standalone capability.** Always paired with a Skill, Specialized agent, or CLAUDE.md reference.
**Location options:**
- `<workspace>/knowledge/<topic>/` — workspace-wide, multiple skills
- `<workspace>/context/` — canonical context (org info, systems, writing style)
- `<project>/inputs/` — project-scoped reference
- `.claude/skills/<name>/<file>.md` — skill-private knowledge
**Pick over baking content into skill body when:** content is long, reused across skills, edited frequently, or maintained by a separate process (e.g., auto-refreshed CSVs).
**Companion to:** Skill, Specialized agent, CLAUDE.md.

#### CLAUDE.md / AGENTS.md (durable doctrine)
**Pick when:** a rule should apply to *every* session in a project (or globally), is durable, human-readable.
**Examples:** "always read context files before starting work", "never use em dashes", "use user stories, not BRDs."
**Locations:**
- `~/.claude/CLAUDE.md` (global, every project)
- `<project>/CLAUDE.md` (project-scoped doctrine)
- `<project>/AGENTS.md` (schema and structural rules)
- `~/.claude/CLAUDE.md` is loaded with every session; project files cascade by directory
**Pick over Memory when:** the rule is authored doctrine, not auto-extracted preference.
**Pick over a Hook when:** you want guidance Claude follows by judgment, not an event-triggered action.

#### @-file mention (inline reference)
**Pick when:** a one-time reference to a specific file in a single conversation. The user types `@path/to/file.md` and that file's content gets pulled into context.
**Skip when:** the reference is durable across sessions. Use CLAUDE.md or a knowledge file instead.

#### Memory entry (auto-memory)
**Pick when:** Claude should *remember* something across sessions — preferences, project facts, references, learned feedback. Trigger is "user is talking about [topic]," not "an event happened."
**Trap:** "from now on, do X every time Y happens" is a hook, not memory. Memory is recall, not action.

### Config (how does Claude Code itself behave?)

#### Permissions / settings change
**Pick when:** reducing prompts ("allow these bash commands"), changing default behavior, scoping access.
**Handoff:** `update-config` or `fewer-permission-prompts`.

#### Output style
**Pick when:** consistent response format change (terse, bulleted-only, narrative-only, JSON-first) for a use case or session type.
**Location:** `.claude/output-styles/` or `/output-style` command.
**Skip when:** writing rules already live in CLAUDE.md.

#### Status line
**Pick when:** persistent context visible at the bottom of every response (branch, token usage, project, custom indicator).
**Handoff:** `statusline-setup` agent or manual `.claude/settings.json`.

#### Keybinding
**Pick when:** a frequently-triggered action deserves a keyboard shortcut, or you want a chord binding for a slash command.
**Location:** `~/.claude/keybindings.json`.
**Handoff:** `keybindings-help`.

#### Model override
**Pick when:** specific work needs a different model (Opus for hard reasoning, Haiku for fast/cheap loops, Sonnet as the default mid).
**Where to set:** per-session via `/model`, per-skill via frontmatter, per-agent via frontmatter, per-Agent-call via the `model` parameter.
**Trap:** don't override globally for one task. Set narrowly.

### Integration (how does Claude reach external systems?)

#### MCP server (use existing)
**Pick when:** structured access to an external system and an MCP already exists (Atlassian, Slack, Airtable, Figma, Notion, Linear, Gmail, Google Calendar, Google Drive).
**How to identify:** check the system reminder for `mcp__<server>__<tool>` tool names.
**Pick over a skill that wraps API calls when:** the MCP exists and is wired up. Skills orchestrate, MCPs access.

#### MCP server (build custom)
**Pick when:** structured access to a system you use heavily, no existing MCP, data shape benefits from typed tools.
**Trap:** building an MCP for something you'd run 4 times a year. Hit the API from a skill instead.
**Cost:** real engineering effort. Worth it only when multiple skills will integrate.

#### Anthropic API (direct)
**Pick when:** the work runs outside Claude Code — production app, batch processing, scheduled job in another system, latency-sensitive integration.
**Pair with:** prompt caching (mandatory for repeated calls), the right model for the job, system-prompt overrides.
**Handoff:** `claude-api` skill for build/migrate/optimize.

#### Agent SDK
**Pick when:** building a long-running agent service, multi-turn assistant deployed in production, or an integration that needs autonomous loops outside Claude Code.
**Pick over Anthropic API direct when:** you need agent loop primitives (tool use, planning, memory) without rebuilding them.

#### Plugin (bundle)
**Pick when:** packaging multiple related skills + agents + commands + hooks for distribution (teammates, public).
**Pick over individual skills when:** one install, shared dependencies, namespaced commands. A `team-toolkit:*` plugin bundling related PM or eng workflows is a typical example.
**Cost:** plugin overhead is high. Worth it only for 3+ related artifacts shipped together.

### Off-Claude-Code paths

#### Custom GPT / Gemini Gem
**Pick when:** prompt used in ChatGPT or Gemini regularly by you or non-technical teammates, knowledge files attach cleanly, you want a clickable interface.
**Tradeoff:** can't be version-controlled. Keep a saved markdown copy alongside.

#### Don't build it — use a tool you already pay for
**Pick when:** Airtable formula, Salesforce flow, Notion AI, Zapier, email rules, calendar rules, IDE features can do this without AI.
**Most under-recommended option.** Recommend it loudly when it fits.

## Anti-patterns (call these out when you see them)

When the user's request shows one of these patterns, name it before recommending. They're the most common mistakes:

- **"From now on, every time X" framed as memory or a skill** → Hook. Memory can't fire. Skills don't auto-trigger on events.
- **Slash command with branching logic** → Skill. Slash commands are flat prompts.
- **Skill scoped to one chat tool that isn't Claude Code** → Saved prompt or Custom GPT. Skills only run in CC.
- **Building a custom MCP for low-frequency access** → Skill calling the API directly. MCPs are for systems multiple skills will share.
- **Plugin for 1-2 artifacts** → Just the skills. Plugin overhead only pays back at 3+ related artifacts.
- **Cron for in-session polling** → `loop` skill. Cron is for fires that survive across sessions.
- **Loop skill for cross-session schedule** → Cron. Loop dies when the session ends.
- **Memory entry for project doctrine** → CLAUDE.md. Memory is auto-extracted preference, CLAUDE.md is authored rule.
- **Skill that bakes a 200-line style guide into its body** → Skill + Knowledge file. Separate logic from content.
- **Subagent for synchronous quick work** → Just do it inline. Subagent overhead only pays back at heavy context or true parallelism.
- **Building anything for a one-off** → Just-prompt-it.

## Output template

```
**Goal (restated)**
[One sentence — what the user wants to do.]

**Best fit: [Primary mechanism]** (with [Companion 1], [Companion 2])
- _Why:_ [2-3 sentences anchored in trigger + 1-2 other dimensions.]
- _What to do:_ [Concrete next step. Name handoff skill if one exists. State the composition explicitly — "build the skill at <path>, register the cron with <command>, knowledge file lives at <path>".]

**Runner-up: [Alternative mechanism]**
- _Pick this if:_ [Condition under which the runner-up beats the best fit.]

**Why not [the obvious wrong answer the user probably considered]**
[1-2 sentences. Most useful when the user is overbuilding or underbuilding. Reference the relevant anti-pattern by name.]

**Diagnostic question** (only if needed)
[One question max. Phrased to confirm the recommendation, not interrogate.]
```

Skip the runner-up section when best fit is overwhelming. Skip the why-not when there's no obvious wrong answer.

## Handoffs

The advisor's job ends with the recommendation. Always point at the next step concretely:

- **Build a skill** → no scaffolding skill exists yet. Action: create `.claude/skills/<name>/SKILL.md` with frontmatter (name, description) and body. Mention the gap.
- **Save a prompt** → `prompt-architect`
- **Add a hook / change settings / fix permissions** → `update-config` or `fewer-permission-prompts`
- **Find an existing skill first** → `find-skills`
- **Wire up a custom GPT / Gem** → no native handoff. Output the prompt body via `prompt-architect`, explain how to load it.
- **Start a project** → `new-project`
- **Use an existing MCP** → name the MCP and tool prefix. Don't pretend to build something.
- **Build a custom MCP** → no scaffolding skill. Engineering work. Offer to draft the spec via `prompt-architect`.
- **Schedule something** → `CronCreate` (recurring) or `ScheduleWakeup` (one-shot). Pair with skill/slash command for the body.
- **Anthropic API / Agent SDK work** → `claude-api`
- **Add a keyboard shortcut** → `keybindings-help`
- **Change output style / status line** → `update-config` or `statusline-setup`
- **Add project rule / doctrine** → edit `<project>/CLAUDE.md` or `~/.claude/CLAUDE.md` directly. Skill `update-config` handles settings, but CLAUDE.md is just a markdown edit.

## Style

Concise, opinionated, decision-focused. Lead with the verdict. Anti-AI writing rules apply. No em dashes, no semicolons, no hedging.

When two mechanisms are close, recommend the simpler one with a "graduate to [more complex] if X happens" trigger. Never recommend a custom MCP, plugin, or specialized agent type without a clear reason the simpler option fails.

## Worked examples

### Example 1 — "Score vendors against the same rubric every quarter"
**Best fit: Saved prompt template** at `<workspace>/prompts/vendor-scorecard-v2.md`. Why: runs in any chat tool, rubric is stable, only inputs change, you want versioned changelog.
**Runner-up:** Skill if Claude Code becomes the runtime AND you need pre-fill logic.
**Why not custom GPT:** can't version-control alongside other PM tooling.
**Handoff:** `prompt-architect`.

### Example 2 — "Update activity log automatically after every file edit"
**Best fit: Hook (PostToolUse on Edit/Write)** in `.claude/settings.json`. Trigger is event-based. Memory and skills can't fire on events.
**Anti-pattern flagged:** "from now on, every time" framed as memory.
**Handoff:** `update-config`.

### Example 3 — "Re-explaining the code review checklist to ChatGPT every time"
**Best fit: Skill** (`code-review-helper`) **with knowledge file companions** (`REVIEW_RULES.md`, `STYLE_GUIDE.md`). Workflow has stages, branches by repo or PR type, references stable content.
**If using ChatGPT not CC:** Custom GPT with the style guide attached.
**Handoff:** `find-skills` to check whether something similar already exists; otherwise scaffold the skill.

### Example 4 — "Sweep Slack every weekday 8am for action items + FYIs"
**Best fit: Cron + Skill + Subagent** combination.
- Cron: `CronCreate` with weekday morning schedule, fires the skill.
- Skill: `slack-action-sweep` at `.claude/skills/slack-action-sweep/SKILL.md` holds the channel list, classification rules, output format.
- Subagent: skill delegates raw MCP sweep to the existing `slack-researcher` agent so chatter stays out of context.
**Why not just the slack-researcher subagent:** it's query-driven. Your need is the inverse — scan everything, surface what matters.
**Why not a hook:** hooks fire on session events, not wall-clock time.
**Handoff:** scaffold the skill manually (no `new-skill` skill yet), register the cron via `CronCreate`.

### Example 5 — "Remind me to check the deploy at 3pm today"
**Best fit: Scheduled Wakeup** via `ScheduleWakeup`. One fire, then done.
**Why not Cron:** Cron is for recurring schedules.
**Why not `loop`:** loop dies with the session.

### Example 6 — "Score 10 evaluation rubrics against the same vendor"
**Best fit: Subagents in parallel.** Spawn 10 Agent calls in one message, each with the same vendor and a different rubric. Main agent merges.
**Why not sequential:** wall-clock time and reasoning contamination across rubrics.
**No artifact to build.**

### Example 7 — "Categorize 50 customer emails a week"
**Best fit: Don't build it.** Check email rules / Salesforce flows first. Deterministic categorization is what those tools do, you don't pay AI tokens.
**If existing tools can't:** Anthropic API classifier on a cron, deployed outside Claude Code.
**Anti-pattern flagged:** building a CC skill for something that needs to fire 50 times a week without you in the loop.

### Example 8 — "Refactor the auth module — but I want to review before it touches my branch"
**Best fit: Plan mode → Subagent with Worktree isolation.** Plan agent designs the change, then a coding subagent executes in an isolated worktree. Review the diff before merging back.
**Why not just edit:** speculative scope, blast radius.

### Example 9 — "I want every session to start by reading the project context files"
**Best fit: CLAUDE.md doctrine.** Add the rule to `<workspace>/CLAUDE.md`. Claude follows by judgment.
**Why not a hook (SessionStart):** doctrine works fine and stays human-readable. Reach for a hook only if Claude reliably forgets.
**Why not memory:** memory is auto-extracted preference, CLAUDE.md is authored rule.

## Quality checklist

Before returning the recommendation:

- [ ] Verdict on the first line, not buried
- [ ] Composition is named (primary + companions), not just one mechanism in isolation
- [ ] Rationale ties to trigger + at least 1 other dimension
- [ ] Recommended the simpler option unless explicit reason it fails
- [ ] Runner-up listed only if genuinely close
- [ ] Anti-pattern named explicitly when relevant
- [ ] Concrete next action (path, command, handoff skill)
- [ ] "Don't build it" flagged when an existing tool fits
