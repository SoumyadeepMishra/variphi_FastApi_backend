# from sqlalchemy.orm import Session
# from typing import List, Optional
# from app.models.user import User
# from app.schemas.user import UserCreate, UserUpdate
# from passlib.context import CryptContext

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# class UserService:
#     """User business logic service"""

#     def __init__(self, db: Session):
#         self.db = db

#     def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
#         """Get all users with pagination"""
#         return self.db.query(User).offset(skip).limit(limit).all()

#     def get_user(self, user_id: int) -> Optional[User]:
#         """Get user by ID"""
#         return self.db.query(User).filter(User.id == user_id).first()

#     def get_user_by_email(self, email: str) -> Optional[User]:
#         """Get user by email"""
#         return self.db.query(User).filter(User.email == email).first()

#     def get_user_by_username(self, username: str) -> Optional[User]:
#         """Get user by username"""
#         return self.db.query(User).filter(User.username == username).first()

#     def create_user(self, user: UserCreate) -> User:
#         """Create a new user"""
#         hashed_password = pwd_context.hash(user.password)
#         db_user = User(
#             email=user.email,
#             username=user.username,
#             full_name=user.full_name,
#             hashed_password=hashed_password,
#             is_active=user.is_active,
#            # role=user.role  # 👈 Added role field
#         )
#         self.db.add(db_user)
#         self.db.commit()
#         self.db.refresh(db_user)
#         return user

#     def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
#         """Update user"""
#         db_user = self.get_user(user_id)
#         if not db_user:
#             return None

#         update_data = user_update.dict(exclude_unset=True)
#         if "password" in update_data:
#             update_data["hashed_password"] = pwd_context.hash(update_data.pop("password"))

#         for field, value in update_data.items():
#             setattr(db_user, field, value)

#         self.db.commit()
#         self.db.refresh(db_user)
#         return db_user

#     def delete_user(self, user_id: int) -> bool:
#         """Delete user"""
#         db_user = self.get_user(user_id)
#         if not db_user:
#             return False

#         self.db.delete(db_user)
#         self.db.commit()
#         return True

#     def verify_password(self, plain_password: str, hashed_password: str) -> bool:
#         """Verify password"""
#         return pwd_context.verify(plain_password, hashed_password)

from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    """User business logic service"""

    def __init__(self, db: Session):
        self.db = db

    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination"""
        return self.db.query(User).offset(skip).limit(limit).all()

    def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self.db.query(User).filter(User.username == username).first()

    def create_user(self, user: UserCreate) -> User:
        """Create a new user"""
        hashed_password = pwd_context.hash(user.password)
        db_user = User(
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            hashed_password=hashed_password,
            is_active=user.is_active,
            roles=getattr(user, "roles", ["user"]),  # 👈 default role = ["user"]
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user  # 👈 returning db_user instead of input schema

    def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """Update user"""
        db_user = self.get_user(user_id)
        if not db_user:
            return None

        update_data = user_update.dict(exclude_unset=True)

        # password hashing
        if "password" in update_data:
            update_data["hashed_password"] = pwd_context.hash(update_data.pop("password"))

        # roles update (if provided)
        if "roles" in update_data and update_data["roles"] is None:
            update_data.pop("roles")  # don’t overwrite roles with None

        for field, value in update_data.items():
            setattr(db_user, field, value)

        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete_user(self, user_id: int) -> bool:
        """Delete user"""
        db_user = self.get_user(user_id)
        if not db_user:
            return False

        self.db.delete(db_user)
        self.db.commit()
        return True

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password"""
        return pwd_context.verify(plain_password, hashed_password)
