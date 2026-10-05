"""Resolve an optional host data root without importing host implementation."""
from __future__ import annotations

import json
import os
from pathlib import Path

from .config_loader import ConfigValidationError


def _absolute_root(value: str) -> Path:
    if not value.strip() or "${" in value or "{" in value or not Path(value).is_absolute():
        raise ConfigValidationError("AI_ROOT must be a concrete absolute path")
    return Path(value).resolve()


def resolve_ai_root(start: Path | None = None) -> Path | None:
    """Environment wins; inspect at most five parents of the source package."""
    if "AI_ROOT" in os.environ:
        return _absolute_root(os.environ["AI_ROOT"])
    anchor = (start or Path(__file__).resolve().parent.parent).resolve()
    for directory in (anchor, *list(anchor.parents)[:5]):
        manifest = directory / "workspace_manifest.yaml"
        if not manifest.is_file():
            continue
        try:
            data = json.loads(manifest.read_text(encoding="utf-8-sig"))
        except (ValueError, OSError) as exc:
            raise ConfigValidationError(f"Cannot read host manifest: {manifest}") from exc
        value = data.get("external_roots", {}).get("qq_raw_filter_ai_root")
        return _absolute_root(value) if isinstance(value, str) else None
    return None
