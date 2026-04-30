from sqlalchemy import Column, ForeignKey, CheckConstraint, UniqueConstraint, String, Text, text, Boolean, BigInteger, Integer, DateTime, Date, Time
from sqlalchemy.sql import func
from models.base import Base

class Ticket(Base):
    __tablename__ = "tickets"
    __table_args__ = (
        CheckConstraint("type IN ('equipment', 'booking')", name="cc_tickets_type"),
        CheckConstraint("status IN ('open', 'in_progress', 'resolved', 'closed')", name="cc_tickets_status"),
        CheckConstraint("resolved_at >= created_at", name="cc_tickets_resolved_at"),
    )

    id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    equipment_id = Column(BigInteger, ForeignKey("equipments.id", ondelete="SET NULL"), nullable=True)
    room_id = Column(BigInteger, ForeignKey("rooms.id"), nullable=True)
    booking_id = Column(BigInteger, ForeignKey("bookings.id"), nullable=True)
    title = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False, server_default=text("'open'"))
    description = Column(Text, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())