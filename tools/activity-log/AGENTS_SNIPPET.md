## Workspace Activity Log

Use `ACTIVITY_LOG.md` and `CONTEXT.md` as local continuity files for substantive multi-session work.

- At session start, read the nearest `CONTEXT.md` when it exists. Fall back to the nearest `ACTIVITY_LOG.md` only when no context snapshot exists or when deeper history is needed.
- Add a narrative milestone when work produces a meaningful decision, reusable workflow, shipped output, or lesson that a future session should be able to reconstruct.
- Use project-specific `ACTIVITY_LOG.md` files as the detailed source of truth for repo or project work. The workspace root `ACTIVITY_LOG.md` is the fallback for broad workspace work and files outside opted-in project folders.
- Do not add secrets, PII, transcripts, or duplicated deliverable content.
- Hooks append a lightweight edited-file trail automatically to the nearest existing `ACTIVITY_LOG.md`. Agent-written notes should capture the reasoning and next step that mechanical logging cannot.
- The shared Stop hook refreshes `CONTEXT.md` beside the chosen log. Treat `CONTEXT.md` as an overwritten session handoff snapshot, not as history.
- New project logs are opt-in. To scaffold one, run `python3 tools/activity-log/activity_logger.py init --path <project-folder>`.
- Record only resources that materially affected the work. Do not inventory every terminal command, passive site visit, or incidental tool call.

Use `tools/activity-log/MILESTONE_TEMPLATE.md` for narrative entries.
