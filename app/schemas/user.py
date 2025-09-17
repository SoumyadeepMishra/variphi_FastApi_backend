# from pydantic import BaseModel, EmailStr
# from typing import Optional
# from datetime import datetime


# class UserBase(BaseModel):
#     """Base user schema"""
#     email: EmailStr
#     username: str
#     full_name: Optional[str] = None
#     is_active: bool = True


# class UserCreate(UserBase):
#     """Schema for creating a user"""
#     password: str


# class UserUpdate(BaseModel):
#     """Schema for updating a user"""
#     email: Optional[EmailStr] = None
#     username: Optional[str] = None
#     full_name: Optional[str] = None
#     is_active: Optional[bool] = None
#     password: Optional[str] = None


# class UserInDB(UserBase):
#     """Schema for user in database"""
#     id: int
#     hashed_password: str
#     is_superuser: bool
#     created_at: datetime
#     updated_at: Optional[datetime] = None
    
#     class Config:
#         from_attributes = True


# class User(UserBase):
#     """Schema for user response"""
#     id: int
#     is_superuser: bool
#     created_at: datetime
#     updated_at: Optional[datetime] = None
    
#     class Config:
#         from_attributes = True


# class UserLogin(BaseModel):
#     """Schema for user login"""
#     username: str
#     password: str


# class Token(BaseModel):
#     """Schema for access token"""
#     access_token: str
#     token_type: str


# class TokenData(BaseModel):
#     """Schema for token data"""
#     username: Optional[str] = None

# app/schemas/user.py
# from pydantic import BaseModel, EmailStr
# from typing import Optional
# from datetime import datetime


# class UserBase(BaseModel):
#     """Base user schema"""
#     email: EmailStr
#     username: str
#     full_name: Optional[str] = None
#     is_active: bool = True
#     #role: str = "user"   # 👈 Added role field


# class UserCreate(UserBase):
#     """Schema for creating a user"""
#     password: str


# class UserUpdate(BaseModel):
#     """Schema for updating a user"""
#     email: Optional[EmailStr] = None
#     username: Optional[str] = None
#     full_name: Optional[str] = None
#     is_active: Optional[bool] = None
#     password: Optional[str] = None
#     role: Optional[str] = None   # 👈 Added role field


# class UserInDB(UserBase):
#     """Schema for user in database"""
#     id: int
#     hashed_password: str
#     is_superuser: bool
#     role: str   # 👈 Added role field
#     created_at: datetime
#     updated_at: Optional[datetime] = None
    
#     class Config:
#         from_attributes = True


# class User(UserBase):
#     """Schema for user response"""
#     id: int
#     is_superuser: bool
#     role: str   # 👈 Added role field
#     created_at: datetime
#     updated_at: Optional[datetime] = None
    
#     class Config:
#         from_attributes = True


# class UserLogin(BaseModel):
#     """Schema for user login"""
#     username: str
#     password: str


# class Token(BaseModel):
#     """Schema for access token"""
#     access_token: str
#     token_type: str


# class TokenData(BaseModel):
#     """Schema for token data"""
#     username: Optional[str] = None
#     role: Optional[str] = None   # 👈 Added role so we can read from JWT

from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    is_active: bool = True
    roles: List[str] = ["user"]   # 👈 multiple roles


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None
    roles: Optional[List[str]] = None


class UserInDB(UserBase):
    id: int
    hashed_password: str
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class User(UserBase):
    id: int
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    roles: Optional[List[str]] = []   # 👈 multiple roles from JWT

