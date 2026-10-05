"""Host defaults are data, and standalone failures must precede output writes."""
import json
from pathlib import Path

import pytest

from qq_raw_filter.config_loader import ConfigValidationError, default_config, resolve_paths
from qq_raw_filter.host_paths import resolve_ai_root
from qq_raw_filter import _cli


def test_environment_overrides_host_manifest(tmp_path, monkeypatch):
    (tmp_path / "workspace_manifest.yaml").write_text(json.dumps({"external_roots": {
        "qq_raw_filter_ai_root": str(tmp_path / "host")}}), encoding="utf-8")
    monkeypatch.setenv("AI_ROOT", str(tmp_path / "override"))
    assert resolve_ai_root(tmp_path) == tmp_path / "override"


def test_host_root_is_discovered_without_cwd_dependency(tmp_path, monkeypatch):
    monkeypatch.delenv("AI_ROOT", raising=False)
    (tmp_path / "workspace_manifest.yaml").write_text(json.dumps({"external_roots": {
        "qq_raw_filter_ai_root": str(tmp_path / "materials")}}), encoding="utf-8")
    nested = tmp_path / "a/b/c/d/e"
    nested.mkdir(parents=True)
    assert resolve_ai_root(nested) == tmp_path / "materials"
    too_deep = nested / "f"
    too_deep.mkdir()
    assert resolve_ai_root(too_deep) is None


@pytest.mark.parametrize("value", ["", "relative", "${WORKSPACE_ROOT}"])
def test_invalid_environment_roots_fail(value, monkeypatch):
    monkeypatch.setenv("AI_ROOT", value)
    with pytest.raises(ConfigValidationError, match="absolute"):
        resolve_ai_root()


def test_relative_paths_need_a_root():
    cfg = default_config()
    cfg["character"]["writer_name"] = "sample"
    with pytest.raises(ConfigValidationError, match="AI_ROOT"):
        resolve_paths(cfg, None)


def test_absolute_paths_work_without_host(tmp_path):
    cfg = {"character": {"writer_name": "sample"},
           "path": {"input_dir": str(tmp_path / "input"), "output_dir": str(tmp_path / "output")},
           "lexicon": {"phrase_bank_path": str(tmp_path / "lexicon.jsonl")},
           "review": {"decisions_path": str(tmp_path / "review.jsonl")}}
    assert resolve_paths(cfg, None)["path"]["output_dir"] == str(tmp_path / "output")


def test_cli_missing_root_does_not_create_output(tmp_path, monkeypatch):
    monkeypatch.setattr(_cli, "resolve_ai_root", lambda: None)
    output = tmp_path / "output"
    assert _cli.main(["--writer-name", "sample", "--me-id", "123", "--output-dir", str(output)]) == 1
    assert not output.exists()


def test_help_does_not_resolve_paths(monkeypatch):
    monkeypatch.setenv("AI_ROOT", "${UNRESOLVED}")
    with pytest.raises(SystemExit) as result:
        _cli.main(["--help"])
    assert result.value.code == 0


@pytest.mark.parametrize("empty", [False, True])
def test_standalone_cli_absolute_paths(tmp_path, monkeypatch, empty):
    cfg = default_config()
    cfg["character"]["writer_name"] = "sample"
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    output = tmp_path / "output"
    cfg["path"].update(input_dir=str(input_dir), output_dir=str(output))
    for key, value in cfg["lexicon"].items():
        if isinstance(value, dict):
            for nested in value:
                if isinstance(value[nested], str):
                    value[nested] = str(tmp_path / f"{key}-{nested}.jsonl")
        elif isinstance(value, str):
            cfg["lexicon"][key] = str(tmp_path / f"{key}.jsonl")
    cfg["review"]["decisions_path"] = str(tmp_path / "review.jsonl")
    if empty:
        cfg["lexicon"]["phrase_bank_path"] = ""
    monkeypatch.setattr(_cli, "resolve_ai_root", lambda: None)
    monkeypatch.setattr(_cli, "load_config", lambda *_: cfg)
    status = _cli.main(["--writer-name", "sample", "--me-id", "123", "--dry-run"])
    assert status == (1 if empty else 0)
    assert not output.exists()
