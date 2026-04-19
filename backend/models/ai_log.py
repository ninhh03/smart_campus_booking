from sqlalchemy import (Column, BigInteger, String, Text, DateTime, ForeignKey, Index, CheckConstraint, text)
from models.base import Base

class AILog(Base):
    __tablename__ = "ai_logs"
    __table_args__ = (
        Index("idx_ai_logs_user", "user_id"),
        Index("idx_ai_logs_booking", "booking_id"),
        Index("idx_ai_logs_type", "type"),
        Index("idx_ai_logs_status", "status"),
        Index("idx_ai_logs_created_at", "created_at"),
        CheckConstraint("type IN ('booking_parse', 'booking_review', 'support', 'chatbot', 'anomaly_detect')", name="ck_ai_logs_type"),
        CheckConstraint("status IN ('success', 'failed', 'rejected')", name="ck_ai_logs_status"),
    )

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    booking_id = Column(BigInteger, ForeignKey("bookings.id", ondelete="SET NULL"), nullable=True)
    type = Column(String(50), nullable=False)
    input = Column(Text, nullable=False)
    output = Column(Text, nullable=True)
    status = Column(String(30), nullable=False)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))