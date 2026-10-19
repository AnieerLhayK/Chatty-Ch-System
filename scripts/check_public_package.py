"""Validate the unified public system, using its owner-local content contract."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
CONTRACT = json.loads((HERE / "public_contract.json").read_text(encoding="utf-8"))
REQUIRED_PATHS = set(CONTRACT["required_paths"])
FORBIDDEN_PATHS = set(CONTRACT["forbidden_paths"])
FORBIDDEN_PATTERNS = [re.compile(pattern, re.IGNORECASE) for pattern in CONTRACT["forbidden_text"]]
TEXT_SUFFIXES = {".json", ".md", ".py", ".txt", ".yaml", ".yml", ".toml", ".gitignore", ".gitattributes", ".ts", ".tsx", ".js", ".mjs", ".html", ".css"}


def linked(path: Path) -> bool:
    return path.is_symlink() or bool(getattr(path.lstat(), "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT)


def snapshot_files(root: Path, contract: dict) -> list[str]:
    """Validate the pinned inventory before any payload is read or copied."""
    approved = []

    def safe_path(relative: str) -> Path:
        parts = PurePosixPath(relative).parts
        if (not parts or PurePosixPath(relative).is_absolute() or "\\" in relative
                or ":" in relative or any(part in {".", "..", ".git"} for part in parts)
                or PurePosixPath(relative).as_posix() != relative):
            raise ValueError(f"Invalid snapshot path: {relative}")
        path = root / relative
        for entry in (*reversed(path.parents), path):
            if linked(entry):
                raise ValueError(f"Forbidden linked snapshot path: {relative}")
        return path

    for entry in contract.get("immutable_snapshots", []):
        prefix = entry["root"]
        directory = safe_path(prefix)
        manifest_relative = prefix + "/" + entry["manifest"]
        manifest_path = safe_path(manifest_relative)
        if manifest_path.stat().st_size > 2 * 1024 * 1024:
            raise ValueError("Snapshot manifest exceeds limit")
        raw = manifest_path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != entry["manifest_sha256"]:
            raise ValueError("Snapshot manifest hash mismatch")
        manifest = json.loads(raw)
        if manifest["version"] != entry["version"]:
            raise ValueError("Snapshot version mismatch")
        expected = {manifest_relative: entry["manifest_sha256"]}
        for relative, digest in manifest["files"].items():
            full = prefix + "/" + relative
            safe_path(full)
            if not re.fullmatch("[0-9a-f]{64}", digest) or full in expected:
                raise ValueError(f"Invalid snapshot inventory: {relative}")
            expected[full] = digest
        actual = set()
        pending = [directory]
        while pending:
            for path in pending.pop().iterdir():
                relative = path.relative_to(root).as_posix()
                if linked(path):
                    raise ValueError(f"Forbidden linked snapshot path: {relative}")
                if path.is_dir():
                    if not any(item.startswith(relative + "/") for item in expected):
                        raise ValueError(f"Extra snapshot directory: {relative}")
                    pending.append(path)
                elif path.is_file():
                    if relative not in expected:
                        raise ValueError(f"Extra snapshot file: {relative}")
                    actual.add(relative)
                else:
                    raise ValueError(f"Invalid snapshot entry: {relative}")
        if actual != set(expected):
            raise ValueError("Snapshot file inventory mismatch")
        for relative, digest in expected.items():
            with safe_path(relative).open("rb") as stream:
                actual_digest = hashlib.file_digest(stream, "sha256").hexdigest()
            if actual_digest != digest:
                raise ValueError(f"Snapshot file hash mismatch: {relative}")
        candidate = json.loads(safe_path(entry["candidate"]).read_text(encoding="utf-8"))
        if (candidate["version"] != manifest["version"]
                or candidate["source_revision"] != manifest["source_revision"]
                or candidate["artifact"] != manifest["artifact"]
                or candidate["snapshot"] != "versions/" + entry["version"]):
            raise ValueError("Candidate and snapshot identity mismatch")
        approved.extend(expected)
    return approved


def check_required(root: Path) -> list[str]:
    return [f"Missing required path: {relative}" for relative in sorted(REQUIRED_PATHS)
            if not (root / relative).is_file()]


def check_forbidden_paths(root: Path) -> list[str]:
    if any(linked(entry) for entry in (*reversed(root.parents), root)):
        return [f"Forbidden linked root: {root}"]
    try:
        immutable_files = snapshot_files(root, CONTRACT)
    except (ValueError, OSError, KeyError, TypeError) as error:
        return [f"Invalid immutable snapshot: {error}"]
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
            allowed_paths = CONTRACT["allowed_files"] + CONTRACT["included_roots"] + immutable_files
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
            if path.name not in {".gitignore", ".gitattributes"} and path.suffix.lower() not in TEXT_SUFFIXES:
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
        result = subprocess.run([sys.executable, "-B", "-m", "pytest", "tests", "-q", "-p", "no:cacheprovider"],
                                cwd=root / relative, capture_output=True, text=True, timeout=180,
                                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
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
        if not issues:
            issues.extend(check_forbidden_text(root))
    for issue in issues:
        print(issue)
    print("FAILED" if issues else "PASSED: unified character-system public boundary and checks")
    return int(bool(issues))


if __name__ == "__main__":
    raise SystemExit(main())
