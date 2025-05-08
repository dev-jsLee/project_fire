#!/bin/bash

# uv로 FastAPI 서버 실행 (Python 3.11.8, src.backend.app:app)
uv --python 3.11.8 uvicorn src.backend.app:app --reload --host 0.0.0.0 --port 8000 