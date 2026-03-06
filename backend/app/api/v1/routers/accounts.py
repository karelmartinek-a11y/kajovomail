from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.session import get_db
from backend.app.schemas.accounts import AccountCreate, AccountRead
from backend.app.services import accounts as accounts_service

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("/", response_model=list[AccountRead])
async def get_accounts(user_id: int = 1, db: AsyncSession = Depends(get_db)):
    return await accounts_service.list_accounts(db, user_id)


@router.post("/", response_model=AccountRead)
async def create_account(payload: AccountCreate, user_id: int = 1, db: AsyncSession = Depends(get_db)):
    account = await accounts_service.add_account(
        db,
        user_id=1,
        provider=payload.provider,
        email=payload.email,
        credentials=payload.credentials,
        capability_flags=payload.capability_flags,
    )
    return account
