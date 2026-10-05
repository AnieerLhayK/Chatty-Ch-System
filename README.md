# Chatty-Ch-System

[简体中文](README.zh-CN.md)

Chatty Ch System groups corpus preparation, character-skill generation, diagnosis,
and maintenance in one public engineering system. It includes the QQ raw material
filter as an internal module. It ships no private corpus, personal lexicons,
finished character, runtime memory, or private reports.

## Modules

All modules live under `packages/character-system/engineering/`:

- `corpus-preparation/qq-raw-material-filter`: parse QCE v5 exports, score and bucket
  material, audit lexicons, and prepare review samples.
- `generation/character-generator`: build style-inspired skills from reviewed,
  authorized material.
- `diagnosis/style-doctor`: diagnose style drift and runtime output failures.
- `maintenance/character-maintainer`: maintain skills and review patches.

Package protocols live in `packages/character-system/shared/`. Portable workspace
policies live in `shared/`. [Frame for AI Workspace](https://github.com/AnieerLhayK/Frame-for-AI-workspace)
is the host framework; preserve package layout and protocols when using another host.

## Filter installation and use

From the repository root:

```bash
python -m pip install -e packages/character-system/engineering/corpus-preparation/qq-raw-material-filter
qce-block-filter --help
```

Set `AI_ROOT` to your own absolute data root. On PowerShell use
`$env:AI_ROOT = 'C:/my-materials'`; on a POSIX shell use `export AI_ROOT=/my/materials`.
Default inputs, outputs, lexicons and review decisions are resolved under
`raw_material/qq/exports/character.<writer_name>/` within that root.

```bash
cd packages/character-system/engineering/corpus-preparation/qq-raw-material-filter
python qce_block_filter.py --writer-name sample --me-id 123456789
```

Input and output overrides are available through `--input-dir` and `--output-dir`.
Relative configured lexicon or review paths still require `AI_ROOT`. Python 3.11+
is required. Raw exports stay read-only and processing stays local.

## Handoff to generation

Review the filter's JSONL buckets and anonymize selected material. Convert approved
material to `.txt`, `.md` or `.docx` before configuring generator corpus sources.
The generator does not directly ingest bucket JSONL. Material in `need_anonymize`
is not an approved corpus; inspect it before any handoff.

Run generator commands from `packages/character-system/engineering/generation/character-generator/`.
Copy its example configuration to an ignored private configuration, supply reviewed
corpus sources, and inspect generated skills and reports before runtime exposure.

## Verification

```bash
python -m pip install pytest
python scripts/check_public_package.py --dir .
```

The checker verifies public boundaries and runs each module's tests in its own
working directory. CI additionally installs the filter and checks its CLI on Python
3.11 and 3.12. Tests use synthetic inputs; optional live samples require an explicit
`QCE_SAMPLE_DATA_DIR` and must never be committed.

## Maintenance and provenance

This repository is a generated projection of the authoritative workspace package.
Maintain module sources and portable projection rules in `character-system`.
The host owns local paths, registered remote identity, TASK authorization and the
aggregate synchronizer. Never maintain a second filter publisher or edit a generated
checkout as source. `PROJECTION_SOURCE.json` identifies the published source revision.

The former [qq-chat-raw-filter](https://github.com/AnieerLhayK/qq-chat-raw-filter)
repository is retired and retained for history. Its functionality is maintained here.

Bilingual navigation and the privacy-focused filter overview adapt the unmerged
[filter documentation PR #1](https://github.com/AnieerLhayK/qq-chat-raw-filter/pull/1)
and [Chatty documentation PR #1](https://github.com/AnieerLhayK/Chatty-Ch-System/pull/1).
The source package remains authoritative; those PRs are not automatically merged.
