from __future__ import annotations

from fastapi.testclient import TestClient

from app.factory import create_app
from app.models.file_record import FileRecord
from app.repositories.repository_repository import RepositoryRepo
from app.db.session import get_session_factory


def _seed_repository(settings) -> int:
    session = get_session_factory(settings)()
    try:
        repo = RepositoryRepo(session).create(
            user_id=None,
            url="https://github.com/example/demo",
            owner="example",
            name="demo",
            default_branch="main",
            commit_hash="abc123",
            status="completed",
            file_count=3,
            language_stats={"python": 2, "text": 1},
            overview={"project_name": "demo"},
            dependency_analysis={"dependencies": [{"name": "fastapi"}]},
            architecture_summary="Demo architecture",
            complexity="low",
            learning_difficulty="easy",
        )
        session.add_all(
            [
                FileRecord(repository_id=repo.id, path="README.md", language="markdown", size=10, hash="1", summary="README"),
                FileRecord(repository_id=repo.id, path="app/main.py", language="python", size=10, hash="2", summary="main"),
                FileRecord(repository_id=repo.id, path="app/api/routes/auth.py", language="python", size=10, hash="3", summary="auth"),
            ]
        )
        session.commit()
        return repo.id
    finally:
        session.close()


def test_docs_health_and_onboarding_endpoints(monkeypatch) -> None:
    app = create_app()
    settings = app.state.settings
    repo_id = _seed_repository(settings)
    client = TestClient(app)

    auth = client.post("/auth/register", json={"email": "user@example.com", "password": "Passw0rd!"}).json()
    headers = {"Authorization": f"Bearer {auth['access_token']}"}

    docs_response = client.post(f"/repos/{repo_id}/docs/generate", headers=headers)
    assert docs_response.status_code == 200
    assert any(item["filename"] == "README.md" for item in docs_response.json()["files"])

    health_response = client.get(f"/repos/{repo_id}/health", headers=headers)
    assert health_response.status_code == 200
    assert health_response.json()["overall_score"] >= 0

    onboarding_response = client.get(f"/repos/{repo_id}/onboarding", headers=headers)
    assert onboarding_response.status_code == 200
    assert len(onboarding_response.json()["lessons"]) >= 4
