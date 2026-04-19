from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.refresh_token import RefreshToken
from datetime import datetime

class AuthRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    async def create_refresh_token(self, user_id: int, token: str, expires_at: datetime, ip: str = None, device: str = None):
        if expires_at.tzinfo is not None:
            expires_at = expires_at.replace(tzinfo=None)
        new_token = RefreshToken(user_id=user_id, token=token, expires_at=expires_at, ip_address=ip, device_info=device)
        self.db.add(new_token)
        await self.db.commit()
        return new_token
    async def get_refresh_token(self, token: str):
        result = await self.db.execute(select(RefreshToken).where(RefreshToken.token == token))
        return result.scalar_one_or_none()
    async def revoke_token(self, token_obj: RefreshToken):
        token_obj.revoked_at = datetime.now()
        await self.db.commit()