# Rhythm Checklist

Use for "sentences too full", "rhythm is off", stiff syntax, or collapsed cadence.

## Signals

- Every sentence has the same length or contour.
- Clauses stack explanation on explanation.
- The output overuses parallel structure.
- It explains before letting a line breathe.
- It uses transitions such as "but", "so", "because", or "still" in predictable ways.
- It ends each paragraph with a polished landing.
- Short sentences feel dramatic rather than natural.
- Long sentences feel padded rather than pressured.

## Diagnosis Questions

- Where does the sentence carry more meaning than it can hold?
- Are pauses doing character work, or only creating fake depth?
- Does the rhythm match the character's emotional speed?
- Does the output need cuts, breaks, rougher turns, or less symmetry?

## Likely Layers

- `style_profile`: cadence rules are missing or too decorative.
- `evaluation_rubric`: rhythm is not evaluated separately.
- `prompts`: runtime instruction allows over-complete prose.
- `task_recipes`: task encourages explanation-heavy output without a compression rule.

## Patch Shape

Add an operational rhythm rule:

```markdown
Rhythm rule: prefer uneven sentence pressure over balanced polish. Let some thoughts stop early. Cut explanatory tails when the emotion is already legible.
```
