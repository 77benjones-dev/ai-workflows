---
name: onepager-deep-prep
description: Orchestrate a multi-stage prep pass for a product one-pager from a rough seed. Use when a product manager wants visible research, a skeletal one-pager, reviewer feedback, open questions, and a concise risk register before polishing the brief.
---

# One-Pager Deep Prep

Run a staged preparation workflow for an early product idea. The goal is not to produce a finished one-pager in one pass. The goal is to create a useful skeleton, expose the evidence and uncertainty behind it, and give the product manager a short list of decisions to resolve.

## References

Read before drafting:

- `../../references/one-pager-guide.md`

Use these when the one-pager will feed delivery planning:

- `../../references/user-story-guide.md`
- `../../references/acceptance-criteria-guide.md`

## Inputs

Resolve these from the user's request:

- **Seed:** a pasted idea, note, request, meeting summary, support thread, customer quote, brief, or path to a source file.
- **Project folder:** a folder where the two outputs should be saved.
- **Topic slug:** a short kebab-case name for the output files.

Ask only when a wrong assumption would create the wrong project or write files in the wrong place.

## Outputs

Create exactly two final files:

1. `<project-folder>/<topic-slug>-onepager.md`
   - Skeletal one-pager.
   - Inline `[ASSUMPTION: ...]` markers.
   - Inline `**TBD** ...` markers.
   - Mechanical fixes applied.
   - Suggested edits.
   - Open questions grouped by priority.

2. `<project-folder>/<topic-slug>-onepager-research.md`
   - Research synthesis.
   - Source coverage and skipped sources.
   - Reviewer panel output.
   - Consolidated themes.
   - Short risk register.

Use a temporary `.research/` folder only while working. Delete it after both final files are complete unless the user asks to keep intermediate files.

## Ground Rules

- Never invent metrics, owners, deadlines, commitments, source findings, or ticket IDs.
- Label weak inferences as assumptions.
- Mark unresolved decisions as `TBD`.
- Keep implementation detail out of the one-pager unless it changes product scope, cost, risk, or feasibility.
- Treat failed or skipped research as unknown, not as "nothing found."
- Preserve the user's terminology when it is clear and public-safe.
- Keep the final answer short. Point to the two files instead of pasting them.

## Stage 0: Resolve The Work

Confirm or infer:

- Seed source.
- Project folder.
- Topic slug.
- Whether the user wants optional research sources included.

Create the project folder if needed. Do not scaffold a full project workspace here. Use the `new-project` skill for that.

Read the seed and identify:

- The likely customer or operator.
- The problem being solved.
- The proposed direction.
- Known evidence.
- Missing evidence.
- Likely dependencies.
- Any delivery or technical unknowns.

Stop if the seed is empty or unreadable.

## Stage 1: Research Fan-Out

Use only research sources the user has authorized or that are already available in the workspace.

Possible research legs:

- **Workspace research:** local notes, prior briefs, research summaries, roadmaps, specs, or related project folders.
- **Ticketing research:** related epics, issues, bugs, spikes, or support tickets.
- **Conversation research:** Slack, Teams, email, meeting notes, or decision logs.
- **Document research:** shared docs, decks, spreadsheets, or requirements repositories.
- **Customer or market research:** interviews, surveys, public benchmarks, competitor examples, policy changes, or industry shifts.
- **Analytics research:** dashboards, event docs, funnel reports, or experiment results.

Before running a source-specific leg:

- Check whether the relevant connector, credential, or local access exists.
- Skip unavailable sources and record the reason.
- Seed each leg with known anchors from the project folder, such as document links, ticket IDs, channel names, or source filenames.

Write each successful leg to `<project-folder>/.research/<source>.md`.

Each research note should include:

- Search terms or source scope.
- Key findings.
- Evidence quality.
- Useful links or file paths.
- Open questions.
- Any source failures or access gaps.

After research returns, summarize skipped or failed sources in a separate "Research that did not complete" block. A failed search is unknown, not evidence of absence.

## Stage 2: Draft The Skeleton

Draft `<topic-slug>-onepager.md` using the canonical structure in `../../references/one-pager-guide.md`.

Top of file:

