import json

import pytest

from qq_raw_filter.corpus_api import read_qce


def test_research_reader_preserves_short_repeated_and_other_messages(tmp_path):
    path = tmp_path / "chat.json"
    path.write_text(json.dumps({"messages": [
        {"id": str(i), "timestamp": 1790000000 + i,
         "sender": {"uid": sender}, "content": {"text": text}}
        for i, (sender, text) in enumerate([("me", "好"), ("me", "好"), ("other", "收到")])
    ]}), encoding="utf-8")
    result = read_qce(path)
    assert [m.text for m in result.messages] == ["好", "好", "收到"]
    assert result.messages[-1].sender_ids == ("other",)
    assert result == read_qce(path)
    assert result.diagnostics == ()
    assert not list(tmp_path.glob("*.jsonl"))


def test_research_reader_diagnoses_invalid_entries_and_unknown_time(tmp_path):
    path = tmp_path / "chat.json"
    path.write_text(json.dumps({"messages": [None, {"text": "short"}]}), encoding="utf-8")
    result = read_qce(path)
    assert result.messages[0].timestamp is None
    assert "qce_unparsed_entries:1" in result.diagnostics
    assert "qce_unknown_timestamp:1" in result.diagnostics
    assert result.messages[0].source_index == 1
    path.write_text("[]", encoding="utf-8")
    with pytest.raises(ValueError, match="qce_expected_object"):
        read_qce(path)


def test_timestamp_string_is_parsed_and_invalid_value_is_not_logged(tmp_path, caplog):
    path = tmp_path / "chat.json"
    path.write_text(json.dumps({"messages": [
        {"text": "one", "timestamp": "2026-10-22T12:00:00+08:00"},
        {"text": "two", "timestamp": "PRIVATE_INVALID_TIMESTAMP"},
        {"text": "three", "timestamp": "2026-10-22 12:00:00"}]}), encoding="utf-8")
    result = read_qce(path)
    assert result.messages[0].timestamp == "2026-10-22T12:00:00+08:00"
    assert result.messages[1].timestamp is None
    assert result.messages[2].timestamp is None
    assert "qce_timezone_unknown:2" in result.diagnostics
    assert "PRIVATE_INVALID_TIMESTAMP" not in caplog.text


def test_structured_non_text_is_not_serialized_into_research_text(tmp_path):
    path = tmp_path / "chat.json"
    path.write_text(json.dumps({"messages": [
        {"type": "type_2", "content": {"file": "PRIVATE_FILENAME", "resources": ["private"]}},
        {"content": {"text": {"unexpected": "PRIVATE_OBJECT"}}},
        {"content": {"elements": [{"data": {"text": "真实文本"}}]}}]}), encoding="utf-8")
    result = read_qce(path)
    assert [m.text for m in result.messages] == ["", "", "真实文本"]
    assert "qce_non_text_payload:0" in result.diagnostics
