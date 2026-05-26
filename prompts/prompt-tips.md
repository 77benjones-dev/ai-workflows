# Prompt Tips

A structured reference of prompting techniques — each with a description, example, and PM use case.

---

## 1. Upload Context Documents

**Description:** Give the AI relevant files upfront so it can ground responses in your actual situation. Upload org charts, PRDs, goals frameworks, meeting notes. When you get a great output, upload *that* too as future context — it teaches the model your standards.

**Example:** "Here's our Q3 OKR doc and our product principles doc. Use these as context for everything I ask today."

**PM Use Case:** Before a planning session, upload last quarter's retro, the current roadmap, and your team's definition of done. The AI reasons from your reality, not generic advice.

---

## 2. Start with an Action Verb

**Description:** Open every prompt with a clear verb that tells the model exactly what to do. "Summarize", "Draft", "Compare", "Rank", "Critique", "Extract". Vague prompts get vague outputs.

**Example:** "Summarize the key risks in this PRD in 5 bullet points." vs. "What do you think about this PRD?"

**PM Use Case:** "Draft a one-pager stakeholder brief for this feature, using the attached spec. Keep it to 300 words." — gives the model a job, not a topic.

---

## 2b. Assign a Role / Persona

**Description:** Tell the model who it is before you ask it anything. A well-defined persona shifts the frame of reference for every answer — expertise level, priorities, blind spots, tone. This is the single highest-leverage one-liner in prompting, and it's different from the multi-expert panel (tip 8), which uses multiple roles for breadth. This is about setting one consistent, precise identity.

**Example:** "You are a senior PM at a Series B SaaS company with a strong bias toward shipping and learning over perfect planning."

**PM Use Case:** Set a persona that matches the review you need — "You are a skeptical VP of Engineering" for a pre-mortem, "You are a B2B customer who churned after 3 months" for churn analysis. Same prompt, different lens.

---

## 3. Set Tone and Audience

**Description:** Explicitly tell the model who the output is for and what register to use. Same content reads completely differently for an exec vs. an engineer vs. a customer.

**Example:** "Write this for a non-technical VP who cares about revenue impact, not implementation details. Keep the tone confident and concise."

**PM Use Case:** Reuse the same feature brief to generate an exec summary, an engineering handoff, and a customer FAQ — just swap the audience instruction.

---

## 4. Provide Good and Bad Examples (Few-Shot)

