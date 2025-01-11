from typing import List, Optional
from sqlmodel import Session, select
from app.models.table import Todo


class TodoCRUD:
    def __init__(self, session: Session):
        self.session = session

    def get_all_todos(self, user_id: str) -> List[Todo]:
        """获取指定用户所有未删除的todo"""
        stmt = select(Todo).where(Todo.user_id ==
                                  user_id, Todo.is_deleted == False)
        return self.session.exec(stmt).all()

    def get_completed_todos(self, user_id: str) -> List[Todo]:
        """获取指定用户所有已完成的todo"""
        stmt = select(Todo).where(
            Todo.user_id == user_id,
            Todo.completed == True,
            Todo.is_deleted == False
        )
        return self.session.exec(stmt).all()

    def get_uncompleted_todos(self, user_id: str) -> List[Todo]:
        """获取指定用户所有未完成的todo"""
        stmt = select(Todo).where(
            Todo.user_id == user_id,
            Todo.completed == False,
            Todo.is_deleted == False
        )
        return self.session.exec(stmt).all()

    def create_todo(self, text: str, user_id: str) -> Todo:
        """创建新的todo"""
        new_todo = Todo(text=text, user_id=user_id)
        self.session.add(new_todo)
        self.session.commit()
        self.session.refresh(new_todo)
        return new_todo

    def get_todo(self, todo_id: str, user_id: str) -> Optional[Todo]:
        """根据ID获取todo，并验证所有权"""
        todo = self.session.get(Todo, todo_id)
        if todo and str(todo.user_id) == user_id:
            return todo
        return None

    def complete_todo(self, todo_id: str, user_id: str) -> Optional[Todo]:
        """将todo标记为已完成，需验证所有权"""
        todo = self.get_todo(todo_id, user_id)
        if not todo:
            return None
        todo.completed = True
        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)
        return todo

    def delete_todo(self, todo_id: str, user_id: str) -> bool:
        """软删除todo，需验证所有权"""
        todo = self.get_todo(todo_id, user_id)
        if not todo:
            return False
        todo.is_deleted = True
        self.session.add(todo)
        self.session.commit()
        return True
