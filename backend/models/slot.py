from sqlalchemy import Column, ForeignKey, CheckConstraint, UniqueConstraint, String, Text, text, Boolean, BigInteger, Integer, DateTime, Date, Time
from sqlalchemy.sql import func
from models.base import Base

class Slot(Base):
    __tablename__ = "slots"
    __table_args__ = (
        CheckConstraint("order_index > 0", name="cc_slots_order_index"),
        CheckConstraint("status IN ('active', 'inactive')", name="cc_slots_status"),
        CheckConstraint("end_time > start_time", name="cc_slots_start_time_end_time"),
        UniqueConstraint("start_time", "end_time", name="uc_slots_start_time_end_time"),
    )

    id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    order_index = Column(Integer, nullable=False, unique=True)
    status = Column(String(50), nullable=False, server_default=text("'active'"))
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)