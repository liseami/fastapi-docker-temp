from datetime import datetime
from datetime import timezone
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field


class TableBase(SQLModel):
    """
    数据库表的基类,提供了所有表共用的基础字段和功能。

    该基类实现了以下核心功能:
    1. 自动生成UUID主键
    2. 自动记录创建和更新时间(UTC时间)
    3. 支持软删除
    4. 支持描述字段

    技术特性:
    - 使用SQLModel作为ORM基类,结合了SQLAlchemy的强大功能和Pydantic的类型检查
    - 所有时间字段使用UTC时间,避免时区问题
    - UUID主键提供了更好的分布式系统支持
    - 软删除支持数据追踪和恢复

    使用建议:
    - 所有业务表都应该继承这个基类
    - 需要时间相关查询时注意使用UTC时间
    - 删除操作优先使用软删除
    """

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
        description="表主键,使用UUID4自动生成"
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        description="记录创建时间(UTC),自动设置"
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
        description="记录最后更新时间(UTC),自动更新"
    )

    is_deleted: bool = Field(
        default=False,
        nullable=False,
        description="软删除标记,True表示已删除"
    )

    description: str | None = Field(
        default=None,
        description="记录的可选描述文本"
    )
