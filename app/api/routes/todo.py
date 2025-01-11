from fastapi import APIRouter, Body, HTTPException
from app.api.depends import CurrentUser, SessionDep
from app.crud.TodoCRUD import TodoCRUD


router = APIRouter()


@router.get("/all", summary="查询当前用户所有的todo")
def get_all_todo(session: SessionDep, user: CurrentUser):
    return TodoCRUD(session).get_all_todos(user_id=str(user.id))


@router.post("/add", summary="添加todo")
def add_todo(session: SessionDep, user: CurrentUser, text: str = Body(embed=True)):
    TodoCRUD(session).create_todo(text, user_id=str(user.id))
    return ""


@router.get("/completed", summary="查询当前用户已完成的todo")
def get_completed_todo(session: SessionDep, user: CurrentUser):
    return TodoCRUD(session).get_completed_todos(user_id=str(user.id))


@router.get("/uncompleted", summary="查询当前用户未完成的todo")
def get_uncompleted_todo(session: SessionDep, user: CurrentUser):
    return TodoCRUD(session).get_uncompleted_todos(user_id=str(user.id))


@router.put("/complete", summary="将todo标记为已完成")
def complete_todo(session: SessionDep, user: CurrentUser, todo_id: str = Body(embed=True)):
    todo = TodoCRUD(session).complete_todo(todo_id, user_id=str(user.id))
    if not todo:
        raise HTTPException(status_code=404, detail="Todo不存在或无权限操作")
    return ""


@router.delete("/", summary="删除todo")
def delete_todo(session: SessionDep, user: CurrentUser, todo_id: str = Body(embed=True)):
    if not TodoCRUD(session).delete_todo(todo_id, user_id=str(user.id)):
        raise HTTPException(status_code=404, detail="Todo不存在或无权限操作")
    return ""
