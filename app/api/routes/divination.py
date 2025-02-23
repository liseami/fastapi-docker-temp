

from fastapi import APIRouter, Body, Depends

from app.api.depends import CurrentUser, SessionDep
from app.crud.DivinationRecordCRUD import DivinationRecordCRUD
from app.models.public_models.Out import RespMod


router = APIRouter()


@router.get("/list", summary="起卦历史记录")
def divination(user: CurrentUser, session: SessionDep):
    records = DivinationRecordCRUD(session=session).get_all_records(user.id)
    return RespMod(message="获取成功", data=records)


@router.post("/delete", summary="删除起卦记录")
def delete_divination(user: CurrentUser,  session: SessionDep, record_id: str = Body(embed=True)):
    DivinationRecordCRUD(session=session).delete_record(record_id, user.id)
    return RespMod(message="删除成功。")
