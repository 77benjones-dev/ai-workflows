---
name: jira-create
description: Use when creating Jira issues from structured markdown stories, especially when converting user stories, acceptance criteria, priorities, issue types, labels, custom fields, and Jira wiki markup into a REST API payload.
---

# Jira Create

Create Jira issues from structured markdown. This skill is designed for teams that draft user stories in markdown, then push them into Jira with consistent fields and wiki-markup formatting.

## Setup Assumptions

Replace the placeholders below with your Jira instance values before using this skill:

- **Server:** `https://jira.example.com`
- **Project key:** `PROJ`
- **Token variable:** `JIRA_BEARER_TOKEN`
- **Default assignee:** omit unless the user explicitly provides one
- **Custom fields:** replace `customfield_00000` and `customfield_11111` with your instance-specific IDs

Do not hardcode credentials in this skill. Read tokens from the environment and pass them via the `Authorization` header.

## Upstream Handoff

When the user provides a structured user story, expect this shape:

```markdown
### [CODE]-[##]: [Story Name] ([JIRA-KEY](https://jira.example.com/browse/JIRA-KEY))

**Priority**: [1 - Critical / 2 - High / 3 - Medium / 4 - Low / Not Prioritized]

#### Problem Statement
As a [persona], I want [goal] so that [benefit].
[1-3 sentences on the why.]

#### Flow
[2-4 sentences of narrative prose.]

#### Acceptance Criteria

1. Given [context], when [action], then [outcome].
2. Given [context], when [action], then [outcome].

#### Missing details
*(if present)*
1. [Statement]
```

Map to Jira fields:

- Heading -> `summary`; strip the heading prefix, story code prefix, trailing ticket link or `(TBD)`, and status markers.
- Priority -> `priority.name`; use exact Jira priority names.
- `####` sections and bodies -> `description`; convert markdown to Jira wiki markup.

## Markdown To Wiki Markup

Convert only the description body. The story heading becomes the Jira summary and should not appear in the description.

| Markdown | Jira wiki markup |
| --- | --- |
| `#### Problem Statement` | `h3. Problem Statement` |
| `#### Flow` | `h3. Flow` |
| `#### Acceptance Criteria` | `h3. Acceptance Criteria` |
| `#### Missing details` | `h3. Missing details` |
| `#### Out of scope` | `h3. Out of scope` |
| `#### Design` | `h3. Design` |
| `**bold**` | `*bold*` |
| `1. item` | `# item` |
| `- item` | `* item` |
| `[text](url)` | `[text\|url]` |
| `` `code` `` | `{{code}}` |
| Blank lines | preserve blank lines |

Do not convert:

- The story heading. Use it for `summary`.
- Legacy inline placeholders such as `**Design**: TBD`; strip them unless they contain a real link or useful detail.
- Emoji or text status markers in the heading; strip them before creating the summary.

## Priority Mapping

Pass exact priority names to `priority.name`.

Common values:

- `1 - Critical`
- `2 - High`
- `3 - Medium`
- `4 - Low`
- `Not Prioritized`

When the user says "2-high" or "priority 2", use `"2 - High"`.

## Issue Type Selection

Default to `Story` for user-story-shaped input. Infer `Analysis` when the work is investigative or scoping rather than implementation.

Use `Analysis` when any of these are true:

- Title contains `[Analysis]`, `Analysis:`, `Spike:`, `Investigation:`, `Discovery:`, `Research:`, or `Evaluation:`.
- Story code suffix hints at analysis, such as `-00`, `ANL-`, or `SPK-`.
- Problem statement is phrased as "As an engineering team, I want to analyze / evaluate / assess / design / recommend an approach..."
- Scope lists investigation verbs such as evaluate, assess, define, confirm, recommend, or design approach, with no concrete user-facing outcome.
- Acceptance criteria describes a deliverable document, recommendation, or technical decision instead of observable user behavior.

Otherwise use `Story` for user-facing or system-facing implementation work with testable acceptance criteria.

Other common issue types: `Bug`, `Task`, `Epic`, `Subtask`. Use these only when the user explicitly asks.

When in doubt, ask. Do not silently pick `Analysis` if the signal is mixed.

## Creating An Issue

Use Jira REST API v2 unless your instance requires another version.

