# Product One-Pager Guide

A product one-pager is a decision document, not a compressed requirements specification. It should make the problem, proposed direction, expected outcome, scope, and unresolved risks understandable in one read.

## Canonical Structure

```markdown
# <Initiative>

## Introduction
- **Owner:** <name or TBD>
- **Status:** <Exploring | Shaping | Committed | In progress | Complete>
- **Last updated:** <YYYY-MM-DD>

## Problem
<Who experiences the problem, what happens, and why it matters.>

**Evidence:** <research, observations, or metrics>

**Size of problem:** <number or TBD>

## Proposed Direction
<The proposed experience or approach in one or two paragraphs.>

## Goals and Success Criteria
**Primary objective:** <one outcome>

| Metric | Baseline | Target | Measurement |
| --- | --- | --- | --- |
| <metric> | <value or TBD> | <value or TBD> | <method or TBD> |

## Scope
**In scope**
- <item>

**Out of scope**
- <item>

**Later**
- <item>

## Dependencies and Partner Needs
- <dependency, owner, or required decision>

## Risks and Open Questions
- <risk or question>

## References
- <link or source>
```

## Quality Rules

- Explain the customer or business consequence before the solution.
- Separate observed evidence from assumptions.
- Use concrete language and measurable outcomes.
- Name the primary objective and the tradeoffs.
- Keep detailed implementation requirements outside the one-pager.
- Mark unknowns as `TBD`; never manufacture confidence.
- Include enough scope detail to prevent different readers from imagining different projects.

## Review Checklist

- Is the decision this document supports clear?
- Is the root problem distinct from its symptoms?
- Is the affected audience specific?
- Is the problem sized, or clearly marked for sizing?
- Does the proposed direction address the stated problem?
- Is success measurable?
- Are in-scope, out-of-scope, and later work distinguishable?
- Are dependencies, risks, and open questions visible?
- Are claims supported by evidence or labeled as assumptions?
