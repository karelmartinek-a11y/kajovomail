from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.session import get_db
from backend.app.services import messages

router = APIRouter(prefix="/messages", tags=["messages"])


@router.get("/")
async def list_messages(account_id: int, folder_id: int | None = None, page: int = 1, db: AsyncSession = Depends(get_db)):
    return await messages.list_messages(db, account_id, folder_id, page)


@router.post("/{message_id}/read")
async def mark_read(message_id: int, db: AsyncSession = Depends(get_db)):
    await messages.mark_read(db, message_id, True)
    return {"ok": True}


@router.post("/{message_id}/flag")
async def flag(message_id: int, db: AsyncSession = Depends(get_db)):
    await messages.set_flag(db, message_id, True)
    return {"ok": True}
