from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from ..database import get_db
from ..models.post import Post
from ..models.user import User
from ..schemas.post import PostCreate, PostUpdate, PostResponse
from ..auth import get_current_user
from datetime import datetime
from sqlalchemy import desc

router = APIRouter()

@router.get("/api/posts")
async def get_posts(
    category: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    query = db.query(Post)
    
    if category:
        query = query.filter(Post.category == category)
    
    total = query.count()
    total_pages = (total + page_size - 1) // page_size
    
    posts = query.order_by(desc(Post.created_at))\
        .offset((page - 1) * page_size)\
        .limit(page_size)\
        .all()
    
    return {
        "posts": posts,
        "total": total,
        "total_pages": total_pages,
        "current_page": page
    } 