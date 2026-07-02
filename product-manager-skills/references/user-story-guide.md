# User Story Guide

User stories describe independently valuable behavior. They are not containers for every requirement related to an initiative.

## Story Format

```markdown
### <Story ID>: <Story name> (<ticket link or TBD>)

**Priority:** <Critical | High | Medium | Low | TBD>

#### Problem Statement
As a <persona>, I want <capability> so that <benefit>.
<One to three sentences explaining why this matters.>

#### Flow
<Two to four sentences describing the happy-path journey.>

#### Acceptance Criteria
1. Given <context>, when <action>, then <observable outcome>.

#### Out of scope
- <item, only when scope confusion is likely>

#### Missing details
1. <Unresolved requirement stated as a decision needed>

#### Design
<link or TBD>
```

## Story Boundaries

- Organize around user goals and observable outcomes.
- Keep each story independently understandable and testable.
- Split work when behavior, value, or acceptance-criteria ownership differs.
- Do not split by device when only layout changes.
- Give each behavior one owning story; reference dependencies instead of duplicating criteria.
- Create separate cross-cutting stories only when accessibility, localization, analytics, migration, or error handling represents substantial independent work.

## Sequencing

Order stories from foundational to dependent:

1. Core journey or enabling behavior
2. Important alternate and failure paths
3. Cross-cutting or operational work
4. Deferred enhancements

## Priority Guide

- **Critical:** Without it, the initiative does not solve the core problem or cannot launch safely.
- **High:** Important to the outcome, but the core journey can function without it.
- **Medium:** Valuable and intentionally considered, but safely deferrable.
- **Low:** Explicitly later or included mainly to inform current decisions.
- **TBD:** A named decision or missing fact prevents prioritization.

## Quality Checklist

- Does each story deliver or enable a distinct outcome?
- Is the persona specific enough to clarify the need?
- Does the benefit explain value rather than repeat the capability?
- Is the flow plain-language and implementation-free?
- Are acceptance criteria observable and testable?
- Are dependencies explicit without duplicating requirements?
- Are material unknowns visible?
