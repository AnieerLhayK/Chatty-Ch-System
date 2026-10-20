# style-doctor

Evaluate an actual character response against the rules that were loaded for it.
Use it to explain drift or review a strong response as possible exemplar evidence.

## Inputs And Result

Supply the selected output, original task, feedback, relevant character files
and explicit loading evidence. Reuse context already present in the session.
A character name, path or pasted rules alone does not prove loading. Without
proof, normal diagnosis stops; an explicit request to continue permits a visibly
provisional evaluation only.

The default result is an outcome, short evidence, likely cause/layer, confidence,
maintenance scope, protected behavior and a test of the hypothesis. Specific
candidate wording is available when explicitly requested. Doctor does not apply
patches, decide maintenance acceptance or promote exemplars; character-maintainer
owns that work. Non-character repository or platform problems use their owning
maintenance workflow.

## Modes And Resources

[SKILL.md](SKILL.md) is the operating contract. Focused checklists and prompts
are selected by symptom; [diagnosis detail](docs/runtime_diagnosis.md) covers
layer mapping and provisional context. For a requested positive review, use
[positive exemplar review](prompts/positive_exemplar_review_prompt.md).

Default text_only requires no runtime-loop installation. When formal saved
records or a maintainer handoff are requested in Workspace, follow
[Workspace records](docs/runtime_records.md) under record_write authority and
link the saved Markdown. Otherwise return text and identify any unsaved records.
Exposure never grants source_patch authority.

Standalone release bundles can omit maintainer and runtime-loop infrastructure.
They remain useful for text-only evaluation and maintenance scope. Positive
outputs stay distinct from failure events, and synthetic exemplars stay distinct
from authorized corpus evidence.
