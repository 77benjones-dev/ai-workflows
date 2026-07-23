# Product Manager Workflows

Reusable AI skills and reference guides for turning an early product idea into a decision-ready one-pager, a coherent story set, testable acceptance criteria, and focused investigation tickets.

## Included Skills

- `skills/jira-create/` - Creates Jira issues from structured markdown stories with wiki-markup conversion, field mapping, and update safeguards.
- `skills/onepager-deep-prep/` - Runs a staged prep workflow for rough ideas, including research, skeleton drafting, reviewer feedback, open questions, and risks.
- `skills/product-onepager/` - Frames and reviews product one-pagers.
- `skills/user-story-generator/` - Breaks initiatives into sequenced user stories and progressively adds detail.
- `skills/spike-ticket-generator/` - Drafts investigation tickets for technical unknowns.

## Included References

- `references/one-pager-guide.md` - Canonical one-pager structure and review checklist.
- `references/user-story-guide.md` - Story format, boundaries, sequencing, and priority guidance.
- `references/acceptance-criteria-guide.md` - Rules for observable, testable acceptance criteria.

## Examples

- `examples/example-one-pager.md`
- `examples/example-user-stories.md`

## Installation

Copy or symlink each folder under `skills/` into the skills directory used by your AI coding or work assistant. Keep the `references/` folder two levels above each `SKILL.md`, or update the relative reference paths after installation.

Most workflows produce Markdown that can be reviewed before anyone creates or updates external records. The Jira create skill is the exception: it is intended for workspaces where the agent has an explicit Jira integration available.

## Design Principles

- Start with the decision and problem, not the proposed feature.
- Separate known evidence, assumptions, and unresolved questions.
- Expand detail progressively instead of generating every artifact at once.
- Treat technical uncertainty as investigation work.
- Never invent metrics, commitments, owners, designs, or ticket IDs.
