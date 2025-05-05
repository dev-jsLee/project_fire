from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
import sys
import time
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

def drop_all_tables():
    """모든 테이블을 삭제합니다."""
    with engine.connect() as conn:
        # SQLite에서 테이블 목록 조회
        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        tables = [row[0] for row in result if row[0] != 'sqlite_sequence']
        
        # 각 테이블 삭제
        for table in tables:
            conn.execute(text(f"DROP TABLE IF EXISTS {table}"))
            print(f"테이블 삭제됨: {table}")
        
        conn.commit()

def init_db():
    """데이터베이스를 초기화합니다."""
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
            like_count INTEGER DEFAULT 0,
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
            parent_id INTEGER,
            content TEXT NOT NULL,
            like_count INTEGER DEFAULT 0,
            is_deleted BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES posts(post_id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
            FOREIGN KEY (parent_id) REFERENCES comments(comment_id) ON DELETE CASCADE
        )
        """,
        
        # 댓글 좋아요 테이블
        """
        CREATE TABLE IF NOT EXISTS comment_likes (
            comment_id INTEGER NOT NULL,
            user_id VARCHAR(50) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (comment_id, user_id),
            FOREIGN KEY (comment_id) REFERENCES comments(comment_id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        )
        """,
        
        # 댓글 알림 테이블
        """
        CREATE TABLE IF NOT EXISTS comment_notifications (
            notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
            comment_id INTEGER NOT NULL,
            post_id INTEGER NOT NULL,
            user_id VARCHAR(50) NOT NULL,
            is_read BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (comment_id) REFERENCES comments(comment_id) ON DELETE CASCADE,
            FOREIGN KEY (post_id) REFERENCES posts(post_id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
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
            FOREIGN KEY (post_id) REFERENCES posts(post_id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        )
        """,
        
        # 게시글 북마크 테이블
        """
        CREATE TABLE IF NOT EXISTS bookmarks (
            user_id VARCHAR(50) NOT NULL,
            post_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, post_id),
            FOREIGN KEY (post_id) REFERENCES posts(post_id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        )
        """,
        
        # 인덱스 생성
        "CREATE INDEX IF NOT EXISTS idx_posts_created_at ON posts(created_at)",
        "CREATE INDEX IF NOT EXISTS idx_posts_user_id ON posts(user_id)",
        "CREATE INDEX IF NOT EXISTS idx_posts_category ON posts(category)",
        "CREATE INDEX IF NOT EXISTS idx_comments_post_id ON comments(post_id)",
        "CREATE INDEX IF NOT EXISTS idx_comments_user_id ON comments(user_id)",
        "CREATE INDEX IF NOT EXISTS idx_comments_parent_id ON comments(parent_id)",
        "CREATE INDEX IF NOT EXISTS idx_comments_created_at ON comments(created_at)",
        "CREATE INDEX IF NOT EXISTS idx_attachments_post_id ON attachments(post_id)",
        "CREATE INDEX IF NOT EXISTS idx_post_likes_post_id ON post_likes(post_id)",
        "CREATE INDEX IF NOT EXISTS idx_bookmarks_post_id ON bookmarks(post_id)",
        "CREATE INDEX IF NOT EXISTS idx_comment_likes_comment_id ON comment_likes(comment_id)",
        "CREATE INDEX IF NOT EXISTS idx_comment_notifications_user_id ON comment_notifications(user_id)",
        "CREATE INDEX IF NOT EXISTS idx_comment_notifications_is_read ON comment_notifications(is_read)"
    ]

    # 각 SQL 문을 개별적으로 실행
    with engine.connect() as conn:
        for sql in init_sql_statements:
            conn.execute(text(sql))
        conn.commit()

if __name__ == "__main__":
    print("\n" + "="*80)
    print("경고: 데이터베이스 초기화를 시작합니다.")
    print("이 작업은 모든 기존 데이터를 삭제하고 새로운 스키마로 재생성합니다.")
    print("="*80 + "\n")
    
    # 사용자 확인
    input(f"\r계속하려면 Enter 입력(Ctrl+C로 취소)")
    
    try:
        print("기존 테이블 삭제 중...")
        drop_all_tables()
        print("\n새로운 테이블 생성 중...")
        init_db()
        print("\n데이터베이스 초기화가 완료되었습니다.")
    except KeyboardInterrupt:
        print("\n\n작업이 취소되었습니다.")
        sys.exit(1)
    except Exception as e:
        print(f"\n오류가 발생했습니다: {str(e)}")
        sys.exit(1) 