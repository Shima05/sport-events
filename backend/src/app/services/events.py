from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.event import Event, EventParticipantRole
from app.repositories import EventRepository, TeamRepository
from app.schemas.event import EventCreate
from app.services.event_filters import EventListParams
from app.services.exceptions import ValidationError


class EventService:
    def __init__(
        self,
        event_repository: EventRepository | None = None,
        team_repository: TeamRepository | None = None,
    ) -> None:
        self._events: EventRepository = event_repository or EventRepository()
        self._teams: TeamRepository = team_repository or TeamRepository()

    async def create_event(
        self,
        session: AsyncSession,
        data: EventCreate,
    ) -> Event:
        self._validate_time_window(data.starts_at, data.ends_at)
        self._validate_participant_roles(data)
        if data.participants:
            await self._validate_participant_teams(session, data)
        return await self._events.create(session, data=data)

    async def list_events(
        self,
        session: AsyncSession,
        *,
        params: EventListParams | None = None,
    ) -> list[Event]:
        params = params or EventListParams()
        return await self._events.list(session, params=params)

    async def get_event(
        self,
        session: AsyncSession,
        event_id: UUID,
    ) -> Event | None:
        return await self._events.get(session, event_id)

    @staticmethod
    def _validate_time_window(starts_at: datetime, ends_at: datetime) -> None:
        if starts_at.tzinfo is None or ends_at.tzinfo is None:
            raise ValidationError("Event timestamps must be timezone-aware (UTC).")
        if starts_at >= ends_at:
            raise ValidationError("Event end time must be after start time.")

    @staticmethod
    def _validate_participant_roles(data: EventCreate) -> None:
        roles_seen: set[EventParticipantRole] = set()
        home_away = {EventParticipantRole.HOME, EventParticipantRole.AWAY}

        for p in data.participants:
            role = p.role
            if role is None:
                continue
            if not isinstance(role, EventParticipantRole):
                try:
                    role = EventParticipantRole(role)
                except ValueError as exc:
                    raise ValidationError(f"Unknown participant role: {p.role}") from exc

            if role in home_away:
                if role in roles_seen:
                    raise ValidationError(f"Duplicate role detected: {role}.")
                roles_seen.add(role)

    async def _validate_participant_teams(
        self,
        session: AsyncSession,
        data: EventCreate,
    ) -> None:
        participant_ids = [p.team_id for p in data.participants]
        unique_ids = set(participant_ids)
        if len(unique_ids) != len(participant_ids):
            raise ValidationError("Duplicate participant teams are not allowed.")

        teams = await self._teams.get_by_ids(session, unique_ids)
        if len(teams) != len(unique_ids):
            raise ValidationError("One or more participant teams do not exist.")

        by_id = {t.id: t for t in teams}
        for team_id in unique_ids:
            team = by_id.get(team_id)
            if team and team.sport_id != data.sport_id:
                raise ValidationError(f"Team '{team.name}' does not belong to the event sport.")
