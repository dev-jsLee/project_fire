from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, BigInteger, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(String(50), primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    name = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 관계 설정
    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    likes = relationship("PostLike", back_populates="user")
    bookmarks = relationship("Bookmark", back_populates="user")

class Post(Base):
    __tablename__ = "posts"

    post_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(50), ForeignKey("users.user_id"), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String(50), default='일반')
    view_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 관계 설정
    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    attachments = relationship("Attachment", back_populates="post", cascade="all, delete-orphan")
    likes = relationship("PostLike", back_populates="post", cascade="all, delete-orphan")
    bookmarks = relationship("Bookmark", back_populates="post", cascade="all, delete-orphan")

class Comment(Base):
    __tablename__ = "comments"

    comment_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    post_id = Column(BigInteger, ForeignKey("posts.post_id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String(50), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 관계 설정
    post = relationship("Post", back_populates="comments")
    user = relationship("User", back_populates="comments")

class Attachment(Base):
    __tablename__ = "attachments"

    attachment_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    post_id = Column(BigInteger, ForeignKey("posts.post_id", ondelete="CASCADE"), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(BigInteger, nullable=False)
    mime_type = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 관계 설정
    post = relationship("Post", back_populates="attachments")

class PostLike(Base):
    __tablename__ = "post_likes"

    post_id = Column(BigInteger, ForeignKey("posts.post_id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(String(50), ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 관계 설정
    post = relationship("Post", back_populates="likes")
    user = relationship("User", back_populates="likes")

class Bookmark(Base):
    __tablename__ = "bookmarks"

    user_id = Column(String(50), ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(BigInteger, ForeignKey("posts.post_id", ondelete="CASCADE"), primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 관계 설정
    post = relationship("Post", back_populates="bookmarks")
    user = relationship("User", back_populates="bookmarks")