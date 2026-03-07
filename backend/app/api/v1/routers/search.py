from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.session import get_db
from backend.app.services import search

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/")
async def query(account_id: int, q: str, folder_id: int | None = None, page: int = 1, db: AsyncSession = Depends(get_db)):
    return await search.search_messages(db, account_id, q, folder_id, page)
