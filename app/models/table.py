
from uuid import UUID
from sqlmodel import Field, Relationship, SQLModel
from app.models.base_models.SMSCodeRecordBase import SMSCodeRecordBase
from app.models.base_models.TodoBase import TodoBase
from app.models.base_models.UserBase import UserBase


# 用户表
class User(UserBase, table=True):
    todos: list["Todo"] = Relationship(back_populates="user")


# 短信发送记录
class SMSCodeRecord(SMSCodeRecordBase, table=True):
    pass


# Todo表
class Todo(TodoBase, table=True):
    user_id: UUID = Field(foreign_key="user.id", description="所属用户ID")
    user: User = Relationship(back_populates="todos")
