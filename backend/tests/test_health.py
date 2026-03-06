import pytest


@pytest.mark.asyncio
async def test_health_endpoints(async_client):
    response = await async_client.get("/api/v1/health/live")
    assert response.status_code == 200
    response = await async_client.get("/api/v1/health/ready")
    assert response.status_code == 200
