from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.config import get_settings
from backend.app.db.session import get_db

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/live")
async def liveness():
    return {"status": "ok"}


@router.get("/ready")
async def readiness(db: AsyncSession = Depends(get_db)):
    settings = get_settings()
    async with db.begin():
        result = await db.execute("SELECT 1")
        _ = result.scalar()
    return {"status": "ready", "database": str(settings.database_url)}
