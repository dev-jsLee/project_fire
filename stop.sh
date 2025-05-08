#!/bin/bash

# 실행 중인 uvicorn 프로세스 찾기 및 안전하게 종료
PIDS=$(pgrep -f "uvicorn src.backend.app:app")

if [ -z "$PIDS" ]; then
  echo "실행 중인 uvicorn 서버가 없습니다."
  exit 0
fi

for PID in $PIDS; do
  echo "uvicorn 프로세스 종료: $PID"
  kill -SIGTERM $PID
  # 종료 대기
  wait $PID 2>/dev/null
done

echo "서버가 안전하게 종료되었습니다." 