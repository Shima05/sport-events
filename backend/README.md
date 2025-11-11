# 🏟️ Sports Events Backend

A lightweight **FastAPI backend** for managing sports events — built as a foundation for a larger Sports Events platform.
It provides clean project structure, database migrations, testing setup, and example endpoints for event management.

---

## 🧭 Overview

This backend is designed as a **FastAPI skeleton** that can easily evolve into a full sports management system.
Key features:

- Async FastAPI app following modern Python 3.12+ practices.
- PostgreSQL + SQLAlchemy (async ORM) with Alembic migrations.
- Docker-based local DB setup with pgAdmin UI.
- Integrated testing, linting, and formatting tools for consistent development workflow.
- Includes seed data and documentation for schema understanding.

---

## ⚙️ Requirements

- **Python 3.12+**
- **pip** (latest version)
- _(Recommended)_ Virtual environment tool (`venv`, `uv`, or similar)

---

## 🚀 Setup Instructions

Clone the repository and create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e 'backend/.[dev]'
```

All dependencies (including dev tools) are managed in `backend/pyproject.toml`.

---

## ▶️ Running the API Locally

```bash
uvicorn app.main:app --reload --app-dir backend/src --host 0.0.0.0 --port 8000
```

Before running, make sure to copy `.env.dist` → `.env` inside `backend/` and fill in any missing environment variables.

---

## 🐘 Database Setup (Docker Compose)

Start PostgreSQL and pgAdmin:

```bash
docker compose -f .dev/docker-compose.yml --env-file backend/.env up -d db
```

Access pgAdmin at [http://localhost:5050](http://localhost:5050).
Ensure your `.env` credentials match your Docker DB settings so Alembic and FastAPI can connect.

To stop and remove the database (including volumes):

```bash
docker compose -f .dev/docker-compose.yml down -v
```

**Database stack:** PostgreSQL 16 (`sc_postgres`) + pgAdmin.
Follows official [SQLAlchemy asyncio best practices](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html).

---

## 🔄 Migrations

```bash
cd backend
alembic upgrade head
```

Alembic reads `SYNC_DATABASE_URL` from `.env`.
To roll back and reset the schema:

```bash
alembic downgrade base
```

---

## 🌱 Seeding Reference Data

```bash
cd backend
python -m scripts.seed_reference
```

This inserts base reference data — sports, venues, and sample teams — if they don’t already exist.
You can modify `app/db/seeds.py` to customize demo data.

---

## 🧩 Domain Model & Assumptions

- The domain model and ER diagram are documented in
  [`docs/domain-model.md`](../docs/domain-model.md).
- Each **event** belongs to a **sport** and **venue**, with optional date filters for listing.
- The schema is optimized for extensibility — e.g., future addition of teams, results, and scheduling modules.
- Database design assumes PostgreSQL 16 and async SQLAlchemy 2.x.

---

## 🧪 Tests & Coverage

Run all tests:

```bash
pytest backend/tests
```

Collect coverage:

```bash
coverage run -m pytest backend/tests
coverage report
```

Integration tests that require a live DB expect this variable:

```
TEST_DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5433/sports_events_test
```

All test configuration lives in `backend/pyproject.toml`.

---

## 🧹 Linting & Formatting

All style tools share config in `backend/pyproject.toml`.

Check code style:

```bash
ruff check backend/src backend/tests
black backend/src backend/tests
```

Auto-fix common issues:

```bash
ruff check backend/src backend/tests --fix
```

---

## 🌐 API Endpoints

**Base URL:** `http://localhost:8000/api/v1`

| Method | Endpoint             | Description                                                       |
| ------ | -------------------- | ----------------------------------------------------------------- |
| `GET`  | `/health`            | Health/readiness check                                            |
| `POST` | `/events`            | Create a new event (`EventCreate` payload)                        |
| `GET`  | `/events`            | List events (supports `sport_id`, `date_from`, `date_to` filters) |
| `GET`  | `/events/{event_id}` | Retrieve a single event by ID                                     |

---

## 💡 Development Decisions & Assumptions

- **FastAPI** was chosen for its async support and easy extensibility.
- **PostgreSQL + SQLAlchemy** provide a production-grade relational setup with clear migration handling.
- The backend is designed to be easily containerized and CI-friendly.
- The **domain model** was intentionally kept simple to focus on structure and testability rather than completeness.
