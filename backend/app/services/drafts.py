from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.tables import Draft


async def save_draft(session: AsyncSession, user_id: int, account_id: int, plaintext: str, html: str, subject: str | None = None) -> Draft:
    result = await session.execute(select(Draft).where(Draft.user_id == user_id).where(Draft.account_id == account_id))
    draft = result.scalar_one_or_none()
    if draft:
        await session.execute(
            update(Draft)
            .where(Draft.id == draft.id)
            .values(plaintext=plaintext, html=html, subject=subject or draft.subject)
        )
        await session.flush()
        await session.refresh(draft)
        return draft
    draft = Draft(user_id=user_id, account_id=account_id, plaintext=plaintext, html=html, subject=subject or "")
    session.add(draft)
    await session.flush()
    await session.refresh(draft)
    return draft
