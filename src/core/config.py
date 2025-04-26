from pydantic_settings import BaseSettings
from typing import Optional
import secrets
import os

class Settings(BaseSettings):
    # 기본 설정
    PROJECT_NAME: str = "게시판 시스템"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # 서버 설정
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # CORS 설정
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8000"]
    # 데이터베이스 설정
    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
    DATABASE_URL: str = f"sqlite:///{os.path.join(BASE_DIR, 'sfire.db')}"
    
    # JWT 토큰 설정
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # 비밀번호 해싱 설정
    PWD_HASH_ROUNDS: int = 12
    
    class Config:
        case_sensitive = True
        env_file = ".env"

# 전역 설정 객체 생성
settings = Settings() 