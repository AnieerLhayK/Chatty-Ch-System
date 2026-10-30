"""Existing-rule output protection, independent of model-based de-identification.

Views are copies: source provenance, selection and research-reader values stay private.
"""
from __future__ import annotations

import copy
import logging
import re


class ExportPrivacy:
    def __init__(self, config):
        flt = config.get("filter", {})
        values = [str(v) for key in ("mask_words", "private_names", "private_places", "drop_sentence_words") for v in flt.get(key, []) if v]
        lexicon = config.get("_lexicon", {})
        values += [str(v) for key in ("mask_phrases", "drop_sentence_phrases") for v in lexicon.get(key, []) if v]
        explicit_values = set(values)
        values += [str(v) for key in ("me_ids", "me_names") for v in config.get("identity", {}).get(key, []) if v]
        writer = config.get("character", {}).get("writer_name")
        if writer:
            values.append(str(writer))
        patterns = []
        for value in sorted(set(values), key=len, reverse=True):
            pattern = re.escape(value)
            if value not in explicit_values and value.isascii():
                pattern = r"(?<![A-Za-z0-9_])" + pattern + r"(?![A-Za-z0-9_])"
            patterns.append(pattern)
        self.pattern = re.compile("|".join(patterns), re.I) if patterns else None
        self.cjk_fragments = {v[i:i + n] for v in values for n in (2, 3, 4) for i in range(len(v) - n + 1)
                              if all("\u3400" <= c <= "\u9fff" for c in v[i:i + n])}
        self.sources = {}

    def text(self, value):
        return self.pattern.sub("[MASKED]", value) if self.pattern else value

    def source(self, value):
        if value not in self.sources:
            self.sources[value] = f"source-{len(self.sources) + 1:04d}"
        return self.sources[value]

    def data(self, value, field=""):
        if isinstance(value, (int, float)) and not isinstance(value, bool) and field in {"me_ids", "speaker_uid", "speaker_uin", "uid", "uin"}:
            protected = self.text(str(value))
            return protected if protected != str(value) else value
        if isinstance(value, str):
            if field in {"term", "phrase"} and any(fragment in value for fragment in self.cjk_fragments):
                return "[MASKED]"
            if field in {"source_file", "all_source_files", "source_files", "filename", "file_path"}:
                return self.source(value)
            if field.endswith(("_path", "_dir")) or field in {"ai_root", "root"}:
                return "[PRIVATE_PATH]" if value else value
            return self.text(value)
        if isinstance(value, dict):
            result = {}
            for key, child in value.items():
                # Fixed schema keys are code, not corpus text. In particular a
                # nickname such as "Me" must not corrupt "time" or "metrics".
                safe_key = self.source(key) if field == "by_source_file" else key
                if safe_key in result:
                    safe_key = f"{safe_key}_{len(result)}"
                result[safe_key] = self.data(child, key)
            return result
        if isinstance(value, (list, tuple, set)):
            return [self.data(v, field) for v in value]
        if hasattr(value, "__slots__"):
            cloned = copy.copy(value)
            for name in value.__slots__:
                if hasattr(value, name):
                    setattr(cloned, name, self.data(getattr(value, name), name))
            return cloned
        return value


def privacy_for(ctx):
    if "_export_privacy" not in ctx:
        ctx["_export_privacy"] = ExportPrivacy(ctx["config"])
    return ctx["_export_privacy"]


class PrivacyLogFilter(logging.Filter):
    """Protect diagnostics too; untrusted exception payloads never become tracebacks."""
    def __init__(self):
        super().__init__()
        self.privacy = ExportPrivacy({})

    def filter(self, record):
        if not record.name.startswith("qq_raw_filter"):
            return True
        if record.exc_info:
            message = "pipeline_exception (details withheld)"
        else:
            message = self.privacy.text(record.getMessage())
            message = re.sub(r"[A-Za-z]:[/\\][^\r\n,;]*", "[PRIVATE_PATH]", message)
        record.msg, record.args = message, ()
        record.exc_info = record.exc_text = None
        return True
