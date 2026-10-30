"""Public CLI regressions: synthetic values only, including derived CJK fragments."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tomllib

from qq_raw_filter.config_loader import default_config, snap_config


def test_public_cli_protects_all_new_outputs_and_diagnostics(tmp_path):
    source_dir, output = tmp_path / "inputs", tmp_path / "outputs"
    source_dir.mkdir()
    marker = "隐私甲乙丙丁"
    messages = []
    for i in range(12):
        messages.append({"id": str(i), "timestamp": 1700000000 + i * 1000,
                         "sender": {"uid": "900001234", "name": "CanaryOwner"}, "type": "type_1",
                         "content": {"text": f"普通表达保留。{marker}。CANARYMASK。MASKVIALEXICON。CANARYDROP。普通表达保留。Sometimes ordinary names remain meaningful."}})
        messages.append({"id": f"other-{i}", "timestamp": 1700000001 + i * 1000,
                         "sender": {"uid": "other", "name": "CanaryOther"}, "type": "type_1",
                         "content": {"text": marker}})
    (source_dir / "CanaryOwner.json").write_text(json.dumps({"chatInfo": {"selfUid": "900001234", "selfName": "CanaryOwner", "type": "private"}, "messages": messages}), encoding="utf-8")
    cfg = default_config()
    cfg["character"]["writer_name"] = "CanaryOwner"
    cfg["identity"] = {"me_ids": ["900001234"], "me_names": ["CanaryOwner", "Me"]}
    cfg["path"].update({"input_dir": str(source_dir), "output_dir": str(output)})
    cfg["filter"].update({"private_names": [marker, "CanaryOwner", "CanaryOther"], "mask_words": ["CANARYMASK"], "drop_sentence_words": ["CANARYDROP"]})
    cfg["phrase_mining"].update({"enabled": True, "min_freq": 1})
    cfg["phrase_mining"].update({"min_entropy": 0, "min_pmi_2gram": 0, "min_pmi_3gram": 0, "min_pmi_4gram": 0})
    cfg["phrase_mining"]["keyness"]["enabled"] = False
    archive = tmp_path / "CanaryOwner-archive.jsonl"
    archive.write_text("\n".join(json.dumps({"phrase": term, "old_category": "privacy.names", "source_file": "PrivateClientFile.jsonl"}) for term in (marker, marker[:3], marker[-3:])) + "\n", encoding="utf-8")
    cfg["lexicon"]["archive"]["mask_words_path"] = str(archive)
    masks = tmp_path / "masks.jsonl"
    masks.write_text(json.dumps({"phrase": "MASKVIALEXICON"}) + "\n", encoding="utf-8")
    cfg["lexicon"]["mask_words_path"] = str(masks)
    auto = tmp_path / "appends" / "new.jsonl"
    auto.parent.mkdir()
    cfg["lexicon"]["phrase_candidates_path"] = str(auto)
    cfg["my_block"].update({"min_my_block_chars": 1, "min_my_msg_count": 1, "min_my_char_ratio": 0})
    config = tmp_path / "settings.toml"
    config.write_text(snap_config(cfg), encoding="utf-8")
    env = {**os.environ, "AI_ROOT": str(tmp_path), "PYTHONIOENCODING": "utf-8"}
    result = subprocess.run([sys.executable, "qce_block_filter.py", "--config", str(config), "--debug"], cwd=Path(__file__).parents[1], env=env, capture_output=True, text=True, encoding="utf-8")
    assert result.returncode == 0, result.stderr
    files = list(output.rglob("*"))
    assert any(p.name == "rejected.jsonl" for p in files)
    assert any(p.name == "debug_sessions.jsonl" for p in files)
    assert any(p.name == "legacy_lexicon_frequency_audit.jsonl" for p in files)
    assert any(p.name == "rejected_high_style_score_sample.jsonl" for p in files) or any("sample" in p.name for p in files)
    content = result.stdout + result.stderr + "\n".join(p.read_text(encoding="utf-8") for p in files if p.is_file())
    assert auto.is_file() and auto.stat().st_size, "The enabled lexicon append exit must actually execute"
    content += auto.read_text(encoding="utf-8")
    snapshot = next(p for p in files if p.name == "active_config.toml")
    assert "time" in tomllib.loads(snapshot.read_text(encoding="utf-8"))
    for value in [marker, "CanaryOwner", "CanaryOther", "PrivateClientFile.jsonl", "900001234", "CANARYMASK", "MASKVIALEXICON", "CANARYDROP", "隐私甲", "乙丙丁"]:
        assert value not in content, value
    assert "普通表达" in content
    rejected = next(p for p in files if p.name == "rejected.jsonl")
    assert any("Sometimes ordinary names remain meaningful." in json.loads(line)["my_text"] for line in rejected.read_text(encoding="utf-8").splitlines())


def test_integer_identity_is_protected_in_config_and_all_cli_outputs(tmp_path):
    source, output = tmp_path / "input", tmp_path / "output"
    source.mkdir()
    (source / "chat.json").write_text(json.dumps({"chatInfo": {"selfUid": "876543210", "selfName": "Me", "type": "private"}, "messages": [{"id": "1", "timestamp": 1700000000, "sender": {"uid": "876543210", "name": "Me"}, "type": "type_1", "content": {"text": "Ordinary content for a synthetic sample."}}]}), encoding="utf-8")
    cfg = default_config()
    cfg["character"]["writer_name"] = "sample"
    cfg["identity"] = {"me_ids": [876543210], "me_names": ["Me"]}
    cfg["path"].update({"input_dir": str(source), "output_dir": str(output)})
    config = tmp_path / "filter.toml"
    config.write_text(snap_config(cfg), encoding="utf-8")
    result = subprocess.run([sys.executable, "qce_block_filter.py", "--config", str(config), "--include-all-speakers"], cwd=Path(__file__).parents[1], env={**os.environ, "AI_ROOT": str(tmp_path), "PYTHONIOENCODING": "utf-8"}, capture_output=True, text=True, encoding="utf-8")
    assert result.returncode == 0, result.stderr
    snapshots = list(output.rglob("active_config.toml"))
    assert len(snapshots) == 1
    contents = result.stdout + result.stderr + "\n".join(p.read_text(encoding="utf-8") for p in output.rglob("*") if p.is_file())
    assert "876543210" not in contents
