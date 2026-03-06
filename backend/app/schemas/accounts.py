from pydantic import BaseModel, EmailStr


class AccountCreate(BaseModel):
    provider: str
    email: EmailStr
    credentials: dict
    capability_flags: list[str] | None = None


class AccountRead(BaseModel):
    id: int
    provider: str
    email: EmailStr
    capability_flags: list[str]

    class Config:
        orm_mode = True
