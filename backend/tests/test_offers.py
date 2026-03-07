import pytest

from backend.app.db.base import Base
from backend.app.db.session import AsyncSessionLocal
from backend.app.services import offers


@pytest.mark.asyncio
async def test_offer_state_flow():
    async with AsyncSessionLocal() as session:
        await session.run_sync(Base.metadata.drop_all)
        await session.run_sync(Base.metadata.create_all)
        offer = await offers.upsert_offer(session, "thread-1", "draft", {"note": "first"})
        assert offer.status == "draft"
        newest = await offers.upsert_offer(session, "thread-1", "sent", {"note": "sent"})
        assert newest.status == "sent"
