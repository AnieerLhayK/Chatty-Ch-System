# Shared Protocols

Canonical dependencies are declared once in
`workspace_manifest.yaml -> skills[style-doctor].protocol_dependencies` and
cross-checked by `packages/character-system/shared/protocol_manifest.json`.
Resolve them from the manifest; do not copy shared content into this skill.

Runtime-loop records apply only to character-output diagnosis. Governance,
manifest, release, migration, CI, Git, and platform issues use workspace task
routing; patch and validation ownership remains with `character-maintainer`.
