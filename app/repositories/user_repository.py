from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def get_by_email(self, email: str) -> User | None:
        return self.session.scalar(select(User).where(User.email == email))

    def get_by_id(self, user_id: int) -> User | None:
        return self.session.get(User, user_id)

    def create(self, *, email: str, password_hash: str) -> User:
        user = User(email=email, password_hash=password_hash)
        return self.add(user)
