from pydantic import BaseModel, EmailStr


class AccountCreate(BaseModel):
    provider: str
    email: EmailStr
    credentials: dict
    capability_flags: list[str] | None = None


class AccountRead(BaseModel):
    id: int
    provider: str
    provider_type: str
    email: EmailStr
    display_name: str | None = None

    class Config:
        orm_mode = True


class Capabilities(BaseModel):
    protocols: list[str]
    features: list[str]
    limited: bool | None = None
