from __future__ import annotations

from app.tasks.celery_app import celery_app


@celery_app.task(name="ingest_repository")
def ingest_repository(job_id: int) -> dict[str, int | str]:
    from app.core.config import get_settings
    from app.db.session import get_session_factory
    from app.services.ingestion import IngestionCoordinator

    settings = get_settings()
    session = get_session_factory(settings)()
    try:
        coordinator = IngestionCoordinator.from_settings(settings, session)
        coordinator.run(job_id)
        return {"job_id": job_id, "status": "completed"}
    finally:
        session.close()
