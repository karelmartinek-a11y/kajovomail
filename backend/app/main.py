from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.v1.routers import api_router
from backend.app.core.config import get_settings
from backend.app.core.logging import configure_logging
from backend.app.db.session import AsyncSessionLocal
from backend.app.services import auth as auth_service
from backend.app.workers import ensure_worker, shutdown

settings = get_settings()
configure_logging("DEBUG" if settings.debug else "INFO")

app = FastAPI(title=settings.project_name, version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.on_event("startup")
async def on_startup():
    async with AsyncSessionLocal() as session:
        await auth_service.ensure_bootstrap_user(
            session,
            settings.bootstrap_login_email,
            settings.bootstrap_login_password,
        )
        await session.commit()

    ensure_worker()


@app.on_event("shutdown")
async def on_shutdown():
    await shutdown()
