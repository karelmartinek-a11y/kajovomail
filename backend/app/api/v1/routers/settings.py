from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.session import get_db
from backend.app.models.tables import User
from backend.app.schemas.settings import (
    AIKeyTestRequest,
    AIKeyTestResponse,
    AIModelsResponse,
    AISettingsResponse,
    AISettingsUpdate,
)
from backend.app.services import ai as ai_service
from backend.app.services import auth as auth_service

SESSION_COOKIE_NAME = "kajovo_session"
ALLOWED_STYLES = {"concise", "balanced", "detailed"}

router = APIRouter(prefix="/settings", tags=["settings"])


def _mask_key(api_key: str | None) -> str | None:
    if not api_key:
        return None
    if len(api_key) <= 8:
        return "*" * len(api_key)
    return f"{api_key[:4]}...{api_key[-4:]}"


async def _current_user(request: Request, db: AsyncSession) -> User:
    token = request.cookies.get(SESSION_COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=401, detail="Missing session")
    session_model = await auth_service.get_session(db, token)
    if not session_model:
        raise HTTPException(status_code=401, detail="Session expired")
    result = await db.execute(select(User).where(User.id == session_model.user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@router.get("/ai", response_model=AISettingsResponse)
async def get_ai_settings(request: Request, db: AsyncSession = Depends(get_db)):
    user = await _current_user(request, db)
    return AISettingsResponse(
        has_openai_api_key=bool(user.openai_api_key),
        openai_api_key_masked=_mask_key(user.openai_api_key),
        response_style=user.ai_response_style or "balanced",
        model=user.openai_model,
    )


@router.put("/ai", response_model=AISettingsResponse)
async def update_ai_settings(payload: AISettingsUpdate, request: Request, db: AsyncSession = Depends(get_db)):
    user = await _current_user(request, db)
    touched = getattr(payload, "model_fields_set", set()) or getattr(payload, "__fields_set__", set())

    if "response_style" in touched and payload.response_style is not None:
        normalized = payload.response_style.strip().lower()
        if normalized not in ALLOWED_STYLES:
            raise HTTPException(status_code=400, detail="Unsupported response style")
        user.ai_response_style = normalized

    if "openai_api_key" in touched:
        incoming = (payload.openai_api_key or "").strip()
        user.openai_api_key = incoming or None

    if "model" in touched:
        user.openai_model = (payload.model or "").strip() or None

    await db.commit()
    await db.refresh(user)

    return AISettingsResponse(
        has_openai_api_key=bool(user.openai_api_key),
        openai_api_key_masked=_mask_key(user.openai_api_key),
        response_style=user.ai_response_style or "balanced",
        model=user.openai_model,
    )


@router.post("/ai/test-key", response_model=AIKeyTestResponse)
async def test_openai_key(payload: AIKeyTestRequest, request: Request, db: AsyncSession = Depends(get_db)):
    user = await _current_user(request, db)
    candidate_key = (payload.openai_api_key or "").strip() or (user.openai_api_key or "").strip()
    if not candidate_key:
        return AIKeyTestResponse(valid=False, message="OpenAI API key is not set.", models=[])

    try:
        models = await ai_service.list_openai_models(candidate_key)
    except Exception as exc:
        return AIKeyTestResponse(valid=False, message=str(exc), models=[])
    return AIKeyTestResponse(valid=True, message="OpenAI API key is valid.", models=models)


@router.get("/ai/models", response_model=AIModelsResponse)
async def list_models(request: Request, db: AsyncSession = Depends(get_db)):
    user = await _current_user(request, db)
    key = (user.openai_api_key or "").strip()
    if not key:
        raise HTTPException(status_code=400, detail="OpenAI API key is not configured.")
    models = await ai_service.list_openai_models(key)
    return AIModelsResponse(models=models)
