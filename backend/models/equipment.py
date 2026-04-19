from sqlalchemy import (Column,BigInteger,String,Text,DateTime,Index, text)
from models.base import Base

class Equipment(Base):
    __tablename__ = "equipments"
    __table_args__ = (
        Index("idx_equipments_code", "code"),
        Index("idx_equipments_status", "status"),
        Index("idx_equipments_type", "type"),
    )

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    code = Column(String(100), nullable=False, unique=True)
    type = Column(String(50), nullable=True)
    status = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    usage_guide = Column(Text, nullable=True)
    qr_code = Column(Text, nullable=True)
    created_at = Column(DateTime,server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"))
    deleted_at = Column(DateTime, nullable=True)