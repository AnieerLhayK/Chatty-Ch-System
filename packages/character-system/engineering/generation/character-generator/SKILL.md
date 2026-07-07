---
name: character-generator
description: Use when building or updating a character writing-style skill from an authorized corpus, template set, or character configuration.
---

# character-generator

Use this skill when building or updating a character writing-style skill from an authorized corpus, template set, or character configuration.

## Workspace Source

The source of truth for this skill is:

```text
workspace_manifest.yaml -> skills[character-generator].source_path
```

Do not edit the linked platform path directly.

## Role, Authority, And Exposure

This is a `production` role with `generator_write` authority. Platform exposure controls discovery only; it does not change the generator boundary or authorize mature-character maintenance.

## Shared Protocols

Before changing generated character structure, consult:

- `packages/character-system/shared/character_skill_spec.md`
- `packages/character-system/shared/runtime_loop_policy.md`
- `packages/character-system/shared/versioning_policy.md`
- `shared/workspace_policy.md`

## Responsibilities

- Ingest public or authorized corpus material.
- Extract style signals.
- Generate character skill scaffolds.
- Validate generated output structure.
- Preserve privacy and avoid impersonation.

## Output Boundary

Allowed outputs:

- Generated character skill scaffolds from authorized corpus and config.
- Build reports, validation summaries, and privacy warnings for generated output.
- Generator-local improvements when explicitly requested and supported by source evidence.

Forbidden outputs:

- Runtime drift diagnosis for an active character; use `style-doctor` instead.
- Patches to mature manually evolved characters; use `character-maintainer` instead.
- Generator template changes from a single unvalidated character failure.
- Private corpus commits, identity impersonation, or private fact inference.

If a runtime lesson is mentioned without a maintainer-approved generalization note, keep it out of generator templates and report it as character-specific or pending review.

## Execution Mode

- Default: `text_only`.
- Allowed: `text_only`, `record_write`, `source_patch`.
- Use `record_write` only for generator-owned reports or validation records.
- Enter `source_patch` only for an explicitly requested build or generator update after resolving the workspace source, inspecting relevant Git state, and confirming a validation path.
- If those checks are unavailable, return the proposed scaffold or change as text and remain in `text_only`.

These modes follow `shared/workspace_policy.md` and do not expand the generator's output boundary.

## Boundaries

This skill creates and updates generator logic. It does not perform runtime drift diagnosis; use `style-doctor` for diagnosis and `character-maintainer` for patching existing character skills.

When a mature character such as `target-character` evolves, do not automatically copy that evolution into generator templates. Record the lesson for maintainer review and classify it as generalizable or character-specific before changing generator assets.

Only accept runtime lessons that have a maintainer-approved generalization note under `packages/character-system/reports/runtime-loop/generalization_backlog/`. Do not change generator templates from a single character patch, a diagnosis packet alone, or an unvalidated runtime failure.
