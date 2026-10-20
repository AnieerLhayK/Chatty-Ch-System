# Runtime Feedback Prompt

Use for live feedback on a selected character output. Load
[SKILL.md](../SKILL.md) first; its scope, load-evidence and authority gates apply.

Read the output, original task, exact feedback and relevant loaded rules already
available in the interaction. Ask only for missing evidence that changes the
evaluation. Give a compact outcome and explanation:

- For drift, identify evidence, likely cause/layer, confidence, smallest
  maintenance scope, protected behavior and a way to test the hypothesis.
- For a requested positive review, use
  [positive_exemplar_review_prompt.md](positive_exemplar_review_prompt.md).

Stop at evaluation and scope. Add specific candidate wording only when
explicitly requested. A request to diagnose does not itself request durable
Workspace records; use the saved-record branch only when requested.
