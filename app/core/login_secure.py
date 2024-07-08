# from sqlmodel import Session


# def login_secure(session: Session, phone_number: str):
#     login_recored = LoginRequestRecord(create_time=int(
#         time.time() * 1000).__str__(), phone_number=phone_number)
#     session.add(login_recored)
#     session.commit()
#     # 先写入登录记录，然后查询数据库中该手机号对应的登录请求记录
#     one_minute_ago = datetime.now() - timedelta(minutes=1)
#     one_minute_ago_timestamp = int(
#         one_minute_ago.timestamp() * 1000)  # 转换为毫秒时间戳
#     login_recored_stmt = select(LoginRequestRecord).where(
#         LoginRequestRecord.phone_number == phone_number
#     ).where(
#         LoginRequestRecord.create_time >= one_minute_ago_timestamp
#     )
#     phone_login_request_records = session.exec(login_recored_stmt).all()
#     # 如果过去一分钟内超过5条记录，直接报错
#     if len(phone_login_request_records) >= 5:
#         raise ErrorMod(message=f"尝试登录过于频繁，请稍后再试。")


# def sms_code_ip_secure(session: Session, client_ip: str):
#     # ========================================
#     # 先查询数据库中该ip地址对应的验证码记录
#     # ========================================
#     sms_code_records_in_ip = crud.get_sms_code_records_by_ip(
#         session=session, client_ip=client_ip)
#     if sms_code_records_in_ip:
#         for record in sms_code_records_in_ip:
#             # 删除所有已经过期的
#             if record.is_expired():
#                 crud.delete_sms_code_record(
#                     session=session,
#                     sms_code_record=record)
#             # 同IP下，还有没有过期的
#             else:
#                 # 同ip下，还有尚未过期的验证码,为sms_code_records_in_ip[0]，60秒内禁止发送
#                 sec = sms_code_records_in_ip[0].sec_to_open()
#                 raise ErrorMod(message=f"调用过于频繁，请{sec}秒后再试。")
