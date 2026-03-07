from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.session import get_db
from backend.app.schemas.offers import OfferCreate
from backend.app.services import offers

router = APIRouter(prefix="/offers", tags=["offers"])


@router.post("/")
async def create_offer(payload: OfferCreate, db: AsyncSession = Depends(get_db)):
    offer = await offers.upsert_offer(db, payload.thread_id, payload.status, payload.metadata)
    return {"id": offer.id, "status": offer.status}


@router.get("/{thread_id}")
async def list_offers(thread_id: str, db: AsyncSession = Depends(get_db)):
    return await offers.list_offers(db, thread_id)
