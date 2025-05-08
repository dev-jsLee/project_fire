-- 데이터베이스 권한 설정

-- 데이터베이스 생성
CREATE DATABASE IF NOT EXISTS sfire
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- 사용자 생성
CREATE USER IF NOT EXISTS 'bb_admin'@'localhost' IDENTIFIED BY 'sfire11!';
CREATE USER IF NOT EXISTS 'bb_user'@'localhost' IDENTIFIED BY 'sfire11!';
CREATE USER IF NOT EXISTS 'bb_guest'@'localhost' IDENTIFIED BY 'sfire11!';

-- 관리자 권한 (모든 권한)
GRANT ALL PRIVILEGES ON sfire.* TO 'bb_admin'@'localhost';
GRANT CREATE, ALTER, DROP, REFERENCES ON sfire.* TO 'bb_admin'@'localhost';
GRANT CREATE, DROP, RELOAD, SHUTDOWN, PROCESS, FILE, REFERENCES, INDEX, ALTER, 
    SHOW DATABASES, SUPER, CREATE TEMPORARY TABLES, LOCK TABLES, EXECUTE, 
    REPLICATION SLAVE, REPLICATION CLIENT, CREATE VIEW, SHOW VIEW, 
    CREATE ROUTINE, ALTER ROUTINE, CREATE USER, EVENT, TRIGGER ON *.* 
    TO 'bb_admin'@'localhost';

-- 일반 사용자 권한 (CRUD 작업)
GRANT SELECT, INSERT, UPDATE, DELETE ON sfire.posts TO 'bb_user'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON sfire.comments TO 'bb_user'@'localhost';
GRANT SELECT, INSERT, DELETE ON sfire.post_likes TO 'bb_user'@'localhost';
GRANT SELECT, INSERT, DELETE ON sfire.bookmarks TO 'bb_user'@'localhost';
GRANT SELECT, INSERT ON sfire.attachments TO 'bb_user'@'localhost';

-- 게스트 권한 (읽기 전용)
GRANT SELECT ON sfire.posts TO 'bb_guest'@'localhost';
GRANT SELECT ON sfire.comments TO 'bb_guest'@'localhost';
GRANT SELECT ON sfire.attachments TO 'bb_guest'@'localhost';

-- 특정 IP에서의 접근 허용 (예: 개발 서버)
CREATE USER IF NOT EXISTS 'bb_admin'@'192.168.1.%' IDENTIFIED BY 'sfire11!';
GRANT ALL PRIVILEGES ON sfire.* TO 'bb_admin'@'192.168.1.%';

-- 백업용 사용자
CREATE USER IF NOT EXISTS 'bb_backup'@'localhost' IDENTIFIED BY 'sfire11!';
GRANT SELECT, SHOW VIEW, LOCK TABLES, EVENT ON sfire.* TO 'bb_backup'@'localhost';

-- 권한 적용
FLUSH PRIVILEGES;

-- 권한 확인을 위한 뷰 생성
CREATE OR REPLACE VIEW sfire.user_privileges AS
SELECT 
    user,
    host,
    db,
    select_priv,
    insert_priv,
    update_priv,
    delete_priv,
    create_priv,
    drop_priv,
    grant_priv,
    references_priv,
    index_priv,
    alter_priv
FROM mysql.db
WHERE db = 'sfire';

-- 권한 그룹 생성 (역할)
CREATE ROLE IF NOT EXISTS 'bb_admin_role';
CREATE ROLE IF NOT EXISTS 'bb_user_role';
CREATE ROLE IF NOT EXISTS 'bb_guest_role';

-- 역할에 권한 부여
GRANT ALL PRIVILEGES ON sfire.* TO 'bb_admin_role';
GRANT SELECT, INSERT, UPDATE, DELETE ON sfire.* TO 'bb_user_role';
GRANT SELECT ON sfire.* TO 'bb_guest_role';

-- 사용자에게 역할 부여
GRANT 'bb_admin_role' TO 'bb_admin'@'localhost';
GRANT 'bb_user_role' TO 'bb_user'@'localhost';
GRANT 'bb_guest_role' TO 'bb_guest'@'localhost';

-- 역할 활성화
SET DEFAULT ROLE 'bb_admin_role' TO 'bb_admin'@'localhost';
SET DEFAULT ROLE 'bb_user_role' TO 'bb_user'@'localhost';
SET DEFAULT ROLE 'bb_guest_role' TO 'bb_guest'@'localhost'; 