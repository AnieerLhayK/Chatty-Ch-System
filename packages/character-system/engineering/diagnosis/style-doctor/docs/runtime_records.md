# Workspace Diagnosis Records

Load this branch only for an explicitly requested saved/formal diagnosis or
maintainer handoff. The core evaluation and load gates remain in
[SKILL.md](../SKILL.md). Positive success alone is not a failure diagnosis event.

## Before Writing

Resolve source and canonical dependencies through [SHARED_PROTOCOLS.md](../SHARED_PROTOCOLS.md).
Follow `shared/workspace/workspace_policy.md` and verify active task authority.
Read `packages/character-system/shared/runtime_loop_policy.md` and
`packages/character-system/shared/patch_protocol.md` for the authoritative
record and handoff contracts. Check canonical paths through the host's read-only
filesystem interface if a platform skill viewer cannot cross the skill folder.

If paths, authority, record uniqueness or safe writing cannot be verified,
return packet Markdown in text_only mode and state that no durable record was
saved. A standalone distribution needs no substitute ledger.

## Save And Cross-Reference

1. Inspect the target directories and diagnosis ledger for unused IDs. Use the
   local creation date, increment the daily sequence and choose a unique
   timestamp/character/case filename; never overwrite another event or a fixed
   latest.md, diagnosis.md, handoff.md or output.md.
2. Write the diagnosis using
   `packages/character-system/shared/templates/diagnosis_packet.template.md`
   under `packages/character-system/reports/runtime-loop/diagnoses/`. A typical
   filename is `DIAG-YYYYMMDD-001-HHMMSS-character-case.md`.
3. When maintenance is needed, use
   `packages/character-system/shared/templates/handoff_packet.template.md`
   under `packages/character-system/reports/runtime-loop/handoffs/`, with a
   matching `HANDOFF-YYYYMMDD-001-HHMMSS-character-case.md` identity. Follow the
   shared packet fields instead of inventing another record format.
4. Include actual `record_path` and linked `diagnosis_record_path`, plus the
   same `character_context` block in both packets. Preserve `session_snapshot`
   with the minimum interaction needed to reassess the diagnosis and
   `session_storage` pointing to a session/thread/export, or `not_available`
   with its reason. Recommended inspection targets are workspace-relative
   character source paths, never platform projections.
5. Add the formal diagnosis to
   `packages/character-system/reports/runtime-loop/ledgers/diagnosis_ledger.md`.
   Re-read packets and cross-links, then link saved files in the chat summary.

Keep maintenance scope advisory; concrete candidate wording is included only
when requested. Leave maintenance decisions, patch/validation/generalization
notes and the patch ledger to character-maintainer. For a strong positive
output, retain a text-only nomination or its validation case instead of adding
a failure-ledger event.
