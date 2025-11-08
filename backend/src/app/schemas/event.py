from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import Field

from app.models.event import EventParticipantRole, EventStatus
from app.schemas.base import Schema


class EventParticipantCreate(Schema):
    team_id: UUID
    role: EventParticipantRole = EventParticipantRole.PARTICIPANT


class EventCreate(Schema):
    sport_id: UUID
    venue_id: UUID | None = None
    title: str
    description: str | None = None
    starts_at: datetime
    ends_at: datetime
    status: EventStatus = EventStatus.SCHEDULED
    ticket_url: str | None = None
    participants: list[EventParticipantCreate] = Field(default_factory=list)


class EventRead(Schema):
    id: UUID
    sport_id: UUID
    venue_id: UUID | None
    title: str
    description: str | None
    starts_at: datetime
    ends_at: datetime
    status: EventStatus
    ticket_url: str | None
