---
name: user-story-generator
description: Turn a product brief or feature idea into a coherent, prioritized set of user stories, then progressively add testable acceptance criteria. Use when listing stories, refining story boundaries, reviewing scope, or preparing stories for a ticketing system.
---

# User Story Generator

Create user stories that are understandable, independently valuable, and ready for product and engineering review.

## References

Read:

- `../../references/user-story-guide.md`
- `../../references/acceptance-criteria-guide.md` before writing full acceptance criteria

## Modes

### Single Story

Use when the user provides one capability or narrowly scoped need. Produce one story with a problem statement, flow, priority, acceptance criteria, and unresolved details.

### Cohesive Story Set

Use when the user provides a one-pager, brief, or initiative. Work in stages:

1. **List:** propose a sequenced story list with one-line descriptions.
2. **Review:** identify missing journeys, overlap, scope problems, and dependencies.
3. **Flesh out:** add full detail only to stories selected by the user.
4. **Final review:** check acceptance-criteria ownership, testability, and cross-cutting concerns.

Do not generate full acceptance criteria for every candidate story before the user confirms the story list.

## Workflow

1. Identify the source material and intended outcome.
2. Extract the core user journeys.
3. Separate distinct behaviors into independently deliverable stories.
4. Add cross-cutting stories only when they represent meaningful work.
5. Sequence foundational stories before dependent stories.
6. Assign priority using impact, necessity, and dependency rather than politeness.
7. Flag technical unknowns that require investigation as spike candidates.
8. Preserve existing story IDs, links, and confirmed content when revising a file.

## Guardrails

- Do not invent requirements, designs, metrics, or ticket IDs.
- Do not split stories by device unless behavior differs.
- Do not duplicate the same outcome across multiple stories.
- Keep implementation details out of customer-facing acceptance criteria.
- Put materially unresolved requirements under `Missing details`.
- Treat technical uncertainty as a spike, not vague acceptance criteria.
- Never create or update tickets unless the user explicitly requests it.

## Output

Follow the formats in `user-story-guide.md`. When saving, use the existing story file if one is available; otherwise default to `user-stories.md`.
