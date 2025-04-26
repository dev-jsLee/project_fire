from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext

from src.api.dependencies import get_db, get_current_user, get_current_active_user
from src.backend.models import User
from src.schemas.user import UserCreate, User as UserSchema

router = APIRouter(prefix="/users", tags=["users"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    새로운 사용자를 등록합니다.
    """
    # 사용자 ID 중복 확인
    db_user = db.query(User).filter(User.user_id == user.user_id).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 사용 중인 사용자 ID입니다."
        )
    
    # 이메일 중복 확인
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 사용 중인 이메일입니다."
        )
    
    # 새 사용자 생성 (비밀번호는 평문으로 저장 - 보안 기능은 나중에 구현)
    db_user = User(
        user_id=user.user_id,
        email=user.email,
        password_hash=user.password,  # 나중에 해싱 처리
        nickname=user.nickname
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.get("/me", response_model=UserSchema)
def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """
    현재 로그인한 사용자의 정보를 조회합니다.
    """
    return current_user 

@router.post("/login", response_model=UserSchema)
def login_user(user_id: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    """
    사용자를 로그인합니다.
    """
    # 사용자 정보 조회
    user = db.query(User).filter(User.user_id == user_id).first()
    
    if not user or not pwd_context.verify(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid credentials"
        )

    return user  # 로그인 성공 시 사용자 정보를 반환

