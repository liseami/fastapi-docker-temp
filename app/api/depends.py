"""依赖注入模块。

本模块提供了FastAPI应用所需的各种依赖注入函数和工具。
包括数据库会话管理、用户认证、权限检查等功能。

主要组件:
    - 数据库会话管理: get_temp_db(), get_db()
    - 用户认证: get_current_user(), get_current_active_superuser() 
    - IP地址获取: get_client_ip()
"""

from collections.abc import Generator
from contextlib import contextmanager
from typing import Annotated
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlmodel import Session
from app.core import security
from app.core.config import settings
from app.core.db import engine
from app.models.base_models.Token import TokenPayload
from app.models.table import User

# OAuth2密码流认证方案
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)
TokenDep = Annotated[str, Depends(reusable_oauth2)]


@contextmanager
def get_temp_db() -> Generator[Session, None, None]:
    """创建一个临时数据库会话的上下文管理器。

    使用上下文管理器模式来管理数据库会话的生命周期,确保资源的正确释放。

    Yields:
        Session: SQLModel数据库会话对象

    Raises:
        Exception: 当数据库操作发生错误时抛出异常并回滚
    """
    session = Session(engine)
    try:
        yield session
        session.commit()  # 如果没有异常发生，提交更改
    except Exception:
        session.rollback()  # 发生异常时回滚
        raise
    finally:
        session.close()  # 无论如何都要关闭会话


def get_db() -> Generator[Session, None, None]:
    """创建数据库会话的依赖注入函数。

    为每个请求创建一个新的数据库会话。

    Yields:
        Session: SQLModel数据库会话对象
    """
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]


def get_current_user(session: SessionDep, token: TokenDep) -> User:
    """获取当前已认证用户。

    验证JWT令牌并返回对应的用户对象。

    Args:
        session: 数据库会话
        token: JWT认证令牌

    Returns:
        User: 当前认证用户对象

    Raises:
        HTTPException: 当令牌无效或用户不存在时抛出400错误
                      当用户被禁用时抛出401错误
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError, ValueError):
        raise HTTPException(
            status_code=400, detail="请重新登录。")
    # 从会话中获取用户
    userid = token_data.sub
    user = session.get(User, userid)
    if not user:
        raise HTTPException(status_code=400, detail="用户不存在。")
    if not user.is_active:
        raise HTTPException(status_code=401, detail="你已被封禁。")

    return user


# 当前用户依赖
CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUser) -> User:
    """验证当前用户是否为超级管理员。

    Args:
        current_user: 当前认证用户对象

    Returns:
        User: 当前超级管理员用户对象

    Raises:
        HTTPException: 当用户不是超级管理员时抛出400错误
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="你没有足够的权限。"
        )
    return current_user


# 当前超级管理员依赖
CurrentSuperUser = Annotated[User, Depends(get_current_active_superuser)]


def get_client_ip(request: Request):
    """获取客户端IP地址。

    首先尝试从X-Forwarded-For头部获取IP,如果不存在则使用直接客户端IP。

    Args:
        request: FastAPI请求对象

    Returns:
        str: 客户端IP地址
    """
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[-1].strip()
    return request.client.host
