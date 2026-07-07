# Coupling Strategy

The maintainer, generator, and character folders must stay weakly coupled.

## Allowed influence

The maintainer may influence generator quality through:

- Reports.
- Suggestions.
- Patch notes.
- Generalization notes.
- Compatibility findings.

## Forbidden influence

The maintainer must not:

- Directly modify `character-generator`.
- Directly overwrite generator templates.
- Replace a maintained character with a newly generated version.
- Normalize away character-specific evolution just to match current generator output.

## Practical rule

If the problem is inside one character, patch the character. If the lesson may help future generated characters, write a generalization note. If a generator template seems wrong, document the issue and proposed template-level change instead of editing it.

## Cross-system contract

- Generator creates the initial baseline.
- Maintainer preserves and improves the living character.
- Character folder remains the runtime source of truth.
