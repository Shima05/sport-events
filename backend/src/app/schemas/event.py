from __future__ import annotations

from uuid import UUID

from pydantic import AnyUrl, AwareDatetime, ConfigDict, Field

from app.models.event import EventParticipantRole, EventStatus
from app.schemas.base import Schema


class EventParticipantCreate(Schema):
    team_id: UUID
    role: EventParticipantRole = EventParticipantRole.PARTICIPANT


class EventParticipantRead(Schema):
    team_id: UUID
    role: EventParticipantRole
    team_name: str | None = None


class EventCreate(Schema):
    sport_id: UUID
    venue_id: UUID | None = None
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=10_000)
    starts_at: AwareDatetime
    ends_at: AwareDatetime
    status: EventStatus = EventStatus.SCHEDULED
    ticket_url: AnyUrl | None = None
    participants: list[EventParticipantCreate] = Field(default_factory=list)


class EventRead(Schema):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    sport_id: UUID
    sport_name: str | None = None
    venue_id: UUID | None
    title: str
    description: str | None
    starts_at: AwareDatetime
    ends_at: AwareDatetime
    status: EventStatus
    ticket_url: AnyUrl | None
    participants: list[EventParticipantRead] = Field(default_factory=list)
