import pytest

from app.services.event_filters import EventListParams, Pagination


def test_pagination_clamps_values() -> None:
    pagination = Pagination(page=1, page_size=500)
    assert pagination.limit() == pagination.max_page_size
    assert pagination.offset() == 0


def test_event_list_params_exposes_limit_offset() -> None:
    pagination = Pagination(page=3, page_size=15)
    params = EventListParams(pagination=pagination, order_desc=True)
    assert params.limit == 15
    assert params.offset == 30
    assert params.order_desc is True


@pytest.mark.parametrize(
    "page,page_size,max_page_size",
    [
        (0, 10, 100),
        (1, 0, 100),
        (1, 10, 0),
    ],
)
def test_pagination_rejects_invalid_values(page: int, page_size: int, max_page_size: int) -> None:
    with pytest.raises(ValueError):
        Pagination(page=page, page_size=page_size, max_page_size=max_page_size)
