from datetime import datetime
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.tables import Account
from backend.app.schemas.accounts import AccountCreate, AccountRead
from backend.app.services import token


async def list_accounts(session: AsyncSession, user_id: int) -> list[Account]:
    result = await session.execute(select(Account).where(Account.user_id == user_id))
    return result.scalars().all()


async def add_account(session: AsyncSession, payload: AccountCreate, user_id: int) -> Account:
    account = Account(
        user_id=user_id,
        provider=payload.provider,
        provider_type=payload.provider,
        email=payload.email,
        credentials=payload.credentials,
        capability_flags=payload.capability_flags or [],
        server=payload.credentials.get("server"),
        display_name=payload.credentials.get("display_name"),
        is_pop3=payload.credentials.get("protocol") == "pop3",
    )
    session.add(account)
    await session.flush()
    await session.refresh(account)
    return account


async def discover_capabilities(session: AsyncSession, account_id: int) -> dict:
    account = await session.get(Account, account_id)
    if not account:
        raise ValueError("account not found")
    caps = {"protocols": ["IMAP", "SMTP"], "features": ["folders", "threading"]}
    if account.is_pop3:
        caps["limited"] = True
    return caps


async def test_connection(session: AsyncSession, account_id: int) -> bool:
    account = await session.get(Account, account_id)
    if not account:
        return False
    return True


async def mark_sync(session: AsyncSession, account_id: int, cursor: str) -> None:
    await session.execute(
        update(Account)
        .where(Account.id == account_id)
        .values(last_sync=datetime.utcnow(), sync_cursor=cursor)
    )
