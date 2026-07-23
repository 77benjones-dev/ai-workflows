import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).parents[1]


class SkillContractTests(unittest.TestCase):
    def test_skill_description_triggers_on_any_youtube_url(self):
        skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        description = skill.split("---", 2)[1]

        self.assertIn("whenever a user message contains any YouTube video URL", description)
        self.assertIn("bare", description)

    def test_report_template_has_all_required_sections(self):
        template = (SKILL_DIR / "references" / "report-template.md").read_text(encoding="utf-8")
        required = [
            "## Bottom Line",
            "## Core Process",
            "## Key Points",
            "## Implementation Details Disclosed",
            "## What Is Missing",
            "## Demonstrated vs. Claimed",
            "## Useful vs. Fluff",
            "## Critique: What's BS",
            "## What to Try",
            "## Notable Timestamps",
        ]

        for heading in required:
            with self.subTest(heading=heading):
                self.assertIn(heading, template)

    def test_skill_uses_public_workspace_placeholders(self):
        skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("<skill-directory>", skill)
        self.assertIn("<workspace>", skill)
        self.assertNotIn("/" + "Users/", skill)
        self.assertNotIn("Library/" + "Mobile Documents", skill)

    def test_skill_documents_compatibility_and_prerequisites(self):
        skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")

        required = [
            "## Compatibility and prerequisites",
            "Python 3.10+",
            "POSIX-compatible shell",
            "internet access",
            "captions",
            "agents/openai.yaml",
        ]

        for text in required:
            with self.subTest(text=text):
                self.assertIn(text, skill)


if __name__ == "__main__":
    unittest.main()
