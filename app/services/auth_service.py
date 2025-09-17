# from datetime import datetime, timedelta
# from typing import Optional
# from jose import JWTError, jwt
# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from sqlalchemy.orm import Session
# from app.database import get_db
# from app.config import settings
# from app.services.user_service import UserService

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# class AuthService:
#     """Authentication service"""
    
#     def __init__(self, db: Session):
#         self.db = db
#         self.user_service = UserService(db)
    
#     def authenticate_user(self, username: str, password: str):
#         """Authenticate user with username and password"""
#         user = self.user_service.get_user_by_username(username)
#         if not user:
#             return False
#         if not self.user_service.verify_password(password, user.hashed_password):
#             return False
#         return user
    
#     def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
#         """Create access token"""
#         to_encode = data.copy()
#         if expires_delta:
#             expire = datetime.utcnow() + expires_delta
#         else:
#             expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
#         to_encode.update({"exp": expire})
#         encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
#         return encoded_jwt
    
#     def get_current_user_instance(self, token: str, db: Session):
#         """Get current user from token (instance method)"""
#         credentials_exception = HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Could not validate credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#         try:
#             payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
#             username: str = payload.get("sub")
#             if username is None:
#                 raise credentials_exception
#         except JWTError:
#             raise credentials_exception
        
#         user_service = UserService(db)
#         user = user_service.get_user_by_username(username=username)
#         if user is None:
#             raise credentials_exception
#         return user


# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     """Get current user from token (for FastAPI dependency injection)"""
#     auth_service = AuthService(db)
#     return auth_service.get_current_user_instance(token, db)

# from datetime import datetime, timedelta
# from typing import Optional
# from jose import JWTError, jwt
# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from sqlalchemy.orm import Session
# from app.database import get_db
# from app.config import settings
# from app.services.user_service import UserService

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# class AuthService:
#     """Authentication service"""
    
#     def __init__(self, db: Session):
#         self.db = db
#         self.user_service = UserService(db)
    
#     def authenticate_user(self, username: str, password: str):
#         """Authenticate user with username and password"""
#         user = self.user_service.get_user_by_username(username)
#         if not user:
#             return False
#         if not self.user_service.verify_password(password, user.hashed_password):
#             return False
#         return user
    
#     def create_access_token(self, user, expires_delta: Optional[timedelta] = None):
#         """Create access token with role"""
#         to_encode = {
#             "sub": user.username,   # subject = username
#             "role": user.role       # 👈 role bhi add kar diya
#         }
#         if expires_delta:
#             expire = datetime.utcnow() + expires_delta
#         else:
#             expire = datetime.utcnow() + timedelta(
#                 minutes=settings.access_token_expire_minutes
#             )
#         to_encode.update({"exp": expire})
#         encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
#         return encoded_jwt
    
#     def get_current_user_instance(self, token: str, db: Session):
#         """Get current user from token (instance method)"""
#         credentials_exception = HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Could not validate credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#         try:
#             payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
#             username: str = payload.get("sub")
#             role: str = payload.get("role")   # 👈 role extract kiya
#             if username is None or role is None:
#                 raise credentials_exception
#         except JWTError:
#             raise credentials_exception
        
#         user_service = UserService(db)
#         user = user_service.get_user_by_username(username=username)
#         if user is None:
#             raise credentials_exception
        
#         # Ensure DB user role and token role match (extra safety)
#         if user.role != role:
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail="Role mismatch in token",
#             )
        
#         return user


# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     """Get current user from token (for FastAPI dependency injection)"""
#     auth_service = AuthService(db)
#     return auth_service.get_current_user_instance(token, db)

from datetime import datetime, timedelta
from typing import Optional, List
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.config import settings
from app.services.user_service import UserService
from app.schemas.user import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


class AuthService:
    """Authentication service"""

    def __init__(self, db: Session):
        self.db = db
        self.user_service = UserService(db)

    def authenticate_user(self, username: str, password: str):
        """Authenticate user with username and password"""
        user = self.user_service.get_user_by_username(username)
        if not user:
            return False
        if not self.user_service.verify_password(password, user.hashed_password):
            return False
        return user

    def create_access_token(self, user, expires_delta: Optional[timedelta] = None):
        """Create access token with roles embedded"""
        to_encode = {
            "sub": user.username,   # subject = username
            "roles": user.roles     # 👈 roles (list) add kiya
        }
        expire = datetime.utcnow() + (
            expires_delta if expires_delta 
            else timedelta(minutes=settings.access_token_expire_minutes)
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.secret_key, algorithm=settings.algorithm
        )
        return encoded_jwt

    def get_current_user_instance(self, token: str, db: Session):
        """Get current user from token (instance method)"""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            username: str = payload.get("sub")
            roles: List[str] = payload.get("roles")   # 👈 roles list extract
            if username is None or roles is None:
                raise credentials_exception
            token_data = TokenData(username=username, roles=roles)
        except JWTError:
            raise credentials_exception

        user_service = UserService(db)
        user = user_service.get_user_by_username(username=token_data.username)
        if user is None:
            raise credentials_exception

        # Ensure DB user roles and token roles match (extra safety)
        if set(user.roles) != set(token_data.roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Roles mismatch in token",
            )

        return user


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Get current user from token (for FastAPI dependency injection)"""
    auth_service = AuthService(db)
    return auth_service.get_current_user_instance(token, db)
