from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.sport import SportRepository


class SportService:
    def __init__(self, sport_repository: SportRepository | None = None) -> None:
        self._sports = sport_repository or SportRepository()

    async def list_sports(self, session: AsyncSession):
        return await self._sports.list_all(session)
