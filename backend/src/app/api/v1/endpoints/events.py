from __future__ import annotations

from enum import Enum
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from pydantic import AwareDatetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db_session
from app.models.event import EventStatus
from app.schemas import EventCreate, EventRead
from app.services import EventService, ValidationError
from app.services.event_filters import EventListParams, Pagination

router = APIRouter(prefix="/events", tags=["Events"])


def get_event_service() -> EventService:
    return EventService()


def _describe_integrity_error(exc: IntegrityError) -> str:
    orig = getattr(exc, "orig", None)
    diag = getattr(orig, "diag", None)
    constraint = (
        getattr(diag, "constraint_name", None)
        or getattr(orig, "constraint_name", None)
        or getattr(orig, "constraint", None)
    )
    raw_message = str(orig) if orig else None

    constraint_messages = {
        "events_starts_before_ends": "Event end time must be after the start time.",
        "_fk_events_sport_id_sports": "Sport referenced by sport_id does not exist.",
        "fk_events_sport_id_sports": "Sport referenced by sport_id does not exist.",
        "_fk_events_venue_id_venues": "Venue referenced by venue_id does not exist.",
        "fk_events_venue_id_venues": "Venue referenced by venue_id does not exist.",
        "_fk_event_participants_team_id_teams": "One or more participant teams do not exist.",
        "fk_event_participants_team_id_teams": "One or more participant teams do not exist.",
        "uq_event_participants_event_id_team_id": "Each team can only be added once to an event.",
        "uq_event_participants_event_id_role_home_away": "Only one HOME and one AWAY participant is allowed per event.",
    }

    if constraint and constraint in constraint_messages:
        return constraint_messages[constraint]
    if raw_message:
        lowered = raw_message.lower()
        for key, message_text in constraint_messages.items():
            if key.lower() in lowered:
                return message_text

    message = getattr(diag, "message_primary", None)
    if message:
        return message

    if constraint:
        return f"Constraint violation ({constraint}) while creating event."

    if raw_message:
        return raw_message

    return "Constraint violation while creating event."


SessionDep = Annotated[AsyncSession, Depends(get_db_session)]
ServiceDep = Annotated[EventService, Depends(get_event_service)]

SportIdQuery = Annotated[UUID | None, Query(alias="sport_id", description="Filter by sport UUID")]
VenueIdQuery = Annotated[UUID | None, Query(alias="venue_id", description="Filter by venue UUID")]
StatusQuery = Annotated[EventStatus | None, Query(alias="status", description="Filter by event status")]
DateFromQuery = Annotated[AwareDatetime | None, Query(description="Filter: start >= date_from (ISO 8601 with tz)")]
DateToQuery = Annotated[AwareDatetime | None, Query(description="Filter: start <= date_to (ISO 8601 with tz)")]


class OrderDirection(str, Enum):
    asc = "asc"
    desc = "desc"


def get_event_list_params(
    sport_id: SportIdQuery = None,
    venue_id: VenueIdQuery = None,
    status_filter: StatusQuery = None,
    date_from: DateFromQuery = None,
    date_to: DateToQuery = None,
    order: Annotated[OrderDirection, Query(description="Sort by starts_at")] = OrderDirection.asc,
    page: Annotated[int, Query(ge=1, description="Page number (1-based)")] = 1,
    page_size: Annotated[int, Query(ge=1, le=100, description="Items per page")] = 20,
) -> EventListParams:
    if date_from and date_to and date_from > date_to:
        # 400 here reads nicer than a server error deeper down
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="date_from must be <= date_to")
    return EventListParams(
        sport_id=sport_id,
        venue_id=venue_id,
        status=status_filter,
        date_from=date_from,
        date_to=date_to,
        order_desc=(order == OrderDirection.desc),
        pagination=Pagination(page=page, page_size=page_size),
    )


ParamsDep = Annotated[EventListParams, Depends(get_event_list_params)]


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
            detail=_describe_integrity_error(exc),
        ) from exc

    response.headers["Location"] = f"/events/{event.id}"
    return EventRead.model_validate(event)


@router.get("", response_model=list[EventRead])
async def list_events(
    session: SessionDep,
    service: ServiceDep,
    params: ParamsDep,
) -> list[EventRead]:
    events = await service.list_events(session, params=params)
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
