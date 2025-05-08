-- 게시글 삭제 전 트리거: 관련 데이터 정리
DELIMITER //
CREATE TRIGGER before_post_delete
BEFORE DELETE ON posts
FOR EACH ROW
BEGIN
    -- 게시글의 댓글 삭제
    DELETE FROM comments WHERE post_id = OLD.post_id;
    -- 게시글의 첨부파일 삭제
    DELETE FROM attachments WHERE post_id = OLD.post_id;
    -- 게시글의 좋아요 삭제
    DELETE FROM post_likes WHERE post_id = OLD.post_id;
    -- 게시글의 북마크 삭제
    DELETE FROM bookmarks WHERE post_id = OLD.post_id;
END //
DELIMITER ;

-- 댓글 삭제 전 트리거: 대댓글이 있는 경우 삭제 방지
DELIMITER //
CREATE TRIGGER before_comment_delete
BEFORE DELETE ON comments
FOR EACH ROW
BEGIN
    DECLARE child_count INT;
    
    -- 대댓글 개수 확인
    SELECT COUNT(*) INTO child_count
    FROM comments
    WHERE parent_id = OLD.comment_id;
    
    -- 대댓글이 있는 경우 삭제 방지
    IF child_count > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = '대댓글이 있는 댓글은 삭제할 수 없습니다.';
    END IF;
    
    -- 댓글의 좋아요 삭제
    DELETE FROM comment_likes WHERE comment_id = OLD.comment_id;
    -- 댓글 관련 알림 삭제
    DELETE FROM comment_notifications WHERE comment_id = OLD.comment_id;
END //
DELIMITER ;

-- 댓글 작성 후 트리거: 알림 생성
DELIMITER //
CREATE TRIGGER after_comment_insert
AFTER INSERT ON comments
FOR EACH ROW
BEGIN
    DECLARE post_author_id VARCHAR(50);
    
    -- 게시글 작성자 ID 가져오기
    SELECT user_id INTO post_author_id
    FROM posts
    WHERE post_id = NEW.post_id;
    
    -- 게시글 작성자에게 알림 생성 (자신의 게시글에 댓글을 달 경우 제외)
    IF post_author_id != NEW.user_id THEN
        INSERT INTO comment_notifications (comment_id, post_id, user_id)
        VALUES (NEW.comment_id, NEW.post_id, post_author_id);
    END IF;
    
    -- 부모 댓글이 있는 경우, 부모 댓글 작성자에게도 알림 생성
    IF NEW.parent_id IS NOT NULL THEN
        DECLARE parent_author_id VARCHAR(50);
        
        SELECT user_id INTO parent_author_id
        FROM comments
        WHERE comment_id = NEW.parent_id;
        
        -- 부모 댓글 작성자에게 알림 생성 (자신의 댓글에 답글을 달 경우 제외)
        IF parent_author_id != NEW.user_id THEN
            INSERT INTO comment_notifications (comment_id, post_id, user_id)
            VALUES (NEW.comment_id, NEW.post_id, parent_author_id);
        END IF;
    END IF;
END //
DELIMITER ; 