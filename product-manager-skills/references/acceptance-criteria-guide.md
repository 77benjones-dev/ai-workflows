# Acceptance Criteria Guide

Acceptance criteria define observable behavior and boundaries. They should help product, engineering, design, and QA agree on what completion means.

## Default Format

Use one scenario per numbered line:

```text
1. Given <context>, when <action>, then <observable outcome>.
```

Use a named subject in the Given clause. Once named, pronouns are acceptable in the When and Then clauses.

## Ordering

When relevant, order scenarios as:

1. Happy path
2. Common alternate path
3. Important eligibility or permission state
4. Recoverable failure
5. Measurement or compliance behavior

Do not add categories that are irrelevant to the story.

## Rules

- Describe what a person can do, see, receive, or understand.
- Keep implementation details out of feature-story criteria.
- Use one Given, one When, and one Then per scenario unless a compound condition is necessary.
- Keep assumptions outside the numbered acceptance-criteria list.
- Put unresolved material decisions under `Missing details`.
- Do not disguise unanswered questions as acceptance criteria.
- Avoid duplicate outcomes across stories.

## Assumptions

Use at most three small, non-critical assumptions:

```text
Assumptions:
- <assumption>
```

If changing the assumption would materially change the feature, move it to `Missing details`.

## Missing Details

State the decision needed rather than asking a conversational question:

```text
Missing details:
1. Confirm whether saved items require an account.
```

## Examples

Good:

```text
1. Given a customer has completed every required field, when they submit the form, then they see confirmation that the request was received.
2. Given a customer leaves a required field empty, when they submit the form, then they see which field needs attention and how to correct it.
```

Avoid:

```text
1. Given the API returns 200, when the database write completes, then the event is emitted.
2. Given the feature works correctly, when the user clicks it, then it succeeds.
```

## Quality Checklist

- Is every outcome observable or operationally verifiable?
- Does each line cover one scenario?
- Are important recovery states represented?
- Are unnecessary edge cases excluded?
- Are assumptions and missing decisions separated?
- Could a reviewer determine whether each scenario passed?
