from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from repositories.user_repo import UserRepository
from repositories.auth_repo import AuthRepository
from services.auth_service import AuthService

async def get_user_repo(db: AsyncSession = Depends(get_db)):
    return UserRepository(db)

async def get_auth_repo(db: AsyncSession = Depends(get_db)):
    return AuthRepository(db)

async def get_auth_service(u_repo: UserRepository = Depends(get_user_repo), a_repo: AuthRepository = Depends(get_auth_repo)):
    return AuthService(user_repo=u_repo, auth_repo=a_repo)