from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None


class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: str | None = None
    is_active: bool
    is_admin: bool
    created_at: datetime

    class Config:
        orm_mode = True


class SessionCreate(BaseModel):
    email: EmailStr
    password: str


class SessionResponse(BaseModel):
    session_token: str
    expires_at: datetime


class ChangePassword(BaseModel):
    current_password: str
    new_password: str


class InviteCode(BaseModel):
    token: str
    expires_at: datetime
