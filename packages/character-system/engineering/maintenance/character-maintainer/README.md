# character-maintainer

`character-maintainer` is an engineering maintenance system for existing character skills. It keeps long-lived character folders coherent, expressive, and compatible as prompts, rubrics, reports, and generator assumptions evolve.

It is not `character-generator`. The generator is responsible for batch production and initial scaffolding. The maintainer is responsible for patching, calibrating, repairing drift, aligning files, preserving manual refinements, and recording evolution after a character already exists.

Its role and authority are independent of platform exposure. A compatible platform may invoke the same source skill, but exposure alone never grants permission to patch.

## Relationship to characters/<character_id>

The maintainer operates on an existing folder such as:

```text
characters/<character_id>/
  SKILL.md
  references/
  prompts/
  reports/
```

It reads the character's source files, diagnoses inconsistencies, applies narrow patches, and writes reports or changelog entries that explain the change. It should treat each character folder as a living artifact rather than a disposable generated output.

## Why patch is better than rewrite

A mature character skill often contains manual refinements, subtle voice decisions, edge-case fixes, and lived-in examples that a full rewrite can erase. Patch-first maintenance protects that accumulated quality.

Patch-first means:

- Change the smallest surface that explains the failure.
- Preserve working examples and prior evolution.
- Prefer additions, clarifications, and local wording fixes.
- Avoid template normalization unless the character is actually broken.

## Long-term evolution

Long-term character quality comes from a loop:

1. Collect feedback, reports, sample failures, and generator compatibility notes.
2. Diagnose the responsible surface: voice, style, pattern, anti-pattern, rubric, recipe, or prompt.
3. Apply a small patch.
4. Validate against adjacent files.
5. Record why the patch was made, what changed, expected effects, and whether the lesson should generalize.

The final division of responsibility is:

- `character-generator`: batch production.
- `character-maintainer`: long-term evolution.
- `characters/target-character`: high-quality real runtime behavior.

When a drift lesson may affect future generated characters, classify it as `generalizable`, `character-specific`, or `uncertain`. Do not directly edit generator templates from maintainer work; record a generalization note instead.

## Runtime Loop Records

When `character-maintainer` receives a handoff packet, it should first review the diagnosis and the character source files, then record an explicit `accepted`, `rejected`, or `deferred` decision.

If `style-doctor` has already edited source files, patch notes, validation notes, generalization notes, or `patch_ledger.md`, treat those changes as untrusted candidate material. Review them against the diagnosis, accept only the useful parts, and remove or revise anything outside the doctor boundary before committing.

Maintainers should locate runtime-loop evidence by explicit path or ID, not by "the newest file." Preferred lookup order:

1. Use the path supplied by the user or packet.
2. Use `handoff_id` to find the handoff, then follow `diagnosis_id` and `diagnosis_record_path`.
3. Use `diagnosis_id` to search `packages/character-system/reports/runtime-loop/diagnoses/` and `packages/character-system/reports/runtime-loop/ledgers/diagnosis_ledger.md`.
4. If only a case/task is named, search by character id and case/task slug; ask the user when multiple records match.

If the matching record is ambiguous, defer rather than patching from the wrong diagnosis.

For accepted runtime-loop patches, the maintainer should:

1. Apply a small scoped patch.
2. Write a patch note using `packages/character-system/shared/templates/patch_note.template.md`.
3. Write a validation note using `packages/character-system/shared/templates/validation_note.template.md`.
4. Update `packages/character-system/reports/runtime-loop/ledgers/patch_ledger.md`.
5. Decide whether a generator generalization note belongs in `packages/character-system/reports/runtime-loop/generalization_backlog/`.

The operating policy is `packages/character-system/shared/runtime_loop_policy.md`.
