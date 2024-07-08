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
from app.models.BaseModels.Token import TokenPayload
from app.models.table import User

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)
TokenDep = Annotated[str, Depends(reusable_oauth2)]

# 在文件顶部，与您现有的代码一起放置


@contextmanager
def get_temp_db() -> Generator[Session, None, None]:
    """
    临时获取数据库会话的上下文管理器。
    使用 'with' 语句来自动管理会话的生命周期。
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
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]


def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError, ValueError):
        raise HTTPException(
            status_code=400, detail="请重新登录。")

    # 从会话中获取用户
    user = session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=400, detail="用户不存在。")
    if not user.is_active:
        raise HTTPException(status_code=401, detail="你已被封禁。")

    return user


# 当前用户
CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUser) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="你没有足够的权限。"
        )
    return current_user


# 当前超级管理员
CurrentSuperUser = Annotated[User, Depends(get_current_active_superuser)]


# ip地址获取
def get_client_ip(request: Request):
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[-1].strip()
    return request.client.host
