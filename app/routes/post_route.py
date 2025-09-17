# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from typing import List

# from app.database import get_db
# from app.schemas.post import Post, PostCreate, PostUpdate, PostWithAuthor
# from app.schemas.user import User
# from app.services.post_service import PostService
# from app.services.auth_service import get_current_user

# router = APIRouter(
#     prefix="/posts",
#     tags=["posts"]
# )

# # Dependency for injecting PostService
# def get_post_service(db: Session = Depends(get_db)) -> PostService:
#     return PostService(db)

# # ---------------- Create Post ----------------
# @router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
# def create_post(
#     post: PostCreate,
#     current_user: User = Depends(get_current_user),
#     post_service: PostService = Depends(get_post_service)
# ):
#     """Create a new post"""
#     return post_service.create_post(post, current_user.id)

# # ---------------- Get All Posts ----------------
# @router.get("/", response_model=List[Post])
# def get_all_posts(
#     skip: int = 0,
#     limit: int = 100,
#     post_service: PostService = Depends(get_post_service)
# ):
#     """Get all posts with pagination"""
#     return post_service.get_posts(skip=skip, limit=limit)

# # ---------------- Get Post by ID ----------------
# @router.get("/{post_id}", response_model=Post)
# def get_post(
#     post_id: int,
#     post_service: PostService = Depends(get_post_service)
# ):
#     """Get post by ID"""
#     post = post_service.get_post(post_id)
#     if not post:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Post not found"
#         )
#     return post

# # ---------------- Get Posts by Author ----------------
# @router.get("/author/{author_id}", response_model=List[Post])
# def get_posts_by_author(
#     author_id: int,
#     skip: int = 0,
#     limit: int = 100,
#     post_service: PostService = Depends(get_post_service)
# ):
#     """Get all posts by a specific author"""
#     return post_service.get_posts_by_author(author_id, skip=skip, limit=limit)

# # ---------------- Get My Posts ----------------
# @router.get("/me/posts", response_model=List[Post])
# def get_my_posts(
#     skip: int = 0,
#     limit: int = 100,
#     current_user: User = Depends(get_current_user),
#     post_service: PostService = Depends(get_post_service)
# ):
#     """Get current user's posts"""
#     return post_service.get_posts_by_author(current_user.id, skip=skip, limit=limit)

# # ---------------- Update Post ----------------
# @router.put("/{post_id}", response_model=Post)
# def update_post(
#     post_id: int,
#     post_update: PostUpdate,
#     current_user: User = Depends(get_current_user),
#     post_service: PostService = Depends(get_post_service)
# ):
#     """Update post (only by the author)"""
#     updated_post = post_service.update_post(post_id, post_update, current_user.id)
#     if not updated_post:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Post not found or you don't have permission to edit this post"
#         )
#     return updated_post

# # ---------------- Delete Post ----------------
# @router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(
#     post_id: int,
#     current_user: User = Depends(get_current_user),
#     post_service: PostService = Depends(get_post_service)
# ):
#     """Delete post (only by the author)"""
#     success = post_service.delete_post(post_id, current_user.id)
#     if not success:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Post not found or you don't have permission to delete this post"
#         )

# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from typing import List

# from app.database import get_db
# from app.schemas.post import Post, PostCreate, PostUpdate
# from app.schemas.user import User
# from app.services.post_service import PostService
# from app.services.auth_service import get_current_user
# from app.core.roles import role_required  # 👈 correct import

# router = APIRouter(
#     prefix="/posts",
#     tags=["posts"]
# )

# # Dependency for injecting PostService
# def get_post_service(db: Session = Depends(get_db)) -> PostService:
#     return PostService(db)


# # ---------------- Create Post ----------------
# @router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
# def create_post(
#     post: PostCreate,
#     current_user: User = Depends(get_current_user),
#     post_service: PostService = Depends(get_post_service)
# ):
#     """Create a new post"""
#     return post_service.create_post(post, current_user.id)


# # ---------------- Get All Posts ----------------
# @router.get("/", response_model=List[Post])
# def get_all_posts(
#     skip: int = 0,
#     limit: int = 100,
#     post_service: PostService = Depends(get_post_service)
# ):
#     """Get all posts with pagination"""
#     return post_service.get_posts(skip=skip, limit=limit)


# # ---------------- Get Post by ID ----------------
# @router.get("/{post_id}", response_model=Post)
# def get_post(
#     post_id: int,
#     post_service: PostService = Depends(get_post_service)
# ):
#     """Get post by ID"""
#     post = post_service.get_post(post_id)
#     if not post:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Post not found"
#         )
#     return post


