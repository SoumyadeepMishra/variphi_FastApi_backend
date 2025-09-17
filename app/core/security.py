# # app/core/security.py
# from passlib.context import CryptContext
# from jose import jwt, JWTError
# from datetime import datetime, timedelta
# from typing import Optional, Dict, Any
# from fastapi import HTTPException, status

# from app.config import settings

# # Password hashing context (bcrypt)
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# # ---------------- Password helpers ----------------
# def get_password_hash(password: str) -> str:
#     """Return bcrypt hash for given plain password."""
#     return pwd_context.hash(password)


# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     """Verify plain password against hashed password."""
#     return pwd_context.verify(plain_password, hashed_password)


# # ---------------- JWT helpers ----------------
# def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
#     """
#     Create a JWT access token containing the given data.
#     `data` should already contain identifying claims (e.g. {"sub": <username>, "role": <role>}).
#     """
#     to_encode = data.copy()
#     expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=settings.access_token_expire_minutes))
#     to_encode.update({"exp": expire})
#     token = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
#     return token


# def decode_access_token(token: str) -> Dict[str, Any]:
#     """
#     Decode JWT token and return payload dict.
#     Raises HTTPException 401 if token is invalid/expired.
#     """
#     try:
#         payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
#         return payload
#     except JWTError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Could not validate credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

# app/core/security.py
from passlib.context import CryptContext
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import HTTPException, status

from app.config import settings

# Password hashing context (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---------------- Password helpers ----------------
def get_password_hash(password: str) -> str:
    """Hash a plain password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


# ---------------- JWT helpers ----------------
def create_access_token(
    data: Dict[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token containing the given data.
    Example `data`: {"sub": <username>, "role": <role>}
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta
        if expires_delta
        else timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return token


def decode_access_token(token: str) -> Dict[str, Any]:
    """
    Decode JWT token and return payload dict.
    Raises HTTPException 401 if token is invalid/expired.
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

