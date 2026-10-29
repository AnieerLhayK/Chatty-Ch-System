---
name: character-maintainer
description: Maintain an existing character skill from an explicit maintenance request or linked diagnosis; propose or apply focused changes while preserving manual refinements.
---

# Character Maintainer

Role: `maintenance`; authority: `source_patch`. Maintain an existing character's
files and preserve its manual refinements and working examples. New characters
belong to `character-generator`; standalone output evaluation belongs to
`style-doctor`. Generator assets remain outside the maintainer's write boundary.

## Execution And Source

Default mode: `text_only`. Allowed modes: `text_only`, `record_write`, `source_patch`.
Use `record_write` for maintenance decisions, notes and permitted ledger updates.
Apply source changes only when the user requests maintenance and the exact
scope, source files, relevant Git state and validation method are verifiable.
Otherwise return a proposal or the precise evidence gap instead of editing.
Follow `shared/workspace/workspace_policy.md` in Workspace and the host's
applicable task/permission rules elsewhere. Platform exposure adds no authority.

## Shared expression

In Workspace, resolve relative links from this entry's canonical source, not
the platform projection; standalone exports use their bundled local reference.

Within this skill's active task, read the [shared expression rules](references/shared-expression.md)
once; reuse them if already read for this task. This reference does not invoke
the full Speaking Like A MAN skill or extend activation beyond this task.
If unreadable, disclose the gap once and continue under this skill's own rules;
do not search the disk, install resources or claim the shared check was completed.

Use the reference when reviewing expression in the target or a proposed patch,
and in maintenance explanations. Preserve intentional voice and manual evolution;
general wording preferences cannot justify rebuilding a mature character. Include
expression in the existing regression check. Doctor suggestions remain advisory;
one local patch does not authorize changing MAN or generator assets.

## Workflow

1. Resolve the target character and current source/version. Inspect file names,
   applicable manual decisions and existing changes before reading deeply.
   A direct maintenance request can proceed without running Doctor: use the
   user's explicit goal, relevant files and available evidence. For behavioral
   repair, inspect the actual input/output when available; for offline alignment,
   inspect the concrete contradiction. Ask for missing evidence only when it
   changes the proposed repair. If a diagnosis/handoff is supplied, verify its
   exact target and source rather than selecting the newest record.
2. Identify the cause and smallest responsible surface. Read only relevant
   references, prompts, rubrics and examples. Use
   [docs/architecture.md](docs/architecture.md) for layer selection. Preserve
   character-specific human refinements; if precedence or the cause remains
   unclear, explain the uncertainty and defer the edit.
3. Propose or apply a focused change within the verified scope and execution
   mode. Tie each edit to the maintenance goal and observable evidence. Preserve
   working examples unless they cause the problem. A broader rewrite needs a
   separately explicit rebuild-level request; ordinary maintenance stays narrow.
4. Validate and record. Re-read changed sections with the adjacent rules they
   depend on; check the requested behavior and regression cases. Report the
   reason, changed files, expected effect, observed checks and remaining gaps in
   the character's established maintenance note/changelog. Mark unrun behavioral
   trials as unverified: a saved patch is not evidence of better runtime output.

Completion means a reviewable narrow proposal or verified patch with its
reason and validation evidence, or a specific rejection/deferral with the
missing evidence. Do not require a Doctor packet for direct maintenance.

## Formal Handoffs And Generalization

For a Workspace runtime-loop handoff, load
[docs/runtime_handoff.md](docs/runtime_handoff.md). Verify linked records and
record `accepted`, `rejected`, or `deferred` before editing; use the existing
patch/validation templates and ledger. Doctor wording or unauthorized side
effects are candidate material, never accepted state.

A lesson can reach the generator only through a separate generalization note
after local validation. Classify it as generalizable, character-specific or
uncertain, with evidence; preserve mature character differences. Read
[docs/coupling_strategy.md](docs/coupling_strategy.md) for this boundary.

## Conditional Resources

- For a substantial offline audit, use
  [prompts/offline_maintenance_prompt.md](prompts/offline_maintenance_prompt.md)
  and [checklists/crossfile_consistency_checklist.md](checklists/crossfile_consistency_checklist.md).
- For qualitative user feedback, use
  [prompts/feedback_patch_prompt.md](prompts/feedback_patch_prompt.md) and the
  matching [drift checklist](checklists/drift_diagnosis_checklist.md).
- For version comparison, use
  [prompts/compare_character_prompt.md](prompts/compare_character_prompt.md).
- For generator-upgrade compatibility, read
  [docs/compatibility_policy.md](docs/compatibility_policy.md); preserve the
  existing character instead of replacing it with regenerated templates.
- For longer-term records, use [docs/evolution_strategy.md](docs/evolution_strategy.md)
  and the matching report/patch/changelog template under `templates/`.
- In Workspace, resolve canonical dependencies through
  [SHARED_PROTOCOLS.md](SHARED_PROTOCOLS.md); formal handoff infrastructure is
  needed only for that branch.
