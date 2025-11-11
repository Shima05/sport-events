from uuid import UUID

from app.schemas.base import Schema


class SportRead(Schema):
    id: UUID
    code: str
    name: str
