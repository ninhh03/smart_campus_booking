from sqlalchemy import (Column,BigInteger,String,Integer,Boolean,Time,DateTime,Index,text,CheckConstraint)
from models.base import Base

class Slot(Base):
    __tablename__ = "slots"
    __table_args__ = (
        Index("idx_slots_order", "order_index"),
        Index("idx_slots_active", "is_active"),
        CheckConstraint("end_time > start_time", name="ck_slot_time"),
    )

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    order_index = Column(Integer, nullable=False, unique=True)
    is_active = Column(Boolean, server_default=text("TRUE"))
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    created_at = Column(DateTime,server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime,server_default=text("CURRENT_TIMESTAMP"),onupdate=text("CURRENT_TIMESTAMP"))