FROM ubuntu:20.04

# 필수 패키지 설치 (curl 등)
RUN apt-get update && apt-get install -y curl ca-certificates && rm -rf /var/lib/apt/lists/*

# uv 설치
RUN curl -Ls https://astral.sh/uv/install.sh | sh

# uv로 Python 3.11.8 설치
RUN uv python install 3.11.8

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일만 먼저 복사 (빌드 캐시 활용)
COPY pyproject.toml uv.lock ./

# 패키지 설치
RUN uv pip install --python 3.11.8 .

# 소스 코드 전체 복사 (나중에)
COPY . .

# start.sh 실행 권한 부여
RUN chmod +x start.sh

# 서버 자동 실행 대신 start.sh로 실행하도록 변경
CMD ["/app/start.sh"] 