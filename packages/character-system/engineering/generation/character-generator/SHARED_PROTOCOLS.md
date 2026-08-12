# Shared Protocols

Canonical dependencies are declared once in
`workspace_manifest.yaml -> skills[character-generator].protocol_dependencies`
and cross-checked by `packages/character-system/shared/protocol_manifest.json`.
Resolve them from the manifest; do not copy shared content into this skill.

Runtime-loop, reporting, and future-drift material is maintenance context. Read
it only when a maintainer-approved generalization decision makes it relevant.
