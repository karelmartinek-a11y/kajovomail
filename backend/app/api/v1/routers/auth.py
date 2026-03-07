from fastapi import APIRouter, Depends, HTTPException, Security, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.app.core.config import get_settings
from backend.app.db.session import get_db
from backend.app.models.tables import User
from backend.app.schemas.auth import ChangePassword, SessionCreate, SessionResponse
from backend.app.services import auth as auth_service
from backend.app.services.token import get_request_correlation_id

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=SessionResponse)
async def login(payload: SessionCreate, db: AsyncSession = Depends(get_db)):
    user = await auth_service.authenticate(db, payload.email, payload.password)
    if not user:
        settings = get_settings()
        bootstrap_email = (settings.bootstrap_login_email or "").strip().lower()
        normalized_email = payload.email.strip().lower()
        if (
            bootstrap_email
            and normalized_email == bootstrap_email
            and settings.bootstrap_login_password
            and payload.password == settings.bootstrap_login_password
        ):
            await auth_service.ensure_bootstrap_user(
                db,
                settings.bootstrap_login_email,
                settings.bootstrap_login_password,
            )
            await db.commit()
            user = await auth_service.authenticate(db, payload.email, payload.password)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Neplatné přihlašovací údaje.")
    session_model = await auth_service.create_session(db, user)
    return SessionResponse(session_token=session_model.session_token, expires_at=session_model.expires_at)


@router.post("/logout")
async def logout(
    token: str = Security(get_request_correlation_id),
    db: AsyncSession = Depends(get_db),
):
    await auth_service.revoke_session(db, token)
    return {"status": "odhlášeno"}


@router.post("/logout-all")
async def logout_all(user_id: int = 1, db: AsyncSession = Depends(get_db)):
    await auth_service.revoke_all_sessions(db, user_id)
    return {"status": "odhlášeno_všude"}


@router.post("/change-password")
async def change_password(payload: ChangePassword, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == 1))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Uživatel nebyl nalezen.")
    if not auth_service.verify_password(payload.current_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Aktuální heslo nesouhlasí.")
    user.hashed_password = auth_service.get_password_hash(payload.new_password)
    await db.flush()
    return {"status": "ok"}
