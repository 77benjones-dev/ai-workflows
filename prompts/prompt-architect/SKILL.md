---
name: prompt-architect
description: Convert a vague request, idea, or task into a production-grade prompt — role, inputs, constraints, output schema, and stress tests. Use when the user says "write a prompt for X", "turn this into a prompt", "help me prompt this", "draft a system prompt", "make this prompt better", "meta-prompt this", or invokes /prompt-architect. Outputs a copy-paste-ready prompt plus shorter and stricter variants. NOT for answering the underlying question — only for crafting the prompt that would.
---

# /prompt-architect Meta-Prompt Builder

Take a user request and produce a production-grade prompt. The deliverable is the *prompt*, not the answer to it.

## When to use

- User wants to write a prompt for a recurring task (ticket-writer, exec brief, churn analysis, etc.)
- User has a vague ask and wants it converted into something they can paste into another model or agent
- User wants to harden an existing prompt — add constraints, structure, stress tests
- User is building a GPT, agent, or skill system prompt
- Invoked as `/prompt-architect`

**Do not use** when the user wants the underlying task done. If they say "draft a stakeholder update", that's `product-management:stakeholder-update`. If they say "draft a prompt for stakeholder updates", that's this skill.

## Knowledge file

Canonical best-practices reference: `examples/prompt-tips.md` in this repo, or wherever you've saved it locally.

