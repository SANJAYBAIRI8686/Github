from __future__ import annotations

from app.core.config import get_settings
from app.db.session import get_session_factory, init_db
from app.models.file_record import FileRecord
from app.repositories.repository_repository import RepositoryRepo


DEMO_CONTENT = {
    "README.md": "# Demo Repo\n\nA small FastAPI example repo used for onboarding and testing.",
    "app/main.py": "from fastapi import FastAPI\n\napp = FastAPI()\n",
    "app/api/routes/auth.py": "from fastapi import APIRouter\nrouter = APIRouter()\n",
    "requirements.txt": "fastapi\nuvicorn\n",
}


def main() -> None:
    settings = get_settings()
    init_db(settings)
    session = get_session_factory(settings)()
    try:
        repo = RepositoryRepo(session).create(
            user_id=None,
            url="https://github.com/fastapi/fastapi",
            owner="fastapi",
            name="fastapi",
            default_branch="master",
            commit_hash="demo",
            status="completed",
            file_count=len(DEMO_CONTENT),
            language_stats={"python": 2, "text": 1},
        )
        for path, content in DEMO_CONTENT.items():
            session.add(
                FileRecord(
                    repository_id=repo.id,
                    path=path,
                    language="python" if path.endswith(".py") else "text",
                    size=len(content),
                    hash=path,
                    summary=content.splitlines()[0],
                )
            )
        session.commit()
        print(f"Seeded demo repository {repo.id}")
    finally:
        session.close()


if __name__ == "__main__":
    main()
