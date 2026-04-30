from sqlalchemy import Column, ForeignKey, CheckConstraint, UniqueConstraint, String, Text, text, Boolean, BigInteger, Integer, DateTime, Date, Time
from sqlalchemy.sql import func
from models.base import Base

class Room(Base):
    __tablename__ = "rooms"
    __table_args__ = (
        CheckConstraint("type IN ('class', 'lab', 'sport')", name="cc_rooms_type"),
        CheckConstraint("status IN ('active', 'maintenance', 'inactive')", name="cc_rooms_status"),
        CheckConstraint("capacity > 0", name="cc_rooms_capacity"),
    )

    id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    type = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False, server_default=text("'active'"))
    capacity = Column(Integer, nullable=False)
    room_number = Column(String(50), nullable=True)
    floor = Column(String(50), nullable=True)
    building = Column(String(50), nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)