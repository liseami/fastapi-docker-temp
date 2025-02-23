
from uuid import UUID
from sqlmodel import Field, Relationship, SQLModel
from app.models.base_models.SMSCodeRecordBase import SMSCodeRecordBase
from app.models.base_models.TodoBase import TodoBase
from app.models.base_models.UserBase import UserBase
from app.models.base_models.DivinationRecordBase import DivinationRecordBase

# 用户表


class User(UserBase, table=True):
    todos: list["Todo"] = Relationship(back_populates="user")
    divination_records: list["DivinationRecord"] = Relationship(
        back_populates="user")

# 短信发送记录


class SMSCodeRecord(SMSCodeRecordBase, table=True):
    pass


# Todo表
class Todo(TodoBase, table=True):
    user_id: UUID = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="todos")


# 起卦记录
class DivinationRecord(DivinationRecordBase, table=True):
    user_id: UUID = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="divination_records")
