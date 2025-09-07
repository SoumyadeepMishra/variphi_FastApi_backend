from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.post import Post
from app.models.user import User
from app.schemas.post import PostCreate, PostUpdate


class PostService:
    """Post business logic service"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_posts(self, skip: int = 0, limit: int = 100) -> List[Post]:
        """Get all posts with pagination"""
        return self.db.query(Post).offset(skip).limit(limit).all()
    
    def get_post(self, post_id: int) -> Optional[Post]:
        """Get post by ID"""
        return self.db.query(Post).filter(Post.id == post_id).first()
    
    def get_posts_by_author(self, author_id: int, skip: int = 0, limit: int = 100) -> List[Post]:
        """Get posts by author ID"""
        return self.db.query(Post).filter(Post.author_id == author_id).offset(skip).limit(limit).all()
    
    def create_post(self, post: PostCreate, author_id: int) -> Post:
        """Create a new post"""
        db_post = Post(
            title=post.title,
            content=post.content,
            author_id=author_id
        )
        self.db.add(db_post)
        self.db.commit()
        self.db.refresh(db_post)
        return db_post
    
    def update_post(self, post_id: int, post_update: PostUpdate, author_id: int) -> Optional[Post]:
        """Update post (only by the author)"""
        db_post = self.db.query(Post).filter(
            Post.id == post_id, 
            Post.author_id == author_id
        ).first()
        
        if not db_post:
            return None
        
        update_data = post_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_post, field, value)
        
        self.db.commit()
        self.db.refresh(db_post)
        return db_post
    
    def delete_post(self, post_id: int, author_id: int) -> bool:
        """Delete post (only by the author)"""
        db_post = self.db.query(Post).filter(
            Post.id == post_id, 
            Post.author_id == author_id
        ).first()
        
        if not db_post:
            return False
        
        self.db.delete(db_post)
        self.db.commit()
        return True
    
    def verify_post_ownership(self, post_id: int, author_id: int) -> bool:
        """Verify if user owns the post"""
        post = self.db.query(Post).filter(
            Post.id == post_id, 
            Post.author_id == author_id
        ).first()
        return post is not None
