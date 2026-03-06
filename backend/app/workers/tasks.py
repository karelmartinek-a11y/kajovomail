from __future__ import annotations

from celery.utils.log import get_task_logger

from backend.app.workers import celery_app

logger = get_task_logger(__name__)


@celery_app.task(bind=True)
def sync_mail(self, account_id: int) -> str:
    logger.info("Starting mail sync for account %s", account_id)
    self.retry(countdown=10)
    logger.info("Mail sync complete for account %s", account_id)
    return "synced"


@celery_app.task(bind=True)
def generate_ai_response(self, user_id: int) -> dict:
    logger.info("Generating AI response for user %s", user_id)
    return {"user": user_id, "status": "queued"}
