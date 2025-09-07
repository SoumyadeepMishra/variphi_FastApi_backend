from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta

from app.database import get_db
from app.models.user import User as UserModel
from app.schemas.user import User, UserCreate, UserUpdate, Token
from app.services.user_service import UserService
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# Dependency for injecting UserService
def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)

# ---------------- Create User ----------------
@router.post("/", response_model=Token, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    """Create a new user and return access token"""

    # Check if user with email already exists
    if user_service.get_user_by_email(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Check if user with username already exists
    if user_service.get_user_by_username(user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    # Create user
    new_user = user_service.create_user(user)
    
    # Generate JWT token using AuthService
    auth_service = AuthService(user_service.db)
    access_token_expires = timedelta(minutes=30)
    access_token = auth_service.create_access_token(
        data={"sub": new_user.username},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


# ---------------- Get User by ID ----------------
@router.get("/{user_id}", response_model=User)
def get_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
):
    """Get user by ID"""
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


# ---------------- Get All Users ----------------
@router.get("/", response_model=List[User])
def get_all_users(
    skip: int = 0,
    limit: int = 100,
    user_service: UserService = Depends(get_user_service)
):
    """Get all users with pagination"""
    return user_service.get_users(skip=skip, limit=limit)


# ---------------- Update User ----------------
@router.put("/{user_id}", response_model=User)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    user_service: UserService = Depends(get_user_service)
):
    """Update user"""
    updated_user = user_service.update_user(user_id, user_update)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return updated_user


# ---------------- Delete User ----------------
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
):
    """Delete user"""
    success = user_service.delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
