# Drift Checklist

Use when the user says the output is "not like target character" or no longer sounds like the active character.

## Drift Types

- Voice drift: diction, stance, intimacy, or address pattern changes.
- Role drift: the character becomes advisor, therapist, critic, or narrator when it should not.
- Temperature drift: too intense, too flat, too sentimental, too clever, or too polished.
- Memory drift: ignores known voice rules, recurring motifs, or anti-patterns.
- Genre drift: becomes essay, motivational note, review, or generic literary prose.
- Task drift: follows the external task but loses the character's way of doing it.

## Diagnosis Questions

- What exact move makes it unlike the character?
- Is the failure local to one phrase, or global across the output?
- Did the model obey the task while abandoning the voice?
- Did it overuse a known motif until it became parody?
- Did it miss a negative constraint that should have stopped the drift?

## Likely Layers

- `voice_card`: core voice contract is underspecified or too abstract.
- `style_profile`: rhythm, imagery, or emotional handling is not operational enough.
- `task_recipes`: the current task lacks a character-specific recipe.
- `prompts`: runtime prompt does not prioritize voice under task pressure.

## Patch Shape

Use a narrow correction:

```markdown
When performing <task>, keep <specific character move> active even while satisfying the task. Avoid switching into <observed drift role>. If a direct explanation is needed, keep it partial, concrete, and voice-bound.
```

## Positive Evidence Check

When the output may be unusually strong, ask:

- Did the user explicitly approve it?
- Is its provenance known?
- Which concrete mechanisms worked?
- Does it add evidence beyond existing references?
- Are facts, privacy, originality, and safety still sound?
- Would promoting its wording create circular self-imitation?
- Is a short mechanism note safer than retaining the full passage?
- Should the maintainer accept, reject, or defer promotion?

The doctor answers the evidence questions but leaves the final promotion
decision to `character-maintainer`.