```bash
curl -s -X POST 'https://jira.example.com/rest/api/2/issue' \
  -H "Authorization: Bearer $JIRA_BEARER_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "fields": {
      "project": {"key": "PROJ"},
      "issuetype": {"name": "Story"},
      "summary": "Issue title here",
      "description": "Optional description",
      "priority": {"name": "2 - High"},
      "labels": ["example-label"],
      "customfield_00000": "PROJ-100",
      "customfield_11111": ["example-system"]
    }
  }'
```

Required fields:

- `project.key`
- `issuetype.name`
- `summary`

Optional fields:

- `description`
- `priority.name`
- `labels`
- instance-specific custom fields such as epic link, component, system, team, or initiative
- `assignee`, only when the user explicitly provides a value

## Formatting Conventions

Jira wiki markup is not markdown. Use these conventions when building `description`:

- Headers: `h3. Header Name`
- Bold text: `*text*`
- Links: `[text|url]`
- Inline code and technical terms: `{{text}}`
- Bullets: `* item`
- Numbered lists: `# item`
- Code blocks: `{code}...{code}` or `{noformat}...{noformat}`
- Mentions: use the format your Jira instance supports; avoid inserting real user identifiers unless the user provided them for this ticket

## Workflow

When the user requests issue creation:

1. Parse the request for issue type, summary, description, priority, labels, and optional fields.
2. Detect whether input matches the structured markdown story format.
3. Convert markdown story sections to Jira wiki markup.
4. Map priority to an exact Jira priority name.
5. Infer issue type, asking when mixed signals make the type ambiguous.
6. Build a JSON payload containing only provided or defaulted fields.
7. POST to `/rest/api/2/issue`.
8. Check HTTP status; treat `201` as success and `400` as validation failure.
9. Return the created issue key and URL.
10. If the source came from a markdown story file, update the last-synced snapshot only after every requested create or push succeeds.

## Last-Synced Snapshot

After a successful create or push from a markdown story file, overwrite a sibling snapshot file so the user can diff in-flight edits against the last state synced to Jira.

Rules:

- Filename: same directory as the source, same basename with `.lastsynced.md` appended. Example: `Product_Stories.md` -> `Product_Stories.lastsynced.md`.
- Write only after every attempted story succeeds.
- Do not write if any create or update fails. Leave the snapshot untouched and warn the user.
- Contents must be a verbatim copy of the source file at the moment of push.
- Skip snapshots for inline pasted stories because there is no source file to mirror.

Use a simple file copy. Do not regenerate the snapshot from parsed data, because the snapshot must match the source byte-for-byte.

## Worked Example

Input:

```markdown
### PAY-01: Customer sees payment status on account page (TBD)

**Priority**: 2 - High

#### Problem Statement
As a customer, I want to see whether my payment is complete so that I know if I need to take another action.

#### Flow
A customer opens the account page after submitting a payment. The page shows a clear payment status and next step.

#### Acceptance Criteria

1. Given a customer has submitted a payment, when the account page loads, then the current payment status is shown.
2. Given a payment needs attention, when the customer views the status, then the page shows the next action.

#### Missing details
1. Confirm the final status labels with the product team.
```

Description payload:

```text
h3. Problem Statement
As a customer, I want to see whether my payment is complete so that I know if I need to take another action.

h3. Flow
A customer opens the account page after submitting a payment. The page shows a clear payment status and next step.

h3. Acceptance Criteria
# Given a customer has submitted a payment, when the account page loads, then the current payment status is shown.
# Given a payment needs attention, when the customer views the status, then the page shows the next action.

h3. Missing details
# Confirm the final status labels with the product team.
```

Derived fields:

- `summary`: `Customer sees payment status on account page`
- `priority.name`: `2 - High`
- `issuetype.name`: `Story`

## Notes

- Jira Cloud and Jira Server/Data Center may differ in authentication, account IDs, API version, wiki markup support, and custom field behavior. Check the target instance before mutating real issues.
- Custom fields are instance-specific. Discover field IDs before using this skill on a new Jira instance.
- Assignee fields are especially instance-dependent. Prefer leaving tickets unassigned unless the user explicitly asks and provides the right identifier.
- This skill works well when paired with /user-story-generator