Load lazily — only read when the request needs technique-level guidance (e.g., user asks "which technique fits here?", or you're unsure which 3-7 techniques to apply). For most prompt-building, the rules below are sufficient.

## Decision rules (non-negotiable)

1. **Ask clarifying questions only if missing information would materially change the output.** Ask one at a time, max 3 total. Always provide a best-effort prompt even when asking.
2. **If the user wants an immediate result, proceed using best-effort assumptions** and label them under **Assumptions**.
3. **Never fabricate facts or sources.** If facts are required, request them or use explicit placeholders like `[NEEDED: ...]`.
4. **When uncertain, surface the assumption explicitly** rather than silently resolving it.

## Input contract — extract and normalize

From the user's request, identify:

- **Task** — action verb, target audience, tone, success criteria
- **Inputs** — required data, files, links, examples
- **Constraints** — length, time, scope, allowed tools, sources
- **Non-goals** — what's explicitly out of scope
- **Ambiguities** — only ask about ones with high impact on the output

## Playbook

Apply the **3–7 most relevant** techniques from the knowledge file implicitly. Do not list techniques in the output — bake them into the prompt itself. Default toolkit:

- Role + objective
- Audience + tone
- Explicit inputs (XML or labeled blocks)
- Output schema (headers, format, length cap)
- Negative prompts (what to avoid)
- Few-shot examples (only if ambiguity is high or format is non-obvious)
- Chain-of-thought trigger (only if reasoning quality matters)
- Self-critique loop (only for high-stakes output)

Prefer minimal high-signal context and explicit structure over technique-stacking.

## Rigor check (conditional)

If the prompt being built is **evaluative** — scoring, ranking, recommending, "should we", build vs. buy, vendor assessment, PRD review, go/no-go, prioritization — bake **one** anti-confirmation-bias mechanism into the Final Prompt. Pick the best fit:

- **Forced disagreement:** "Before recommending, name the strongest counter-argument. If it's weak, say why. If you haven't tested it, say so."
- **Bull/bear:** "Give the strongest case for and against, then your recommendation."
- **Pre-mortem:** "Assume this decision failed two years from now. What went wrong?"
- **Distribution check:** "If your scores cluster in one band, re-examine — uniform scores usually mean the rubric isn't discriminating."
- **Self-critique loop:** "Draft → critique against [criteria] → revise."
- **Disconfirming evidence:** "List the top 3 facts that, if true, would invalidate your recommendation. Flag any you can't verify."

Pick **one**, not all. Stacking them produces output that hedges instead of decides.

**Skip this section for generative tasks** (drafts, summaries, release notes, comms, copy). Adding skepticism to writing tasks produces wishy-washy prose.

## Clarify threshold

Critical inputs — without them the output is decorative, not useful:

1. **Task verb** — what is the prompt supposed to make the model *do*?
2. **Audience or use context** — who reads the output, or which model/agent runs the prompt?
3. **Output destination** — one-off paste into ChatGPT, system prompt for an agent, slash command, GPT instructions?

**Threshold rule:** if **2 or more** of these are missing or ambiguous, ask **one** clarifying question first (max 3 across the conversation, per decision rule 1). Otherwise proceed with assumptions labeled.

Soft signals that also trigger a question — but only one — when they're material:

- Evaluative task with no rubric, no decision threshold, no stakes
- High-stakes use (production system prompt, customer-facing) with no examples or refusal rules
- Domain-specific task with no domain context

Never ask about: tone preferences, format preferences, length. Default to assumptions and let the user redirect.

## Output template

Always use these headers, in this order:

```
**Goal (restated)**
[One sentence — what the user is trying to accomplish.]

**Assumptions**
[Bulleted list. Omit if none.]

**Clarifying Question**
[Only if needed. One question. Otherwise omit this section entirely.]

**Final Prompt**
[Copy-paste ready. Use XML tags or clear labeled blocks. Wrap in a fenced code block.]

**Variants**
- _Shorter:_ [tighter version, ~50% length]
- _Stricter:_ [same length but with harder constraints, refusal rules, or output schema]

**Stress Test**
[3–5 edge or adversarial inputs and the expected behavior. Use 0–2 if the task is trivial.]

**Capability Hints** (conditional — see rules below)
[2–3 Claude capabilities that would meaningfully upgrade this prompt, each with a "when to pick it" trigger. Omit entirely when skip rule applies.]
```

## Capability Hints rules

Include the **Capability Hints** section only when at least one of these is true:

- The task is evaluative, analytical, or decision-supporting (scoring, ranking, recommending, reviewing)
- The prompt is intended for repeated use (5+ runs, system prompt, GPT, agent, slash command)
- The output is high-stakes (going to leadership, customer-facing, audit-relevant)
- The user explicitly asks "what tools should I use" or "how should I run this"

**Skip entirely** for simple generative tasks (one-off drafts, summaries, comms, copy tweaks) and quick gut-check prompts. Adding capability suggestions to a "draft a Slack message" prompt is filler.

When included, pick **at most 3** from the menu below. Frame each as "if X about your use case, use Y." Do not list everything — pick what genuinely fits.

**Capability menu:**

- **Extended Thinking** — when the answer involves tradeoffs, ambiguity, or multi-step reasoning. Tell the user to enable thinking mode (default on Opus 4.7 in Claude Code; `thinking: { type: "enabled", budget_tokens: 10000 }` via API). Best for evaluative prompts.
- **Prompt Caching** — when the same prompt will run 5+ times with only one variable changing (e.g., scoring multiple vendors against the same rubric). 90% cost reduction. Cache the static blocks via API `cache_control: { type: "ephemeral" }`.
- **Tool Use (Web Search)** — when input data is incomplete, stale, or vendor-supplied (only one side of the story). Removes manual data-prep step. Add an explicit rule to distinguish independent sources from supplied ones.
- **Citations** — when output must be auditable and every claim traceable. Critical for high-stakes evaluations going up the chain. Enable via API document `citations: { enabled: true }`, or simulate in-prompt by requiring inline quoted excerpts.
- **Subagents (parallel)** — when the task decomposes cleanly into independent parts (per-category scoring, multi-persona review). Each subagent works in isolation, main agent merges. Use `Agent` tool with multiple parallel calls.
- **Memory / saved prompts** — when the user is building a recurring system. Suggest saving the prompt to a versioned `prompts/saved/` folder (or your local equivalent), or wrapping as a slash command if Claude Code is the runtime.
- **Structured Output (JSON)** — when output feeds into another system (Airtable, comparison sheet, downstream tool). Two-pass approach: model emits JSON, render markdown separately.
- **Self-critique loop (two-turn)** — when the prompt produces a draft that benefits from a second-pass review. The model is more honest about a draft it's already committed to than one it's still writing.

**Format for each hint:**
- **[Capability name]** — _When to pick it:_ one sentence. _What it adds:_ one sentence. _How to enable:_ one line (Claude Code, API, or in-prompt instruction).

## Quality checklist

Before returning, verify the **Final Prompt** has:

- [ ] Role and objective stated
- [ ] Audience and tone specified
- [ ] Inputs called out explicitly
- [ ] Constraints (length, format, sources, refusals) stated
- [ ] Output schema defined
- [ ] Edge cases or refusal rules covered
- [ ] Examples — only if ambiguity is high

## Style

Concise, technical, actionable. Brief rationale or tradeoffs welcome. No lengthy step-by-step internal reasoning unless the user asks. Anti-AI writing rules apply (no em dashes, semicolons, hedging).

## Saving prompts

When the user says "save this" or "version this", write to your local saved-prompts folder as `<name>-v<N>.md` with a header noting date, what changed from the prior version, and why. This makes prompts a compounding asset (see Tip 11b in the knowledge file).
