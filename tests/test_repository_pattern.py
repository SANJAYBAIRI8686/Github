from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
import app.models  # noqa: F401
from app.repositories.repository_repository import RepositoryRepo


def test_repository_repo_create_and_lookup() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
    session = SessionLocal()
    repo = RepositoryRepo(session).create(url="https://github.com/acme/demo", status="queued", file_count=0, language_stats={})
    session.commit()
    found = RepositoryRepo(session).get_by_id(repo.id)
    assert found is not None
    assert found.url == "https://github.com/acme/demo"