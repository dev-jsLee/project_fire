from sqlalchemy.orm import Session
from typing import List, Optional

from src.models.category import Category

def get_categories(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    only_active: bool = True
) -> List[Category]:
    """
    카테고리 목록을 조회합니다.
    """
    query = db.query(Category)
    if only_active:
        query = query.filter(Category.is_active == True)
    return query.offset(skip).limit(limit).all()

def get_category(db: Session, category_id: int) -> Optional[Category]:
    """
    특정 카테고리를 조회합니다.
    """
    return db.query(Category).filter(Category.category_id == category_id).first()

def get_category_by_name(db: Session, name: str) -> Optional[Category]:
    """
    카테고리 이름으로 카테고리를 조회합니다.
    """
    return db.query(Category).filter(Category.name == name).first() 