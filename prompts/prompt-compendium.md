# Prompt Compendium

A practical reference for getting better outputs from AI. Useful for product managers or anyone who works with language models daily.

## What This Is

18 core prompting techniques, 5 reusable frameworks, 6 bonus techniques for advanced use cases, and a meta-prompt to help you write better prompts. Each entry includes a description, example, PM use case, and knowledge worker use case. Treat this as a toolkit, not a tutorial - techniques layer and combine.

## How to Use This

- **Starting out?** Read techniques 1-10 in order. They're foundational.
- **Need a structure?** Use the Frameworks section as a checklist when writing complex prompts.
- **Optimizing a recurring task?** Combine techniques. Few-shot examples, step-by-step reasoning, and XML tags are force multipliers.
- **Advanced patterns?** Check the Bonus Techniques section for iteration, role-playing, and strategic foresight.
- **Want help writing prompts?** Use the Meta Prompt to have AI optimize your prompts for clarity and effectiveness.

Best practice: save prompts that work. Version them. Refine them over time. This document is a reference, but your personal prompt library is the asset that compounds.

---

## Table of Contents

- [Prompt Frameworks](#prompt-frameworks) - reusable prompt templates
- [Core Techniques](#core-techniques) - foundational prompting skills
- [Bonus Techniques](#bonus-techniques) - advanced patterns for iteration and exploration
- [Meta Prompt](#meta-prompt) - use AI to write better prompts

---

<a id="prompt-frameworks"></a>

## Prompt Frameworks

*Reusable structural templates - apply as a scaffold, then layer in techniques from above. Note: most framework components (Role, Format, Examples, etc.) map directly to techniques covered above. Their real value isn't teaching new tricks - it's acting as a **checklist at prompt-writing time** so you don't forget a critical ingredient.*

---

### 1. COSTAR

**Context, Objective, Style, Tone, Audience, Response** - Best for generating structured, tailored content where voice, register, and audience precision all matter.

**Context** - The background situation the AI needs to understand before responding.
**Objective** - The specific goal or outcome you want the output to achieve.
**Style** - The writing style to adopt (e.g., formal, conversational, journalistic).
**Tone** - The emotional register (e.g., confident, empathetic, urgent).
**Audience** - Who the output is for and their level of familiarity with the topic.
**Response** - The desired format, length, or structure of the output.

---

### 2. CARE

**Context, Action, Result, Example** - Ideal for business tasks where you need to anchor a request in a real scenario and show what "good" looks like.

**Context** - The situation or background the AI should factor in.
**Action** - The specific task you want the AI to perform.
**Result** - The outcome or goal you're aiming for.
**Example** - A concrete sample that illustrates the standard you expect.

---

### 3. RACE

**Role, Action, Context, Expectation** - A quick, agile framework useful for task-specific, high-volume prompts where speed matters.

**Role** - The persona or expertise the AI should adopt.
**Action** - The specific task to perform.
**Context** - Relevant background or constraints the AI needs to know.
**Expectation** - The desired output format, quality bar, or success criteria.

---

### 4. CLEAR

**Concise, Logical, Explicit, Adaptive, Reflective** - Focuses on the quality and structure of the prompt itself rather than specifying content components.

**Concise** - Keep the prompt brief; remove filler and redundancy.
**Logical** - Structure your ask in a coherent, sequenced order.
**Explicit** - State exactly what you want with no ambiguity or assumed context.
**Adaptive** - Adjust the prompt based on model responses and prior outputs.
**Reflective** - Consider what the model actually needs to know to succeed.

---

### 5. RTF

**Role, Task, Format** - The simplest framework; best for fast, one-off prompts where you just need a reliable result quickly.

**Role** - Who the AI should be.
**Task** - What to do.
**Format** - How to structure or present the output.

---

<a id="core-techniques"></a>

## Core Techniques

### 1. Upload Context Documents

**Description:** Give the AI relevant files upfront so it can ground responses in your actual situation. Upload org charts, PRDs, goals frameworks, meeting notes. When you get a great output, upload *that* too as future context - it teaches the model your standards.

**Example:** "Here's our Q3 OKR doc and our product principles doc. Use these as context for everything I ask today."

**PM Use Case:** Before a planning session, upload last quarter's retro, the current roadmap, and your team's definition of done. The AI reasons from your reality, not generic advice. 

**Knowledge Worker Use Case:** Upload your company's style guide, past reports you've written, and internal documentation before drafting. The AI matches your organization's standards and references real context instead of making assumptions.

---

### 2. Grounding / Citation Requirements

**Description:** Explicitly require the AI to cite or quote from provided context when making claims. This dramatically reduces hallucinations and makes outputs verifiable. Force the model to distinguish between what's in your documents vs. what it's inferring or generating.

**Example:** "Only use information from the attached PRD. For every claim, quote the specific section you're referencing. If something isn't in the doc, say 'Not specified in document.'"

**PM Use Case:** When synthesizing user research or analyzing competitive docs, require citations so you can trace every insight back to source material. Critical for exec summaries where accuracy matters more than completeness.

**Knowledge Worker Use Case:** When analyzing contracts, legal documents, or research papers, require direct quotes with page/section numbers. Makes fact-checking trivial and builds audit trails for compliance or due diligence work.

---

### 3. Start with an Action Verb

**Description:** Open every prompt with a clear verb that tells the model exactly what to do. "Summarize", "Draft", "Compare", "Rank", "Critique", "Extract". Vague prompts get vague outputs.

**Example:** "Summarize the key risks in this PRD in 5 bullet points." vs. "What do you think about this PRD?"

**PM Use Case:** "Draft a one-pager stakeholder brief for this feature, using the attached spec. Keep it to 300 words." - gives the model a job, not a topic.

**Knowledge Worker Use Case:** "Extract action items from this meeting transcript and assign ownership based on context." Clear verbs ("Extract", "Summarize", "Compare") eliminate ambiguity and speed up routine tasks.

---

### 4. Assign a Role / Persona

**Description:** Tell the model who it is before you ask it anything. A well-defined persona shifts the frame of reference for every answer - expertise level, priorities, blind spots, tone. This is the single highest-leverage one-liner in prompting, and it's different from the multi-expert panel (technique 11), which uses multiple roles for breadth. This is about setting one consistent, precise identity.

**Example:** "You are a senior PM at a Series B SaaS company with a strong bias toward shipping and learning over perfect planning."

**PM Use Case:** Set a persona that matches the review you need - "You are a skeptical VP of Engineering" for a pre-mortem, "You are a B2B customer who churned after 3 months" for churn analysis. Same prompt, different lens.

**Knowledge Worker Use Case:** "You are a tax accountant reviewing this expense report for compliance issues" or "You are a senior editor for The Economist" - the persona sets expertise level and catches errors you might miss.

---

### 5. Set Tone and Audience

**Description:** Explicitly tell the model who the output is for and what register to use. Same content reads completely differently for an exec vs. an engineer vs. a customer.

**Example:** "Write this for a non-technical VP who cares about revenue impact, not implementation details. Keep the tone confident and concise."

**PM Use Case:** Reuse the same feature brief to generate an exec summary, an engineering handoff, and a customer FAQ - just swap the audience instruction.

**Knowledge Worker Use Case:** Turn meeting notes into a board memo (formal, concise), an internal wiki update (detailed, conversational), or a client email (friendly, action-oriented) - same facts, different packaging for each stakeholder.

---

### 6. Provide Good and Bad Examples (Few-Shot)

**Description:** Show the model 2-4 labeled examples of what you want (and optionally what you don't). Best when the *format or style* of the output matters more than the reasoning - it's easier to demonstrate "good" than to describe it. Models follow patterns over descriptions. (Contrast with Chain-of-Thought, technique 13, which improves the *reasoning process* rather than the output shape.)

**Example:** "Here is a GOOD acceptance criteria: [example]. Here is a BAD one: [example]. Now write acceptance criteria for this user story: [story]."

**PM Use Case:** Share three past tickets you're proud of as "good examples" before asking it to write new ones. Also works for tone-matching comms, classifying user feedback, or locking in a specific doc structure. Your style becomes the template.

**Knowledge Worker Use Case:** Provide 2-3 examples of "good" email responses to customer complaints before drafting new ones. The AI learns your company's voice, empathy level, and resolution patterns without explicit instructions.

---

### 7. Negative Prompting

**Description:** Tell the model what to leave out, avoid, or not do. This narrows the solution space and stops unwanted defaults - like generic fluff, excessive caveats, or wrong formats.

**Example:** "Do not include implementation suggestions. Do not use bullet points. Do not hedge with phrases like 'it depends'."

**PM Use Case:** When generating a stakeholder update: "Don't include technical jargon or mention sprint numbers. No preamble - just start with the key message."

**Knowledge Worker Use Case:** When drafting a policy document: "Don't use legal jargon. Don't include implementation timelines. No hedging language like 'may' or 'should consider.'" Gets you a clear, direct draft.

---

### 8. Constrain the Scope

**Description:** Bound the problem before asking for a solution. State fixed assumptions, time horizons, out-of-scope areas, and constraints explicitly. Without this, the model solves a reasonable version of your problem - not necessarily *your* version. This is distinct from negative prompting (technique 7), which controls the output; this controls the *problem space*.

**Example:** "Assume we won't change pricing. Assume a 3-month delivery window. Ignore enterprise customers for now. Given those constraints, what's the best go-to-market approach?"

**PM Use Case:** When asking for a roadmap recommendation: "Assume the team is 3 engineers and 1 designer, budget is fixed, and we're not touching the core infrastructure this half." Constraints force the model to operate in your reality.

**Knowledge Worker Use Case:** When planning an event: "Assume budget is $5K, venue must be downtown, and we can't schedule during Q4. Given those constraints, what's the best approach?" Prevents solutions that ignore your real limitations.

---

### 9. Define Output Structure

**Description:** Specify the exact format you want the response in. Use headers, tables, JSON, numbered lists, or XML - whatever fits your workflow. Models follow structure much better when you enforce it.

**Example:** "Respond using this format exactly: ## Problem | ## Solution | ## Risks | ## Open Questions."

**PM Use Case:** Standardize all meeting debrief outputs: "Always respond with: Key decisions, Action items (owner + due date), Open questions, and Next steps."

**Knowledge Worker Use Case:** For weekly reports: "## Accomplishments | ## Blockers | ## Next Week | ## Help Needed" - same structure every time makes pattern recognition easy for managers and creates a searchable archive.

---

### 10. Request Challenge + Pros/Cons (Bull/Bear)

**Description:** Ask the model to actively critique your idea, not just support it. Request bull and bear cases, risks, or devil's advocate arguments. This is where AI earns its keep vs. a search engine.

**Example:** "Give me the strongest bull case and the strongest bear case for launching this feature in Q2. Then give me your honest recommendation."

**PM Use Case:** Before a leadership review, run your proposal through: "What are the 3 biggest reasons this fails? What would a skeptical VP of Engineering push back on?"

**Knowledge Worker Use Case:** Before proposing a new policy: "What's the strongest case for this policy? What's the strongest case against it? Where's the evidence weakest?" Surfaces blind spots before you present to leadership.

---

### 11. Multi-Expert Panel

**Description:** Tell the model to respond as a panel of experts with different, sometimes conflicting, perspectives. This surfaces blind spots and forces broader thinking than a single-voice answer. (Credit: Andrej Karpathy)

**Example:** "Respond as three experts: a growth PM, a risk-averse engineer, and a UX researcher. What does each say about this proposal?"

**PM Use Case:** When evaluating a build vs. buy decision, have the model roleplay your CTO, your CFO, and a startup founder who's already solved this problem.

**Knowledge Worker Use Case:** When analyzing a budget proposal, ask for perspectives from finance (cost control), operations (feasibility), and HR (headcount implications). Different lenses reveal different risks.

---

### 12. Ask for Clarifying Questions

**Description:** Instruct the model to ask you questions before answering if your request is ambiguous. This mimics good human collaboration and catches assumptions before they compound.

**Example:** "Before you respond, ask me any clarifying questions you need to give me a precise, useful answer."

**PM Use Case:** When kicking off a new brief or strategy doc, let the AI interview you first. The questions it asks often reveal what you haven't thought through yet.

**Knowledge Worker Use Case:** When drafting a complex proposal or analysis: "Ask clarifying questions before you start" reveals gaps in your thinking - budget assumptions you forgot, stakeholders you missed, constraints you didn't communicate.

---

### 13. Chain of Thought (Step-by-Step Reasoning)

**Description:** Explicitly tell the model to think through a problem step-by-step before giving a conclusion. This dramatically improves accuracy on complex reasoning, analysis, and decisions. It turns AI from an answer machine into a thinking partner, and it gives you something you can actually challenge, refine, and trust.

**Example:** "Think step-by-step. For each step, briefly explain your reasoning. Then summarize your conclusion at the end."

**PM Use Case:** "Walk me through how you'd prioritize these 8 features using RICE. Show your reasoning for each before giving a final ranking."

**Knowledge Worker Use Case:** When analyzing quarterly budget variances: "Explain step-by-step why each category is over/under budget. Show your calculations." You get auditable reasoning, not just a conclusion.

---

### 14. Test and Iterate

**Description:** Treat prompting like A/B testing - change one variable at a time and compare outputs. The first prompt is rarely the best one. Keep a "golden task" to test changes against.

**Example:** Run the same task with: (a) your original prompt, (b) with a persona added, (c) with examples added. Compare quality systematically.

**PM Use Case:** Use a standard PRD section as your benchmark task. Each time you refine your prompt template, run it on the same PRD to see if the output improves.

**Knowledge Worker Use Case:** Keep a reference email or report as your test case. Each time you refine your "draft monthly report" prompt, run it on the same raw data to measure improvement objectively.

---

### 15. Save + Version Your Prompts

**Description:** Treat your best prompts like code - save them, name them, and version them. Every time you refine a prompt and get a better output, update the saved version. This is the difference between a PM who's good at prompting and one who's built a compounding system.

**Example:** Keep a `prompts.md` file with named entries: `[ticket-writer-v3]`, `[exec-brief-v2]`, `[churn-analysis-v1]`. Note what changed between versions and why.

**PM Use Case:** Your "weekly status update" prompt gets better every time you tweak it. If you don't save it, you're starting from scratch next Friday. Version-controlled prompts are a personal productivity asset that compounds over time.

**Knowledge Worker Use Case:** Your "draft client proposal" or "summarize meeting notes" prompts improve weekly. Save them in a `prompts.txt` file. Each refinement compounds - you're 10x faster by month three.

---

### 16. Combine Few-Shot + Chain-of-Thought

**Description:** Few-shot locks in the *shape* of the output; chain-of-thought improves the *reasoning inside* it. Used together, you get format consistency *and* rigorous thinking - the combo is stronger than either alone.

**Example:** "Here are two examples of a risk assessment [examples]. Now think step-by-step about the risks in this new feature, then write your assessment in the same format as the examples."

**PM Use Case:** When doing a pre-mortem or sizing exercise: show 2-3 past examples of good analysis (few-shot), then ask it to reason through the new case before writing up the output. You get your format and you get the work shown.

**Knowledge Worker Use Case:** Show examples of past quarterly reports (format), then ask it to analyze new data step-by-step before drafting. You get consistent structure with rigorous analysis - best of both techniques.

---

### 17. Use XML Tags for Structure

**Description:** Wrap your prompt in XML-style tags to separate role, context, task, and format. This dramatically reduces misinterpretation, especially in long or complex prompts. Claude is particularly responsive to XML.

**Example:**
```
<role>You are a senior PM at a B2B SaaS company.</role>
<context>[paste your PRD or notes here]</context>
<task>Write a one-page executive summary of this feature.</task>
<output_format>Use: ## Summary | ## Business Case | ## Key Risks</output_format>
```

**PM Use Case:** Build a reusable template for your most common tasks (PRD review, stakeholder update, retrospective summary) - just swap the `<context>` block each time.

**Knowledge Worker Use Case:** Build reusable templates for contract review, expense analysis, or meeting summaries. XML tags keep context organized and prompts maintainable as they grow complex.

---

### 18. Task Decomposition + Chaining

**Description:** Break large, complex tasks into a sequence of smaller steps. The output of step 1 feeds step 2. This improves reliability - models hallucinate more when asked to do too much at once.

**Example:** Step 1: "Extract all user pain points from this research." → Step 2: "Group them into themes." → Step 3: "Rank by frequency and impact."

**PM Use Case:** Discovery synthesis: decompose "turn these 20 interview transcripts into a strategy recommendation" into: extract insights → cluster → prioritize → draft narrative.

**Knowledge Worker Use Case:** Turn "write Q4 board report" into: extract financial highlights → identify operational risks → summarize strategic initiatives → draft executive summary. Each step is verifiable, reducing compound errors.


---

<a id="bonus-techniques"></a>

## Bonus Techniques

### 1. Iterative Refinement

**Description:** Ask the AI to revise its own output through multiple passes, each time optimizing for a different criterion or audience. Explicitly request explanation of what changed and why. This turns the AI into a refinement partner, not just a first-draft generator.

**Example:** “Revise this update to be clearer for non-technical teams. Now make it more player-focused. Explain what changed between versions and what trade-offs you made.”

**PM Use Case:** Use for high-stakes communication - exec updates, launch announcements, customer messaging - where multiple perspectives matter and you need the work shown, not just the final result.

**Knowledge Worker Use Case:** Draft an important email, then ask: "Revise for brevity. Now revise for diplomacy. Show what changed and why." Get multiple perspectives on tone and content before you send.

---

### 2. Role-Playing

**Description:** Instruct the AI to embody a specific stakeholder persona and respond from that perspective. Unlike the multi-expert panel (technique 11), this technique focuses on a single, sustained role at a time - useful for simulating real conversations or decisions.

**Example:** “Act as a gameplay designer focused on player delight and balance. Now switch to a producer responsible for timelines and team capacity. Where do these perspectives clash, and what compromises emerge?”

**PM Use Case:** Before alignment meetings, simulate how different stakeholders will react to your proposal. Use their feedback to refine your pitch before the real conversation.

**Knowledge Worker Use Case:** Before presenting a budget proposal, roleplay your CFO's questions and concerns. Draft responses to likely objections before the meeting so you're never caught flat-footed.

---

### 3. Time Travel

**Description:** Ask the model to assume a future state (success or failure) and work backward to explain how you got there. This borrows clarity from hindsight to inform present decisions - classic pre-mortem and success visioning combined.

**Example:** “Assume it is two years after launch and this initiative failed. What went wrong, what early signals did we miss, and what would you change if you could go back to today?”

**PM Use Case:** Run a failure post-mortem before you ship. Or flip it: assume wild success and reverse-engineer what made it work. Both reveal assumptions and risks your team hasn't surfaced yet.

**Knowledge Worker Use Case:** Before a major organizational change: "Assume it's one year later and this restructure failed catastrophically. What went wrong?" Surfaces political risks, resource gaps, and communication failures before they happen.

---

### 4. Few-Shot With Variance

**Description:** Provide multiple high-quality examples (few-shot), but explicitly request variations that maintain the standard while exploring different tones, angles, or framings. This scales quality without cloning.

**Example:** “Here are three example messages that match our tone and clarity standards. Create five new variations that follow the same structure, but vary emotional tone and player motivation.”

**PM Use Case:** When you need multiple versions of the same message - A/B test variants, regional adaptations, or audience-specific rewrites - while keeping quality consistent across all outputs.

**Knowledge Worker Use Case:** Need five different versions of a client rejection email - same professionalism, varying levels of warmth and detail. Maintains brand voice while personalizing to relationship context.

---

### 5. Simulated Debate and Reflection

**Description:** Ask the model to argue multiple conflicting perspectives on a decision, then critique the debate itself and identify what evidence or data would resolve it. This surfaces trade-offs and gaps in your thinking.

**Example:** “Debate this proposal from the perspective of player trust, operational cost, and long-term brand impact. Then critique the strongest argument and explain what evidence would be needed to make a final decision.”

**PM Use Case:** Before a high-stakes decision review, pressure-test the proposal. The AI won't make the call, but it will clarify what you're actually choosing between and what unknowns remain.

**Knowledge Worker Use Case:** Evaluating vendor proposals: debate from cost, quality, and risk perspectives. Then identify what data would break the tie. Clarifies which unknowns actually matter vs. which are noise.

---

### 6. Self-Consistency / Multiple Generations

**Description:** Generate 3-5 independent solutions or answers to the same problem, then compare them to identify the most consistent or synthesize the best elements from each. This reduces hallucinations and improves reasoning quality on complex problems where a single pass might miss nuances.

**Example:** “Generate three different prioritization recommendations for these features. For each, use different reasoning approaches. Then compare the three and synthesize a final recommendation that accounts for what all three surfaced.”

**PM Use Case:** For high-stakes decisions like roadmap prioritization or architecture choices, generate multiple independent analyses and look for convergence. Where they disagree reveals your real uncertainties. Where they agree gives you confidence.

**Knowledge Worker Use Case:** For major hiring decisions, generate 3 separate candidate assessments using different frameworks. Convergence = confidence. Divergence = dig deeper or pass. Reduces bias and prevents rushed judgments.

---

<a id="meta-prompt"></a>

## Meta Prompt

### Prompt Architect

Use this prompt to help improve your prompts!

You are an expert prompt engineer optimizing for correctness, clarity, and controllability. Convert the user’s request into a production-grade prompt.

**Decision rules (non-negotiable):**
1. Ask clarifying questions **only if** missing information would materially change the output. Ask **one at a time**, **max 3 total**. Always provide best-effort even if asking questions
2. If the user wants an immediate result, proceed using best-effort assumptions and label them under **Assumptions**.
3. Never fabricate facts or sources. If facts are required, request them or use explicit placeholders like `[NEEDED: …]`.
4. When uncertain, surface the assumption explicitly rather than silently resolving it.

**Input contract (extract/normalize):**
- Task/action verb, target audience, tone, success criteria
- Required inputs (data, files, links, examples), tools allowed, constraints (length/time/scope), non-goals/out-of-scope
- Ambiguities + their impact (only ask if high impact)

**Output template (always use these headers in this order):**

- **Goal (restated)**
- **Assumptions** (if any)
- **Clarifying Question** (only if needed; otherwise omit)
- **Final Prompt** (copy/paste ready)
- **Variants** (exactly 2: _Shorter_ and _Stricter_)
- **Stress Test** (3-5 edge/adversarial inputs + expected behavior; use 0-2 if the task is trivial)

**Prompt quality checklist (apply as relevant):** role+objective, audience+tone, explicit inputs, constraints (length/tools/sources/safety), output schema, evaluation criteria, edge cases/refusals, examples **only when ambiguity is high**.

**Style:** concise, technical, actionable. Provide brief rationale/tradeoffs; do not provide lengthy step-by-step internal reasoning unless the user asks.
