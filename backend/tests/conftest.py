import os

os.environ.setdefault('ENVIRONMENT', 'test')
os.environ.setdefault('CELERY_TASK_ALWAYS_EAGER', 'true')
os.environ.setdefault('DATABASE_URL', 'sqlite+aiosqlite:///./backend/tests/test.db')
os.environ.setdefault('REDIS_URL', 'redis://localhost:6379/1')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('OPENAI_API_KEY', '')

from backend.app.main import app
from backend.app.db.base import Base
from backend.app.db.session import engine

import pytest_asyncio
import pytest
from httpx import AsyncClient
from httpx import ASGITransport

pytest_plugins = ["pytest_asyncio"]


@pytest_asyncio.fixture(scope='session')
async def prepare_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def async_client(prepare_db):
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://testserver') as client:
        yield client
