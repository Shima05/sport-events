from fastapi import APIRouter

from app.api.v1.endpoints import events, health, sports, teams

api_router = APIRouter()
api_router.include_router(health.router, prefix="/v1")
api_router.include_router(events.router, prefix="/v1")
api_router.include_router(sports.router, prefix="/v1")
api_router.include_router(teams.router, prefix="/v1")
