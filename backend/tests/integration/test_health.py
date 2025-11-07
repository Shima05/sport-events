import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_readiness_probe(client: AsyncClient) -> None:
    """Health endpoint should respond with a 200 and status payload."""

    response = await client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
