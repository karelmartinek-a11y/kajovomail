import hashlib
import hmac
import logging
import secrets
import uuid
from datetime import datetime, timedelta

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.tables import Session, User

logger = logging.getLogger(__name__)


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
    new_user = User(email=email.lower(), hashed_password=get_password_hash(password), full_name=full_name)
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


async def get_user_by_session_token(session: AsyncSession, token: str) -> User | None:
    now = datetime.utcnow()
    result = await session.execute(
        select(User)
        .join(Session, Session.user_id == User.id)
        .where(Session.session_token == token, Session.expires_at > now)
    )
    return result.scalar_one_or_none()


async def ensure_bootstrap_user(
    session: AsyncSession, email: str | None, password: str | None
) -> User | None:
    if not email or not password:
        logger.info(
            "Bootstrap user skipped because KAJOVOMAIL_LOGIN_EMAIL/KAJOVOMAIL_LOGIN_PASSWORD are missing."
        )
        return None

    normalized_email = email.strip().lower()
    result = await session.execute(select(User).where(User.email == normalized_email))
    user = result.scalar_one_or_none()

    if user is None:
        user = await create_user(
            session,
            email=normalized_email,
            password=password,
            full_name="KajovoMail Admin",
        )
        user.is_admin = True
        user.is_active = True
        await session.flush()
        logger.info("Created bootstrap user '%s'.", normalized_email)
        return user

    password_changed = False
    if not verify_password(password, user.hashed_password):
        user.hashed_password = get_password_hash(password)
        password_changed = True

    if not user.is_admin:
        user.is_admin = True
    if not user.is_active:
        user.is_active = True
    if not user.full_name:
        user.full_name = "KajovoMail Admin"

    await session.flush()
    if password_changed:
        logger.info("Bootstrap user '%s' password has been updated.", normalized_email)
    else:
        logger.info("Bootstrap user '%s' already exists.", normalized_email)
    return user
