from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import db_dep, get_current_user
from app.models.user import User
from app.repositories.job_repository import JobRepository
from app.schemas.jobs import JobStatusResponse, JobRead

router = APIRouter(tags=["jobs"])


@router.get("/{job_id}", response_model=JobStatusResponse)
def get_job(job_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(db_dep)) -> JobStatusResponse:
    job = JobRepository(db).get_by_id(job_id)
    if job is None:
        from app.core.errors import NotFoundError

        raise NotFoundError("Job not found")
    return JobStatusResponse(job=JobRead.model_validate(job))
