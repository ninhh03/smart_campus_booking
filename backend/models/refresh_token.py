from sqlalchemy import Column, ForeignKey, CheckConstraint, UniqueConstraint, String, Text, text, Boolean, BigInteger, Integer, DateTime, Date, Time
from sqlalchemy.sql import func
from models.base import Base

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    __table_args__ = (
        CheckConstraint("ip_address ~ '^[0-9.]+$'", name="cc_user_sessions_ip_address"),
        CheckConstraint("expired_at > issued_at", name="cc_user_sessions_expired_at"),
        CheckConstraint("revoked_at >= issued_at", name="cc_user_sessions_revoked_at"),
    )

    id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    device_info = Column(String(255), nullable=False)
    ip_address = Column(String(50), nullable=False)
    token = Column(Text, nullable=False, unique=True)
    issued_at = Column(DateTime, nullable=False, server_default=func.now())
    expired_at = Column(DateTime, nullable=False)
    revoked_at = Column(DateTime, nullable=True)