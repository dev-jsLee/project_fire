@echo off
echo Starting server...

:: 가상환경 활성화
call .venv\Scripts\activate

:: 서버 실행
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

pause