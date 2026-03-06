from typing import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.tables import Account


async def list_accounts(session: AsyncSession, user_id: int) -> list[Account]:
    result = await session.execute(select(Account).where(Account.user_id == user_id))
    return result.scalars().all()


async def add_account(
    session: AsyncSession,
    user_id: int,
    provider: str,
    email: str,
    credentials: dict,
    capability_flags: list[str] | None = None,
) -> Account:
    account = Account(
        user_id=user_id,
        provider=provider,
        email=email,
        credentials=credentials,
        capability_flags=capability_flags or [],
    )
    session.add(account)
    await session.flush()
    await session.refresh(account)
    return account
