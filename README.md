# Chatty Ch System

Chatty Ch System is the public engineering layer of a character-skill system for
building, diagnosing, and maintaining style-inspired chatting and writing bots.
It intentionally ships no finished character, private corpus, runtime memory, or
personal material.

This repository is best used inside
[Frame for AI Workspace](https://github.com/AnieerLhayK/Frame-for-AI-workspace), where routing, shared policy,
validation, and workspace migration rules are already in place. The system can
also be copied into another governed workspace if you preserve the package
layout and shared protocols.

## What Is Included

- `packages/character-system/engineering/generation/character-generator`: build
  a character skill from an authorized or public corpus.
- `packages/character-system/engineering/diagnosis/style-doctor`: diagnose
  style drift and runtime output failures.
- `packages/character-system/engineering/maintenance/character-maintainer`:
  maintain generated skills across patches and version changes.
- `packages/character-system/shared`: schemas, templates, drift taxonomy,
  patch protocol, handoff format, and runtime-loop policy.
- `shared`: portable root-level workspace policies needed to understand how the
  package is meant to be moved and governed.

## What Is Not Included

- No runtime character folders.
- No private or personal corpus.
- No diagnosis, handoff, validation, or patch reports from a private workspace.
- No distribution bundle such as a finished toolkit release.
- No local absolute paths or machine-specific configuration.

## Quick Check

```bash
python scripts/check_public_package.py --dir .
cd packages/character-system/engineering/generation/character-generator
python -m pytest tests -q
```

## Basic Use

1. Put authorized or public source material in an ignored local `corpus/`
   directory.
2. Copy `configs/character_config.example.json` to a private config path and
   edit the character id, display name, corpus sources, target tasks, and
   privacy settings.
3. Run the generator from
   `packages/character-system/engineering/generation/character-generator`.
4. Inspect the generated skill and reports before exposing it to any runtime
   platform.

Generated character skills are style-inspired writing tools. They are not
identity simulators, impersonation bots, private fact inference tools, or corpus
reconstruction tools.
