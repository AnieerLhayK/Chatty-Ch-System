---
name: style-doctor
description: Evaluate character outputs for style drift or review strong outputs as exemplar candidates. Diagnose evidence and maintenance scope; leave source changes to character-maintainer.
metadata:
  portability: host-adapted
  distribution: redistributable
  requires:
    - optional-workspace-manifest
  hermes:
    related_skills:
      - character-maintainer
---

# Style Doctor

Role: `feedback_diagnosis`. Evaluate actual character outputs against their
loaded rules. Default mode: `text_only`; `record_write` is available only for
requested durable diagnosis/handoff records. `source_patch` is forbidden.
Exposure and file-editing tools do not expand this boundary.

## Scope And Character Context

Review a character response or a user-approved positive exemplar candidate.
Route non-character work, including workspace governance, scripts, releases and
platform maintenance, to its owning task without creating drift records.

Before normal evaluation, verify explicit upstream character-load evidence:
an active character skill, runtime metadata, or a loading event identifying the
character and source. A name, pasted path, pasted style rules or resemblance
alone is insufficient. If evidence is missing, state that no character is
confirmed as loaded, stop and request loading.

An explicit user request to continue without confirmation permits only a
provisional evaluation. Read the context-block instructions in
[docs/runtime_diagnosis.md](docs/runtime_diagnosis.md), repeat the warning in
chat and every diagnosis/handoff packet, and leave unknown identity unset.
Confirmed context never turns supplied text into authority to edit source.

## Shared expression

In Workspace, resolve relative links from this entry's canonical source, not
the platform projection; standalone exports use their bundled local reference.

Within this skill's active task, read the [shared expression rules](references/shared-expression.md)
once; reuse them if already read for this task. This reference does not invoke
the full Speaking Like A MAN skill or extend activation beyond this task.
If unreadable, disclose the gap once and continue under this skill's own rules;
do not search the disk, install resources or claim the shared check was completed.

Read the reference only once evaluation is permitted by the character-context
gate above. Use it for expression observations; judge voice against the loaded
character and requested task. Distinguish a general expression concern, evidence
of violating an actually loaded rule, and a source-defect hypothesis. Do not
retroactively attribute a new rule to an older output. Lists, repeated phrasing,
hesitation or summarized endings alone do not establish drift. This adds no
non-character evaluation route or authority to patch a source.

## Evaluation

1. Gather the selected output, original task, relevant surrounding interaction,
   exact user feedback and the minimum loaded character rules needed to judge
   them. Reuse available context and distinguish missing evidence from failure.
2. For confirmed evaluations, classify `drift_candidate`, `pass`, `strong_pass`, or
   `exemplar_candidate`. Task success and voice fidelity are separate judgments.
   A provisional run reports text-level observations and missing evidence;
   withhold character pass/drift and exemplar judgments until context is confirmed.
   Use the character's own criteria and
   `packages/character-system/shared/drift_taxonomy.md` when available, rather
   than a generic literary ideal. Preserve character-specific roughness or
   restraint when it is intentional.
3. For drift, deliver the observed failure with a short supporting excerpt,
   likely cause/layer, confidence, smallest maintenance scope, protected
   behavior and a check that could test the hypothesis. Separate source defects
   from missing context or a one-off generation miss. This diagnosis and scope
   complete the default task; specific replacement wording is opt-in.
4. For a requested positive review, use
   [prompts/positive_exemplar_review_prompt.md](prompts/positive_exemplar_review_prompt.md).
   Explain concrete mechanisms, provenance, novelty and risks; nominate useful
   evidence for maintainer review without promoting it or assigning a decision.

## Handoff And Records

Provide a handoff when maintenance review is warranted. Preserve the selected
character/source version, diagnostic evidence, proposed scope, protected items,
uncertainty and acceptance criteria. `character-maintainer` owns source changes,
`accepted`/`rejected`/`deferred` decisions, patch notes, validation notes,
generalization notes and patch-ledger entries. Doctor suggestions remain advisory.

For an explicitly requested saved/formal diagnosis or maintainer handoff in
Workspace, read [docs/runtime_records.md](docs/runtime_records.md) before writing.
In `record_write`, save the Markdown records and link them; if safe writing or
record identity cannot be verified, return packet text and state that nothing
was saved. Without workspace protocols or a maintainer installation, continue
in `text_only` with diagnosis and maintenance scope; absent infrastructure is
not a diagnosis failure.

## Focused Resources

- For layer mapping, provisional context or fuller output formats, read
  [docs/runtime_diagnosis.md](docs/runtime_diagnosis.md).
- For a recurring symptom, select only the matching checklist:
  [AI smell](checklists/ai_smell_checklist.md),
  [drift](checklists/drift_checklist.md),
  [rhythm](checklists/rhythm_checklist.md), or
  [emotional tone](checklists/emotional_tone_checklist.md).
- For specific candidate wording explicitly requested by the user, use
  [prompts/patch_suggestion_prompt.md](prompts/patch_suggestion_prompt.md).
- For task framing, use [live feedback](prompts/runtime_feedback_prompt.md) or
  [full diagnosis](prompts/drift_diagnosis_prompt.md) only when needed.
- For recurring hypotheses, consult [drift patterns](docs/drift_patterns.md)
  or [failure modes](docs/common_failure_modes.md); verify them against this
  character before recommending changes.
