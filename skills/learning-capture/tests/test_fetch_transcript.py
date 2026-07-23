import importlib.util
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT_PATH = Path(__file__).parents[1] / "scripts" / "fetch_transcript.py"


def load_module():
    spec = importlib.util.spec_from_file_location("fetch_transcript", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class FakeTranscript:
    def __init__(self, language_code, *, generated=False, translatable=True):
        self.language_code = language_code
        self.language = language_code
        self.is_generated = generated
        self.is_translatable = translatable


class FetchTranscriptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()

    def test_extracts_video_id_from_supported_inputs(self):
        cases = {
            "hObRMv6qCi0": "hObRMv6qCi0",
            "https://youtu.be/hObRMv6qCi0?si=test": "hObRMv6qCi0",
            "https://www.youtube.com/watch?v=hObRMv6qCi0&t=30": "hObRMv6qCi0",
            "https://youtube.com/shorts/hObRMv6qCi0": "hObRMv6qCi0",
            "https://www.youtube.com/live/hObRMv6qCi0?feature=share": "hObRMv6qCi0",
        }

        for value, expected in cases.items():
            with self.subTest(value=value):
                self.assertEqual(self.module.extract_video_id(value), expected)

    def test_rejects_invalid_input(self):
        with self.assertRaisesRegex(ValueError, "valid YouTube"):
            self.module.extract_video_id("https://example.com/video")

    def test_prefers_manual_english_then_generated_english(self):
        generated_english = FakeTranscript("en", generated=True)
        manual_spanish = FakeTranscript("es")
        manual_english = FakeTranscript("en-US")

        selected = self.module.select_transcript(
            [generated_english, manual_spanish, manual_english]
        )

        self.assertIs(selected, manual_english)

    def test_falls_back_to_generated_english_then_first_available(self):
        generated_english = FakeTranscript("en", generated=True)
        manual_spanish = FakeTranscript("es")

        self.assertIs(
            self.module.select_transcript([manual_spanish, generated_english]),
            generated_english,
        )
        self.assertIs(
            self.module.select_transcript([manual_spanish]),
            manual_spanish,
        )

    def test_shapes_structured_output(self):
        result = self.module.build_result(
            video_id="hObRMv6qCi0",
            source_url="https://youtu.be/hObRMv6qCi0",
            transcript=FakeTranscript("en", generated=True),
            segments=[
                {"text": "First point", "start": 1.25, "duration": 2.5},
                {"text": "Second point", "start": 5.0, "duration": 1.0},
            ],
            metadata={"title": "Example", "channel": "Channel", "duration": 90},
        )

        self.assertEqual(result["video"]["id"], "hObRMv6qCi0")
        self.assertEqual(result["video"]["title"], "Example")
        self.assertEqual(result["transcript"]["kind"], "auto-generated")
        self.assertEqual(result["transcript"]["segment_count"], 2)
        self.assertEqual(result["transcript"]["segments"][0]["timestamp"], "00:01")
        json.dumps(result)

    def test_empty_transcript_list_has_clear_error(self):
        with self.assertRaisesRegex(RuntimeError, "No captions"):
            self.module.select_transcript([])

    def test_transcript_succeeds_when_metadata_retrieval_fails(self):
        transcript = FakeTranscript("en", generated=True)
        with (
            patch.object(self.module, "get_metadata", side_effect=RuntimeError("metadata failed")),
            patch.object(
                self.module,
                "fetch_with_transcript_api",
                return_value=(transcript, [{"text": "Available", "start": 0, "duration": 1}]),
            ),
        ):
            result = self.module.fetch("hObRMv6qCi0")

        self.assertIsNone(result["video"]["title"])
        self.assertEqual(result["transcript"]["segments"][0]["text"], "Available")


if __name__ == "__main__":
    unittest.main()
