from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime
from models.user import User

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    async def get_by_id(self, user_id: int): # Đảm bảo tên hàm CHÍNH XÁC là get_by_id
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    async def get_by_external_id(self, external_id: str):
        result = await self.db.execute(select(User).where(User.external_id == external_id))
        return result.scalar_one_or_none()
    # repositories/user_repo.py

    async def get_by_email(self, email: str):
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
    async def update_last_login(self, user: User):
        user.last_login_at = datetime.now()
        await self.db.commit()
    # repositories/user_repo.py

    async def update_user(self, user_id: int, update_data: dict):
        # 1. Lấy user object đang gắn với session hiện tại
        user = await self.get_by_id(user_id)
        if not user:
            return None
        
        # 2. Cập nhật các trường dữ liệu
        for key, value in update_data.items():
            setattr(user, key, value)
        
        # 3. Cập nhật thời gian sửa đổi
        user.updated_at = datetime.now()
        
        try:
            # Sử dụng flush để đẩy dữ liệu xuống DB tạm thời để kiểm tra lỗi Integrity (nếu có)
            await self.db.flush() 
            # Sau đó mới commit
            await self.db.commit()
            # Refresh để đồng bộ lại dữ liệu mới nhất từ DB vào object
            await self.db.refresh(user)
            return user
        except Exception as e:
            await self.db.rollback()
            # Log lỗi chi tiết ra console để biết chính xác là lỗi gì
            print(f"DEBUG UPDATE ERROR: {str(e)}")
            raise e
    async def get_by_id(self, user_id: int):
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
    async def update_password(self, user_id: int, new_hashed_password: str):
        user = await self.get_by_id(user_id)
        if user:
            user.password_hash = new_hashed_password
            await self.db.commit()
            await self.db.refresh(user)
        return user