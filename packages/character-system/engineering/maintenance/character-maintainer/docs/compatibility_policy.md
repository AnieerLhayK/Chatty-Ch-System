# Compatibility Policy

Generator upgrades should not erase older character quality. Treat compatibility as maintenance of a living artifact, not as forced migration to a new template.

## Upgrade review

When generator behavior or templates change:

1. Compare the character's current structure against the new expected surfaces.
2. Identify missing compatibility fields or changed prompt assumptions.
3. Decide whether the character actually needs a patch.
4. Patch only the missing or conflicting local surface.
5. Record migration notes in `reports/`.

## Legacy characters

Older characters may use different file names or section headings. Preserve them when they work. Add adapter notes or small bridging sections rather than reorganizing the whole folder.

## Template drift

If a new generator template conflicts with a maintained character:

- Do not replace the character file.
- Prefer a local compatibility note.
- Add a generator generalization note if the conflict indicates a broader template issue.

## Validation

After a compatibility patch, check:

- Runtime prompts still point to the correct source of truth.
- Rubric criteria still match the character's voice and style.
- Anti-patterns still guard against observed failures.
- Changelog explains why migration was partial or local.
