# GitHub Repo Analyzer

Milestone 1 delivered authenticated repository ingestion. Milestone 2 added cited chat, semantic search, overview generation, dependency analysis, and static bug/security inspection. Milestone 3 adds the consumer UI, generated documentation, repository health scoring, onboarding lessons, and full-stack packaging.

## Folder Tree

```text
app/
  api/
    deps.py
    routes/
      auth.py
      health.py
      jobs.py
      repositories.py
  core/
    config.py
    errors.py
    logging.py
    security.py
  db/
    base.py
    session.py
  models/
    __init__.py
    file_record.py
    ingestion_job.py
    repository.py
    user.py
  repositories/
    base.py
    file_repository.py
    job_repository.py
    repository_repository.py
    user_repository.py
  schemas/
    auth.py
    common.py
    jobs.py
    repositories.py
    users.py
  services/
    chunking.py
    embedding_provider.py
    file_reader.py
    git_service.py
    ignore_rules.py
    ingestion.py
    vector_store.py
  tasks/
    celery_app.py
    ingestion_tasks.py
alembic/
  env.py
  script.py.mako
  versions/
    0001_initial.py
```

## Quick Start

1. Copy `.env.example` to `.env` and set `SECRET_KEY`.
2. Install dependencies: `pip install -e .[test]`.
3. Create the schema with Alembic: `alembic upgrade head`.
4. Run the API: `uvicorn app.main:app --reload`.
5. Start Celery with Redis: `celery -A app.tasks.celery_app.celery_app worker --loglevel=info`.

## Example Curl

```bash
curl -s http://localhost:8000/health
```

```bash
curl -s -X POST http://localhost:8000/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"email":"user@example.com","password":"Passw0rd!"}'
```

```bash
curl -s -X POST http://localhost:8000/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"user@example.com","password":"Passw0rd!"}'
```

```bash
curl -s -X POST http://localhost:8000/repositories \
  -H "Authorization: Bearer <token>" \
  -H 'Content-Type: application/json' \
  -d '{"url":"https://github.com/owner/repo","branch":"main","shallow_clone":true}'
```

```bash
curl -s http://localhost:8000/jobs/<job-id> \
  -H "Authorization: Bearer <token>"
```

## Milestone 2 API Examples

```bash
curl -s http://localhost:8000/repos/<repo-id>/overview \
  -H "Authorization: Bearer <token>"
```

```bash
curl -s http://localhost:8000/repos/<repo-id>/deps \
  -H "Authorization: Bearer <token>"
```

```bash
curl -s -X POST http://localhost:8000/repos/<repo-id>/search \
  -H "Authorization: Bearer <token>" \
  -H 'Content-Type: application/json' \
  -d '{"query":"How does login work?","file_path":"app/api/routes/auth.py"}'
```

```bash
curl -N -X POST http://localhost:8000/repos/<repo-id>/chat \
  -H "Authorization: Bearer <token>" \
  -H 'Content-Type: application/json' \
  -d '{"message":"How does login work?","file_path":"app/api/routes/auth.py"}'
```

```bash
curl -s http://localhost:8000/repos/<repo-id>/files/app%2Fapi%2Froutes%2Fauth.py/summary \
  -H "Authorization: Bearer <token>"
```

```bash
curl -s -X POST http://localhost:8000/explain \
  -H "Authorization: Bearer <token>" \
  -H 'Content-Type: application/json' \
  -d '{"repo_id":1,"symbol_name":"login","file_path":"app/api/routes/auth.py"}'
```

```bash
curl -s -X POST http://localhost:8000/repos/<repo-id>/bugs \
  -H "Authorization: Bearer <token>"
```

```bash
curl -s -X POST http://localhost:8000/repos/<repo-id>/security \
  -H "Authorization: Bearer <token>"
```

## Milestone 3 API Examples

```bash
curl -s -X POST http://localhost:8000/repos/<repo-id>/docs/generate \
  -H "Authorization: Bearer <token>"
```

```bash
curl -s http://localhost:8000/repos/<repo-id>/docs/download \
  -H "Authorization: Bearer <token>" -o repo-docs.zip
```

```bash
curl -s http://localhost:8000/repos/<repo-id>/health \
  -H "Authorization: Bearer <token>"
```

```bash
curl -s http://localhost:8000/repos/<repo-id>/architecture \
  -H "Authorization: Bearer <token>"
```

```bash
curl -s http://localhost:8000/repos/<repo-id>/onboarding \
  -H "Authorization: Bearer <token>"
```

## Deployment

Use `docker compose up --build` to launch the full stack: API, worker, Redis, PostgreSQL, Chroma, and the Next.js frontend.

The frontend lives in [frontend/](frontend) and uses typed API calls against the backend REST endpoints.
