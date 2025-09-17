# app/core/roles.py
from fastapi import Depends, HTTPException, status
from typing import Callable, Iterable
from app.core.auth import get_current_user
from app.models.user import User as UserModel

def role_required(required_role: str) -> Callable:
    """
    Dependency factory: only allow users whose user.role == required_role.
    Usage: Depends(role_required("admin"))
    """
    def _dependency(current_user: UserModel = Depends(get_current_user)):
        if getattr(current_user, "role", None) != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied, requires role '{required_role}'"
            )
        return current_user
    return _dependency


def roles_allowed(*allowed_roles: str) -> Callable:
    """
    Dependency factory: allow any of the provided roles.
    Usage: Depends(roles_allowed("admin","moderator"))
    """
    allowed = set(allowed_roles)

    def _dependency(current_user: UserModel = Depends(get_current_user)):
        if getattr(current_user, "role", None) not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied, requires one of roles: {', '.join(allowed)}"
            )
        return current_user
    return _dependency
