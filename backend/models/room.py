from sqlalchemy import (Column,BigInteger,String,Integer,DateTime,Index,Text, text)
from models.base import Base

class Room(Base):
    __tablename__ = "rooms"
    __table_args__ = (
        Index("idx_rooms_type", "type"),
        Index("idx_rooms_status", "status"),
        Index("idx_rooms_capacity", "capacity"),
    )

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False)
    capacity = Column(Integer, nullable=False)
    room_number = Column(String(50), nullable=False, unique=True)
    floor = Column(Integer, nullable=True)
    building = Column(String(100), nullable=True)
    created_at = Column(DateTime,server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime,server_default=text("CURRENT_TIMESTAMP"),onupdate=text("CURRENT_TIMESTAMP"))
    deleted_at = Column(DateTime, nullable=True)