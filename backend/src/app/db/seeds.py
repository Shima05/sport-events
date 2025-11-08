from __future__ import annotations

from collections.abc import Mapping

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Sport, Team, Venue

DEFAULT_SPORTS = (
    ("soccer", "Soccer"),
    ("basketball", "Basketball"),
    ("tennis", "Tennis"),
)

DEFAULT_VENUES = (
    {
        "name": "National Arena",
        "city": "London",
        "country": "UK",
        "timezone": "Europe/London",
        "capacity": 60000,
    },
    {
        "name": "Downtown Stadium",
        "city": "New York",
        "country": "USA",
        "timezone": "America/New_York",
        "capacity": 45000,
    },
)

DEFAULT_TEAMS = (
    {
        "sport_code": "soccer",
        "name": "London City FC",
        "abbr": "LCF",
    },
    {
        "sport_code": "soccer",
        "name": "New York United",
        "abbr": "NYU",
    },
    {
        "sport_code": "basketball",
        "name": "Metro Ballers",
        "abbr": "MBL",
    },
    {
        "sport_code": "basketball",
        "name": "Downtown Shooters",
        "abbr": "DTS",
    },
    {
        "sport_code": "tennis",
        "name": "Baseline Smashers",
        "abbr": "BSM",
    },
    {
        "sport_code": "tennis",
        "name": "Court Masters",
        "abbr": "CM",
    },
)


async def seed_reference_data(session: AsyncSession) -> None:
    """Insert baseline reference rows if they don't exist."""

    sport_map = await _seed_sports(session)
    await session.commit()

    await _seed_venues(session)
    await session.commit()

    await _seed_teams(session, sport_map)
    await session.commit()


async def _seed_sports(session: AsyncSession) -> dict[str, Sport]:
    result = await session.execute(select(Sport))
    existing = {sport.code: sport for sport in result.scalars()}

    for code, name in DEFAULT_SPORTS:
        if code not in existing:
            sport = Sport(code=code, name=name)
            session.add(sport)
            existing[code] = sport

    await session.flush()
    return existing


async def _seed_venues(session: AsyncSession) -> None:
    result = await session.execute(select(Venue.name, Venue.city))
    existing = set(result.all())
    for payload in DEFAULT_VENUES:
        key = (payload["name"], payload.get("city"))
        if key in existing:
            continue
        session.add(Venue(**payload))


async def _seed_teams(session: AsyncSession, sports: Mapping[str, Sport]) -> None:
    result = await session.execute(select(Team.sport_id, Team.name))
    existing = set(result.all())
    for payload in DEFAULT_TEAMS:
        sport = sports.get(payload["sport_code"])
        if not sport:
            continue

        key = (sport.id, payload["name"])
        if key in existing:
            continue

        session.add(
            Team(
                sport_id=sport.id,
                name=payload["name"],
                abbr=payload.get("abbr"),
            )
        )
