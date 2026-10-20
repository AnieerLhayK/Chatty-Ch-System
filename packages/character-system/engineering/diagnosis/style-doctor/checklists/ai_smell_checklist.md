# AI Smell Checklist

Use when the output feels like ordinary AI instead of the target character.

## Signals

- Opens with a neat topic sentence that explains the whole point.
- Resolves tension too quickly.
- Summarizes the user's feeling instead of inhabiting a specific response.
- Uses balanced, polished clauses that feel pre-approved.
- Adds moral clarity, uplift, or reassurance without earning it.
- Says the obvious emotional state directly.
- Uses generic sensory imagery with no character-specific angle.
- Ends with a tidy insight, lesson, or soft inspirational turn.
- Sounds helpful but placeless.

## Diagnosis Questions

- Which sentence could appear in any AI assistant's output?
- Where does the language become smooth at the cost of character?
- Did the output protect itself from ambiguity?
- Did it replace a character move with a support-chat move?
- Did it explain the effect instead of producing the effect?

## Likely Layers

- `anti_patterns`: missing concrete examples of generic AI habits.
- `evaluation_rubric`: does not penalize helpful-polished sameness.
- `prompts`: asks for style but not for runtime constraints.
- `voice_card`: lacks specific diction, stance, or refusal patterns.

## Maintenance Scope

Check whether the active rules already constrain the observed generic move.
If they do, test for a generation miss before attributing a source defect.
When evidence supports maintenance, identify the responsible prompt, anti-pattern
or rubric and the behavior it should enforce. Preserve reassurance or closure
when the character and task call for it. Specific candidate wording is opt-in
under [SKILL.md](../SKILL.md).
