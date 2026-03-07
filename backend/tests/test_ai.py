import pytest
from backend.app.services import ai
from backend.app.db.base import Base
from backend.app.db.session import AsyncSessionLocal


@pytest.mark.asyncio
async def test_ai_orchestration_respects_schema():
    async with AsyncSessionLocal() as session:
        await session.run_sync(Base.metadata.drop_all)
        await session.run_sync(Base.metadata.create_all)
        request = await ai.orchestrate_response(session, user_id=1, account_id=None, prompt={"body": "hello"})
        assert request.major_status == "complete"
        assert "plaintext" in request.result
