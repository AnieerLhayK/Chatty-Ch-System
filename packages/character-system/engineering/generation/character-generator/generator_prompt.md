# generator_prompt.md

Use this prompt with an agent that can run Python, write the configured output directory, inspect Git state, and validate the generated package.

## Conversational Personal-Corpus Prompt

Use this first for normal personal-character builds:

```text
Use character-generator.

I want to create a style-inspired character skill from authorized corpus
sources. Use conversational intake and do not make me hand-write JSON.

Required information:

1. Character identity
- Character id, if already decided:
- Display name / user-facing label:

2. Authorized corpus sources
- Source path(s):
- Source type(s): work / chat / notes / profile / mixed / unknown
- Source role(s): long-form style, friend-chat core, critique voice, background orientation, etc.
- Include each source in style extraction: yes / no
- Generate README for each source: yes / no
- Speaker/context-note rules:

3. Authorization and privacy
- I confirm I am authorized to use these sources: yes / no
- I accept style-inspired output only, not identity impersonation: yes / no
- I accept no private fact inference and no verbatim reconstruction: yes / no

4. Target use
- Target tasks or interaction type:
- Typical user situation:
- Desired language:

Optional information:
- Preferred output folder:
- Privacy level:
- Style strength:
- Quote policy or max quote length:
- Personal profile / background orientation:
- Desired relationship posture:
- Source normalization preferences:
- Extra forbidden tasks or postures:
- Whether reports should hide external local paths:

Additional requirements:
- The generated character should be especially good at:
- It should avoid sounding like:
- Examples of outputs I would consider successful:
- Topics or boundaries that need extra care:
- Anything else I want the build plan to preserve:
```

The agent should collect required information conversationally, then write an
ignored local intake or plan file and run:

```bash
python scripts/build_character.py --intake configs/_private/<character>.intake.json
```

If required information is missing, stop with a missing-info report. If only
optional information is missing, continue with safe defaults and report the
quality gaps at the end.

## Standard Config Prompt

请按照 character-generator workflow，读取 `configs/sample-character.json`，生成 sample-character 的风格启发型数字人 skill。

## What The Agent Should Do

When receiving a request like the above, the agent should:

1. Decide whether the request is conversational intake or explicit config mode.
2. For conversational intake, check required fields before generating. Do not
   guess authorization, corpus paths, privacy acceptance, or target tasks.
3. For config mode, locate the requested config file, such as `configs/sample-character.json`.
4. If the config is missing, stop and ask for a config or conversational intake. Do not guess values or continue generation.
5. Read only the declarative fields needed from config:
   - `character_id`
   - `display_name`
   - `corpus_path`
   - `corpus_sources`
   - `output_path`
   - `privacy_level`
   - `style_strength`
   - `target_tasks`
   - `forbidden_tasks`
   - `quote_policy`
   - `max_quote_chars`
6. Run:

```bash
python scripts/build_character.py --config configs/sample-character.json
```

7. Confirm that the output folder exists:

```text
characters/sample-character/
```

8. Confirm the generated package includes:
   - `SKILL.md`
   - `README.md`
   - `references/`
   - `prompts/`
   - `reports/`
   - `reports/corpus_reading_handoff.md` when source planning is active
   - `output_manifest.json`

## Missing Config Behavior

If the user explicitly asks for config mode for a character such as `bob`, but `configs/bob.json` does not exist, the invoking agent must stop and respond:

```text
请先创建 configs/bob.json，或者复制 configs/character_config.example.json 后填写完整配置。配置完成后再重新运行 workflow。
```

The agent must not infer corpus paths, display names, privacy settings, authorization, privacy acceptance, or task lists for missing configs or intake.

## Boundary

This workflow creates a style-inspired writing and bounded discussion skill. It must not create a real-person identity simulator, impersonation bot, private-fact inference tool, private chatbot, or corpus reconstruction tool.
