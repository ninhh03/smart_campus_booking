from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, date
from typing import Optional

class LoginRequest(BaseModel):
    external_id: str = Field(..., example="B20DCCN001")
    password: str = Field(..., min_length=6, example="123456")

class TokenRefreshRequest(BaseModel):
    refresh_token: str

class UserUpdateMe(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None

class UserBriefResponse(BaseModel):
    id: int
    external_id: str
    full_name: str
    role: str
    class Config:
        from_attributes = True

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: UserBriefResponse

class UserMeResponse(BaseModel):
    id: int
    external_id: str
    full_name: str
    gender: str
    date_of_birth: date
    email: EmailStr
    phone: str
    role: str
    is_active: bool
    last_login_at: Optional[datetime] = None
    class Config:
        from_attributes = True


class ChangePasswordRequest(BaseModel):
    old_password: str = Field(..., description="Mật khẩu hiện tại")
    new_password: str = Field(..., min_length=6, description="Mật khẩu mới (tối thiểu 6 ký tự)")
    confirm_password: str = Field(..., min_length=6)
    class Config:
        from_attributes = True