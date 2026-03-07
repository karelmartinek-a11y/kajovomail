from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.config import get_settings
from backend.app.db.session import get_db
from backend.app.models.tables import User
from backend.app.schemas.auth import SessionCreate
from backend.app.services import auth as auth_service

SESSION_COOKIE_NAME = "kajovo_session"
settings = get_settings()

router = APIRouter(prefix="/session", tags=["session"])


def _session_payload(user: User | None, csrf_token: str | None) -> dict:
    return {
        "user": (
            {
                "id": str(user.id),
                "email": user.email,
                "name": user.full_name or user.email,
                "roles": ["admin"] if user.is_admin else ["user"],
            }
            if user
            else None
        ),
        "csrfToken": csrf_token,
    }


@router.post("/login")
async def login(
    response: Response,
    payload: SessionCreate,
    db: AsyncSession = Depends(get_db),
):
    user = await auth_service.authenticate(db, payload.email, payload.password)
    if not user:
        response.status_code = 401
        return {"message": "Invalid credentials"}

    session_model = await auth_service.create_session(db, user)
    await db.commit()

    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=session_model.session_token,
        httponly=True,
        secure=settings.is_production,
        samesite="lax",
        expires=int(session_model.expires_at.replace(tzinfo=timezone.utc).timestamp()),
        path="/",
    )
    return _session_payload(user, session_model.session_token)


@router.get("/current")
async def current_session(request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    token = request.cookies.get(SESSION_COOKIE_NAME)
    if not token:
        return _session_payload(None, None)

    session_model = await auth_service.get_session(db, token)
    if not session_model:
        await db.commit()
        response.delete_cookie(SESSION_COOKIE_NAME, path="/")
        return _session_payload(None, None)

    if session_model.expires_at <= datetime.utcnow():
        await auth_service.revoke_session(db, token)
        await db.commit()
        response.delete_cookie(SESSION_COOKIE_NAME, path="/")
        return _session_payload(None, None)

    result = await db.execute(select(User).where(User.id == session_model.user_id))
    user = result.scalar_one_or_none()
    if not user:
        return _session_payload(None, None)
    return _session_payload(user, token)


@router.post("/logout")
async def logout(request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    token = request.cookies.get(SESSION_COOKIE_NAME)
    if token:
        await auth_service.revoke_session(db, token)
        await db.commit()
    response.delete_cookie(SESSION_COOKIE_NAME, path="/")
    return {"status": "logged_out"}
