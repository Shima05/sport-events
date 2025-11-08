import pytest
from alembic import command


@pytest.mark.integration
def test_alembic_migrations_upgrade_and_downgrade(alembic_config) -> None:
    command.upgrade(alembic_config, "head")
    command.downgrade(alembic_config, "base")
