

from fastapi import APIRouter, Body


router = APIRouter()


@router.get("/all", summary="查询数据库中所有的todo")
def get_all_todo():
    return ""


@router.post("/add", summary="添加todo")
def add_todo(text: str = Body(embed=True)):
    return ""
