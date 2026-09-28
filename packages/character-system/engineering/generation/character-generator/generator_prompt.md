# Character Generator Prompt

Use `character-generator` to build a style-inspired writing skill from an authorized corpus or an existing config. It requires Python execution, Git inspection, write access to the configured output, and package validation.

## Conversational intake

Do not make the user hand-write JSON. Collect the required information conversationally:

- Character id and display name.
- Each corpus path, source type and role, whether to include it in extraction, and speaker/context rules for chat-like sources.
- Confirmation that the user is authorized to use the sources and accepts style-inspired output, no impersonation, no private-fact inference, and no verbatim reconstruction.
- Target tasks, typical situation, and language.

Ask for optional preferences only when useful: output path, privacy and style strength, quote policy, relationship posture, normalization, forbidden tasks, report path visibility, and successful-output examples. If a required path, authorization, privacy acceptance, or target is missing, stop and ask; do not infer it. Safe defaults are allowed only for optional fields, and gaps must be reported.

Do not edit existing runtime characters or the `character-maintainer` and `style-doctor` skills as part of generation.

When source planning is active, write the ignored local intake/plan and preserve the corpus-reading handoff. Generate or update source README files only when requested.

## Existing config

Read the named config and only its declarative generation fields: `character_id`, `display_name`, `corpus_path`, `corpus_sources`, `output_path`, `privacy_level`, `style_strength`, `target_tasks`, `forbidden_tasks`, `quote_policy`, and `max_quote_chars`. If it is missing or incomplete, stop and ask for the config or conversational intake. Do not invent paths, identity, authorization, privacy settings, or tasks.

Run from the generator package:

```powershell
python scripts/build_character.py --config configs/<character>.json
```

For conversational intake, use:

```powershell
python scripts/build_character.py --intake configs/_private/<character>.intake.json
```

## Rebuild safety

Before rebuilding, verify the config's output path and inspect the target state. Do not overwrite a manually evolved character or a mature character such as `target-character`; route changes to an existing character through `character-maintainer`. Rebuild only a generator-owned output when the user requested that rebuild. Never commit private corpus material.

## Report

Confirm the output contains `SKILL.md`, `README.md`, `references/`, `prompts/`, `reports/`, `output_manifest.json`, and `reports/corpus_reading_handoff.md` when source planning is active. Summarize the build plan without private excerpts, generated files, validation, privacy/quality gaps, and whether maintainer follow-up is recommended. Do not commit unless explicitly asked.

The output is a style-inspired, bounded writing and discussion skill. Never create an identity simulator, impersonation bot, private-fact inference tool, private chatbot, or corpus reconstruction tool.
