# from datetime import timedelta
# import time
# from typing import Annotated
# from app.api import crud
# from app.core import login_secure
# from app.models.BaseModels.Token import Token
# from fastapi import APIRouter, Body, Depends, HTTPException, Request
# from fastapi.security import OAuth2PasswordRequestForm
# from app.api.depends import SessionDep, get_client_ip
# from app.core.config import settings
# from app.core.security import create_access_token
# from app.models.PublicModels.In import PhoneNumberIn
# from app.models.PublicModels.Out import ErrorMod, RespMod
# from app.models.table import SMSCodeRecord
# router = APIRouter()


# @router.post("/request_sms_code", summary="发送登录验证码", response_model=RespMod)
# async def request_sms_code(
#     session: SessionDep,
#     phone_number: PhoneNumberIn = Body(),
#     client_ip: str = Depends(get_client_ip)
# ):
#     """
#     发送短信验证码给手机号注册的用户
#     验证码60秒内只能请求一次，请勿重复请求。
#     """
#     phone_number = phone_number.phone_number
#     # ip安全过滤，同ip60秒内只能发送一次验证码
#     login_secure.sms_code_ip_secure(session, client_ip)
#     sms_code_record_phone = session.get_one(
#         SMSCodeRecord, phone_number=phone_number)
#     if sms_code_record_phone is None:
#         # 手机号下发送记录不存在，发送验证码
#         await send_sms_code_to_phone_number(session=session, phone_number=phone_number, client_ip=client_ip)
#         return RespMod(message="验证码发送成功。")
#     else:
#         # 存在不同IP地址下，同一个手机号的发送记录
#         # 检测该记录是否已过期？
#         if sms_code_record_phone.is_expired():
#             # 手机记录已过期，删除手机记录，重新发送验证码
#             crud.delete_sms_code_record(
#                 session=session,
#                 sms_code_record=sms_code_record_phone)
#             await send_sms_code_to_phone_number(session=session, phone_number=phone_number, client_ip=client_ip)
#             return RespMod(message="验证码发送成功。")
#         else:
#             sec = sms_code_record_phone.sec_to_open()
#             raise ErrorMod(message=f"调用过于频繁，请{sec}秒后再试。")


# # 调用阿里云短信服务发送短信，并且，记录发送记录
# async def send_sms_code_to_phone_number(*, session=SessionDep, phone_number: str, client_ip: str):
#     # 如果不是生产服，或者是苹果测试人员，直接发送9999
#     if settings.ENVIRONMENT != "production" or phone_number == "13999999999":
#         verification_code = 9999
#     else:
#         verification_code = generate_random_sms_code(length=4)
#         await alibaba.send_sms_code_async(code=verification_code, phone_number=phone_number)
#     # 阿里巴巴短信验证码发送
#     current_time = int(time.time() * 1000)
#     record_create = SMSCodeRecordBase(
#         phone_number=phone_number,
#         client_ip=client_ip,
#         sms_code=verification_code,
#         # 60 秒后过期
#         expire_time=str(current_time + int(60 * 1000)),
#         create_time=str(current_time)
#     )
#     crud.create_sms_code_record(session=session, sms_code_record=record_create)


# @router.post("/signup_and_login_with_mobile_phone_and_sms_code", summary="验证码注册&自动登录用户", response_model=RespMod)
# def phone_login(request: Request, session: SessionDep, phone_number: str = Body(), sms_code: int = Body()):
#     """
#     验证短信验证码并注册用户
#     """
#     channel = request.headers.get("channel") or "unknown"

#     # 先执行登录安全检查
#     secure.login_secure(session=session, phone_number=phone_number)

#     # 获取验证码记录
#     sms_code_record = crud.get_sms_code_record_by_phone(
#         session=session, phone_number=phone_number)
#     if sms_code_record is None:
#         raise ErrorMod(message=f"验证码不存在。")
#     elif sms_code_record.sms_code == sms_code:
#         if not sms_code_record.is_expired():
#             return handle_valid_sms_code(session, phone_number, channel, sms_code_record)
#         else:
#             crud.delete_sms_code_record(
#                 session=session, sms_code_record=sms_code_record)
#             raise ErrorMod(message=f"验证码超时。")
#     else:
#         raise ErrorMod(message=f"无效的验证码。")


# def handle_valid_sms_code(session, phone_number, channel, sms_code_record):
#     session.delete(sms_code_record)
#     delete_stmt = delete(LoginRequestRecord).where(
#         LoginRequestRecord.phone_number == phone_number)
#     session.exec(delete_stmt)
#     session.commit()
#     user = crud.get_user_by_phone(session=session, phone_number=phone_number)
#     # 用户不存在，创建用户，并登录
#     if user is None:
#         new_user = crud.create_new_user(session, phone_number, channel)
#         token = make_token_for_user_to_login(user_id=new_user.id)
#         tokeninfo = Token(access_token=token)
#         LogSNAG.get_instance().log_user_login(user=new_user)
#         return RespMod(message="注册并登录成功。", data=tokeninfo.model_dump())
#     # 用户存在，登录
#     else:
#         token = make_token_for_user_to_login(user_id=user.id)
#         tokeninfo = Token(access_token=token)
#         return RespMod(message="自动登录成功。", data=tokeninfo.model_dump())


# # 根据user_id生成访问令牌
# def make_token_for_user_to_login(user_id: int):
#     # 生成访问令牌的过期时间
#     access_token_expires = timedelta(
#         minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     # 创建访问令牌并返回
#     access_token = security.create_access_token(
#         user_id, expires_delta=access_token_expires)
#     return access_token


# @router.post("/access-token", summary="⚠️非前端接口/数据库登录")
# def login(
#     session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
# ) -> Token:
#     """
#     OAuth2 兼容的令牌登录，获取用于未来请求的访问令牌
#     """
#     # 通过提供的表单数据验证用户身份
#     user = crud.authenticate(
#         session=session, phone_number=form_data.username, password=form_data.password
#     )
#     if not user:
#         # 如果用户不存在或密码错误，返回错误响应
#         raise HTTPException(
#             status_code=400, detail="手机号或密码错误")
#     elif not user.is_active:
#         # 如果用户处于非活跃状态，返回错误响应
#         raise HTTPException(status_code=400, detail="非活跃用户")
#     # 生成访问令牌的过期时间
#     access_token_expires = timedelta(
#         minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     # 创建访问令牌并返回.
#     return Token(
#         access_token=create_access_token(
#             user.id, expires_delta=access_token_expires
#         )
#     )
