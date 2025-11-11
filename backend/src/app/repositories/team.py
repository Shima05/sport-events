from __future__ import annotations

from uuid import UUID

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.team import Team


class TeamRepository:
    async def list(
        self,
        session: AsyncSession,
        *,
        sport_id: UUID | None = None,
    ) -> list[Team]:
        stmt: Select[Team] = select(Team).order_by(Team.name)
        if sport_id:
            stmt = stmt.where(Team.sport_id == sport_id)
        result = await session.scalars(stmt)
        return list(result.all())

    async def get_by_ids(self, session: AsyncSession, ids: set[UUID]) -> list[Team]:
        if not ids:
            return []
        stmt: Select[Team] = select(Team).where(Team.id.in_(ids))
        result = await session.scalars(stmt)
        return list(result.all())
