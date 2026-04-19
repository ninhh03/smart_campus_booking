from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from core.config import settings
from repositories.user_repo import UserRepository
from dependencies.services import get_user_repo

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), user_repo: UserRepository = Depends(get_user_repo)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Không thể xác thực thông tin người dùng", headers={"WWW-Authenticate": "Bearer"},)
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        external_id: str = payload.get("sub")
        if external_id is None:
            raise credentials_exception   
    except JWTError:
        raise credentials_exception
    user = await user_repo.get_by_external_id(external_id)
    if user is None:
        raise credentials_exception 
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Tài khoản đã bị khóa")
    return user