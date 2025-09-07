from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PostBase(BaseModel):
    """Base post schema"""
    title: str
    content: str


class PostCreate(PostBase):
    """Schema for creating a post"""
    pass


class PostUpdate(BaseModel):
    """Schema for updating a post"""
    title: Optional[str] = None
    content: Optional[str] = None


class Post(PostBase):
    """Schema for post response"""
    id: int
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class PostWithAuthor(Post):
    """Schema for post with author information"""
    author: dict  # This will contain basic user info
    
    class Config:
        from_attributes = True
