import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.services import auth as auth_service
from backend.app.db.session import AsyncSessionLocal
from backend.app.models.tables import User


@pytest.mark.asyncio
async def test_login_roundtrip(async_client: AsyncClient):
    async with AsyncSessionLocal() as session:
        user = User(email="tester@example.com", hashed_password=auth_service.get_password_hash("secret"))
        session.add(user)
        await session.commit()

    response = await async_client.post(
        "/api/v1/auth/login", json={"email": "tester@example.com", "password": "secret"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "session_token" in data
