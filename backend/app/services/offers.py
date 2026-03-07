from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.tables import Offer


async def list_offers(session: AsyncSession, thread_id: str) -> list[Offer]:
    result = await session.execute(select(Offer).where(Offer.thread_id == thread_id).order_by(Offer.created_at.desc()))
    return result.scalars().all()


async def upsert_offer(session: AsyncSession, thread_id: str, status: str, metadata: dict) -> Offer:
    result = await session.execute(select(Offer).where(Offer.thread_id == thread_id))
    offer = result.scalar_one_or_none()
    if offer:
        await session.execute(
            update(Offer)
            .where(Offer.id == offer.id)
            .values(status=status, metadata_payload=metadata, updated_at=datetime.utcnow())
        )
        await session.flush()
        await session.refresh(offer)
        return offer
    offer = Offer(thread_id=thread_id, status=status, metadata_payload=metadata)
    session.add(offer)
    await session.flush()
    await session.refresh(offer)
    return offer
