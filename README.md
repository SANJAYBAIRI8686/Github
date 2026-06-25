# GitHub Repo Analyzer

Milestone 1 delivers the foundation for authenticated repository ingestion. The service clones a GitHub URL, filters noise, parses code into semantic chunks, embeds those chunks, and stores vector + relational metadata so later query phases can build on a stable backbone.

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
