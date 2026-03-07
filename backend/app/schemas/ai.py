from datetime import datetime

from pydantic import BaseModel


class AIRequestCreate(BaseModel):
    account_id: int | None = None
    body: str


class AIRequestResponse(BaseModel):
    id: int
    user_id: int
    account_id: int | None
    input_payload: dict
    result: dict
    major_status: str
    created_at: datetime
    updated_at: datetime
