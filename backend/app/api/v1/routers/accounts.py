from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.deps import get_current_user
from backend.app.db.session import get_db
from backend.app.models.tables import User
from backend.app.schemas.accounts import AccountCreate, AccountRead, Capabilities
from backend.app.services import accounts as accounts_service

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("/", response_model=list[AccountRead])
async def list_accounts(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await accounts_service.list_accounts(db, user_id=user.id)


@router.post("/", response_model=AccountRead)
async def create_account(
    payload: AccountCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    account = await accounts_service.add_account(db, payload, user_id=user.id)
    return account


@router.get("/{account_id}/capabilities", response_model=Capabilities)
async def capabilities(
    account_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        caps = await accounts_service.discover_capabilities(db, account_id, user_id=user.id)
        return Capabilities(**caps)
    except ValueError:
        raise HTTPException(status_code=404, detail="Account not found")


@router.post("/{account_id}/test-connection")
async def test_connection(
    account_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    success = await accounts_service.test_connection(db, account_id, user_id=user.id)
    return {"ok": success}
