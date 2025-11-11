from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.team import TeamRepository


class TeamService:
    def __init__(self, team_repository: TeamRepository | None = None) -> None:
        self._teams = team_repository or TeamRepository()

    async def list_teams(
        self,
        session: AsyncSession,
        *,
        sport_id: UUID | None = None,
    ):
        return await self._teams.list(session, sport_id=sport_id)
