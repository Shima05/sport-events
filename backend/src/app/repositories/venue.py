"""Venue repository helpers."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.venue import Venue


class VenueRepository:
    async def list_all(self, session: AsyncSession) -> list[Venue]:
        result = await session.scalars(select(Venue).order_by(Venue.name))
        return result.all()
