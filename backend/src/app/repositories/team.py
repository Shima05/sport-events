from __future__ import annotations

from collections.abc import Collection
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.team import Team


class TeamRepository:
    async def get_by_ids(
        self,
        session: AsyncSession,
        team_ids: Collection[UUID],
    ) -> list[Team]:
        if not team_ids:
            return []

        result = await session.scalars(select(Team).where(Team.id.in_(team_ids)))
        return result.all()
