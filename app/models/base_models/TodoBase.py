

from sqlmodel import Field
from app.models.base_models.Base import TableBase

# SQLModel Field 函数的主要参数说明:

# 1. 基础参数
#   - default: 字段的默认值
#   - default_factory: 用于生成默认值的工厂函数
#   - description: 字段的描述文本
#   - title: 字段的标题

# 2. 验证参数
#   - gt/ge: 大于/大于等于(数值类型)
#   - lt/le: 小于/小于等于(数值类型)
#   - min_length/max_length: 最小/最大长度(字符串)
#   - regex: 正则表达式验证(字符串)
#   - unique_items: 列表元素是否必须唯一

# 3. 数据库相关参数
#   - primary_key: 是否为主键
#   - foreign_key: 外键关联
#   - unique: 是否唯一
#   - index: 是否创建索引
#   - nullable: 是否可为空

# 4. SQLAlchemy特定参数
#   - sa_type: 指定 SQLAlchemy 列类型
#   - sa_column_args: SQLAlchemy Column 构造函数参数
#   - sa_column_kwargs: SQLAlchemy Column 构造函数关键字参数

# 5. 其他参数
#   - alias: 字段别名
#   - allow_mutation: 是否允许修改
#   - schema_extra: 额外的schema信息


class TodoBase(TableBase):
    text: str = Field(
        nullable=False,
        unique=True,
        index=True,
        description="用户名,系统内唯一"
    )
    completed: bool = Field(
        default=False,
        description="是否完成"
    )
