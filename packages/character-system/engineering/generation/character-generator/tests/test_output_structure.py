import tempfile
import unittest
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_character import is_batch_skipped_config
from extract_style import build_style_values
from validate_pack import validate_pack


def config(max_quote_chars=80):
    return {
        "character_id": "sample-character",
        "display_name": "Sample Character",
        "max_quote_chars": max_quote_chars,
    }


class OutputStructureTest(unittest.TestCase):
    def test_validate_pack_finds_missing_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            ok, issues = validate_pack(Path(tmp), config())
            self.assertFalse(ok)
            self.assertTrue(any("Missing required file" in issue for issue in issues))

    def test_validate_pack_finds_long_quote(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "references").mkdir()
            (root / "reports").mkdir()
            (root / "prompts").mkdir()
            (root / "SKILL.md").write_text(
                "style-inspired impersonation private quote boundary", encoding="utf-8"
            )
            (root / "README.md").write_text("readme", encoding="utf-8")
            (root / "references" / "style_profile.md").write_text(
                '"这是一段明显超过限制的引用文本，用来确认验证器可以发现超长引用问题。"',
                encoding="utf-8",
            )
            ok, issues = validate_pack(root, config(max_quote_chars=10))
            self.assertFalse(ok)
            self.assertTrue(any("Long quote" in issue for issue in issues))

    def test_batch_skips_draft_and_disabled_configs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            draft = root / "writer.draft.json"
            draft.write_text("{}", encoding="utf-8")
            disabled = root / "writer.json"
            disabled.write_text('{"enabled": false}', encoding="utf-8")

            self.assertTrue(is_batch_skipped_config(draft))
            self.assertTrue(is_batch_skipped_config(disabled))

    def test_interaction_scaffold_renders_from_existing_config(self):
        generator_config = {
            "character_id": "sample-character",
            "display_name": "Sample Character",
            "privacy_level": "high",
            "style_strength": "medium",
            "quote_policy": "short_only",
            "max_quote_chars": 80,
            "target_tasks": ["rewrite", "discussion"],
            "forbidden_tasks": ["impersonation", "private_fact_inference"],
        }
        stats = {
            "average_sentence_length": 30,
            "top_chars": [("我", 3)],
            "top_terms": [("memory", 2)],
            "file_count": 1,
            "paragraph_count": 1,
            "sentence_count": 2,
            "total_chars": 40,
        }
        chunks = [{"text": "A concrete memory. A second sentence with uncertainty."}]
        values = build_style_values(generator_config, stats, chunks, {})

        voice = (ROOT / "templates" / "voice_card.template.md").read_text(
            encoding="utf-8"
        ).format(**values)
        profile = (ROOT / "templates" / "style_profile.template.md").read_text(
            encoding="utf-8"
        ).format(**values)
        discussion = (ROOT / "templates" / "prompt_discussion.template.md").read_text(
            encoding="utf-8"
        ).format(**values)

        self.assertIn("Interaction Posture", voice)
        self.assertIn("Inference Discipline", voice)
        self.assertIn("Candidate Domain Fit", profile)
        self.assertIn("candidate domains", profile)
        self.assertIn("context sufficiency", discussion)


if __name__ == "__main__":
    unittest.main()
