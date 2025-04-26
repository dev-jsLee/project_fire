from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# SQLite 데이터베이스 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLITE_DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'sfire.db')}"
print(SQLITE_DATABASE_URL)
# 데이터베이스 엔진 생성
engine = create_engine(
    SQLITE_DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite를 위한 설정
    echo=True  # SQL 쿼리 로깅 활성화
)

# 세션 팩토리 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 모델 기본 클래스 생성
Base = declarative_base()

# 데이터베이스 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 