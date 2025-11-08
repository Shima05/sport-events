from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Team(Base):
    __tablename__ = "teams"
    __table_args__ = (UniqueConstraint("sport_id", "name", name="uq_teams_sport_id_name"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sport_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("sports.id", name="fk_teams_sport_id_sports"),
        index=True,
    )
    name: Mapped[str] = mapped_column(String(255))
    abbr: Mapped[str | None] = mapped_column(String(16), nullable=True)
    founded_year: Mapped[int | None] = mapped_column(Integer, nullable=True)

    sport = relationship("Sport", back_populates="teams")
    participants = relationship("EventParticipant", back_populates="team", cascade="all, delete-orphan")
