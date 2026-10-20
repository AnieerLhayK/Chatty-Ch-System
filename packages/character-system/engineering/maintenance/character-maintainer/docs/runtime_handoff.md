# Workspace Runtime Handoff

Load this branch for a formal Workspace runtime-loop handoff. Direct maintenance
uses [SKILL.md](../SKILL.md) without requiring a Doctor packet.

## Resolve The Evidence

1. Use the supplied path; otherwise locate handoff_id and follow diagnosis_id
   and diagnosis_record_path. If only diagnosis_id is supplied, search
   `packages/character-system/reports/runtime-loop/diagnoses/` and
   `packages/character-system/reports/runtime-loop/ledgers/diagnosis_ledger.md`.
2. With only a character/case slug, identify matching records and ask or defer
   if more than one could be the target. Never select latest.md or a record
   merely because it is newest.
3. Verify filename, packet and linked IDs, character/source version and ledger
   status. Read session_snapshot, session_storage and character_context; inspect
   original context when the diagnosis is uncertain. Missing or provisional load
   evidence cannot establish a normal runtime style failure. Resolve that gap
   or defer; do not silently promote provisional evidence to confirmed.
4. Re-check the claimed failure against current character source and relevant
   Git state. Treat Doctor wording and any Doctor-authored source, patch-note,
   validation, generalization or patch-ledger changes as candidate material.
   Existing manual decisions and unrelated work remain protected.

## Decide, Patch And Record

Follow `packages/character-system/shared/runtime_loop_policy.md` and
`packages/character-system/shared/patch_protocol.md`, with dependencies resolved
through [SHARED_PROTOCOLS.md](../SHARED_PROTOCOLS.md). Verify host task authority
before record or source writes.

Record accepted, rejected or deferred before source editing. For accepted work,
apply only the smallest patch satisfying the handoff's acceptance criteria.
Use `packages/character-system/shared/templates/patch_note.template.md`, then
`packages/character-system/shared/templates/validation_note.template.md` under
`packages/character-system/reports/runtime-loop/validations/`. Update
`packages/character-system/reports/runtime-loop/ledgers/patch_ledger.md` with the
actual decision and observed state. Preserve unique IDs and linked record paths.

Re-read the changed rules together and report actual checks, remaining risks and
rollback guidance. Unrun output trials remain unverified; keep the record short
of validated/closed when required evidence is missing. Missing optional historic
reports do not require recreating unrelated records.

Only a validated local lesson with evidence beyond one character can justify a
separate generalization note under
`packages/character-system/reports/runtime-loop/generalization_backlog/` using
the shared generalization template. Classify uncertainty explicitly and never
edit generator assets as part of this handoff.
