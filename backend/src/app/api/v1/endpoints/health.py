from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["Health"], summary="Service readiness probe")
async def readiness() -> dict[str, str]:
    """Simple endpoint to confirm the API is up."""

    return {"status": "ok"}
