import os
from collections.abc import AsyncIterator
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy.engine import URL, make_url
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


def _build_alembic_config() -> Config:
    project_root = Path(__file__).resolve().parents[2]
    config = Config(str(project_root / "alembic.ini"))
    config.set_main_option("script_location", str(project_root / "alembic"))
    return config


def _require_test_database_url() -> str:
    test_url = os.getenv("TEST_DATABASE_URL")
    if not test_url:
        pytest.skip("TEST_DATABASE_URL is not set; skipping integration test.")
    return test_url


def _as_async_url(url: str) -> str:
    parsed: URL = make_url(url)
    if parsed.drivername.endswith("+psycopg"):
        parsed = parsed.set(
            drivername=parsed.drivername.replace("+psycopg", "+asyncpg"),
        )
    return parsed.render_as_string(hide_password=False)


@pytest.fixture(scope="session")
def alembic_config() -> Config:
    config = _build_alembic_config()
    config.set_main_option("sqlalchemy.url", _require_test_database_url())
    return config


@pytest.fixture()
def migrated_db(alembic_config: Config):
    """Ensure the database schema is upgraded before a test and reset after."""

    command.downgrade(alembic_config, "base")
    command.upgrade(alembic_config, "head")
    try:
        yield
    finally:
        command.downgrade(alembic_config, "base")


@pytest.fixture()
async def async_db_session(migrated_db) -> AsyncIterator[AsyncSession]:
    test_url = _require_test_database_url()
    async_engine = create_async_engine(_as_async_url(test_url))
    session_factory = async_sessionmaker(bind=async_engine, expire_on_commit=False)
    async with session_factory() as session:
        yield session
    await async_engine.dispose()
