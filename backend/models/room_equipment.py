from sqlalchemy import Column,BigInteger,Text,DateTime,ForeignKey,Index,UniqueConstraint,text
from models.base import Base

class RoomEquipment(Base):
    __tablename__ = "rooms_equipments"
    __table_args__ = (
        UniqueConstraint("room_id", "equipment_id", name="uq_room_equipment"),
        Index("idx_re_room_id", "room_id"),
        Index("idx_re_equipment_id", "equipment_id"),
    )

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    room_id = Column(BigInteger,ForeignKey("rooms.id", ondelete="CASCADE"),nullable=False)
    equipment_id = Column(BigInteger,ForeignKey("equipments.id", ondelete="CASCADE"),nullable=False)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime,server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime,server_default=text("CURRENT_TIMESTAMP"),onupdate=text("CURRENT_TIMESTAMP"))
    deleted_at = Column(DateTime, nullable=True)