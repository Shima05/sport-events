from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime
from uuid import UUID

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.event import Event, EventParticipant
from app.schemas.event import EventCreate


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
        sport_id: UUID | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        limit: int | None = None,
        offset: int | None = None,
        overlap: bool = False,
    ) -> Sequence[Event]:
        query: Select[Event] = select(Event).options(selectinload(Event.participants)).order_by(Event.starts_at)

        if sport_id:
            query = query.where(Event.sport_id == sport_id)

        if date_from and date_to and overlap:
            query = query.where((Event.ends_at >= date_from) & (Event.starts_at <= date_to))
        else:
            if date_from:
                query = query.where(Event.starts_at >= date_from)
            if date_to:
                query = query.where(Event.starts_at <= date_to)

        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)

        result = await session.execute(query)
        return list(result.scalars().all())

    async def get(
        self,
        session: AsyncSession,
        event_id: UUID,
    ) -> Event | None:
        query = select(Event).options(selectinload(Event.participants)).where(Event.id == event_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()
