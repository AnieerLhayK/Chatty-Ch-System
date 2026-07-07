# Interface Design

## Principle

`character-generator` exposes a small stable interface and hides internal workflow details. Users should not need to understand prompt engineering, anonymization, chunking, validation, templates, or manifest generation.

## External Interface

The stable interface has four parts:

1. conversational intake handled by the invoking agent;
2. optional ignored local intake/plan files such as `configs/_private/*.intake.json`;
3. config builds through `python scripts/build_character.py --config ...`;
4. `generator_prompt.md`

Everything else is internal implementation detail.

For normal personal-character builds, the user should not hand-write JSON. The
agent should ask for missing required information, normalize the answers into
an internal build plan, and run `--intake` or a private generated plan.

Config files remain the stable automation interface for repeatable builds.

## Configs as Declarative Contracts

Each config or normalized intake plan declares:

- Which character package to build.
- Where the authorized corpus lives, either as one legacy `corpus_path` or as
  multiple `corpus_sources`.
- Where output should be written.
- Which privacy level and quote policy apply.
- Which tasks are supported or forbidden.
- Whether the config is enabled for batch builds.
- Whether source planning should generate source-local README guidance and a
  generated character corpus handoff.
- Whether source-local `README.md` files are only reading contracts, and whether
  `worklist.md` should expand to referenced source files.

The config is a contract, not an implementation script. A user says "what to build" and "under what boundary"; the generator decides "how to build it".

This allows internal modules to evolve without changing the user workflow. Future versions may change chunk size, extraction heuristics, templates, reports, or retrieval systems while preserving the same config shape.

## Internal Modules

Internal modules include:

- `templates/`: file blueprints.
- `scripts/ingest_corpus.py`: corpus loading.
- `scripts/anonymize_corpus.py`: privacy redaction.
- `scripts/chunk_corpus.py`: chunking with metadata.
- `scripts/corpus_stats.py`: corpus statistics.
- `scripts/validate_pack.py`: package validation.
- `scripts/write_manifest.py`: manifest generation.

These modules are intentionally hidden from normal users. Engineering agents
may maintain them within the generator authority boundary, but ordinary
generation should require only a config and one command.

## Missing Intake Or Config Behavior

If a user asks for a personal character but required intake information is
missing, the workflow must stop before generating files. It must not guess
corpus paths, authorization, privacy acceptance, display names, or target
tasks.

If a user explicitly asks for config mode and `configs/bob.json` does not
exist, the workflow must stop and ask for a config or conversational intake.

## Draft Config Behavior

Unfinished configs should use `configs/<id>.draft.json`, `configs/_drafts/<id>.json`, or `"enabled": false`.

Batch mode skips these configs. Direct `--config` mode can still be used for deliberate testing after the config is complete enough to validate.

## Stability Rule

The following command should remain stable:

```bash
python scripts/build_character.py --config configs/sample-character.json
```

Internal files may change as long as this interface and generated output contract remain intact.

The conversational command is additive and may evolve internally:

```bash
python scripts/build_character.py --intake configs/_private/sample-character.intake.json
```

The user-facing contract is the information check and build behavior, not the
private JSON shape.

## Source Planning Defaults

Normal personal-corpus sources use conservative defaults:

- source README files are not author voice and are skipped during extraction;
- `worklist.md` may point to authorized external source files and is treated as
  an index rather than author voice;
- chat sources exclude bracketed context notes and non-author speaker blocks by
  default;
- generated character handoffs record source roles and normalization decisions
  without embedding raw private excerpts.
