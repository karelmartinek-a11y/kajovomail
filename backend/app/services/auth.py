import hashlib
import hmac
import secrets
import uuid
from datetime import datetime, timedelta

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.tables import Session, User


def get_password_hash(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 200_000)
    return f"{salt}${digest.hex()}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        salt, digest = hashed_password.split("$", 1)
    except ValueError:
        return False
    new_digest = hashlib.pbkdf2_hmac("sha256", plain_password.encode(), salt.encode(), 200_000)
    return hmac.compare_digest(new_digest.hex(), digest)


async def create_user(session: AsyncSession, email: str, password: str, full_name: str | None = None) -> User:
    new_user = User(email=email, hashed_password=get_password_hash(password), full_name=full_name)
    session.add(new_user)
    await session.flush()
    await session.refresh(new_user)
    return new_user


async def authenticate(session: AsyncSession, email: str, password: str) -> User | None:
    result = await session.execute(select(User).where(User.email == email.lower()))
    user = result.scalar_one_or_none()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


async def create_session(
    session: AsyncSession, user: User, expires_in: int = 60 * 60 * 24
) -> Session:
    token = uuid.uuid4().hex
    expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
    new_session = Session(user_id=user.id, session_token=token, expires_at=expires_at)
    session.add(new_session)
    await session.flush()
    await session.refresh(new_session)
    return new_session


async def get_session(session: AsyncSession, token: str) -> Session | None:
    result = await session.execute(select(Session).where(Session.session_token == token))
    session_model = result.scalar_one_or_none()
    if not session_model:
        return None
    if session_model.expires_at <= datetime.utcnow():
        await revoke_session(session, token)
        return None
    return session_model


async def revoke_session(session: AsyncSession, token: str) -> None:
    await session.execute(delete(Session).where(Session.session_token == token))


async def revoke_all_sessions(session: AsyncSession, user_id: int) -> None:
    await session.execute(delete(Session).where(Session.user_id == user_id))


async def ensure_bootstrap_user(
    session: AsyncSession, email: str | None, password: str | None
) -> None:
    if not email or not password:
        return
    normalized_email = email.strip().lower()
    if not normalized_email:
        return
    result = await session.execute(select(User).where(User.email == normalized_email))
    user = result.scalar_one_or_none()
    if not user:
        await create_user(
            session,
            email=normalized_email,
            password=password,
            full_name="KajovoMail Admin",
        )
        return
    if not verify_password(password, user.hashed_password):
        user.hashed_password = get_password_hash(password)
    user.is_active = True
    user.is_admin = True
