from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from app.models.event import EventStatus


@dataclass(frozen=True)
class Pagination:
    page: int = 1
    page_size: int = 20
    max_page_size: int = 100

    def __post_init__(self):
        if self.page < 1:
            raise ValueError("page must be >= 1")
        if self.page_size < 1:
            raise ValueError("page_size must be >= 1")
        if self.max_page_size < 1:
            raise ValueError("max_page_size must be >= 1")

    def limit(self) -> int:
        return min(self.page_size, self.max_page_size)

    def offset(self) -> int:
        return (self.page - 1) * self.limit()


@dataclass(frozen=True)
class EventListParams:
    sport_id: UUID | None = None
    venue_id: UUID | None = None
    status: EventStatus | None = None
    date_from: datetime | None = None
    date_to: datetime | None = None
    order_desc: bool = False
    pagination: Pagination = field(default_factory=Pagination)

    @property
    def limit(self) -> int:
        return self.pagination.limit()

    @property
    def offset(self) -> int:
        return self.pagination.offset()
