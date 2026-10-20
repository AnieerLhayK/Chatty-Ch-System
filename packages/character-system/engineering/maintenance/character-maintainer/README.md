# character-maintainer

Maintain an existing character skill while preserving its manual refinements and
working examples. Start from an explicit maintenance goal or an exact linked
Doctor diagnosis/handoff; a direct request does not require running Doctor first.

## Inputs And Result

Supply the target source/version, maintenance goal and relevant evidence.
Behavioral repairs use actual input/output and feedback when available; offline
alignment uses source contradictions. Follow linked records precisely instead of
selecting the newest one. Missing material evidence produces a specific request
or deferral rather than a speculative edit.

Return a focused proposal or authorized patch with its reason, affected files,
protected behavior, regression checks and evidence gaps. Saving a new version
does not demonstrate improved runtime output. Preserve character-specific files
and conventions instead of replacing them with generator output.

## Modes And Resources

[SKILL.md](SKILL.md) defines scope and execution modes. Default text_only returns
a proposal. Source patches require an explicit request, verified source/scope,
relevant Git state and a validation method under the host's authority rules.
Record_write covers maintenance notes and permitted decisions/ledgers.

For a formal Workspace runtime-loop handoff, follow
[runtime handoff](docs/runtime_handoff.md): verify the linked evidence, record
accepted/rejected/deferred, and maintain the established patch/validation trail.
This branch is conditional, not a prerequisite for every maintenance request.

[Architecture](docs/architecture.md) maps responsible layers. Focused prompts and
checklists cover offline audits, feedback repairs and version comparison.
[Compatibility](docs/compatibility_policy.md) handles generator upgrades without
normalizing mature characters. Only validated, reviewed broader lessons enter
the generalization backlog; maintainer never edits generator assets directly.
