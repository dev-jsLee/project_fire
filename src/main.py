from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from starlette.middleware.sessions import SessionMiddleware
import os

from src.core.config import settings
from src.api.endpoints import users, auth
from src.backend.database import SessionLocal
from src.backend.models import User

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 세션 미들웨어 설정
app.add_middleware(
    SessionMiddleware,
    secret_key=os.environ.get("SECRET_KEY", "your-secret-key-here"),
    session_cookie="session",
    max_age=1800  # 30분
)

# 정적 파일 설정
app.mount("/static", StaticFiles(directory="src/static", html=True), name="static")

# 템플릿 설정
templates = Jinja2Templates(directory="src/templates")

# API 라우터 등록
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(users.router, prefix=settings.API_V1_STR)

# 비밀번호 해싱을 위한 CryptContext 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 데이터베이스 세션을 생성하는 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: Session = Depends(get_db)):
    """루트 경로에서 index.html을 반환"""
    user = None
    user_id = request.session.get("user_id")
    if user_id:
        user = db.query(User).filter(User.user_id == user_id).first()
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request, 
            "user": user,
            "footer": "fragments/footer.html"  # 푸터 템플릿 경로 추가
        }
    )

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    """로그인 페이지"""
    return templates.TemplateResponse("member/login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
async def login(
    request: Request,
    user_id: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    # 사용자 정보 조회
    user = db.query(User).filter(User.user_id == user_id).first()
    
    if not user or not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # 로그인 성공 시 세션에 사용자 정보 저장
    request.session["user_id"] = user.user_id
    request.session["user_name"] = user.name

    return templates.TemplateResponse("index.html", {"request": request, "user": user})

@app.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    """회원가입 페이지"""
    return templates.TemplateResponse("member/register.html", {"request": request})

@app.post("/register", response_class=HTMLResponse)
async def register(
    request: Request,
    user_id: str = Form(...),
    password: str = Form(...),
    password_confirm: str = Form(...),
    email: str = Form(...),
    name: str = Form(...),
    db: Session = Depends(get_db)
):
    # 유효성 검사
    if password != password_confirm:
        return templates.TemplateResponse("member/register.html", {"request": request, "error": "비밀번호가 일치하지 않습니다."})

    # 비밀번호 해싱
    hashed_password = pwd_context.hash(password)

    # 사용자 정보 저장
    new_user = User(
        user_id=user_id,
        email=email,
        password=hashed_password,
        name=name
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return templates.TemplateResponse("member/login.html", {"request": request, "message": "회원가입이 완료되었습니다."})

@app.get("/posts", response_class=HTMLResponse)
async def post_list(request: Request):
    """게시글 목록 페이지"""
    return templates.TemplateResponse("post/list.html", {"request": request})

@app.get("/posts/new", response_class=HTMLResponse)
async def post_edit(request: Request):
    """게시글 작성 페이지"""
    return templates.TemplateResponse("post/edit.html", {"request": request}) 