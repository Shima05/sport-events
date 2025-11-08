from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sport import Sport


class SportRepository:
    async def list_all(self, session: AsyncSession) -> list[Sport]:
        result = await session.scalars(select(Sport).order_by(Sport.name))
        return result.all()
