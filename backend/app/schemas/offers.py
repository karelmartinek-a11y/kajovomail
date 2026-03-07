from pydantic import BaseModel


class OfferCreate(BaseModel):
    thread_id: str
    status: str
    metadata: dict
