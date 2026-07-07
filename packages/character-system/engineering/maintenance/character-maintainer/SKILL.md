---
name: character-maintainer
description: Long-term engineering maintenance for existing character skills under character folders. Use when a capable agent needs to diagnose, patch, align, evolve, or preserve a character skill across SKILL.md, references, prompts, reports, rubrics, changelogs, and generator compatibility without rewriting the character or modifying character-generator templates.
---

# Character Maintainer

## Role, Authority, And Exposure

This is a `maintenance` role with `source_patch` authority. Platform exposure makes the skill discoverable but does not widen its authority or bypass its execution-mode checks.

## Operating Contract

Maintain existing character skills. Do not generate new characters, rewrite a whole character skill, or perform only runtime style diagnosis. Work on `characters/<character_id>/` and preserve the user's manual refinements.

Hard rules:

- Diagnose first, patch second.
- Patch first: prefer small, targeted edits over broad rewrites.
- Never overwrite human evolution, nuanced examples, or hard-won voice details.
- Never directly modify `character-generator` or generator templates.
- Let maintainer and generator stay weakly coupled through reports, suggestions, patch notes, and generalization notes.
- Make every change traceable: why it changed, what changed, expected effect, and whether it should generalize.
- For runtime-loop handoffs, record an `accepted`, `rejected`, or `deferred` decision before editing.

## Output Boundary

Allowed outputs:

- Character-local diagnosis, maintainer decision, narrow source patch, patch note, validation note, and patch-ledger update.
- Rejection or deferral when evidence is weak, ambiguous, or outside the character boundary.
- Generalization note only when a validated lesson may apply beyond one character.

Forbidden outputs:

- Whole-character rewrites unless the user explicitly requests a rebuild-level intervention.
- Direct edits to `character-generator` or generator templates.
- Treating `style-doctor` candidate wording, source diffs, or ledger edits as automatically accepted.
- Patching from the newest diagnosis when the target record is ambiguous.
- Promoting character-specific behavior into generator defaults without a separate generalization decision.

If the model cannot verify the handoff, source files, and current Git state, defer instead of patching.

## Execution Mode

- Default: `text_only`.
- Allowed: `text_only`, `record_write`, `source_patch`.
- Use `record_write` for maintainer-owned decisions, patch notes, validation notes, and permitted ledger updates without changing character source.
- Enter `source_patch` only when the user requests a patch and the exact diagnosis or maintenance scope, source files, relevant Git state, and validation method can be verified.
- If any requirement is unavailable or ambiguous, remain in `text_only` or `record_write` and return a proposed patch instead of applying it.

These modes follow `shared/workspace_policy.md` and do not permit generator edits or broader character rewrites.

## Expected Character Layout

Read only what is needed, but start by mapping the available files:

```text
characters/<character_id>/
  SKILL.md
  references/
  prompts/
  reports/
```

Typical files may include `voice_card`, `style_profile`, `writing_patterns`, `anti_patterns`, `evaluation_rubric`, `task_recipes`, prompt packs, sample outputs, drift reports, and changelog entries.

If a character has a different layout, adapt conservatively and document the assumption in the report.

## Workflow

1. Establish scope
   - Identify the target character id and maintenance mode: offline maintenance or feedback-based maintenance.
   - Inspect file names and recent reports/changelog entries before reading deeply.
   - Protect unrelated files and existing local changes.

2. Diagnose
   - Compare `voice_card`, `style_profile`, `writing_patterns`, `anti_patterns`, `evaluation_rubric`, `task_recipes`, and prompts.
   - Look for style drift, cross-file contradiction, prompt inconsistency, weak anti-patterns, rubric gaps, generic writing tendencies, and overcorrection.
   - Use the checklists only as lenses, not as permission to rewrite.
   - If a handoff packet exists, verify the linked diagnosis before deciding whether to accept, reject, or defer.

3. Choose patch targets
   - Map each issue to the smallest responsible surface:
     - Voice identity or relational posture: `voice_card`.
     - Sentence rhythm, diction, emotional temperature: `style_profile` or `writing_patterns`.
     - Repeated bad output habits: `anti_patterns`.
     - Missed evaluation failures: `evaluation_rubric`.
     - Task-specific behavior mismatch: `task_recipes` or prompts.
     - Generator-wide lesson: reports or generalization notes only.
   - If one small patch can fix the issue, do not touch adjacent files.

4. Patch
   - Make narrow edits with `apply_patch`.
   - Preserve examples unless they are directly causing the failure.
   - Add or refine constraints instead of replacing whole sections.
   - Keep wording compatible with the character's existing vocabulary.

5. Record evolution
   - Add a patch note or changelog entry in `reports/` or the character's established changelog location.
   - Include the diagnosis, files changed, expected effect, regression risk, validation method, and generalization recommendation.
   - If a lesson may improve future generation, write a generator generalization note. Do not edit generator code or templates.
   - For runtime-loop work, use `packages/character-system/shared/templates/patch_note.template.md` and update `packages/character-system/reports/runtime-loop/ledgers/patch_ledger.md`.

