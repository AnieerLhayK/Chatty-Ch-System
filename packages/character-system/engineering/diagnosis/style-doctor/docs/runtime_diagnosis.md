# Runtime Evaluation And Diagnosis

Runtime evaluation starts from the actual output and user response, not from an abstract idea of the character. Most evaluations diagnose failure; unusually strong outputs may instead become positive evidence candidates.

Runtime evaluation is only for character skill outputs. Workspace governance,
manifest, release, platform exposure, migration, script, CI, Git, or repository
maintenance issues are out of scope and should be routed to workspace task
resolution instead of `style-doctor`.

## Inputs

- Active character skill context.
- Current generated output.
- User feedback.
- Any task constraints that shaped the output.

## Method

1. Preserve the user's wording.
2. Identify the first sentence or move where the character breaks.
3. Separate task success from voice success.
4. Classify the failure: AI smell, drift, rhythm, emotion, imagery, or prompt failure.
5. Map the failure to a likely layer.
6. Suggest the smallest patch that would have prevented this exact failure.

For a successful output:

1. Classify it as `pass`, `strong_pass`, or `exemplar_candidate`.
2. Identify concrete mechanisms rather than praising the passage generally.
3. Verify provenance, factual fidelity, privacy, originality, safety, and maintainability.
4. Check whether it merely repeats existing guidance or adds useful evidence.
5. Send any promotion recommendation to `character-maintainer`.

## Authority Boundary

Runtime diagnosis stops before maintenance. It may produce diagnosis and handoff records, but it should not edit character files, write patch notes, update the patch ledger, or decide accepted/rejected/deferred.

Suggested patch text is candidate material for `character-maintainer`, not an applied patch.

Positive evaluation also stops before maintenance. The doctor may nominate an
exemplar but cannot insert it into references, authorize it as corpus, or make
the maintainer's promotion decision.

## Layer Map

`voice_card` defines who is speaking and the basic relational posture.

`style_profile` defines how the voice moves: rhythm, syntax, image density, emotional indirectness, and texture.

`anti_patterns` defines what must not happen, ideally with concrete bad examples.

`evaluation_rubric` defines how outputs are judged and what failures should be caught before delivery.

`prompts` define runtime instruction priority and failure handling.

`task_recipes` define how the character behaves in specific tasks.

## Good Diagnosis

A good diagnosis is narrow, evidenced, and maintainable. It explains why the output failed, not just that it failed.

When a diagnosis is saved, it should be a Markdown packet in the default
runtime-loop directories, not just text in the conversation. Saved packets must
include a concise `session_snapshot` and a `session_storage` pointer when
available. If the session cannot be referenced later, state that explicitly.
This lets `character-maintainer` re-check the evidence, especially when the
diagnosis was produced by a weaker model.

## Bad Diagnosis

A bad diagnosis says only "make it more target character", recommends more poetic language, or rewrites the whole character without locating the failed layer.

A bad positive review says only "this is beautiful", copies the whole passage
into references, ignores provenance, or treats one model-generated success as
proof of authentic character biography.
