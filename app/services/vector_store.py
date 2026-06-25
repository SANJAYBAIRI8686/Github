from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class VectorStore(ABC):
    @abstractmethod
    def upsert_chunks(self, repository_id: int, chunks: list[dict[str, Any]], embeddings: list[list[float]]) -> None:
        raise NotImplementedError


class ChromaVectorStore(VectorStore):
    def __init__(self, persist_dir: str) -> None:
        self.persist_dir = persist_dir
        Path(persist_dir).mkdir(parents=True, exist_ok=True)
        import chromadb

        self.client = chromadb.PersistentClient(path=persist_dir)

    def _collection_name(self, repository_id: int) -> str:
        return f"repository_{repository_id}"

    def upsert_chunks(self, repository_id: int, chunks: list[dict[str, Any]], embeddings: list[list[float]]) -> None:
        collection = self.client.get_or_create_collection(name=self._collection_name(repository_id))
        ids = [chunk["id"] for chunk in chunks]
        documents = [chunk["text"] for chunk in chunks]
        metadatas = [chunk["metadata"] for chunk in chunks]
        collection.upsert(ids=ids, documents=documents, metadatas=metadatas, embeddings=embeddings)