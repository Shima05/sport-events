from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db_session
from app.schemas import TeamRead
from app.services import TeamService

router = APIRouter(prefix="/teams", tags=["Teams"])


def get_team_service() -> TeamService:
    return TeamService()


SessionDep = Annotated[AsyncSession, Depends(get_db_session)]
ServiceDep = Annotated[TeamService, Depends(get_team_service)]


@router.get("", response_model=list[TeamRead])
async def list_teams(
    session: SessionDep,
    service: ServiceDep,
    sport_id: Annotated[UUID | None, Query(description="Filter by sport UUID")] = None,
) -> list[TeamRead]:
    teams = await service.list_teams(session, sport_id=sport_id)
    return [TeamRead.model_validate(team) for team in teams]
