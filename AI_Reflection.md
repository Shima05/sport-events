## AI Collaboration Notes

- AI assistant reviewed `backend/pyproject.toml`, configured linting/formatting/testing tools (pytest, coverage, black, ruff), and reviewed the structure to stay aligned with FastAPI best practices.
- AI assistant drafted the project README (root pointer + `backend/README.md`) explaining setup, tooling, and usage.
- AI assistant created backend-specific `.gitignore` entries to avoid committing virtualenvs, caches, coverage outputs, etc.
- AI assistant built the Mermaid ER diagram + supporting notes in `docs/domain-model.md` so the schema stays understandable.
- AI assistant configured Alembic (`alembic.ini`, env setup, initial migration) and helped me scaffold the Postgres schema/migrations.
- AI assistant reviewed the SQLAlchemy async session + data model code against the official docs (https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html) to ensure best practices.
- AI assistant helped me both unit tests (metadata checks) and integration tests (migration upgrade/downgrade) for coverage of the new DB layer.
