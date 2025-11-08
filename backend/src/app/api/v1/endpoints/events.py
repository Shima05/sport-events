from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from pydantic import AwareDatetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db_session
from app.schemas import EventCreate, EventRead
from app.services import EventService, ValidationError

router = APIRouter(prefix="/events", tags=["Events"])


def get_event_service() -> EventService:
    return EventService()


SessionDep = Annotated[AsyncSession, Depends(get_db_session)]
ServiceDep = Annotated[EventService, Depends(get_event_service)]

SportIdQuery = Annotated[UUID | None, Query()]
DateFromQuery = Annotated[AwareDatetime | None, Query(description="ISO 8601 with timezone")]
DateToQuery = Annotated[AwareDatetime | None, Query(description="ISO 8601 with timezone")]


@router.post("", response_model=EventRead, status_code=status.HTTP_201_CREATED)
async def create_event(
    payload: EventCreate,
    session: SessionDep,
    service: ServiceDep,
    response: Response,
) -> EventRead:
    try:
        event = await service.create_event(session, payload)
    except ValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(exc),
        ) from exc
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Constraint violation while creating event.",
        ) from exc

    response.headers["Location"] = f"/events/{event.id}"
    return EventRead.model_validate(event)


@router.get("", response_model=list[EventRead])
async def list_events(
    session: SessionDep,
    service: ServiceDep,
    sport_id: SportIdQuery = None,
    date_from: DateFromQuery = None,
    date_to: DateToQuery = None,
) -> list[EventRead]:
    events = await service.list_events(
        session,
        sport_id=sport_id,
        date_from=date_from,
        date_to=date_to,
    )
    return [EventRead.model_validate(e) for e in events]


@router.get("/{event_id}", response_model=EventRead)
async def get_event(
    event_id: UUID,
    session: SessionDep,
    service: ServiceDep,
) -> EventRead:
    event = await service.get_event(session, event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found.",
        )
    return EventRead.model_validate(event)
