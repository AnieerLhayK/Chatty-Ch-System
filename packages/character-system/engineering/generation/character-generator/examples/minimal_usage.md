# Minimal Usage

## 1. Prepare Corpus

Create:

```text
corpus/sample-character/
```

Add authorized `.txt`, `.md`, or `.docx` files.

## 2. Check Config

Use:

```text
configs/sample-character.json
```

Or copy:

```text
configs/character_config.example.json
```

to:

```text
configs/newWriter.json
```

Then edit `character_id`, `display_name`, `corpus_path`, and `output_path`.

## 3. Build

Follow [the skill contract](../SKILL.md) before execution: verify the explicit
output target is new or generator-owned. A manually evolved character uses
character-maintainer rather than being overwritten by this command.

```bash
python scripts/build_character.py --config configs/sample-character.json
```

## 4. Expose Output

Expose the same source folder to any compatible local-skill platform:

```text
characters/sample-character/
```

The generated skill is style-inspired. It must not be used as a real-person simulator.
