from datetime import datetime
import os

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.config import get_settings
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
    if not settings.openai_api_key:
        return {"error": "not configured"}
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            "https://api.openai.com/v1/responses",
            headers={"Authorization": f"Bearer {settings.openai_api_key}"},
            json={
                "model": "gpt-4.1",
                "input": prompt,
                "output_format": "json",
                "user": str(user_id),
                "store": False,
            },
        )
        response.raise_for_status()
        data = response.json()
    return data
