# Architecture

`character-maintainer` is a maintenance workflow for already-created character skills. It assumes the character has accumulated intent, examples, and reports that must be preserved.

## Core surfaces

- `SKILL.md`: entrypoint, activation contract, runtime-critical instructions.
- `references/`: voice cards, style profiles, writing patterns, anti-patterns, rubrics, recipes, examples.
- `prompts/`: reusable runtime prompts and task prompts.
- `reports/`: drift reports, comparison notes, finetune reports, patch notes, changelog entries.

## Maintenance loop

1. Inventory the character folder.
2. Identify the requested maintenance mode.
3. Diagnose across files before editing.
4. Select the smallest responsible file and section.
5. Apply a patch.
6. Re-check neighboring files for consistency.
7. Record the evolution.

## Non-goals

- Do not create characters from scratch.
- Do not replace a character with generator output.
- Do not act as a pure runtime critic that stops at diagnosis.
- Do not edit `character-generator` or its templates.

## Patch target hierarchy

Use the smallest effective surface:

1. Report-only note when evidence is weak.
2. Prompt patch when behavior fails only in one task path.
3. Anti-pattern or rubric patch when a repeated failure needs enforcement.
4. Style or writing-pattern patch when prose texture drifts.
5. Voice-card patch only when identity, stance, or relational posture is wrong.
6. Multi-file patch only when consistency requires it.
