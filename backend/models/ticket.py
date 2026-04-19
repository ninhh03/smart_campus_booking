from sqlalchemy import (Column, BigInteger, String, Text, DateTime, ForeignKey, Index, CheckConstraint, text)
from models.base import Base

class Ticket(Base):
    __tablename__ = "tickets"
    __table_args__ = (
        Index("idx_ticket_status", "status"),
        Index("idx_ticket_type", "type"),
        Index("idx_ticket_user", "user_id"),
        Index("idx_ticket_booking", "booking_id"),
        Index("idx_ticket_room", "room_id"),
        CheckConstraint("status IN ('open', 'in_progress', 'resolved', 'closed')", name="ck_ticket_status"),
        CheckConstraint("type IN ('equipment', 'booking', 'system', 'ai_anomaly')", name="ck_ticket_type"),
    )

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    room_id = Column(BigInteger, ForeignKey("rooms.id", ondelete="SET NULL"), nullable=True)
    equipment_id = Column(BigInteger, ForeignKey("equipments.id", ondelete="SET NULL"), nullable=True)
    booking_id = Column(BigInteger, ForeignKey("bookings.id", ondelete="SET NULL"), nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(30), nullable=False)
    type = Column(String(30), nullable=False)
    resolved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"))