from typing import Iterable

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.tables import Folder


async def list_folders(session: AsyncSession, account_id: int) -> list[Folder]:
    result = await session.execute(select(Folder).where(Folder.account_id == account_id).order_by(Folder.id))
    return result.scalars().all()


async def create_folder(session: AsyncSession, account_id: int, name: str, is_default: bool = False) -> Folder:
    folder = Folder(account_id=account_id, name=name, is_default=is_default)
    session.add(folder)
    await session.flush()
    await session.refresh(folder)
    return folder


async def rename_folder(session: AsyncSession, folder_id: int, name: str) -> Folder:
    await session.execute(update(Folder).where(Folder.id == folder_id).values(name=name))
    return await session.get(Folder, folder_id)


async def delete_folder(session: AsyncSession, folder_id: int) -> None:
    await session.execute(delete(Folder).where(Folder.id == folder_id))


async def move_folder(session: AsyncSession, folder_id: int, new_account_id: int) -> Folder:
    await session.execute(update(Folder).where(Folder.id == folder_id).values(account_id=new_account_id))
    return await session.get(Folder, folder_id)
