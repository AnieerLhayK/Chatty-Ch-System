# Offline Maintenance Prompt

Use this prompt shape for a full maintenance pass over an existing character.

```text
Maintain characters/<character_id> as an existing character skill.

Do not rewrite the character. Diagnose first, then make only necessary patch-level edits.

Read the available SKILL.md, references/, prompts/, and reports/. Check cross-file alignment among voice_card, style_profile, writing_patterns, anti_patterns, evaluation_rubric, task_recipes, and prompts.

Find style drift, prompt inconsistency, weak anti-patterns, rubric failures, generic writing tendencies, compatibility issues, and stale evolution notes.

Output:
- concise diagnosis
- targeted patches
- report or changelog entry
- generator generalization note only if the lesson should affect future generated characters

Never edit character-generator or generator templates.
```