6. Validate
   - Re-read the changed sections together with the files they align with.
   - Check that the patch did not contradict higher-priority identity, rubric, or prompt instructions.
   - When sample outputs exist, compare before/after behavior qualitatively and note remaining risks.
   - For runtime-loop work, write `packages/character-system/reports/runtime-loop/validations/VAL-YYYYMMDD-001-*.md` from `packages/character-system/shared/templates/validation_note.template.md`.

## Runtime Loop Handoff Mode

When a handoff packet arrives:

1. Locate the exact handoff and diagnosis by explicit path or ID. Do not assume the newest file is relevant.
2. Re-read the diagnosis packet and relevant character files.
3. Verify that filename ID, packet ID, linked IDs, and ledger status agree. If multiple records match a case/task slug, ask the user or defer.
4. Check whether `style-doctor` already edited source files, patch notes, validation notes, generalization notes, or `patch_ledger.md`. Treat any such changes as candidate material, not accepted state.
5. Record `accepted`, `rejected`, or `deferred`.
6. If accepted, apply only the smallest patch that satisfies the acceptance criteria.
7. Write a patch note.
8. Write a validation note.
9. Update the patch ledger.
10. Decide whether to create a generalization note in `packages/character-system/reports/runtime-loop/generalization_backlog/`.

Lookup order:

1. Use the path supplied by the user or packet.
2. Use `handoff_id` to find the handoff, then follow `diagnosis_id` and `diagnosis_record_path`.
3. Use `diagnosis_id` to search `packages/character-system/reports/runtime-loop/diagnoses/` and `packages/character-system/reports/runtime-loop/ledgers/diagnosis_ledger.md`.
4. If only a case/task is named, search by character id and case/task slug; ask the user when multiple records match.

Do not patch from `latest.md`, fixed output filenames, or an ambiguous search result.

## Maintenance Modes

### Offline Maintenance

Use when the input is an existing character skill and the user asks for audit, cleanup, alignment, drift repair, compatibility maintenance, or evolution.

Outputs:

- Targeted patches.
- Alignment fixes.
- Finetune or maintenance report.
- Changelog or patch note.
- Optional generator generalization note.

Use `prompts/offline_maintenance_prompt.md`, `checklists/crossfile_consistency_checklist.md`, and `templates/finetune_report.template.md` when the audit is non-trivial.

### Feedback-Based Maintenance

Use when the input is user feedback such as "too AI-like", "emotion is too explicit", "rhythm is off", "sounds generic", or "not like target-character anymore".

Process:

- Translate feedback into observable failure modes.
- Locate the responsible surface before editing.
- Patch only the necessary file or section.
- Record the feedback phrase, diagnosis, patch, and expected behavioral change.

Use `prompts/feedback_patch_prompt.md`, `checklists/drift_diagnosis_checklist.md`, and `templates/patch_note.template.md`.

## Cross-File Alignment Rules

Maintain consistency across these surfaces:

- `voice_card`: identity, posture, boundaries, relational stance.
- `style_profile`: prose texture, pacing, diction, emotional temperature.
- `writing_patterns`: repeatable constructive moves and sentence-level habits.
- `anti_patterns`: concrete forbidden habits with replacement behavior.
- `evaluation_rubric`: measurable pass/fail criteria matching the above.
- `prompts`: runtime instructions that must not fight the character source of truth.

When files disagree, prefer the most character-specific and human-refined source. If precedence is unclear, patch reports first with a recommendation instead of making a risky edit.

## Generator Compatibility

Treat generator upgrades as an input to compatibility maintenance, not as a reason to normalize old characters.

- Do not edit `character-generator`.
- Do not replace character files with newly generated templates.
- Add compatibility notes, migration patches, or adapter guidance inside the character's reports.
- Preserve older character-specific decisions unless they directly break runtime behavior.
- Classify each broader lesson as generalizable, character-specific, or uncertain before recommending generator changes.

Read `docs/compatibility_policy.md` when generator compatibility is the user's main concern.

## Resource Map

- `docs/architecture.md`: maintainer role, boundaries, and system surfaces.
- `docs/coupling_strategy.md`: weak coupling with generator and character folders.
- `docs/evolution_strategy.md`: long-term changelog and learning loop.
- `docs/compatibility_policy.md`: generator upgrade and legacy character maintenance.
- `checklists/*.md`: focused audit lenses for alignment, drift, and consistency.
- `prompts/*.md`: reusable task prompts for maintenance passes.
- `templates/*.template.md`: report, patch note, changelog, and comparison formats.
- `packages/character-system/shared/runtime_loop_policy.md`: durable runtime-loop record policy and state machines.
- `packages/character-system/shared/templates/*.template.md`: workspace-level diagnosis, handoff, patch, validation, and generalization templates.
