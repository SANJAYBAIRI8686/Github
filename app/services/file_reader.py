from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

from app.services.ignore_rules import build_spec, should_skip_path


LANGUAGE_BY_SUFFIX = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".go": "go",
    ".java": "java",
    ".rb": "ruby",
    ".rs": "rust",
    ".php": "php",
    ".cs": "csharp",
    ".c": "c",
    ".cc": "cpp",
    ".cpp": "cpp",
    ".h": "c",
    ".hpp": "cpp",
    ".md": "markdown",
    ".rst": "markdown",
    ".txt": "text",
    ".yml": "yaml",
    ".yaml": "yaml",
    ".json": "json",
}


@dataclass(slots=True)
class ReadFileResult:
    path: str
    language: str | None
    size: int
    content: str
    hash: str


def detect_language(path: str) -> str | None:
    return LANGUAGE_BY_SUFFIX.get(Path(path).suffix.lower())


def is_binary(content: bytes) -> bool:
    return b"\0" in content[:4096]


def read_repo_files(root: Path, max_file_size_bytes: int, extra_ignore_patterns: list[str] | None = None) -> list[ReadFileResult]:
    spec = build_spec(extra_ignore_patterns)
    results: list[ReadFileResult] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        if should_skip_path(relative, spec):
            continue
        size = path.stat().st_size
        if size > max_file_size_bytes:
            continue
        content_bytes = path.read_bytes()
        if is_binary(content_bytes):
            continue
        content = content_bytes.decode("utf-8", errors="ignore")
        results.append(
            ReadFileResult(
                path=relative,
                language=detect_language(relative),
                size=size,
                content=content,
                hash=sha256(content_bytes).hexdigest(),
            )
        )
    return results