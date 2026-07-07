import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_character
from build_character import write_corpus_reading_handoff, write_source_readmes
from ingest_corpus import ingest_corpus


def base_config(*sources):
    return {
        "character_id": "sample-character",
        "display_name": "Sample Character",
        "output_path": "characters/sample-character",
        "language": "zh-CN",
        "privacy_level": "high",
        "style_strength": "medium",
        "target_tasks": ["discussion"],
        "forbidden_tasks": ["impersonation", "private_fact_inference"],
        "quote_policy": "short_only",
        "max_quote_chars": 80,
        "generate_reports": True,
        "corpus_sources": list(sources),
    }


class CorpusPlanningTest(unittest.TestCase):
    def test_multi_source_ingests_all_explicit_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            one = root / "work"
            two = root / "chat"
            one.mkdir()
            two.mkdir()
            (one / "a.md").write_text("第一份材料。\n\n有一点长句。", encoding="utf-8")
            (two / "b.txt").write_text("第二份材料。\n\n口语一点。", encoding="utf-8")

            docs = ingest_corpus(
                base_config(
                    {"source_id": "work", "path": str(one), "explicit": True},
                    {"source_id": "chat", "path": str(two), "explicit": True},
                ),
                ROOT,
            )

            self.assertEqual(len(docs), 2)
            self.assertEqual({doc["source_id"] for doc in docs}, {"work", "chat"})

    def test_absolute_path_requires_explicit_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp)
            (source / "a.txt").write_text("authorized text", encoding="utf-8")
            config = base_config({"path": str(source), "explicit": False})

            with self.assertRaisesRegex(ValueError, "Absolute corpus paths"):
                ingest_corpus(config, ROOT)

            config["corpus_sources"][0]["explicit"] = True
            self.assertEqual(len(ingest_corpus(config, ROOT)), 1)

    def test_speaker_and_context_filters_exclude_non_author_material(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp)
            (source / "chat.txt").write_text(
                "A: author line\nplain continuation\nB: other line\n[context note]\nother continuation",
                encoding="utf-8",
            )
            docs = ingest_corpus(
                base_config(
                    {
                        "path": str(source),
                        "explicit": True,
                        "author_speaker": "A",
                        "exclude_non_author_speakers": True,
                        "exclude_context_notes": True,
                    }
                ),
                ROOT,
            )

            text = docs[0]["text"]
            self.assertIn("author line", text)
            self.assertIn("plain continuation", text)
            self.assertNotIn("other line", text)
            self.assertNotIn("other continuation", text)
            self.assertNotIn("context note", text)

    def test_generated_source_plan_readme_is_not_author_corpus(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp)
            (source / "README.md").write_text(
                "<!-- character-generator-source-plan:start -->\n# Corpus Source Plan",
                encoding="utf-8",
            )
            (source / "author.txt").write_text("author evidence", encoding="utf-8")

            docs = ingest_corpus(
                base_config({"path": str(source), "explicit": True}),
                ROOT,
            )

            self.assertEqual(len(docs), 1)
            self.assertEqual(Path(docs[0]["path"]).name, "author.txt")

    def test_plain_readme_is_not_author_corpus_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp)
            (source / "README.md").write_text("reading rules, not author voice", encoding="utf-8")
            (source / "author.txt").write_text("author evidence", encoding="utf-8")

            docs = ingest_corpus(
                base_config({"path": str(source), "explicit": True}),
                ROOT,
            )

            self.assertEqual(len(docs), 1)
            self.assertEqual(docs[0]["text"], "author evidence")

    def test_chat_source_defaults_skip_intro_context_and_non_author_b_blocks(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp)
            (source / "chat.md").write_text(
                "整理说明不是作者声音\n\n"
                "【时间：2026-7】\n\n"
                "【起因：context only】\n\n"
                "A：author first\n"
                "plain author continuation\n"
                "B：other speaker\n"
                "other speaker continuation\n"
                "A：author second",
                encoding="utf-8",
            )

            docs = ingest_corpus(
                base_config({"path": str(source), "explicit": True, "source_type": "chat"}),
                ROOT,
            )

            text = docs[0]["text"]
            self.assertIn("author first", text)
            self.assertIn("plain author continuation", text)
            self.assertIn("author second", text)
            self.assertNotIn("整理说明", text)
            self.assertNotIn("context only", text)
            self.assertNotIn("other speaker", text)

    def test_worklist_expands_authorized_external_files_and_skips_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            external = root / "external"
            source.mkdir()
            external.mkdir()
            target = external / "piece.txt"
            target.write_text("worklist target evidence", encoding="utf-8")
            (source / "README.md").write_text("reading rules", encoding="utf-8")
            (source / "worklist.md").write_text(f'@\"{target}\"', encoding="utf-8")

            docs = ingest_corpus(
                base_config({"path": str(source), "explicit": True, "source_type": "work"}),
                ROOT,
            )

            self.assertEqual(len(docs), 1)
            self.assertEqual(docs[0]["text"], "worklist target evidence")

    def test_readme_generation_can_be_enabled_per_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            old_root = build_character.PROJECT_ROOT
            build_character.PROJECT_ROOT = ROOT
            try:
                source_a = Path(tmp) / "a"
                source_b = Path(tmp) / "b"
                source_a.mkdir()
                source_b.mkdir()
                (source_a / "one.txt").write_text("one", encoding="utf-8")
                (source_b / "two.txt").write_text("two", encoding="utf-8")

                records = write_source_readmes(
                    base_config(
                        {
                            "source_id": "a",
                            "path": str(source_a),
                            "explicit": True,
                            "generate_readme": True,
                            "role": "chat_core",
                        },
                        {
                            "source_id": "b",
                            "path": str(source_b),
                            "explicit": True,
                            "generate_readme": False,
                        },
                    )
                    | {"source_planning_enabled": True}
                )

                self.assertEqual(records[0]["status"], "written")
                self.assertTrue((source_a / "README.md").exists())
                self.assertFalse((source_b / "README.md").exists())
            finally:
                build_character.PROJECT_ROOT = old_root

    def test_generated_character_handoff_is_written_when_planning_enabled(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "character"
            output.mkdir()
            path = write_corpus_reading_handoff(
                output,
                base_config(
                    {
                        "source_id": "work",
                        "path": str(Path(tmp)),
                        "explicit": True,
                        "role": "long_form_style",
                    }
                )
                | {"source_planning_enabled": True, "optional_missing_info": ["profile"]},
                [],
                [{"path": "a.txt", "text": "x"}],
                [{"chunk_id": "chunk_0001"}],
            )

            self.assertIsNotNone(path)
            text = path.read_text(encoding="utf-8")
            self.assertIn("Corpus Reading Handoff", text)
            self.assertIn("profile", text)

    def test_external_source_paths_are_disambiguated_in_handoff(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_a = root / "wechat_selected_chats" / "character.sample-style"
            source_b = root / "work" / "character.sample-style"
            source_a.mkdir(parents=True)
            source_b.mkdir(parents=True)
            output = root / "character"
            output.mkdir()

            path = write_corpus_reading_handoff(
                output,
                base_config(
                    {"source_id": "chat", "path": str(source_a), "explicit": True},
                    {"source_id": "work", "path": str(source_b), "explicit": True},
                )
                | {"source_planning_enabled": True},
                [],
                [],
                [],
            )

            text = path.read_text(encoding="utf-8")
            self.assertIn("wechat_selected_chats/character.sample-style", text)
            self.assertIn("work/character.sample-style", text)


if __name__ == "__main__":
    unittest.main()
