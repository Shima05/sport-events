from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class EventStatus(str, Enum):
    SCHEDULED = "scheduled"
    LIVE = "live"
    FINISHED = "finished"
    CANCELLED = "cancelled"


class Event(Base):
    __tablename__ = "events"
    __table_args__ = (CheckConstraint("starts_at < ends_at", name="events_starts_before_ends"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sport_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("sports.id", name="fk_events_sport_id_sports"),
        index=True,
    )
    venue_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("venues.id", name="fk_events_venue_id_venues"),
        nullable=True,
    )
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    status: Mapped[EventStatus] = mapped_column(
        SQLEnum(EventStatus, name="event_status", create_type=False),
        default=EventStatus.SCHEDULED,
        server_default=EventStatus.SCHEDULED.value,
    )
    ticket_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        server_default=text("timezone('utc', now())"),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        server_default=text("timezone('utc', now())"),
    )

    sport = relationship("Sport", back_populates="events")
    venue = relationship("Venue", back_populates="events")
    participants = relationship("EventParticipant", back_populates="event", cascade="all, delete-orphan")


class EventParticipantRole(str, Enum):
    HOME = "home"
    AWAY = "away"
    PARTICIPANT = "participant"


class EventParticipant(Base):
    __tablename__ = "event_participants"
    __table_args__ = (
        UniqueConstraint(
            "event_id",
            "role",
            name="uq_event_participants_event_id_role",
        ),
        UniqueConstraint(
            "event_id",
            "team_id",
            name="uq_event_participants_event_id_team_id",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("events.id", name="fk_event_participants_event_id_events"),
    )
    team_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("teams.id", name="fk_event_participants_team_id_teams"),
    )
    role: Mapped[EventParticipantRole] = mapped_column(
        SQLEnum(EventParticipantRole, name="event_participant_role", create_type=False),
        default=EventParticipantRole.PARTICIPANT,
        server_default=EventParticipantRole.PARTICIPANT.value,
    )

    event = relationship("Event", back_populates="participants")
    team = relationship("Team", back_populates="participants")
