from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import UUID

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db_session
from app.db.seeds import seed_reference_data
from app.main import app
from app.models import Sport, Team
from app.models.event import EventParticipantRole


@pytest.fixture()
async def api_client(async_db_session: AsyncSession):
    async def _override_session():
        yield async_db_session

    app.dependency_overrides[get_db_session] = _override_session
    transport = ASGITransport(app=app)
    try:
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            yield client
    finally:
        app.dependency_overrides.pop(get_db_session, None)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_create_event_invalid_time_window_returns_422(async_db_session: AsyncSession, api_client: AsyncClient):
    await seed_reference_data(async_db_session)
    sport = await _get_first_sport(async_db_session)
    teams = await _get_teams_for_sport(async_db_session, sport.id, limit=2)
    now = datetime.now(tz=UTC)
    payload = {
        "sport_id": str(sport.id),
        "title": "Bad time window",
        "starts_at": (now + timedelta(days=1)).isoformat(),
        "ends_at": (now + timedelta(days=1)).isoformat(),
        "participants": [
            {"team_id": str(teams[0].id), "role": EventParticipantRole.HOME.value},
            {"team_id": str(teams[1].id), "role": EventParticipantRole.AWAY.value},
        ],
    }

    resp = await api_client.post("/api/v1/events", json=payload)
    assert resp.status_code == 422
    assert "end time" in resp.json().get("detail", "").lower()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_create_event_duplicate_team_ids_returns_422(async_db_session: AsyncSession, api_client: AsyncClient):
    await seed_reference_data(async_db_session)
    sport = await _get_first_sport(async_db_session)
    teams = await _get_teams_for_sport(async_db_session, sport.id, limit=1)

    now = datetime.now(tz=UTC)
    same_team_id = str(teams[0].id)
    payload = {
        "sport_id": str(sport.id),
        "title": "Duplicate teams",
        "starts_at": (now + timedelta(days=1)).isoformat(),
        "ends_at": (now + timedelta(days=1, hours=2)).isoformat(),
        "participants": [
            {"team_id": same_team_id, "role": EventParticipantRole.HOME.value},
            {"team_id": same_team_id, "role": EventParticipantRole.AWAY.value},
        ],
    }

    resp = await api_client.post("/api/v1/events", json=payload)
    assert resp.status_code == 422
    assert "duplicate" in resp.json().get("detail", "").lower()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_create_event_team_sport_mismatch_returns_422(async_db_session: AsyncSession, api_client: AsyncClient):
    await seed_reference_data(async_db_session)
    sport_a, sport_b = await _get_two_distinct_sports(async_db_session)
    team_a = (await _get_teams_for_sport(async_db_session, sport_a.id, limit=1))[0]
    team_b = (await _get_teams_for_sport(async_db_session, sport_b.id, limit=1))[0]

    now = datetime.now(tz=UTC)

    payload = {
        "sport_id": str(sport_a.id),
        "title": "Mismatch sport",
        "starts_at": (now + timedelta(days=1)).isoformat(),
        "ends_at": (now + timedelta(days=1, hours=2)).isoformat(),
        "participants": [
            {"team_id": str(team_a.id), "role": EventParticipantRole.HOME.value},
            {"team_id": str(team_b.id), "role": EventParticipantRole.AWAY.value},  # wrong sport
        ],
    }

    resp = await api_client.post("/api/v1/events", json=payload)
    assert resp.status_code == 422
    msg = resp.json().get("detail", "").lower()
    assert "does not belong to the event sport" in msg or "must belong to the event sport" in msg


# ----------------- helpers -----------------


async def _get_first_sport(session: AsyncSession) -> Sport:
    result = await session.scalars(select(Sport).order_by(Sport.name))
    sport = result.first()
    assert sport, "seed should create at least one sport"
    return sport


async def _get_two_distinct_sports(session: AsyncSession) -> tuple[Sport, Sport]:
    result = await session.scalars(select(Sport).order_by(Sport.name))
    sports = list(result.all())
    assert len(sports) >= 2, "seed should create at least two sports"
    return sports[0], sports[1]


async def _get_teams_for_sport(session: AsyncSession, sport_id: UUID, limit: int) -> list[Team]:
    result = await session.scalars(select(Team).where(Team.sport_id == sport_id).order_by(Team.name))
    teams = list(result.all())
    assert len(teams) >= limit, "seed should create enough teams"
    return teams[:limit]
