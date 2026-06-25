from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import db_dep, settings_dep
from app.core.config import Settings
from app.core.errors import AuthError, ConflictError
from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.schemas.users import UserRead

router = APIRouter(tags=["auth"])


@router.post("/register", response_model=TokenResponse)
def register(
    payload: RegisterRequest,
    db: Session = Depends(db_dep),
    settings: Settings = Depends(settings_dep),
) -> TokenResponse:
    repo = UserRepository(db)
    existing = repo.get_by_email(payload.email)
    if existing:
        raise ConflictError("Email already registered")
    user = repo.create(email=payload.email, password_hash=hash_password(payload.password))
    db.commit()
    db.refresh(user)
    token = create_access_token(str(user.id), settings)
    return TokenResponse(access_token=token, user=UserRead.model_validate(user))


@router.post("/login", response_model=TokenResponse)
def login(
    payload: LoginRequest,
    db: Session = Depends(db_dep),
    settings: Settings = Depends(settings_dep),
) -> TokenResponse:
    repo = UserRepository(db)
    user = repo.get_by_email(payload.email)
    if user is None or not verify_password(payload.password, user.password_hash):
        raise AuthError("Invalid email or password")
    token = create_access_token(str(user.id), settings)
    return TokenResponse(access_token=token, user=UserRead.model_validate(user))
