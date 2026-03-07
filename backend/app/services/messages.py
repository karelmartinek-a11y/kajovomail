from typing import Iterable

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.tables import Message


async def list_messages(session: AsyncSession, account_id: int, folder_id: int | None = None, page: int = 1, per_page: int = 25) -> list[Message]:
    query = select(Message).where(Message.account_id == account_id)
    if folder_id:
        query = query.where(Message.folder_id == folder_id)
    query = query.order_by(Message.created_at.desc()).offset((page - 1) * per_page).limit(per_page)
    result = await session.execute(query)
    return result.scalars().all()


async def get_message(session: AsyncSession, message_id: int) -> Message | None:
    return await session.get(Message, message_id)


async def mark_read(session: AsyncSession, message_id: int, read: bool = True) -> None:
    await session.execute(update(Message).where(Message.id == message_id).values(is_read=read))


async def set_flag(session: AsyncSession, message_id: int, flag: bool = True) -> None:
    await session.execute(update(Message).where(Message.id == message_id).values(metadata_payload={"flagged": flag}))


async def move_message(session: AsyncSession, message_id: int, folder_id: int) -> None:
    await session.execute(update(Message).where(Message.id == message_id).values(folder_id=folder_id))


async def delete_message(session: AsyncSession, message_id: int) -> None:
    await session.execute(delete(Message).where(Message.id == message_id))
