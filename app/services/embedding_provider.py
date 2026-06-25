from __future__ import annotations

from abc import ABC, abstractmethod
from hashlib import sha256


class EmbeddingProvider(ABC):
    @abstractmethod
    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError


class OpenAIEmbeddingProvider(EmbeddingProvider):
    def __init__(self, api_key: str | None, model: str) -> None:
        self.api_key = api_key
        self.model = model

    def _local_embedding(self, text: str, dimensions: int = 8) -> list[float]:
        digest = sha256(text.encode("utf-8")).digest()
        return [round(b / 255.0, 6) for b in digest[:dimensions]]

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if not self.api_key:
            return [self._local_embedding(text) for text in texts]
        try:
            from openai import OpenAI

            client = OpenAI(api_key=self.api_key)
            response = client.embeddings.create(model=self.model, input=texts)
            return [item.embedding for item in response.data]
        except Exception:
            return [self._local_embedding(text) for text in texts]