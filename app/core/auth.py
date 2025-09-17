# app/core/auth.py
# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from sqlalchemy.orm import Session

# from app.database import get_db
# from app.services.user_service import UserService
# from app.core.security import decode_access_token

# # tokenUrl is used by OpenAPI UI for the "Authorize" button. Keep the same path as your login route.
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     """
#     FastAPI dependency to get current authenticated user (ORM object).
#     - Decodes token (via core.security.decode_access_token)
#     - Reads 'sub' claim (username) from payload
#     - Loads fresh user from DB and checks active status
#     """
#     payload = decode_access_token(token)  # will raise 401 if invalid
#     username: str = payload.get("sub")
#     if username is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

#     user_service = UserService(db)
#     user = user_service.get_user_by_username(username)
#     if user is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="User not found",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

#     if not user.is_active:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Inactive user"
#         )

#     # At this point 'user' is a SQLAlchemy ORM object (with .role, .id, etc.)
#     return user

# app/core/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.services.user_service import UserService
from app.core.security import decode_access_token

# tokenUrl is used by OpenAPI UI for the "Authorize" button. Keep the same path as your login route.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    FastAPI dependency to get current authenticated user (ORM object).
    - Decodes token (via core.security.decode_access_token)
    - Reads 'sub' (username) and 'roles' from payload
    - Loads fresh user from DB and checks active status
    """
    payload = decode_access_token(token)  # raises 401 if invalid
    username: str = payload.get("sub")
    token_roles: List[str] = payload.get("roles", [])

    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_service = UserService(db)
    user = user_service.get_user_by_username(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

    # Extra safety: check that token roles and DB roles align
    if set(token_roles) != set(user.roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Role mismatch in token",
        )

    return user


def require_roles(required_roles: List[str]):
    """
    Dependency generator to enforce role-based access.
    Example:
        @router.get("/admin")
        def admin_dashboard(user: User = Depends(require_roles(["admin"]))):
            return {"msg": "Welcome admin!"}
    """
    def role_checker(user = Depends(get_current_user)):
        if not any(role in user.roles for role in required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required: {required_roles}"
            )
        return user
    return role_checker

