from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, Date, CheckConstraint, text, Text
from models.base import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint("role IN ('admin', 'student', 'lecturer')", name="ck_users_role"),
    )

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    external_id = Column(String(50), nullable=False, unique=True)
    full_name= Column(String(255), nullable=False)
    gender = Column(String(20), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    email = Column(String(255), nullable=False, unique=True)
    phone = Column(String(20), nullable=False, unique=True)
    role = Column(String(20), nullable=False)
    is_active = Column(Boolean, nullable=False, server_default=text("TRUE"))
    password_hash = Column(Text, nullable=False)
    last_login_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=True, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, nullable=True, server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"))