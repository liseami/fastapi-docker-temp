from datetime import datetime, timedelta
from typing import Any
from jose import jwt
from passlib.context import CryptContext
from sqlmodel import Session, select
from app.core.config import settings
from app.models.table import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


def create_access_token(subject: str | Any, expires_delta: timedelta) -> str:
    """创建JWT访问令牌。

    Args:
        subject: 令牌主题,通常是用户ID
        expires_delta: 令牌过期时间增量

    Returns:
        生成的JWT令牌字符串
    """
    expire = datetime.now() + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证明文密码是否与哈希密码匹配。

    Args:
        plain_password: 用户输入的明文密码
        hashed_password: 数据库中存储的哈希密码

    Returns:
        密码是否匹配
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """生成密码的哈希值。

    Args:
        password: 需要哈希的明文密码

    Returns:
        密码的哈希字符串
    """
    return pwd_context.hash(password)


def authenticate(*, session: Session, phone_number: str, password: str) -> User | None:
    """验证用户凭据。

    Args:
        session: 数据库会话
        phone_number: 用户手机号
        password: 用户密码

    Returns:
        如果验证成功返回用户对象,否则返回None
    """
    user = session.exec(
        select(User)
        .where(User.phone_number == phone_number, User.is_deleted == False)
    ).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def make_token_for_user_to_login(user_id: str):
    """为用户生成访问令牌。

    Args:
        user_id: 用户ID(UUID格式)

    Returns:
        JWT访问令牌字符串
    """
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        user_id, expires_delta=access_token_expires)
    return access_token
