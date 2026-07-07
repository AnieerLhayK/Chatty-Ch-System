# Shared Protocols

This skill uses manifest-routed workspace and character-system protocols:

- `packages/character-system/shared/character_skill_spec.md`
- `packages/character-system/shared/drift_taxonomy.md`
- `packages/character-system/shared/patch_protocol.md`
- `packages/character-system/shared/handoff_format.md`
- `packages/character-system/shared/runtime_loop_policy.md`
- `packages/character-system/shared/versioning_policy.md`
- `shared/workspace_policy.md`

Resolve these paths through `workspace_manifest.yaml`. Do not copy shared protocol content into this skill. Update shared docs in the manifest-declared shared source when the protocol changes.

Related governance policies:

- `shared/reporting_policy.md`
- `packages/character-system/shared/future_drift_policy.md`

Runtime-loop work writes durable records under `packages/character-system/reports/runtime-loop/`. The `character-maintainer` authority contract covers maintainer decisions, patch notes, validation notes, patch-ledger updates, and the decision to create generator generalization notes.
