from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from core.security import create_access_token
from shared.utils import verify_password, hash_password
from core.config import settings
from schemas.auth import UserUpdateMe, ChangePasswordRequest

class AuthService:
    def __init__(self, user_repo, auth_repo):
        self.user_repo = user_repo
        self.auth_repo = auth_repo
    async def login(self, external_id: str, password: str, ip: str = None, device: str = None):
        user = await self.user_repo.get_by_external_id(external_id)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=401, detail="ID hoặc mật khẩu không chính xác")
        access_token = create_access_token(
            data={"sub": user.external_id, "role": user.role}
        )
        refresh_token_str = create_access_token(
            data={"sub": user.external_id, "type": "refresh"},
            expires_delta=timedelta(days=7)
        )
        expires_at = (datetime.now(timezone.utc) + timedelta(days=7)).replace(tzinfo=None)
        await self.auth_repo.create_refresh_token(
            user_id=user.id,
            token=refresh_token_str,
            expires_at=expires_at,
            ip=ip,
            device=device
        )
        await self.user_repo.update_last_login(user)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token_str,
            "user": {
                "id": user.id,
                "external_id": user.external_id,
                "full_name": user.full_name,
                "role": user.role
            }
        }
    async def refresh_access_token(self, refresh_token_str: str):
        db_token = await self.auth_repo.get_refresh_token(refresh_token_str)
        if not db_token or db_token.revoked_at or db_token.expires_at < datetime.now():
            raise HTTPException(status_code=401, detail="Refresh token không hợp lệ hoặc đã hết hạn")
        user = await self.user_repo.get_by_id(db_token.user_id)
        new_access_token = create_access_token(data={"sub": user.external_id, "role": user.role})
        return {
            "access_token": new_access_token,
            "refresh_token": refresh_token_str
        }
    async def logout(self, refresh_token_str: str):
        db_token = await self.auth_repo.get_refresh_token(refresh_token_str)
        if db_token:
            await self.auth_repo.revoke_token(db_token)
        return {"message": "Logout successful"}

    async def update_profile(self, user_id: int, update_data: UserUpdateMe):
        # 1. Tìm user để đảm bảo nó tồn tại
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User không tồn tại")

        # 2. Lấy dữ liệu thực tế gửi lên
        update_dict = update_data.model_dump(exclude_unset=True)

        # 3. Không có gì đổi thì trả về luôn
        if not update_dict:
            return user

        # 4. Kiểm tra trùng email (Bạn đã làm rất tốt chỗ này)
        if "email" in update_dict:
            existing_user = await self.user_repo.get_by_email(update_dict["email"])
            if existing_user and existing_user.id != user_id:
                raise HTTPException(status_code=400, detail="Email này đã được sử dụng")

        # 5. THAY ĐỔI Ở ĐÂY: Truyền ID thay vì truyền object user
        # Việc này giúp tránh lỗi "Object out of sync" của SQLAlchemy
        return await self.user_repo.update_user(user_id, update_dict)
    async def change_password(self, user_id: int, passwords: ChangePasswordRequest):
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User không tồn tại")
        if not verify_password(passwords.old_password, user.password_hash):
            raise HTTPException(status_code=400, detail="Mật khẩu cũ không chính xác")
        new_hashed = hash_password(passwords.new_password)
        await self.user_repo.update_password(user_id, new_hashed)
        return {"message": "Đổi mật khẩu thành công"}