# Feedback Maintenance Prompt

Load [SKILL.md](../SKILL.md) and apply its source, scope and execution-mode checks.
Use the exact user feedback, relevant input/output and current character rules;
direct maintenance does not require a prior Doctor diagnosis.

Translate the complaint into an observable mismatch. Identify its responsible
surface before proposing the smallest useful change. Preserve human refinements
and examples unless they cause that mismatch. If a supplied diagnosis/handoff is
relevant, verify its exact target/version and re-evaluate its evidence; formal
Workspace handoffs use [runtime_handoff.md](../docs/runtime_handoff.md).

Return the focused proposal or authorized patch with feedback/evidence, reason,
affected files, protected behavior, expected effect and a regression trial.
Record the observed checks in the established maintenance note; label unrun
behavior trials unverified. Request missing evidence only when it materially
changes the repair.
