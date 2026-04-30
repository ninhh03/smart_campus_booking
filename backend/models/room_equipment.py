from sqlalchemy import Column, ForeignKey, CheckConstraint, UniqueConstraint, String, Text, text, Boolean, BigInteger, Integer, DateTime, Date, Time
from sqlalchemy.sql import func
from models.base import Base

class RoomEquipment(Base):
    __tablename__ = "rooms_equipments"
    __table_args__ = (
        UniqueConstraint("room_id", "equipment_id", name="uc_rooms_equipments_room_equipment"),
    )

    id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True)
    room_id = Column(BigInteger, ForeignKey("rooms.id"), nullable=False)
    equipment_id = Column(BigInteger, ForeignKey("equipments.id", ondelete="CASCADE"), nullable=False)