from typing import Optional
from pydantic import BaseModel
from datetime import date
from pydantic import BaseModel, model_validator

# Login request
class LoginRequest(BaseModel):
    external_id: str
    password: str
    remember_me: bool

# Login response
class TokenInfo(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None

class UserInfo(BaseModel):
    full_name: str
    status: str
    role: str

class SessionInfo(BaseModel):
    issued_at: str
    ip_address: str
    device_info: str

class LoginData(BaseModel):
    tokens: TokenInfo
    user: UserInfo
    session: SessionInfo

class LoginResponse(BaseModel):
    message: str
    status: str
    data: Optional[LoginData] = None

class ErrorResponse(BaseModel):
    message: str
    status: str

# Remember request
class RefreshTokenRequest(BaseModel):
    refresh_token: str

# Remember response
class RefreshTokenData(BaseModel):
    tokens: TokenInfo

class RefreshTokenResponse(BaseModel):
    message: str
    status: str
    data: Optional[RefreshTokenData] = None

# Logout request
class LogoutRequest(BaseModel):
    refresh_token: str

# Logout response
class LogoutResponse(BaseModel):
    message: str
    status: str

# UserProfile response
class UserProfileInfo(BaseModel):
    external_id: str
    full_name: str
    gender: str
    date_of_birth: date
    phone: str
    email: str
    status: str
    role: str

class UserProfileData(BaseModel):
    user: UserProfileInfo

class UserProfileResponse(BaseModel):
    message: str
    status: str
    data: Optional[UserProfileData] = None

# ChangePassword request
class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str

    @model_validator(mode='after')
    def check_passwords_match(self) -> 'ChangePasswordRequest':
        if self.new_password != self.confirm_password:
            raise ValueError('Mật khẩu xác nhận không khớp với mật khẩu mới')
        return self

# ChangePassword response
class ChangePasswordResponse(BaseModel):
    message: str
    status: str