"""create core domain tables

Revision ID: 202511081000
Revises:
Create Date: 2025-11-08 10:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "202511081000"
down_revision: str | None = None
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")

    op.create_table(
        "sports",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_sports"),
        sa.UniqueConstraint("code", name="uq_sports_code"),
    )
    op.create_index("ix_sports_code", "sports", ["code"], unique=True)

    op.create_table(
        "venues",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("city", sa.String(length=128), nullable=True),
        sa.Column("country", sa.String(length=64), nullable=True),
        sa.Column("timezone", sa.String(length=64), nullable=False),
        sa.Column("capacity", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id", name="pk_venues"),
    )

    op.create_table(
        "teams",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("sport_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("abbr", sa.String(length=16), nullable=True),
        sa.Column("founded_year", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["sport_id"],
            ["sports.id"],
            name="fk_teams_sport_id_sports",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_teams"),
        sa.UniqueConstraint(
            "sport_id",
            "name",
            name="uq_teams_sport_id_name",
        ),
    )
    op.create_index("ix_teams_sport_id", "teams", ["sport_id"], unique=False)

    op.create_table(
        "events",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("sport_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("venue_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("starts_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ends_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "scheduled",
                "live",
                "finished",
                "cancelled",
                name="event_status",
                create_type=False,
            ),
            server_default="scheduled",
            nullable=False,
        ),
        sa.Column("ticket_url", sa.String(length=512), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.CheckConstraint("starts_at < ends_at", name="events_starts_before_ends"),
        sa.ForeignKeyConstraint(
            ["sport_id"],
            ["sports.id"],
            name="fk_events_sport_id_sports",
        ),
        sa.ForeignKeyConstraint(
            ["venue_id"],
            ["venues.id"],
            name="fk_events_venue_id_venues",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_events"),
    )
    op.create_index("ix_events_sport_id", "events", ["sport_id"], unique=False)

    op.create_table(
        "event_participants",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("event_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("team_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "role",
            sa.Enum(
                "home",
                "away",
                "participant",
                name="event_participant_role",
                create_type=False,
            ),
            server_default="participant",
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["event_id"],
            ["events.id"],
            name="fk_event_participants_event_id_events",
        ),
        sa.ForeignKeyConstraint(
            ["team_id"],
            ["teams.id"],
            name="fk_event_participants_team_id_teams",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_event_participants"),
        sa.UniqueConstraint(
            "event_id",
            "team_id",
            name="uq_event_participants_event_id_team_id",
        ),
        sa.UniqueConstraint(
            "event_id",
            "role",
            name="uq_event_participants_event_id_role",
        ),
    )


def downgrade() -> None:
    op.drop_table("event_participants")
    op.drop_table("events")
    op.drop_index("ix_teams_sport_id", table_name="teams")
    op.drop_table("teams")
    op.drop_table("venues")
    op.drop_index("ix_sports_code", table_name="sports")
    op.drop_table("sports")

    op.execute("DROP TYPE IF EXISTS event_participant_role CASCADE")
    op.execute("DROP TYPE IF EXISTS event_status CASCADE")
