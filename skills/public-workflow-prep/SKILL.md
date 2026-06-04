---
name: public-workflow-prep
description: Use when preparing a skill, prompt, agent instruction, hook, package, or markdown workflow for a public ai-workflows repository, especially when sanitizing personal, client, employer, internal-system, path, credential, or private-project details.
---

# Public Workflow Prep

Prepare reusable AI workflow material for a public `ai-workflows` repository. Preserve the useful workflow, remove private context, use placeholders for specifics, and show the user exactly what changed before finalizing.

## Audience

Assume the target repository is public. A reader may be a recruiter, colleague, or AI-tool user with no access to the original workspace.

Default public-sharing rule:

- No personal names, email addresses, usernames, or local machine paths.
- No client, employer, vendor, customer, or private repository names.
- No internal URLs, Slack workspaces, Jira projects, ticket IDs, dashboards, base IDs, workspace IDs, or system names.
- No credentials, tokens, API keys, secrets, cookies, or private config values.
- No customer, candidate, employee, or user PII.
- Use placeholders such as `[company]`, `[client]`, `[project]`, `[tool]`, `[repo]`, `[ticket]`, `[colleague]`, `user@example.com`, `https://example.com`, `<your-token>`, and `/path/to/workspace`.
- Public product and tool names are fine only when they are generic dependencies or examples, not private context.

## When To Use

Use this skill when the user says things like:

- "generalize this for ai-workflows"
- "make this ready to share publicly"
- "sanitize this skill"
- "copy this prompt into ai-workflows"
- "prepare this workflow for the public repo"

Do not use it for one-off copy editing when there is no public-sharing or sanitization goal.

## Inputs

Resolve the source first:

- Skill name: search likely skill folders in the current workspace and common personal skill locations.
- Explicit path: use the provided file or folder.
- Vague reference: list likely matches and ask only if choosing would risk copying the wrong material.

Resolve the target:

- Skill folder -> `ai-workflows/skills/<skill-name>/`
- Prompt -> `ai-workflows/prompts/<prompt-name>/` or `ai-workflows/prompts/<name>.md`
- Example instruction file -> `ai-workflows/examples/<filename>`
- Package or multi-file workflow -> `ai-workflows/<package-name>/`
- Ambiguous artifact -> ask whether it is a skill, prompt, example, or package before writing.

## Process

1. **Inspect before copying.** Read the source, nearby files, and existing target conventions. Note whether the target already exists.

2. **Make a verbatim staging copy when practical.** For a direct sync, copy source content first, then sanitize that target. For a newly adapted version, keep the original content available for diff comparison. If the target already exists, ask before overwriting existing public material.

3. **Sanitize in place.** Replace private specifics with public-safe placeholders while preserving the workflow's shape.

   Deterministic replacements:

   | Private detail | Public treatment |
   | --- | --- |
   | Personal names, usernames, handles | `[person]`, `[colleague]`, or remove if unnecessary |
   | Email addresses | `user@example.com` |
   | Local paths such as `/Users/<name>/...` or `~/.../<private-folder>` | `/path/to/workspace/...` or `~/path/to/project` |
   | Company, client, employer, team, or org names | `[company]`, `[client]`, `[team]`, or `[organization]` |
   | Private project, repo, codename, roadmap, incident, or initiative names | `[project]`, `[repo]`, or `[initiative]` |
   | Internal systems, domains, dashboards, Slack/Jira/CRM/base URLs | `[tool]`, `https://example.com`, or `[internal-system]` |
   | Ticket IDs and project keys | `[ticket]` or `PROJ-123` |
   | Credentials, tokens, keys, cookies, IDs, base IDs, secrets | `<your-token>` or `<your-secret>` and warn that real secrets should be rotated |
   | Customer, candidate, employee, or user data | Remove or replace with clearly fake sample data |

   Keep tool names such as Codex, Claude Code, GitHub, Vercel, Supabase, Jira, Slack, or Airtable only when they describe a transferable integration pattern rather than a private instance.

4. **Flag uncertain items instead of guessing.** List possible private terms for user review:

   - Capitalized multi-word phrases that look like internal names.
   - Acronyms not clearly public or tool-related.
   - Real-looking IDs, keys, base IDs, ticket IDs, domains, or paths.
   - Named people, teams, clients, employers, and private repositories.
   - Examples that could reveal business strategy, customer behavior, incidents, or confidential process.

5. **Make it reusable.** After sanitization, adjust only what is needed for public usefulness:

   - Replace private assumptions with reader-owned placeholders.
   - Keep examples small and generic.
   - Remove one-person workflow quirks unless they teach a reusable pattern.
   - Keep frontmatter descriptions focused on trigger conditions.
   - Do not add auxiliary docs unless the artifact needs them.

6. **Show the review packet.** Before calling the work done, report:

   - Source path.
   - Target path.
   - Sanitization summary.
   - Flagged items and how they were handled.
   - Diff summary or changed files.
   - Anything intentionally left as a placeholder.

7. **Confirm before external actions.** Do not commit, push, publish, or install the public version unless the user explicitly asks.

## Public Scan Checklist

Before finishing, search changed files for:

- Secret markers: `token`, `secret`, `api_key`, `apikey`, `password`, `bearer`, `cookie`, `private_key`
- Paths: `/Users/`, `~/`, private workspace folder names
- Emails: `@`
- URLs: `http://`, `https://`, private domains
- Tickets or IDs: project-key patterns, long alphanumeric IDs, Airtable-style IDs
- Private nouns: company names, client names, team names, project names, personal names

If a search hit is a safe placeholder or public tool reference, say so briefly.

## Output Template

```text
**Source:** <path>
**Target:** <path>

**Prepared for public sharing**
- Replaced <private detail> with <placeholder>.
- Removed <unnecessary private context>.
- Kept <public tool name> because it is part of the reusable pattern.

**Flagged for review**
- Line <n>: "<term>" - <why it may be private> - <recommendation>

**Verification**
- Searched changed files for secrets, paths, emails, URLs, IDs, and private names.
- Reviewed Markdown/frontmatter readability.

**Next**
- Ready for your review. Not committed or pushed.
```

## Rules

- Preserve the useful workflow. Do not rewrite the artifact into generic advice.
- Prefer placeholders over invented examples.
- Ask before resolving ambiguous private terms.
- Never leave real credentials in place, even in examples.
- Never claim something is public-safe without running a targeted scan.
- Never commit, push, publish, or install without explicit user approval.
