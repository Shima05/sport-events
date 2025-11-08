from __future__ import annotations

import os
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config


def _get_test_config() -> Config:
    project_root = Path(__file__).resolve().parents[2]
    config_path = project_root / "alembic.ini"
    config = Config(str(config_path))
    config.set_main_option("script_location", str(project_root / "alembic"))
    test_url = os.getenv("TEST_DATABASE_URL")
    if not test_url:
        pytest.skip("TEST_DATABASE_URL is not set; skipping migration test.")
    config.set_main_option("sqlalchemy.url", test_url)
    return config


@pytest.mark.integration
def test_alembic_migrations_upgrade_and_downgrade() -> None:
    config = _get_test_config()
    command.upgrade(config, "head")
    command.downgrade(config, "base")
