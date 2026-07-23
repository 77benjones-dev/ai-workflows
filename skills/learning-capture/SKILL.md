---
name: learning-capture
description: Use whenever a user message contains any YouTube video URL, including a bare youtube.com, youtu.be, Shorts, live, or embed link, or when the user asks to capture learning, analyze, summarize, critique, or extract a process from a video.
---

# Learning Capture

Turn every shared YouTube video into a durable learning report. Optimize for transferable understanding, not a generic summary.

## Compatibility and prerequisites

The core workflow is not Codex-only. It works with agent runtimes that can load `SKILL.md`, execute local scripts, and write files. The optional `agents/openai.yaml` file provides Codex/OpenAI interface metadata; other runtimes may ignore it. Automatic activation when a YouTube URL is pasted depends on the runtime's skill-discovery behavior.

Required:

- Python 3.10+ with `venv` and `pip`
- a POSIX-compatible shell on macOS or Linux; Windows requires WSL or an equivalent shell environment
- internet access to YouTube and the Python package index
- permission to execute local scripts and write the transcript cache and report
- captions available for the video; this workflow does not download audio or video

The first run installs `youtube-transcript-api` and `yt-dlp` into a skill-local virtual environment.

## Required workflow

For each distinct YouTube video:

1. Retrieve structured metadata and timestamped captions:

```sh
"<skill-directory>/scripts/fetch_transcript.sh" \
  "<youtube-url>" \
  --output "<workspace>/scratch/youtube-learning/<video-id>.json"
```

Resolve `<skill-directory>` to the installed `learning-capture` skill folder. Resolve `<workspace>` to the current project or another user-selected workspace root.

2. Read the transcript. For long videos, inspect it in sections before synthesizing.
3. Analyze using the evidence standards below.
4. Read `references/report-template.md` and create every required section.
5. Save the report to:

```text
<workspace>/artifacts/reports/youtube-learning/YYYY-MM-DD-<concise-video-slug>.md
```

6. Tell the user the bottom line and saved report path.

Create one report per video. Follow additional user instructions, but still save the standard report unless the user explicitly says not to.

## Evidence standards

Do not invent prompts, tools, models, agents, instructions, metrics, implementation details, or evidence. Mark absent details as **undisclosed**.

Classify important claims:

- **Demonstrated:** direct evidence or a concrete example is shown.
- **Explained:** a coherent mechanism is given without direct evidence.
- **Asserted:** stated without meaningful support.
- **Opinion or prediction:** interpretive or future-looking.

Label inferred process steps explicitly. A list of ideas is not automatically a reproducible process.

Use web research only when an unstable, consequential, or suspicious claim needs verification. Cite material external sources in the report.

## Analysis priorities

Extract:

- the core process or workflow, if one exists
- useful and transferable lessons
- named skills, tools, models, agents, instructions, prompts, configurations, and workflows
- missing details needed to reproduce the work
- what is demonstrated versus merely claimed
- high-value sections versus conversation fluff
- practical experiments worth trying

Critique precisely. Use labels such as **unsupported**, **exaggerated**, **misleading**, **contradicted**, or **unverifiable**, followed by the reason. Do not treat disagreement as proof.

Treat repeated points, promotional material, rapport-building, vague inspiration, and anecdotes without a transferable lesson as likely fluff. Preserve conversational context when it clarifies motivation, constraints, or consequences.

## Failure handling

- If captions are unavailable, still save a short report recording the failure and missing analysis.
- If only translated captions are available, state that prominently.
- If metadata fails but captions succeed, continue with known information.
- Do not download video or audio. Ask before proposing an audio-transcription fallback.
