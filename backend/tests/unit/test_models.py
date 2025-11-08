from sqlalchemy import UniqueConstraint

from app.models.base import Base


def test_tables_registered() -> None:
    tables = Base.metadata.tables
    for table in ("sports", "venues", "teams", "events", "event_participants"):
        assert table in tables, f"{table} not in metadata"


def test_events_constraints() -> None:
    event_table = Base.metadata.tables["events"]
    assert "starts_at" in event_table.c
    constraint_names = {constraint.name for constraint in event_table.constraints if constraint.name}
    assert "ck_events_events_starts_before_ends" in constraint_names


def test_participant_unique_constraints() -> None:
    participant_table = Base.metadata.tables["event_participants"]
    unique_names = {
        constraint.name
        for constraint in participant_table.constraints
        if isinstance(constraint, UniqueConstraint) and constraint.name
    }
    assert "uq_event_participants_event_id_role" in unique_names
    assert "uq_event_participants_event_id_team_id" in unique_names
