from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
import app.models  # noqa: F401
from app.repositories.repository_repository import RepositoryRepo


def test_duplicate_detection_by_url_and_commit() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
    session = SessionLocal()
    repo_repo = RepositoryRepo(session)
    repo = repo_repo.create(url="https://github.com/acme/demo", commit_hash="abc123", status="completed", file_count=1, language_stats={})
    session.commit()
    found = repo_repo.get_by_url_and_commit("https://github.com/acme/demo", "abc123")
    assert found is not None
    assert found.id == repo.id