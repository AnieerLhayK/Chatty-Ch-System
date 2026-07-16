# style-doctor

`style-doctor` is a runtime style evaluation skill for character skills.

It is used while a compatible runtime platform is actively using a character and something feels wrong: drift, AI smell, generic writing, flattened voice, wrong rhythm, overloaded imagery, direct emotion, fake literary tone, or prompt failure.

Its diagnosis target must be a character skill output or a positive exemplar
candidate for a character skill. It is not a workspace governance, release,
manifest, platform exposure, script, CI, Git, or repository optimization
diagnostic tool.

Before it diagnoses, it must confirm from upstream conversation/runtime context
that a character has actually been loaded. A character name, pasted path,
generic style rules, or a character-like output is not sufficient evidence. If
no load evidence is available, it must tell the user that no character is
currently confirmed as loaded and stop normal diagnosis until the character is
loaded.

If the user explicitly insists on continuing, the doctor may provide a
provisional diagnosis. It must mark the run as degraded and include a
`character_context` block with `status: missing` or `unconfirmed`,
`context_warning: true`, `user_override: true`, the available load evidence,
and the impact on reliability in both chat output and any diagnosis or handoff
packet. It must not infer the character identity or private facts to compensate
for the missing context.

Its `feedback_diagnosis` role and diagnosis-only authority stay the same on every exposure. Platform visibility does not grant source-patch authority.

It can also review unusually strong outputs. Positive review expands what the
doctor can evaluate, not what it can modify.

Standalone release bundles intentionally omit the maintainer and durable
runtime-loop infrastructure. The bundled doctor remains useful as a text-only
diagnostic companion: it can explain drift and suggest candidate changes, but
it cannot write records, approve patches, or modify skill source.

## Difference from character-maintainer

`character-maintainer` repairs and evolves the character skill.

`style-doctor` diagnoses live failures and produces focused patch suggestions for the maintainer. It should not rewrite the whole character, replace references, or refactor the project.

If the problem is about workspace structure, platform exposure, release
packaging, migration, validation scripts, manifests, shared governance, or
agent permissions, route it to the relevant workspace maintenance flow instead
of using `style-doctor`.

## Authority Boundary

`style-doctor` is allowed to:

- read manifest-declared source files needed for diagnosis;
- produce a diagnosis packet;
- produce a handoff packet when maintainer work is needed;
- suggest patch scope, insertion targets, and candidate wording;
- update the diagnosis ledger only when recording a formal diagnosis event.
- classify runtime evidence as `pass`, `strong_pass`, or
  `exemplar_candidate`, and explain why.

`style-doctor` is not allowed to:

- edit character source files, generator files, maintainer files, or shared protocols;
- create patch notes, validation notes, or generalization notes;
- update `packages/character-system/reports/runtime-loop/ledgers/patch_ledger.md`;
- mark a patch `accepted`, `rejected`, `deferred`, `applied`, or `validated`;
- treat its suggested patch text as already approved.
- promote an exemplar into character references or mix synthetic examples into
  authorized corpus.
- diagnose non-character workspace issues or create diagnosis, handoff, patch
  suggestion, or ledger material for them.

If a model cannot safely write files or is unsure about ownership, it should
output packet Markdown only and state that no durable record was saved. When
`record_write` is available and the user asks for a formal diagnosis or
maintainer handoff, the diagnosis and handoff should be saved as `.md` files in
the default runtime-loop directories, not left only in the chat transcript.

Recommended file paths in handoff packets should be workspace-relative source paths, such as `local-runtime-character-output/target-character/SKILL.md`, not platform projection paths.

## Why runtime diagnosis matters

Character drift often appears only during actual use. A skill can look correct in its files but still fail at runtime because the prompt overgeneralizes, the rubric misses a failure mode, a task recipe is absent, or the model reaches for generic AI habits under pressure.

Runtime diagnosis catches the exact moment where the character stops sounding like itself.

## How to use

When reviewing an output, provide:

- The active character skill or relevant files.
- The current generated output.
- The user's feedback, including exact complaints, praise, favorite passages,
  disagreements, or reasons the output feels unusually successful.

Do not use this skill for workspace-level optimization requests. For those,
select a workspace task such as `skill_architecture_update`,
`runtime_authorization_enforcement`, `platform_exposure`, or another
manifest-routed maintenance task.

`style-doctor` returns:

- An outcome: `drift_candidate`, `pass`, `strong_pass`, or
  `exemplar_candidate`.
- For drift, a focused diagnosis.
- The likely failed layer: `voice_card`, `anti_patterns`, `evaluation_rubric`, `prompts`, `style_profile`, or `task_recipes`.
- A small patch suggestion for character-maintainer when drift exists.
- For positive evidence, reusable mechanisms, provenance, risks, and a
  maintainer-owned promotion recommendation.
- A note on what not to change.

## Positive Evidence Boundary

A strong output may be nominated when the user explicitly values it and an
independent review confirms that it adds evidence beyond merely pleasant
wording.

Use provenance labels:

- `authorized_corpus_evidence`
- `user_authored_exemplar`
- `user_confirmed_synthetic_exemplar`
- `unknown_provenance`

The doctor may nominate, but it may not approve or perform promotion. Successful
outputs do not enter the failure ledger merely for being successful. Preserve
them in validation cases or return a text-only candidate recommendation for
`character-maintainer`.

## Runtime Loop Records

When the diagnosis concerns a live runtime drift, `style-doctor` should write or provide a diagnosis packet using `packages/character-system/shared/templates/diagnosis_packet.template.md`.

If maintainer action is needed, it should also create a handoff packet using `packages/character-system/shared/templates/handoff_packet.template.md` and place the durable record under `packages/character-system/reports/runtime-loop/handoffs/`.

Runtime-loop records must never overwrite prior diagnoses. Use unique filenames with ID, timestamp, character id, and case/task slug:

```text
packages/character-system/reports/runtime-loop/diagnoses/DIAG-YYYYMMDD-001-HHMMSS-<character-id>-<case-or-task>.md
packages/character-system/reports/runtime-loop/handoffs/HANDOFF-YYYYMMDD-001-HHMMSS-<character-id>-<case-or-task>.md
```

Each packet should include its `record_path`. Handoff packets should include `diagnosis_record_path` when available so `character-maintainer` can retrieve the exact diagnosis instead of guessing from the newest file.

Each packet should also include:

- `session_snapshot`: a compact summary of the reviewed interaction, including
  the user feedback and the critical output move.
- `session_storage`: the session/thread/export path or identifier the
  maintainer can inspect later. If no durable session location is available,
  write `not_available` and explain why.
- `character_context`: the load status, character id, load evidence, warning
  flag, user override, and reliability impact. For a forced run without
  confirmed load evidence, this block is mandatory and must remain visibly
  marked as provisional.

This is important because `style-doctor` is often invoked through weaker models.
The maintainer should not have to trust the diagnosis blindly when the original
session context can be referenced.

`style-doctor` does not directly apply patches. Its runtime-loop output should reference `packages/character-system/shared/runtime_loop_policy.md` and `packages/character-system/shared/patch_protocol.md`, then leave accepted/rejected/deferred decisions to `character-maintainer`.

Its drift vocabulary should stay aligned with `packages/character-system/shared/drift_taxonomy.md`. If a new drift type is needed, update shared taxonomy first, then adjust style-doctor prompts or checklists.
