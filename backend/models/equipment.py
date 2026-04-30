from sqlalchemy import Column, ForeignKey, CheckConstraint, UniqueConstraint, String, Text, text, Boolean, BigInteger, Integer, DateTime, Date, Time
from sqlalchemy.sql import func
from models.base import Base

class Equipment(Base):
    __tablename__ = "equipments"
    __table_args__ = (
        CheckConstraint("type IN ('projector', 'ac', 'chair', 'table', 'board', 'computer', 'speaker')", name="cc_equipments_type"),
        CheckConstraint("status IN ('active', 'broken', 'maintenance')", name="cc_equipments_status"),
    )

    id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False, server_default=text("'active'"))
    description = Column(String(255), nullable=True)
    usage_guide = Column(Text, nullable=False)
    code = Column(String(50), nullable=False, unique=True)
    qr_code = Column(Text, nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())