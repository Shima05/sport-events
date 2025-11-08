## Sports Events Backend

FastAPI skeleton for the Sports Events platform.

---

## Requirements

- Python 3.12+
- `pip`
- (Recommended) a virtual environment tool such as `venv` or `uv`

---

## Installation

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e 'backend/.[dev]'
```

Dependencies are defined in `backend/pyproject.toml`.

---

## Running the API locally

```bash
uvicorn app.main:app --reload --app-dir backend/src --host 0.0.0.0 --port 8000
```

## Add configuration values to `backend/.env` (see `.env.dist` for inspiration)

---

## Database via Docker Compose

```bash
docker compose -f .dev/docker-compose.yml --env-file backend/.env up -d db
```

**Remove Database**

```bash
docker compose -f .dev/docker-compose.yml down -v   # removes db_data
```

This boots PostgreSQL 16 (`sc_postgres`) plus pgAdmin (http://localhost:5050). Use
the same credentials in `backend/.env` so FastAPI + Alembic can connect.
Async SQLAlchemy sessions follow the official guidance:
[SQLAlchemy asyncio docs](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html).

### Migrations

```bash
cd backend
alembic upgrade head
```

Alembic reads `SYNC_DATABASE_URL` from `.env`. Run `alembic downgrade base` if you
need to reset the schema locally.

### Seed reference data

```bash
cd backend
python -m scripts.seed_reference
```

Seeds insert baseline sports, venues, and a few teams only if they do not already exist. Feel free to edit `app/db/seeds.py`
to add more demo data.

## Domain Model & Data Assumptions

- ERD and PostgreSQL-specific constraints live in
  [docs/domain-model.md](../docs/domain-model.md).

## Tests & Coverage

Run the test suite:

```bash
pytest backend/tests
```

Collect coverage (configuration lives in `backend/pyproject.toml`):

```bash
coverage run -m pytest backend/tests
coverage report
```

Integration tests that rely on a real PostgreSQL instance expect
`TEST_DATABASE_URL` to be defined (e.g.,
`postgresql+psycopg://postgres:postgres@localhost:5433/sports_events_test`).

---

## Linting & Formatting

All style tools share their configuration via `backend/pyproject.toml`.

```bash
ruff check backend/src backend/tests         # static analysis
black backend/src backend/tests              # code formatter
```

Apply Ruff’s auto-fixes if desired:

```bash
ruff check backend/src backend/tests --fix
```

---

## API Endpoints

Base URL: `http://localhost:8000/api/v1`

- `GET /health` – readiness probe.
- `POST /events` – create a new event (`EventCreate` payload).
- `GET /events` – list events (optional `sport_id`, `date_from`, `date_to` filters).
- `GET /events/{event_id}` – retrieve one event.

Example:

```bash
curl -X POST http://localhost:8000/api/v1/events \
  -H "Content-Type: application/json" \
  -d '{
        "sport_id": "REPLACE_WITH_REAL_SPORT_UUID",
        "title": "Friendly Match",
        "starts_at": "2025-01-01T12:00:00Z",
        "ends_at": "2025-01-01T14:00:00Z",
        "participants": []
      }'
```
