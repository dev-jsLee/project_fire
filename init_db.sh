#!/bin/bash

echo "==================================================="
echo "[경고] 데이터베이스 초기화를 시작합니다."
echo "이 작업은 모든 데이터를 삭제하고 초기 상태로 되돌립니다."
echo "==================================================="
echo

read -p "정말로 데이터베이스를 초기화하시겠습니까? (y/N): " confirm

if [[ ! $confirm =~ ^[Yy]$ ]]; then
    echo "초기화가 취소되었습니다."
    exit 1
fi

echo
echo "데이터베이스 초기화를 진행합니다..."

# 컨테이너가 실행 중인지 확인
if ! docker-compose ps | grep -q "db"; then
    echo "데이터베이스 컨테이너를 시작합니다..."
    docker-compose up -d db
    # MySQL이 완전히 시작될 때까지 대기
    sleep 10
fi

# 초기화 스크립트 실행
echo "데이터베이스 초기화를 진행합니다..."
docker-compose exec -T db mysql -uroot -prootpassword < src/database/init.sql

echo
echo "==================================================="
echo "데이터베이스 초기화가 완료되었습니다."
echo "===================================================" 