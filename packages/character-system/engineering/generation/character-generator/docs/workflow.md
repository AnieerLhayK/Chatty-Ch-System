# Workflow

## Public Command

Conversational intake:

```bash
python scripts/build_character.py --intake configs/_private/sample-character.intake.json --write-plan configs/_private/sample-character.plan.json
```

Single character:

```bash
python scripts/build_character.py --config configs/sample-character.json
```

All configured characters:

```bash
python scripts/build_character.py --all
```

`--all` skips:

- `configs/character_config.example.json`
- `configs/*.draft.json`
- `configs/_drafts/*.json`
- configs with `"enabled": false`

## Internal Pipeline

The command performs:

1. Read intake or config.
2. For intake, check required information and normalize safe defaults.
3. Validate the normalized config against schema rules.
4. Inventory configured corpus source(s).
5. Optionally create or update source-local README planning blocks.
6. Ingest corpus files from all included sources.
7. Skip source README files by default, expand `worklist.md` entries when present, clean text, and apply source metadata filters for speaker/context notes.
8. Anonymize sensitive content.
9. Chunk corpus.
10. Compute corpus statistics.
11. Extract style, theme, rhythm, and vocabulary signals.
12. Render reference templates.
13. Render task prompt templates.
14. Render `SKILL.md` and `README.md`.
15. Write reports, including `reports/corpus_reading_handoff.md` when source planning is active.
16. Validate output package.
17. Write `output_manifest.json`.

## Output

Generated files are written to:

```text
characters/<character_id>/
```

This folder is the character skill. The generator project itself should not be copied into a platform loading root as the skill.

## Failure Handling

- Missing required intake: stop and report missing required fields before output creation.
- Missing config in config mode: stop and ask for a config or conversational intake.
- Invalid config: show validation errors.
- Missing corpus: stop and ask for authorized corpus files.
- Missing optional intake: continue with safe defaults, then report quality gaps and maintainer follow-up.
- Validation failure: write the evaluation report and fail the build.

## Source README And Worklist Handling

Source-local `README.md` files are treated as reading contracts and are skipped
by default during style extraction. Set `include_readme_as_corpus` only for a
deliberate, reviewed source where the README itself is author voice.

When a source directory contains `worklist.md`, the ingester expands entries in
the form `@"path"` and reads the referenced `.txt`, `.md`, or `.docx` files.
The index file itself is skipped when expansion is enabled.

For `source_type: chat`, the ingester defaults to reading from the first
`【时间...】` marker onward, excluding bracketed context notes and non-author
speaker blocks such as `B:` or `B：` when `A` is present. These defaults can be
overridden with source metadata.
