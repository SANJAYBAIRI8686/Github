from __future__ import annotations

from sqlalchemy import select

from app.models.repository import Repository
from app.repositories.base import BaseRepository


class RepositoryRepo(BaseRepository[Repository]):
    def get_by_id(self, repository_id: int) -> Repository | None:
        return self.session.get(Repository, repository_id)

    def get_by_url_and_commit(self, url: str, commit_hash: str | None) -> Repository | None:
        if commit_hash is None:
            return None
        return self.session.scalar(
            select(Repository).where(Repository.url == url, Repository.commit_hash == commit_hash)
        )

    def create(self, **kwargs) -> Repository:
        repository = Repository(**kwargs)
        return self.add(repository)
