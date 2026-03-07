from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.session import get_db
from backend.app.services import drafts

router = APIRouter(prefix="/drafts", tags=["drafts"])


@router.post("/")
async def save(user_id: int, account_id: int, plaintext: str, html: str, db: AsyncSession = Depends(get_db)):
    draft = await drafts.save_draft(db, user_id, account_id, plaintext, html)
    return {"id": draft.id, "status": "saved"}
