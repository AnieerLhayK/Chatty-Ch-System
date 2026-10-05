"""Validate the unified public system, using its owner-local content contract."""
from __future__ import annotations

import argparse
import json
import re
import stat
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONTRACT = json.loads((HERE / "public_contract.json").read_text(encoding="utf-8"))
REQUIRED_PATHS = set(CONTRACT["required_paths"])
FORBIDDEN_PATHS = set(CONTRACT["forbidden_paths"])
FORBIDDEN_PATTERNS = [re.compile(pattern, re.IGNORECASE) for pattern in CONTRACT["forbidden_text"]]
TEXT_SUFFIXES = {".json", ".md", ".py", ".txt", ".yaml", ".yml", ".toml", ".gitignore"}


def linked(path: Path) -> bool:
    return path.is_symlink() or bool(getattr(path.lstat(), "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT)


def check_required(root: Path) -> list[str]:
    return [f"Missing required path: {relative}" for relative in sorted(REQUIRED_PATHS)
            if not (root / relative).is_file()]


def check_forbidden_paths(root: Path) -> list[str]:
    if any(linked(entry) for entry in (*reversed(root.parents), root)):
        return [f"Forbidden linked root: {root}"]
    issues = []
    allowed_roots = set(CONTRACT["allowed_top_level"])
    for entry in root.iterdir():
        if entry.name != ".git" and entry.name not in allowed_roots:
            issues.append(f"Unexpected top-level path: {entry.name}")
    pending = [root]
    while pending:
        for path in pending.pop().iterdir():
            relative = path.relative_to(root).as_posix()
            if relative == ".git":
                continue
            parts = path.relative_to(root).parts
            forbidden = (
                linked(path)
                or any(part in CONTRACT["forbidden_parts"] or part.endswith(".egg-info") for part in parts)
                or any(relative == prefix or relative.startswith(prefix + "/") for prefix in FORBIDDEN_PATHS)
                or any(part.endswith((".local.json", ".local.toml", ".draft.json", ".pyc")) for part in parts)
                or ("debug" in parts and path.name != ".gitkeep" and not path.is_dir())
                or path.suffix.lower() in CONTRACT["forbidden_suffixes"]
            )
            allowed_paths = CONTRACT["allowed_files"] + CONTRACT["included_roots"]
            allowed = any(relative == item or relative.startswith(item + "/")
                          or (path.is_dir() and item.startswith(relative + "/")) for item in allowed_paths)
            forbidden = forbidden or not allowed
            if forbidden:
                issues.append(f"Forbidden path exists: {relative}")
            elif path.is_dir():
                pending.append(path)
    return sorted(issues)


def check_forbidden_text(root: Path) -> list[str]:
    issues = check_forbidden_paths(root)
    if issues:
        return issues
    for prefix in CONTRACT["text_scan_roots"]:
        directory = root / prefix
        if not directory.exists():
            continue
        paths = [directory] if directory.is_file() else directory.rglob("*")
        for path in paths:
            if path.is_symlink() or not path.is_file():
                continue
            relative = path.relative_to(root).as_posix()
            if relative in CONTRACT["text_scan_exemptions"]:
                continue
            if path.name != ".gitignore" and path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            for pattern in FORBIDDEN_PATTERNS:
                if pattern.search(text):
                    issues.append(f"{relative}: forbidden text {pattern.pattern!r}")
            if path.suffix == ".py" and re.search(r'Path\([\"\']\$\{', text):
                issues.append(f"{relative}: executable path placeholder")
    return issues


def run_tests(root: Path) -> list[str]:
    issues = []
    for relative in CONTRACT["test_roots"]:
        result = subprocess.run([sys.executable, "-m", "pytest", "tests", "-q", "-p", "no:cacheprovider"],
                                cwd=root / relative, capture_output=True, text=True, timeout=180)
        if result.returncode:
            issues.append(f"Tests failed in {relative}: {(result.stdout + result.stderr)[-1200:]}")
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", default=".")
    parser.add_argument("--skip-tests", action="store_true")
    args = parser.parse_args(argv)
    root = Path(args.dir).absolute()
    if not root.is_dir():
        parser.error("--dir must name an existing directory")
    issues = check_forbidden_paths(root)
    if not issues:
        issues.extend(check_required(root))
    # Do not traverse a tree after a boundary violation.
    if not issues:
        issues.extend(check_forbidden_text(root))
    if not args.skip_tests and not issues:
        issues.extend(run_tests(root))
    for issue in issues:
        print(issue)
    print("FAILED" if issues else "PASSED: unified character-system public boundary and checks")
    return int(bool(issues))


if __name__ == "__main__":
    raise SystemExit(main())
