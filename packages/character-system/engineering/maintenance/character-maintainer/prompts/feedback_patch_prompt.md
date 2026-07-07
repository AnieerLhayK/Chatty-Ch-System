# Feedback Patch Prompt

Use this prompt shape when the user gives qualitative feedback.

```text
Patch characters/<character_id> based on this feedback:

"<user_feedback>"

First translate the feedback into observable failure modes. Then identify the smallest responsible surface: voice_card, style_profile, writing_patterns, anti_patterns, evaluation_rubric, prompts, task_recipes, or reports.

Make the smallest patch that should change future behavior. Preserve existing manual evolution and examples unless they directly cause the failure.

Add a patch note explaining:
- original feedback
- diagnosis
- files changed
- expected effect
- validation check
- whether this should generalize to generator guidance

Do not rewrite the character and do not edit character-generator.
```
