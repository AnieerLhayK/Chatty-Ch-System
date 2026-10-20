# Candidate Wording Prompt

Use only when the user explicitly requests specific candidate wording after or
alongside diagnosis. Load [SKILL.md](../SKILL.md) and apply its scope, load-evidence
and authority gates. Preserve a provisional context warning when applicable.

From the observed failure and relevant source excerpts, return:

1. Exact character-local target file/section.
2. Minimal candidate insertion or replacement text.
3. Evidence linking that wording to the intended behavior.
4. Overcorrection risk, protected behavior and a test of the hypothesis.

Prefer a concrete desired behavior over another blanket prohibition. Keep hard
boundaries where needed. Mark the text advisory for character-maintainer review;
it is neither an applied patch nor an accepted maintenance decision. If the
responsible source section is unavailable, describe scope instead of inventing
an insertion target. Doctor does not edit source or maintenance records.
