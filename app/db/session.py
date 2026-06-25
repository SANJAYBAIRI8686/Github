from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import Settings, get_settings
from app.db.base import Base
import app.models  # noqa: F401

_engine = None
_SessionLocal = None


def _build_engine(settings: Settings):
    connect_args = {}
    poolclass = None
    if settings.database_url.startswith("sqlite"):
        connect_args = {"check_same_thread": False}
        if ":memory:" in settings.database_url:
            poolclass = StaticPool
    return create_engine(settings.database_url, connect_args=connect_args, poolclass=poolclass, future=True)


def get_engine(settings: Settings | None = None):
    global _engine
    settings = settings or get_settings()
    if _engine is None:
        _engine = _build_engine(settings)
    return _engine


def get_session_factory(settings: Settings | None = None):
    global _SessionLocal
    if _SessionLocal is None:
        engine = get_engine(settings)
        _SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
    return _SessionLocal


def get_db_session(settings: Settings | None = None) -> Generator[Session, None, None]:
    session_factory = get_session_factory(settings)
    session = session_factory()
    try:
        yield session
    finally:
        session.close()


def init_db(settings: Settings | None = None) -> None:
    engine = get_engine(settings)
    Base.metadata.create_all(bind=engine)
