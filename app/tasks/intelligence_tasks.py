from __future__ import annotations

from app.core.config import get_settings
from app.db.session import get_session_factory
from app.services.intelligence import RepositoryIntelligenceService
from app.tasks.celery_app import celery_app


@celery_app.task(name="generate_repository_overview")
def generate_repository_overview(repository_id: int) -> dict[str, object]:
    settings = get_settings()
    session = get_session_factory(settings)()
    try:
        service = RepositoryIntelligenceService(session, settings)
        overview = service.build_overview(repository_id)
        return overview.model_dump()
    finally:
        session.close()


@celery_app.task(name="generate_file_summary")
def generate_file_summary(repository_id: int, file_path: str) -> dict[str, object]:
    settings = get_settings()
    session = get_session_factory(settings)()
    try:
        service = RepositoryIntelligenceService(session, settings)
        summary = service.summarize_file(repository_id, file_path)
        return summary.model_dump()
    finally:
        session.close()


@celery_app.task(name="analyze_repository_intelligence")
def analyze_repository_intelligence(repository_id: int) -> dict[str, object]:
    settings = get_settings()
    session = get_session_factory(settings)()
    try:
        service = RepositoryIntelligenceService(session, settings)
        return {
            "overview": service.build_overview(repository_id).model_dump(),
            "dependencies": service.analyze_dependencies(repository_id).model_dump(),
            "bugs": service.detect_bugs(repository_id).model_dump(),
            "security": service.audit_security(repository_id).model_dump(),
        }
    finally:
        session.close()