```markdown
# <One-Pager Title>

_Status: Skeleton, drafted by onepager-deep-prep._
_Source seed: <path or short description>_
_Generated: YYYY-MM-DD_
```

Fill every relevant section with best-effort content from the seed and research. Keep the draft honest:

- Use `[ASSUMPTION: ...]` for inferred claims.
- Use `**TBD** ...` for missing facts or decisions.
- Cite local paths, URLs, or source names where claims depend on research.
- Omit sections only when the reference guide says they are optional or irrelevant.

## Stage 3: Reviewer Panel

Run a reviewer panel against the skeleton. Use real named personas only if the user supplied them. Otherwise use role-based reviewers.

Default panel:

| Reviewer | Lens |
| --- | --- |
| Product leader | Strategic fit, priority, tradeoffs, decision readiness |
| Engineering lead | Feasibility, dependencies, sequencing, hidden delivery risk |
| Designer or UX lead | Journey clarity, usability, content, edge states |
| Data or analytics partner | Measurability, baselines, success criteria, instrumentation |

Add conditional reviewers when relevant:

- **Support or operations:** support cost, escalation paths, handoffs, operational readiness.
- **Legal, privacy, or compliance:** consent, data handling, regulated flows, policy exposure.
- **Content or SEO:** information architecture, discoverability, page templates, publishing workflow.
- **Security:** authentication, authorization, abuse risk, sensitive data.

Write the full panel output to `<project-folder>/.research/reviewer-panel.md`.

For each reviewer include:

- Lens.
- Three to six concerns tied to skeleton sections.
- Two to four questions.
- One or two strengths, if present.

Keep each reviewer section short enough to act on.

## Stage 4: Apply Mechanical Fixes

Read the panel output and sort feedback into three buckets.

**Mechanical fixes:** apply directly to the skeleton only when the fix is unambiguous and introduces no new facts. Examples:

- Correcting terminology drift.
- Adding a reference already present in the seed.
- Fixing heading order.
- Moving a delivery milestone out of a problem section.
- Replacing unsupported certainty with `TBD`.

Log each fix in the skeleton:

```markdown
## Mechanical fixes applied

- <What changed>. _Surfaced by:_ <reviewer>.
```

**Suggested edits:** propose, but do not apply, when the edit needs product judgment. Cap at five.

```markdown
## Suggested edits

1. **Suggest:** <specific text or section change>.
   _Reason:_ <reviewer and concern>.
```

**Open questions:** carry into Stage 5 when the user must supply a fact, decision, owner, date, metric, constraint, or tradeoff.

## Stage 5: Add Open Questions And Research File

Append open questions to the skeleton:

```markdown
## Open questions

### Critical
1. **<Question>.** _Why it matters:_ <one line>. _Maps to:_ <section, TBD, assumption, or research finding>.

### Important
1. ...

### Nice-to-have
1. ...
```

Question rules:

- Make each answerable in one or two sentences.
- Tie each question to a `TBD`, assumption, research finding, or reviewer concern.
- Rank by whether the one-pager can move forward without the answer.

Write `<topic-slug>-onepager-research.md`:

```markdown
---
generated: YYYY-MM-DD
seed: <path or short description>
skeleton: <path>
status: complete | partial
---

# Research: <One-Pager Title>

## Verdict
<Two to three sentences on whether the idea is ready to shape further.>

## Research coverage
- <Source>: <completed, skipped, or failed, plus reason>

## Findings
<Synthesis from completed sources, with references.>

## Reviewer panel
<Panel output or concise transcript.>

## Consolidated themes
- <Theme raised by multiple sources or reviewers>

## Risks
- **<Risk theme>.** <One clause>. _Likelihood:_ High | Medium | Low. _Impact:_ High | Medium | Low.
```

Cap the risk register at five items.

## Stage 6: Clean Up And Return

Delete the temporary `.research/` folder unless the user asked to keep it.

Return:

1. One-line verdict.
2. Skeleton path.
3. Research path.
4. Count of critical questions and one example.
5. Top risk theme.
6. Research coverage headline.
7. Suggested next step.

Do not paste the full skeleton or research file into chat.

## Why This Is Staged

The stages make the work inspectable. The product manager can pause after research, edit the skeleton before review, or re-run a single stage without losing the whole chain of reasoning.
