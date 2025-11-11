from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db_session
from app.schemas import SportRead
from app.services import SportService

router = APIRouter(prefix="/sports", tags=["Sports"])


def get_sport_service() -> SportService:
    return SportService()


SessionDep = Annotated[AsyncSession, Depends(get_db_session)]
ServiceDep = Annotated[SportService, Depends(get_sport_service)]


@router.get("", response_model=list[SportRead])
async def list_sports(session: SessionDep, service: ServiceDep) -> list[SportRead]:
    sports = await service.list_sports(session)
    return [SportRead.model_validate(s) for s in sports]
