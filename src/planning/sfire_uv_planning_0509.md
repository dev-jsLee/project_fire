# FastAPI, Docker Compose, uv 도입 방안 (2025-05-09, 최신 반영)

## 1. FastAPI 도입 방안
- **현황**: FastAPI 기반으로 프로젝트가 구성되어 있음(`src/backend/app.py` 등).
- **구조 개선**:
    - 라우터 분리 및 모듈화 강화 (api, backend 등 디렉토리 활용)
    - Pydantic 기반 스키마 관리(schemas 디렉토리)
    - 비동기 처리 및 의존성 주입(Depends 등) 적극 활용
    - OpenAPI/Swagger 문서 자동화 및 커스터마이징
    - 테스트 코드(pytest, httpx 등) 작성 및 자동화
    - FastAPI 앱 진입점 파일명을 `main.py`에서 `app.py`로 변경하여 네이밍 충돌 방지

## 2. Docker Compose 도입 방안
- **목표**: 개발/운영 환경에서 서비스, DB, 기타 의존성(예: Redis 등)을 컨테이너로 통합 관리
- **구성 예시**:
    - `app`: FastAPI 서버 (uvicorn, Python 3.11, uv, src/backend/app.py)
    - `db`: MySQL 8.0 (DB명: sfire, 기본 비밀번호: 1234, 환경변수로 관리)
- **환경변수 관리**:
    - `.env` 파일을 통해 DB 비밀번호 등 민감 정보 관리
    - docker-compose.yml에서 `${변수명}` 형태로 참조
- **실행 예시**:
    ```yaml
    version: '3.8'
    services:
      app:
        build: .
        command: uvicorn src.backend.app:app --host 0.0.0.0 --port 8000
        ports:
          - "8000:8000"
        volumes:
          - .:/app
        depends_on:
          - db
        environment:
          DB_HOST: db
          DB_PORT: 3306
          DB_USER: ${MYSQL_USER}
          DB_PASSWORD: ${MYSQL_PASSWORD}
          DB_NAME: ${MYSQL_DATABASE}
      db:
        image: mysql:8.0
        restart: always
        environment:
          MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
          MYSQL_DATABASE: ${MYSQL_DATABASE}
          MYSQL_USER: ${MYSQL_USER}
          MYSQL_PASSWORD: ${MYSQL_PASSWORD}
        ports:
          - "3306:3306"
        volumes:
          - db_data:/var/lib/mysql
        command: --default-authentication-plugin=mysql_native_password
    volumes:
      db_data:
    ```
- **.env 예시**:
    ```env
    MYSQL_ROOT_PASSWORD=1234
    MYSQL_DATABASE=sfire
    MYSQL_USER=user
    MYSQL_PASSWORD=1234
    ```
- **장점**:
    - 환경 일관성 확보
    - 민감 정보 노출 최소화
    - 서비스 확장 및 관리 편리

## 3. uv 도입 방안
- **목표**: 패키지 설치 및 가상환경 관리 속도 개선, reproducibility 강화
- **적용 방법**:
    - 기존 pip 대신 uv 사용 (`uv pip install ...`, `uv venv ...` 등)
    - Dockerfile 내 패키지 설치 단계에서 uv 활용
    - pyproject.toml, uv.lock 파일로 의존성 관리
- **예시**:
    ```dockerfile
    FROM ubuntu:20.04
    # ... (python 설치 등)
    RUN pip install uv
    COPY pyproject.toml uv.lock ./
    RUN uv pip install -r requirements.txt
    # 또는
    RUN uv pip install --system --no-deps .
    ```
- **장점**:
    - pip 대비 빠른 설치 속도
    - 의존성 충돌 최소화
    - CI/CD 환경에서 빌드 시간 단축

## 4. 통합 적용 시나리오
- 개발자는 uv로 가상환경 및 패키지 관리
- Dockerfile/Docker Compose로 환경 일관성 유지
- FastAPI 구조화 및 모듈화로 유지보수성 강화
- CI/CD 파이프라인에 uv, Docker Compose 연동
- DB 환경변수 및 민감 정보는 .env 파일로 관리
- FastAPI 앱 진입점은 `src/backend/app.py`로 통일

---

*작성일: 2024-05-09, 최근 수정 반영* 