# # ---------------- Get Posts by Author ----------------
# @router.get("/author/{author_id}", response_model=List[Post])
# def get_posts_by_author(
#     author_id: int,
#     skip: int = 0,
#     limit: int = 100,
#     post_service: PostService = Depends(get_post_service)
# ):
#     """Get all posts by a specific author"""
#     return post_service.get_posts_by_author(author_id, skip=skip, limit=limit)


# # ---------------- Get My Posts ----------------
# @router.get("/me/posts", response_model=List[Post])
# def get_my_posts(
#     skip: int = 0,
#     limit: int = 100,
#     current_user: User = Depends(get_current_user),
#     post_service: PostService = Depends(get_post_service)
# ):
#     """Get current user's posts"""
#     return post_service.get_posts_by_author(current_user.id, skip=skip, limit=limit)


# # ---------------- Update Post ----------------
# @router.put("/{post_id}", response_model=Post)
# def update_post(
#     post_id: int,
#     post_update: PostUpdate,
#     current_user: User = Depends(get_current_user),
#     post_service: PostService = Depends(get_post_service)
# ):
#     """Update post (only author or admin can update)"""
#     post = post_service.get_post(post_id)
#     if not post:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Post not found"
#         )

#     # Allow if current user is author OR admin
#     if post.author_id != current_user.id and current_user.role != "admin":
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="You don't have permission to edit this post"
#         )

#     return post_service.update_post(post_id, post_update, current_user.id)


# # ---------------- Delete Post ----------------
# @router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(
#     post_id: int,
#     current_user: User = Depends(get_current_user),
#     post_service: PostService = Depends(get_post_service)
# ):
#     """Delete post (only author or admin can delete)"""
#     post = post_service.get_post(post_id)
#     if not post:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Post not found"
#         )

#     # Allow if current user is author OR admin
#     if post.author_id != current_user.id and current_user.role != "admin":
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="You don't have permission to delete this post"
#         )

#     success = post_service.delete_post(post_id, current_user.id)
#     if not success:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Failed to delete post"
#         )

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.post import Post, PostCreate, PostUpdate
from app.schemas.user import User
from app.services.post_service import PostService
from app.services.auth_service import get_current_user
from app.core.roles import role_required  # 👈 correct import

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

# Dependency for injecting PostService
def get_post_service(db: Session = Depends(get_db)) -> PostService:
    return PostService(db)


# ---------------- Create Post ----------------
@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
def create_post(
    post: PostCreate,
    current_user: User = Depends(get_current_user),
    post_service: PostService = Depends(get_post_service)
):
    """Create a new post"""
    return post_service.create_post(post, current_user.id)


# ---------------- Get All Posts ----------------
@router.get("/", response_model=List[Post])
def get_all_posts(
    skip: int = 0,
    limit: int = 100,
    post_service: PostService = Depends(get_post_service)
):
    """Get all posts with pagination"""
    return post_service.get_posts(skip=skip, limit=limit)


# ---------------- Get Post by ID ----------------
@router.get("/{post_id}", response_model=Post)
def get_post(
    post_id: int,
    post_service: PostService = Depends(get_post_service)
):
    """Get post by ID"""
    post = post_service.get_post(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    return post


# ---------------- Get Posts by Author ----------------
@router.get("/author/{author_id}", response_model=List[Post])
def get_posts_by_author(
    author_id: int,
    skip: int = 0,
    limit: int = 100,
    post_service: PostService = Depends(get_post_service)
):
    """Get all posts by a specific author"""
    return post_service.get_posts_by_author(author_id, skip=skip, limit=limit)


# ---------------- Get My Posts ----------------
@router.get("/me/posts", response_model=List[Post])
def get_my_posts(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    post_service: PostService = Depends(get_post_service)
):
    """Get current user's posts"""
    return post_service.get_posts_by_author(current_user.id, skip=skip, limit=limit)


# ---------------- Update Post ----------------
@router.put("/{post_id}", response_model=Post)
def update_post(
    post_id: int,
    post_update: PostUpdate,
    current_user: User = Depends(get_current_user),
    post_service: PostService = Depends(get_post_service)
):
    """Update post (only author or admin can update)"""
    post = post_service.get_post(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    # ✅ Allow if current user is author OR has "admin" role
    if post.author_id != current_user.id and "admin" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to edit this post"
        )

    return post_service.update_post(post_id, post_update, current_user.id)


# ---------------- Delete Post ----------------
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    post_service: PostService = Depends(get_post_service)
):
    """Delete post (only author or admin can delete)"""
    post = post_service.get_post(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    # ✅ Allow if current user is author OR has "admin" role
    if post.author_id != current_user.id and "admin" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this post"
        )

    success = post_service.delete_post(post_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to delete post"
        )
