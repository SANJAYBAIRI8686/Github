from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from app.schemas.common import ORMModel


class JobRead(ORMModel):
    id: int
    repository_id: int
    status: str
    progress_pct: int
    stage: str | None
    error: str | None
    task_id: str | None
    created_at: datetime
    updated_at: datetime


class JobStatusResponse(BaseModel):
    job: JobRead
