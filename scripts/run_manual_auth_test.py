print('starting manual auth test script', flush=True)
print('setting env defaults', flush=True)

import asyncio
import os

os.environ.setdefault('DATABASE_URL', 'sqlite+aiosqlite:///./backend/tests/test.db')
os.environ.setdefault('REDIS_URL', 'redis://localhost:6379/1')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('ENVIRONMENT', 'test')

from backend.app.main import app
from backend.app.db.session import AsyncSessionLocal
from backend.app.services import auth as auth_service
from backend.app.models.tables import User
from httpx import AsyncClient


async def main():
    print('opening session', flush=True)
    async with AsyncSessionLocal() as session:
        user = User(email='tester@example.com', hashed_password=auth_service.get_password_hash('secret'))
        session.add(user)
        await session.commit()
    print('session committed', flush=True)

    async with AsyncClient(app=app, base_url='http://testserver') as client:
        print('client ready, sending request', flush=True)
        response = await client.post('/api/v1/auth/login', json={'email': 'tester@example.com', 'password': 'secret'})
        print('status', response.status_code, flush=True)
        print('body', response.text, flush=True)


asyncio.run(main())
