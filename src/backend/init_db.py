from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
if __name__ == "__main__":
    from database import engine, Base
else:
    from .database import engine, Base


# SQLite 데이터베이스 파일 경로
# DATABASE_URL = "sqlite:///./sql_app.db"

# 데이터베이스 엔진 생성
# engine = create_engine(
#     DATABASE_URL, connect_args={"check_same_thread": False}
# )

# 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    # 데이터베이스 초기화 SQL 문들을 리스트로 정의
    init_sql_statements = [
        # 사용자 테이블
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id VARCHAR(50) PRIMARY KEY,
            email VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            name VARCHAR(50) NOT NULL,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login_at TIMESTAMP
        )
        """,
        
        # 사용자 테이블 인덱스
        "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)",
        "CREATE INDEX IF NOT EXISTS idx_users_name ON users(name)",

        # 게시글 테이블
        """
        CREATE TABLE IF NOT EXISTS posts (
            post_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id VARCHAR(50) NOT NULL,
            title VARCHAR(200) NOT NULL,
            content TEXT NOT NULL,
            category VARCHAR(50) DEFAULT '일반',
            view_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        )
        """,
        
        # 댓글 테이블
        """
        CREATE TABLE IF NOT EXISTS comments (
            comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            user_id VARCHAR(50) NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES posts(post_id) ON DELETE CASCADE
        )
        """,
        
        # 파일 첨부 테이블
        """
        CREATE TABLE IF NOT EXISTS attachments (
            attachment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            file_name VARCHAR(255) NOT NULL,
            file_path VARCHAR(500) NOT NULL,
            file_size INTEGER NOT NULL,
            mime_type VARCHAR(100) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES posts(post_id) ON DELETE CASCADE
        )
        """,
        
        # 게시글 좋아요 테이블
        """
        CREATE TABLE IF NOT EXISTS post_likes (
            post_id INTEGER NOT NULL,
            user_id VARCHAR(50) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, post_id),
            FOREIGN KEY (post_id) REFERENCES posts(post_id) ON DELETE CASCADE
        )
        """,
        
        # 게시글 북마크 테이블
        """
        CREATE TABLE IF NOT EXISTS bookmarks (
            user_id VARCHAR(50) NOT NULL,
            post_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, post_id),
            FOREIGN KEY (post_id) REFERENCES posts(post_id) ON DELETE CASCADE
        )
        """,
        
        # 인덱스 생성
        "CREATE INDEX IF NOT EXISTS idx_posts_created_at ON posts(created_at)",
        "CREATE INDEX IF NOT EXISTS idx_posts_user_id ON posts(user_id)",
        "CREATE INDEX IF NOT EXISTS idx_posts_category ON posts(category)",
        "CREATE INDEX IF NOT EXISTS idx_comments_post_id ON comments(post_id)",
        "CREATE INDEX IF NOT EXISTS idx_attachments_post_id ON attachments(post_id)",
        "CREATE INDEX IF NOT EXISTS idx_post_likes_post_id ON post_likes(post_id)",
        "CREATE INDEX IF NOT EXISTS idx_bookmarks_post_id ON bookmarks(post_id)"
    ]

    # 각 SQL 문을 개별적으로 실행
    with engine.connect() as conn:
        for sql in init_sql_statements:
            conn.execute(text(sql))
        conn.commit()

if __name__ == "__main__":
    print("데이터베이스 초기화를 시작합니다...")
    init_db()
    print("데이터베이스 초기화가 완료되었습니다.") 