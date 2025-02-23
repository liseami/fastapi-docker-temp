from sqlmodel import Field, SQLModel
from .Base import TableBase
from pydantic import BaseModel


class UserBase(TableBase):
    """用户基础模型类

    定义了用户的核心属性和字段约束:
    - username: 用户名,唯一且可搜索
    - is_active: 账号状态标记
    - phone_number: 手机号,唯一且可选
    - hashed_password: 密码哈希值
    - is_superuser: 超级用户标记

    继承自TableBase获得:
    - UUID主键
    - 创建和更新时间
    - 软删除支持
    - 描述字段
    """
    username: str | None = Field(
        unique=True,
        index=True,
        description="用户名,系统内唯一"
    )
    is_active: bool = Field(
        default=True,
        description="账号是否激活"
    )
    phone_number: str | None = Field(
        unique=True,
        default=None,
        index=True,
        description="手机号,可选但必须唯一"
    )
    hashed_password: str | None = Field(
        default=None,
        description="密码哈希值,不存储原始密码"
    )
    is_superuser: bool = Field(
        default=False,
        description="是否为超级管理员"
    )
    shortid: str | None = Field(
        unique=True,
        index=True,
        default=None,
        description="用户短ID,系统内唯一"
    )


class UserCreate(UserBase):
    """用户创建模型

    扩展UserBase用于新用户注册:
    - 新增password字段接收原始密码
    - 在service层进行密码哈希化
    - 创建完成后密码会被转换为hashed_password存储
    """
    password: str


class UserUpdate(BaseModel):
    username: str | None = Field(None, description="用户名")
