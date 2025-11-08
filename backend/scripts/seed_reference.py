import asyncio

from app.db.seeds import seed_reference_data
from app.db.session import async_session_factory


async def _main() -> None:
    session_factory = async_session_factory()
    async with session_factory() as session:
        await seed_reference_data(session)


if __name__ == "__main__":
    asyncio.run(_main())
