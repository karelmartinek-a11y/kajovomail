from fastapi import APIRouter

from .accounts import router as accounts_router
from .health import router as health_router
from .ai import router as ai_router
from .drafts import router as drafts_router
from .events import router as events_router
from .folders import router as folders_router
from .messages import router as messages_router
from .offers import router as offers_router
from .search import router as search_router
from .users import router as users_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health_router)
api_router.include_router(users_router)
api_router.include_router(accounts_router)
api_router.include_router(ai_router)
api_router.include_router(drafts_router)
api_router.include_router(events_router)
api_router.include_router(folders_router)
api_router.include_router(messages_router)
api_router.include_router(offers_router)
api_router.include_router(search_router)

__all__ = ["api_router"]
