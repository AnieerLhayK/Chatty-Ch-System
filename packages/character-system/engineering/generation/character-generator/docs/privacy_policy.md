# Privacy Policy

## Scope

This policy applies to `character-generator` and every character skill it generates.

The workflow accepts public or authorized corpora. It must not be used to expose private data or create a real-person identity simulator.

## Required Protections

The generator must redact:

- Phone numbers.
- Email addresses.
- URLs.
- Chinese ID numbers.
- QQ, WeChat, or similar account hints.
- Address-like phrases.
- Contextual Chinese names when high privacy mode is enabled.

## High Privacy Mode

When `privacy_level` is `high`, anonymization should be more aggressive. It may remove or mask borderline personal identifiers even when doing so slightly reduces stylistic fidelity.

## Copyright Boundary

The workflow should favor:

- Abstract style rules.
- Statistical and structural summaries.
- Newly created examples.
- Short sanitized fragments only when useful.

Default quote limit is 80 characters. Long corpus reconstruction is forbidden.

## Identity Boundary

Generated skills must not:

- Claim to be a real person.
- Speak as a real person.
- Infer private facts.
- Reconstruct unavailable or protected text.
- Encourage users to believe they are interacting with the source person.

## Reporting

Privacy reports should include redaction counts, not raw sensitive values.

Source planning reports should not expose private absolute corpus paths unless
the build is explicitly local-only. For reusable examples, templates, and
committed configs, use workspace-relative or placeholder paths.

Source README files may live beside private corpora. They should describe
source roles, speaker rules, cleanup policy, and privacy boundaries, but they
must not quote long private excerpts or turn profile facts into impersonation
instructions.
