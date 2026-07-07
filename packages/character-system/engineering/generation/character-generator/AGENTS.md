# AGENTS.md

## Project Goal

`character-generator` is a workflow project for producing platform-neutral, style-inspired character skills. Any agent with the required Python, filesystem, source, and validation capabilities may operate it within its `generator_write` authority boundary. Generated output under `characters/<character_id>/` may be exposed to compatible local-skill platforms through projections or adapters.

The project must never turn a real person into an identity simulator. Generated skills must be positioned as writing aids inspired by public or authorized works, not as "the person as AI".

## File Structure

- `configs/`: one JSON config per character. This is the main external contract.
- `schemas/`: JSON schemas for configs and output manifests.
- `templates/`: stable templates for generated skill files, references, prompts, and reports.
- `scripts/`: internal workflow implementation.
- `tests/`: unit tests for validation, privacy rules, and output structure.
- `docs/`: design and policy documents.
- `examples/`: minimal user-facing examples.
- `characters/`: generated character skills.

## Working Principles

- Keep the public interface simple: users edit `configs/<character_id>.json`, run `python scripts/build_character.py --config ...`, or use `generator_prompt.md`.
- Keep implementation details internal: chunking, anonymization, style extraction, prompt generation, validation, and manifest writing should not leak into the user workflow.
- Treat config files as declarative contracts. They declare source, destination, safety level, style strength, and tasks; they do not tell the implementation how to work internally.
- Prefer Python standard library code unless a dependency is already necessary.
- Keep scripts modular and callable from `build_character.py`.
- Do not absorb mature character maintenance into the generator. Runtime drift belongs to `style-doctor`; long-term character patches belong to `character-maintainer`.
- Treat reports as snapshots. Regenerate them when manifest, shared policy, or Git state changes.

## Version Control Rules

- Use Git as the safety backup for this workflow. Before changing workflow files, inspect `git status --short`.
- After meaningful workflow changes, run tests and create a focused commit.
- Do not commit private corpora, generated character folders, Python caches, or local/draft/private configs.
- Keep `corpus/`, `characters/<character_id>/`, `configs/*.local.json`, `configs/*.draft.json`, `configs/_private/`, and `configs/_drafts/` out of Git unless the user explicitly approves a reviewed exception.
- Prefer small commits that describe the workflow change, such as `Add draft config handling`.
- If a change breaks the workflow, use Git history to inspect or restore the last known good version instead of rewriting files from memory.

## Safety Principles

- The generated skill must say it is style-inspired, not identity-based.
- Do not generate copy claiming "I am <real person>".
- Do not infer or reveal non-public private facts.
- Do not reconstruct long passages from the corpus.
- Use abstract style rules and newly created examples by default.
- Enforce `max_quote_chars`, defaulting to 80.

## Privacy Rules

- Mask phone numbers, emails, URLs, ID numbers, likely QQ/WeChat identifiers, address-like phrases, and heuristic Chinese names where appropriate.
- High privacy mode should anonymize more aggressively.
- Reports may describe privacy findings but must not expose raw sensitive values.
- Corpus snippets used in generated files must be short and sanitized.

## Testing Rules

Run this after changes:

```bash
python -m unittest discover tests
```

Tests should cover:

- Required config fields.
- Enum validation for privacy and style.
- Output structure validation.
- Privacy masking for phone and email.
- Long quote detection.

## Code Style

- Keep code readable and small.
- Use friendly errors with actionable next steps.
- Avoid hard-coded character IDs, paths, or task lists outside schema defaults and examples.
- Keep generated output deterministic where possible.
- Add comments only for non-obvious logic.

## Do Not Do

- Do not merge generator project files with generated character skill files.
- Do not require users to understand prompt engineering or chunking.
- Do not output real private contact details.
- Do not create a real-person chatbot or identity emulator.
- Do not silently create a missing config from a guessed character name.

## Checks After Modification

1. Run unit tests.
2. Generate a sample character if corpus is available.
3. Inspect `characters/<character_id>/SKILL.md` for safety boundaries.
4. Inspect reports for privacy leakage.
5. Confirm `output_manifest.json` matches the generated files.
6. Commit the workflow changes when tests pass and private/generated files remain ignored.
