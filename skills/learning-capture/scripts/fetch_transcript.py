#!/usr/bin/env python3
import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path
from urllib.parse import parse_qs, urlparse


VIDEO_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{11}$")


def extract_video_id(value):
    value = value.strip()
    if VIDEO_ID_PATTERN.fullmatch(value):
        return value

    parsed = urlparse(value)
    host = parsed.netloc.lower().removeprefix("www.")

    if host == "youtu.be":
        candidate = parsed.path.strip("/").split("/")[0]
    elif host in {"youtube.com", "m.youtube.com", "music.youtube.com"}:
        if parsed.path == "/watch":
            candidate = parse_qs(parsed.query).get("v", [""])[0]
        else:
            parts = parsed.path.strip("/").split("/")
            candidate = parts[1] if len(parts) > 1 and parts[0] in {"shorts", "live", "embed"} else ""
    else:
        candidate = ""

    if not VIDEO_ID_PATTERN.fullmatch(candidate):
        raise ValueError(f"Not a valid YouTube video URL or ID: {value}")
    return candidate


def select_transcript(transcripts):
    transcripts = list(transcripts)
    if not transcripts:
        raise RuntimeError("No captions are available for this video.")

    def rank(transcript):
        language = transcript.language_code.lower()
        english = language == "en" or language.startswith("en-")
        return (
            0 if english and not transcript.is_generated else
            1 if english else
            2 if not transcript.is_generated else
            3
        )

    return min(transcripts, key=rank)


def format_timestamp(seconds):
    total = max(0, int(float(seconds)))
    hours, remainder = divmod(total, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def normalize_segments(segments):
    normalized = []
    for segment in segments:
        if hasattr(segment, "text"):
            text = segment.text
            start = segment.start
            duration = segment.duration
        else:
            text = segment.get("text", "")
            start = segment.get("start", 0)
            duration = segment.get("duration", 0)
        text = " ".join(str(text).split())
        if text:
            normalized.append(
                {
                    "start": round(float(start), 3),
                    "duration": round(float(duration), 3),
                    "timestamp": format_timestamp(start),
                    "text": text,
                }
            )
    return normalized


def build_result(*, video_id, source_url, transcript, segments, metadata):
    normalized = normalize_segments(segments)
    upload_date = metadata.get("upload_date")
    if upload_date and len(upload_date) == 8:
        upload_date = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:]}"

    return {
        "video": {
            "id": video_id,
            "url": metadata.get("webpage_url") or f"https://www.youtube.com/watch?v={video_id}",
            "source_url": source_url,
            "title": metadata.get("title"),
            "channel": metadata.get("channel") or metadata.get("uploader"),
            "upload_date": upload_date,
            "duration_seconds": metadata.get("duration"),
        },
        "transcript": {
            "language": transcript.language,
            "language_code": transcript.language_code,
            "kind": "auto-generated" if transcript.is_generated else "manual",
            "is_translatable": bool(transcript.is_translatable),
            "segment_count": len(normalized),
            "segments": normalized,
        },
    }


def get_metadata(video_url):
    try:
        from yt_dlp import YoutubeDL
    except ImportError:
        return {}

    options = {"quiet": True, "no_warnings": True, "skip_download": True}
    with YoutubeDL(options) as ydl:
        return ydl.extract_info(video_url, download=False)


def fetch_with_transcript_api(video_id):
    from youtube_transcript_api import YouTubeTranscriptApi

    api = YouTubeTranscriptApi()
    transcript = select_transcript(api.list(video_id))
    return transcript, transcript.fetch()


class FallbackTranscript:
    def __init__(self, language_code, *, generated):
        self.language_code = language_code
        self.language = language_code
        self.is_generated = generated
        self.is_translatable = False


def fetch_with_ytdlp(metadata):
    choices = []
    for generated, group_name in ((False, "subtitles"), (True, "automatic_captions")):
        for language, formats in (metadata.get(group_name) or {}).items():
            json3 = next((item for item in formats if item.get("ext") == "json3"), None)
            if json3:
                english = language in {"en", "en-orig"} or language.startswith("en-")
                choices.append((0 if english and not generated else 1 if english else 2, generated, language, json3["url"]))

    if not choices:
        raise RuntimeError("No captions are available for this video.")

    _, generated, language, url = min(choices, key=lambda item: item[0])
    with urllib.request.urlopen(url) as response:
        payload = json.load(response)

    segments = []
    for event in payload.get("events", []):
        text = "".join(part.get("utf8", "") for part in event.get("segs", []))
        if text.strip():
            segments.append(
                {
                    "text": text,
                    "start": event.get("tStartMs", 0) / 1000,
                    "duration": event.get("dDurationMs", 0) / 1000,
                }
            )
    return FallbackTranscript(language, generated=generated), segments


def fetch(value):
    video_id = extract_video_id(value)
    canonical_url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        metadata = get_metadata(canonical_url)
    except Exception:
        # Captions are the required artifact; metadata enrichment must not block them.
        metadata = {}

    try:
        transcript, segments = fetch_with_transcript_api(video_id)
    except Exception as primary_error:
        # YouTube changes caption endpoints frequently; yt-dlp provides an independent fallback.
        try:
            transcript, segments = fetch_with_ytdlp(metadata)
        except Exception as fallback_error:
            raise RuntimeError(
                f"Transcript retrieval failed. Primary: {primary_error}. Fallback: {fallback_error}"
            ) from fallback_error

    return build_result(
        video_id=video_id,
        source_url=value,
        transcript=transcript,
        segments=segments,
        metadata=metadata,
    )


def main():
    parser = argparse.ArgumentParser(description="Fetch structured YouTube transcript data.")
    parser.add_argument("youtube_url_or_id")
    parser.add_argument("--output", type=Path, help="Write JSON to this path instead of stdout.")
    args = parser.parse_args()

    try:
        result = fetch(args.youtube_url_or_id)
    except Exception as error:
        print(str(error), file=sys.stderr)
        return 1

    payload = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8")
        print(args.output)
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
