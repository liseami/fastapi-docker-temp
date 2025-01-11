from typing import List, Optional
from sqlmodel import Session, select
from app.models.table import Todo


class TodoCRUD:
    def __init__(self, session: Session):
        self.session = session

    def get_all_todos(self) -> List[Todo]:
        """获取所有未删除的todo"""
        stmt = select(Todo).where(Todo.is_deleted == False)
        return self.session.exec(stmt).all()

    def get_completed_todos(self) -> List[Todo]:
        """获取所有已完成的todo"""
        stmt = select(Todo).where(Todo.completed ==
                                  True, Todo.is_deleted == False)
        return self.session.exec(stmt).all()

    def get_uncompleted_todos(self) -> List[Todo]:
        """获取所有未完成的todo"""
        stmt = select(Todo).where(Todo.completed ==
                                  False, Todo.is_deleted == False)
        return self.session.exec(stmt).all()

    def create_todo(self, text: str, userid: str) -> Todo:
        """创建新的todo"""
        new_todo = Todo(text=text, userid=userid)
        self.session.add(new_todo)
        self.session.commit()
        self.session.refresh(new_todo)
        return new_todo

    def get_todo(self, todo_id: str) -> Optional[Todo]:
        """根据ID获取todo"""
        return self.session.get(Todo, todo_id)

    def complete_todo(self, todo_id: str) -> Optional[Todo]:
        """将todo标记为已完成"""
        todo = self.get_todo(todo_id)
        if not todo:
            return None
        todo.completed = True
        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)
        return todo

    def delete_todo(self, todo_id: str) -> bool:
        """软删除todo"""
        todo = self.get_todo(todo_id)
        if not todo:
            return False
        todo.is_deleted = True
        self.session.add(todo)
        self.session.commit()
        return True
