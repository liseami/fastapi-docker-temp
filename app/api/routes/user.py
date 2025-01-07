from fastapi import APIRouter, HTTPException
from sqlmodel import select
from app.models.public_models.Out import ErrorMod
from app.api.depends import CurrentUser, SessionDep
from app.models.public_models.Out import RespMod
from app.crud.UserCRUD import UserCRUD

router = APIRouter()


@router.get("/ping", summary="健康检查接口",
            description="用于检查API服务是否正常运行")
def health_check() -> dict:
    """执行简单的健康检查。

    返回一个包含状态信息的字典,用于确认API服务正常运行。

    Returns:
        dict: 包含状态信息的响应字典
            - status (str): 服务状态
            - message (str): 状态描述
    """
    return {
        "status": "healthy",
        "message": "API服务运行正常"
    }


@router.get("/profile", summary="获取用户详细信息",
            description="获取当前登录用户的完整个人信息")
def get_user_profile(user: CurrentUser, session: SessionDep):
    user = UserCRUD(session=session).get_user(user.id)
    if user:
        return RespMod(data=user.model_dump())
    else:
        raise ErrorMod(message="用户不存在")
