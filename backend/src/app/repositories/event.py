from __future__ import annotations

from uuid import UUID

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.event import Event, EventParticipant
from app.schemas.event import EventCreate
from app.services.event_filters import EventListParams


class EventRepository:
    async def create(
        self,
        session: AsyncSession,
        *,
        data: EventCreate,
    ) -> Event:
        event = Event(
            sport_id=data.sport_id,
            venue_id=data.venue_id,
            title=data.title,
            description=data.description,
            starts_at=data.starts_at,
            ends_at=data.ends_at,
            status=data.status,
            ticket_url=data.ticket_url,
            participants=[EventParticipant(team_id=p.team_id, role=p.role) for p in data.participants],
        )
        session.add(event)
        await session.flush()
        return event

    async def list(
        self,
        session: AsyncSession,
        *,
        params: EventListParams,
    ) -> list[Event]:
        order_col = Event.starts_at.desc() if params.order_desc else Event.starts_at.asc()
        q: Select[Event] = select(Event).options(selectinload(Event.participants)).order_by(order_col, Event.id)

        if params.sport_id:
            q = q.where(Event.sport_id == params.sport_id)
        if params.venue_id:
            q = q.where(Event.venue_id == params.venue_id)
        if params.status:
            q = q.where(Event.status == params.status)
        if params.date_from:
            q = q.where(Event.starts_at >= params.date_from)
        if params.date_to:
            q = q.where(Event.starts_at <= params.date_to)

        if params.limit:
            q = q.limit(params.limit)
        if params.offset:
            q = q.offset(params.offset)

        result = await session.scalars(q)
        return list(result.all())

    async def get(
        self,
        session: AsyncSession,
        event_id: UUID,
    ) -> Event | None:
        q = select(Event).options(selectinload(Event.participants)).where(Event.id == event_id)
        result = await session.scalars(q)
        return result.one_or_none()
