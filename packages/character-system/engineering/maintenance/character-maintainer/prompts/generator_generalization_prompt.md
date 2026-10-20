# Generator Generalization Prompt

Use this prompt only after local validation provides evidence for a possible
generator-level lesson. Apply [SKILL.md](../SKILL.md) and the shared runtime-loop
generalization rules; a diagnosis or attractive patch alone is insufficient.

```text
Write a generator generalization note based on the maintenance finding below.

Finding:
<maintenance_finding>

Character:
<character_id>

Do not edit character-generator or templates.

Output:
- observed character-level failure
- local patch that fixed it
- validation evidence and remaining uncertainty
- why the issue may generalize
- proposed generator guidance or template adjustment
- risks of overgeneralizing
- classification: generalizable, character-specific or uncertain
- examples of characters where this should not apply
```
