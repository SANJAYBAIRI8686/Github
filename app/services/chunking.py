from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class Chunk:
    text: str
    metadata: dict[str, Any]


def _semantic_chunks_from_python(content: str, file_path: str, language: str) -> list[Chunk]:
    import ast

    chunks: list[Chunk] = []
    try:
        tree = ast.parse(content)
    except SyntaxError:
        return []

    lines = content.splitlines()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            start_line = getattr(node, "lineno", None)
            end_line = getattr(node, "end_lineno", start_line)
            if not start_line or not end_line:
                continue
            snippet = "\n".join(lines[start_line - 1 : end_line])
            chunks.append(
                Chunk(
                    text=snippet,
                    metadata={
                        "file_path": file_path,
                        "language": language,
                        "symbol_name": node.name,
                        "start_line": start_line,
                        "end_line": end_line,
                        "chunk_type": "semantic",
                    },
                )
            )
    return chunks


def _fallback_text_chunks(content: str, file_path: str, language: str) -> list[Chunk]:
    lines = content.splitlines()
    chunk_size = 80
    overlap = 10
    chunks: list[Chunk] = []
    index = 0
    chunk_number = 0
    while index < len(lines):
        end = min(index + chunk_size, len(lines))
        snippet = "\n".join(lines[index:end])
        if snippet.strip():
            chunks.append(
                Chunk(
                    text=snippet,
                    metadata={
                        "file_path": file_path,
                        "language": language,
                        "symbol_name": None,
                        "start_line": index + 1,
                        "end_line": end,
                        "chunk_type": "text",
                        "chunk_index": chunk_number,
                    },
                )
            )
            chunk_number += 1
        index = max(end - overlap, index + 1)
    return chunks


def chunk_file(content: str, file_path: str, language: str | None) -> list[Chunk]:
    if language == "python":
        semantic = _semantic_chunks_from_python(content, file_path, language)
        if semantic:
            return semantic
    if language in {"markdown", "text", None}:
        return _fallback_text_chunks(content, file_path, language or "text")
    return _fallback_text_chunks(content, file_path, language)