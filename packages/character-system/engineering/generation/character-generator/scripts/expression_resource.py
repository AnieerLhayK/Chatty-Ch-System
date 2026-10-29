"""Bundle the single approved expression reference; no skill invocation or I/O discovery."""
from __future__ import annotations

from pathlib import Path
import re
import stat

WORKSPACE_REFERENCE = "skills/content/speaking-like-a-man/references/shared-expression.md"
LOCAL_REFERENCE = "references/shared-expression.md"
SOURCE_LINK = re.compile(r"(?<=\]\()(?:\.\./)+" + re.escape(WORKSPACE_REFERENCE) + r"(?=\))")


def read_reference(root: Path, relative: str) -> bytes:
    """Read one declared regular UTF-8 file without following linked entries."""
    path = root
    for part in ("", *Path(relative).parts):
        path = path / part
        mode = path.lstat()
        if stat.S_ISLNK(mode.st_mode) or getattr(mode, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT:
            raise ValueError(f"Linked expression resource: {path}")
    if not path.is_file():
        raise ValueError(f"Expression resource must be a regular file: {path}")
    content = path.read_bytes()
    if not content.decode("utf-8").strip():
        raise ValueError("Expression resource is empty")
    return content


def generator_reference(project_root: Path) -> bytes:
    """The Workspace uses its canonical source; exported generators use their bundle."""
    if len(project_root.parents) > 4:
        workspace = project_root.parents[4]
        if (workspace / "workspace_manifest.yaml").is_file():
            return read_reference(workspace, WORKSPACE_REFERENCE)
    return read_reference(project_root, LOCAL_REFERENCE)


def bundle_reference(skill_root: Path, content: bytes) -> None:
    """Localize exactly one approved pointer and copy bytes without prose scrubbing."""
    skill_file = skill_root / "SKILL.md"
    text = skill_file.read_text(encoding="utf-8")
    text, count = SOURCE_LINK.subn(LOCAL_REFERENCE, text)
    template_link = f"](../{LOCAL_REFERENCE})"
    count += text.count(template_link)
    text = text.replace(template_link, f"]({LOCAL_REFERENCE})")
    if count != 1 and not (count == 0 and text.count(f"]({LOCAL_REFERENCE})") == 1):
        raise ValueError(f"Expected one shared expression pointer: {skill_file}")
    skill_file.write_text(text, encoding="utf-8", newline="\n")
    target = skill_root / LOCAL_REFERENCE
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(content)
    template = skill_root / "templates/character_SKILL.template.md"
    if template.is_file():
        text, count = SOURCE_LINK.subn("../" + LOCAL_REFERENCE, template.read_text(encoding="utf-8"))
        if count != 1 and not (count == 0 and text.count(template_link) == 1):
            raise ValueError(f"Expected one shared expression template pointer: {template}")
        template.write_text(text, encoding="utf-8", newline="\n")
