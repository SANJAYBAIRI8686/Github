from __future__ import annotations

from sqlalchemy import select

from app.models.ingestion_job import IngestionJob
from app.repositories.base import BaseRepository


class JobRepository(BaseRepository[IngestionJob]):
    def get_by_id(self, job_id: int) -> IngestionJob | None:
        return self.session.get(IngestionJob, job_id)

    def create(self, *, repository_id: int, status: str = "pending", progress_pct: int = 0, stage: str | None = None) -> IngestionJob:
        job = IngestionJob(repository_id=repository_id, status=status, progress_pct=progress_pct, stage=stage)
        return self.add(job)

    def update(self, job: IngestionJob, **changes) -> IngestionJob:
        for key, value in changes.items():
            setattr(job, key, value)
        self.session.flush()
        return job
