---
name: spike-ticket-generator
description: Draft investigation tickets for technical unknowns or audit a product brief for questions engineering must answer before implementation stories can be completed.
---

# Spike Ticket Generator

Create focused investigation tickets that reduce uncertainty and lead to a decision.

## Modes

### Draft One Spike

Use when the user already knows the uncertainty to investigate.

Gather only missing information:

- Why the investigation matters now
- The decision it must support
- Questions that remain unanswered
- Expected outputs or decisions
- Relevant constraints, dependencies, and supporting links
- Explicitly excluded work

### Audit A Brief

Use when the user provides a one-pager, PRD, or story set. Identify technical unknowns that materially block scoping, architecture, sequencing, estimation, or acceptance criteria.

Do not turn every implementation detail into a spike. Recommend a spike only when answering the question changes the plan or meaningfully reduces delivery risk.

## Output Format

```markdown
### [Spike] <Investigation topic>

**Priority:** <Critical | High | Medium | Low | TBD>

#### Problem Statement
<Why this uncertainty matters and what decision it blocks.>

#### Questions to investigate
- <Question>
- <Question>

#### Expected outcome
- <Recommendation, decision, rule, prototype finding, or documented constraint>

#### Out of scope
- <Implementation or adjacent question not included>

#### Supporting context
- <Link or reference, when available>
```

## Guardrails

- Phrase technical direction as areas to investigate, not implementation orders.
- Describe expected content, not the required document or tool used to deliver it.
- Do not ask for effort estimates as the spike's primary output.
- Do not invent systems, constraints, owners, or ticket IDs.
- Keep each spike centered on one decision area.
- Never create a ticket unless the user explicitly requests it.
