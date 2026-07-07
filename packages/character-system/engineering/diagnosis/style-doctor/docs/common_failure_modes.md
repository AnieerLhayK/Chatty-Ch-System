# Common Failure Modes

## "Too AI"

Symptoms:
- Generic helpfulness.
- Polished structure.
- Safe emotional validation.
- Tidy final takeaway.

Patch direction:
- Add anti-pattern examples.
- Penalize generic closure in the rubric.
- Strengthen prompt priority for character voice over helpful assistant defaults.

## "Not Like target character"

Symptoms:
- Missing characteristic stance.
- Wrong intimacy level.
- Too much explanation.
- Incompatible emotional access.

Patch direction:
- Clarify `voice_card`.
- Add task-specific recipe if the drift appears only in one task.
- Add runtime evaluation criteria for voice fidelity.

## "Sentences Too Full"

Symptoms:
- Clause stacking.
- Over-explained transitions.
- Ending each paragraph with a final meaning.

Patch direction:
- Add rhythm and compression rules to `style_profile`.
- Add a rubric item for breath, interruption, and uneven pressure.

## "Emotion Too Direct"

Symptoms:
- Names the primary feeling.
- Explains vulnerability.
- Uses therapeutic reassurance.

Patch direction:
- Add emotional indirectness rules.
- Add anti-patterns for direct feeling labels.

## "Imagery Too Stacked"

Symptoms:
- Multiple images compete in one sentence.
- Images decorate instead of changing the thought.
- Literary density replaces character specificity.

Patch direction:
- Add image economy rules.
- Ban decorative image piles in `anti_patterns`.
- Score image function in `evaluation_rubric`.

## "Prompt Failure"

Symptoms:
- Correct skill files but repeated runtime failure.
- Task instruction overpowers character instruction.
- Output ignores a known anti-pattern.

Patch direction:
- Move the relevant constraint into the active prompt.
- Add a pre-delivery self-check.
- Add a task recipe for the recurring task.
