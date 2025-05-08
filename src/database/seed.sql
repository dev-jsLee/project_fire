-- 기본 카테고리 추가
INSERT INTO categories (name, description) VALUES
('공지사항', '중요한 공지사항을 확인하세요'),
('일반', '일반적인 게시글'),
('일정', '일정 공유'),
-- ('정보', '유용한 정보를 공유해보세요'),
-- ('후기', '사용 후기를 공유해보세요'),
('질문', '질문과 답변');

-- admin 사용자 추가
INSERT INTO users (user_id, email, password, name, is_active)
VALUES (
    'admin',
    'admin@example.com',
    -- 비밀번호: 1324 (실제 프로덕션에서는 해시된 비밀번호를 사용해야 합니다)
    '1324',
    '관리자',
    TRUE
); 