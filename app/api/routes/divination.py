

from fastapi import APIRouter


router = APIRouter()


@router.get("/", summary="起卦接口")
def divination():
    return "起卦接口"
