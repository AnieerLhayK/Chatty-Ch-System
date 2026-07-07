# Shared Protocols

This skill uses manifest-routed workspace and character-system protocols:

- `packages/character-system/shared/character_skill_spec.md`
- `packages/character-system/shared/runtime_loop_policy.md`
- `packages/character-system/shared/versioning_policy.md`
- `shared/workspace_policy.md`

Resolve these paths through `workspace_manifest.yaml`. Do not copy shared protocol content into this skill. Update shared docs in the manifest-declared shared source when the protocol changes.

Related governance policies:

- `shared/reporting_policy.md`
- `packages/character-system/shared/future_drift_policy.md`

Generator changes based on runtime drift require a maintainer-approved generalization note in `packages/character-system/reports/runtime-loop/generalization_backlog/`. Character-specific runtime patches are not generator requirements by themselves.
