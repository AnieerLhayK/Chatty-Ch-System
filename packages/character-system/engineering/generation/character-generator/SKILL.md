---
name: character-generator
description: Generate a new character writing-style skill from authorized material or a character config; maintain generator assets when explicitly requested.
---

# Character Generator

Create a style-inspired character baseline. Existing manually evolved characters
belong to `character-maintainer`; runtime output evaluation belongs to
`style-doctor`. Keep source material authorized, abstract style from evidence,
and produce fresh writing guidance without impersonation or private-fact inference.

## Authority And Source

Role: `production`; authority: `generator_write`. Default mode: `text_only`.
Allowed modes: `text_only`, `record_write`, `source_patch`.

Resolve editable source through
`workspace_manifest.yaml -> skills[character-generator].source_path` in Workspace;
platform paths are projections. Follow the host's task and permission rules.
Use `record_write` for generator-owned reports. Enter `source_patch` only for an
explicit build or generator update after verifying source, relevant Git state,
output ownership and a validation path. Otherwise return a text proposal and
state which check is unavailable. Exposure adds no authority.

## Shared expression

In Workspace, resolve relative links from this entry's canonical source, not
the platform projection; standalone exports use their bundled local reference.

Within this skill's active task, read the [shared expression rules](references/shared-expression.md)
once; reuse them if already read for this task. This reference does not invoke
the full Speaking Like A MAN skill or extend activation beyond this task.
If unreadable, disclose the gap once and continue under this skill's own rules;
do not search the disk, install resources or claim the shared check was completed.

Apply the reference to generated guidance and task explanations while keeping
character-specific voice separate. Builds bundle an identical reference for the
new character, whose existing delivery check includes it. Sharing this reference
does not authorize regenerating mature characters; future runtime lessons still
require the established generalization review.

## Workflow

1. Establish the build. Read [generator_prompt.md](generator_prompt.md) for
   conversational intake or an existing config. Resolve the display label,
   character id, authorized sources, target tasks and privacy acceptance. Reuse
   supplied answers; ask only for missing required inputs. Before execution,
   confirm an explicit output target and that it is new or generator-owned.
2. Select the existing route. Use the intake or config build described in
   [docs/workflow.md](docs/workflow.md). Optional preferences use the documented
   defaults. Source README planning is opt-in. A mature character change routes
   to the maintainer; a rebuild requires an explicit request and a verified
   generator-owned target.
3. Build and check. Before changing generated structure, consult
   `packages/character-system/shared/character_skill_spec.md` and
   `packages/character-system/shared/versioning_policy.md`. Validate the package,
   referenced resources, manifest and privacy findings using the existing build
   checks. Distinguish structural validation from observed writing quality.
4. Deliver a reviewable baseline or precise missing-input report. Identify the
   output, executed checks, evidence gaps and any recommended runtime trials.
   A scaffold or a successful build alone does not establish character fidelity.

## Generator Maintenance

For an explicitly requested generator-local improvement, inspect its callers
and tests, change only the responsible generator assets, and run the relevant
checks in [AGENTS.md](AGENTS.md). Preserve manually evolved characters.

Runtime lessons enter generator assets only through a maintainer-approved
note under `packages/character-system/reports/runtime-loop/generalization_backlog/`.
A diagnosis or single character patch is insufficient; keep unreviewed lessons
character-specific or pending review.

## Conditional Resources

- In Workspace, resolve shared dependencies through
  [SHARED_PROTOCOLS.md](SHARED_PROTOCOLS.md) and follow
  `shared/workspace/workspace_policy.md`; load runtime-loop/reporting detail
  only for an approved generalization or generator-owned record.
- For interface/config details, read [docs/interface_design.md](docs/interface_design.md).
- For corpus handling and quotation rules, read [docs/privacy_policy.md](docs/privacy_policy.md).
