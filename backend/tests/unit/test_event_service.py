from __future__ import annotations

from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from uuid import uuid4

import pytest
from pytest import raises

from app.models.event import EventParticipantRole, EventStatus
from app.schemas import EventCreate, EventParticipantCreate
from app.services import EventService, ValidationError


class DummyRepo:
    def __init__(self):
        self.create_returns = SimpleNamespace(id=uuid4())
        self.create_called_with = None

    async def create(self, session, *, data):
        self.create_called_with = data
        return self.create_returns

    async def list(self, *args, **kwargs):
        return []

    async def get(self, *args, **kwargs):
        return None


class DummyTeamRepo:
    def __init__(self, teams):
        self.teams = teams

    async def get_by_ids(self, *_, **__):
        return self.teams


@pytest.mark.asyncio
async def test_create_event_rejects_invalid_time():
    service = EventService(event_repository=DummyRepo(), team_repository=DummyTeamRepo([]))
    now = datetime.now(tz=UTC)
    data = EventCreate(
        sport_id=uuid4(),
        title="Bad event",
        starts_at=now,
        ends_at=now,
    )
    with raises(ValidationError):
        await service.create_event(object(), data)


@pytest.mark.asyncio
async def test_create_event_rejects_duplicate_roles():
    sport_id = uuid4()
    service = EventService(event_repository=DummyRepo(), team_repository=DummyTeamRepo([]))
    now = datetime.now(tz=UTC)
    data = EventCreate(
        sport_id=sport_id,
        title="Duplicate roles",
        starts_at=now,
        ends_at=now + timedelta(hours=1),
        participants=[
            EventParticipantCreate(team_id=uuid4(), role=EventParticipantRole.HOME),
            EventParticipantCreate(team_id=uuid4(), role=EventParticipantRole.HOME),
        ],
    )
    with raises(ValidationError):
        await service.create_event(object(), data)


@pytest.mark.asyncio
async def test_create_event_rejects_team_with_wrong_sport():
    good_sport = uuid4()
    other_sport = uuid4()
    repo = DummyRepo()
    teams = [SimpleNamespace(id=uuid4(), sport_id=other_sport, name="Other")]
    service = EventService(event_repository=repo, team_repository=DummyTeamRepo(teams))
    now = datetime.now(tz=UTC)
    data = EventCreate(
        sport_id=good_sport,
        title="Mismatch",
        starts_at=now,
        ends_at=now + timedelta(hours=2),
        participants=[EventParticipantCreate(team_id=teams[0].id, role=EventParticipantRole.HOME)],
    )
    with raises(ValidationError):
        await service.create_event(object(), data)


@pytest.mark.asyncio
async def test_create_event_calls_repository():
    sport_id = uuid4()
    repo = DummyRepo()
    team = SimpleNamespace(id=uuid4(), sport_id=sport_id, name="Home Team")
    service = EventService(event_repository=repo, team_repository=DummyTeamRepo([team]))
    now = datetime.now(tz=UTC)
    data = EventCreate(
        sport_id=sport_id,
        title="Happy path",
        starts_at=now,
        ends_at=now + timedelta(hours=1),
        status=EventStatus.SCHEDULED,
        participants=[
            EventParticipantCreate(team_id=team.id, role=EventParticipantRole.HOME),
        ],
    )
    result = await service.create_event(object(), data)
    assert result is repo.create_returns
    assert repo.create_called_with == data
