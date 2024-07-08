from fastapi import APIRouter
from sqlmodel import select
from app.api.depends import CurrentUser, SessionDep
from app.models.table import User


router = APIRouter()


@router.get("/ai", summary="第一个接口",
            description="第一个接口的说明")
def hello_world():
    """
    接口的说明
    """
    return {"message": "Hello 赵纯想"}


@router.get("/user", summary="获取当前用户和数据库连接",
            description="fastapi依赖示例")
def hello_world(user: CurrentUser, session: SessionDep):
    """
    接口的说明
    """
    stmt = select(User).where(User.id == user.id)
    db_user = session.exec(stmt).first()
    return {"message": db_user}
