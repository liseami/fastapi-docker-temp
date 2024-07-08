
# 包含访问令牌的 JSON 负载


from sqlmodel import SQLModel


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"

# JWT 令牌的内容


class TokenPayload(SQLModel):
    sub: int | None = None
