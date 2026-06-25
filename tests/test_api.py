from __future__ import annotations

from fastapi.testclient import TestClient

from app.factory import create_app
from app.models.ingestion_job import IngestionJob
from app.repositories.job_repository import JobRepository


def test_auth_and_repository_submission(monkeypatch) -> None:
    app = create_app()

    def fake_run(self, job_id: int) -> None:
        job = JobRepository(self.session).get_by_id(job_id)
        assert job is not None
        JobRepository(self.session).update(job, status="completed", progress_pct=100, stage="finished", error=None)
        repository = job.repository
        repository.status = "completed"
        repository.commit_hash = "deadbeef"
        repository.default_branch = "main"
        self.session.commit()

    monkeypatch.setattr("app.services.ingestion.IngestionCoordinator.run", fake_run)

    client = TestClient(app)
    register_response = client.post("/auth/register", json={"email": "user@example.com", "password": "Passw0rd!"})
    assert register_response.status_code == 200
    token = register_response.json()["access_token"]

    submit_response = client.post(
        "/repositories",
        headers={"Authorization": f"Bearer {token}"},
        json={"url": "https://github.com/acme/demo", "branch": "main", "shallow_clone": True},
    )
    assert submit_response.status_code == 200
    job_id = submit_response.json()["job_id"]

    job_response = client.get(f"/jobs/{job_id}", headers={"Authorization": f"Bearer {token}"})
    assert job_response.status_code == 200
    assert job_response.json()["job"]["status"] == "completed"
    assert job_response.json()["job"]["progress_pct"] == 100