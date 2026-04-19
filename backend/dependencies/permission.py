from fastapi import Depends, HTTPException, status
from models.user import User
from dependencies.auth import get_current_user
class RoleChecker:
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles
    def __call__(self, user: User = Depends(get_current_user)):
        if user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Quyền hạn của bạn ({user.role}) không được phép thực hiện thao tác này"
            )
        return user
is_admin = RoleChecker(["admin"])
is_lecturer = RoleChecker(["admin", "lecturer"])
is_student = RoleChecker(["student"])