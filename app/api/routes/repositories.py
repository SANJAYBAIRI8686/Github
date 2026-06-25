from __future__ import annotations

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from app.api.deps import db_dep, get_current_user, settings_dep
from app.core.config import Settings
from app.models.user import User
from app.schemas.repositories import RepositoryIngestRequest, RepositoryRead, RepositorySubmissionResponse
from app.services.ingestion import IngestionCoordinator

router = APIRouter(tags=["repositories"])


@router.post("", response_model=RepositorySubmissionResponse)
def submit_repository(
    payload: RepositoryIngestRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(db_dep),
    settings: Settings = Depends(settings_dep),
) -> RepositorySubmissionResponse:
    coordinator = IngestionCoordinator.from_settings(settings, db)
    repository, job = coordinator.create_job(current_user.id, payload)
    db.commit()
    background_tasks.add_task(coordinator.enqueue_or_run, job.id)
    return RepositorySubmissionResponse(repository=RepositoryRead.model_validate(repository), job_id=job.id)
