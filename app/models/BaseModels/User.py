

from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    username: str | None = Field(unique=True, index=True)
    is_active: bool = Field(default=True)
    phone_number: str | None = Field(unique=True, default=None, index=True)
    hashed_password: str | None = Field(default=None)
    is_superuser: bool = Field(default=False)


# 创建新用户
class UserCreate(UserBase):
    password: str