**Description:** Show the model 2–4 labeled examples of what you want (and optionally what you don't). Best when the *format or style* of the output matters more than the reasoning — it's easier to demonstrate "good" than to describe it. Models follow patterns over descriptions. (Contrast with Chain-of-Thought, tip 10, which improves the *reasoning process* rather than the output shape.)

**Example:** "Here is a GOOD acceptance criteria: [example]. Here is a BAD one: [example]. Now write acceptance criteria for this user story: [story]."

**PM Use Case:** Share three past tickets you're proud of as "good examples" before asking it to write new ones. Also works for tone-matching comms, classifying user feedback, or locking in a specific doc structure. Your style becomes the template.

---

## 5. Negative Prompting

**Description:** Tell the model what to leave out, avoid, or not do. This narrows the solution space and stops unwanted defaults — like generic fluff, excessive caveats, or wrong formats.

**Example:** "Do not include implementation suggestions. Do not use bullet points. Do not hedge with phrases like 'it depends'."

**PM Use Case:** When generating a stakeholder update: "Don't include technical jargon or mention sprint numbers. No preamble — just start with the key message."

---

## 5b. Constrain the Scope

**Description:** Bound the problem before asking for a solution. State fixed assumptions, time horizons, out-of-scope areas, and constraints explicitly. Without this, the model solves a reasonable version of your problem — not necessarily *your* version. This is distinct from negative prompting (tip 5), which controls the output; this controls the *problem space*.

**Example:** "Assume we won't change pricing. Assume a 3-month delivery window. Ignore enterprise customers for now. Given those constraints, what's the best go-to-market approach?"

**PM Use Case:** When asking for a roadmap recommendation: "Assume the team is 3 engineers and 1 designer, budget is fixed, and we're not touching the core infrastructure this half." Constraints force the model to operate in your reality.

---

## 6. Define Output Structure

**Description:** Specify the exact format you want the response in. Use headers, tables, JSON, numbered lists, or XML — whatever fits your workflow. Models follow structure much better when you enforce it.

**Example:** "Respond using this format exactly: ## Problem | ## Solution | ## Risks | ## Open Questions."

**PM Use Case:** Standardize all meeting debrief outputs: "Always respond with: Key decisions, Action items (owner + due date), Open questions, and Next steps."

---

## 7. Request Challenge + Pros/Cons (Bull/Bear)

**Description:** Ask the model to actively critique your idea, not just support it. Request bull and bear cases, risks, or devil's advocate arguments. This is where AI earns its keep vs. a search engine.

**Example:** "Give me the strongest bull case and the strongest bear case for launching this feature in Q2. Then give me your honest recommendation."

**PM Use Case:** Before a leadership review, run your proposal through: "What are the 3 biggest reasons this fails? What would a skeptical VP of Engineering push back on?"

---

## 8. Multi-Expert Panel

**Description:** Tell the model to respond as a panel of experts with different, sometimes conflicting, perspectives. This surfaces blind spots and forces broader thinking than a single-voice answer. (Credit: Andrej Karpathy)

**Example:** "Respond as three experts: a growth PM, a risk-averse engineer, and a UX researcher. What does each say about this proposal?"

**PM Use Case:** When evaluating a build vs. buy decision, have the model roleplay your CTO, your CFO, and a startup founder who's already solved this problem.

---

## 9. Ask for Clarifying Questions

**Description:** Instruct the model to ask you questions before answering if your request is ambiguous. This mimics good human collaboration and catches assumptions before they compound.

**Example:** "Before you respond, ask me any clarifying questions you need to give me a precise, useful answer."

**PM Use Case:** When kicking off a new brief or strategy doc, let the AI interview you first. The questions it asks often reveal what you haven't thought through yet.

---

## 10. Chain of Thought (Step-by-Step Reasoning)

**Description:** Explicitly tell the model to think through a problem step-by-step before giving a conclusion. This dramatically improves accuracy on complex reasoning, analysis, and decisions. It turns AI from an answer machine into a thinking partner, and it gives you something you can actually challenge, refine, and trust.

**Example:** "Think step-by-step. For each step, briefly explain your reasoning. Then summarize your conclusion at the end."

**PM Use Case:** "Walk me through how you'd prioritize these 8 features using RICE. Show your reasoning for each before giving a final ranking."

---

## 11. Test and Iterate

**Description:** Treat prompting like A/B testing — change one variable at a time and compare outputs. The first prompt is rarely the best one. Keep a "golden task" to test changes against.

**Example:** Run the same task with: (a) your original prompt, (b) with a persona added, (c) with examples added. Compare quality systematically.

**PM Use Case:** Use a standard PRD section as your benchmark task. Each time you refine your prompt template, run it on the same PRD to see if the output improves.

---

## 11b. Save + Version Your Prompts

**Description:** Treat your best prompts like code — save them, name them, and version them. Every time you refine a prompt and get a better output, update the saved version. This is the difference between a PM who's good at prompting and one who's built a compounding system.

**Example:** Keep a `prompts.md` file with named entries: `[ticket-writer-v3]`, `[exec-brief-v2]`, `[churn-analysis-v1]`. Note what changed between versions and why.

**PM Use Case:** Your "weekly status update" prompt gets better every time you tweak it. If you don't save it, you're starting from scratch next Friday. Version-controlled prompts are a personal productivity asset that compounds over time.

---

## 11b. Combine Few-Shot + Chain-of-Thought

**Description:** Few-shot locks in the *shape* of the output; chain-of-thought improves the *reasoning inside* it. Used together, you get format consistency *and* rigorous thinking — the combo is stronger than either alone.

**Example:** "Here are two examples of a risk assessment [examples]. Now think step-by-step about the risks in this new feature, then write your assessment in the same format as the examples."

**PM Use Case:** When doing a pre-mortem or sizing exercise: show 2–3 past examples of good analysis (few-shot), then ask it to reason through the new case before writing up the output. You get your format and you get the work shown.

---

## 12. Use XML Tags for Structure

**Description:** Wrap your prompt in XML-style tags to separate role, context, task, and format. This dramatically reduces misinterpretation, especially in long or complex prompts. Claude is particularly responsive to XML.

**Example:**
```
<role>You are a senior PM at a B2B SaaS company.</role>
<context>[paste your PRD or notes here]</context>
<task>Write a one-page executive summary of this feature.</task>
<output_format>Use: ## Summary | ## Business Case | ## Key Risks</output_format>
```

**PM Use Case:** Build a reusable template for your most common tasks (PRD review, stakeholder update, retrospective summary) — just swap the `<context>` block each time.

---

## 13. Task Decomposition + Chaining

**Description:** Break large, complex tasks into a sequence of smaller steps. The output of step 1 feeds step 2. This improves reliability — models hallucinate more when asked to do too much at once.

**Example:** Step 1: "Extract all user pain points from this research." → Step 2: "Group them into themes." → Step 3: "Rank by frequency and impact."

**PM Use Case:** Discovery synthesis: decompose "turn these 20 interview transcripts into a strategy recommendation" into: extract insights → cluster → prioritize → draft narrative.

---

---

# 🛠 Product-Building Settings

*The tips below shift from "how to prompt" to "how to configure the AI environment itself." These are the levers you control when building AI-powered products or persistent assistants — not just one-off conversations.*

---

## P1. Tune Hyperparameters

**Description:** Hyperparameters are the configuration settings that shape how a model behaves *before* it processes your prompt — they're the operating environment, not the intelligence. The most important ones for PMs building with AI: **Temperature** (0 = precise/deterministic, 1 = creative/varied), **Max Tokens** (caps response length, affects cost and latency), **System Prompt** (the always-on instruction layer users never see), and **Context Window** (how much the model can "see" at once). When a product feels off — too robotic, too unpredictable, too verbose — it's almost always a hyperparameter issue, not a model issue.

**Example:** A support bot should have temperature ~0.2 (consistent, accurate). A brainstorming tool should be ~0.8 (varied, generative). Same model, completely different feel.

**PM Use Case:** Before writing a single word of a system prompt, decide on temperature. Are users coming for reliable answers or creative exploration? That decision shapes everything else. Low temp + tight system prompt = predictable product. High temp + loose system prompt = divergent tool.

---

## 14. Create Specialized Agents (GPTs)

**Description:** Build dedicated AI setups for recurring tasks instead of re-prompting from scratch each time. Each "agent" has a baked-in persona, context, and output format for one specific job.
One agent for writing tickets, one for reviewing PRDs, one for competitive analysis. Each has its own system prompt and relevant docs loaded. Can re-use these GPTs/agents in router-knowledge setups. 

**Example:** AC style guide (attachment)

**PM Use Case:** A "User story" agent with your team's definition of done, your story format, and three good examples always loaded — so ticket quality is consistent with zero ramp-up.

---

## 15. Router + Knowledge File Architecture

**Description:** Build a master prompt that routes requests to the right sub-prompt or knowledge source depending on what's being asked. Pair it with structured knowledge files (org context, goals, definitions) the model references on demand.

**Example:** A "PM Assistant" that detects if you're asking about strategy, execution, or communication — and applies a different template + pulls from the relevant doc.

**PM Use Case:** One AI assistant that knows your team's goals, your product's glossary, and your standard formats — so every output is pre-calibrated to your context without re-explaining every time.

---

## 16. Disposition Statement

**Description:** Define the AI's personality, values, and working style at the start of a system prompt or session. This shapes *how* it answers, not just *what* it answers — useful for consistency across long sessions.

**Example:** "You are direct, skeptical, and prioritize clarity over comprehensiveness. When you're unsure, say so. Never pad responses with filler."

**PM Use Case:** Set a disposition that mirrors how you want a senior colleague to interact with you — e.g., "Challenge my assumptions. Point out when I'm asking the wrong question."

---

## 17. Error Root Cause Debrief

**Description:** When the model gives a bad output, ask it *why* it got it wrong — what in your prompt, its interpretation, or its approach led to the mistake. Then use that diagnosis to improve the prompt.

**Example:** "That output missed the mark. What in my prompt caused you to go in that direction? What would a better prompt have said?"

**PM Use Case:** After a hallucinated sprint estimate or a misframed problem statement, debrief with the AI before re-trying. You're building prompt intuition with every debrief.

---

## 18. Troubleshooting Retrospective

**Description:** After a difficult or lengthy problem-solving session, ask the model to generalize what you both learned into reusable principles. Store these in a running document and reference it next time. (Credit: Reddit)

**Example:** "Why did this take so long to resolve? What could we have done differently to find the root cause faster? Now generalize that into a troubleshooting tip I can reuse."

**PM Use Case:** After a messy incident post-mortem or a tricky prioritization debate, capture the reasoning pattern that finally worked — then use it to shortcut the next one.

---

## 19. Self-Critique Loop (Generate → Critique → Improve)

**Description:** Ask the model to produce an output, then immediately critique it against specific criteria, then revise. All in one prompt or in sequence. This removes the need for you to be the editor on every draft.

**Example:** "Draft a feature announcement. Then critique it: is it clear, compelling, and right for a non-technical audience? Then rewrite it based on the critique."

**PM Use Case:** Use for any high-stakes external communication — launch emails, exec updates, or customer-facing release notes — where a second pass would normally require another person.

---

## 20. Context Engineering (Minimal High-Signal Tokens)

**Description:** Think of your prompt as a context budget. Cut filler, prioritize high-signal information. Ask: "What is the smallest, most precise context that gives the model the best chance of the right output?" (Credit: Andrej Karpathy, Tobi Lütke)

**Example:** Instead of pasting an entire 40-page strategy doc, extract and paste the 5 most relevant sections. The model performs better on focused, curated input.

**PM Use Case:** When asking for a competitive analysis, don't dump every doc you have — extract the specific claims, metrics, or decisions you need analyzed. Precision in, precision out.

---

## 21. Prompt Repetition

**Description:** Repeat the core instruction 2–3 times in a long prompt — once near the top and once at the end. Research shows this measurably improves adherence to key constraints, especially in complex prompts. (Credit: Google research, 2025)

**Example:** "Your output must be 200 words max. [... full prompt ...] Remember: keep your response to 200 words maximum."

**PM Use Case:** When format discipline matters — like a character-limited exec summary or a tightly scoped decision brief — bookend your prompt with the constraint to reinforce it.

---

---

# 📐 Prompt Frameworks

*Reusable structural templates — apply as a scaffold, then layer in techniques from above. Note: most framework components (Role, Format, Examples, etc.) map directly to techniques covered above. Their real value isn't teaching new tricks — it's acting as a **checklist at prompt-writing time** so you don't forget a critical ingredient.*

---

## F1. COSTAR

**Context, Objective, Style, Tone, Audience, Response** — Best for generating structured, tailored content where voice, register, and audience precision all matter.

**Context** — The background situation the AI needs to understand before responding.
**Objective** — The specific goal or outcome you want the output to achieve.
**Style** — The writing style to adopt (e.g., formal, conversational, journalistic).
**Tone** — The emotional register (e.g., confident, empathetic, urgent).
**Audience** — Who the output is for and their level of familiarity with the topic.
**Response** — The desired format, length, or structure of the output.

---

## F2. CARE

**Context, Action, Result, Example** — Ideal for business tasks where you need to anchor a request in a real scenario and show what "good" looks like.

**Context** — The situation or background the AI should factor in.
**Action** — The specific task you want the AI to perform.
**Result** — The outcome or goal you're aiming for.
**Example** — A concrete sample that illustrates the standard you expect.

---

## F3. RACE

**Role, Action, Context, Expectation** — A quick, agile framework useful for task-specific, high-volume prompts where speed matters.

**Role** — The persona or expertise the AI should adopt.
**Action** — The specific task to perform.
**Context** — Relevant background or constraints the AI needs to know.
**Expectation** — The desired output format, quality bar, or success criteria.

---

## F4. CLEAR

**Concise, Logical, Explicit, Adaptive, Reflective** — Focuses on the quality and structure of the prompt itself rather than specifying content components.

**Concise** — Keep the prompt brief; remove filler and redundancy.
**Logical** — Structure your ask in a coherent, sequenced order.
**Explicit** — State exactly what you want with no ambiguity or assumed context.
**Adaptive** — Adjust the prompt based on model responses and prior outputs.
**Reflective** — Consider what the model actually needs to know to succeed.

---

## F5. RTF

**Role, Task, Format** — The simplest framework; best for fast, one-off prompts where you just need a reliable result quickly.

**Role** — Who the AI should be.
**Task** — What to do.
**Format** — How to structure or present the output.

---

<from EA workshop> (need to rework them to avoid copyright)
## Iterative Refinement:
**Why this matters**
This mirrors how real work happens. AI becomes a partner in refinement, helping you move faster without settling for the first draft.
**Prompt the AI:**
“Revise this update to be clearer for non-technical teams. Now make it more player-focused. Explain what changed between versions and what trade-offs you made.”


## Role-Playing (like group of experts)
**Why this matters**
This turns AI into a stand-in for real stakeholders, helping you pressure-test ideas before alignment meetings even start.
Prompt the AI:
“Act as a gameplay designer focused on player delight and balance. Now switch to a producer responsible for timelines and team capacity. Where do these perspectives clash, and what compromises emerge?”

## Time Travel
Prompt the AI:
 “Assume it is two years after launch and this initiative failed. What went wrong, what early signals did we miss, and what would you change if you could go back to today?”
Why this matters
 This helps you make better decisions now by borrowing clarity from hindsight and foresight.

## Few-Shot With Variance
Prompt the AI:
“Here are three example messages that match EA’s tone and clarity standards. Create five new variations that follow the same structure, but vary emotional tone and player motivation.”
Why this matters
This is how you scale quality without cloning content. AI learns your standards, then helps you explore the creative space around them.

## Simulated Debate and Reflection (similar to group of experts)
Prompt the AI:
“Debate this proposal from the perspective of player trust, operational cost, and long-term brand impact. Then critique the strongest argument and explain what evidence would be needed to make a final decision.”
Why this matters
This is how collaboration becomes judgment. AI helps you pressure-test thinking, surface trade-offs, and walk away with a decision you can stand behind.

</
