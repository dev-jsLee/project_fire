from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text
from sqlalchemy.orm import relationship

from src.database.base_class import Base

class Category(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(200))
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    # 관계 설정
    posts = relationship("Post", back_populates="category") 