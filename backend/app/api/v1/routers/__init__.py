from fastapi import APIRouter

from .auth import router as auth_router
from .health import router as health_router
from .users import router as users_router
from .accounts import router as accounts_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(accounts_router)

__all__ = ["api_router"]
