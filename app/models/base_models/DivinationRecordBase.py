

from sqlmodel import Field
from app.models.base_models.Base import TableBase


class DivinationRecordBase(TableBase):
    # 起卦的标题
    title: str = Field(
        nullable=False,
        unique=False,
        index=True,
        description="起卦的标题"
    )
    # 起卦的用户问题
    question: str = Field(
        nullable=False,
        description="起卦的用户问题"
    )
    # 起卦的卦象
    current_gua: str = Field(
        nullable=False,
        description="当前卦象"
    )
    # 变卦的卦象
    change_gua: str = Field(
        nullable=False,
        description="变卦的卦象"
    )
    # 卦象的解释
    ai_answer: str = Field(
        nullable=False,
        description="卦象的解释"
    )
