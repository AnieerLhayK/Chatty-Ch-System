# Shared Protocols

This skill uses manifest-routed workspace and character-system protocols:

- `packages/character-system/shared/drift_taxonomy.md`
- `packages/character-system/shared/patch_protocol.md`
- `packages/character-system/shared/handoff_format.md`
- `packages/character-system/shared/runtime_loop_policy.md`
- `shared/workspace_policy.md`

Resolve these paths through `workspace_manifest.yaml`. Do not copy shared protocol content into this skill. Update shared docs in the manifest-declared shared source when the protocol changes.

Related governance policies:

- `shared/reporting_policy.md`
- `packages/character-system/shared/future_drift_policy.md`

Runtime-loop records use the templates in `packages/character-system/shared/templates/` and the audit directories under `packages/character-system/reports/runtime-loop/`. `style-doctor` may create diagnosis and handoff packets, and may update the diagnosis ledger for formal diagnosis events. Patch notes, validation notes, generalization notes, patch-ledger updates, and accepted/rejected/deferred decisions belong to `character-maintainer`.

Those runtime-loop records are only for character-output diagnosis. Workspace
governance, manifest, platform exposure, release, migration, validation script,
CI, Git, or repository maintenance issues must use workspace task routing
instead of `style-doctor`.
