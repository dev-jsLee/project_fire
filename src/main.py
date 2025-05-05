from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from starlette.middleware.sessions import SessionMiddleware
import os
from datetime import datetime

from src.core.config import settings
from src.api.endpoints import users, auth
from src.backend.database import SessionLocal
from src.backend.models import User, Post

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
    max_age=86400,  # 24시간
    same_site="lax",
    https_only=False
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
    return_url = request.query_params.get("return_url", "/")
    return templates.TemplateResponse(
        "member/login.html", 
        {
            "request": request,
            "return_url": return_url
        }
    )

@app.post("/login", response_class=HTMLResponse)
async def login(
    request: Request,
    user_id: str = Form(...),
    password: str = Form(...),
    return_url: str = Form("/"),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user or not pwd_context.verify(password, user.password):
        # 에러 메시지와 함께 로그인 페이지 렌더링
        return templates.TemplateResponse(
            "member/login.html",
            {
                "request": request,
                "error": "아이디 또는 비밀번호가 올바르지 않습니다.",
                "return_url": return_url
            }
        )
    # 로그인 성공 시 세션에 사용자 정보 저장
    request.session["user_id"] = user.user_id
    request.session["user_name"] = user.name
    return RedirectResponse(url=return_url, status_code=303)

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
async def post_list(request: Request, db: Session = Depends(get_db)):
    """게시글 목록 페이지"""
    # 세션에서 사용자 정보 가져오기
    user = None
    user_id = request.session.get("user_id")
    if user_id:
        user = db.query(User).filter(User.user_id == user_id).first()
    # 로그인하지 않은 경우 로그인 페이지로 리다이렉트
    if not user:
        return RedirectResponse(
            url=f"/login?return_url=/posts",
            status_code=303
        )
    # 게시글 목록 조회
    posts = db.query(Post).order_by(Post.created_at.desc()).all()
    now_year = datetime.now().year
    return templates.TemplateResponse(
        "post/post_list.html",
        {
            "request": request,
            "posts": posts,
            "user": user,
            "now_year": now_year
        }
    )

@app.get("/posts/new", response_class=HTMLResponse)
async def post_new(request: Request):
    """게시글 작성 페이지"""
    return templates.TemplateResponse("post/edit.html", {"request": request, "is_edit": False})

@app.get("/posts/{post_id}/edit", response_class=HTMLResponse)
async def post_edit(request: Request, post_id: int, db: Session = Depends(get_db)):
    """게시글 수정 페이지"""
    post = db.query(Post).filter(Post.post_id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    
    return templates.TemplateResponse(
        "post/edit.html",
        {
            "request": request,
            "post": post,
            "is_edit": True
        }
    )

@app.post("/posts", response_class=HTMLResponse)
async def post_create(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    category: str = Form("일반"),
    db: Session = Depends(get_db)
):
    """게시글 작성 처리"""
    # 세션에서 사용자 ID 가져오기
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")

    # 새 게시글 생성
    new_post = Post(
        user_id=user_id,
        title=title,
        content=content,
        category=category
    )
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    # 게시글 상세 페이지로 리다이렉트
    return RedirectResponse(url=f"/posts/{new_post.post_id}", status_code=303)

@app.post("/posts/{post_id}", response_class=HTMLResponse)
async def post_update(
    request: Request,
    post_id: int,
    title: str = Form(...),
    content: str = Form(...),
    category: str = Form("일반"),
    db: Session = Depends(get_db)
):
    """게시글 수정 처리"""
    # 세션에서 사용자 ID 가져오기
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")

    # 게시글 조회
    post = db.query(Post).filter(Post.post_id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    
    # 권한 확인
    if post.user_id != user_id:
        raise HTTPException(status_code=403, detail="수정 권한이 없습니다.")

    # 게시글 수정
    post.title = title
    post.content = content
    post.category = category
    post.updated_at = datetime.now()
    
    db.commit()
    db.refresh(post)

    # 게시글 상세 페이지로 리다이렉트
    return RedirectResponse(url=f"/posts/{post_id}", status_code=303)

@app.get("/posts/{post_id}", response_class=HTMLResponse)
async def post_detail(request: Request, post_id: int, db: Session = Depends(get_db)):
    """게시글 상세 페이지"""
    post = db.query(Post).filter(Post.post_id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    
    # 조회수 증가
    post.view_count += 1
    db.commit()
    
    return templates.TemplateResponse(
        "post/detail.html",
        {
            "request": request,
            "post": post
        }
    )

@app.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    """로그아웃 처리"""
    # 세션에서 사용자 정보 삭제
    request.session.clear()
    
    # 메인 페이지로 리다이렉트
    return RedirectResponse(url="/", status_code=303)

@app.get("/mypage", response_class=HTMLResponse)
async def mypage(request: Request, db: Session = Depends(get_db)):
    """마이페이지"""
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login?return_url=/mypage", status_code=303)
    
    # 사용자 정보 조회
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    
    # 사용자가 작성한 게시글 목록 조회
    posts = db.query(Post).filter(Post.user_id == user_id).order_by(Post.created_at.desc()).all()
    
    return templates.TemplateResponse(
        "member/mypage.html",
        {
            "request": request,
            "user": user,
            "posts": posts,
            "current_year": datetime.now().year
        }
    )

@app.get("/posts/{post_id}/delete", response_class=HTMLResponse)
async def post_delete(request: Request, post_id: int, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login?return_url=/posts", status_code=303)
    post = db.query(Post).filter(Post.post_id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    # 작성자 또는 admin만 삭제 가능
    if post.user_id != user_id and user_id != "admin":
        raise HTTPException(status_code=403, detail="삭제 권한이 없습니다.")
    db.delete(post)
    db.commit()
    return RedirectResponse(url="/posts", status_code=303) 