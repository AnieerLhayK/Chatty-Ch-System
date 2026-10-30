# QQ Chat Raw Material Filter

[简体中文](README.zh-CN.md)

The corpus-preparation module inside [Chatty Ch System](https://github.com/AnieerLhayK/Chatty-Ch-System).
It reads QCE v5 JSON exports locally and produces scored JSONL buckets, lexicon audits,
phrase candidates and review samples without modifying raw exports.

## Use

Run from this module directory on Python 3.11+:

```bash
python -m pip install -e .
python qce_block_filter.py --help
python qce_block_filter.py --writer-name sample --me-id 123456789
```

Set `AI_ROOT` to your absolute data root. The authoritative local workspace may instead
supply its configured default through its manifest. Inputs, outputs, lexicons and review
decisions default to `raw_material/qq/exports/character.<writer_name>/` under that root.
`--input-dir` and `--output-dir` override the corresponding paths; relative lexicon
paths still require a root. Use `--dry-run` to parse without writing pipeline output.

## Buckets and handoff

Buckets include `candidates`, `micro_style`, `need_anonymize`, `chaos_style`,
`debatable` and `rejected`. Review and anonymize selected material before handoff.
Convert approved material to `.txt`, `.md` or `.docx` for character-generator;
there is no direct JSONL ingestion. Privacy-related phrases do not automatically
enter an allowed output lexicon. Raw exports, personal lexicons and review decisions
remain outside version control.

## Tests and maintenance

`from qq_raw_filter.corpus_api import read_qce` reads one explicitly supplied
QCE JSON file and returns messages, source SHA-256, parser version and coded
diagnostics. It bypasses character scoring, length thresholds, bucketing and
deduplication. Short, repeated and non-self messages remain available; callers
decide authorship and research selection. Returned text and identifiers remain
private. This reader is not an anonymizer. The character pipeline separately
protects its new exports with the configured mask/private-name/private-place/drop
rules and configured self identifiers, including context, fragments, turns,
rejected buckets, configuration snapshots, debug/review, audit and diagnostic
outputs. Mining exports use a protected copy so sensitive n-gram fragments do
not escape; original in-memory mining still drives scoring and selection.
New lexicon appends are protected, but existing private lexicon contents are not
rewritten or approved for sharing. Export source names become neutral aliases,
and configuration snapshots omit private paths and are not replayable originals.
These are existing-rule masking guarantees, not three-level semantic review or
anonymity. Review residual context before disclosure; research-reader outputs
remain raw and private.

```bash
python -m pytest tests -q
```

Tests use synthetic inputs by default. Live sample tests only run with explicitly
configured `QCE_SAMPLE_DATA_DIR`; never commit those samples.

Maintain this module in its owning package. The system owns portable generation,
checking, documentation and CI; workspace owns host paths, registered remotes,
TASK authorization and aggregate synchronization. The former independent filter
repository is retired; do not maintain another publisher or edit generated checkouts.

The English overview adapts the unmerged
[documentation PR #1](https://github.com/AnieerLhayK/qq-chat-raw-filter/pull/1).
See the Chinese companion for detailed pipeline, parameters and lexicon lifecycle.
