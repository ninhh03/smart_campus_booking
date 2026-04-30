from sqlalchemy import Column, ForeignKey, CheckConstraint, UniqueConstraint, String, Text, text, Boolean, BigInteger, Integer, DateTime, Date, Time
from sqlalchemy.sql import func
from models.base import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint("gender IN ('male', 'female')", name="cc_users_gender"),
        CheckConstraint("date_of_birth < CURRENT_DATE", name="cc_users_date_of_birth"),
        CheckConstraint("phone ~ '^[0-9]{10}$'", name="cc_users_phone"),
        CheckConstraint("email LIKE '%@%'", name="cc_users_email"),
        CheckConstraint("status IN ('active', 'block')", name="cc_users_status"),
        CheckConstraint("role IN ('admin', 'lecturer', 'student')", name="cc_users_role"),
    )

    id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True)
    external_id = Column(String(50), nullable=False, unique=True)
    full_name = Column(String(255), nullable=False)
    gender = Column(String(50), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    phone = Column(String(50), nullable=True)
    email = Column(String(255), nullable=False, unique=True)
    graduation_date = Column(Date, nullable=True)
    password_hash = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False, server_default=text("'active'"))
    role = Column(String(50), nullable=False, server_default=text("'student'"))
    last_login_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())