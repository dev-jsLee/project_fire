from fastapi import APIRouter

from src.api.endpoints import auth, users, posts, categories

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(posts.router, prefix="/posts", tags=["posts"])
api_router.include_router(categories.router, prefix="/api", tags=["categories"]) 