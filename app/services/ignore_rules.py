from __future__ import annotations

from pathlib import Path

import pathspec


DEFAULT_IGNORES = [
    ".git/",
    "node_modules/",
    "dist/",
    "build/",
    "__pycache__/",
    ".venv/",
    "venv/",
    "vendor/",
    "*.lock",
]

IGNORED_DIR_NAMES = {".git", "node_modules", "dist", "build", "__pycache__", ".venv", "venv", "vendor"}
IGNORED_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf", ".zip", ".tar", ".gz", ".exe", ".dll", ".so", ".dylib", ".lock"}


def build_spec(extra_patterns: list[str] | None = None) -> pathspec.PathSpec:
    patterns = DEFAULT_IGNORES + (extra_patterns or [])
    return pathspec.PathSpec.from_lines("gitwildmatch", patterns)


def should_skip_path(relative_path: str, spec: pathspec.PathSpec | None = None) -> bool:
    path = Path(relative_path)
    if any(part in IGNORED_DIR_NAMES for part in path.parts):
        return True
    if path.suffix.lower() in IGNORED_SUFFIXES:
        return True
    return spec.match_file(relative_path) if spec else False