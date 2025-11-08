from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import UUID

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.seeds import seed_reference_data
from app.models import Sport, Team
from app.models.event import EventParticipantRole, EventStatus
from app.schemas import EventCreate, EventParticipantCreate
from app.services import EventService
from app.services.event_filters import EventListParams


@pytest.mark.integration
@pytest.mark.asyncio
async def test_create_and_list_events(async_db_session: AsyncSession) -> None:
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
    assert created.status == EventStatus.SCHEDULED
    assert created.starts_at.tzinfo is not None and created.ends_at.tzinfo is not None
    roles = sorted(p.role for p in created.participants)
    assert roles == [EventParticipantRole.AWAY, EventParticipantRole.HOME]

    params = EventListParams(sport_id=sport.id)
    events = await service.list_events(async_db_session, params=params)
    assert any(event.id == created.id for event in events)


async def _get_first_sport(session: AsyncSession) -> Sport:
    result = await session.scalars(select(Sport).order_by(Sport.name))
    sport = result.first()
    assert sport, "Seed script should create at least one sport."
    return sport


async def _get_teams_for_sport(session: AsyncSession, sport_id: UUID, limit: int) -> list[Team]:
    result = await session.scalars(select(Team).where(Team.sport_id == sport_id).order_by(Team.name))
    teams = list(result.all())
    assert len(teams) >= limit, "Seed script should create multiple teams per sport."
    return teams[:limit]
