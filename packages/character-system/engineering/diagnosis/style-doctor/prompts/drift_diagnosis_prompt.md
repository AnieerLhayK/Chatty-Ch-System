# Full Diagnosis Prompt

Use for a detailed evaluation. Load [SKILL.md](../SKILL.md) first and apply its
scope, character-context and authority gates. This prompt supplies inputs and
analysis focus, rather than another permission contract.

Inputs:
- Selected output and original task.
- Exact feedback and relevant surrounding interaction.
- Explicit upstream loading evidence and character/source version.
- Relevant character rules; session/thread/export pointer when available.

Identify the first concrete mismatch. Compare task fit and voice fidelity,
explain the likely responsible layer, and separate supported findings from
missing context or a one-off generation miss. Return the outcome, minimal
supporting excerpt, cause/confidence, smallest maintenance scope, protected
behavior and a test of the hypothesis. If the output succeeds, follow the
requested positive-review branch instead of manufacturing a failure.

Complete with diagnosis and scope. Specific replacement wording is opt-in via
[patch_suggestion_prompt.md](patch_suggestion_prompt.md); a formal saved diagnosis
or maintainer handoff uses [runtime_records.md](../docs/runtime_records.md).
