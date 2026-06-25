from __future__ import annotations

from sqlalchemy import select

from app.models.file_record import FileRecord
from app.repositories.base import BaseRepository


class FileRepository(BaseRepository[FileRecord]):
    def get_by_repo_and_path(self, repository_id: int, path: str) -> FileRecord | None:
        return self.session.scalar(
            select(FileRecord).where(FileRecord.repository_id == repository_id, FileRecord.path == path)
        )

    def create(self, **kwargs) -> FileRecord:
        file_record = FileRecord(**kwargs)
        return self.add(file_record)
