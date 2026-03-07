from datetime import datetime

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.config import get_settings
from backend.app.models.tables import User
from backend.app.models.tables import AIRequest


async def orchestrate_response(session: AsyncSession, user_id: int, account_id: int | None, prompt: dict) -> AIRequest:
    settings = get_settings()
    result_payload = {"status": "noop", "plaintext": prompt.get("body", ""), "html": f"<p>{prompt.get('body','')}</p>", "preview": prompt.get("body", "")[:120]}
    ai_request = AIRequest(user_id=user_id, account_id=account_id, input_payload=prompt, result=result_payload, major_status="complete")
    session.add(ai_request)
    await session.flush()
    await session.refresh(ai_request)
    return ai_request


async def call_openai(prompt: str, user_id: int, account_id: int | None = None) -> dict:
    settings = get_settings()
    api_key, style, model = await _resolve_user_openai_settings(None, user_id)
    if not api_key:
        api_key = settings.openai_api_key
    if not model:
        model = "gpt-4.1-mini"
    if not style:
        style = "balanced"
    if not api_key:
        return {"error": "not configured"}

    style_instruction = {
        "concise": "Respond briefly and directly.",
        "balanced": "Respond with balanced detail and clarity.",
        "detailed": "Respond with detailed explanation and thorough context.",
    }.get(style, "Respond with balanced detail and clarity.")

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            "https://api.openai.com/v1/responses",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": model,
                "input": [
                    {"role": "system", "content": style_instruction},
                    {"role": "user", "content": prompt},
                ],
                "output_format": "json",
                "user": str(user_id),
                "store": False,
            },
        )
        response.raise_for_status()
        data = response.json()
    return data


async def _resolve_user_openai_settings(session: AsyncSession | None, user_id: int) -> tuple[str | None, str, str | None]:
    if session is None:
        return None, "balanced", None
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        return None, "balanced", None
    return user.openai_api_key, user.ai_response_style or "balanced", user.openai_model


async def list_openai_models(api_key: str) -> list[str]:
    settings = get_settings()
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(
            "https://api.openai.com/v1/models",
            headers={"Authorization": f"Bearer {api_key}"},
        )
        response.raise_for_status()
        data = response.json()
    entries = data.get("data", [])
    model_ids = sorted([entry.get("id", "") for entry in entries if entry.get("id")])
    if not model_ids and settings.openai_api_key == api_key:
        return ["gpt-4.1-mini"]
    return model_ids
