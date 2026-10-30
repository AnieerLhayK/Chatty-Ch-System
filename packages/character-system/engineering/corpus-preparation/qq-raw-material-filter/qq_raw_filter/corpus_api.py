"""Lossless research intake; never runs the character-selection pipeline.

Identifiers and text returned here are PRIVATE source data, not anonymized data.
Only explicitly supplied files are read. Repeated messages remain separate.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from hashlib import sha256
import json
from pathlib import Path

from .qce_parser import _extract_text_from_content, _parse_single_message

PARSER_VERSION = "qce-corpus/1"


@dataclass(frozen=True)
class CorpusMessage:
    source_index: int
    message_id: str
    sequence: str
    text: str
    timestamp: str | None
    source_timestamp: object
    sender_ids: tuple[str, ...]
    sender_name: str
    message_type: str
    is_system: bool
    is_recalled: bool


@dataclass(frozen=True)
class CorpusRead:
    messages: tuple[CorpusMessage, ...]
    source_sha256: str
    parser_version: str
    diagnostics: tuple[str, ...]


def read_qce(path: str | Path) -> CorpusRead:
    """Read one QCE JSON file, preserving short/repeated/non-self messages.

    Raises ValueError for unreadable/malformed documents. Missing timestamps and
    unsupported entries are diagnosed without echoing private source values.
    The caller, not this reader, decides authorship and sample inclusion.
    """
    path = Path(path)
    try:
        raw = path.read_bytes()
        value = json.loads(raw.decode("utf-8-sig"))
    except (OSError, UnicodeError, ValueError) as error:
        raise ValueError("qce_unreadable_or_invalid_json") from error
    if not isinstance(value, dict):
        raise ValueError("qce_expected_object")
    rows = value.get("messages", value.get("data", value.get("list")))
    if not isinstance(rows, list):
        raise ValueError("qce_expected_message_list")
    if value.get("chatInfo") is not None and not isinstance(value["chatInfo"], dict):
        raise ValueError("qce_invalid_chat_info")
    diagnostics = []
    skipped = 0
    messages = []
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            skipped += 1
            continue
        try:
            message = _parse_single_message(row)
        except (TypeError, ValueError, AttributeError, OverflowError):
            diagnostics.append(f"qce_invalid_message:{index}")
            skipped += 1
            continue
        if message is None:
            skipped += 1
            continue
        source_time = row.get("timestamp") or row.get("time") or row.get("msgTime")
        at = message.datetime_obj.isoformat() if message.datetime_obj and message.timestamp_ms else None
        if isinstance(source_time, str) and not source_time.strip().lstrip("+-").isdigit():
            try:
                parsed_time = datetime.fromisoformat(source_time.replace("Z", "+00:00"))
                at = parsed_time.isoformat() if parsed_time.tzinfo is not None else None
                if parsed_time.tzinfo is None:
                    diagnostics.append(f"qce_timezone_unknown:{index}")
            except ValueError:
                at = None
        if at is None:
            diagnostics.append(f"qce_unknown_timestamp:{index}")
        content = row.get("content") or row.get("message") or row.get("msgContent") or {}
        text = _extract_text_from_content(content, strings_only=True)
        if not text:
            text = next((row[key] for key in ("text", "message", "msg", "content")
                         if isinstance(row.get(key), str) and row[key]), "")
        if not text and (content or message.msg_type != "text"):
            diagnostics.append(f"qce_non_text_payload:{index}")
        messages.append(CorpusMessage(
            index, message.msg_id, message.seq, text, at, source_time,
            tuple(dict.fromkeys(item for item in (message.sender_uid, message.sender_uin) if item)),
            message.sender_name, message.msg_type, message.is_system, message.is_recalled,
        ))
    if skipped:
        diagnostics.append(f"qce_unparsed_entries:{skipped}")
    return CorpusRead(tuple(messages), sha256(raw).hexdigest(), PARSER_VERSION, tuple(diagnostics))
