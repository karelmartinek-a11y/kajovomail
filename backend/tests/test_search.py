import pytest

from backend.app.db.base import Base
from backend.app.db.session import AsyncSessionLocal
from backend.app.tests.helpers import seed_message
from backend.app.services.search import search_messages


@pytest.mark.asyncio
async def test_search_basic(asyncio_loop):
    async with AsyncSessionLocal() as session:
        await session.run_sync(Base.metadata.drop_all)
        await session.run_sync(Base.metadata.create_all)
        await seed_message(session, subject="Hello world", account_id=1, folder_id=1, body="text")
        await session.commit()
        results = await search_messages(session, 1, "Hello")
        assert len(results) == 1
