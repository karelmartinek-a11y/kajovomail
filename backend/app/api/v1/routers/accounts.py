from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.session import get_db
from backend.app.schemas.accounts import AccountCreate, AccountRead, Capabilities
from backend.app.services import accounts as accounts_service

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("/", response_model=list[AccountRead])
async def list_accounts(db: AsyncSession = Depends(get_db)):
    return await accounts_service.list_accounts(db, user_id=1)


@router.post("/", response_model=AccountRead)
async def create_account(payload: AccountCreate, db: AsyncSession = Depends(get_db)):
    account = await accounts_service.add_account(db, payload, user_id=1)
    return account


@router.get("/{account_id}/capabilities", response_model=Capabilities)
async def capabilities(account_id: int, db: AsyncSession = Depends(get_db)):
    try:
        caps = await accounts_service.discover_capabilities(db, account_id)
        return Capabilities(**caps)
    except ValueError:
        raise HTTPException(status_code=404, detail="Account not found")


@router.post("/{account_id}/test-connection")
async def test_connection(account_id: int, db: AsyncSession = Depends(get_db)):
    success = await accounts_service.test_connection(db, account_id)
    return {"ok": success}
