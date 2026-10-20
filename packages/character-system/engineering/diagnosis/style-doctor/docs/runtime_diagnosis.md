# Diagnosis Detail

Use [SKILL.md](../SKILL.md) for scope, load gates and the evaluation sequence.
This reference supplies layer mapping, context fields and optional fuller output
formats. Load only the section needed for the current evaluation.

## Layer Selection

Locate the first observable move where the output diverges from the loaded
rules. Separate task success, voice success and context uncertainty. Attribute
the failure only as far as the supplied evidence supports.

| Surface | Evidence to inspect |
| --- | --- |
| SKILL.md / prompts / task_recipes | Routing, active instructions and task-specific behavior |
| voice_card | Relational posture, stance and voice identity |
| style_profile / writing_patterns | Diction, rhythm, image function and paragraph movement |
| anti_patterns | An observed recurring habit the existing rules fail to constrain |
| evaluation_rubric | A demonstrated failure the existing evaluation misses |

Use the character's actual paths, including dedicated rhythm/imagery files when
present. These are hypotheses, not a mandatory patch order. One output can be a
generation miss without proving a source defect. A character's intentional
roughness, silence or directness is not drift by itself.

## Character Context Block

Include all six fields below in every diagnosis/handoff packet, including packet
text returned without writing. For normal evaluation use confirmed, false, false
and the actual character id, load evidence and reliability impact.

On an explicit user override without load confirmation, show this block in the
chat response and every packet. Use unconfirmed when a character is named but
not verified; otherwise use missing. Keep an unknown character_id empty.

```yaml
character_context:
  status: missing
  character_id:
  load_evidence: no explicit character-load evidence found in upstream context
  context_warning: true
  user_override: true
  impact: character-specific conclusions are provisional and may be invalid
```

A provisional evaluation may identify textual mechanisms and uncertainty; it
cannot establish the named character's runtime behavior. Withhold a character
pass/drift or exemplar verdict rather than forcing one of the confirmed-context
classifications. Do not infer private facts or a missing identity to complete
the block.

## Optional Fuller Response

Default to a compact answer that includes the outcome, concrete evidence,
likely cause/layer and confidence, maintenance scope, protected behavior and a
hypothesis-testing check. Expand only when the task warrants it:

```markdown
**Outcome And Context**
<drift_candidate / pass / strong_pass / exemplar_candidate; source/load evidence>

**Evidence And Cause**
<minimum excerpt, rule mismatch, likely layer, confidence and alternatives>

**Maintenance Scope**
<smallest responsible section and the intended behavior change>

**Preserve And Check**
<working behavior to protect; a prompt or comparison that tests the hypothesis>
```

Specific replacement text uses the opt-in
[candidate wording prompt](../prompts/patch_suggestion_prompt.md). A handoff can
use scope and intended behavior without pre-writing the maintainer's patch.
Durable Workspace records follow [runtime_records.md](runtime_records.md).
