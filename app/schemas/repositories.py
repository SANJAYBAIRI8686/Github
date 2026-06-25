from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, HttpUrl

from app.schemas.common import ORMModel


class RepositoryIngestRequest(BaseModel):
    url: str
    branch: str | None = None
    shallow_clone: bool = True


class RepositoryRead(ORMModel):
    id: int
    url: str
    owner: str | None
    name: str | None
    default_branch: str | None
    commit_hash: str | None
    status: str
    file_count: int
    language_stats: dict[str, Any]
    created_at: datetime


class RepositorySubmissionResponse(BaseModel):
    repository: RepositoryRead
    job_id: int


class RepositoryIngestResponse(BaseModel):
    repository: RepositoryRead
    job_id: int
