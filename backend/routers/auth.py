from fastapi import APIRouter, Depends, status, Request
from schemas.auth import LoginRequest, LoginResponse, UserMeResponse, UserUpdateMe, TokenRefreshRequest, ChangePasswordRequest
from services.auth_service import AuthService
from dependencies.services import get_auth_service
from dependencies.auth import get_current_user
from dependencies.permission import is_admin
from models.user import User
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login(request: Request, data: OAuth2PasswordRequestForm = Depends(), service: AuthService = Depends(get_auth_service)):
    ip_address = request.client.host
    device_info = request.headers.get("user-agent")
    return await service.login(external_id=data.username, password=data.password, ip=ip_address, device=device_info)

@router.post("/refresh", response_model=dict)
async def refresh_token(data: TokenRefreshRequest, service: AuthService = Depends(get_auth_service)):
    return await service.refresh_access_token(data.refresh_token)

@router.get("/me", response_model=UserMeResponse)
async def read_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.patch("/me", response_model=UserMeResponse)
async def update_me(data: UserUpdateMe, current_user: User = Depends(get_current_user), service: AuthService = Depends(get_auth_service)):
    return await service.update_profile(current_user.id, data)

@router.post("/logout")
async def logout(data: TokenRefreshRequest, service: AuthService = Depends(get_auth_service)):
    return await service.logout(data.refresh_token)

@router.post("/change-password")
async def change_password(
    data: ChangePasswordRequest,
    current_user: User = Depends(get_current_user), # Chỉ người đã đăng nhập mới đổi được
    service: AuthService = Depends(get_auth_service)
):
    return await service.change_password(user_id=current_user.id, passwords=data)