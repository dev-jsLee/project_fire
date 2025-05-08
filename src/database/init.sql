-- 데이터베이스 생성
CREATE DATABASE IF NOT EXISTS sfire_uv;
USE sfire_uv;

-- 스키마 적용
SOURCE /docker-entrypoint-initdb.d/schema.sql;

-- 트리거 적용
SOURCE /docker-entrypoint-initdb.d/triggers.sql;

-- 권한 설정 적용
SOURCE /docker-entrypoint-initdb.d/privileges.sql;

-- 초기 데이터 추가
SOURCE /docker-entrypoint-initdb.d/seed.sql; 