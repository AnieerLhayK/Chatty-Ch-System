# Evolution Strategy

Character maintenance is cumulative. Every useful patch should leave a trail that future maintainers can trust.

## Evolution record

Each patch should record:

- Trigger: feedback, audit finding, generator upgrade, comparison result, or rubric failure.
- Diagnosis: what failed and which surface caused it.
- Change: files and sections changed.
- Expected effect: what should improve in output.
- Validation: how the maintainer checked the patch.
- Generalization: whether the lesson belongs only to this character or should inform generator guidance.

## Preserve human refinements

Treat manual edits, nuanced examples, and previous changelog decisions as high-value context. Do not flatten them into generic style rules.

## Avoid evolution debt

Do not accumulate vague instructions such as "be more human" or "sound natural". Convert them into concrete patterns, anti-patterns, rubric checks, or task prompt adjustments.

## Healthy evolution signs

- Fewer contradictions between prompts and references.
- More precise anti-patterns with replacement behavior.
- Rubrics that catch actual observed failures.
- Changelog entries that explain why a choice exists.
- Character voice that becomes more stable without becoming rigid.
