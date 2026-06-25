from __future__ import annotations

from collections.abc import Generator

from fastapi import Depends, Header
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.core.errors import AuthError
from app.core.security import decode_access_token
from app.db.session import get_db_session
from app.models.user import User
from app.repositories.user_repository import UserRepository


def settings_dep() -> Settings:
    return get_settings()


def db_dep(settings: Settings = Depends(settings_dep)) -> Generator[Session, None, None]:
    yield from get_db_session(settings)


def get_current_user(authorization: str | None = Header(default=None), db: Session = Depends(db_dep), settings: Settings = Depends(settings_dep)) -> User:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise AuthError("Missing bearer token")
    token = authorization.split(" ", 1)[1].strip()
    subject = decode_access_token(token, settings)
    user = UserRepository(db).get_by_id(int(subject))
    if user is None:
        raise AuthError("User not found")
    return user
