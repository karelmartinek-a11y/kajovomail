from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.session import get_db
from backend.app.services import folders

router = APIRouter(prefix="/folders", tags=["folders"])


@router.get("/")
async def list_folders(account_id: int, db: AsyncSession = Depends(get_db)):
    return await folders.list_folders(db, account_id)


@router.post("/")
async def create_folder(account_id: int, name: str, db: AsyncSession = Depends(get_db)):
    return await folders.create_folder(db, account_id, name)


@router.post("/{folder_id}/rename")
async def rename_folder(folder_id: int, name: str, db: AsyncSession = Depends(get_db)):
    return await folders.rename_folder(db, folder_id, name)
