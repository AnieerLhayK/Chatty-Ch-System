#!/usr/bin/env python3
"""Validate that this public package contains no private character artifacts."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_PATHS = {
    "README.md",
    ".github/workflows/ci.yml",
    "packages/character-system/engineering/generation/character-generator/SKILL.md",
    "packages/character-system/engineering/diagnosis/style-doctor/SKILL.md",
    "packages/character-system/engineering/maintenance/character-maintainer/SKILL.md",
    "packages/character-system/shared/protocol_manifest.json",
    "shared/delivery_output_policy.md",
}

FORBIDDEN_PATHS = {
    "packages/character-system/runtime",
    "packages/character-system/reports",
    "packages/character-system/distribution",
    "packages/character-system/engineering/generation/character-generator/configs/writerA.json",
    "packages/character-system/engineering/corpus-preparation/qq-raw-material-filter",
}

FORBIDDEN_TEXT = [
    re.compile(r"D:[\\/]+AI", re.IGNORECASE),
    re.compile(r"C:[\\/]+Users[\\/]+Z1377", re.IGNORECASE),
    re.compile(r"packages/character-system/runtime/characters", re.IGNORECASE),
    re.compile(r"zyc-toolkit", re.IGNORECASE),
    re.compile(r"\bZYC\b"),
    re.compile(r"\bzyc\b"),
]

SKIP_TEXT_SCAN = {
    "scripts/check_public_package.py",
}

TEXT_SUFFIXES = {".json", ".md", ".py", ".txt", ".yaml", ".yml", ".toml", ".gitignore"}


def is_text(path: Path) -> bool:
    return path.name == ".gitignore" or path.suffix.lower() in TEXT_SUFFIXES


def check_required(root: Path) -> list[str]:
    return [f"Missing required path: {rel}" for rel in sorted(REQUIRED_PATHS) if not (root / rel).is_file()]


def check_forbidden_paths(root: Path) -> list[str]:
    issues = []
    for rel in sorted(FORBIDDEN_PATHS):
        if (root / rel).exists():
            issues.append(f"Forbidden path exists: {rel}")
    return issues


def check_text(root: Path) -> list[str]:
    issues = []
    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts or not is_text(path):
            continue
        rel = path.relative_to(root).as_posix()
        if rel in SKIP_TEXT_SCAN:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for pattern in FORBIDDEN_TEXT:
            match = pattern.search(text)
            if match:
                line = text[: match.start()].count("\n") + 1
                issues.append(f"{rel}:{line}: forbidden text matched {pattern.pattern!r}")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", default=".", help="Repository root to validate.")
    args = parser.parse_args()
    root = Path(args.dir).resolve()

    issues = []
    issues.extend(check_required(root))
    issues.extend(check_forbidden_paths(root))
    issues.extend(check_text(root))

    if issues:
        print("FAILED: public package boundary check found issues:")
        for issue in issues:
            print(f"  - {issue}")
        return 1
    print("PASSED: public package boundary check.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
