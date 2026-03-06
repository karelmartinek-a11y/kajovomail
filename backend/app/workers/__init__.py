import os

from celery import Celery

from backend.app.core.config import get_settings

settings = get_settings()

if settings.environment == "test":
    celery_app = None


    def ensure_worker() -> None:
        return


    async def shutdown() -> None:
        return
else:
    celery_app = Celery(
        "kajovomail_worker",
        broker=settings.redis_url,
        backend=settings.redis_url,
    )

    celery_app.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        task_default_retry_delay=5,
        task_return_exceptions=False,
        task_annotations={"*": {"max_retries": 3}},
    )

    if os.environ.get("CELERY_TASK_ALWAYS_EAGER", "false").lower() in ("1", "true", "yes"):
        celery_app.conf.task_always_eager = True
        celery_app.conf.task_eager_propagates = True


    def ensure_worker() -> None:
        celery_app.loader.import_module("backend.app.workers.tasks")


    async def shutdown() -> None:
        celery_app.control.broadcast("shutdown")
