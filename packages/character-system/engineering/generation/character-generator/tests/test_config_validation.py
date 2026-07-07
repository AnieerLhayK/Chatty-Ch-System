import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_character import validate_config
from intake_plan import normalize_intake_to_config


def valid_config():
    return {
        "character_id": "sample-character",
        "display_name": "Sample Character",
        "corpus_path": "corpus/sample-character",
        "output_path": "characters/sample-character",
        "language": "zh-CN",
        "privacy_level": "high",
        "style_strength": "medium",
        "target_tasks": ["rewrite", "continuation"],
        "forbidden_tasks": ["impersonation", "private_fact_inference"],
        "quote_policy": "short_only",
        "max_quote_chars": 80,
        "generate_opencode_skill": True,
        "generate_reports": True,
    }


class ConfigValidationTest(unittest.TestCase):
    def test_missing_required_field_fails(self):
        config = valid_config()
        del config["character_id"]
        with self.assertRaisesRegex(ValueError, "character_id"):
            validate_config(config)

    def test_invalid_privacy_level_fails(self):
        config = valid_config()
        config["privacy_level"] = "extreme"
        with self.assertRaisesRegex(ValueError, "privacy_level"):
            validate_config(config)

    def test_enabled_is_optional_but_valid(self):
        config = valid_config()
        config["enabled"] = False
        validate_config(config)

    def test_discussion_is_valid_target_task(self):
        config = valid_config()
        config["target_tasks"].append("discussion")
        validate_config(config)

    def test_legacy_generate_opencode_skill_is_optional(self):
        config = valid_config()
        del config["generate_opencode_skill"]
        validate_config(config)

    def test_corpus_sources_can_replace_legacy_corpus_path(self):
        config = valid_config()
        del config["corpus_path"]
        config["corpus_sources"] = [
            {
                "path": "corpus/sample-character",
                "source_type": "work",
                "role": "long_form_style",
                "include": True,
            }
        ]
        validate_config(config)

    def test_missing_any_corpus_source_fails(self):
        config = valid_config()
        del config["corpus_path"]
        with self.assertRaisesRegex(ValueError, "corpus_path` or `corpus_sources"):
            validate_config(config)

    def test_missing_required_intake_stops_before_config(self):
        with self.assertRaisesRegex(ValueError, "Generation stopped"):
            normalize_intake_to_config({"display_name": "Sample Character"})

    def test_optional_intake_gaps_allow_safe_defaults(self):
        config, optional_missing = normalize_intake_to_config(
            {
                "display_name": "Sample Character",
                "corpus_sources": [{"path": "corpus/sample-character"}],
                "authorization_confirmed": True,
                "privacy_boundary_accepted": True,
                "target_tasks": ["discussion"],
            }
        )
        self.assertEqual(config["character_id"], "Sample-Character")
        self.assertEqual(config["privacy_level"], "high")
        self.assertIn("personal profile", optional_missing[0])

    def test_conversational_target_type_maps_to_supported_task(self):
        config, _optional_missing = normalize_intake_to_config(
            {
                "display_name": "Sample Character",
                "corpus_sources": [{"path": "corpus/sample-character"}],
                "authorization_confirmed": True,
                "privacy_boundary_accepted": True,
                "target_interaction_type": "friend chat and writing collaborator",
            }
        )
        self.assertEqual(config["target_tasks"], ["discussion"])


if __name__ == "__main__":
    unittest.main()
