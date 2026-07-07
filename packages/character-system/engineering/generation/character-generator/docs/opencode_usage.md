# OpenCode Adapter And Exposure

This file documents one platform-specific exposure path. It does not make the generated package OpenCode-owned.

## What OpenCode Receives

OpenCode should receive the generated character folder:

```text
characters/sample-character/
```

This folder contains `SKILL.md`, references, prompts, reports, and a manifest.

## How the Skill Should Behave

The generated `SKILL.md` tells OpenCode:

- When to use the skill.
- When not to use it.
- Which reference files to read.
- How to execute rewrite, continuation, imitation, critique, style transfer, and bounded discussion tasks.
- How to enforce privacy and copyright boundaries.

## Boundary

The skill is not a real-person AI. It is a writing assistant inspired by abstract style patterns.

OpenCode should refuse requests for:

- Identity impersonation.
- Private fact inference.
- Long source reconstruction.
- Contact detail extraction.

## Updating OpenCode Skills

Regenerate the character folder after corpus or config changes, then expose OpenCode to the updated `characters/<character_id>/` folder through the workspace projection model.

Other compatible agents may load the same source folder through their own projection or adapter. Do not copy the generated source to create platform-specific variants.
