# character-generator

`character-generator` builds style-inspired digital writing skills. It takes a public or authorized corpus and produces a platform-neutral local skill package under `characters/<character_id>/`.

The generator is not the character skill. The generator lives in this project. The generated skill lives in `characters/<character_id>/` and may be exposed to any compatible local-skill platform through a projection or adapter.

## Cooperation Boundary

`character-generator` creates initial scaffolds and generation workflow assets. It does not maintain long-lived manually evolved characters. Runtime drift should be diagnosed by `style-doctor`, and existing character patches should be handled by `character-maintainer`.

Do not promote a mature character's special structure into generator templates without first deciding whether the lesson is generalizable or character-specific.

Generator-level changes from runtime drift must come through `packages/character-system/reports/runtime-loop/generalization_backlog/`. A single character patch is not enough to modify generator templates; the maintainer must first record a generalization note and decision.

## What It Produces

Each build creates:

- `SKILL.md`
- `README.md`
- `references/`
- `prompts/`
- `reports/`
- `tests/cases/`
- `output_manifest.json`

The result is a writing assistant inspired by patterns in the corpus. It is not a simulator of a real person's identity.

Generated skills may also include bounded `discussion` support when the config lists it in `target_tasks`. Discussion means a natural style-inspired response to a user thought; it does not mean identity roleplay, private memory invention, or a real-person chatbot.

`tests/cases/` contains empty validation case templates for user-assisted quality checks. They are not training data and should be filled only with user-approved, anonymized, or synthetic text for that character.

## Prepare a Corpus

Place public or authorized source files in a corpus directory, for example:

```text
corpus/sample-character/
  essay-01.md
  notes.txt
```

Supported input formats:

- `.txt`
- `.md`
- `.docx` when Python can read its internal document XML

Hidden files and empty files are skipped.

## Add a Character Conversationally

Normal personal-character builds should start from conversational intake, not
from hand-written JSON. The user supplies the build goal, display label,
authorized corpus sources, target interaction tasks, privacy confirmation, and
any optional profile or source notes. The agent then writes a temporary intake
or normalized plan in an ignored local location and runs:

```bash
python scripts/build_character.py --intake configs/_private/sample-character.intake.json --write-plan configs/_private/sample-character.plan.json
```

If required information is missing, generation stops before creating the
character. If only optional information is missing, the build continues with
safe defaults and reports follow-up gaps in the generated corpus handoff.

Required intake:

- `character_id` or enough information to derive one from `display_name`;
- `display_name` or a user-approved display label;
- at least one authorized corpus source path;
- `authorization_confirmed: true`;
- target tasks or target interaction type;
- `privacy_boundary_accepted: true`.

Safe defaults include high privacy, medium style strength, short-only quotes,
an output folder under `characters/<character_id>`, and standard forbidden
tasks for impersonation, private fact inference, and verbatim reconstruction.

## Add A Character With A Config

Create one config file per character:

```text
configs/sample-character.json
```

Use `configs/character_config.example.json` as the template. Users should add a new config instead of editing a global config or changing scripts.

For unfinished configs, use one of these draft locations:

```text
configs/newWriter.draft.json
configs/_drafts/newWriter.json
```

Draft configs are skipped by `--all` and ignored by Git.

## Generate One Character

```bash
python scripts/build_character.py --config configs/sample-character.json
```

This reads the config, ingests the corpus, anonymizes sensitive content, extracts style signals, generates the skill files, validates the package, and writes a manifest.

Config builds remain supported for automation and repeatable local builds. New
personal-corpus flows may use `corpus_sources` instead of the legacy single
`corpus_path`.

Example multi-source shape:

```json
{
  "corpus_sources": [
    {
      "path": "corpus/sample-character/work",
      "source_type": "work",
      "role": "long_form_style",
      "include": true,
      "generate_readme": true,
      "explicit": true
    },
    {
      "path": "corpus/sample-character/chat",
      "source_type": "chat",
      "role": "friend_chat_core",
      "include": true,
      "generate_readme": true,
      "author_speaker": "A",
      "exclude_non_author_speakers": true,
      "exclude_context_notes": true,
      "speaker_rules": "A is author; bracketed lines are context."
    }
  ]
}
```

Absolute local corpus paths are allowed only when explicitly supplied through a
local/private plan or source entry. Do not commit private absolute paths into
reusable configs, examples, templates, or reports intended for sharing.

## Generate All Characters

```bash
python scripts/build_character.py --all
```

This scans `configs/*.json`, skips `character_config.example.json`, and builds each declared character.

## Platform Exposure

Expose the generated folder to a compatible platform:

```text
characters/sample-character/
```

The platform should use that folder as a character skill. The skill's `SKILL.md` indexes references and task prompts. OpenCode is one supported deployment example; it is not part of the generated skill's role or authority model.

The legacy config field `generate_opencode_skill` is accepted for backward compatibility but does not branch the current build. Existing configs may retain it; new configs do not need it.

## Update a Character

1. Add, remove, or edit files in the configured corpus directory.
2. Adjust `configs/<character_id>.json` if needed.
3. Run the same build command again.

The output folder is regenerated from config and corpus.

## Future RAG Extension

This project is designed so retrieval can be added internally without changing the public interface. Future versions can add embeddings, chunk indexes, and retrieval-time style examples under internal files while keeping the same user workflow:

```bash
python scripts/build_character.py --config configs/sample-character.json
```

## Safety Position

Generated skills must:

- Say they are style-inspired.
- Avoid impersonation.
- Avoid private fact inference.
- Avoid long verbatim reconstruction.
- Prefer abstract style rules and self-created examples.

## Git and Private Data

This project should version the generator workflow, not private source material.

The default `.gitignore` excludes:

- `corpus/`
- generated `characters/<character_id>/` folders
- `configs/*.local.json`
- `configs/*.draft.json`
- `configs/_private/`
- `configs/_drafts/`

Generated character skills may contain corpus-derived style notes, so commit them only after an explicit privacy review.

Reports produced by this workflow are snapshots. If a generated report conflicts with `workspace_manifest.yaml`, shared policy, or current Git state, regenerate the report and trust the source documents.

## Runtime Loop Input

The generator only accepts runtime lessons that have passed through maintainer review:

1. A diagnosis packet records the runtime failure.
2. A handoff packet routes it to `character-maintainer`.
3. A patch note and validation note show the local repair.
4. A generalization note in `packages/character-system/reports/runtime-loop/generalization_backlog/` explains why the lesson should affect generator assets.

Until that record exists, keep the lesson character-specific and do not modify generator logic or templates.
