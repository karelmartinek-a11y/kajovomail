from fastapi import HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.tables import User
from backend.app.services import auth as auth_service

SESSION_COOKIE_NAME = "kajovo_session"


async def get_current_user(request: Request, db: AsyncSession) -> User:
    token = request.cookies.get(SESSION_COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=401, detail="Missing session")

    session_model = await auth_service.get_session(db, token)
    if not session_model:
        raise HTTPException(status_code=401, detail="Session expired")

    user = await db.get(User, session_model.user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
