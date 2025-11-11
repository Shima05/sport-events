from uuid import UUID

from app.schemas.base import Schema


class TeamRead(Schema):
    id: UUID
    sport_id: UUID
    name: str
    abbr: str | None = None
