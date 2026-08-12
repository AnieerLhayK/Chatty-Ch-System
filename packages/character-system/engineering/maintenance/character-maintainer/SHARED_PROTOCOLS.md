# Shared Protocols

Canonical dependencies are declared once in
`workspace_manifest.yaml -> skills[character-maintainer].protocol_dependencies`
and cross-checked by `packages/character-system/shared/protocol_manifest.json`.
Resolve them from the manifest; do not copy shared content into this skill.

Runtime-loop templates and ledgers are loaded only for a formal runtime-loop
handoff. Maintainer decisions, patches, validation notes, and generalization
records remain exclusive to the maintainer boundary.
