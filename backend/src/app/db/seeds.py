from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Sport

DEFAULT_SPORTS = (
    ("soccer", "Soccer"),
    ("basketball", "Basketball"),
    ("tennis", "Tennis"),
)


async def seed_reference_data(session: AsyncSession) -> None:
    """Insert baseline sport rows if they don't exist."""

    result = await session.execute(select(Sport.code))
    existing_codes = set(result.scalars().all())
    for code, name in DEFAULT_SPORTS:
        if code in existing_codes:
            continue
        session.add(Sport(code=code, name=name))
    await session.commit()
