from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.tables import Message


async def list_messages(session: AsyncSession, account_id: int) -> list[Message]:
    result = await session.execute(select(Message).where(Message.account_id == account_id))
    return result.scalars().all()


async def create_message(session: AsyncSession, **payload) -> Message:
    message = Message(**payload)
    session.add(message)
    await session.flush()
    await session.refresh(message)
    return message
