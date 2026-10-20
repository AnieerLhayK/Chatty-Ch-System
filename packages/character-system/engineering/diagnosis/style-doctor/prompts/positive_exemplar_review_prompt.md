# Positive Exemplar Review

Use when the user asks why a character output worked or nominates it as possible
character evidence. Load [SKILL.md](../SKILL.md) and apply its scope and load gates;
an explicit override remains provisional with the required context warning.

Review the task/input, selected output, exact user judgment and relevant rules.

1. Classify pass, strong_pass or exemplar_candidate. Positive feedback is
   evidence, not proof of character fidelity or a reason to suppress concerns.
2. Name reusable mechanisms with short supporting evidence. Separate them from
   merely attractive wording and ask whether they add anything to existing rules.
3. Record provenance: authorized_corpus_evidence, user_authored_exemplar,
   user_confirmed_synthetic_exemplar or unknown_provenance. An exemplar_candidate
   requires user approval, known provenance and a potentially useful new mechanism;
   preserve uncertainty rather than inventing provenance.
4. Check task fit, factual fidelity, privacy, originality, safety, maintainability
   and circular self-imitation. Keep synthetic examples distinct from corpus.
5. Give a promotion recommendation and smallest suitable target for maintainer
   review. State what this sample cannot establish, especially biography,
   authorship or a general rule beyond this character.

The maintainer owns accepted/rejected/deferred and any promotion. Success alone
creates no failure diagnosis packet or diagnosis-ledger row; return a text-only
nomination or retain it in its existing validation case. Include character_context
in any packet; formal record conventions are in
[runtime_records.md](../docs/runtime_records.md).
