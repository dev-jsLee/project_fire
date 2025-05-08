from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.database.session import get_db
from src.schemas.category import Category
from src.crud import category as category_crud

router = APIRouter()

@router.get("/categories", response_model=List[Category])
def get_categories(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    활성화된 카테고리 목록을 조회합니다.
    """
    categories = category_crud.get_categories(db, skip=skip, limit=limit)
    return categories 