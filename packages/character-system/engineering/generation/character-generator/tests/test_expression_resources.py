"""Behavioral invariants of the bundled content, not generated prose matching."""
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from expression_resource import generator_reference, read_reference, bundle_reference
from validate_pack import validate_pack


class ExpressionResourceTests(unittest.TestCase):
    def test_standalone_generator_uses_only_bundled_reference(self):
        content = generator_reference(ROOT)
        with tempfile.TemporaryDirectory() as temp:
            isolated = Path(temp) / "generator"
            target = isolated / "references/shared-expression.md"
            target.parent.mkdir(parents=True)
            target.write_bytes(content)
            self.assertEqual(generator_reference(isolated), content)
            target.unlink()
            with self.assertRaises(FileNotFoundError):
                generator_reference(isolated)

    def test_bundle_localizes_pointer_and_preserves_exact_bytes(self):
        content = generator_reference(ROOT)
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)
            skill = output / "SKILL.md"
            skill.write_text("# Test\n[rules](../../skills/content/speaking-like-a-man/references/shared-expression.md)\n", encoding="utf-8")
            template = output / "templates/character_SKILL.template.md"
            template.parent.mkdir()
            template.write_text("# Template\n[rules](../../skills/content/speaking-like-a-man/references/shared-expression.md)\n", encoding="utf-8")
            bundle_reference(output, content)
            self.assertEqual((output / "references/shared-expression.md").read_bytes(), content)
            self.assertEqual(skill.read_text(encoding="utf-8"), "# Test\n[rules](references/shared-expression.md)\n")
            bundle_reference(output, content)
            self.assertNotIn("skills/content/", skill.read_text(encoding="utf-8"))
            self.assertIn("](../references/shared-expression.md)", template.read_text(encoding="utf-8"))
            generated = output / "new-character"
            generated.mkdir()
            (generated / "SKILL.md").write_text(template.read_text(encoding="utf-8"), encoding="utf-8")
            bundle_reference(generated, content)
            self.assertEqual((generated / "references/shared-expression.md").read_bytes(), content)
            self.assertIn("](references/shared-expression.md)", (generated / "SKILL.md").read_text(encoding="utf-8"))

    def test_undeclared_pointer_stops_bundling(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)
            (output / "SKILL.md").write_text("# No resource pointer\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                bundle_reference(output, b"# Rules\n")

    def test_empty_reference_stops_build_input(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)
            (output / "rules.md").write_text(" \n", encoding="utf-8")
            with self.assertRaises(ValueError):
                read_reference(output, "rules.md")

    def test_pack_validator_rejects_missing_and_changed_shared_rules(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)
            _, issues = validate_pack(output, {"max_quote_chars": 80})
            self.assertIn("Missing required file: references/shared-expression.md", issues)
            (output / "references").mkdir()
            (output / "references/shared-expression.md").write_text("Changed rules\n", encoding="utf-8")
            _, issues = validate_pack(output, {"max_quote_chars": 80})
            self.assertIn("Shared expression resource differs from the generator source.", issues)
