from sqlalchemy import Column, ForeignKey, CheckConstraint, UniqueConstraint, String, Text, text, Boolean, BigInteger, Integer, DateTime, Date, Time
from sqlalchemy.sql import func
from models.base import Base

class AILog(Base):
    __tablename__ = "ai_logs"
    __table_args__ = (
        CheckConstraint("type IN ('natural_language_booking', 'moderation', 'troubleshooting')", name="cc_ai_logs_type"),
        CheckConstraint("status IN ('success', 'flagged', 'escalated', 'failed')", name="cc_ai_logs_status"),
    )

    id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    equipment_id = Column(BigInteger, ForeignKey("equipments.id"), nullable=True)
    room_id = Column(BigInteger, ForeignKey("rooms.id"), nullable=True)
    booking_id = Column(BigInteger, ForeignKey("bookings.id"), nullable=True)
    type = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False)
    input_text = Column(Text, nullable=False)
    output_text = Column(Text, nullable=False)
    metadata_json = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())