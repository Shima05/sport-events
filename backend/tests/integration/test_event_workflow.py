from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import select

from app.db.seeds import seed_reference_data
from app.models import Sport, Team
from app.models.event import EventParticipantRole
from app.schemas import EventCreate, EventParticipantCreate
from app.services import EventService


@pytest.mark.integration
@pytest.mark.asyncio
async def test_create_and_list_events(async_db_session):
    await seed_reference_data(async_db_session)
    sport = await _get_first_sport(async_db_session)
    teams = await _get_teams_for_sport(async_db_session, sport.id, limit=2)

    service = EventService()
    now = datetime.now(tz=UTC)
    data = EventCreate(
        sport_id=sport.id,
        title="Season Opener",
        starts_at=now + timedelta(days=1),
        ends_at=now + timedelta(days=1, hours=2),
        participants=[
            EventParticipantCreate(team_id=teams[0].id, role=EventParticipantRole.HOME),
            EventParticipantCreate(team_id=teams[1].id, role=EventParticipantRole.AWAY),
        ],
    )
    created = await service.create_event(async_db_session, data)
    assert created.id is not None

    events = await service.list_events(async_db_session, sport_id=sport.id)
    assert any(event.id == created.id for event in events)


async def _get_first_sport(session):
    result = await session.execute(select(Sport).order_by(Sport.name))
    sport = result.scalars().first()
    if sport is None:
        raise AssertionError("Seed script should create at least one sport.")
    return sport


async def _get_teams_for_sport(session, sport_id, limit: int):
    result = await session.execute(select(Team).where(Team.sport_id == sport_id).order_by(Team.name))
    teams = result.scalars().all()
    if len(teams) < limit:
        raise AssertionError("Seed script should create multiple teams per sport.")
    return teams[:limit]
