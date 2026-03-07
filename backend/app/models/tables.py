from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from backend.app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    openai_api_key = Column(Text, nullable=True)
    ai_response_style = Column(String(32), default="balanced")
    openai_model = Column(String(64), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    sessions = relationship("Session", back_populates="user")
    accounts = relationship("Account", back_populates="user")


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    session_token = Column(String(255), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_agent = Column(String(255), nullable=True)

    user = relationship("User", back_populates="sessions")


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    provider = Column(String(50), nullable=False)
    provider_type = Column(String(50), nullable=False, default="imap")
    email = Column(String(255), nullable=False)
    display_name = Column(String(255), nullable=True)
    server = Column(String(255), nullable=True)
    is_disabled = Column(Boolean, default=False)
    is_pop3 = Column(Boolean, default=False)
    capability_flags = Column(JSON, default=list)
    credentials = Column(JSON, nullable=False)
    sync_cursor = Column(String(255), nullable=True)
    last_sync = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="accounts")


class Folder(Base):
    __tablename__ = "folders"

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    name = Column(String(255), nullable=False)
    is_default = Column(Boolean, default=False)
    is_favorite = Column(Boolean, default=False)
    provider_id = Column(String(255), nullable=True)


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    folder_id = Column(Integer, ForeignKey("folders.id"), nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    subject = Column(String(512), nullable=False)
    body = Column(Text, nullable=True)
    is_read = Column(Boolean, default=False)
    has_attachment = Column(Boolean, default=False)
    thread_id = Column(String(255), nullable=True)
    provider_uid = Column(String(255), nullable=True)
    metadata_payload = Column("metadata", JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)

    attachments = relationship("Attachment", back_populates="message")


class Draft(Base):
    __tablename__ = "drafts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    subject = Column(String(512), nullable=True)
    plaintext = Column(Text, default="")
    html = Column(Text, default="")


class Offer(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True)
    thread_id = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False)
    metadata_payload = Column("metadata", JSON, default=dict)
    updated_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)
    source = Column(String(100), nullable=False)
    user_id = Column(Integer, nullable=True)
    session_id = Column(Integer, nullable=True)
    correlation_id = Column(String(255), nullable=True)
    action = Column(String(255), nullable=False)
    payload = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class AIRequest(Base):
    __tablename__ = "ai_requests"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    input_payload = Column(JSON, nullable=False)
    major_status = Column(String(50), default="queued")
    result = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (UniqueConstraint("user_id", "id", name="uq_ai_request_user_id"),)


class Attachment(Base):
    __tablename__ = "attachments"

    id = Column(Integer, primary_key=True)
    message_id = Column(Integer, ForeignKey("messages.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    content_type = Column(String(255), nullable=False)
    size = Column(Integer, nullable=False)
    stored_path = Column(String(1024), nullable=False)

    message = relationship("Message", back_populates="attachments")
