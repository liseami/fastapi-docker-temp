
from datetime import timedelta
from typing import Annotated
from sqlmodel import Session
from app.core import security
from app.models.base_models.Token import Token
from fastapi import APIRouter, Body, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from app.api.depends import SessionDep, get_client_ip
from app.core.config import settings
from app.core.security import create_access_token, make_token_for_user_to_login
from app.models.public_models.Out import ErrorMod, RespMod
from app.tool.random import RandomGenerator
from app.crud.SMSCodeRecordCRUD import SMSCodeRecordCRUD
from app.crud.UserCRUD import UserCRUD
router = APIRouter()


@router.post("/request_sms_code", summary="发送登录验证码", response_model=RespMod)
async def request_sms_code(
    session: SessionDep,
    phone_number: str = Body(embed=True),
    client_ip: str = Depends(get_client_ip)
):
    """发送短信验证码给指定手机号.

    Args:
        session: 数据库会话依赖
        phone_number: 目标手机号
        client_ip: 客户端IP地址

    Returns:
        RespMod: 包含成功消息的响应对象

    Note:
        验证码60秒内只能请求一次,请勿重复请求
    """
    await send_sms_code_to_phone_number(session=session, phone_number=phone_number)
    return RespMod(message="验证码发送成功。")


async def send_sms_code_to_phone_number(*, session=SessionDep, phone_number: str):
    """调用阿里云短信服务发送验证码并记录.

    Args:
        session: 数据库会话
        phone_number: 目标手机号
        client_ip: 客户端IP地址
    """
    if settings.ENVIRONMENT != "production":
        sms_code = 9999
    else:
        sms_code = RandomGenerator().generate_sms_code(length=4)
        # await alibaba.send_sms_code_async(code=verification_code, phone_number=phone_number)
    SMSCodeRecordCRUD(session).create_sms_code_record(
        phone_number=phone_number, sms_code=sms_code)


@router.post("/signup_and_login_with_mobile_phone_and_sms_code", summary="验证码注册&自动登录用户", response_model=RespMod)
def phone_login(request: Request, session: SessionDep, phone_number: str = Body(), sms_code: int = Body()):
    """使用短信验证码进行用户注册和登录.

    Args:
        request: HTTP请求对象
        session: 数据库会话依赖
        phone_number: 用户手机号
        sms_code: 短信验证码

    Returns:
        RespMod: 包含登录结果的响应对象

    Raises:
        ErrorMod: 当验证码不存在、无效或过期时抛出
    """
    sms_code_record = SMSCodeRecordCRUD(
        session).get_latest_sms_code_record(phone_number=phone_number)
    if sms_code_record is None:
        raise ErrorMod(message=f"验证码不存在。")
    elif sms_code_record.sms_code == sms_code:
        if not sms_code_record.is_expired():
            return handle_valid_sms_code(session, phone_number)
        else:
            SMSCodeRecordCRUD(session=session).delete_sms_code_record(
                record_id=sms_code_record.id)
            raise ErrorMod(message=f"验证码超时。")
    else:
        raise ErrorMod(message=f"无效的验证码。")


def handle_valid_sms_code(session: Session, phone_number):
    """处理有效的验证码登录请求.

    Args:
        session: 数据库会话
        phone_number: 用户手机号
        channel: 登录渠道
        sms_code_record: 验证码记录对象

    Returns:
        RespMod: 包含登录结果和token的响应对象
    """
    user = UserCRUD(session).get_user_by_phone(phone_number)
    if user is None:
        new_user = UserCRUD(session).create_user(
            phone_number
        )
        token = make_token_for_user_to_login(user_id=new_user.id)
        tokeninfo = Token(access_token=token)
        return RespMod(message="注册并登录成功。", data=tokeninfo.model_dump())
    else:
        token = make_token_for_user_to_login(user_id=user.id)
        tokeninfo = Token(access_token=token)
        return RespMod(message="自动登录成功。", data=tokeninfo.model_dump())


@router.post("/access-token", summary="⚠️非前端接口")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    OAuth2 兼容的令牌登录，获取用于未来请求的访问令牌
    """
    # 通过提供的表单数据验证用户身份
    pass
