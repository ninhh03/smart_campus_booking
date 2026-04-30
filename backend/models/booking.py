from sqlalchemy import Column, ForeignKey, CheckConstraint, UniqueConstraint, String, Text, text, Boolean, BigInteger, Integer, DateTime, Date, Time
from sqlalchemy.sql import func
from models.base import Base

class Booking(Base):
    __tablename__ = "bookings"
    __table_args__ = (
        UniqueConstraint("room_id", "slot_id", "date", "cancelled_at", name="uc_bookings_room_slot_date_cancelled_at"),
        CheckConstraint("date >= CURRENT_DATE", name="cc_bookings_date"),
        CheckConstraint("source IN ('manual', 'ai')", name="cc_bookings_source"),
        CheckConstraint("status IN ('pending', 'approved', 'rejected', 'cancelled', 'completed')", name="cc_bookings_status"),
        CheckConstraint("approved_at >= created_at", name="cc_bookings_approved_at"),
        CheckConstraint("checked_in_at >= approved_at", name="cc_bookings_checkin_at"),
        CheckConstraint("cancelled_at >= created_at", name="cc_bookings_cancelled_at"),
    )

    id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    room_id = Column(BigInteger, ForeignKey("rooms.id"), nullable=False)
    slot_id = Column(BigInteger, ForeignKey("slots.id"), nullable=False)
    date = Column(Date, nullable=False)
    source = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False, server_default=text("'pending'"))
    note = Column(String(255), nullable=True)
    approved_at = Column(DateTime, nullable=True)
    checked_in_at = Column(DateTime, nullable=True)
    cancelled_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())