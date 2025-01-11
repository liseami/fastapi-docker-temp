from fastapi import APIRouter, Body, HTTPException
from app.api.depends import SessionDep
from app.crud.TodoCRUD import TodoCRUD


router = APIRouter()


@router.get("/all", summary="查询数据库中所有的todo")
def get_all_todo(session: SessionDep):
    return TodoCRUD(session).get_all_todos()


@router.post("/add", summary="添加todo")
def add_todo(session: SessionDep, text: str = Body(embed=True)):
    TodoCRUD(session).create_todo(text, user_id="")
    return ""


@router.get("/completed", summary="查询已完成的todo")
def get_completed_todo(session: SessionDep):
    return TodoCRUD(session).get_completed_todos()


@router.get("/uncompleted", summary="查询未完成的todo")
def get_uncompleted_todo(session: SessionDep):
    return TodoCRUD(session).get_uncompleted_todos()


@router.put("/complete", summary="将todo标记为已完成")
def complete_todo(session: SessionDep, todo_id: str = Body(embed=True)):
    todo = TodoCRUD(session).complete_todo(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo不存在")
    return ""


@router.delete("/", summary="删除todo")
def delete_todo(session: SessionDep, todo_id: str = Body(embed=True)):
    if not TodoCRUD(session).delete_todo(todo_id):
        raise HTTPException(status_code=404, detail="Todo不存在")
    return ""
