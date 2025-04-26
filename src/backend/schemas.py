from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# 사용자 스키마
class UserBase(BaseModel):
    user_id: str = Field(..., min_length=4, max_length=20)
    email: EmailStr
    name: str = Field(..., min_length=2, max_length=50)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=20)

class UserLogin(BaseModel):
    user_id: str
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    password: Optional[str] = Field(None, min_length=8, max_length=20)

class User(UserBase):
    user_id: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    name: str

# 게시글 스키마
class PostBase(BaseModel):
    title: str
    content: str
    category: Optional[str] = "일반"

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class Post(PostBase):
    post_id: int
    user_id: str
    view_count: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

# 댓글 스키마
class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    post_id: int

class CommentUpdate(CommentBase):
    pass

class Comment(CommentBase):
    comment_id: int
    post_id: int
    user_id: str
    created_at: datetime

    class Config:
        from_attributes = True

# 첨부파일 스키마
class AttachmentBase(BaseModel):
    file_name: str
    file_path: str
    file_size: int
    mime_type: str

class AttachmentCreate(AttachmentBase):
    post_id: int

class Attachment(AttachmentBase):
    attachment_id: int
    post_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# 좋아요 스키마
class PostLikeBase(BaseModel):
    post_id: int
    user_id: str

class PostLike(PostLikeBase):
    created_at: datetime

    class Config:
        from_attributes = True

# 북마크 스키마
class BookmarkBase(BaseModel):
    post_id: int
    user_id: str

class Bookmark(BookmarkBase):
    created_at: datetime

    class Config:
        from_attributes = True

# 페이지네이션 응답 스키마
class Page(BaseModel):
    items: List
    total: int
    page: int
    size: int
    pages: int 