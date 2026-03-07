from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.session import get_db
from backend.app.schemas.ai import AIRequestCreate, AIRequestResponse
from backend.app.services import ai as ai_service

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/", response_model=AIRequestResponse)
async def generate(payload: AIRequestCreate, db: AsyncSession = Depends(get_db)):
    request = await ai_service.orchestrate_response(db, user_id=1, account_id=payload.account_id, prompt=payload.dict())
    return AIRequestResponse(**request.__dict__)
