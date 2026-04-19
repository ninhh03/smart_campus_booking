from sqlalchemy import (Column, BigInteger, String, Date, DateTime, Text, ForeignKey, Index, UniqueConstraint, CheckConstraint, text)
from models.base import Base

class Booking(Base):
    __tablename__ = "bookings"
    __table_args__ = (
        UniqueConstraint("room_id", "slot_id", "date", name="uq_room_slot_date"),
        Index("idx_booking_date", "date"),
        Index("idx_booking_room_date", "room_id", "date"),
        Index("idx_booking_user", "user_id"),
        Index("idx_booking_status", "status"),
        CheckConstraint("status IN ('pending', 'approved', 'rejected', 'cancelled', 'completed')", name="ck_booking_status"),
        CheckConstraint("source IN ('manual', 'ai')", name="ck_booking_source"),
    )

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    room_id = Column(BigInteger, ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False)
    slot_id = Column(BigInteger, ForeignKey("slots.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(String(30), nullable=False)
    approved_by = Column(BigInteger, ForeignKey("users.id"), nullable=True)
    approved_at = Column(DateTime, nullable=True)
    source = Column(String(20), nullable=False)
    note = Column(Text, nullable=True)
    checked_in_at = Column(DateTime, nullable=True)
    cancelled_at = Column(DateTime, nullable=True)
    cancelled_by = Column(BigInteger, ForeignKey("users.id"), nullable=True)
    cancel_reason = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"))