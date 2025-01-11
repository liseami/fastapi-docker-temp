
# 包含访问令牌的 JSON 负载

from .Base import TableBase
from sqlmodel import SQLModel


class Token(TableBase):
    access_token: str
    token_type: str = "bearer"

# JWT 令牌的内容


class TokenPayload(SQLModel):
    sub: str | None = None
