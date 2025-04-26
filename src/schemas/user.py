from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """사용자 기본 정보 스키마"""
    email: EmailStr
    name: str = Field(..., min_length=2, max_length=50)

class UserCreate(UserBase):
    """사용자 등록 스키마"""
    user_id: str = Field(..., min_length=4, max_length=50)
    password: str = Field(..., min_length=6, max_length=50)

class User(UserBase):
    """사용자 정보 응답 스키마"""
    user_id: str
    # profile_image: Optional[str] = None
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
    last_login_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TokenData(BaseModel):
    """JWT 토큰 데이터 스키마"""
    user_id: str 