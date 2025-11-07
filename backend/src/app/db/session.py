from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker


def build_engine() -> AsyncEngine:
    raise NotImplementedError("Engine configuration will be added later.")


def async_session_factory() -> async_sessionmaker[AsyncSession]:
    raise NotImplementedError("Session logic will be added later.")
