from fastapi import APIRouter
from app.api.routes import divination, login, user
api_router = APIRouter()

api_router.include_router(user.router, prefix="/user", tags=["用户"])
api_router.include_router(login.router, prefix="/login", tags=["登录"])
api_router.include_router(divination.router, prefix="/divination", tags=["占卜"])
